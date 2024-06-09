"""
Tests for mtb-core
"""

import pytest

from mtb.core.format import human_readable_size


@pytest.mark.parametrize(
    "size_bytes, expected",
    [(1024, "1.00 KB"), (1.573e7, "15.00 MB")],
)
def test_human_readable(size_bytes, expected):
    """Various test case for the humand readable function."""
    assert human_readable_size(size_bytes) == expected


# - These are just reminders I might need
def test_example_float_approx():
    assert 0.1 + 0.2 == pytest.approx(0.3)


def test_example_error():
    with pytest.raises(ValueError):
        int("string")
