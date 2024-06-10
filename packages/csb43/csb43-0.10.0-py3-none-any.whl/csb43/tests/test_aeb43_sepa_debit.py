#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations
import pytest

from ..aeb43 import sepa_debit as sd
from ..aeb43.record.context import Aeb43Context
from ..aeb43.record.errors import ValidationException


@pytest.fixture(name="raw1", scope="session")
def fixture_raw1():
    "raw item1"
    return b"2301COREAcme Mobile, S.L.U.                                                     "


@pytest.fixture(name="raw2", scope="session")
def fixture_raw2():
    "raw item2"
    return b"2302ES99999Z99999999                   2023999999999999                         "


@pytest.fixture(name="raw3", scope="session")
def fixture_raw3():
    "raw item3"
    return b"2303OTHR    ACMEMOBILE FACT. 777777777777777                                    "


@pytest.fixture(name="raw4", scope="session")
def fixture_raw4():
    "raw item4"
    return b"2304                                                                            "


@pytest.fixture(name="raw5", scope="session")
def fixture_raw5():
    "raw item5"
    return b"2305                                   XXXX YYYYYY                              "


@pytest.fixture(name="item1")
def fixture_item1(context: Aeb43Context, raw1):
    "item1"
    return sd.SepaDebitItem1(context=context, raw=raw1)


@pytest.fixture(name="item2")
def fixture_item2(context: Aeb43Context, raw2):
    "item2"
    return sd.SepaDebitItem2(context=context, raw=raw2)


@pytest.fixture(name="item3")
def fixture_item3(context: Aeb43Context, raw3):
    "item3"
    return sd.SepaDebitItem3(context=context, raw=raw3)


@pytest.fixture(name="item4")
def fixture_item4(context: Aeb43Context, raw4):
    "item4"
    return sd.SepaDebitItem4(context=context, raw=raw4)


@pytest.fixture(name="item5")
def fixture_item5(context: Aeb43Context, raw5):
    "item5"
    return sd.SepaDebitItem5(context=context, raw=raw5)


@pytest.fixture(name="debit1")
def fixture_debit1(context, raw1, raw2, raw3, raw4, raw5):
    "a composite SEPA debit record"
    return sd.SepaDebit(
        item1=raw1,
        item2=raw2,
        item3=raw3,
        item4=raw4,
        item5=raw5,
        context=context,
    )


@pytest.fixture(name="empty_debit")
def fixture_empty_debit(context):
    "an empty composite SEPA debit record"
    return sd.SepaDebit.new(context=context)


# scheme code
###############

def test_scheme_code_item1(item1: sd.SepaDebitItem1):
    assert item1.scheme_code == "CORE"


def test_scheme_code_debit1(debit1: sd.SepaDebit):
    assert debit1.scheme_code == "CORE"


@pytest.mark.parametrize("value,ref", [
    ("CORE", "CORE"),
    (" CORE ", "CORE"),
    (b"CORE", "CORE"),
    (b"  CORE ", "CORE"),
    ("B2B", "B2B"),
    (" B2B ", "B2B"),
    (b"B2B", "B2B"),
    (b" B2B ", "B2B"),
], ids=repr)
def test_set_valid_scheme_code(empty_debit, value, ref):
    empty_debit.scheme_code = value
    assert empty_debit.item1.scheme_code == ref
    assert empty_debit.scheme_code == ref


@pytest.mark.parametrize("value", [
    "ASDF",
    "ASDFE",
    1,
    "",
    "   ",
    b"    ",
    b""
])
def test_set_invalid_scheme_code(empty_debit, value):
    with pytest.raises(ValidationException):
        empty_debit.scheme_code = value


# creditor name
################

def test_creditor_name_item1(item1: sd.SepaDebitItem1):
    assert item1.creditor_name == "Acme Mobile, S.L.U."


def test_creditor_name_debit1(debit1: sd.SepaDebitItem1):
    assert debit1.creditor_name == "Acme Mobile, S.L.U."


@pytest.mark.parametrize("value,ref", [
    (" Word1 Word2 ", "Word1 Word2"),
    ("Word1 Word2", "Word1 Word2"),
    (b" Word1 Word2 ", "Word1 Word2"),
    (b"Word1 Word2", "Word1 Word2"),
    (1234, "1234"),
    ("", ""),
    (" ", ""),
])
def test_set_valid_creditor_name(empty_debit, value, ref):
    empty_debit.creditor_name = value
    assert empty_debit.item1.creditor_name == ref
    assert empty_debit.creditor_name == ref


@pytest.mark.parametrize("value", [
    "A" * 71,
    b"A" * 71,
])
def test_set_invalid_creditor_name(empty_debit, value):
    with pytest.raises(ValidationException):
        empty_debit.creditor_name = value


# creditor id
##############

def test_creditor_id_item2(item2: sd.SepaDebitItem2):
    assert item2.creditor_id == "ES99999Z99999999"


def test_creditor_id_debit1(debit1: sd.SepaDebit):
    assert debit1.creditor_id == "ES99999Z99999999"


@pytest.mark.parametrize("value,ref", [
    ("AB123456789", "AB123456789"),
    (" AB123456789 ", "AB123456789"),
    (b"AB123456789", "AB123456789"),
    (b" AB123456789 ", "AB123456789"),
    (1234567890, "1234567890"),
    ("", ""),
    ("  ", ""),
    (b" ", ""),
], ids=repr)
def test_set_valid_creditor_id(empty_debit, value, ref):
    empty_debit.creditor_id = value
    assert empty_debit.item2.creditor_id == ref
    assert empty_debit.creditor_id == ref


@pytest.mark.parametrize("value", [
    "1" * 36,
    b"1" * 36,
])
def test_set_invalid_creditor_id(empty_debit, value):
    with pytest.raises(ValidationException):
        empty_debit.creditor_id = value


# mandate reference
####################

def test_mandate_reference_item2(item2: sd.SepaDebitItem2):
    assert item2.mandate_reference == "2023999999999999"


def test_mandate_reference_debit1(debit1: sd.SepaDebit):
    assert debit1.mandate_reference == "2023999999999999"


@pytest.mark.parametrize("value,ref", [
    ("AB123456789", "AB123456789"),
    (" AB123456789 ", "AB123456789"),
    (b"AB123456789", "AB123456789"),
    (b" AB123456789 ", "AB123456789"),
    (1234567890, "1234567890"),
    ("", ""),
    ("  ", ""),
    (b" ", ""),
], ids=repr)
def test_set_valid_mandate_reference(empty_debit, value, ref):
    empty_debit.mandate_reference = value
    assert empty_debit.item2.mandate_reference == ref
    assert empty_debit.mandate_reference == ref


@pytest.mark.parametrize("value", [
    "1" * 36,
    b"1" * 36,
])
def test_set_invalid_mandate_reference(empty_debit, value):
    with pytest.raises(ValidationException):
        empty_debit.mandate_reference = value


# purpose
##########

def test_purpose_item3(item3: sd.SepaDebitItem3):
    assert item3.purpose == "OTHR"


def test_purpose_debit1(debit1: sd.SepaDebit):
    assert debit1.purpose == "OTHR"


@pytest.mark.parametrize("value,ref", [
    ("ABCD", "ABCD"),
    ("1234", "1234"),
    (" ABCD ", "ABCD"),
    (1234, "1234"),
    ("", ""),
    (" ", ""),
    (b"ABCD", "ABCD"),
    (b"1234", "1234"),
    (b" ABCD ", "ABCD"),
    (b"", ""),
    (b" ", ""),
], ids=repr)
def test_set_valid_purpose(empty_debit, value, ref):
    empty_debit.purpose = value
    assert empty_debit.item3.purpose == ref
    assert empty_debit.purpose == ref


@pytest.mark.parametrize("value", [
    "1" * 5,
    b"1" * 5,
    12345,
])
def test_set_invalid_purpose(empty_debit, value):
    with pytest.raises(ValidationException):
        empty_debit.purpose = value


# purpose category

def test_purpose_category_item3(item3: sd.SepaDebitItem3):
    assert item3.purpose_category == ""


def test_purpose_category_debit1(debit1: sd.SepaDebit):
    assert debit1.purpose_category == ""


@pytest.mark.parametrize("value,ref", [
    ("ABCD", "ABCD"),
    ("1234", "1234"),
    (" ABCD ", "ABCD"),
    (1234, "1234"),
    ("", ""),
    (" ", ""),
    (b"ABCD", "ABCD"),
    (b"1234", "1234"),
    (b" ABCD ", "ABCD"),
    (b"", ""),
    (b" ", ""),
], ids=repr)
def test_set_valid_purpose_category(empty_debit, value, ref):
    empty_debit.purpose_category = value
    assert empty_debit.item3.purpose_category == ref
    assert empty_debit.purpose_category == ref


@pytest.mark.parametrize("value", [
    "1" * 5,
    b"1" * 5,
    12345,
], ids=repr)
def test_set_invalid_purpose_category(empty_debit, value):
    with pytest.raises(ValidationException):
        empty_debit.purpose_category = value


# remitance information

def test_remitance_information_item3(item3: sd.SepaDebitItem3):
    assert item3.remitance_information == "ACMEMOBILE FACT. 777777777777777"


def test_remitance_information_debit1(debit1: sd.SepaDebit):
    assert debit1.remitance_information == "ACMEMOBILE FACT. 777777777777777"


def test_remitance_information_cont_item4(item4: sd.SepaDebitItem4):
    assert item4.remitance_information_cont == ""


@pytest.mark.parametrize("value,ref,ref1,ref2", [
    ("A1B2C3D4", "A1B2C3D4", "A1B2C3D4", ""),
    (" A1B2C3D4 ", "A1B2C3D4", "A1B2C3D4", ""),
    (b"A1B2C3D4", "A1B2C3D4", "A1B2C3D4", ""),
    (b" A1B2C3D4 ", "A1B2C3D4", "A1B2C3D4", ""),
    ("A" * 67 + "  " + "B" * 20, "A" * 67 + "  " + "B" * 20, "A" * 67, "B" * 20),
    ("A" * (68 + 72), "A" * (68 + 72), "A" * 68, "A" * 72),
], ids=repr)
def test_set_valid_remitance_information(empty_debit, value, ref, ref1, ref2):
    empty_debit.remitance_information = value
    assert empty_debit.remitance_information == ref
    assert empty_debit.item3.remitance_information == ref1
    assert empty_debit.item4.remitance_information_cont == ref2


@pytest.mark.parametrize("value", [
    "A" * (68 + 72 + 1),
    b"A" * (68 + 72 + 1),
], ids=repr)
def test_set_invalid_remitance_information(empty_debit, value):
    with pytest.raises(ValidationException):
        empty_debit.remitance_information = value


# creditor reference

def test_creditor_reference_item5(item5: sd.SepaDebitItem5):
    assert item5.creditor_reference == ""


def test_creditor_reference_debit1(debit1: sd.SepaDebit):
    assert debit1.creditor_reference == ""


@pytest.mark.parametrize("value,ref", [
    ("AB123456789", "AB123456789"),
    (" AB123456789 ", "AB123456789"),
    (b"AB123456789", "AB123456789"),
    (b" AB123456789 ", "AB123456789"),
    (1234567890, "1234567890"),
    ("", ""),
    ("  ", ""),
    (b" ", ""),
], ids=repr)
def test_set_valid_creditor_reference(empty_debit, value, ref):
    empty_debit.creditor_reference = value
    assert empty_debit.item5.creditor_reference == ref
    assert empty_debit.creditor_reference == ref


@pytest.mark.parametrize("value", [
    "1" * 36,
    b"1" * 36,
])
def test_set_invalid_creditor_reference(empty_debit, value):
    with pytest.raises(ValidationException):
        empty_debit.creditor_reference = value


# debtor name

def test_debtor_name_item5(item5: sd.SepaDebitItem5):
    assert item5.debtor_name == "XXXX YYYYYY"


def test_debtor_name_debit1(debit1: sd.SepaDebit):
    assert debit1.debtor_name == "XXXX YYYYYY"


@pytest.mark.parametrize("value,ref", [
    ("AB123456789", "AB123456789"),
    (" AB123456789 ", "AB123456789"),
    (b"AB123456789", "AB123456789"),
    (b" AB123456789 ", "AB123456789"),
    (1234567890, "1234567890"),
    ("", ""),
    ("  ", ""),
    (b" ", ""),
], ids=repr)
def test_set_valid_debtor_name(empty_debit, value, ref):
    empty_debit.debtor_name = value
    assert empty_debit.item5.debtor_name == ref
    assert empty_debit.debtor_name == ref


@pytest.mark.parametrize("value", [
    "1" * 42,
    b"1" * 42,
])
def test_set_invalid_debtor_name(empty_debit, value):
    with pytest.raises(ValidationException):
        empty_debit.debtor_name = value


def test_iter(debit1: sd.SepaDebit, raw1, raw2, raw3, raw4, raw5):
    assert tuple(debit1) == (raw1, raw2, raw3, raw4, raw5)

