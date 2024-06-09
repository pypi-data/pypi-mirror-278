import pytest

from mtb.core.naming import abbreviate_name, sanitize_name, unique_name


# Test sanitize_name function
def test_sanitize_name():
    assert sanitize_name("My@Name!") == "My_Name"
    assert sanitize_name("AlreadyGood123") == "AlreadyGood123"
    assert sanitize_name("Bad$Char^") == "Bad_Char"
    assert sanitize_name("With Space ") == "With_Space"


# Test abbreviate_name function
def test_abbreviate_name():
    assert abbreviate_name("LongName", 4, "..") == "Lo.."
    assert abbreviate_name("Short", 10) == "Short"
    assert abbreviate_name("ExactSize", 9) == "ExactSize"

    with pytest.raises(ValueError):
        abbreviate_name("Name", 1, "...")


# Test unique_name function
def test_unique_name():
    name1 = unique_name("prefix_")
    name2 = unique_name("prefix_")

    assert name1 != name2
    assert name1.startswith("prefix_")
    assert name2.startswith("prefix_")
