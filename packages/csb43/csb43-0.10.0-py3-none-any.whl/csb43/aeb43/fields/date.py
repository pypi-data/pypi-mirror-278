#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Descriptor for date fields
"""
from __future__ import annotations
from typing import (
    Any,
    Iterator,
    Union,
    Callable,
)
import dataclasses
from datetime import date, datetime

from ..record import (
    FieldValue,
    Record,
    RegexValidator,
)
from . import (
    Field,
    as_string,
)
from ...i18n import tr as _


@dataclasses.dataclass(frozen=True)
class Date(Field[date, Union[date, datetime]]):
    "date field"
    field_id: Any
    factory: Callable[[], date] = date.today

    def default_factory(self) -> date:
        return self.factory()

    def _template(self, this: Record, short: bool) -> str:
        "get the date format template"
        if short:
            if this.get_context().year_first:
                return "%y%m%d"
            return "%d%m%y"
        if this.get_context().year_first:
            return "%Y%m%d"
        return "%d%m%Y"

    def _str2date(self, this: Record, value: str) -> date:
        value = value.replace("/", "").replace("-", "").replace(" ", "").strip()
        size = len(value)
        if size not in (6, 8):
            raise this.get_context().new_validation_error(_("invalid date format: {value}").format(
                value=value
            ))
        return datetime.strptime(value, self._template(this, size <= 6)).date()

    def to_field(self, this: Record) -> date:
        value = as_string(this, self.field_id)
        return self._str2date(this, value)

    def to_bytes(self, this: Record, value: Union[date, datetime]) -> Iterator[FieldValue]:
        record = value.strftime(self._template(this, True)).encode(this.get_context().encoding)
        yield FieldValue(self.field_id, record)

    def adapt(self, this: Record, value: date | datetime) -> date:
        if not isinstance(value, (date, datetime)):
            return self._str2date(this, this.get_context().to_string(value))
        return value


def date_validator(warning=False) -> RegexValidator:
    "a standard date validator"
    return RegexValidator(pattern=br"^\d{6}$", warning=warning)
