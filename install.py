import itertools
import sys
import json
import os
from pathlib import Path
from subprocess import run, DEVNULL, PIPE
import re
import tempfile
from urllib import request
import shutil
from collections import namedtuple
from typing import Union
import argparse

# The "latest" release is ambiguous because there are several programs
# each with their own versions but generally I'm defining it as the
# release with the latest version of gcc.
# I'm hard coding this tag in for now. Maybe I'll automate this if it
# seems like a good idea in the future.
LATEST = "12.2.0-14.0.6-10.0.0-msvcrt-r1"

Asset = namedtuple("ReleaseAsset", ["name", "url"])


def api(path):
    """Pull a json from Github's API."""
    BASE = "https://api.github.com/repos/brechtsanders/winlibs_mingw"
    url = '/'.join((BASE, path.strip("/")))
    with request.urlopen(url) as req:
        return json.load(req)


def releases(per_page=100):
    """Get all releases by tag and their release files' urls."""
    out = {}
    for i in itertools.count():
        page = api(f"releases?page={i};per_page={per_page}")
        out.update((r["tag_name"], r["assets"]) for r in page)
        if len(page) < per_page:
            break
    return out


def release(tag):
    """Get a specific tagged release. Raise an error if the tag doesn't exist.
    """
    _releases = releases()
    if tag in _releases:
        return _releases[tag]
    raise ValueError(
        f"The tag '{tag}' does not exist. Possible tags are:\n  " +
        "\n  ".join(_releases))


def deserialise_config(serialised):
    config = json.loads(serialised)

    # Booleans come out as strings for some reason.
    # Turn them back into proper booleans.
    for key in ["with_clang", "add_to_path"]:
        if isinstance(config[key], str):
            config[key] = json.loads(config[key])

    if config["tag"].lower() == "latest":
        config["tag"] = LATEST

    return config


architecture_aliases = {
    "x86_64": [64, "64", "x64", "x86_64", "amd64"],
    "i686": [32, "32", "x86", "i686"],
}


def normalise_architecture(architecture: Union[str, int]):
    """Convert any valid architecture alias to either 'x86_64' or 'i686'.
    Raise an error for invalid input.
    """
    for (true_name, aliases) in architecture_aliases.items():
        if architecture in aliases:
            return true_name
        elif isinstance(architecture, str) and architecture.lower() in aliases:
            return true_name
    raise ValueError(
        f"Invalid architecture {repr(architecture)}. "
        f"Legal 64 bit values are:\n    {architecture_aliases['x86_64']}\n"
        f"And legal 32 bit values are:\n    {architecture_aliases['i686']}\n"
    )


def release_assets(_release: list):
    """List all downloadable files in a given github release."""
    return [
        Asset(asset["name"], asset["browser_download_url"])
        for asset in _release if asset["name"].endswith(".7z")
    ]


def pull(asset: Asset, dest: str) -> Path:
    """Download a single file from a github release."""
    dest = Path(dest, asset.name)
    with request.urlopen(asset.url) as req:
        with dest.open("wb") as f:
            shutil.copyfileobj(req, f)
    return dest


def unpack(archive, dest) -> Path:
    Path(dest).mkdir(parents=True, exist_ok=True)

    # Using this apparently redundant shutil.which() is a hack to respect PATHEX
    # so that 7z.bat shims are recognised.
    run([shutil.which("7z"), "x", "-y", "-o" + str(dest),
         str(archive)],
        stdout=DEVNULL,
        check=True)
    location = Path(dest) / archive_top_level(archive)
    assert location.is_dir(), f"{location} not in {os.listdir(dest)}"
    return location


def archive_top_level(archive):
    """Find the name of the top level folder in a 7z archive."""
    p = run([shutil.which("7z"), "l", "-ba", "-slt",
             str(archive)],
            stdout=PIPE,
            check=True,
            universal_newlines=True)
    return min(re.findall("Path = (.*)", p.stdout), key=len)


def set_output(key, value):
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write("{}={}\n".format(key, value))


def prepend_to_path(path):
    """Persistently prepend a directory to the PATH environment variable."""
    import winreg

    path = str(path)
    _key = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    RW = winreg.KEY_READ | winreg.KEY_WRITE

    # If on GitHub Actions, registers are ignored in favour of a temporary file
    # whose location is stored in GITHUB_PATH. This needs to be handled outside
    # of Python.
    if os.environ.get("GITHUB_PATH"):
        with open(os.environ["GITHUB_PATH"], "a") as f:
            f.write(path + "\n")
        return

    # Try to write to the system-wide PATH.
    try:
        environment = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, _key, 0, RW)
    except PermissionError:
        # If we lack permission, get the current user's SID and write to that
        # SID's PATH instead.
        p = run(["whoami", "/USER", "/FO", "CSV", "/NH"], stdout=PIPE)
        sid = re.match(rb'"[^"]+", *"([^"]+)"', p.stdout)[1].decode("ascii")
        _key = os.path.join(sid, "Environment")
        environment = winreg.OpenKey(winreg.HKEY_USERS, _key, 0, RW)

    with environment:
        old, type = winreg.QueryValueEx(environment, "Path")
        old = (i for i in old.split(os.pathsep) if i != path)
        new = os.pathsep.join([path, *old])
        winreg.SetValueEx(environment, "Path", 0, type, new)


def select_asset(assets, with_clang, architecture):
    """Filter a list of download options for the one with the chosen
    architecture and desired presence or absence of clang/LLVM.
    """
    asset: Asset
    for asset in assets:
        if with_clang != ("llvm" in asset.name.lower()):
            continue
        if architecture not in asset.name:
            continue
        return asset
    raise ValueError("No {} {} clang found out of:\n{}\n".format(
        architecture, 'with' if with_clang else 'without',
        '\n'.join(i.name for i in assets)))


def install(tag: str, with_clang: bool, destination: str, add_to_path: bool,
            architecture: str):
    """Select, download and install a WinLibs build."""

    tag = tag or LATEST
    architecture = normalise_architecture(architecture or "x86_64")
    destination = Path(destination or os.environ["localappdata"]).resolve()

    # Find which files are available.
    assets = release_assets(release(tag))
    # Select the one we want.
    asset = select_asset(assets, with_clang, architecture)

    with tempfile.TemporaryDirectory() as temp:
        # Download it.
        archive = pull(asset, temp)
        # Unzip it.
        mingw32_dir = unpack(archive, destination)

    if add_to_path:
        prepend_to_path(mingw32_dir / "bin")

    # Make notes of where the key folders are.
    set_output("root", mingw32_dir)
    set_output("bin", mingw32_dir / "bin")


def main(args=None):
    p = argparse.ArgumentParser()
    p.add_argument("--config", help="Raw JSON containing all configuration")
    p.add_argument("--tag")
    p.add_argument("--with-clang", action="store_true")
    p.add_argument("--add-to-path", action="store_true")
    p.add_argument("--destination")
    p.add_argument("--architecture")
    arguments = vars(p.parse_args(args))
    config = arguments.pop("config")
    if config is not None:
        install(**deserialise_config(config))
    else:
        install(**arguments)


if __name__ == "__main__":
    main()
