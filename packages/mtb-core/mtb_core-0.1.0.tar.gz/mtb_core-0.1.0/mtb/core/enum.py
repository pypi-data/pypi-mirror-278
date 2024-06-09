from enum import Enum
from typing import TypeVar

T = TypeVar("T", bound="StringConvertibleEnum")


class StringConvertibleEnum(Enum):
    """Base class for enums with utility methods for string conversion and member listing."""

    @classmethod
    def from_str(cls: type[T], label: str | T) -> T:
        """
        Convert a string to the corresponding enum value (case sensitive).

        Args:
            label (Union[str, T]): The string or enum value to convert.

        Returns
        -------
            T: The corresponding enum value.

        Raises
        ------
            ValueError: If the label does not correspond to any enum member.
        """
        if isinstance(label, cls):
            return label
        if isinstance(label, str):
            # from key
            if label in cls.__members__:
                return cls[label]

            for member in cls:
                if member.value == label:
                    return member

        raise ValueError(
            f"Unknown label: '{label}'. Valid members: {list(cls.__members__.keys())}, "
            f"valid values: {cls.list_members()}"
        )

    @classmethod
    def to_str(cls: type[T], enum_value: T) -> str:
        """
        Convert an enum value to its string representation.

        Args:
            enum_value (T): The enum value to convert.

        Returns
        -------
            str: The string representation of the enum value.

        Raises
        ------
            ValueError: If the enum value is invalid.
        """
        if isinstance(enum_value, cls):
            return enum_value.value
        raise ValueError(f"Invalid Enum: {enum_value}")

    @classmethod
    def list_members(cls: type[T]) -> list[str]:
        """
        Return a list of string representations of all enum members.

        Returns
        -------
            List[str]: List of all enum member values.
        """
        return [enum.value for enum in cls]

    def __str__(self) -> str:
        """
        Returns the string representation of the enum value.

        Returns
        -------
            str: The string representation of the enum value.
        """
        return self.value
