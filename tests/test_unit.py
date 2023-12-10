import sys
from pathlib import Path
import os

import pytest

HERE = Path(__file__, "..").resolve()
ROOT = HERE.parent

# Ensure that scripts in the root of this repo are importable.
sys.path.insert(0, str(ROOT))

import install


def test_normalise_architecture():
    """Test converting user input architectures to internal ones."""

    assert install.normalise_architecture("x86_64") == "x86_64"
    assert install.normalise_architecture("i686") == "i686"
    assert install.normalise_architecture(32) == "i686"
    assert install.normalise_architecture("64") == "x86_64"
    assert install.normalise_architecture("AMD64") == "x86_64"
    assert install.normalise_architecture("X86") == "i686"

    with pytest.raises(ValueError, match=_error_pattern):
        install.normalise_architecture("62")
    with pytest.raises(ValueError, match=r" 99\."):
        install.normalise_architecture(99)


_error_pattern = r"""
Invalid architecture '62'\. Legal .* are:
    \[.*\]
And .* are:
    \[.*\]
""".strip()


def test_paginated_releases():
    """Test the paginated release searching will still work when the number of
    WinLibs releases available exceeds the page size.
    """
    assert len(list(install.tags(os.environ.get("token"), per_page=25))) > 30


def test_tag_sort():
    assert install.latest([
        "9.2.0-7.0.0",
        "9.2.0-7.0.0-r4",
        "1.2.0-16.0.6-11.0.0-msvcrt-r1",
    ]) == "1.2.0-16.0.6-11.0.0-msvcrt-r1"

    assert install.latest([
        "12.0.1-snapshot20220123-9.0.0-msvcrt-r1",
        "11.3.0-14.0.1-10.0.0-msvcrt-r2",
        "12.0.0-snapshot20211205-9.0.0-msvcrt-r1",
        "14.0.0-snapshot20231119posix-11.0.1-msvcrt-r1",
    ]) == "11.3.0-14.0.1-10.0.0-msvcrt-r2"

    assert install.latest([
        "13.1.0posix-16.0.3-11.0.0-ucrt-r1",
        "13.1.0posix-16.0.3-11.0.0-msvcrt-r1",
        "13.1.0-16.0.5-11.0.0-ucrt-r5",
        "13.1.0-16.0.5-11.0.0-msvcrt-r5",
    ]) == "13.1.0-16.0.5-11.0.0-msvcrt-r5"

    assert install.latest([
        "13.1.2posix-16.0.3-11.0.0-ucrt-r1",
        "13.1.1posix-16.0.3-11.0.0-msvcrt-r1",
        "13.1.0-16.0.5-11.0.0-ucrt-r5",
        "13.2.0mcf-16.0.6-11.0.0-ucrt-r1",
        "13.1.0-16.0.5-11.0.0-msvcrt-r5",
    ]) == "13.1.1posix-16.0.3-11.0.0-msvcrt-r1"

    assert install.latest([
        "llvm10.0.1-7.0.0-r0",
        "14.0.0-snapshot20231119posix-11.0.1-msvcrt-r1",
        "13.2.0posix-17.0.5-11.0.1-ucrt-r3",
        "13.2.0mcf-16.0.6-11.0.1-ucrt-r2",
        "13.2.0mcf-11.0.1-ucrt-r3",
        "13.1.0-11.0.0-ucrt-r5",
        "13.1.0-11.0.0-ucrt-r4b",
        "13.1.0-11.0.0-msvcrt-r5",
        "13.1.0-11.0.0-msvcrt-r4b",
        "13.0.0-snapshot20221030-10.0.0-msvcrt-r1posix",
        "13.0.0-snapshot20221030-10.0.0-msvcrt-r1mcf",
        "10.2.0-11.0.0-8.0.0-r4nvptx",
        "0.3-0.1-0.0.0-msvcrt-r27897",
    ]) == "0.3-0.1-0.0.0-msvcrt-r27897"
