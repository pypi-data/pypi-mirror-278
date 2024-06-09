#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: cli_tools.py
# Project: comfy_mtb
# Author: Mel Massadian
# Copyright (c) 2023 Mel Massadian
#
###

from contextlib import contextmanager

import keyboard
from rich.box import MINIMAL as box
from rich.console import Console
from rich.live import Live
from rich.prompt import InvalidResponse, PromptBase
from rich.style import Style
from rich.table import Table

SELECTED = Style(color="blue", bgcolor="white", bold=True)
from pathlib import Path


class PathPrompt(PromptBase[Path]):
    """A prompt that returns a pathlib Path.

    Example:
        >>> my_path = PathPrompt.ask("Where should we save the file?")

    """

    response_type = Path
    validate_error_message = "[prompt.invalid]Please enter a valid path"

    def process_response(self, value: str) -> bool:
        """Convert str to Path and check existance."""
        value = Path(value.strip())
        if not value.exists():
            raise InvalidResponse(self.validate_error_message)
        return value


def _generate_table(console, headers, items, selected) -> Table:
    table = Table(box=box)
    for h in headers:
        table.add_column(h)

    size = console.height - 4
    rows = items
    if len(items) + 3 > size:
        if selected < size / 2:
            rows = rows[:size]
        elif selected + size / 2 > len(items):
            rows = rows[-size:]
            selected -= len(items) - size
        else:
            rows = rows[selected - size // 2 : selected + size // 2]
            selected -= selected - size // 2

    for i, row in enumerate(rows):
        table.add_row(*row, style=SELECTED if i == selected else None)
    return table


def _return_selected(live: Live, selected):
    live.stop()
    print(selected)
    exit(0)


def select_table(console, headers, items, custom_actions=None):
    selected = -1
    selected_item = None
    if custom_actions is None:
        # custom_actions = {28: lambda l: _return_selected(l, selected)}
        custom_actions = {}
    with Live(
        _generate_table(console, headers, items, selected),
        auto_refresh=False,
        screen=True,
    ) as live:
        try:
            while True:
                key_event = keyboard.read_event(suppress=True)
                if key_event.event_type == keyboard.KEY_DOWN:
                    action = custom_actions.get(key_event.scan_code)
                    if action:
                        action(live)

                    if key_event.scan_code == 72:  # up
                        selected = max(0, selected - 1)
                    elif key_event.scan_code == 80:  # down
                        selected = min(len(items) - 1, selected + 1)

                    elif key_event.scan_code == 28:  # enter
                        selected_item = items[selected]

                        console.print(f"Getting {selected} from {items}: {selected_item}")

                        break
                    # Add your additional key logic here.

                    live.update(
                        _generate_table(console, headers, items, selected),
                        refresh=True,
                    )
        finally:
            return selected_item


# region parsers


def add_argument_with_default(parser, *args, **kwargs):
    default = kwargs.get("default")
    if default is not None:
        kwargs["help"] = f"{kwargs.get('help', '')} (default: {default})"
    parser.add_argument(*args, **kwargs)


# endregion

__all__ = ["add_argument_with_default", "select_table", "PathPrompt"]
