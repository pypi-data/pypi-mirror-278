#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations
import pytest

from ..aeb43 import sepa_transfer as sd
from ..aeb43.record.errors import ValidationException


@pytest.fixture(name="transfer")
def fixture_transfer(context):
    "an empty composite SEPA transfer record"
    return sd.SepaTransfer.new(context=context)


@pytest.mark.parametrize("value,ref", [
    (" Word1 Word2 ", "Word1 Word2"),
    ("Word1 Word2", "Word1 Word2"),
    (b" Word1 Word2 ", "Word1 Word2"),
    (b"Word1 Word2", "Word1 Word2"),
    (1234, "1234"),
    ("a" * 66, "a" * 66),
    ("", ""),
    (" ", ""),
], ids=repr)
def test_set_valid_originator_name(transfer, value, ref):
    transfer.originator_name = value
    assert transfer.item1.originator_name == ref
    assert transfer.originator_name == ref


@pytest.mark.parametrize("value", [
    "A" * 67,
    b"A" * 67,
], ids=repr)
def test_set_invalid_originator_name(transfer, value):
    with pytest.raises(ValidationException):
        transfer.originator_name = value


@pytest.mark.parametrize("value,ref", [
    (" Word Word ", "Word Word"),
    ("Word Word", "Word Word"),
    (b" Word Word ", "Word Word"),
    (b"Word Word", "Word Word"),
    (1234, "1234"),
    ("a" * 10, "a" * 10),
    ("", ""),
    (" ", ""),
], ids=repr)
def test_set_valid_originator_code(transfer, value, ref):
    transfer.originator_code = value
    assert transfer.item1.originator_code == ref
    assert transfer.originator_code == ref


@pytest.mark.parametrize("value", [
    "A" * 11,
    b"A" * 11,
], ids=repr)
def test_set_invalid_originator_code(transfer, value):
    with pytest.raises(ValidationException):
        transfer.originator_code = value


@pytest.mark.parametrize("value,ref", [
    (" Word1 Word2 ", "Word1 Word2"),
    ("Word1 Word2", "Word1 Word2"),
    (b" Word1 Word2 ", "Word1 Word2"),
    (b"Word1 Word2", "Word1 Word2"),
    (1234, "1234"),
    ("a" * 35, "a" * 35),
    ("", ""),
    (" ", ""),
])
def test_set_valid_originator_reference(transfer, value, ref):
    transfer.originator_reference = value
    assert transfer.item2.originator_reference == ref
    assert transfer.originator_reference == ref


@pytest.mark.parametrize("value", [
    "A" * 36,
    b"A" * 36,
], ids=repr)
def test_set_invalid_originator_reference(transfer, value):
    with pytest.raises(ValidationException):
        transfer.originator_reference = value


@pytest.mark.parametrize("value,ref", [
    (" Word1 Word2 ", "Word1 Word2"),
    ("Word1 Word2", "Word1 Word2"),
    (b" Word1 Word2 ", "Word1 Word2"),
    (b"Word1 Word2", "Word1 Word2"),
    (1234, "1234"),
    ("a" * 41, "a" * 41),
    ("", ""),
    (" ", ""),
], ids=repr)
def test_set_valid_originator_reference_party(transfer, value, ref):
    transfer.originator_reference_party = value
    assert transfer.item2.originator_reference_party == ref
    assert transfer.originator_reference_party == ref


@pytest.mark.parametrize("value", [
    "A" * 42,
    b"A" * 42,
], ids=repr)
def test_set_invalid_originator_reference_party(transfer, value):
    with pytest.raises(ValidationException):
        transfer.originator_reference_party = value


@pytest.mark.parametrize("value,ref", [
    (" Word1 Word2 ", "Word1 Word2"),
    ("Word1 Word2", "Word1 Word2"),
    (b" Word1 Word2 ", "Word1 Word2"),
    (b"Word1 Word2", "Word1 Word2"),
    (1234, "1234"),
    ("a" * 76, "a" * 76),
    ("", ""),
    (" ", ""),
], ids=repr)
def test_set_valid_additional_info(transfer, value, ref):
    transfer.additional_info = value
    assert transfer.item5.additional_info == ref
    assert transfer.additional_info == ref


@pytest.mark.parametrize("value", [
    "A" * 77,
    b"A" * 77,
], ids=repr)
def test_set_invalid_additional_info(transfer, value):
    with pytest.raises(ValidationException):
        transfer.additional_info = value


@pytest.mark.parametrize("value,ref,ref1,ref2", [
    ("A1B2C3D4", "A1B2C3D4", "A1B2C3D4", ""),
    (" A1B2C3D4 ", "A1B2C3D4", "A1B2C3D4", ""),
    (b"A1B2C3D4", "A1B2C3D4", "A1B2C3D4", ""),
    (b" A1B2C3D4 ", "A1B2C3D4", "A1B2C3D4", ""),
    ("A" * 67 + "  " + "B" * 20, "A" * 67 + "  " + "B" * 20, "A" * 67, "B" * 20),
    ("A" * (68 + 72), "A" * (68 + 72), "A" * 68, "A" * 72),
], ids=repr)
def test_set_valid_remitance_information(transfer, value, ref, ref1, ref2):
    transfer.remitance_information = value
    assert transfer.remitance_information == ref
    assert transfer.item3.remitance_information == ref1
    assert transfer.item4.remitance_information_cont == ref2


@pytest.mark.parametrize("value", [
    "A" * (68 + 72 + 1),
    b"A" * (68 + 72 + 1),
], ids=repr)
def test_set_invalid_remitance_information(transfer, value):
    with pytest.raises(ValidationException):
        transfer.remitance_information = value


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
def test_set_valid_purpose(transfer, value, ref):
    transfer.purpose = value
    assert transfer.item3.purpose == ref
    assert transfer.purpose == ref


@pytest.mark.parametrize("value", [
    "1" * 5,
    b"1" * 5,
    12345,
], ids=repr)
def test_set_invalid_purpose(transfer, value):
    with pytest.raises(ValidationException):
        transfer.purpose = value


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
def test_set_valid_purpose_category(transfer, value, ref):
    transfer.purpose_category = value
    assert transfer.item3.purpose_category == ref
    assert transfer.purpose_category == ref


@pytest.mark.parametrize("value", [
    "1" * 5,
    b"1" * 5,
    12345,
], ids=repr)
def test_set_invalid_purpose_category(transfer, value):
    with pytest.raises(ValidationException):
        transfer.purpose_category = value