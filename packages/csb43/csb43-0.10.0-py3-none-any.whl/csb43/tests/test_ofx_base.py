#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import datetime
import pytest
import pycountry

from ..ofx import base as ofx


@pytest.mark.parametrize("name,content,result", [
    ("tag", "12345", '<TAG>12345</TAG>'),
    ("tag", "", "<TAG></TAG>"),
    ("tag", None, ""),
    (None, None, ""),
    (None, "12345", ""),
])
def test_xml_element(name, content, result):
    "check xml_element"
    elm = ofx.xml_element(name, content)
    assert result == elm


@pytest.mark.parametrize("name,content,result", [
    ("tag", "12345", '<TAG>12345</TAG>'),
    ("tag", '', "<TAG></TAG>"),
    ("tag", None, ""),
    (None, None, ""),
    (None, "12345", ""),
])
def test_xml_aggregate(name, content, result):
    "check xml_aggregatet"
    elm = ofx.xml_aggregate(name, content)
    assert result == elm


@pytest.mark.parametrize("name,content,result", [
    ("tag", "12345", '<TAG>12345'),
    ("tag", "", "<TAG>"),
    ("tag", None, ""),
    (None, None, ""),
    (None, "12345", ""),
])
def test_sgml_element(name, content, result):
    "check sgml_element"
    elm = ofx.sgml_element(name, content)
    assert result == elm


@pytest.mark.parametrize("name,content,result", [
    ("tag", "12345", '<TAG>12345</TAG>'),
    ("tag", '', "<TAG></TAG>"),
    ("tag", None, ""),
    (None, None, ""),
    (None, "12345", ""),
])
def test_sgml_aggregate(name, content, result):
    "check sgml_aggregate"
    elm = ofx.sgml_aggregate(name, content)
    assert result == elm


@pytest.mark.parametrize("ivalue,ovalue", [
    ("aeiou", "aeiou"),
    ('s&m', 's&amp;m'),
    ('s<m', 's&lt;m'),
    ('s>m', 's&gt;m'),
])
def test_text_to_str(ivalue, ovalue):
    "check conversion from str to xml text"
    res = ofx.text_to_str(ivalue)
    assert ovalue == res


@pytest.mark.parametrize("value,ref", [
    (datetime.date(year=2004, month=3, day=1), "20040301"),
    (None, None),
])
def test_date_to_str(value, ref):
    "check date to str"
    outcome = ofx.date_to_str(value)
    assert outcome == ref


@pytest.mark.parametrize("value", [5])
def test_invalid_date_to_str(value):
    "invalid values to date_to_str"
    with pytest.raises(Exception):
        ofx.date_to_str(value)


@pytest.mark.parametrize("value,ref", [
    (True, "Y"),
    (False, "N"),
    (None, None),
    (5, "Y"),
    ("", "N"),
])
def test_bool_to_str(value, ref):
    assert ref == ofx.bool_to_str(value)


@pytest.mark.parametrize("value,ref", [
    (pycountry.currencies.get(alpha_3='EUR'), "EUR"),
    (None, None),
])
def test_currency_to_str(value, ref):
    assert ref == ofx.currency_to_str(value)


@pytest.mark.parametrize("value", [5])
def test_invalid_currency_to_str(value):
    with pytest.raises(Exception):
        ofx.currency_to_str(value)


def test_ofxobject_empty_init():
    ofx.OfxObject()


@pytest.mark.parametrize("value", [
    None,
    "1234",
    5,
])
def test_ofxobject_init(value):
    ofx.OfxObject(value)


@pytest.mark.parametrize("value", [
    "tag1", "tag2"
])
def test_ofxobject_tag_name(value):
    obj = ofx.OfxObject(value)
    assert value == obj.tag_name


def test_ofxobject_str():
    obj = ofx.OfxObject('tag')
    assert "" == str(obj)
