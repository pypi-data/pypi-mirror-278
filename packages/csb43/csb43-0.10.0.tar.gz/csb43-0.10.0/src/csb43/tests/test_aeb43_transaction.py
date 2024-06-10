#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations

from decimal import Decimal
from datetime import datetime
from datetime import date

import pytest

from ..aeb43.record.context import Aeb43Context
from ..aeb43.record.errors import (
    ValidationException,
    ValidationWarning,
)
from ..aeb43.transaction import Transaction
from ..aeb43.exchange import Exchange
from ..aeb43.item import Item
from ..aeb43.sepa_transfer import SepaTransfer
from ..aeb43.sepa_debit import SepaDebit


@pytest.fixture(name="strict_record")
def fixture_strict_record(strict_context: Aeb43Context) -> Transaction:
    "an item with a strict context"
    return Transaction(context=strict_context)


@pytest.fixture(name="default_record")
def fixture_default_record() -> Transaction:
    "a default item"
    return Transaction()


@pytest.fixture(name="non_strict_record")
def fixture_non_strict_record(non_strict_context: Aeb43Context) -> Transaction:
    "an item with a non strict context"
    return Transaction(context=non_strict_context)


@pytest.fixture(name="record")
def fixture_record(context: Aeb43Context) -> Transaction:
    "a transaction object"
    return Transaction(context=context)


@pytest.fixture(name="mode1_record")
def fixture_mode1_record(mode1_context: Aeb43Context) -> Transaction:
    "an exchange object"
    return Transaction(context=mode1_context)


@pytest.fixture(name="mode2_record")
def fixture_mode2_record(mode2_context: Aeb43Context) -> Transaction:
    "an exchange object"
    return Transaction(context=mode2_context)


@pytest.fixture(name="mode3_record")
def fixture_mode3_record(mode3_context: Aeb43Context) -> Transaction:
    "an exchange object"
    return Transaction(context=mode3_context)


def test_context(record: Transaction):
    "each record must have a context"
    assert record.get_context() is not None


def test_context_default_record(default_record: Transaction):
    "default record must have a context"
    assert default_record.get_context() is not None


def test_to_dict(record: Transaction):
    "`to_dict` method must not fail"
    res = record.to_dict()
    assert res
    assert isinstance(res, dict)


@pytest.fixture(name="raw_bad_length", scope="session")
def fixture_raw_bad_length() -> bytes:
    "a bad raw record"
    return b"22011023402150"


def test_constructor_bad_length(raw_bad_length: bytes):
    "creating a bad record should raise an exception"
    with pytest.raises(ValidationException):
        Transaction(raw=raw_bad_length)


def test_from_raw_bad_length(record: Transaction, raw_bad_length: bytes):
    "assigning a bad record should raise an exception"
    with pytest.raises(ValidationException):
        record.from_raw(raw_bad_length)


@pytest.fixture(name="raw_item1", scope="session")
def fixture_raw_item() -> bytes:
    "a valid raw record"
    return b"22" + (b"0" * 25) + b"1" + (b"0" * 52)


def test_init_bad_code_str(record: Transaction, raw_item1: bytes):
    "a raw record with a bad code should trigger an error"
    raw = b"23" + raw_item1[2:]
    with pytest.raises(ValidationException):
        record.from_raw(raw)


def test_init(record: Transaction, raw_item1: bytes):
    "construct a valid transaction"
    record.from_raw(raw_item1)


def test_from_raw(record: Transaction, raw_item1: bytes):
    "updating a record from raw"
    record.from_raw(raw_item1)


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
def test_valid_amount(record: Transaction, amount, ref):
    "check the amount property"
    record.amount = amount
    assert record.amount == ref


@pytest.mark.parametrize("amount", [
    "12345" * 4,
    b"12345" * 4,
    b"asdagsa",
    "asdagsa",
    "asdagsa" * 4,
], ids=repr)
def test_invalid_amount(record: Transaction, amount):
    "an invalid amount must raise an exception"
    with pytest.raises(ValueError):
        record.amount = amount


def _get_mode23_valid_branch_code():
    return [
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
    ]


@pytest.mark.parametrize("value,ref", _get_mode23_valid_branch_code(), ids=repr)
def test_valid_branch_code_mode2(mode2_record: Transaction, value, ref):
    "set the branch code"
    mode2_record.branch_code = value
    assert mode2_record.branch_code == ref


@pytest.mark.parametrize("value,ref", _get_mode23_valid_branch_code(), ids=repr)
def test_valid_branch_code_mode3(mode3_record: Transaction, value, ref):
    "set the branch code"
    mode3_record.branch_code = value
    assert mode3_record.branch_code == ref


@pytest.mark.parametrize("value,ref", [
    ("1234", "1234"),
    (b"1234", "1234"),
    (1234, "1234"),
    (1, "0001"),
    ("1", "0001"),
    (0, "0000"),
    ("0", "0000"),
    ("", ""),
    (None, ""),
    (b"", ""),
    (b"    ", ""),
], ids=repr)
def test_valid_branch_code_mode1(mode1_record: Transaction, value, ref):
    "set the branch code"
    mode1_record.branch_code = value
    assert mode1_record.branch_code == ref


@pytest.mark.parametrize("value,warning", [
    ("12345", False),
    ("asdf", True),
], ids=repr)
def test_invalid_branch_code(record: Transaction, value, warning):
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
def test_valid_document_number(record: Transaction, value, ref):
    "set the document number"
    record.document_number = value
    assert record.document_number == ref


@pytest.mark.parametrize("value,warning", [
    ("asdfa", True),
    ("1" * 11, False),
    ("1" * 15, False),
    (1234567890123, False),
], ids=repr)
def test_invalid_document_number(record: Transaction, value, warning):
    "setting an invalid branch must raise an exception"
    is_warning = not record.get_context().strict and warning
    if is_warning:
        with pytest.warns(ValidationWarning):
            record.document_number = value
    else:
        with pytest.raises(ValidationException):
            record.document_number = value


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
def test_valid_transaction_date(record: Transaction, value, ref):
    "set the transaction date"
    record.transaction_date = value
    assert record.transaction_date == ref


@pytest.mark.parametrize("value", _get_invalid_dates(), ids=repr)
def test_invalid_transaction_date(record: Transaction, value):
    "setting and invalid date must raise an exception"
    with pytest.raises(ValidationException):
        record.transaction_date = value


@pytest.mark.parametrize("value,ref", _get_valid_dates(), ids=repr)
def test_valid_value_date(record: Transaction, value, ref):
    "set the effective date"
    record.value_date = value
    assert record.value_date == ref


@pytest.mark.parametrize("value", _get_invalid_dates(), ids=repr)
def test_invalid_value_date(record: Transaction, value):
    "setting and invalid date must raise an exception"
    with pytest.raises(ValidationException):
        record.value_date = value


@pytest.mark.parametrize("value,ref", [
    (1, 1),
    ("1", 1),
    (b"1", 1),
    ("01", 1),
    (123, 123),
    ("123", 123),
    (b"123", 123),
], ids=repr)
def test_valid_own_item(record: Transaction, value, ref):
    "own item"
    record.own_item = value
    assert record.own_item == ref


@pytest.mark.parametrize("value", [
    "abc",
    "1234",
    1234,
    "",
    b"",
    None,
], ids=repr)
def test_invalid_own_item(record: Transaction, value):
    "own item"
    with pytest.raises(ValidationException):
        record.own_item = value


@pytest.mark.parametrize("value,ref", [
    (1, 1),
    ("1", 1),
    (b"1", 1),
    ("01", 1),
    (12, 12),
    ("12", 12),
    (b"12", 12),
    (" 12 ", 12),
    (b" 12 ", 12),
], ids=repr)
def test_valid_shared_item(record: Transaction, value, ref):
    "shared item"
    record.shared_item = value
    assert record.shared_item == ref


@pytest.mark.parametrize("value", [
    "ab",
    "123",
    123,
    "",
    b"",
    None,
], ids=repr)
def test_invalid_shared_item(record: Transaction, value):
    "own item"
    with pytest.raises(ValidationException):
        record.shared_item = value


def _valid_mode12_reference1():
    return [
        ('0123456789ab', '0123456789ab'),
        (' 1234       ', '1234'),
        (b'0123456789ab', '0123456789ab'),
        (b'012345678900', '012345678900'),
    ]


@pytest.mark.parametrize("value,ref", _valid_mode12_reference1(), ids=repr)
def test_valid_reference1_mode1(mode1_record: Transaction, value, ref):
    "reference1 must not trigger validation warning or error in mode 1 or 2"
    mode1_record.reference1 = value
    assert mode1_record.reference1 == ref


@pytest.mark.parametrize("value,ref", _valid_mode12_reference1(), ids=repr)
def test_valid_reference1_mode2(mode2_record: Transaction, value, ref):
    "reference1 must not trigger validation warning or error in mode 1 or 2"
    mode2_record.reference1 = value
    assert mode2_record.reference1 == ref


@pytest.mark.parametrize("value,ref", [
    (b"012345678900", "012345678900"),
    ("012345678900", "012345678900"),
    ("12345678900", "012345678900"),
    (b" 012345678900 ", "012345678900"),
    (" 012345678900 ", "012345678900"),
    (" 12345678900 ", "012345678900"),
], ids=repr)
def test_valid_reference1_mode3(mode3_record: Transaction, value, ref):
    "mode3 reference1 must match control digit"
    mode3_record.reference1 = value
    assert mode3_record.reference1 == ref


@pytest.mark.parametrize("value,ref", [
    (12345, "12345"),
    ("12345", "12345"),
    ("asdfa123", "asdfa123"),
    (12345, "12345"),
    (" 12345 ", "12345"),
    (" asdfa123 ", "asdfa123"),
    (None, ""),
    ("", ""),
    (b"1234", "1234"),
    (" " * 17, ""),
    (b" " * 17, ""),
], ids=repr)
def test_valid_reference2(record: Transaction, value, ref):
    "reference2"
    record.reference2 = value
    assert record.reference2 == ref


@pytest.mark.parametrize("value", [
    "1" * 17,
    b"1" * 17,
], ids=repr)
def test_invalid_reference2(record: Transaction, value):
    "invalid reference 2 value"
    with pytest.raises(ValidationException):
        record.reference2 = value


def test_unset_exchange(record: Transaction):
    "check that there is not exchange record"
    assert record.exchange is None


@pytest.fixture(name="raw_exchange1")
def fixture_exchange1():
    "a valid exchange raw record"
    return b"2401" + b"840" + (b"14" * 7) + (b"1" * 59)


def test_set_raw_exchange(record: Transaction, raw_exchange1):
    "set an exchange record from raw"
    record.exchange = raw_exchange1
    assert isinstance(record.exchange, Exchange)
    assert bytes(record.exchange) == raw_exchange1


def test_append_raw_exchange(record: Transaction, raw_exchange1):
    "set an exchange record from raw"
    record.append(raw_exchange1)
    assert isinstance(record.exchange, Exchange)
    assert bytes(record.exchange) == raw_exchange1


def test_set_object_exchange(record: Transaction, raw_exchange1):
    "set an exchange record from object"
    obj = Exchange(raw=raw_exchange1)
    record.exchange = obj
    assert record.exchange is obj


@pytest.fixture(name="item")
def fixture_item():
    "an optional item"
    item = Item()
    item.record_code = 1
    item.item1 = "AA"
    item.item2 = "BB"
    return item


def test_add_optional_1item(record: Transaction, item: Item):
    "add one object item"
    assert record.optional_items is not None
    record.optional_items.append(item)
    assert len(record.optional_items) == 1
    assert isinstance(record.optional_items[0], Item)


def test_add_optional_1rawitem(record: Transaction, item: Item):
    "add one raw item"
    assert record.optional_items is not None
    record.optional_items.append(bytes(item))
    assert len(record.optional_items) == 1
    assert isinstance(record.optional_items[0], Item)


def test_add_optional_5rawitems(record: Transaction, item: Item):
    "add 5 raw items"
    assert record.optional_items is not None
    for idx in range(5):
        item.record_code = idx + 1
        record.optional_items.append(bytes(item))
    assert record.sepa_debit or record.sepa_transfer or (len(record.optional_items) == 5)
    for idx, oitem in enumerate(record.optional_items):
        assert oitem.record_code == idx + 1


def test_accepts_nested_codes_item(record: Transaction, item: Item):
    """a transaction must accept items if there are no sepa objects
    and there is less than 5 items
    """
    for idx in range(5):
        item.record_code = idx + 1
        assert record.accepts_nested_codes(bytes(item))


def test_accepts_nested_codes_full_items(record: Transaction, item: Item):
    """a transaction must accept items if there are no sepa objects
    and there is less than 5 items
    """
    assert record.optional_items is not None
    for idx in range(5):
        item.record_code = idx + 1
        record.optional_items.append(bytes(item))
    assert record.sepa_debit or record.sepa_transfer or not record.accepts_nested_codes(bytes(item))


@pytest.fixture(name="sepa_transfer")
def fixture_sepa_transfer():
    "a sepa transfer"
    return SepaTransfer.new()


def test_add_sepa_transfer(record: Transaction, sepa_transfer: SepaTransfer):
    "add a sepa transfer"
    record.sepa_transfer = sepa_transfer
    assert len(record.optional_items or []) == 0
    assert not record.sepa_debit
    assert record.sepa_transfer is sepa_transfer


def test_convert_sepa_transfer(record: Transaction, sepa_transfer: SepaTransfer):
    "convert optional items to sepa transfer"
    assert record.optional_items is not None
    for raw in sepa_transfer:
        record.optional_items.append(raw)
    if record.get_context().sepa:
        assert record.sepa_transfer is not None
        assert not record.sepa_debit
        assert not record.optional_items
    else:
        assert not record.sepa_transfer
        assert not record.sepa_debit
        assert len(record.optional_items or []) == 5


@pytest.fixture(name="sepa_debit")
def fixture_sepa_debit():
    "a sepa transfer"
    return SepaDebit.new()


def test_add_sepa_debit(record: Transaction, sepa_debit: SepaDebit):
    "add a sepa debit"
    record.sepa_debit = sepa_debit
    assert len(record.optional_items or []) == 0
    assert not record.sepa_transfer
    assert record.sepa_debit is sepa_debit


def test_convert_sepa_debit(record: Transaction, sepa_debit: SepaDebit):
    "convert optional items to sepa debit"
    assert record.optional_items is not None
    for raw in sepa_debit:
        record.optional_items.append(raw)
    if record.get_context().sepa:
        assert record.sepa_debit is not None
        assert not record.sepa_transfer
        assert not record.optional_items
    else:
        assert not record.sepa_transfer
        assert not record.sepa_debit
        assert len(record.optional_items or []) == 5
