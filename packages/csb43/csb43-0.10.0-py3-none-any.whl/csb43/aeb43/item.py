#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Complementary item

[es] Registro complementario de concepto
"""

from __future__ import annotations
from dataclasses import dataclass, field
import enum

from ..utils import messages as msg
from .record import (
    Record,
    SingleRecordMixin,
    RecordManifest,
)
from .fields.string import String, string_validator
from .fields.integer import Integer, IntegerValidator


MIN_ITEMS = 1
MAX_ITEMS = 5


class Field(enum.Enum):
    "field identifiers for Exchange record"

    # data code
    RECORD = enum.auto()
    # item 1
    ITEM1 = enum.auto()
    # item 2
    ITEM2 = enum.auto()


def default_record_code():
    "default record code"
    return 1


@dataclass
class Item(SingleRecordMixin, Record):
    """
    **COD 23**

    Complementary item / [es] Registro complementario de concepto.

    For SEPA normalization using item records, see:

    - :mod:`csb43.aeb43.sepa_debit`
    - :mod:`csb43.aeb43.sepa_transfer`

    See [n43_2012]_ Appendix 1, section 1.3

    Fields
    ------
    record_code : Integer[1..5]
        sequence code for complementary item record / [es] código de registro
    item1 : String[38]
        item #1 / [es] concepto 1
    item2 : String[38]
        item #2 / [es] concepto 2
    """
    manifest = RecordManifest(
        code=b"23",
        sections={
            Field.RECORD: (slice(2, 4), IntegerValidator(2, MIN_ITEMS, MAX_ITEMS)),
            Field.ITEM1: (slice(4, 42), string_validator(38)),
            Field.ITEM2: (slice(42, 80), string_validator(38)),
        }
    )

    record_code: Integer = field(
        default=Integer(field_id=Field.RECORD, factory=default_record_code),
        metadata={"i18n": msg.T_RECORD_CODE}
    )
    item1: String = field(
        default=String(field_id=Field.ITEM1),
        metadata={"i18n": msg.T_ITEM_1}
    )
    item2: String = field(
        default=String(field_id=Field.ITEM2),
        metadata={"i18n": msg.T_ITEM_2}
    )

    @classmethod
    def accepts_sequence_code(cls, encoding: str, start: int, code: bytes) -> bool:
        """return True if the provided `code` is allowed at the current transaction

        Args
        ----
        encoding
            string encoding
        start
            first item record to check
        """
        start = max(start, MIN_ITEMS)
        for index in range(start, MAX_ITEMS):
            seq = f"0{index:d}".encode(encoding)
            if code.startswith(cls.manifest.code + seq):
                return True
        return False
