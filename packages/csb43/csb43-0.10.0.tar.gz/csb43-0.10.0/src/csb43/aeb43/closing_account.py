#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Closing account record.

[es] Registro de asiento de cuenta
"""

from __future__ import annotations
import dataclasses
import enum

from ..utils import messages as msg
from .record import (
    RecordManifest,
    SingleRecordMixin,
    RegexValidator,
)
from .fields.string import String, string_validator, Trim
from .fields.integer import Integer, IntegerValidator
from .fields.money import Money, money_validator, money_mode_validator
from .fields.currency import Currency, currency_validator
from .closing import ClosingRecord


class Field(enum.Enum):
    "field identifiers for ClosingAccount record"
    BANK_CODE = enum.auto()
    BRANCH_CODE = enum.auto()
    ACCOUNT_NUMBER = enum.auto()
    EXPENSE_ENTRIES = enum.auto()
    EXPENSE_AMOUNT = enum.auto()
    INCOME_ENTRIES = enum.auto()
    INCOME_AMOUNT = enum.auto()
    FINAL_BALANCE_CODE = enum.auto()
    FINAL_BALANCE = enum.auto()
    CURRENCY_CODE = enum.auto()
    PADDING = enum.auto()


_opt_bank_val = RegexValidator(br"^(?:\d{4}| {4})$", warning=True)


# pylint: disable=too-many-instance-attributes
@dataclasses.dataclass
class ClosingAccount(SingleRecordMixin, ClosingRecord):
    """
    **COD 33**

    Closing account record

    [es] Registro de asiento de cuentas

    See [n43_2012]_ Appendix 1, section 1.5

    Fields
    ------
    bank_code : String[4]
        bank code / clave de la entidad
    branch_code : String[4]
        branch code / clave de oficina origen
    account_number : String[10]
        account number / número de cuenta
    expense_entries : Integer
        expense entries / número de apuntes en el Debe
    expense : Money[12.2]
        expense / total importes en el Debe
    income_entries : Integer
        income entries / número de apuntes en el Haber
    income : Money[12.2]
        income / total importes en el Haber
    padding : String[4]
        padding / libre uso
    """
    manifest = RecordManifest(
        code=b"33",
        sections={
            Field.BANK_CODE: (slice(2, 6), _opt_bank_val),
            Field.BRANCH_CODE: (slice(6, 10), _opt_bank_val),
            Field.ACCOUNT_NUMBER: (slice(10, 20), IntegerValidator(10, warning=True)),
            Field.EXPENSE_ENTRIES: (slice(20, 25), IntegerValidator(5)),
            Field.EXPENSE_AMOUNT: (slice(25, 39), money_validator()),
            Field.INCOME_ENTRIES: (slice(39, 44), IntegerValidator(5)),
            Field.INCOME_AMOUNT: (slice(44, 58), money_validator()),
            Field.FINAL_BALANCE_CODE: (slice(58, 59), money_mode_validator()),
            Field.FINAL_BALANCE: (slice(59, 73), money_validator()),
            Field.CURRENCY_CODE: (slice(73, 76), currency_validator()),
            Field.PADDING: (slice(76, 80), string_validator(4)),
        }
    )

    bank_code: String = dataclasses.field(
        default=String(
            Field.BANK_CODE, padding=b"0", trim=Trim.BOTH_BLANK, align_left=False
        ),
        metadata={"i18n": msg.T_BANK_CODE}
    )
    branch_code: String = dataclasses.field(
        default=String(
            Field.BRANCH_CODE, padding=b"0", trim=Trim.BOTH_BLANK, align_left=False
        ),
        metadata={"i18n": msg.T_BRANCH_CODE}
    )
    account_number: String = dataclasses.field(
        default=String(
            Field.ACCOUNT_NUMBER, padding=b"0", trim=Trim.BOTH_BLANK, align_left=False
        ),
        metadata={"i18n": msg.T_ACCOUNT_NUMBER}
    )
    expense_entries: Integer = dataclasses.field(
        default=Integer(Field.EXPENSE_ENTRIES),
        metadata={"i18n": msg.T_EXPENSES_ENTRIES}
    )
    expense: Money = dataclasses.field(
        default=Money(Field.EXPENSE_AMOUNT, non_negative=True),
        metadata={"i18n": msg.T_EXPENSES}
    )
    income_entries: Integer = dataclasses.field(
        default=Integer(Field.INCOME_ENTRIES),
        metadata={"i18n": msg.T_INCOME_ENTRIES}
    )
    income: Money = dataclasses.field(
        default=Money(Field.INCOME_AMOUNT, non_negative=True),
        metadata={"i18n": msg.T_INCOME}
    )
    final_balance: Money = dataclasses.field(
        default=Money(Field.FINAL_BALANCE, Field.FINAL_BALANCE_CODE),
        metadata={"i18n": msg.T_FINAL_BALANCE}
    )
    currency: Currency = dataclasses.field(
        default=Currency(Field.CURRENCY_CODE),
        metadata={"i18n": msg.T_CURRENCY}
    )
    padding: String = dataclasses.field(
        default=String(Field.PADDING),
        metadata={"i18n": msg.T_PADDING}
    )
