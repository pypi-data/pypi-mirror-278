#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Base tools for building descriptors fields for representing typed values and storing in bytes
"""
from __future__ import annotations
from typing import (
    Generic,
    TypeVar,
    Iterator,
)
import dataclasses

from ..record import (
    FieldValue,
    Record,
)
from ...i18n import tr as _


InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


def as_string(this: Record, field_id) -> str:
    "get the field identified by `field_id` from a record as a string"
    return this.get_field(field_id).decode(this.get_context().encoding)


_FIELD_MIXIN_CACHE = "_field_mixin_cache_{}"

# pylint: disable=too-few-public-methods
class FieldMixin(Generic[OutputT]):
    "Chacheable descriptor field mix-in"

    def _varname(self) -> str:
        return _FIELD_MIXIN_CACHE.format(id(self))

    def _has_value(self, this) -> bool:
        return hasattr(this, self._varname())

    def _set_value(self, this, value):
        setattr(this, self._varname(), value)

    def _get_value(self, this) -> OutputT:
        return getattr(this, self._varname())

    def _del_value(self, this) -> None:
        delattr(this, self._varname())


@dataclasses.dataclass(frozen=True)
class Field(Generic[OutputT, InputT], FieldMixin[OutputT]):
    "a typed representation for a field"

    def default_factory(self) -> OutputT:
        "return default factory function"
        raise NotImplementedError()

    def __get__(self, this: Record | None, this_type=None) -> OutputT:
        if this is None:
            return self.default_factory()
        if this.get_context().cache_fields and self._has_value(this):
            return self._get_value(this)
        value = self.to_field(this)
        if this.get_context().cache_fields:
            self._set_value(this, value)
        return value

    def __set__(self, this: Record, value: InputT) -> None:
        # convert to internal representation
        if value is self:
            return
        try:
            value = self.adapt(this, value)
        except Exception as exc:
            raise this.get_context().new_validation_error(
                _("unable to convert value to internal representation format: {exc}").format(
                    exc=exc
                )
            ) from exc
        # convert to bytes
        if this.update_fields(*self.to_bytes(this, value)) is None:
            return
        if not this.get_context().cache_fields and self._has_value(this):
            self._del_value(this)
        elif this.get_context().cache_fields:
            self._set_value(this, self.to_field(this))

    def adapt(self, this: Record, value: InputT) -> InputT:
        """adapt input for processing or raise an Aeb43Exception"""
        raise NotImplementedError()

    def to_field(self, this: Record) -> OutputT:
        "convert bytes chunks to a typed field"
        raise NotImplementedError()

    def to_bytes(self, this: Record, value: InputT) -> Iterator[FieldValue]:
        "convert a typed field to bytes chunks"
        raise NotImplementedError()
