#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Batch of accounts

[es] Lote de cuentas
"""

from __future__ import annotations
from typing import (
    Iterator,
    IO,
)
import dataclasses
import enum

from ..utils import messages as msg
from ..utils.tabulated import adjust_table_width
from ..i18n import tr as _
from .record import (
    RecordManifest,
    SingleRecordMixin,
    CompositeRecordMixin,
)
from .record.context import (
    Aeb43Context,
    BatchContext,
    ContextualMixin,
)
from .fields.nested import NestedCollection, RecordCollection, Contextual
from .fields.integer import Integer, IntegerValidator
from .fields.string import String, string_validator
from .account import Account
from .closing import Closeable, ClosingRecord, SummaryField


class Field(enum.Enum):
    "field identifiers for EndOfFile record"
    TOTAL_RECORDS = enum.auto()
    PADDING = enum.auto()


@dataclasses.dataclass
class EndOfFile(SingleRecordMixin, ClosingRecord):
    """
    **COD 88**

    End of file record

    [es] Registro de fin de fichero

    See [n43_2012]_ Appendix 1, section 1.6

    Fields
    ------
    total_records : Integer
        total number of records / número total de registros
    padding : String[54]
        padding / libre uso
    """
    manifest = RecordManifest(
        code=b"88" + b"9" * 18,
        sections={
            Field.TOTAL_RECORDS: (slice(20, 26), IntegerValidator(6)),
            Field.PADDING: (slice(26, 80), string_validator(54)),
        }
    )

    total_records: Integer = dataclasses.field(
        default=Integer(Field.TOTAL_RECORDS),
        metadata={"i18n": _("total_records")}
    )
    padding: String = dataclasses.field(
        default=String(Field.PADDING),
        metadata={"i18n": msg.T_PADDING}
    )


def _create_account_collection(record: Contextual, initial_values):
    "account record factory"
    assert isinstance(record, Batch)
    return RecordCollection(
        context_f=record.get_context,
        record_type=Account,
        initial_data=initial_values
    )


@dataclasses.dataclass
class Batch(ContextualMixin, CompositeRecordMixin, Closeable):
    """
    A batch of transactions grouped by accounts

    Fields
    ------
    accounts : list[Account]
        accounts / cuentas
    summary : EndOfFile
        summary record / registro de recuento
    """
    context: Aeb43Context | None = None
    accounts: NestedCollection[Account] = NestedCollection(_create_account_collection)
    summary: SummaryField[EndOfFile] = SummaryField(EndOfFile, optional=True)

    def _create_summary(self) -> int:
        total_records = 0
        # pylint: disable=not-an-iterable
        assert self.accounts is not None
        for account in self.accounts:
            for _record in account:
                total_records += 1
        return total_records

    def _set_new_summary(self):
        total_records = self._create_summary()
        summary = EndOfFile(context=self.context)
        summary.total_records = total_records
        self.summary = summary

    def is_closed(self):
        return self.summary is not None

    def validate_summary(self, summary: EndOfFile):
        total_records = self._create_summary()
        if total_records != summary.total_records:
            self.get_context().emit_validation_error(_(
                "incongruent closing record of file: "
                "total records {alt:d} != {ref:d}"
            ).format(alt=summary.total_records, ref=total_records))

    # pylint: disable=not-an-iterable
    def __iter__(self) -> Iterator[bytes]:
        assert self.accounts is not None
        for account in self.accounts:
            yield from account
        if self.summary:
            yield from self.summary

    def accepts_nested_codes(self, record: bytes):
        if self.is_closed():
            return False
        return (
            record.startswith(Account.manifest.code)
            or (self.accounts and self.accounts[-1].accepts_nested_codes(record))
            or record.startswith(EndOfFile.manifest.code)
        )

    def append(self, raw: bytes):
        if self.is_closed():
            self.get_context().emit_validation_error(_("adding records to a closed batch"))
        if not self.summary and raw.startswith(EndOfFile.manifest.code):
            self.summary = raw
        elif raw.startswith(Account.manifest.code):
            # pylint: disable=no-member
            assert self.accounts is not None
            self.accounts.append(raw)
        elif self.accounts:
            self.accounts[-1].append(raw)
        else:
            self.get_context().emit_validation_error(
                _("unknown or illegal record: {}").format(raw)
            )

    def to_dict(self, translated=True):
        "return content as a dictionary"
        # pylint: disable=no-member
        data = {}
        if self.summary:
            k_sum = msg.T_SUMMARY if translated else "summary"
            data[k_sum] = self.summary.to_dict(translated)
        if self.accounts:
            # pylint: disable=not-an-iterable
            k_tr = msg.T_ACCOUNTS if translated else "accounts"
            data[k_tr] = [
                tran.to_dict(translated)
                for tran in self.accounts
            ]
        return data

    def describe(self, indent: str = ""):
        templates = [
            _("Encoding: {encoding:s}"),
            _("File properly closed: {file_is_closed}")
        ] + list(adjust_table_width((
            _("Accounts read:||{naccounts:>5d}"),
            _("Records read:||{total_records:>5d}"),
        )))

        if self.summary:
            # pylint: disable=no-member
            total_records = self.summary.total_records
        else:
            total_records = self._create_summary()

        assert self.accounts is not None
        header = "\n".join(indent + line for line in templates).format(
            encoding=self.get_context().encoding,
            naccounts=len(self.accounts),
            file_is_closed=self.is_closed(),
            total_records=total_records
        )

        return header + "\n\n" + "\n\n".join(acc.describe(indent=indent) for acc in self.accounts)

    def dump(self) -> bytes:
        "dump content to bytes"
        return b"\n".join(self)


def read_batch(stream: IO[bytes], context: Aeb43Context | None = None) -> Batch:
    "read a batch of accounts from a binary stream"
    batch = Batch(context=context)
    with BatchContext().scope() as b_context:
        for idx, line in enumerate(stream):
            b_context.line = idx
            batch.append(line.rstrip(b'\r\n'))
    return batch
