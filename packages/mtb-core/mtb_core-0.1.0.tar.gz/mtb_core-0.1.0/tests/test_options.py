#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: test_options.py
# Project: comfy_mtb
# Author: Mel Massadian
# Copyright (c) 2023 Mel Massadian
#
###
import pytest

from mtb.core.atoms.options import Options  # replace 'your_module' with the actual module name


def test_options_initialization():
    opts = Options(a=1, b=2, c="three")
    assert opts.a == 1
    assert opts.b == 2
    assert opts.c == "three"


def test_options_string_representation():
    opts = Options(x=10, y=20)
    assert str(opts) == "{'x': 10, 'y': 20}"


def test_options_repr():
    opts = Options(x=10, y=20)
    assert repr(opts) == "Options({'x': 10, 'y': 20})"


def test_options_to_from_json():
    opts = Options(x=1, y=2)
    json_str = opts.to_json()
    new_opts = Options()
    new_opts.from_json(json_str)
    assert opts.equals(new_opts)


def test_options_update():
    opts = Options()
    opts.update(a=1, b=2)
    assert opts.a == 1 and opts.b == 2


def test_options_keys_values_items():
    opts = Options(a=1, b=2)
    assert opts.keys() == ["a", "b"]
    assert opts.values() == [1, 2]
    assert opts.items() == [("a", 1), ("b", 2)]


def test_options_len():
    opts = Options(a=1, b=2)
    assert len(opts) == 2


def test_options_contains():
    opts = Options(a=1)
    assert "a" in opts
    assert not "b" in opts


def test_options_has_key():
    opts = Options(a=1)
    assert opts.has_key("a")
    assert not opts.has_key("b")


def test_options_clear():
    opts = Options(a=1, b=2)
    opts.clear()
    assert len(opts) == 0


def test_options_filter():
    opts = Options(cat=1, car=2, dog=3)
    assert opts.filter("ca") == {"cat": 1, "car": 2}


def test_options_equals():
    opts1 = Options(a=1, b=2)
    opts2 = Options(a=1, b=2)
    assert opts1.equals(opts2)


def test_options_merge():
    opts1 = Options(a=1)
    opts2 = Options(b=2)
    opts1.merge(opts2)
    assert opts1.a == 1 and opts1.b == 2


def test_options_transform():
    opts = Options(a=1, b=2)
    opts.transform(lambda x: x * 2)
    assert opts.a == 2 and opts.b == 4


def test_options_missing_attribute_returns_none():
    opts = Options()
    assert opts.missing_attribute is None


def test_options_getattr_setattr():
    opts = Options()
    opts.a = 1
    assert opts.a == 1
    assert opts.b is None


def test_options_contains():
    opts = Options(a=1)
    assert ("a" in opts) == True
    assert ("b" in opts) == False


def test_options_filter():
    opts = Options(a=1, b=2, c_apple=3, c_banana=4)
    filtered = opts.filter("c_")
    assert filtered == {"c_apple": 3, "c_banana": 4}


def test_options_merge():
    opts1 = Options(a=1)
    opts2 = Options(b=2)
    opts1.merge(opts2)
    assert opts1.a == 1
    assert opts1.b == 2


def test_options_transform():
    opts = Options(a=1, b=2)
    opts.transform(lambda x: x * 2)
    assert opts.a == 2
    assert opts.b == 4
