#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations
from decimal import Decimal
import pytest
import pycountry

from ..aeb43.record.context import Aeb43Context
from ..aeb43.record.errors import ValidationException
from ..aeb43.exchange import Exchange


@pytest.fixture(name="default_record")
def fixture_default_record() -> Exchange:
    "a default exchange"
    return Exchange()


@pytest.fixture(name="record")
def fixture_record(context: Aeb43Context) -> Exchange:
    "an exchange object"
    return Exchange(context=context)


def test_context(record: Exchange):
    "each record must have a context"
    assert record.get_context() is not None


def test_context_default_record(default_record: Exchange):
    "default record must have a context"
    assert default_record.get_context() is not None


def test_default_bytes(record: Exchange, default_record: Exchange):
    "bytes for each record must be the same"
    assert bytes(default_record) == bytes(record)


@pytest.fixture(name="raw_bad_length", scope="session")
def fixture_raw_bad_length() -> bytes:
    "a truncated raw record"
    return b"24011023402150"


def test_constructor_bad_length(raw_bad_length: bytes):
    "creating a record from a truncated raw record must raise an exception"
    with pytest.raises(ValidationException):
        Exchange(raw=raw_bad_length)


def test_from_raw_bad_length(record: Exchange, raw_bad_length: bytes):
    "updating a record from a truncated raw record must raise an exception"
    with pytest.raises(ValidationException):
        record.from_raw(raw_bad_length)


@pytest.fixture(name="raw_exchange1", scope="session")
def fixture_exchange1() -> bytes:
    "a valid exchange raw record"
    return b"2401" + b"840" + (b"14" * 7) + (b"1" * 59)


def test_init_bad_code(raw_exchange1: bytes, record: Exchange):
    "a bad code must raise an exception"
    raw = b"25" + raw_exchange1[2:]
    with pytest.raises(ValidationException):
        record.from_raw(raw)


@pytest.fixture(name="exchange1")
def fixture_exchange(raw_exchange1: bytes, record: Exchange):
    "a valid exchange object"
    record.from_raw(raw_exchange1)
    return record


def test_amount(exchange1: Exchange):
    "check 'amount' for exchange1"
    assert exchange1.amount == Decimal('141414141414.14')


def test_original_currency(exchange1: Exchange):
    "check 'currency' for exchange1"
    assert exchange1.original_currency.alpha_3 == "USD"


def test_default_currency(record: Exchange):
    "check 'currenct' for a default record"
    assert record.original_currency.alpha_3 == "EUR"


@pytest.mark.parametrize(
    "value",
    [3, "asdfalsjk", b"asdfalsjk", None],
    ids=["code", "string", "bytes", "None"]
)
def test_original_currency_set_invalid(record: Exchange, value):
    "an invalid source currency must raise an exception"
    with pytest.raises(ValueError):
        record.original_currency = value


@pytest.mark.parametrize("value", [
    978,
    "978",
    "eur",
    "EUR",
    b"EUR",
    pycountry.currencies.get(numeric="978")
])
def test_original_currency_set_euro(exchange1: Exchange, value):
    "different ways to set source currency to Euro"
    exchange1.original_currency = value

    assert exchange1.original_currency.numeric == "978"
    assert exchange1.original_currency.alpha_3 == "EUR"


@pytest.mark.parametrize("value,expected", [
    (12, Decimal("12")),
    (Decimal("12.07"), Decimal("12.07")),
    ("1212.08", Decimal("1212.08")),
    (b"1212.08", Decimal("1212.08")),
    ("123456789012.34", Decimal("123456789012.34")),
    (12.34, Decimal("12.34")),
])
def test_amount_set_valid(record: Exchange, value, expected):
    "check setting valid values to amount"
    record.amount = value
    assert record.amount == expected, (record.amount, expected)


@pytest.mark.parametrize("value", [
    None,
    "12345678901234"
])
def test_amount_set_invalid(record: Exchange, value):
    "setting an invalid value to amount must raise an exception"
    with pytest.raises(ValidationException):
        record.amount = value


def test_bytes(exchange1: Exchange, raw_exchange1: bytes):
    "bytes from object must be the same than the raw record"
    assert bytes(exchange1) == raw_exchange1


def test_iter(exchange1: Exchange, raw_exchange1: bytes):
    "iter from object must return the own raw record"
    records = list(exchange1)
    assert len(records) == 1
    assert records[0] == raw_exchange1
