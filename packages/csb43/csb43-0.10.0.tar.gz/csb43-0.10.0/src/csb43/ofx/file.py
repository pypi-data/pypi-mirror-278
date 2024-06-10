#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""
OFX: File and Response structures
"""
from __future__ import annotations
from typing import (
    Sequence,
    Any,
)
import dataclasses
from datetime import datetime

from deprecated.sphinx import deprecated

from ..utils.currency import AnyCurrency
from .base import (
    date_to_str,
    currency_to_str,
    text_to_str,
    OfxObject,
)
from .bank_account import BankAccount
from .balance import Balance
from .transaction import TransactionList


@dataclasses.dataclass
class SignOnResponse(OfxObject):
    """
    `SONRS`

    See [OFX]_ 2.5.1
    """
    tag_name: str = "sonrs"

    def _get_content(self) -> str:
        elem = self._elem_f
        aggr = self._aggr_f
        code = elem("code", 0)
        severity = elem("severity", "INFO")
        status = aggr("status", code + severity)
        dtserver = elem("dtserver", date_to_str(datetime.utcnow()))
        language = elem("language", "SPA")

        return aggr(self.tag_name, status + dtserver + language)


@dataclasses.dataclass
class Response(OfxObject):
    """
    `STMTRS`

    See [OFX]_ 11.4.2.2 Response
    """
    tag_name: str = "stmtrs"
    currency: AnyCurrency | None = None
    account_from: BankAccount | None = None
    transaction_list: TransactionList | None = None
    ledger_balance: Balance | None = None
    available_balance: Balance | None = None
    balances: list[Balance] = dataclasses.field(default_factory=list)
    mktginfo: Any | None = None

    def _get_content(self) -> str:
        elem = self._elem_f
        aggr = self._aggr_f
        str_c = elem("curdef", currency_to_str(self.currency))
        str_c += aggr("bankacctfrom", self.account_from)
        str_c += aggr("banktranlist", self.transaction_list)
        str_c += aggr("ledgerbal", self.ledger_balance)
        str_c += aggr("availbal", self.available_balance)
        if len(self.balances) > 0:
            str_c += aggr(
                "ballist",
                "".join(aggr(x.tag_name, x) for x in self.balances)
            )
        str_c += elem("mktginfo", text_to_str(self.mktginfo))

        return str_c

    @deprecated(version="0.10.0", reason="use attribute")
    def get_currency(self):
        '''
        :rtype: :class:`pycountry.dbCurrency` -- \
        Default currency for the statement
        '''
        return self.currency

    @deprecated(version="0.10.0", reason="use attribute")
    def get_bank_account_from(self) -> BankAccount | None:
        '''
        :rtype: :class:`BankAccount` -- Account-from aggregate
        '''
        return self.account_from

    @deprecated(version="0.10.0", reason="use attribute")
    def get_transaction_list(self) -> TransactionList | None:
        '''
        :rtype: :class:`TransactionList` -- \
        Statement-transaction-data aggregate
        '''
        return self.transaction_list

    @deprecated(version="0.10.0", reason="use attribute")
    def get_ledger_balance(self) -> Balance | None:
        '''
        :rtype: :class:`Balance` -- the ledger balance aggregate
        '''
        return self.ledger_balance

    @deprecated(version="0.10.0", reason="use attribute")
    def get_available_balance(self) -> Balance | None:
        '''
        :rtype: `Balance` -- the available balance aggregate
        '''
        return self.available_balance

    @deprecated(version="0.10.0", reason="use attribute")
    def get_balances(self) -> Sequence[Balance] | None:
        '''
        :rtype: :class:`list` of miscellaneous other :class:`Balance` s
        '''
        return self.balances

    @deprecated(version="0.10.0", reason="use attribute")
    def get_mktginfo(self):
        '''
        :rtype: marketing info
        '''
        return self.mktginfo

    @deprecated(version="0.10.0", reason="use attribute")
    def set_currency(self, value):
        '''
        :param value: currency
        :type value: :class:`pycountry.db.Currency`
        '''
        self.currency = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_bank_account_from(self, value: BankAccount):
        '''
        :param value: value
        :type value: :class:`BankAccount`
        '''
        self.account_from = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_transaction_list(self, value: TransactionList):
        '''
        :param value: transactions list
        :type value: :class:`TransactionList`
        '''
        self.transaction_list = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_ledger_balance(self, value: Balance):
        '''
        :param value: ledger balance
        :type value: :class:`Balance`
        '''
        self.ledger_balance = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_available_balance(self, value: Balance):
        '''
        :param value: available balance
        :type  value: :class:`Balance`
        '''
        self.available_balance = value

    @deprecated(version="0.10.0", reason="use attribute")
    def add_balance(self, value: Balance):
        '''
        Add a complementary balance

        :param value: a complementary balance
        :type  value: :class:`Balance`
        '''
        self.balances.append(value)

    @deprecated(version="0.10.0", reason="use attribute")
    def set_mktginfo(self, value):
        '''
        :param value: marketing info
        '''
        self.mktginfo = value


@dataclasses.dataclass
class File(OfxObject):
    '''
    An OFX file

    See [OFX]_ 2.4.1

    Fields
    ------
    responses
    '''
    tag_name: str = "ofx"
    responses: list[Response] = dataclasses.field(default_factory=list)

    def _get_content(self) -> str:
        elem = self._elem_f
        aggr = self._aggr_f
        if self.sgml:
            header = (
                "OFXHEADER:100\n"
                "DATA:OFXSGML\n"
                "VERSION:103\n"
                "ENCODING:UNICODE\n\n"
            )
        else:
            header = (
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                '<?OFX OFXHEADER="200" VERSION="211" SECURITY="NONE"'
                ' OLDFILEUID="NONE" NEWFILEUID="NONE"?>'
            )
        content = ""
        for r in self.responses:
            aux = elem("trnuid", 0)
            aux += aggr("status",
                        elem("code", 0) + elem("severity", "INFO"))
            aux += aggr(r.tag_name, r)
            content += aggr("stmttrnrs", aux)
        content = (
            aggr("signonmsgsrsv1", SignOnResponse(sgml=self.sgml))
            + aggr("bankmsgsrsv1", content)
        )
        return header + aggr(self.tag_name, content)

    @deprecated(version="0.10.0", reason="use attribute `responses`")
    def get_responses(self) -> Sequence[Response]:
        '''
        :rtype: :class:`list` of :class:`Response`
        '''
        return self.responses

    @deprecated(version="0.10.0", reason="use attribute `responses`")
    def add_response(self, value: Response):
        '''
        Add a response to the file

        :param value: a response object to include in this object
        :type value: :class:`Response`
        '''
        self.responses.append(value)