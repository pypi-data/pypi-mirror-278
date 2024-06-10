#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Descriptors for storing nested records
"""

from __future__ import annotations
from typing import (
    Type,
    TypeVar,
    Iterable,
    Callable,
    Union,
    Sequence,
)
# from collections.abc import Sequence
import dataclasses

from ...i18n import tr as _
from ..record import (
    Record,
    AnyBytes,
    Aeb43Context,
)
from ..record.context import Contextual
from ..fields import FieldMixin


ContextualT = TypeVar("ContextualT", bound=Contextual)


@dataclasses.dataclass(frozen=True)
class NestedContextual(FieldMixin[ContextualT]):
    "nested record descriptor"
    record_type: Type[ContextualT]
    optional: bool = False

    def __get__(self, this, this_type=None) -> ContextualT | None:
        if this is None:
            if self.optional:
                return None
            raise AttributeError()
        if self.optional:
            return getattr(this, self._varname(), None)
        return self._get_value(this)

    def __set__(self, this: Contextual, value: ContextualT | None):
        if isinstance(value, self.record_type):
            value.context = this.get_context()
        elif (value is not None) or not self.optional:
            raise ValueError(_("unexpected type"))
        self._set_value(this, value)


AnyRecord = TypeVar("AnyRecord", bound=Record)


def convert_record(
    record_type: Type[AnyRecord],
    context: Aeb43Context | None,
    value: AnyRecord | AnyBytes
) -> AnyRecord:
    "convert `value` to a `record_type` object with a compatible context"
    if isinstance(value, (bytes, bytearray)):
        return record_type(context, raw=value)
    if isinstance(value, record_type):
        value.context = context
        return value
    raise ValueError(_("unexpected type"))


@dataclasses.dataclass(frozen=True)
class NestedRecord(NestedContextual[AnyRecord]):
    "a nested record descriptor"

    def __set__(self, this: Contextual, value: AnyRecord | AnyBytes | None):
        if self.optional and value is None:
            self._set_value(this, value)
        elif value is not None:
            self._set_value(
                this,
                convert_record(self.record_type, this.get_context(), value)
            )
        else:
            raise ValueError(_("'None' value is not allowed"))


@dataclasses.dataclass
class RecordCollection(Sequence[AnyRecord]):
    "collection of record objects"
    context_f: Callable[[], Aeb43Context | None]
    record_type: Type[AnyRecord]
    _data: list[AnyRecord] = dataclasses.field(default_factory=list, repr=False)
    initial_data: dataclasses.InitVar[Iterable[AnyRecord | AnyBytes]] = dataclasses.field(
        default=None
    )

    def __post_init__(self, initial_data):
        if not initial_data:
            return
        for item in initial_data:
            self.append(item)

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __reversed__(self):
        return reversed(self._data)

    def index(self, value, start=None, stop=None):
        return self._data.index(value, start, stop)

    def _process_item(self, item: AnyRecord) -> AnyRecord:
        return item

    def append(self, item: AnyRecord | AnyBytes):
        "append record to this collection"
        record = self._process_item(convert_record(self.record_type, self.context_f(), item))
        self._data.append(record)
        self._post_append()

    def _post_append(self) -> None:
        pass

    def clear(self):
        "clear items in collection"
        self._data.clear()


TColFactory = Callable[[Contextual, Iterable[Union[AnyRecord, AnyBytes]]], RecordCollection]


@dataclasses.dataclass(frozen=True)
class NestedCollection(FieldMixin[RecordCollection[AnyRecord]]):
    "field for storing record collections"
    default_factory: TColFactory

    def __get__(self, this: Contextual | None, this_type=None) -> RecordCollection | None:
        if this is None:
            return None
        if not self._has_value(this):
            value = self.default_factory(this, [])
            self._set_value(this, value)
        else:
            value = self._get_value(this)
        return value

    def __set__(self, this: Contextual, value: Iterable[AnyRecord | AnyBytes]):
        self._set_value(this, self.default_factory(this, value))
