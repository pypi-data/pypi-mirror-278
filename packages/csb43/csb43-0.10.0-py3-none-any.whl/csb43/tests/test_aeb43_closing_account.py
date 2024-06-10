#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations
from decimal import Decimal
import pytest
import pycountry

from ..aeb43.record.context import Aeb43Context
from ..aeb43.record.errors import ValidationException, ValidationWarning
from ..aeb43.closing_account import ClosingAccount


@pytest.fixture(name="strict_record")
def fixture_strict_record(strict_context: Aeb43Context) -> ClosingAccount:
    "an item with a strict context"
    return ClosingAccount(context=strict_context)


@pytest.fixture(name="default_record")
def fixture_default_record() -> ClosingAccount:
    "a default item"
    return ClosingAccount()


@pytest.fixture(name="non_strict_record")
def fixture_non_strict_record(non_strict_context: Aeb43Context) -> ClosingAccount:
    "an item with a non strict context"
    return ClosingAccount(context=non_strict_context)


@pytest.fixture(name="record")
def fixture_record(context: Aeb43Context) -> ClosingAccount:
    "an account object"
    return ClosingAccount(context=context)


def test_context(record: ClosingAccount):
    "each record must have a context"
    assert record.get_context() is not None


def test_context_default_record(default_record: ClosingAccount):
    "default record must have a contexT"
    assert default_record.get_context() is not None


def test_to_dict(record: ClosingAccount):
    "`to_dict` method must not fail"
    res = record.to_dict()
    assert res
    assert isinstance(res, dict)


@pytest.fixture(name="raw_item1", scope="session")
def fixture_raw_item() -> bytes:
    "a valid raw record"
    return b"33" + (b"1" * 78)


def test_init(record: ClosingAccount, raw_item1: bytes):
    "construct a valid account"
    record.from_raw(raw_item1)


def test_from_raw(record: ClosingAccount, raw_item1: bytes):
    "updating a record from raw"
    record.from_raw(raw_item1)


def _get_valid_entries():
    return [
        (0, 0),
        ("0", 0),
        (123, 123),
        ("00000", 0),
        (99999, 99999),
    ]


def _get_invalid_entries():
    return [
        "abcd",
        100000,
    ]


@pytest.mark.parametrize("value,ref", _get_valid_entries(), ids=repr)
def test_valid_expense_entries(record: ClosingAccount, value, ref):
    "check expense_entries property"
    record.expense_entries = value
    assert record.expense_entries == ref


@pytest.mark.parametrize("value", _get_invalid_entries(), ids=repr)
def test_invalid_expense_entries(record: ClosingAccount, value):
    "setting an invalid expense entries must raise an exception"
    with pytest.raises(ValidationException):
        record.expense_entries = value


@pytest.mark.parametrize("value,ref", _get_valid_entries(), ids=repr)
def test_valid_income_entries(record: ClosingAccount, value, ref):
    "check expense_entries property"
    record.income_entries = value
    assert record.income_entries == ref


@pytest.mark.parametrize("value", _get_invalid_entries(), ids=repr)
def test_invalid_income_entries(record: ClosingAccount, value):
    "setting an invalid expense entries must raise an exception"
    with pytest.raises(ValidationException):
        record.income_entries = value


def _get_valid_amount():
    return [
        (1, Decimal("1")),
        ("1", Decimal("1")),
        (12345, Decimal("12345")),
        (b"12345", Decimal("12345")),
        ("12345", Decimal("12345")),
        (123456, Decimal("123456")),
        (123456.12, Decimal("123456.12")),
        ("123456.87", Decimal("123456.87")),
        # truncation
        ("123456.876", Decimal("123456.87")),
        (123456.876, Decimal("123456.87")),
    ]


def _get_invalid_amount():
    return [
        (-12345, False),
        ("-12345", False),
        ("12345" * 4, True),
        (b"12345" * 4, True),
        (b"asdagsa", True),
        ("asdagsa", True),
        ("asdagsa" * 4, True),
        (-123456, False),
    ]


@pytest.mark.parametrize("value,ref", _get_valid_amount(), ids=repr)
def test_valid_expense(record: ClosingAccount, value, ref):
    "test the property accepts a valid value"
    record.expense = value
    assert record.expense == ref


@pytest.mark.parametrize("value,is_strict", _get_invalid_amount(), ids=repr)
def test_invalid_expense(record: ClosingAccount, value, is_strict):
    "an invalid value must raise or trigger an error"
    if not is_strict and not record.get_context().strict:
        with pytest.warns(ValidationWarning):
            record.expense = value
    else:
        with pytest.raises(ValidationException):
            record.expense = value


@pytest.mark.parametrize("value,ref", _get_valid_amount(), ids=repr)
def test_valid_income(record: ClosingAccount, value, ref):
    "test the property accepts a valid value"
    record.income = value
    assert record.income == ref


@pytest.mark.parametrize("value,is_strict", _get_invalid_amount(), ids=repr)
def test_invalid_income(record: ClosingAccount, value, is_strict):
    "an invalid value must raise or trigger an error"
    if not is_strict and not record.get_context().strict:
        with pytest.warns(ValidationWarning):
            record.income = value
    else:
        with pytest.raises(ValidationException):
            record.income = value


@pytest.mark.parametrize("amount,ref", [
    (1, Decimal("1")),
    ("1", Decimal("1")),
    (12345, Decimal("12345")),
    (b"12345", Decimal("12345")),
    ("12345", Decimal("12345")),
    ("-12345", Decimal("-12345")),
    (-12345, Decimal("-12345")),
    (123456, Decimal("123456")),
    (-123456, Decimal("-123456")),
    (123456.12, Decimal("123456.12")),
    ("123456.87", Decimal("123456.87")),
    # truncation
    ("123456.876", Decimal("123456.87")),
    (123456.876, Decimal("123456.87")),
])
def test_valid_final_balance(record: ClosingAccount, amount, ref):
    "check the amount property"
    record.final_balance = amount
    assert record.final_balance == ref


@pytest.mark.parametrize("amount", [
    "12345" * 4,
    b"12345" * 4,
    b"asdagsa",
    "asdagsa",
    "asdagsa" * 4,
], ids=repr)
def test_invalid_final_balance(record: ClosingAccount, amount):
    "an invalid amount must raise an exception"
    with pytest.raises(ValueError):
        record.final_balance = amount


@pytest.mark.parametrize(
    "value",
    [3, "asdfalsjk", b"asdfalsjk", None],
    ids=["code", "string", "bytes", "None"]
)
def test_currency_set_invalid(record: ClosingAccount, value):
    "an invalid source currency must raise an exception"
    with pytest.raises(ValueError):
        record.currency = value


@pytest.mark.parametrize("value", [
    978,
    "978",
    "eur",
    "EUR",
    b"EUR",
    pycountry.currencies.get(numeric="978")
])
def test_original_currency_set_euro(record: ClosingAccount, value):
    "different ways to set source currency to Euro"
    record.currency = value

    assert record.currency.numeric == "978"
    assert record.currency.alpha_3 == "EUR"
