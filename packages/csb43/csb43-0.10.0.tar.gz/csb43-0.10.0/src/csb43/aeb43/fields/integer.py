#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Descriptors for representing int fields
"""

from __future__ import annotations
from typing import (
    Any,
    Iterator,
    Callable,
    Pattern,
)
import dataclasses
from numbers import Number
import re

from ...i18n import tr as _
from ..record import (
    FieldValue,
    Record,
    AnyBytes,
)
from . import Field, as_string

from ...utils import b_left_pad


@dataclasses.dataclass(frozen=True)
class Integer(Field[int, int]):
    "integer field"
    field_id: Any
    factory: Callable[[], int] = int

    def default_factory(self) -> int:
        return self.factory()

    def to_field(self, this: Record) -> int:
        return int(as_string(this, self.field_id))

    def to_bytes(self, this: Record, value: int) -> Iterator[FieldValue]:
        record = f"{value:d}".encode(this.get_context().encoding)
        max_size = this.manifest.size_for(self.field_id)
        record = b_left_pad(record, max_size, b"0")
        yield FieldValue(self.field_id, record)

    def adapt(self, this: Record, value: int) -> int:
        if isinstance(value, Number):
            return int(value)
        return int(this.get_context().to_string(value))


@dataclasses.dataclass
class IntegerValidator:
    """
    Validator for integer fields

    Attributes:
        size
            number of digits (base 10)
        min_value
            minimum allowed value
        max_value
            maximum allowed value
        warning
            emit warning if validation fails instead of auto
    """
    size: int
    min_value: int | None = None
    max_value: int | None = None
    warning: bool = False
    regex: Pattern[bytes] = dataclasses.field(init=False)

    def __post_init__(self):
        pattern = fr"^\d{{{self.size}}}$"
        self.regex = re.compile(pattern.encode("latin1"))

    def _as_string(self) -> str:
        out = f"r{repr(self.regex.pattern)}"
        if self.min_value is not None:
            out = f"{self.min_value} <= {out}"
        if self.max_value is not None:
            out = f"{out} <= {self.max_value}"
        return out

    def __call__(self, _context, field: AnyBytes) -> tuple[str | None, str | None]:
        match_ = self.regex.match(field)
        valid = match_ is not None
        message: str | None = None
        if valid:
            value = int(field.decode("latin1"))
            if self.min_value is not None:
                valid = self.min_value <= value
            if self.max_value is not None:
                valid = valid and (value <= self.max_value)
        if not valid:
            message = _(
                "Bad format: content {content!r} mismatches the "
                "expected format {value} for this field"
            ).format(content=field, value=self._as_string())

        if self.warning:
            return None, message
        return message, None
