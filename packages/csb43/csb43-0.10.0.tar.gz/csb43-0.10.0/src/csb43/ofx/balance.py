#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""
An OFX Balance structure
"""
from __future__ import annotations
import datetime as dt
from decimal import Decimal
import dataclasses

from deprecated.sphinx import deprecated

from .base import (
    date_to_str,
    OfxObject,
)


@dataclasses.dataclass
class Balance(OfxObject):
    '''
    a balance

    See [OFX]_ 11.4.4.1

    Fields
    ------
    amount
        field `<BALAMT>`
    date
        field `<DTASOF>`
    '''
    tag_name: str = "bal"
    amount: int | float | Decimal | None = None
    date: dt.datetime | dt.date | None = None

    def _get_content(self) -> str:
        elem = self._elem_f
        return f"{elem('balamt', self.amount)}{elem('dtasof', date_to_str(self.date))}"

    @deprecated(version="0.10.0", reason="use attribute")
    def get_amount(self) -> int | float | Decimal| None:
        '''
        :rtype: the amount of the balance
        '''
        return self.amount

    @deprecated(version="0.10.0", reason="use attribute")
    def get_date(self) -> dt.datetime | dt.date | None:
        '''
        :rtype: :class:`datetime` -- date of the balance
        '''
        return self.date

    @deprecated(version="0.10.0", reason="use attribute")
    def set_amount(self, value: int | float | Decimal):
        '''
        :param value: amount
        '''
        self.amount = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_date(self, value: dt.datetime | dt.date):
        '''
        :param value: a date object
        :type  value: :class:`datetime.datetime`
        '''
        self.date = value
