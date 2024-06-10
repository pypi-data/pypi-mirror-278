# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

# -*- coding: utf-8 -*-
from __future__ import annotations
try:
    import importlib_resources as resources
except ImportError:
    from importlib import resources

import datetime
from decimal import Decimal
import pytest

from .. import csb43
from .. import aeb43


def sample1():
    "sample1"
    batch = csb43.File(strict=False)

    for n in range(2):
        acc = csb43.Account(strict=batch.strict_mode)

        acc.currency = "EUR"
        acc.shortName = "José Müller Muñiz Avinyò"
        acc.accountNumber = f"{n:010d}"
        acc.bankCode = "0001"
        acc.branchCode = "0005"
        acc.informationMode = 1
        acc.initialBalance = 10 ** n

        batch.add_account(acc)

        for idx, tid in enumerate(range(3)):
            trn = csb43.Transaction(
                strict=acc.strict_mode,
                informationMode=acc.informationMode
            )
            trn.transactionDate = datetime.date(
                year=2012,
                month=2,
                day=n + 1
            )
            trn.valueDate = trn.transactionDate
            trn.documentNumber = n * 10 + tid
            trn.sharedItem = 12
            trn.ownItem = 123
            trn.reference1 = "1" * 12
            trn.reference2 = "2" * 16
            trn.amount = '53.2'

            if idx == 0:
                e = csb43.Exchange()
                e.sourceCurrency = 'USD'
                e.amount = '60.87'

                trn.add_exchange(e)

            batch.add_transaction(trn)

        acc.initialDate = acc.transactions[0].transactionDate
        acc.finalDate = acc.transactions[-1].transactionDate

        batch.close_account()

    batch.close_file()

    return batch


@pytest.fixture(name="aeb43sample1", scope="session")
def fixture_aeb43sample1(context) -> aeb43.Batch:
    "an AEB43 sample"
    batch = aeb43.Batch(context=context)

    for n in range(2):
        acc = aeb43.Account(
            currency="EUR",
            short_name="José Müller Muñiz Avinyò",
            account_number=f"{n:010d}",
            bank_code="0001",
            branch_code="0005",
            information_mode=1,
            initial_balance=10 ** n,
        )

        assert batch.accounts is not None
        batch.accounts.append(acc)  # pylint: disable=no-member

        for idx, tid in enumerate(range(3)):
            today = datetime.date(
                year=2012,
                month=2,
                day=n + 1
            )
            trn = aeb43.Transaction(
                transaction_date=today,
                value_date=today,
                document_number=f"{n * 10 + tid:010d}",
                shared_item=12,
                own_item=123,
                reference1="1" * 12,
                reference2="2" * 16,
                amount=Decimal('53.2'),
            )

            if idx == 0:
                trn.exchange = aeb43.Exchange(
                    original_currency="USD",
                    amount=Decimal("60.87"),
                )
                trn.sepa_transfer = aeb43.SepaTransfer.new()
                trn.sepa_transfer.purpose = "SALA"
                trn.sepa_transfer.remitance_information = "a transfer"
                trn.sepa_transfer.originator_code = 321
            if idx == 1:
                trn.sepa_debit = aeb43.SepaDebit.new()
                trn.sepa_debit.creditor_name = "creditor1"
                trn.sepa_debit.creditor_id = 123
                trn.sepa_debit.mandate_reference = "ABCD"
                trn.sepa_debit.purpose = "OTHR"
                trn.sepa_debit.remitance_information = "a debit"

            assert acc.transactions is not None
            acc.transactions.append(trn)  # pylint: disable=no-member

        assert acc.transactions
        acc.initial_date = acc.transactions[0].transaction_date
        acc.final_date = acc.transactions[-1].transaction_date

        acc.close()

    batch.close()

    return batch


@pytest.fixture(name="bytes_sample_data_path", scope="session")
def fixture_bytes_sample_data_path():
    "data path"
    return resources.files("csb43.tests").joinpath("sample_sepa.csb")


@pytest.fixture(name="bytes_sample", scope="session")
def fixture_bytes_sample(bytes_sample_data_path, non_strict_context) -> aeb43.Batch:
    "a batch"
    with open(bytes_sample_data_path, "rb") as stream:
        return aeb43.read_batch(stream, context=non_strict_context)
