#!/usr/bin/env python
# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

'''
Homebank CSV format

References:

    [http://homebank.free.fr/help/06csvformat.html]
'''
from __future__ import annotations

import datetime
from decimal import Decimal

import dataclasses

from deprecated.sphinx import deprecated

from ..utils import (
    check_strict,
    raiseCsb43Exception,
)
from ..i18n import tr as _

'''
0. tarjeta de credito
1. cheque
2. efectivo
3. transferencia
4. transferencia interna
5. tarjeta de debito
6. orden de posicion
7. pago electronico
8. deposito
9. honorarios FI
'''

def to_str(data) -> str:
    "convert to str or return the empty string"
    if data is None:
        return ""
    return str(data)


@dataclasses.dataclass
class HomebankCsvTransaction:
    """
    Homebank CSV transaction
    """
    date: datetime.date | None = None
    mode: int | None = None
    info: str | None = None
    payee: str | None = None
    description: str | None = None
    amount: Decimal | None = None
    category: str | None = None

    def to_tuple(self):
        "return data as a tuple ready for CSV writing"
        if self.date is not None:
            mdate = self.date.strftime("%d-%m-%y")
        else:
            mdate = ""
        return (
            mdate,
            to_str(self.mode),
            to_str(self.payee),
            to_str(self.description),
            to_str(self.amount),
            to_str(self.category),
        )


@deprecated(
    version="0.10.0",
    reason="use csb43.homebank.HomebankCsvTransaction"
)
class Transaction:
    '''
    Hombebank CSV transaction

    - Creating a record::

        >>> from csb43.homebank import Transaction
        >>> t = Transaction()
        >>> t.amount = 12.45
        >>> import datetime
        >>> t.date = datetime.date(year=2013, month=3, day=19)
        >>> print(t)
        19-03-13;;;;;12.45;

    - Parsing a record::

        >>> t = Transaction("19-03-13;;;;;12.45;")
        >>> t.amount
        Decimal('12.45')
        >>> t.date
        datetime.date(2013, 3, 19)


    '''

    def __init__(self, record: str | None = None):
        '''
        :param record: a Homebank csv record
        :type record: :class:`str`

        :raises: :class:`csb43.utils.Csb43Exception`
        '''
        self.__date: datetime.date | None = None
        self.__mode: int | None = None
        self.__info: str | None = None
        self.__payee: str | None = None
        self.__description: str | None = None
        self.__amount: Decimal | None = None
        self.__category: str | None = None

        if record is not None:
            fields = record.split(";")
            if len(fields) < 6:
                raiseCsb43Exception(
                    _(
                        "bad format, 6 fields expected, but"
                        "{n_fields:d} found"
                    ).format(n_fields=len(fields)),
                    True
                )

            self._set_date_str(fields[0])
            self.mode = fields[1]
            self.info = fields[2]
            self.payee = fields[3]
            self.description = fields[4]
            self.amount = fields[5]
            if len(fields) >= 7:
                self.category = fields[6]
            else:
                self.category = None

    @property
    def date(self) -> datetime.date | None:
        "date of transaction (:class:`datetime.date`)"
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        #import datetime
        if not isinstance(value, datetime.date):
            raiseCsb43Exception(_("datetime.date expected"), strict=True)
        self.__date = value

    @property
    def mode(self):  # -> Optional[int]:
        "mode of transaction"
        return self.__mode

    @mode.setter
    def mode(self, value: str | int) -> None:
        self.__mode = int(value) if value != '' else None

    @property
    def info(self) -> str | None:
        "transaction's info"
        return self.__info

    @info.setter
    def info(self, value) -> None:
        self.__info = value

    @property
    def payee(self) -> str | None:
        "payee of the transaction"
        return self.__payee

    @payee.setter
    def payee(self, value):
        self.__payee = value

    @property
    def description(self) -> str | None:
        "description of the transaction"
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def amount(self):  # -> Optional[Decimal]:
        "amount of the transaction"
        return self.__amount

    @amount.setter
    def amount(self, value):
        self.__amount = Decimal(value)

    @property
    def category(self):
        "transaction category, according to HomeBank"
        return self.__category

    @category.setter
    def category(self, value):
        self.__category = value

    @check_strict(r"^(\d{2}\-\d{2}\-\d{2})?$")
    def _set_date_str(self, value, strict=True):
        if value == '':
            self.__date = None
        else:
            self.__date = datetime.datetime.strptime(value, "%d-%m-%y").date()

    def __str__(self):
        '''
        :rtype: :class:`str` representation of this record as a row of a \
        Homebank CSV file
        '''
        def f(x):
            return '' if x is None else str(x)

        if self.__date is not None:
            mdate = self.__date.strftime("%d-%m-%y")
        else:
            mdate = None

        text_fields = (f(x) for x in [
            mdate,
            self.mode,
            self.info,
            self.payee,
            self.description,
            #"%0.2f" % self.amount,
            str(self.amount or ''),
            self.category
        ])

        return ";".join(text_fields)
