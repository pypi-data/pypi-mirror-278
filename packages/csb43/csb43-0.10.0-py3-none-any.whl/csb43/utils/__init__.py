# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

# -*- coding: utf-8 -*-
'''
.. note::

    license: GNU Lesser General Public License v3.0 (see LICENSE)
'''
from __future__ import annotations
from typing import (
    Union,
    TypeVar,
)
import re
import datetime
import functools
from decimal import Decimal
import warnings

from deprecated.sphinx import deprecated

from ..i18n import tr as _
from . import currency
#import pycountry


T = TypeVar('T')
AnyString = Union[str, bytes]


class BytesMixin:

    def __str__(self) -> str:
        return self.__unicode__()

    def __bytes__(self) -> bytes:
        raise NotImplementedError("__bytes__")

    def __unicode__(self) -> str:
        raise NotImplementedError("__unicode__")


class Message(BytesMixin):

    def __init__(self, message: AnyString):
        self.message = message

    def __unicode__(self):
        if isinstance(self.message, bytes):
            return self.message.decode("utf-8")
        return self.message

    def __bytes__(self):
        if isinstance(self.message, str):
            return self.message.encode("utf-8")
        return self.message


class Csb43Exception(Message, Exception):
    pass


class Csb43Warning(Message, UserWarning):
    pass


def raiseCsb43Exception(
    value='',
    strict=False,
    silent=False,
    line: int | None = None,
    **kwargs
):
    '''
    raise a :class:`Csb43Exception` or print the exception's message to \
    standard error

    :param value: message of the exception
    :param strict: print to standard error instead of raising an exception if \
    not `strict`

    :raises: :class:`Csb43Exception`
    '''
    #exc = Csb43Exception(value)
    if line is not None:
        value = f"[{line:04d}] {value}"
    if strict:
        raise Csb43Exception(value)
    if not silent:
        warnings.warn(Csb43Warning(value))


def check_string(pattern='', field='', strict=True, **csbexc):
    '''
    :param pattern: pattern description using regular expressions
    :type  pattern: :class:`basestring`

    :param field: variable to be checked

    :param strict: treat exceptions as warnings if `False`
    :type  strict: :class:`bool`

    :raises: :class:`Csb43Exception` if `field` doesn't match `pattern` and \
    `strict` is `True`
    '''

    if len(re.findall(pattern, field)) != 1:
        raiseCsb43Exception(
            _(
                "Bad format: content {content!r} mismatches the "
                "expected format r{pattern!r} for this field"
            ).format(content=field, pattern=pattern),
            strict=strict,
            **csbexc
        )


def check_strict(pattern: AnyString):
    """
    .. note::

        decorator

    :param pattern: pattern description using regular expressions
    :type  pattern: :class:`basestring`

    :param field: variable to be checked

    :param strict: treat exceptions as warnings if `False`
    :type  strict: :class:`bool`

    :raises: :class:`Csb43Exception` if `field` doesn't match `pattern` and \
    `strict` is `True`
    """
    def _decorator(f):

        @functools.wraps(f)
        def _wrapped(self, *args, **kw):
            check_string(pattern, *args, **kw)
            return f(self, *args, **kw)

        return _wrapped

    return _decorator


DECIMAL = 2
DATEFORMAT = ["%d%m%y", "%y%m%d"]


def raw2currency(
    value: str | bytes | int,
    decimal: int = DECIMAL,
    debit: str | bytes = '2'
) -> Decimal:
    '''
    Format the CSB composite type for amounts as a real number

    Args:
        value (long or str) -- absolute amount without decimal separator
        decimal (int)       -- number of digits reserved for decimal numbers
        debit ('1','2')     -- '1' debit, '2' credit

    Return:
        (float) the amount as a real number

    Examples:

    >>> raw2currency('123456')
    Decimal('1234.56')
    >>> raw2currency('12345',debit='1')
    Decimal('-123.45')

    '''
    val = -int(value) if int(debit) == 1 else int(value)
    return (Decimal(val) / Decimal(10 ** decimal))


def currency2raw(
    value: float | int | Decimal,
    decimal: int = DECIMAL
) -> tuple[int, str]:
    '''
    Convert a real to the CSB amount format

    Args:
        value (float) -- quantity as a real number
        decimal (int) -- number of digits reserved for decimal numbers

    Return:
        tuple of absolute amount and debit flag

    Examples:

    >>> currency2raw(-123.456)
    (12345, '1')
    >>> currency2raw(123.45)
    (12345, '2')
    '''
    return (
        abs(int(value * (10 ** decimal))),
        '1' if value < 0 else '2'
    )


def raw2date(value: str, yearFirst=True) -> datetime.date:
    '''
    Convert the CSB date format to a datetime.date object

    Args:
        value (str)      -- date using the CSB format
        yearFirst (bool) -- if *False*, consider the CSB format is DDMMYY \
            instead of YYMMDD

    Return:
        (datetime.date) the date object

    Examples:

    >>> raw2date('020301')
    datetime.date(2002, 3, 1)
    '''
    f = DATEFORMAT[1] if yearFirst else DATEFORMAT[0]
    return datetime.datetime.strptime(value, f).date()


def date2raw(
    value: datetime.datetime | datetime.date,
    yearFirst=True
) -> str:
    '''
    Convert a datetime.date / datetime.datetime object to a CSB formatted date

    Args:
        value (datetime.datetime, datetime.date) -- datetime object
        yearFirst (bool) -- if *False*, consider the CSB format is DDMMYY \
            instead of YYMMDD

    Return:
        (str) the CSB date

    Examples:

    >>> a = raw2date('020301')
    >>> date2raw(a)
    '020301'
    '''
    if isinstance(value, (datetime.datetime, datetime.date)):
        f = DATEFORMAT[1] if yearFirst else DATEFORMAT[0]
        return value.strftime(f)

    raise Csb43Exception(
        _(
            "instance of datetime or date expected, but "
            "{val!r} found"
        ).format(val=type(value))
    )


@deprecated(version="0.10.0", reason="use utils.currency.CurrencyLite")
def CurrencyLite(*args, **kwargs):
    return currency.CurrencyLite(*args, **kwargs)


currencyISO = deprecated(version="0.10.0", reason="use utils.currency.currency_from_iso_number")(
    currency.currency_from_iso_number
)


currencyISOByLetter = deprecated(version="0.10.0", reason="use utils.currency.currency_from_iso_letter")(
    currency.currency_from_iso_letter
)


isCurrency = deprecated(version="0.10.0", reason="use utils.currency.is_currency")(currency.is_currency)


def b_left_pad(bvalue: bytes, n: int, fill=b' ') -> bytes:
    "pad with `fill` chars at the leftside and return a record of `n` chars"
    return fill * (n - len(bvalue)) + bvalue


def b_right_pad(bvalue: bytes, n: int, fill=b' ') -> bytes:
    "pad with `fill` chars at the rightside and return a record of `n` chars"
    return bvalue + fill * (n - len(bvalue))


def nullable(f):
    @functools.wraps(f)
    def wrapper(value, *args, **kwds):
        if value is None:
            return value
        return f(value, *args, **kwds)
    return wrapper


@nullable
def export_date(value) -> str:
    return str(value)


@nullable
def export_currency_code(value) -> str:
    return str(value.alpha_3)


@nullable
def export_decimal(
    value: Decimal,
    fallback: T | None = None
) -> Decimal | float | str | T:
    if fallback == "float":
        return float(value)
    if fallback == "str":
        return str(value)
    if fallback:
        raise ValueError(f"fallback={fallback!r}")
    return value
