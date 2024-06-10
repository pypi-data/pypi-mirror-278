#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Utils for summaries
"""

from __future__ import annotations
from typing import (
    TypeVar,
    Generic,
)
import dataclasses

from .record import Record
from .record.context import Contextual
from .fields.nested import NestedRecord


# pylint: disable=abstract-method
@dataclasses.dataclass
class ClosingRecord(Record):
    """
    Mix-in class for closing/summary records

    A closing record can be validated.
    """
    _validated: bool = dataclasses.field(repr=False, default=False)

    def set_validated(self, value: bool = True):
        "set this record as validated"
        self._validated = value

    def is_validated(self):
        "return True if this record is already validated"
        return self._validated


ClosingRecordT = TypeVar("ClosingRecordT", bound=ClosingRecord)


class Closeable(Generic[ClosingRecordT]):
    "A composite record that can be closed by a summary record"

    def validate_summary(self, summary: ClosingRecordT) -> None:
        "validate summary against the current content"
        raise NotImplementedError()

    def close(self, summary: ClosingRecordT | None = None) -> None:
        """Close the container with the given record

        If `summary` is not None, validate against the current content
        Otherwise, generate a summary
        """
        if summary:
            self.validate_summary(summary)
        else:
            self._set_new_summary()

    def _set_new_summary(self) -> None:
        "create a summary and set to the associated summary field"
        raise NotImplementedError()

    def is_closed(self) -> bool:
        "return True if the container is closed"
        raise NotImplementedError()

    def describe(self, indent: str = "") -> str:
        "user friendly summary"
        raise NotImplementedError()


@dataclasses.dataclass(frozen=True)
class SummaryField(NestedRecord[ClosingRecordT]):
    "nested field for summary records"

    def _set_value(self, this: Contextual, value):
        if value and isinstance(this, Closeable):
            this.validate_summary(value)
        super()._set_value(this, value)
