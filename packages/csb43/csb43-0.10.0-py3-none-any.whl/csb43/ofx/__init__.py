# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

'''
Partial implementation of a OFX file writer.

This package is not intended to fully implement the OFX Spec. Its final purpose
is the conversion from CSB43 (norma 43 del Consejo Superior Bancario). That is,
only transaction response is (partially) implemented.

References
----------

.. [OFX] [http://www.ofx.net/] Open Financial Exchange, Specification 2.2 (nov 26, 2017).
   Intuit Inc.  Envestnet
'''
from __future__ import annotations

from deprecated.sphinx import deprecated
from . import base
from .bank_account import BankAccount
from .payee import Payee
from .balance import Balance
from .transaction import Transaction, TransactionList
from .file import File, SignOnResponse, Response

__all__ = [
    "File",
    "SignOnResponse",
    "Response",
    "Transaction",
    "TransactionList",
    "Balance",
    "Payee",
    "BankAccount",
]


XMLElement = deprecated(
    version="0.10.0",
    reason="use csb43.ofx.base.xml_element"
)(base.xml_element)


XMLAggregate = deprecated(
    version="0.10.0",
    reason="use csb43.ofx.base.xml_aggregate"
)(base.xml_aggregate)


SGMLElement = deprecated(
    version="0.10.0",
    reason="use csb43.ofx.base.sgml_element"
)(base.sgml_element)


SGMLAggregate = deprecated(
    version="0.10.0",
    reason="use csb43.ofx.base.sgml_aggregate"
)(base.sgml_aggregate)


strDate = deprecated(
    version="0.10.0",
    reason="use csb43.ofx.base.date_to_str"
)(base.date_to_str)


strBool = deprecated(
    version="0.10.0",
    reason="use csb43.ofx.base.bool_to_str"
)(base.bool_to_str)


strCurrency = deprecated(
    version="0.10.0",
    reason="use csb43.ofx.base.currency_to_str"
)(base.currency_to_str)


strText = deprecated(
    version="0.10.0",
    reason="use csb43.ofx.base.text_to_str"
)(base.text_to_str)


@deprecated(version="0.10.0", reason="use csb43.ofx.base.OfxObject")
def OfxObject(*args, **kwargs):
    "OfxObject deprecation wrapper"
    return base.OfxObject(*args, **kwargs)
