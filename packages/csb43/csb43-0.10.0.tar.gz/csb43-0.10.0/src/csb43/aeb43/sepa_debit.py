#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
SEPA direct debit records.

[es] Registros de adeudos SEPA
"""

from __future__ import annotations
from typing import Iterator, Any
import dataclasses
import enum

from ..i18n import tr as _
from ..utils import messages as msg
from .record import (
    Record,
    SingleRecordMixin,
    RecordManifest,
    chain_validator,
    AnyBytes,
)
from .record.context import ContextualMixin, Aeb43Context
from .fields.string import String, string_validator
from .fields.nested import NestedRecord
from .item import Item

# Sepa Transfer


class Field(enum.Enum):
    "field identifiers for Sepa Direct Debit"
    # código del esquema Core/B2B (AT-20) (CORE/B2B)
    SCHEME_CODE = enum.auto()
    # nombre del acreedor (AT-03)
    CREDITOR_NAME = enum.auto()
    # libre
    PADDING = enum.auto()
    # identificador del acreedor
    CREDITOR_ID = enum.auto()
    # referencia única del mandato / unique mandate reference
    MANDATE_REFERENCE = enum.auto()
    # propósito del cobro (AT-58) / the purpose of the collection
    PURPOSE = enum.auto()
    # categoría del propósito del cobro (AT-59) / the category purpose of the collection
    PURPOSE_CATEGORY = enum.auto()
    # concepto (AT-22) / the remitance information sent by the creditor
    # to the debtor in the collection
    REMITANCE_INFORMATION = enum.auto()
    REMITANCE_INFORMATION_CONT = enum.auto()
    # referencia del acreedor (AT-10) / the creditor's reference of
    # the direct debit transaction
    CREDITOR_REFERENCE = enum.auto()
    # nombre deudor (AT-14) - último deudor (AT-15) / the name of the
    # debtor - the name of the debtor reference party
    DEBTOR_NAME = enum.auto()


def validate_scheme_code(_context: Aeb43Context, value: bytes) -> tuple[str | None, None]:
    "scheme code must be CORE or B2B"
    if (value.strip() == b"CORE") or (value.strip() == b"B2B"):
        return None, None
    return _("Unknown scheme code for SEPA direct debit: '%s'") % value, None


@dataclasses.dataclass
class SepaDebitItem1(SingleRecordMixin, Record):
    """
    **COD 23-01**

    SEPA direct debit record #1

    [es] registro 1 de adeudo SEPA

    See [n43_2012]_ Appendix 4, section 2

    Fields
    ------
    scheme_code : String["CORE"|"B2B"]
        scheme code [AT-20] / código de esquema [AT-20]
    creditor_name : String[70]
        creditor name [AT-03] / nombre del acreedor [AT-03]
    padding : String[2]
        padding / espacio libre
    """
    manifest = RecordManifest(
        code=b"2301",
        sections={
            # CORE/B2B
            Field.SCHEME_CODE: (
                slice(4, 8),
                chain_validator(
                    string_validator(4),
                    validate_scheme_code,
                )
            ),
            Field.CREDITOR_NAME: (slice(8, 78), string_validator(70)),
            Field.PADDING: (slice(78, 80), string_validator(2)),
        }
    )

    scheme_code: String = dataclasses.field(
        default=String(field_id=Field.SCHEME_CODE, factory=lambda: "CORE"),
        metadata={"i18n": msg.T_SCHEME_CODE}
    )
    creditor_name: String = dataclasses.field(
        default=String(field_id=Field.CREDITOR_NAME),
        metadata={"i18n": msg.T_CREDITOR_NAME}
    )
    padding: String = dataclasses.field(
        default=String(field_id=Field.PADDING),
        metadata={"i18n": _("padding1")}
    )


@dataclasses.dataclass
class SepaDebitItem2(SingleRecordMixin, Record):
    """
    **COD 23-02**

    SEPA direct debit record #2

    [es] registro 2 de adeudo SEPA

    See [n43_2012]_ Appendix 4, section 2

    Fields
    ------
    creditor_id : String[35]
        creditor id [AT-02] / identificador del acreedor [AT-02]
    mandate_reference : String[35]
        mandate reference [AT-01] / referencia única del mandato [AT-01]
    padding : String[6]
        padding / espacio libre
    """
    manifest = RecordManifest(
        code=b"2302",
        sections={
            # identificador del acreedor
            Field.CREDITOR_ID: (slice(4, 39), string_validator(35)),
            # referencia única del mandato
            Field.MANDATE_REFERENCE: (slice(39, 74), string_validator(35)),
            # libre
            Field.PADDING: (slice(74, 80), string_validator(6)),
        }
    )

    creditor_id: String = dataclasses.field(
        default=String(field_id=Field.CREDITOR_ID),
        metadata={"i18n": msg.T_CREDITOR_ID}
    )
    mandate_reference: String = dataclasses.field(
        default=String(field_id=Field.MANDATE_REFERENCE),
        metadata={"i18n": msg.T_MANDATE_REFERENCE}
    )
    padding: String = dataclasses.field(
        default=String(field_id=Field.PADDING),
        metadata={"i18n": _("padding2")}
    )


_remitance_information_string = String(field_id=Field.REMITANCE_INFORMATION)


@dataclasses.dataclass
class SepaDebitItem3(SingleRecordMixin, Record):
    """
    **COD 23-03**

    SEPA direct debit record #3

    [es] registro 3 de adeudo SEPA

    See [n43_2012]_ Appendix 4, section 2

    Fields
    ------
    purpose : String[4]
        purpose [AT-58] / propósito del cobro [AT-58]
    purpose_category : String[4]
        purpose category [AT-59] / categoría del propósito del cobro [AT-59]
    remitance_information : String[68]
        remitance information [AT-22] / concepto [AT-22]
    """
    manifest = RecordManifest(
        code=b"2303",
        sections={
            # propósito del cobro (AT-58)
            Field.PURPOSE: (slice(4, 8), string_validator(4)),
            # categoría del propósito del cobro (AT-59)
            Field.PURPOSE_CATEGORY: (slice(8, 12), string_validator(4)),
            # concepto (AT-22)
            Field.REMITANCE_INFORMATION: (slice(12, 80), string_validator(68)),
        }
    )

    purpose: String = dataclasses.field(
        default=String(field_id=Field.PURPOSE),
        metadata={"i18n": msg.T_PURPOSE}
    )
    purpose_category: String = dataclasses.field(
        default=String(field_id=Field.PURPOSE_CATEGORY),
        metadata={"i18n": msg.T_PURPOSE_CATEGORY}
    )
    remitance_information: String = dataclasses.field(
        default=_remitance_information_string,
        metadata={"i18n": msg.T_REMITANCE_INFORMATION}
    )

    def remitance_information_part(self) -> bytes:
        "return bytes from field without right trimming"
        field = self.get_field(Field.REMITANCE_INFORMATION)
        return field.lstrip(b" ")


_remitance_information_cont_string = String(field_id=Field.REMITANCE_INFORMATION_CONT)


@dataclasses.dataclass
class SepaDebitItem4(SingleRecordMixin, Record):
    """
    **COD 23-04**

    SEPA direct debit record #4

    [es] registro 4 de adeudo SEPA

    See [n43_2012]_ Appendix 4, section 2

    Fields
    ------
    remitance_information : String[72]
        remitance information continuation [AT-22] / continuación del concepto [AT-22]
    padding : String[4]
        padding / espacio libre
    """
    manifest = RecordManifest(
        code=b"2304",
        sections={
            Field.REMITANCE_INFORMATION_CONT: (slice(4, 76), string_validator(72)),
            Field.PADDING: (slice(76, 80), string_validator(4)),
        }
    )

    remitance_information_cont: String = dataclasses.field(
        default=_remitance_information_cont_string,
        metadata={"i18n": _("remitance_information_cont")}
    )
    padding: String = dataclasses.field(
        default=String(field_id=Field.PADDING),
        metadata={"i18n": _("padding4")}
    )

    def remitance_information_part(self) -> bytes:
        "return bytes from field without left trimming"
        field = self.get_field(Field.REMITANCE_INFORMATION_CONT)
        return field.rstrip(b" ")


@dataclasses.dataclass
class SepaDebitItem5(SingleRecordMixin, Record):
    """
    **COD 23-05**

    SEPA direct debit record #5

    [es] registro 5 de adeudo SEPA

    See [n43_2012]_ Appendix 4, section 2

    Fields
    ------
    creditor_reference : String[35]
        creditor reference [AT-10] / referencia del acreedor [AT-10]
    debtor_name : String[41]
        debtor name [AT-14] / último deudor [AT-15]
    """
    manifest = RecordManifest(
        code=b"2305",
        sections={
            Field.CREDITOR_REFERENCE: (slice(4, 39), string_validator(35)),
            Field.DEBTOR_NAME: (slice(39, 80), string_validator(41)),
        }
    )

    creditor_reference: String = dataclasses.field(
        default=String(field_id=Field.CREDITOR_REFERENCE),
        metadata={"i18n": msg.T_CREDITOR_REFERENCE}
    )
    debtor_name: String = dataclasses.field(
        default=String(field_id=Field.DEBTOR_NAME),
        metadata={"i18n": msg.T_DEBTOR_NAME}
    )


class SepaMixin:
    "common records for SEPA direct debit / transfer"
    item3: NestedRecord[SepaDebitItem3]
    item4: NestedRecord[SepaDebitItem4]

    @property
    def remitance_information(self):
        "remitance information [AT-22] / concepto [AT-22]"
        # pylint: disable=no-member
        if not self.item4.remitance_information_cont:
            return self.item3.remitance_information
        field1 = self.item3.remitance_information_part()
        field2 = self.item4.remitance_information_part()
        return (field1 + field2).decode(self.get_context().encoding)

    # pylint: disable=no-member
    @remitance_information.setter
    def remitance_information(self, value):
        size = SepaDebitItem3.manifest.size_for(Field.REMITANCE_INFORMATION)
        if not isinstance(value, (bytes, bytearray)):
            b_value = self.get_context().to_string(value).encode(self.get_context().encoding)
        else:
            b_value = value
        assert self.item3
        self.item3.update_fields(_remitance_information_string.pad(self.item3, b_value[:size]))
        assert self.item4
        self.item4.update_fields(_remitance_information_cont_string.pad(self.item4, b_value[size:]))

    @property
    def purpose(self):
        "purpose [AT-58] / propósito del cobro [AT-58]"
        # pylint: disable=no-member
        return self.item3.purpose

    @purpose.setter
    def purpose(self, value):
        self.item3.purpose = value

    @property
    def purpose_category(self):
        "purpose category [AT-59] / categoría del propósito del cobro [AT-59]"
        # pylint: disable=no-member
        return self.item3.purpose_category

    @purpose_category.setter
    def purpose_category(self, value):
        self.item3.purpose_category = value

    @staticmethod
    def pad_items(*records: AnyBytes, max_items=5) -> list[AnyBytes | None]:
        "return 5 bytes records or None"
        items: list[AnyBytes | None] = list(records)
        size = len(items)
        if size < max_items:
            items.extend([None] * (max_items - size))
        return items[:max_items]

    def _update_dict(self, data: dict[str, Any], translated: bool):
        assert self.item3
        data.update(self.item3.to_dict(translated))
        assert self.item4
        data.update(self.item4.to_dict(translated))
        k_ric = "remitance_information_cont"
        if translated:
            k_ric = _(k_ric)
        k_ri = "remitance_information"
        if translated:
            k_ri = _(k_ri)
        if k_ric in data:
            del data[k_ric]
        data[k_ri] = self.remitance_information


@dataclasses.dataclass
class SepaDebit(SepaMixin, ContextualMixin):
    """SEPA direct debit

    Set of five 80-bytes records

    See [n43_2012]_ Appendix 4, section 2
    """
    item1: NestedRecord[SepaDebitItem1] = NestedRecord(SepaDebitItem1)
    item2: NestedRecord[SepaDebitItem2] = NestedRecord(SepaDebitItem2)
    item3: NestedRecord[SepaDebitItem3] = NestedRecord(SepaDebitItem3)
    item4: NestedRecord[SepaDebitItem4] = NestedRecord(SepaDebitItem4)
    item5: NestedRecord[SepaDebitItem5] = NestedRecord(SepaDebitItem5)
    context: Aeb43Context | None = None

    @classmethod
    def new(
        cls,
        *records: AnyBytes,
        context: Aeb43Context | None = None,
    ) -> "SepaDebit":
        "return an empty/default SEPA direct debit object"
        items = cls.pad_items(*records)
        return cls(
            SepaDebitItem1(context=context, raw=items[0]),  # type: ignore
            SepaDebitItem2(context=context, raw=items[1]),  # type: ignore
            SepaDebitItem3(context=context, raw=items[2]),  # type: ignore
            SepaDebitItem4(context=context, raw=items[3]),  # type: ignore
            SepaDebitItem5(context=context, raw=items[4]),  # type: ignore
        )

    @property
    def scheme_code(self):
        "scheme code [AT-20] / código de esquema [AT-20]"
        # pylint: disable=no-member
        return self.item1.scheme_code

    @scheme_code.setter
    def scheme_code(self, value):
        self.item1.scheme_code = value

    @property
    def creditor_name(self):
        "creditor name [AT-03] / nombre del acreedor [AT-03]"
        # pylint: disable=no-member
        return self.item1.creditor_name

    @creditor_name.setter
    def creditor_name(self, value):
        self.item1.creditor_name = value

    @property
    def creditor_id(self):
        "creditor id [AT-02] / identificador del acreedor [AT-02]"
        # pylint: disable=no-member
        return self.item2.creditor_id

    @creditor_id.setter
    def creditor_id(self, value):
        self.item2.creditor_id = value

    @property
    def mandate_reference(self):
        "mandate reference [AT-01] / referencia única del mandato [AT-01]"
        # pylint: disable=no-member
        return self.item2.mandate_reference

    @mandate_reference.setter
    def mandate_reference(self, value):
        self.item2.mandate_reference = value

    @property
    def creditor_reference(self):
        "creditor reference [AT-10] / referencia del acreedor [AT-10]"
        # pylint: disable=no-member
        return self.item5.creditor_reference

    @creditor_reference.setter
    def creditor_reference(self, value):
        self.item5.creditor_reference = value

    @property
    def debtor_name(self):
        "debtor name [AT-14] / último deudor [AT-15]"
        # pylint: disable=no-member
        return self.item5.debtor_name

    @debtor_name.setter
    def debtor_name(self, value):
        self.item5.debtor_name = value

    def as_optional_items(self) -> Iterator[Item]:
        "convert to vanilla complementary items"
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
