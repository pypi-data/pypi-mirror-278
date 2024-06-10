#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations

import pytest

from ..aeb43.record.context import Aeb43Context, InformationMode
from ..aeb43.batch import Batch, read_batch
from ..aeb43.record.errors import ValidationException
from ..aeb43.account import Account
from ..aeb43.transaction import Transaction


def read_data(path, context):
    "read a batch"
    with open(path, "rb") as stream:
        return read_batch(stream, context)


@pytest.fixture(name="batch1")
def fixture_batch(bytes_sample_data_path, non_strict_context: Aeb43Context) -> Batch:
    "a batch"
    return read_data(bytes_sample_data_path, non_strict_context)


def test_read_strict_batch(bytes_sample_data_path, strict_context: Aeb43Context):
    "strict batch info 3 will fail reference1"
    with pytest.raises(ValidationException):
        read_data(bytes_sample_data_path, strict_context)


def test_n_accounts(batch1: Batch):
    "there is only 1 account"
    assert batch1.accounts is not None
    assert len(batch1.accounts) == 1


def test_batch_is_closed(batch1: Batch):
    "batch is properly closed"
    assert batch1.is_closed()


def test_n_records(batch1: Batch):
    "check batch number of records"
    assert batch1.summary is not None
    assert batch1.summary.total_records == 38


@pytest.fixture(name="account")
def fixture_account(batch1: Batch):
    "return unique account"
    assert batch1.accounts is not None
    return batch1.accounts[0]


def test_account_is_closed(account: Account):
    "check the account is closed"
    assert account.is_closed()


def test_n_transactions(account: Account):
    "check number of transactions"
    assert account.transactions is not None
    assert len(account.transactions) == 14


@pytest.fixture(name="transaction", params=range(14), ids=lambda x: f"transaction{x}")
def fixture_transaction(account: Account, request):
    "a transaction with index"
    assert account.transactions
    return request.param, account.transactions[request.param]


def test_transaction_context(transaction: tuple[int, Transaction]):
    "check that the transaction acquires parent account's context"
    _idx, tran = transaction
    assert tran.get_context().information_mode == InformationMode.THIRD


def test_sepa_transaction(transaction: tuple[int, Transaction]):
    "check transaction items"
    idx, tran = transaction
    if idx in (1, 4):
        context = tran.get_context()
        if context.sepa:
            assert not tran.optional_items
            assert tran.sepa_debit is not None
        else:
            assert tran.optional_items and len(tran.optional_items) == 5
            assert tran.sepa_transfer is None
            assert tran.sepa_debit is None
    else:
        assert tran.optional_items and len(tran.optional_items) == 1
        assert tran.sepa_transfer is None
        assert tran.sepa_debit is None
