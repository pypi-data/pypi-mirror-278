#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Exchange record.

[es] Registro complementario de información de equivalencia de importe del apunte.

References:

@techreport{n43_2012,
	author = {Varios},
	institution = {Confederación Española de Cajas de Ahorros},
	month = 6,
	number = {Serie normas y procedimientos bancarios nº 43},
	publisher = {Asociación Española de Banca},
	title = {{Información normalizada de cuenta corriente (SEPA)}},
	year = {2012}
}
"""

from __future__ import annotations
from dataclasses import dataclass, field
import enum

from ..utils import messages as msg

from .record import (
    Record,
    RecordManifest,
    SingleRecordMixin,
)
from .fields import money, string, currency


class Field(enum.Enum):
    "field identifiers for Exchange record"
    # currency / divisa
    CURRENCY = enum.auto()
    # amount / importe
    AMOUNT = enum.auto()
    # padding / libre
    PADDING = enum.auto()


@dataclass
class Exchange(SingleRecordMixin, Record):
    """
    **COD 24-01**

    Exchange record

    [es] Registro complementario de información de equivalencia
    de importe del apunte.

    See [n43_2012]_ Appendix 1, section 1.4

    Fields
    ------
    original_currency : Currency
        original currency / divisa origen del movimiento
    amount : Money[12.2]
        transaction amount in the original currency / import en divisa origen
    padding : String[59]
        unused space in record / libre
    """
    manifest = RecordManifest(
        code=b"2401",
        sections={
            Field.CURRENCY: (slice(4, 7), currency.currency_validator()),
            Field.AMOUNT: (slice(7, 21), money.money_validator(14)),
            Field.PADDING: (slice(21, 80), string.string_validator(59)),
        }
    )

    original_currency: currency.Currency = field(
        default=currency.Currency(field_id=Field.CURRENCY),
        metadata={"i18n": msg.T_ORIGINAL_CURRENCY}
    )
    amount: money.Money = field(
        default=money.Money(value_id=Field.AMOUNT),
        metadata={"i18n": msg.T_AMOUNT}
    )
    padding: string.String = field(
        default=string.String(field_id=Field.PADDING),
        metadata={"i18n": msg.T_PADDING}
    )
