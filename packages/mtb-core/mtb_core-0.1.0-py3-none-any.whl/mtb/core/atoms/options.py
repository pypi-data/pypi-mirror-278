#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: options.py
# Project: comfy_mtb
# Author: Mel Massadian
# Copyright (c) 2023 Mel Massadian
#
###
import json
from typing import Any, Callable, Dict, List, Tuple


class Options:
    """
    A class to encapsulate various options as attributes.

    This class provides arbitrary attribute access and manipulation,
    mimicking the behavior of a dictionary.

    Attributes:
        Any attribute can be added during initialization or runtime.

    Example:
        opts = Options(
            center=Vector(0, 0, 0),
            rotation=QtGui.QQuaternion(1, 0, 0, 0)
        )
        opts.distance = 10.0
    """

    def __init__(self, **kwargs):
        """Initializes the options by storing keyword arguments as attributes."""
        self.__dict__.update(kwargs)

    def __str__(self) -> str:
        """Return a string representation."""
        return str(self.__dict__)

    def __repr__(self) -> str:
        """Return the official string representation."""
        return f"Options({self.__dict__})"

    def to_json(self) -> str:
        """Serializes the object to a JSON-formatted string."""
        return json.dumps(self.__dict__)

    def from_json(self, json_str: str):
        """Initializes attributes from a JSON-formatted string."""
        self.__dict__.update(json.loads(json_str))

    def update(self, **kwargs):
        """Updates multiple attributes at once."""
        self.__dict__.update(kwargs)

    def keys(self) -> List[str]:
        """Returns a list of all attribute names."""
        return list(self.__dict__.keys())

    def values(self) -> List[Any]:
        """Returns a list of all attribute values."""
        return list(self.__dict__.values())

    def items(self) -> List[Tuple[str, Any]]:
        """Returns a list of all (key, value) pairs."""
        return list(self.__dict__.items())

    def __len__(self) -> int:
        """Returns the number of attributes."""
        return len(self.__dict__)

    def __contains__(self, key: str) -> bool:
        """Check if key exists."""
        return self.has_key(key)

    def has_key(self, key: str) -> bool:
        """Checks if a certain key exists."""
        return key in self.__dict__

    def clear(self):
        """Removes all attributes, resetting the object to an empty state."""
        self.__dict__.clear()

    def filter(self, prefix: str) -> Dict[str, Any]:
        """Returns a dictionary of attributes that have keys starting with a given prefix."""
        return {k: v for k, v in self.__dict__.items() if k.startswith(prefix)}

    def equals(self, other) -> bool:
        """Checks if this object is equal to another Options object."""
        return self.__dict__ == other.__dict__

    def merge(self, other):
        """Merges attributes from another Options object."""
        self.__dict__.update(other.__dict__)

    def transform(self, func: Callable[[Any], Any]):
        """Applies a function to all attribute values."""
        for key, value in self.__dict__.items():
            self.__dict__[key] = func(value)

    def __getattr__(self, key):
        """Gets the value of the specified attribute."""
        return self.__dict__.get(key)

    def __setattr__(self, key, value):
        """Sets the value of the specified attribute."""
        self.__dict__[key] = value
