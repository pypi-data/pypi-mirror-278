#!/usr/bin/env python
# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

'''
Conversion from AEB43 to Homebank CSV
'''
from __future__ import annotations
from typing import (
    Sequence,
    Iterable,
    IO,
)
import warnings
import csv

from deprecated.sphinx import deprecated

from . import Transaction, HomebankCsvTransaction

from ..aeb43.batch import Batch
from ..csb43.csb_file import File as CsbFile


#: conversion table CSB - Homebank for pay modes
PAYMODES = {
    1: 2,
    2: 2,
    4: 3,
    12: 5
}


def convert_aeb43_to_rows(batch: Batch) -> Iterable[HomebankCsvTransaction]:
    "convert an AEB43 batch to Homebank CSV transactions"
    if not batch.accounts:
        return

    if len(batch.accounts) > 1:
        warnings.warn(
            "More than 1 account found in batch. "
            "Only the first account will be converted"
        )

    account = batch.accounts[0]

    for tran in account.transactions:
        record = HomebankCsvTransaction(
            date=tran.value_date,
            mode=PAYMODES.get(int(tran.shared_item)),
            info=tran.own_item,
            payee=tran.reference1.rstrip(" "),
            amount=tran.amount,
        )

        if tran.optional_items:
            info = [part for part in (it.strip() for it in tran.iter_optional_items()) if part]
        elif tran.sepa_debit:
            info = [
                f"{key}: {value}"
                for key, value in tran.sepa_debit.to_dict().items()
                if value
            ]
        elif tran.sepa_transfer:
            info = [
                f"{key}: {value}"
                for key, value in tran.sepa_transfer.to_dict().items()
                if value
            ]
        else:
            info = []

        if info:
            record.description = " | ".join(info)

        yield record


def dump_from_aeb43(batch: Batch, stream: IO[str]) -> None:
    "dump homebank csv from an AEB43 batch"
    writer = csv.writer(stream, delimiter=",")
    for record in convert_aeb43_to_rows(batch):
        writer.writerow(record.to_tuple())


@deprecated(
    version="0.10.0",
    reason="use csb43.homebank.converter.convert_aeb43_to_rows"
)
def convertFromCsb(csb: CsbFile) -> Sequence[Transaction]:
    '''
    Convert a CSB43 file into a HomeBank CSV file.

    Only first account is converted.

    :param csb: a CSB43 file
    :type csb: :class:`csb43.csb43.File`

    :rtype: :class:`list` of :class:`Transaction`

    >>> # Homebank
    >>> from csb43 import csb43
    >>> #
    >>> csbFile = csb43.File(open("movimientos.csb"), strict=False) # doctest: +SKIP
    >>> #
    >>> # print to stdout
    >>> for line in convertFromCsb(csbFile): # doctest: +SKIP
    ...    print(line)
    ...
    '''

    for ac in csb.accounts:

        hbTrans = []

        for t in ac.transactions:
            record = Transaction()
            record.date = t.valueDate
            record.mode = PAYMODES.get(int(t.sharedItem), '')
            record.info = t.ownItem
            record.payee = t.reference1.rstrip(' ')

            info = [
                "%s: %s" % (x.item1.rstrip(' '), x.item2.rstrip(' '))
                for x in t.optionalItems
            ]
            record.description = "/".join(info)
            record.amount = "%1.2f" % t.amount

            hbTrans.append(record)

        return hbTrans

    return []