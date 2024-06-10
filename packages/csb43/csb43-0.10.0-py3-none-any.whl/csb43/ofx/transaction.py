#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
OFX Transaction structure
"""
from __future__ import annotations
from typing import Sequence, Any, ClassVar
import datetime as dt
from decimal import Decimal
import dataclasses
import enum

from deprecated.sphinx import deprecated

from ..utils.currency import (
    AnyCurrency,
)
from . import base
from .bank_account import BankAccount
from .payee import Payee


#: type of transaction
class TransactionType(enum.Enum):
    """
    transaction types used in TRNTYPE

    See [OFX]_ Section 11.4.4.3
    """
    # Generic credit
    CREDIT = 0
    # Generic debit
    DEBIT = 1
    # Interest earned or paid
    INT = 2
    # Dividend
    DIV = 3
    # FI fee
    FEE = 4
    # Service charge
    SRVCHG = 5
    # Deposit
    DEP = 6
    # ATM debit or credit
    ATM = 7
    # Point of sale debit or credit
    POS = 8
    # Transfer
    XFER = 9
    # Check
    CHECK = 10
    # Electronic payment
    PAYMENT = 11
    # Cash withdrawal
    CASH = 12
    # Direct deposit
    DIRECTDEP = 13
    # Merchant initiated debit
    DIRECTDEBIT = 14
    # Repeating payment/standing order
    REPEATPMT = 15
    # Other
    OTHER = 16
    # Only valid in <STMTTRNP>; indicates the amount is under a hold
    HOLD = 17


@dataclasses.dataclass
class Transaction(base.OfxObject):
    '''
    A OFX transaction

    See [OFX]_ 11.4.4.1
    '''
    # deprecated
    TYPE: ClassVar[tuple[str, ...]] = (
        "CREDIT",  # 0
        "DEBIT",  # 1
        "INT",  # 2
        "DIV",  # 3
        "FEE",  # 4
        "SRVCHG",  # 5
        "DEP",  # 6
        "ATM",  # 7
        "POS",  # 8
        "XFER",  # 9
        "CHECK",  # 10
        "PAYMENT",  # 11
        "CASH",  # 12
        "DIRECTDEP",  # 13
        "DIRECTDEBIT",  # 14
        "REPEATPMT",  # 15
        "OTHER"  # 16
    )
    tag_name: str = "stmttrn"
    type: str = TransactionType.OTHER.name
    date_posted: dt.datetime | dt.date | None = None
    date_initiated: dt.datetime | dt.date | None = None
    date_available: dt.datetime | dt.date | None = None
    amount: int | float | Decimal | None = None
    transaction_id: str | None = None
    correct_fit_id: str | None = None
    correct_action: str | None = None
    server_tid: str | None = None
    check_num: str | None = None
    ref_num: str | None = None
    standard_industrial_code: str | None = None
    payee: Payee | None = None
    bank_account_to: BankAccount | None = None
    cc_account_to: BankAccount | None = None
    memo: str | None = None
    image_data: Any | None = None
    currency = None
    origin_currency: AnyCurrency | None = None
    origin_amount: int | float | Decimal | None = None
    inv401ksource: Any | str = None
    payeeid: str | None = None
    name: str | None = None
    extended_name: str | None = None

    def _get_content(self) -> str:
        elem = self._elem_f
        aggr = self._aggr_f

        str_c = elem("trntype", self.type)
        str_c += elem("dtposted", base.date_to_str(self.date_posted))
        str_c += elem("dtuser", base.date_to_str(self.date_initiated))
        str_c += elem("dtavail", base.date_to_str(self.date_available))
        str_c += elem("trnamt", self.amount)
        str_c += elem("fitid", base.text_to_str(self.transaction_id))
        str_c += elem("correctfitid", base.text_to_str(self.correct_fit_id))
        str_c += elem("correctaction", self.correct_action)
        str_c += elem("srvrtid", base.text_to_str(self.server_tid))
        str_c += elem("checknum", base.text_to_str(self.check_num))
        str_c += elem("refnum", base.text_to_str(self.ref_num))
        str_c += elem("sic", base.text_to_str(self.standard_industrial_code))
        str_c += elem("payeeid", base.text_to_str(self.payeeid))
        str_c += elem("name", base.text_to_str(self.name))
        str_c += elem("extdname", base.text_to_str(self.extended_name))
        str_c += aggr("payee", self.payee)
        str_c += aggr("bankacctto", self.bank_account_to)
        str_c += aggr("ccacctto", self.cc_account_to)
        str_c += elem("memo", base.text_to_str(self.memo))
        str_c += aggr("imagedata", self.image_data)
        str_c += elem("currency", base.currency_to_str(self.currency))
        str_curr = None
        if self.origin_currency and (self.amount is not None) and self.origin_amount:
            ratio = round(float(self.amount) / float(self.origin_amount), 20)
            str_curr = elem("currate", ratio)
            str_curr += elem("cursym", base.currency_to_str(self.origin_currency))
        str_c += aggr("origcurrency", str_curr)
        str_c += elem("inv401ksource", self.inv401ksource)

        return str_c

    @deprecated(version="0.10.0", reason="use attribute `name`")
    def get_name(self) -> str | None:
        '''
        :rtype: :class:`str` -- name of payee or description of transaction
        '''
        return self.name

    @deprecated(version="0.10.0", reason="use attribute `extended_name`")
    def get_extended_name(self) -> str | None:
        '''
        :rtype: :class:`str` -- extended name of payee or description of \
        transaction
        '''
        return self.extended_name

    @deprecated(version="0.10.0", reason="use attribute `name`")
    def set_name(self, value: str):
        '''
        :param value: name of payee or description of transaction
        '''
        self.name = value

    @deprecated(version="0.10.0", reason="use attribute `extended_name`")
    def set_extended_name(self, value: str):
        '''
        :param value: extended name of payee or description of transaction
        '''
        self.extended_name = value

    @deprecated(version="0.10.0", reason="use attribute `ref_num`")
    def get_ref_num(self) -> str | None:
        '''
        :rtype: :class:`str` -- reference number that uniquely indentifies \
        the transaction.
        '''
        return self.ref_num

    @deprecated(version="0.10.0", reason="use attribute `ref_num`")
    def set_ref_num(self, value: str):
        '''
        :param value: reference number that uniquely indentifies the \
        transaction.
        '''
        self.ref_num = value

    @deprecated(version="0.10.0", reason="use attribute `type`")
    def get_type(self) -> str:
        '''
        :rtype: :class:`str` -- transaction type. See :class:`TYPE`. Default \
        ('OTHER')
        '''
        if self.type is None:
            return TransactionType.OTHER.name
        return self.type

    @deprecated(version="0.10.0", reason="use attribute `date_posted`")
    def get_date_posted(self) -> dt.datetime | dt.date | None:
        '''
        :rtype: :class:`datetime.datetime` -- date transaction was posted to \
        account
        '''
        return self.date_posted

    @deprecated(version="0.10.0", reason="use attribute `date_initiated`")
    def get_date_initiated(self) -> dt.datetime | dt.date | None:
        '''
        :rtype: :class:`datetime.datetime` -- date user initiated transaction
        '''
        return self.date_initiated

    @deprecated(version="0.10.0", reason="use attribute `date_available`")
    def get_date_available(self) -> dt.datetime | dt.date | None:
        '''
        :rtype: :class:`datetime.datetime` -- date funds are available
        '''
        return self.date_available

    @deprecated(version="0.10.0", reason="use attribute `amount`")
    def get_amount(self) -> int | float | Decimal | None:
        '''
        :rtype: number -- amount of transaction
        '''
        return self.amount

    @deprecated(version="0.10.0", reason="use attribute `transaction_id`")
    def get_transaction_id(self) -> str | None:
        '''
        :rtype: :class:`str` -- transaction ID issued by financial institution
        '''
        return self.transaction_id

    @deprecated(version="0.10.0", reason="use attribute `correct_fit_id`")
    def get_correct_fit_id(self) -> str | None:
        '''
        correct fit id
        '''
        return self.correct_fit_id

    @deprecated(version="0.10.0", reason="use attribute `correct_action`")
    def get_correct_action(self) -> str | None:
        '''
        correct action
        '''
        return self.correct_action

    @deprecated(version="0.10.0", reason="use attribute `server_tid`")
    def get_server_tid(self) -> str | None:
        '''
        server transaction id
        '''
        return self.server_tid

    @deprecated(version="0.10.0", reason="use attribute `check_num`")
    def get_check_num(self) -> str | None:
        '''
        :rtype: :class:`str` -- check (or other reference) number
        '''
        return self.check_num

    @deprecated(version="0.10.0", reason="use attribute `standard_industrial_code`")
    def get_standard_industrial_code(self) -> str | None:
        '''
        standard industrial code
        '''
        return self.standard_industrial_code

    @deprecated(version="0.10.0", reason="use attribute `payee`")
    def get_payee(self) -> Payee | None:
        '''
        :rtype: :class:`Payee`
        '''
        return self.payee

    @deprecated(version="0.10.0", reason="use attribute `payeeid`")
    def get_payeeid(self) -> str | None:
        '''
        :rtype: :class:`str` -- payee identifier
        '''
        return self.payeeid

    @deprecated(version="0.10.0", reason="use attribute `bank_account_to`")
    def get_bank_account_to(self) -> BankAccount | None:
        '''
        :rtype: :class:`BankAccount` -- account the transaction is \
        transferring to
        '''
        return self.bank_account_to

    @deprecated(version="0.10.0", reason="use attribute `cc_account_to`")
    def get_cc_account_to(self) -> BankAccount | None:
        '''
        cc account to
        '''
        return self.cc_account_to

    @deprecated(version="0.10.0", reason="use attribute `memo`")
    def get_memo(self) -> str | None:
        '''
        :rtype: :class:`str` -- extra information
        '''
        return self.memo

    @deprecated(version="0.10.0", reason="use attribute `image_data`")
    def get_image_data(self) -> Any | None:
        '''
        image data
        '''
        return self.image_data

    @deprecated(version="0.10.0", reason="use attribute `currency`")
    def get_currency(self) -> AnyCurrency | None:
        '''
        :rtype: :class:`pycountry.db.Currency` -- currency of the \
        transaction, if different from the one in :class:`BankAccount`
        '''
        return self.currency

    @deprecated(version="0.10.0", reason="use attribute `origin_currency`")
    def get_origin_currency(self) -> AnyCurrency | None:
        '''
        :rtype: :class:`pycountry.db.Currency` -- currency of the \
        transaction, if different from the one in :class:`BankAccount`
        '''
        return self.origin_currency

    @deprecated(version="0.10.0", reason="use attribute `origin_amount`")
    def get_origin_amount(self):
        return self.origin_amount

    @deprecated(version="0.10.0", reason="use attribute `inv_401ksource`")
    def get_inv_401ksource(self):
        return self.inv401ksource

    @deprecated(version="0.10.0", reason="use attribute `type`")
    def set_type(self, value):
        self.type = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_date_posted(self, value: dt.datetime | dt.date):
        self.date_posted = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_date_initialised(self, value: dt.datetime | dt.date):
        self.date_initiated = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_date_available(self, value: dt.datetime | dt.date):
        self.date_available = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_amount(self, value: int | float | Decimal):
        self.amount = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_transaction_id(self, value: str):
        self.transaction_id = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_correct_fit_id(self, value: str):
        self.correct_fit_id = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_correct_action(self, value: str):
        self.correct_action = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_server_tid(self, value: str):
        self.server_tid = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_check_num(self, value: str):
        self.check_num = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_standard_industrial_code(self, value: str):
        self.standard_industrial_code = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_payee(self, value: Payee):
        self.payee = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_payeeid(self, value: str):
        self.payeeid = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_bank_account_to(self, value: BankAccount):
        self.bank_account_to = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_cc_account_to(self, value: BankAccount):
        self.cc_account_to = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_memo(self, value: str):
        self.memo = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_image_data(self, value):
        self.image_data = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_currency(self, value):
        self.currency = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_origin_currency(self, value):
        self.origin_currency = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_origin_amount(self, value):
        self.origin_amount = value

    @deprecated(version="0.10.0", reason="use attribute")
    def set_inv_401ksource(self, value):
        self.inv401ksource = value


@dataclasses.dataclass
class TransactionList(base.OfxObject):
    '''
    Transaction list aggregate
    '''
    tag_name: str = "banktranlist"
    date_start: dt.datetime | dt.date | None = None
    date_end: dt.datetime | dt.date | None = None
    transactions: list[Transaction] = dataclasses.field(default_factory=list)

    def _get_content(self) -> str:
        elem = self._elem_f
        str_c = elem("dtstart", base.date_to_str(self.date_start))
        str_c += elem("dtend", base.date_to_str(self.date_end))
        for t in self.transactions:
            str_c += self._aggr_f(t.tag_name, t)

        return str_c

    @deprecated(version="0.10.0", reason="use attribute `date_start`")
    def get_date_start(self) -> dt.datetime| dt.date | None:
        '''
        :rtype: :class:`datetime.datetime` -- date of the first transaction
        '''
        return self.date_start

    @deprecated(version="0.10.0", reason="use attribute `date_end`")
    def get_date_end(self) -> dt.datetime | dt.date | None:
        '''
        :rtype: :class:`datetime.datetime` -- date of the first transaction
        '''
        return self.date_end

    @deprecated(version="0.10.0", reason="use attribute `transactions`")
    def get_list(self) -> Sequence[Transaction]:
        '''
        :rtype: :class:`list` of :class:`Transaction`
        '''
        return self.transactions

    @deprecated(version="0.10.0", reason="use attribute `date_start`")
    def set_date_start(self, value):
        '''
        :param value: date of start
        :type  value: :class:`datetime.datetime`
        '''
        self.date_start = value

    @deprecated(version="0.10.0", reason="use attribute `date_end`")
    def set_date_end(self, value: dt.datetime | dt.date):
        '''
        :param value: date of end
        :type  value: :class:`datetime.datetime`
        '''
        self.date_end = value

    @deprecated(version="0.10.0", reason="use attribute `transactions`")
    def add_transaction(self, value: Transaction):
        '''
        Add a new transaction to the list

        :param value: a transaction
        :type  value: :class:`Transaction`
        '''
        self.transactions.append(value)
