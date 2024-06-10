#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations
from datetime import datetime, date
from decimal import Decimal
import pytest

from ..aeb43.record.context import Aeb43Context, InformationMode
from ..aeb43.record.errors import (
    ValidationException,
    ValidationWarning,
)
from ..aeb43.account import Account
from ..aeb43.transaction import Transaction


@pytest.fixture(name="strict_record")
def fixture_strict_record(strict_context: Aeb43Context) -> Account:
    "an item with a strict context"
    return Account(context=strict_context)


@pytest.fixture(name="default_record")
def fixture_default_record() -> Account:
    "a default item"
    return Account()


@pytest.fixture(name="non_strict_record")
def fixture_non_strict_record(non_strict_context: Aeb43Context) -> Account:
    "an item with a non strict context"
    return Account(context=non_strict_context)


@pytest.fixture(name="record")
def fixture_record(context: Aeb43Context) -> Account:
    "an account object"
    return Account(context=context)


def test_context(record: Account):
    "each record must have a context"
    assert record.get_context() is not None


def test_context_default_record(default_record: Account):
    "default record must have a contexT"
    assert default_record.get_context() is not None


def test_to_dict(record: Account):
    "`to_dict` method must not fail"
    res = record.to_dict()
    assert res
    assert isinstance(res, dict)


@pytest.fixture(name="raw_bad_length", scope="session")
def fixture_raw_bad_length() -> bytes:
    "a bad raw record"
    return b"1112380118008"


def test_constructor_bad_length(raw_bad_length: bytes):
    "creating a bad record should raise an exception"
    with pytest.raises(ValidationException):
        Account(raw=raw_bad_length)


def test_from_raw_bad_length(record: Account, raw_bad_length: bytes):
    "assigning a bad record should raise an exception"
    with pytest.raises(ValidationException):
        record.from_raw(raw_bad_length)


@pytest.fixture(name="raw_item1", scope="session")
def fixture_raw_item() -> bytes:
    "a valid raw record"
    return b"11" + (b"1" * 78)


def test_init_bad_code_str(record: Account, raw_item1: bytes):
    "a raw record with a bad code should trigger an error"
    raw = b"12" + raw_item1[2:]
    with pytest.raises(ValidationException):
        record.from_raw(raw)


def test_init(record: Account, raw_item1: bytes):
    "construct a valid account"
    record.from_raw(raw_item1)


def test_from_raw(record: Account, raw_item1: bytes):
    "updating a record from raw"
    record.from_raw(raw_item1)


@pytest.mark.parametrize("value,ref", [
    ("1234", "1234"),
    (b"1234", "1234"),
    (1234, "1234"),
    (1, "0001"),
    ("1", "0001"),
    (0, "0000"),
    ("0", "0000"),
    ("", "0000"),
    (b"", "0000"),
    (b"    ", "0000"),
], ids=repr)
def test_valid_bank_code(record: Account, value, ref):
    "set the branch code"
    record.bank_code = value
    assert record.bank_code == ref


@pytest.mark.parametrize("value,warning", [
    ("12345", False),
    ("asdf", True),
], ids=repr)
def test_invalid_bank_code(record: Account, value, warning):
    "setting an invalid branch must raise an exception"
    is_warning = not record.get_context().strict and warning
    if is_warning:
        with pytest.warns(ValidationWarning):
            record.bank_code = value
    else:
        with pytest.raises(ValidationException):
            record.bank_code = value


@pytest.mark.parametrize("value,ref", [
    ("1234", "1234"),
    (b"1234", "1234"),
    (1234, "1234"),
    (1, "0001"),
    ("1", "0001"),
    (0, "0000"),
    ("0", "0000"),
    ("", "0000"),
    (b"", "0000"),
    (b"    ", "0000"),
], ids=repr)
def test_valid_branch_code(record: Account, value, ref):
    "set the branch code"
    record.branch_code = value
    assert record.branch_code == ref


@pytest.mark.parametrize("value,warning", [
    ("12345", False),
    ("asdf", True),
], ids=repr)
def test_invalid_branch_code(record: Account, value, warning):
    "setting an invalid branch must raise an exception"
    is_warning = not record.get_context().strict and warning
    if is_warning:
        with pytest.warns(ValidationWarning):
            record.branch_code = value
    else:
        with pytest.raises(ValidationException):
            record.branch_code = value


@pytest.mark.parametrize("value,ref", [
    ("12345", "0000012345"),
    (b"12345", "0000012345"),
    (b" 12345 ", "0000012345"),
    (12345, "0000012345"),
    ("0123456789", "0123456789"),
    ("", "0000000000"),
    (b"", "0000000000"),
], ids=repr)
def test_valid_account_number(record: Account, value, ref):
    "set the account number"
    record.account_number = value
    assert record.account_number == ref


@pytest.mark.parametrize("value,warning", [
    ("asdfa", True),
    ("1" * 11, False),
    ("1" * 15, False),
    (1234567890123, False),
], ids=repr)
def test_invalid_account_number(record: Account, value, warning):
    "setting an invalid account number must raise an exception"
    is_warning = not record.get_context().strict and warning
    if is_warning:
        with pytest.warns(ValidationWarning):
            record.account_number = value
    else:
        with pytest.raises(ValidationException):
            record.account_number = value


def _get_valid_dates():
    now = datetime.now()
    return [
        (now, now.date()),
        (now.date(), now.date()),
        ("20010102", date(day=2, month=1, year=2001)),
        ("010102", date(day=2, month=1, year=2001)),
        ("2001/01/02", date(day=2, month=1, year=2001)),
        ("01/01/02", date(day=2, month=1, year=2001)),
        ("2001-01-02", date(day=2, month=1, year=2001)),
        ("01-01-02", date(day=2, month=1, year=2001)),
    ]


def _get_invalid_dates():
    return [
        "asdfa",
        "012",
        "01111",
        "0111111",
        None,
    ]


@pytest.mark.parametrize("value,ref", _get_valid_dates(), ids=repr)
def test_valid_initial_date(record: Account, value, ref):
    "set the initial date"
    record.initial_date = value
    assert record.initial_date == ref


@pytest.mark.parametrize("value", _get_invalid_dates(), ids=repr)
def test_invalid_initial_date(record: Account, value):
    "setting and invalid date must raise an exception"
    with pytest.raises(ValidationException):
        record.initial_date = value


@pytest.mark.parametrize("value,ref", _get_valid_dates(), ids=repr)
def test_valid_final_date(record: Account, value, ref):
    "set the final date"
    record.final_date = value
    assert record.final_date == ref


@pytest.mark.parametrize("value", _get_invalid_dates(), ids=repr)
def test_invalid_final_date(record: Account, value):
    "setting and invalid date must raise an exception"
    with pytest.raises(ValidationException):
        record.final_date = value


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
def test_valid_initial_balance(record: Account, amount, ref):
    "check the initial_balance property"
    record.initial_balance = amount
    assert record.initial_balance == ref


@pytest.mark.parametrize("amount", [
    "12345" * 4,
    b"12345" * 4,
    b"asdagsa",
    "asdagsa",
    "asdagsa" * 4,
], ids=repr)
def test_invalid_initial_balance(record: Account, amount):
    "an invalid initial_balance must raise an exception"
    with pytest.raises(ValueError):
        record.initial_balance = amount


@pytest.mark.parametrize("value,ref", [
    ("John Smith", "John Smith"),
    (b"John Smith", "John Smith"),
    ("José Müller Muñiz Avinyò", "José Müller Muñiz Avinyò"),
], ids=repr)
def test_valid_short_name(record: Account, value, ref):
    "check the short name property"
    record.short_name = value
    assert record.short_name == ref


@pytest.mark.parametrize("value,ref", [
    (1, InformationMode.FIRST),
    (2, InformationMode.SECOND),
    (3, InformationMode.THIRD),
    ("1", InformationMode.FIRST),
    ("2", InformationMode.SECOND),
    ("3", InformationMode.THIRD),
    (b"1", InformationMode.FIRST),
    (b"2", InformationMode.SECOND),
    (b"3", InformationMode.THIRD),
    (InformationMode.FIRST, InformationMode.FIRST),
    (InformationMode.SECOND, InformationMode.SECOND),
    (InformationMode.THIRD, InformationMode.THIRD),
], ids=repr)
def test_valid_information_mode(record: Account, value, ref):
    "check the information mode property"
    record.information_mode = value
    assert record.information_mode == ref


@pytest.mark.parametrize("value", [
    InformationMode.FIRST,
    InformationMode.SECOND,
    InformationMode.THIRD,
], ids=repr)
def test_context_information_mode(record: Account, value):
    "check information mode is changed in context"
    record.information_mode = value
    assert record.information_mode == value
    assert record.get_context().information_mode == value
    assert record.get_context().information_mode == record.information_mode


@pytest.mark.parametrize("value", [
    5,
    "12",
    "a",
], ids=repr)
def test_invalid_information_mode(record: Account, value):
    "an invalid information mode must raise an exception"
    with pytest.raises(ValidationException):
        record.information_mode = value


def test_is_closed(record: Account):
    "an account without a summary is not closed"
    assert record.summary is None
    assert not record.is_closed()


@pytest.fixture(name="raw_transaction1")
def fixture_raw_transaction() -> bytes:
    "a valid raw record"
    return b"22" + (b"0" * 25) + b"1" + (b"0" * 52)


def test_append_transaction(record: Account, raw_transaction1):
    "append accepts transactions"
    assert not record.transactions
    for idx in range(6):
        record.append(raw_transaction1)
        assert record.transactions
        assert len(record.transactions) == (idx + 1)
        assert isinstance(record.transactions[-1], Transaction)


def test_add_transaction(record: Account, raw_transaction1):
    "append accepts transactions"
    assert record.transactions is not None
    for idx in range(6):
        record.transactions.append(raw_transaction1)
        assert record.transactions
        assert len(record.transactions) == (idx + 1)
        assert isinstance(record.transactions[-1], Transaction)
