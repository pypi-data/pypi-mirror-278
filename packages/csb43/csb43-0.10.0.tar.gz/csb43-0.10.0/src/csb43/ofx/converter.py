#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

'''
Conversion from AEB43 to OFX
'''
from __future__ import annotations
from collections import defaultdict
from deprecated.sphinx import deprecated
from . import (
    BankAccount,
    File,
    Response,
    Balance,
    TransactionList,
    Transaction
)
from .transaction import TransactionType
from ..aeb43.batch import Batch as CsbBatch
from ..aeb43.account import Account as CsbAccount
from ..aeb43.transaction import Transaction as CsbTransaction
from ..csb43 import File as CsbFile

#: conversion table OFX - Homebank for pay modes
PAYMODES = {
    1: TransactionType.CHECK,
    2: TransactionType.CREDIT,
    3: TransactionType.SRVCHG,
    4: TransactionType.XFER,
    5: TransactionType.DIV,
    # 6:
    7: TransactionType.REPEATPMT,
    8: TransactionType.FEE,
    9: TransactionType.DIV,
    10: TransactionType.CHECK,
    11: TransactionType.ATM,
    12: TransactionType.POS,
    # 13:
    # 14:
    15: TransactionType.XFER,
    # 16:
    17: TransactionType.INT,
    # 98:
    99: TransactionType.OTHER,
}

DEFAULT_NAME = "-"
DEFAULT_MEMO = "-"


def convert_from_aeb43(batch: CsbBatch, sgml=False) -> File:
    """
    convert an AEB43 batch to OFX.

    Use `sgml=True` in order to generate SGML instead of XML
    """
    ids: dict[str, int] = defaultdict(lambda: 0)

    ofx_file = File(sgml=sgml)

    account: CsbAccount
    for account in (batch.accounts or []):

        o_response = Response(
            sgml=sgml,
            # currency
            currency = account.currency,
            # account
            account_from = BankAccount(
                sgml=sgml,
                bank_id = account.bank_code,
                branch_id = account.branch_code,
                id = account.account_number,
                key = account.account_control_key,
            ),
        )

        # balance (ledger)
        o_response.ledger_balance = Balance(
            sgml=sgml,
            date=account.initial_date
        )

        if account.summary:
            o_response.ledger_balance.amount = account.summary.final_balance

        # transactions
        o_tran_list = TransactionList(
            sgml=sgml,
            date_start=account.initial_date,
            date_end=account.final_date,
        )

        trn: CsbTransaction
        for trn in (account.transactions or []):
            trn_id = "-".join((
                account.bank_code,
                account.branch_code,
                account.account_control_key,
                account.account_number,
                trn.transaction_date.strftime("%Y%m%d"),
            ))
            o_trn = Transaction(
                sgml=sgml,
                type=PAYMODES.get(trn.shared_item, TransactionType.OTHER).name,
                date_posted=trn.transaction_date,
                date_available=trn.value_date,
                # composing a unique transaction id
                transaction_id=f"{trn_id}-{ids[trn_id]}",
                ref_num=(trn.reference2 or f"{trn.branch_code}-{trn.reference1}").strip()[:32],
                payeeid=(trn.reference1 or "").strip()[:12],
                amount=trn.amount,
            )

            # increment counter just in case another transaction has the same signature
            ids[trn_id] += 1

            if trn.document_number and any(c != "0" for c in trn.document_number):
                o_trn.ref_num = f"{trn.document_number}-{o_trn.ref_num}"

            if trn.exchange is not None:
                o_trn.origin_currency = trn.exchange.original_currency
                o_trn.origin_amount = trn.exchange.amount

            if trn.optional_items:
                infos = [x for x in (v.strip() for v in trn.iter_optional_items()) if x]
                if infos:
                    o_trn.name = " | ".join(infos[:2])
                    o_trn.memo = " | ".join(infos)
            elif trn.sepa_debit:
                o_trn.name = trn.sepa_debit.creditor_name
                o_trn.memo = " | ".join(
                    f"{k}={v}" for k, v in trn.sepa_debit.to_dict().items() if v
                )
                o_trn.type = TransactionType.DIRECTDEBIT.name
                if trn.sepa_debit.creditor_id:
                    o_trn.payeeid = trn.sepa_debit.creditor_id.strip()[:12] or o_trn.payeeid
                    o_trn.memo = f"ref1={trn.reference1} | {o_trn.memo}"
            elif trn.sepa_transfer:
                o_trn.name = trn.sepa_transfer.originator_name
                o_trn.memo = " | ".join(
                    f"{k}={v}" for k, v in trn.sepa_transfer.to_dict().items() if v
                )
                if trn.sepa_transfer.originator_code:
                    o_trn.payeeid = (
                        trn.sepa_transfer.originator_code.strip()[:12]
                        or o_trn.payeeid
                    )
                    o_trn.memo = f"ref1={trn.reference1} | {o_trn.memo}"

            o_trn.name = o_trn.name or DEFAULT_NAME
            o_trn.memo = (o_trn.memo or DEFAULT_MEMO)[:100]

            # check lengths
            if len(o_trn.name) > 32:
                o_trn.extended_name = o_trn.name
                o_trn.name = o_trn.name[:32]

            o_tran_list.transactions.append(o_trn)

        o_response.transaction_list = o_tran_list

        ofx_file.responses.append(o_response)

    return ofx_file


@deprecated(
    version="0.10.0",
    reason="use csb43.ofx.converter.convert_from_aeb43"
)
def convertFromCsb(csb: CsbFile, sgml=False) -> File:
    '''
    Convert a File file into an OFX file

    :param csb: a CSB43 file
    :type csb: :class:`csb43.csb43.File`

    :rtype: :class:`csb43.ofx.File`

    >>> # OFX
    >>> from csb43 import csb43
    >>> #
    >>> csbFile = csb43.File(open("movimientos.csb"), strict=False) # doctest: +SKIP
    >>> #
    >>> # print to stdout
    >>> print(convertFromCsb(csbFile)) # doctest: +SKIP

    '''
    ofx_file = File(sgml=sgml)

    for account in csb.accounts:
        o_response = Response(
            sgml=sgml,
            currency=account.currency,
            account_from=BankAccount(
                sgml=sgml,
                bank_id=account.bankCode,
                branch_id=account.branchCode,
                id=account.accountNumber,
                key=account.get_account_key()
            )
        )

        # balance (ledger)
        balance = Balance(
            sgml=sgml,
            date=account.initialDate,
        )
        if account.abstract:
            balance.amount = account.abstract.balance

        o_response.ledger_balance = balance

        # balance (available)
        # o_response.set_available_balance(balance)

        # transactions
        o_tran_list = TransactionList(
            sgml=sgml,
            date_start=account.initialDate,
            date_end=account.finalDate,
        )

        for idx, trn in enumerate(account.transactions):
            o_trn = Transaction(
                sgml=sgml,
                type=PAYMODES.get(int(trn.sharedItem), TransactionType.OTHER).name,
                date_posted=trn.transactionDate,
                date_available=trn.valueDate,
                ref_num=trn.reference2,
                payeeid=trn.reference1,
                amount=trn.amount,
            )
            # composing a unique transaction id
            o_trn.transaction_id = "-".join((
                account.bankCode,
                account.branchCode,
                account.get_account_key(),
                account.accountNumber,
                trn.transactionDate.strftime("%Y%m%d"),
                f"{idx:d}"
            ))
            # o_trn.set_name(trn.commonItem)
            # o_trn.set_extended_name(trn.particularItem)
            name = ", ".join(x.item1.rstrip(' ') for x in trn.optionalItems)
            if not name:
                name = DEFAULT_NAME
            o_trn.name = name
            extdname = ", ".join(x.item2.rstrip(' ') for x in trn.optionalItems)
            if not extdname:
                extdname = DEFAULT_MEMO
            o_trn.memo = extdname

            if trn.exchange is not None:
                o_trn.origin_currency = trn.exchange.sourceCurrency
                o_trn.origin_amount = trn.exchange.amount

            o_tran_list.transactions.append(o_trn)

        o_response.transaction_list = o_tran_list

        ofx_file.responses.append(o_response)

    return ofx_file
