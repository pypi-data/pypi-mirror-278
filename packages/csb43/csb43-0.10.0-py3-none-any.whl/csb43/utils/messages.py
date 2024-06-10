# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

# -*- coding: utf-8 -*-
'''
@license: GNU Lesser General Public License v3.0 (see LICENSE)
'''
from ..i18n import tr as _


def BAD_RECORD(x: bytes) -> str:
    return _('bad code of record or unexpected length: >>>%s<<<') % repr(x)


T_INCOMPATIBLE_OBJECT = _(
    "incompatible object '{found!r}', type(s) {expected} expected"
)


T_CURRENCY_EXPECTED = _(
    "pycountry.Currencies object or a valid ISO 4217 code expected, but {obj!r} found"
)


T_PADDING = _("padding")
T_ACCOUNTS = _("accounts")
# Account ID
T_BANK_CODE = _('bank_code')
T_BRANCH_CODE = _('branch_code')
T_ACCOUNT_KEY = _('account_key')
T_ACCOUNT_NUMBER = _('account_number')

# Account abstract
T_INFORMATION_MODE = _('information_mode')
T_SHORT_NAME = _('short_name')
T_CURRENCY = _('currency')
T_INITIAL_DATE = _('initial_date')
T_FINAL_DATE = _('final_date')
T_INITIAL_BALANCE = _('initial_balance')
T_FINAL_BALANCE = _('final_balance')
T_INCOME = _('income')
T_EXPENSES = _('expenses')
T_INCOME_ENTRIES = _('income_entries')
T_EXPENSES_ENTRIES = _('expenses_entries')
T_SUMMARY = _("summary")
T_TRANSACTIONS = _("transactions")

# Transaction
T_DOCUMENT_NUMBER = _('document_number')
T_SHARED_ITEM = _('shared_item')
T_OWN_ITEM = _('own_item')
T_ITEM_1 = _('item1')
T_ITEM_2 = _('item2')
T_REFERENCE_1 = _('reference1')
T_REFERENCE_2 = _('reference2')
T_TRANSACTION_DATE = _('transaction_date')
T_VALUE_DATE = _('value_date')
T_AMOUNT = _('amount')
T_ORIGINAL_CURRENCY = _('original_currency')
T_ORIGINAL_AMOUNT = _('original_amount')
T_OPTIONAL_ITEMS = _('optional_items')
T_EXCHANGE = _('exchange')
T_SEPA_DEBIT = _("sepa_debit")
T_SEPA_TRANSFER = _("sepa_transfer")

# Item
T_RECORD_CODE = _('record_code')

# SEPA
T_SCHEME_CODE = _("scheme_code")
T_CREDITOR_NAME = _("creditor_name")
T_CREDITOR_ID = _("creditor_id")
T_MANDATE_REFERENCE = _("mandate_reference")
T_PURPOSE = _("purpose")
T_PURPOSE_CATEGORY = _("purpose_category")
T_REMITANCE_INFORMATION = _("remitance_information")
T_CREDITOR_REFERENCE = _("creditor_reference")
T_DEBTOR_NAME = _("debtor_name")
T_ORIGINATOR_NAME = _("originator_name")
T_ORIGINATOR_CODE = _("originator_code")
T_ORIGINATOR_REFERENCE = _("originator_reference")
T_ORIGINATOR_REFERENCE_PARTY = _("originator_reference_party")
T_ADDITIONAL_INFO = _("additional_info")