import sys
import json
import re
import os
from pathlib import Path
from subprocess import run, PIPE, DEVNULL
import tempfile

# The "latest" release is ambiguous because there are several programs
# each with their own versions but generally I'm defining it as the
# release with the latest version of gcc.
# I'm hard coding this tag in for now. Maybe I'll automate this if it
# seems like a good idea in the future.
LATEST = "11.1.0-12.0.0-9.0.0-r1"


def deserialise_config(serialised):
    config = json.loads(serialised)

    # Booleans come out as strings for some reason.
    # Turn them back into proper booleans.
    for key in ["with_clang", "add_to_path"]:
        if isinstance(config[key], str):
            config[key] = json.loads(config[key])

    # Normalise architectures to their full names.
    # Again be wary of strings which should be integers.
    if config["architecture"] in (64, "64"):
        config["architecture"] = "x86_64"
    elif config["architecture"] in (32, "32"):
        config["architecture"] = "i686"

    config["destination"] = Path(config.get("destination", '') or
                                 os.environ["localappdata"]).resolve()

    return config


def _release_assets(stdout: str):
    return re.findall(r"^asset:\t(.*\.7z)$", stdout.split("\n--\n")[0], re.M)


def release_assets(tag: str):
    """List all downloadable files in a given github release."""
    p = run(
        ["gh", "release", "--repo=brechtsanders/winlibs_mingw", "view", tag],
        stdout=PIPE, universal_newlines=True, check=True)
    return _release_assets(p.stdout)


def pull(tag: str, asset: str, dest: str) -> Path:
    """Download a single file from a github release."""
    run(["gh", "release", "--repo=brechtsanders/winlibs_mingw", "download",
         "--pattern", asset, "--dir", dest, tag],
        check=True, stdout=DEVNULL)
    return Path(dest, asset)


def unpack(archive, dest) -> Path:
    run(["7z", "x", "-y", "-o" + str(dest),
         str(archive)],
        stdout=DEVNULL,
        check=True)
    location = Path(dest) / "mingw32"
    assert location.is_dir()
    return location


def set_output(key, value):
    # https://docs.github.com/en/actions/reference/workflow-commands-for-github-actions#setting-an-environment-variable
    print("::set-output ", key, "=", str(value), sep="")


def select_asset(assets, with_clang, architecture):
    """Filter a list of download options for the one with the chosen
    architecture and desired presence or absence of clang/LLVM.
    """
    for asset in assets:
        if with_clang != ("llvm" in asset.lower()):
            continue
        if architecture not in asset:
            continue
        return asset
    raise ValueError("No {} {} clang found out of:\n{}\n".format(
        architecture, 'with' if with_clang else 'without', '\n'.join(assets)))


def install(tag: str, with_clang: bool, destination: str, add_to_path: bool,
            architecture: str):
    """Select, download and install a WinLibs build."""

    # Find which files are available.
    assets = release_assets(tag)
    # Select the one we want.
    asset = select_asset(assets, with_clang, architecture)

    with tempfile.TemporaryDirectory() as temp:
        # Download it.
        archive = pull(tag, asset, temp)
        # Unzip it.
        mingw32_dir = unpack(archive, destination)

    # Make notes of where the key folders are.
    set_output("root", mingw32_dir)
    set_output("bin", mingw32_dir / "bin")


if __name__ == "__main__":
    config = deserialise_config(sys.argv[1])
    install(**config)
