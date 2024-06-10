#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations
from typing import (
    Protocol,
)
from dataclasses import dataclass
import sys
import re

from .currency_data import CURRENCY_DATA


# pylint: disable=too-few-public-methods
class AnyCurrency(Protocol):
    "protocol for a currency object compatible with pycountry"
    alpha_3: str | None
    numeric: str | None


@dataclass(frozen=True)
class CurrencyLite(AnyCurrency):
    "cheap alternative to pycountry Currency"
    alpha_3: str | None
    numeric: str | None


__CUR_LETTER = {}
__CUR_NUMERIC = {}

for cod_let, cod_num in CURRENCY_DATA:
    __tmp = CurrencyLite(cod_let, cod_num)
    if cod_let:
        __CUR_LETTER[cod_let] = __tmp
    if cod_num:
        __CUR_NUMERIC[cod_num] = __tmp


try:
    import pycountry
    FROZEN_CURRENCY = hasattr(sys, "frozen")
except ImportError:
    FROZEN_CURRENCY = True


def currency_from_iso_number(numeric: str | None) -> AnyCurrency | None:
    """
    Return a currency object from a `numeric` ISO 4217 code.
    """
    if numeric is None:
        return None
    if FROZEN_CURRENCY:
        return __CUR_NUMERIC[numeric]
    return pycountry.currencies.get(numeric=numeric)


def currency_from_iso_letter(alpha_3: str) -> AnyCurrency:
    """
    Return a currency object from an `alpha_3` ISO 4217 code.
    """
    if FROZEN_CURRENCY:
        return __CUR_LETTER[alpha_3]
    return pycountry.currencies.get(alpha_3=alpha_3)


CUR_NUM = re.compile(r'^\d{3}$')
CUR_LET = re.compile(r'^[a-zA-Z]{3}$')


def currency_from_iso_code(code: str) -> AnyCurrency | None:
    """
    Return `AnyCurrency` from an ISO 4217 numeric or letter code
    Return None if no code was found
    """
    try:
        if CUR_NUM.match(code):
            return currency_from_iso_number(code)
        if CUR_LET.match(code):
            return currency_from_iso_letter(code)
    except KeyError:
        pass
    return None


def is_currency(obj) -> bool:
    "return True is `obj` is a currency object"
    if FROZEN_CURRENCY:
        return isinstance(obj, CurrencyLite)
    return isinstance(obj, (CurrencyLite, pycountry.db.Data))


def simplify_currency(obj: AnyCurrency) -> CurrencyLite:
    "convert currency to CurrencyLite"
    if isinstance(obj, CurrencyLite):
        return obj
    return CurrencyLite(alpha_3=obj.alpha_3, numeric=obj.numeric)


def yaml_currency_representer(dumper, obj: AnyCurrency):
    "a yaml representer for AnyCurrency"
    code = obj.numeric
    if code is None:
        return dumper.represent_none(None)
    return dumper.represent_str(code)
