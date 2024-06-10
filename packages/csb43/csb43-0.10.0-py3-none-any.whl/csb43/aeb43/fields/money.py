#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Descriptors for money amount fields
"""

from __future__ import annotations
from typing import (
    Any,
    Iterator,
    Union,
    Callable,
)
import dataclasses
from decimal import Decimal

from ..record import (
    FieldValue,
    Record,
    RegexValidator,
)
from . import (
    Field,
    as_string,
)
from ...utils import b_left_pad
from ...i18n import tr as _


def float2decimal(value: float, decimals: int) -> Decimal:
    "get a scaled decimal from a float value using a limited number of decimals"
    scale = 10 ** decimals
    return Decimal(int(value * scale)) / scale


@dataclasses.dataclass(frozen=True)
class Money(Field[Decimal, Union[Decimal, int]]):
    "money field"
    value_id: Any
    mode_id: Any | None = None
    default_mode: bytes = b"2"
    padding: bytes = b"0"
    non_negative: bool = False
    factory: Callable[[], Decimal] = Decimal

    def default_factory(self) -> Decimal:
        return self.factory()

    def _is_debit(self, this: Record):
        mode = self.default_mode
        if self.mode_id is not None:
            mode = this.get_field(self.mode_id)
        return mode == b"1"

    def to_field(self, this: Record) -> Decimal:
        value = Decimal(as_string(this, self.value_id))
        if self._is_debit(this):
            value = -value
        return value / Decimal(10 ** this.get_context().decimals)

    def _format_amount(self, this: Record, value: Decimal | int) -> bytes:
        amount = f"{abs(int(value * (10 ** this.get_context().decimals)))}"
        max_size = this.manifest.size_for(self.value_id)
        return b_left_pad(amount.encode(this.get_context().encoding), max_size, self.padding)

    def to_bytes(self, this: Record, value: Decimal | int) -> Iterator[FieldValue]:
        yield FieldValue(
            self.value_id,
            self._format_amount(this, value)
        )
        if self.mode_id is None:
            return
        debit_mode = b"1" if value < 0 else b"2"
        yield FieldValue(
            self.mode_id,
            debit_mode
        )

    def adapt(self, this: Record, value: Decimal | int) -> Decimal:
        if isinstance(value, (Decimal, int, str)):
            out = Decimal(value)
        elif isinstance(value, float):
            out = float2decimal(value, this.get_context().decimals)
        else:
            out = Decimal(this.get_context().to_string(value))
        if self.non_negative and out < 0:
            this.get_context().emit_validation_error(_("non-negative values are not allowed"))
        return out


def money_validator(size: int = 14, warning=False) -> RegexValidator:
    "a validator for money amounts"
    pattern = fr"^\d{{{size}}}$"
    return RegexValidator(pattern=pattern.encode("utf-8"), warning=warning)


def money_mode_validator(warning=False) -> RegexValidator:
    "a validator for money amount mode (debit or credit code)"
    return RegexValidator(pattern=br"^[12]$", warning=warning)
