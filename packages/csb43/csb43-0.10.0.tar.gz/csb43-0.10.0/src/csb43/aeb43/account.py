#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Account record.

[es] Registro de cabecera de cuenta.
"""

from __future__ import annotations
from typing import (
    Iterable,
)
import dataclasses
import enum
from decimal import Decimal

from ..utils import messages as msg
from ..utils.tabulated import adjust_table_width
from ..i18n import tr as _
from .record import (
    Record,
    RecordManifest,
    RegexValidator,
    CompositeRecordMixin,
    FieldValue,
)
from .fields.string import String, string_validator, Trim
from .fields.integer import IntegerValidator
from .fields.date import Date, date_validator
from .fields.money import Money, money_validator, money_mode_validator
from .fields.currency import Currency, currency_validator
from .fields.nested import (
    NestedCollection,
    RecordCollection,
)
from .fields.information_mode import InformationModeField
from .transaction import Transaction
from .closing import (
    Closeable,
    SummaryField,
)
from .closing_account import ClosingAccount


class Field(enum.Enum):
    "field identifiers for Account record"
    BANK_CODE = enum.auto()
    BRANCH_CODE = enum.auto()
    ACCOUNT_NUMBER = enum.auto()
    INITIAL_DATE = enum.auto()
    FINAL_DATE = enum.auto()
    EXPENSE_OR_INCOME = enum.auto()
    INITIAL_BALANCE = enum.auto()
    CURRENCY_CODE = enum.auto()
    INFORMATION_MODE = enum.auto()
    SHORT_NAME = enum.auto()
    PADDING = enum.auto()


def _create_transaction_collection(record, initial_values):
    "transaction factory"
    assert isinstance(record, Account)
    return RecordCollection(
        context_f=record.get_context,
        record_type=Transaction,
        initial_data=initial_values
    )


@dataclasses.dataclass
class _Summary:
    income_entries: int = 0
    income: Decimal = Decimal(0)
    expense_entries: int = 0
    expense: Decimal = Decimal(0)
    balance: Decimal = Decimal(0)


def _sumprod(code: Iterable, weights: Iterable[int]):
    return sum(int(x) * y for x, y in zip(code, weights))


def _number_to_code(value: int) -> int:
    value = value % 11
    if value == 10:
        value = 1
    return value


def get_account_key(
    bank_code: str, branch_code: str, account_number: str
) -> str:
    '''
    Generate the two-digits checksum for the bank account
    from `bank_code`, `branch_code` and `account_number`.

    When invalid values are provided, the empty string
    is returned.
    '''
    bank_code = bank_code.strip() or "0"
    branch_code = branch_code.strip() or "0"
    account_number = account_number.strip() or "0"

    weights = (10, 9, 7, 3, 6, 1, 2, 4, 8, 5)
    bank_weights = weights[2:6]
    branch_weights = weights[6:]

    try:
        digit1 = _number_to_code(
            _sumprod(bank_code, bank_weights)
            + _sumprod(branch_code, branch_weights)
        )

        digit2 = _number_to_code(_sumprod(account_number, weights))
    except ValueError:
        return ""

    return f"{digit1:d}{digit2:d}"


_opt_bank_val = RegexValidator(br"^(?:\d{4}| {4})$", warning=True)


# pylint: disable=too-many-instance-attributes
@dataclasses.dataclass
class Account(CompositeRecordMixin, Closeable[ClosingAccount], Record):
    """
    **COD 11**

    Account record

    [es] Registro de cabecera de cuenta

    See [n43_2012]_ Appendix 1, section 1.1

    Fields
    ------
    bank_code : String[4]
        bank code / clave de la entidad
    branch_code : String[4]
        branch code / clave de oficina
    account_number : String[10]
        account number / número de cuenta
    initial_date : Date
        initial date / fecha inicial
    final_date : Date
        final date / fecha final
    initial_balance : Money[12.2]
        initial balance / importe saldo inicial
    currency : Currency
        currency / divisa
    information_mode : Integer[1..3]
        information mode / modalidad de información
    short_name : String[26]
        short name / nombre abreviado
    padding : String[3]
        padding / libre uso
    """
    manifest = RecordManifest(
        code=b"11",
        sections={
            Field.BANK_CODE: (slice(2, 6), _opt_bank_val),
            Field.BRANCH_CODE: (slice(6, 10), _opt_bank_val),
            Field.ACCOUNT_NUMBER: (slice(10, 20), IntegerValidator(10, warning=True)),
            Field.INITIAL_DATE: (slice(20, 26), date_validator()),
            Field.FINAL_DATE: (slice(26, 32), date_validator()),
            Field.EXPENSE_OR_INCOME: (slice(32, 33), money_mode_validator()),
            Field.INITIAL_BALANCE: (slice(33, 47), money_validator()),
            Field.CURRENCY_CODE: (slice(47, 50), currency_validator()),
            Field.INFORMATION_MODE: (slice(50, 51), IntegerValidator(1, 1, 3)),
            Field.SHORT_NAME: (slice(51, 77), string_validator(26)),
            Field.PADDING: (slice(77, 80), string_validator(3)),
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
    initial_date: Date = dataclasses.field(
        default=Date(Field.INITIAL_DATE),
        metadata={"i18n": msg.T_INITIAL_DATE}
    )
    final_date: Date = dataclasses.field(
        default=Date(Field.FINAL_DATE),
        metadata={"i18n": msg.T_FINAL_DATE}
    )
    initial_balance: Money = dataclasses.field(
        default=Money(Field.INITIAL_BALANCE, Field.EXPENSE_OR_INCOME),
        metadata={"i18n": msg.T_INITIAL_BALANCE}
    )
    currency: Currency = dataclasses.field(
        default=Currency(Field.CURRENCY_CODE),
        metadata={"i18n": msg.T_CURRENCY}
    )
    information_mode: InformationModeField = dataclasses.field(
        default=InformationModeField(Field.INFORMATION_MODE),
        metadata={"i18n": msg.T_INFORMATION_MODE}
    )
    short_name: String = dataclasses.field(
        default=String(Field.SHORT_NAME),
        metadata={"i18n": msg.T_SHORT_NAME}
    )
    padding: String = dataclasses.field(
        default=String(Field.PADDING),
        metadata={"i18n": msg.T_PADDING}
    )

    transactions: NestedCollection[Transaction] = NestedCollection(_create_transaction_collection)
    # closing account
    # validate
    summary: SummaryField[ClosingAccount] = SummaryField(ClosingAccount, optional=True)

    def _accepted_fields(self, changes: Iterable[FieldValue]):
        "update context if information mode changed"
        infmode = None
        for change in changes:
            if change.field_id == Field.INFORMATION_MODE:
                infmode = change
                break

        if infmode:
            mode = InformationModeField.convert_bytes(self, infmode.value)
            context = self.get_context()
            if mode != context.information_mode:
                self.context = dataclasses.replace(context, information_mode=mode)

    @property
    def account_control_key(self):
        "get the account control key (CC)"
        return get_account_key(
            self.bank_code,
            self.branch_code,
            self.account_number
        )

    def _compare(self, ref, alt, name: str):
        if ref == alt:
            return
        self.get_context().emit_validation_error(
            _(name + " ({alt}) mismatch in summary ({ref})").format(
                alt=alt,
                ref=ref,
            )
        )

    def validate_summary(self, summary: ClosingAccount):
        "validate summary record against the extant nested records"
        if summary.is_validated():
            return
        total = self._create_summary()

        self._compare(self.bank_code, summary.bank_code, "bank code")
        self._compare(self.branch_code, summary.branch_code, "branch code")
        self._compare(self.account_number, summary.account_number, "account number")
        self._compare(total.income_entries, summary.income_entries, "income entries")
        self._compare(total.expense_entries, summary.expense_entries, "expense entries")
        self._compare(total.income, summary.income, "income")
        self._compare(total.expense, summary.expense, "expense")
        self._compare(total.balance, summary.final_balance, "final balance")

    def _create_summary(self) -> _Summary:
        data = _Summary(balance=self.initial_balance)
        # pylint: disable=not-an-iterable
        assert self.transactions is not None
        for transaction in self.transactions:
            if transaction.amount >= 0:
                data.income_entries += 1
                data.income += transaction.amount
            else:
                data.expense_entries += 1
                data.expense += transaction.amount
            data.balance += transaction.amount
        data.expense = abs(data.expense)
        return data

    def _set_new_summary(self):
        data = self._create_summary()
        summary = ClosingAccount(context=self.context)
        summary.bank_code = self.bank_code
        summary.branch_code = self.branch_code
        summary.account_number = self.account_number
        summary.income = data.income
        summary.income_entries = data.income_entries
        summary.expense = data.expense
        summary.expense_entries = data.expense_entries
        summary.final_balance = data.balance
        self.summary = summary

    def is_closed(self) -> bool:
        "return True if this account has a final summary"
        return self.summary is not None

    def __iter__(self):
        yield bytes(self)
        # pylint: disable=not-an-iterable
        for transaction in self.transactions:
            yield from transaction
        if self.summary:
            yield from self.summary

    def accepts_nested_codes(self, record: bytes) -> bool:
        if self.is_closed():
            return False
        return (
            record.startswith(Transaction.manifest.code)
            or (self.transactions and self.transactions[-1].accepts_nested_code(record))
            or record.startswith(ClosingAccount.manifest.code)
        )

    def append(self, raw: bytes):
        if self.is_closed():
            self.get_context().emit_validation_error(_("adding records to a closed account"))
        # summary
        assert self.transactions is not None
        if not self.summary and raw.startswith(ClosingAccount.manifest.code):
            self.summary = raw
        elif raw.startswith(Transaction.manifest.code):
            # pylint: disable=no-member
            self.transactions.append(raw)
        elif self.transactions:
            self.transactions[-1].append(raw)
        else:
            self.get_context().emit_validation_error(
                _("unknown or illegal record: {record}").format(record=raw)
            )

    def to_dict(self, translated=True):
        # pylint: disable=no-member
        data = super().to_dict(translated)
        if self.summary:
            k_sum = msg.T_SUMMARY if translated else "summary"
            data[k_sum] = self.summary.to_dict(translated)
        if self.transactions:
            # pylint: disable=not-an-iterable
            k_tr = msg.T_TRANSACTIONS if translated else "transactions"
            data[k_tr] = [
                tran.to_dict(translated)
                for tran in self.transactions
            ]
        return data

    # pylint: disable=no-member
    def describe(self, indent: str = "") -> str:
        "return a textual summary"
        templates = (
            [
                _("+ Account: {account_number}\t{short_name}"),
            ] +
            list(adjust_table_width((
                _("From:||{date_from}"),
                _("To:||{date_to}"),
            ), indent=2)) +
            [
                "",
                "  " + _("{ntransactions:d} transaction(s) read"),
                "  " + _("Account properly closed: {ac_is_closed}"),
                "  " + _("Information mode: {information_mode}"),
            ] +
            list(adjust_table_width((
                _("Previous amount:||{ib_amount:14.2f} {ib_currency}"),
                _(" Income:||{inc_amount:14.2f} {inc_currency}"),
                _(" Expense:||{exp_amount:14.2f} {exp_currency}"),
                _("Balance:||{bal_amount:14.2f} {bal_currency}"),
            ), indent=2))
        )

        template = "\n".join(indent + line for line in templates)

        currency = self.currency.alpha_3

        if self.summary:
            income = self.summary.income
            expense = self.summary.expense
            balance = self.summary.final_balance
        else:
            data = self._create_summary()
            income = data.income
            expense = data.expense
            balance = data.balance

        return template.format(
            account_number=self.account_number,
            short_name=self.short_name,
            date_from=self.initial_date.strftime("%Y-%m-%d"),
            date_to=self.final_date.strftime("%Y-%m-%d"),
            ntransactions=len(self.transactions or []),
            ac_is_closed=self.is_closed(),
            information_mode=self.information_mode.value,
            ib_amount=self.initial_balance,
            ib_currency=currency,
            inc_amount=income,
            inc_currency=currency,
            exp_amount=expense,
            exp_currency=currency,
            bal_amount=balance,
            bal_currency=currency,
        )
