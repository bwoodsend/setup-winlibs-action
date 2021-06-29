import sys
from pathlib import Path
import pytest

HERE = Path(__file__, "..").resolve()
ROOT = HERE.parent

# Ensure that scripts in the root of this repo are importable.
sys.path.insert(0, str(ROOT))

import select_version


def test_normalise_architecture():
    """Test converting user input architectures to internal ones."""

    assert select_version.normalise_architecture("x86_64") == "x86_64"
    assert select_version.normalise_architecture("i686") == "i686"
    assert select_version.normalise_architecture(32) == "i686"
    assert select_version.normalise_architecture("64") == "x86_64"

    with pytest.raises(ValueError, match=_error_pattern):
        select_version.normalise_architecture("62")
    with pytest.raises(ValueError, match=r" 99\."):
        select_version.normalise_architecture(99)


_error_pattern = r"""
Invalid architecture '62'\. Legal .* are:
    \[.*\]
And .* are:
    \[.*\]
""".strip()
