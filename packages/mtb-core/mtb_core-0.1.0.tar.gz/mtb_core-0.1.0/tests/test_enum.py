import pytest
from mtb.core.enum import StringConvertibleEnum


class Precision(StringConvertibleEnum):
    FULL = "full"
    FP32 = "fp32"
    FP16 = "fp16"
    BF16 = "bf16"
    FP8 = "fp8"


class Operation(StringConvertibleEnum):
    COPY = "copy"
    CONVERT = "convert"
    DELETE = "delete"


def test_from_str():
    assert Precision.from_str("full") == Precision.FULL
    assert Precision.from_str("fp32") == Precision.FP32
    assert Operation.from_str("copy") == Operation.COPY
    with pytest.raises(ValueError):
        Precision.from_str("unknown")


def test_to_str():
    assert Precision.to_str(Precision.FP16) == "fp16"
    assert Operation.to_str(Operation.DELETE) == "delete"
    with pytest.raises(ValueError):
        Precision.to_str("invalid_enum")


def test_list_members():
    assert Precision.list_members() == ["full", "fp32", "fp16", "bf16", "fp8"]
    assert Operation.list_members() == ["copy", "convert", "delete"]


def test_str():
    assert str(Precision.FP16) == "fp16"
    assert str(Operation.CONVERT) == "convert"


if __name__ == "__main__":
    pytest.main()
