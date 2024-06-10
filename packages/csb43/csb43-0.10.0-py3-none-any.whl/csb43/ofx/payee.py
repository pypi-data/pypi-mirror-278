#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""
OFX Payee structure
"""
from __future__ import annotations
import dataclasses

from deprecated.sphinx import deprecated

from .base import (
    text_to_str,
    OfxObject,
)

@dataclasses.dataclass
class Payee(OfxObject):
    """
    payee info

    Fields
    ------
    name
        `<NAME>`
    payee
        `<PAYEE>`
    extended_name
        `<EXTDNAME>`
    """
    tag_name: str = "payeeid"
    name: str | None = None
    payee: str | None = None
    extended_name: str | None = None

    def _get_content(self) -> str:
        elem = self._elem_f

        str_content = ""

        if self.name:
            str_content += elem("name", text_to_str(self.name))
        else:
            str_content += self._aggr_f("payee", self.payee)
            str_content += elem("extdname", text_to_str(self.extended_name))

        return str_content

    @deprecated(version="0.10.0", reason="use attribute `name`")
    def get_name(self) -> str | None:
        return self.name

    @deprecated(version="0.10.0", reason="use attribute `payee`")
    def get_payee(self) -> str | None:
        return self.payee

    @deprecated(version="0.10.0", reason="use attribute `extended_name`")
    def get_extended_name(self) -> str | None:
        return self.extended_name

    @deprecated(version="0.10.0", reason="use attribute `name`")
    def set_name(self, value: str):
        self.name = value

    @deprecated(version="0.10.0", reason="use attribute `payee`")
    def set_payee(self, value: str):
        self.payee = value

    @deprecated(version="0.10.0", reason="use attribute `extended_name`")
    def set_extended_name(self, value: str):
        self.extended_name = value
