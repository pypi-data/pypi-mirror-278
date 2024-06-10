#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations
import pytest

from ..aeb43.record.context import Aeb43Context
from ..aeb43.record.errors import ValidationException
from ..aeb43.item import Item


@pytest.fixture(name="default_record")
def fixture_default_record():
    "a default item"
    return Item()


@pytest.fixture(name="record")
def fixture_record(context: Aeb43Context):
    "a record"
    return Item(context=context)


def test_context(record: Item):
    "check if the item has a context"
    assert record.get_context() is not None


def test_context_default_record(default_record: Item):
    "default record must have a context"
    assert default_record.get_context() is not None


def test_default_bytes(record: Item, default_record: Item):
    "bytes for each record must be the same"
    assert bytes(default_record) == bytes(record)


@pytest.fixture(name="raw_bad_length", scope="session")
def fixture_raw_bad_length():
    "a bad raw record"
    return b"230001230405"


def test_constructor_bad_length(raw_bad_length):
    "creating a bad record should raise an exception"
    with pytest.raises(ValidationException):
        Item(raw=raw_bad_length)


def test_from_raw_bad_length(record, raw_bad_length):
    "assigning a bad record should raise an exception"
    with pytest.raises(ValidationException):
        record.from_raw(raw_bad_length)


@pytest.mark.parametrize("raw", [
    b"22" + (b"0" * 78),
    b"2306" + (b"0" * 76),
    b"2315" + (b"0" * 76)
])
def test_init_bad_code_str(record, raw):
    "a raw record with a bad code should trigger an error"
    with pytest.raises(ValidationException):
        record.from_raw(raw)


@pytest.fixture(name="raw_item1", scope="session")
def fixture_raw_item1():
    "a valid raw record"
    return b"2305" + (b"0" * 76)


@pytest.fixture(name="raw_item2", scope="session")
def fixture_raw_item2():
    "a valid raw record"
    return b"2305" + (b" " * 76)


@pytest.fixture(name="item", params=[
    "raw_item1",
    "raw_item2",
])
def fixture_item(record, request):
    "a valid item"
    raw = request.getfixturevalue(request.param)
    record.from_raw(raw)
    return record, raw


def test_record_code(item):
    "test record code value"
    obj, _ = item
    assert obj.record_code == 5


@pytest.mark.parametrize("value,expected", [
    (123, "123"),
    ("áéóüñç", "áéóüñç"),
    (b"asdfg hijk", "asdfg hijk"),
    ("0123456789ABCDEF G 0123456789ABCDEF G ", "0123456789ABCDEF G 0123456789ABCDEF G"),
    (b"0123456789ABCDEF G 0123456789ABCDEF G ", "0123456789ABCDEF G 0123456789ABCDEF G"),
    (None, "")
])
def test_optional_item1_set_valid(item, value, expected):
    "test setting optional item1"
    obj, _ = item
    obj.item1 = value
    assert obj.item1 == expected


def test_optional_item1_set_invalid(item):
    "setting optional item1 to an invalid content should raise an exception"
    obj, _ = item
    with pytest.raises(ValueError):
        obj.item1 = b"0" * 80


@pytest.mark.parametrize("value,expected", [
    (123, "123"),
    ("áéóüñç", "áéóüñç"),
    (b"asdfg hijk", "asdfg hijk"),
    ("0123456789ABCDEF G 0123456789ABCDEF G ", "0123456789ABCDEF G 0123456789ABCDEF G"),
    (b"0123456789ABCDEF G 0123456789ABCDEF G ", "0123456789ABCDEF G 0123456789ABCDEF G"),
    (None, "")
])
def test_optional_item2_set_valid(item, value, expected):
    "test setting vañod optional item2"
    obj, _ = item
    obj.item2 = value
    assert obj.item2 == expected


def test_bytes(item):
    "an item converte to bytes should be equal to the raw record"
    obj, raw = item
    assert bytes(obj) == raw


def test_iter(item):
    "an iterator over an item should return the raw record"
    obj, raw = item
    records = list(obj)
    assert len(records) == 1
    assert records[0] == raw
