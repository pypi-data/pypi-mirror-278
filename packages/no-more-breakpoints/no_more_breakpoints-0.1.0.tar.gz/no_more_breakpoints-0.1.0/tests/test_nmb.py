from pathlib import Path

import pytest

from no_more_breakpoints import validate_file


@pytest.mark.parametrize(
    "file, expected_success",
    [
        ("with_breakpoint.py", False),
        ("without_breakpoint.py", True),
    ],
)
def test_validate(file, expected_success):
    path = Path(__file__).parent / file
    print(path)
    if expected_success:
        validate_file(path)
    else:
        with pytest.raises(ValueError):
            validate_file(path)
