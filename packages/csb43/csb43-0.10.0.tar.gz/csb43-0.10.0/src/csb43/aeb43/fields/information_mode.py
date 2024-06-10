#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Descriptor for AEB43 information mode fields
"""
from __future__ import annotations
from typing import (
    Any,
    Iterator,
    Union,
    Callable,
)
import dataclasses

from ..record import (
    FieldValue,
    Record,
    TValidator,
)
from . import Field
from ..record.context import (
    Aeb43Context,
    InformationMode,
)


@dataclasses.dataclass(frozen=True)
class InformationModeField(Field[InformationMode, Union[InformationMode, int]]):
    "descriptor field for information mode enum"
    field_id: Any
    factory: Callable[[], InformationMode] = lambda: InformationMode.THIRD

    def default_factory(self) -> InformationMode:
        return self.factory()

    def adapt(self, this: Record, value: InformationMode | int):
        if isinstance(value, int):
            return value
        return int(this.get_context().to_string(value))

    @staticmethod
    def convert_bytes(this: Record, value: bytes) -> InformationMode:
        "convert from bytes to information mode"
        return InformationMode(int(value.decode(this.get_context().encoding)))

    def to_field(self, this: Record) -> InformationMode:
        return self.convert_bytes(this, this.get_field(self.field_id))

    def to_bytes(self, this: Record, value: InformationMode | int) -> Iterator[FieldValue]:
        if isinstance(value, InformationMode):
            value = value.value
        record = f"{value:d}".encode(this.get_context().encoding)
        yield FieldValue(self.field_id, record)


@dataclasses.dataclass
class OnModeValidator:
    "validator for each information mode"
    validator1: TValidator
    validator2: TValidator
    validator3: TValidator

    def __call__(self, context: Aeb43Context, field) -> tuple[str | None, str | None]:
        val_f: TValidator
        if context.information_mode == InformationMode.FIRST:
            val_f = self.validator1
        elif context.information_mode == InformationMode.SECOND:
            val_f = self.validator2
        else:
            val_f = self.validator3
        return val_f(context, field)
