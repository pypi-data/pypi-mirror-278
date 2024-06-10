#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
functions for tabulated strings manipulation
"""

from __future__ import annotations
from collections import defaultdict
from typing import Sequence, Iterator


def adjust_table_width(
    data: Sequence[str],
    delim="||",
    gap=1,
    indent=0
) -> Iterator[str]:
    "adjust width for columns marked by `sep`"
    width: dict[int, int] = defaultdict(lambda: 0)

    table = []
    for line in data:
        cols = line.split(delim)
        table.append(cols)
        for idx_c, col in enumerate(cols):
            width[idx_c] = max(len(col) + gap, width[idx_c])

    for cols in table:
        new_line = []
        if indent:
            new_line.append(" " * indent)
        for idx_c, col in enumerate(cols):
            new_line.append(col)
            pad = width[idx_c] - len(col)
            if pad:
                new_line.append(" " * pad)
        yield "".join(new_line)
