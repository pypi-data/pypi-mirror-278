#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Descriptor for string fields
"""
from __future__ import annotations
from typing import (
    Any,
    Iterator,
    Callable,
    Mapping,
)
from types import MappingProxyType
import dataclasses
import enum

from ..record import (
    FieldValue,
    Record,
    RegexValidator,
    AnyStr,
)
from ..record.context import InformationMode
from . import Field

from ...utils import (
    b_left_pad,
    b_right_pad,
)


class Trim(enum.IntFlag):
    "trim mode"
    NONE = 0
    LEFT_PAD = enum.auto()
    LEFT_BLANK = enum.auto()
    RIGHT_PAD = enum.auto()
    RIGHT_BLANK = enum.auto()
    LEFT = LEFT_PAD | LEFT_BLANK
    RIGHT = RIGHT_PAD | RIGHT_BLANK
    BOTH_PAD = LEFT_PAD | RIGHT_PAD
    BOTH_BLANK = LEFT_BLANK | RIGHT_BLANK
    BOTH = BOTH_PAD | BOTH_BLANK


@dataclasses.dataclass(frozen=True, unsafe_hash=True)
class String(Field[str, str]):
    "string field"
    field_id: Any
    # padding character used in the raw field
    padding: bytes = b" "
    # trim padding characters before returning the string value
    trim: Trim = Trim.BOTH
    # align value at the left of the field (default: right)
    align_left: bool = True
    mode: Mapping[InformationMode, Mapping[str, Any]] = dataclasses.field(
        default_factory=lambda: MappingProxyType({})
    )
    factory: Callable[[], str] = str

    def default_factory(self) -> str:
        return self.factory()

    def to_field(self, this: Record) -> str:
        value = this.get_field(self.field_id)
        value = self._trim(this, value)
        return value.decode(this.get_context().encoding)

    def _trim(self, this: Record, value: AnyStr) -> AnyStr:
        trim = self.get_trim(this)
        if trim == Trim.NONE:
            return value

        b_padding = self.get_padding(this)
        if not isinstance(value, (bytes, bytearray)):
            padding = b_padding.decode(this.get_context().encoding)
        else:
            padding = b_padding

        if Trim.LEFT_PAD in trim:
            value = value.lstrip(padding)
        if Trim.RIGHT_PAD in trim:
            value = value.rstrip(padding)
        if Trim.LEFT_BLANK in trim:
            value = value.lstrip()
        if Trim.RIGHT_BLANK in trim:
            value = value.rstrip()
        return value

    def pad(self, this: Record, record: bytes) -> FieldValue:
        "pad a record"
        max_size = this.manifest.size_for(self.field_id)
        padding = self.get_padding(this)
        if self.get_align_left(this):
            record = b_right_pad(record, max_size, padding)
        else:
            record = b_left_pad(record, max_size, padding)
        return FieldValue(self.field_id, record)

    def to_bytes(self, this: Record, value: str) -> Iterator[FieldValue]:
        record = value.encode(this.get_context().encoding)
        yield self.pad(this, record)

    def adapt(self, this: Record, value: str) -> str:
        return self._trim(this, this.get_context().to_string(value))

    def _current_mode(self, this: Record) -> Mapping[str, Any]:
        return self.mode.get(this.get_context().information_mode, {})

    def get_padding(self, this: Record) -> bytes:
        "padding for the current information mode"
        return self._current_mode(this).get("padding", self.padding)

    def get_align_left(self, this: Record) -> bool:
        "trim_left for the current information mode"
        return self._current_mode(this).get("align_left", self.align_left)

    def get_trim(self, this: Record) -> Trim:
        "trimmed for the current information mode"
        return self._current_mode(this).get("trim", self.trim)


def string_validator(size: int, warning=False) -> RegexValidator:
    "a validator for strings with printable characters"
    pattern = fr'^[\x20-\xFF]{{{size}}}$'
    return RegexValidator(pattern=pattern.encode("utf-8"), warning=warning)
