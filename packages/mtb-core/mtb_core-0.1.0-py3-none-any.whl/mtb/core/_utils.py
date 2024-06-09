#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: _utils.py
# Project: comfy_mtb
# Author: Mel Massadian
# Copyright (c) 2023 Mel Massadian
#
###
def print_dir(obj, use_dict=False):
    """
    Returns the values of the given object's __dict__ attribute.
    """
    if use_dict:
        for key, value in obj.__dict__.items():
            print(f"{key}: {value}")
    else:
        for key in dir(obj):
            print(f"{key}: {getattr(obj, key)}")
