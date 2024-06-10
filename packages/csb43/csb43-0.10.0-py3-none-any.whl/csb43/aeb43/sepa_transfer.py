#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
SEPA transfer records.

[es] Registros de transferencias SEPA
"""

from __future__ import annotations
from typing import Iterator
import dataclasses
import enum

from ..utils import messages as msg
from .record import (
    Record,
    SingleRecordMixin,
    RecordManifest,
    AnyBytes
)
from .record.context import ContextualMixin, Aeb43Context
from .fields.string import String, string_validator
from .fields.nested import NestedRecord
from .item import Item
from .sepa_debit import (
    SepaDebitItem3,
    SepaDebitItem4,
    SepaMixin,
)

# Sepa Transfer


class Field(enum.Enum):
    "field identifiers for Sepa Transfer"
    # nombre del ordenante (AT-02)
    ORIGINATOR_NAME = enum.auto()
    # código del ordenante (AT-10)
    ORIGINATOR_CODE = enum.auto()
    # referencia del ordenante (AT-41)
    ORIGINATOR_REFERENCE = enum.auto()
    # nombre de "por cuenta de" (AT-08)
    ORIGINATOR_REFERENCE_PARTY = enum.auto()
    # propósito de la transferencia (AT-44)
    PURPOSE = enum.auto()
    # categoría del propósito de la transferencia (AT-45) [ISO 20022 UNIFI]
    PURPOSE_CATEGORY = enum.auto()
    # concepto (AT-05)
    REMITANCE_INFORMATION = enum.auto()
    REMITANCE_INFORMATION_CONT = enum.auto()
    PADDING = enum.auto()
    ADDITIONAL_INFO = enum.auto()


@dataclasses.dataclass
class SepaTransferItem1(SingleRecordMixin, Record):
    """
    **COD 23-01**

    SEPA transfer record #1

    [es] registro 1 de transferencia SEPA

    See [n43_2012]_ Appendix 4, section 1

    Fields
    ------
    originator_name : String[66]
        originator name [AT-02] / nombre del ordenante [AT-02]
    originator_code : String[10]
        originator code [AT-02] / código del ordenante [AT-02]
    """
    manifest = RecordManifest(
        code=b"2301",
        sections={
            Field.ORIGINATOR_NAME: (slice(4, 70), string_validator(66)),
            Field.ORIGINATOR_CODE: (slice(70, 80), string_validator(10)),
        }
    )

    originator_name: String = dataclasses.field(
        default=String(field_id=Field.ORIGINATOR_NAME),
        metadata={"i18n": msg.T_ORIGINATOR_NAME}
    )
    originator_code: String = dataclasses.field(
        default=String(field_id=Field.ORIGINATOR_CODE),
        metadata={"i18n": msg.T_ORIGINATOR_CODE}
    )


@dataclasses.dataclass
class SepaTransferItem2(SingleRecordMixin, Record):
    """
    **COD 23-02**

    SEPA transfer record #2

    [es] registro 2 de transferencia SEPA

    See [n43_2012]_ Appendix 4, section 1

    Fields
    ------
    originator_reference : String[35]
        originator reference [AT-41] / referencia del ordenante [AT-41]
    originator_reference_party : String[41]
        originator reference party [AT-08] & nombre de "por cuenta de" [AT-08]
    """
    manifest = RecordManifest(
        code=b"2302",
        sections={
            Field.ORIGINATOR_REFERENCE: (slice(4, 39), string_validator(35)),
            Field.ORIGINATOR_REFERENCE_PARTY: (slice(39, 80), string_validator(41)),
        }
    )

    originator_reference: String = dataclasses.field(
        default=String(field_id=Field.ORIGINATOR_REFERENCE),
        metadata={"i18n": msg.T_ORIGINATOR_REFERENCE}
    )
    originator_reference_party: String = dataclasses.field(
        default=String(field_id=Field.ORIGINATOR_REFERENCE_PARTY),
        metadata={"i18n": msg.T_ORIGINATOR_REFERENCE_PARTY}
    )


@dataclasses.dataclass
class SepaTransferItem5(SingleRecordMixin, Record):
    """
    **COD 23-05**

    SEPA transfer record #5

    [es] registro 5 de transferencia SEPA

    See [n43_2012]_ Appendix 4, section 1

    Fields
    ------
    additional_info : String[76]
        additional info / campo de libre uso para información del beneficiario
    """
    manifest = RecordManifest(
        code=b"2305",
        sections={
            Field.ADDITIONAL_INFO: (slice(4, 80), string_validator(76)),
        }
    )

    additional_info: String = dataclasses.field(
        default=String(field_id=Field.ADDITIONAL_INFO),
        metadata={"i18n": msg.T_ADDITIONAL_INFO}
    )


@dataclasses.dataclass
class SepaTransfer(ContextualMixin, SepaMixin):
    """SEPA transfer

    Set of five 80-bytes records

    See [n43_2012]_ Appendix 4, section 1
    """
    item1: NestedRecord[SepaTransferItem1] = NestedRecord(SepaTransferItem1)
    item2: NestedRecord[SepaTransferItem2] = NestedRecord(SepaTransferItem2)
    item3: NestedRecord[SepaDebitItem3] = NestedRecord(SepaDebitItem3)
    item4: NestedRecord[SepaDebitItem4] = NestedRecord(SepaDebitItem4)
    item5: NestedRecord[SepaTransferItem5] = NestedRecord(SepaTransferItem5)
    context: Aeb43Context | None = None

    @classmethod
    def new(
        cls,
        *records: AnyBytes,
        context: Aeb43Context | None = None
    ) -> "SepaTransfer":
        "return an empty/default SEPA transfer object"
        items = cls.pad_items(*records)
        return cls(
            SepaTransferItem1(context=context, raw=items[0]),  # type: ignore
            SepaTransferItem2(context=context, raw=items[1]),  # type: ignore
            SepaDebitItem3(context=context, raw=items[2]),  # type: ignore
            SepaDebitItem4(context=context, raw=items[3]),  # type: ignore
            SepaTransferItem5(context=context, raw=items[4]),  # type: ignore
        )

    @property
    def originator_name(self):
        "originator name [AT-02] / nombre del ordenante [AT-02]"
        # pylint: disable=no-member
        return self.item1.originator_name

    @originator_name.setter
    def originator_name(self, value):
        self.item1.originator_name = value

    @property
    def originator_code(self):
        "originator code [AT-02] / código del ordenante [AT-02]"
        # pylint: disable=no-member
        return self.item1.originator_code

    @originator_code.setter
    def originator_code(self, value):
        self.item1.originator_code = value

    @property
    def originator_reference(self):
        "originator reference [AT-41] / referencia del ordenante [AT-41]"
        # pylint: disable=no-member
        return self.item2.originator_reference

    @originator_reference.setter
    def originator_reference(self, value):
        self.item2.originator_reference = value

    @property
    def originator_reference_party(self):
        "originator reference party [AT-08] & nombre de 'por cuenta de' [AT-08]"
        # pylint: disable=no-member
        return self.item2.originator_reference_party

    @originator_reference_party.setter
    def originator_reference_party(self, value):
        self.item2.originator_reference_party = value

    @property
    def additional_info(self):
        "additional info / campo de libre uso para información del beneficiario"
        # pylint: disable=no-member
        return self.item5.additional_info

    @additional_info.setter
    def additional_info(self, value):
        self.item5.additional_info = value

    def as_optional_items(self) -> Iterator[Item]:
        "convert to conventional vanilla items"
        for raw in iter(self):
            # pylint: disable=no-member
            yield Item(self.context, raw=raw)

    def __iter__(self) -> Iterator[bytes]:
        assert self.item1
        yield bytes(self.item1)
        assert self.item2
        yield bytes(self.item2)
        assert self.item3
        yield bytes(self.item3)
        assert self.item4
        yield bytes(self.item4)
        assert self.item5
        yield bytes(self.item5)

    def to_dict(self, translated: bool=True):
        "return dict with field values"
        assert self.item1
        # pylint: disable=no-member
        data = self.item1.to_dict(translated)
        assert self.item2
        data.update(self.item2.to_dict(translated))
        assert self.item3
        self._update_dict(data, translated)
        assert self.item5
        data.update(self.item5.to_dict(translated))
        return data
