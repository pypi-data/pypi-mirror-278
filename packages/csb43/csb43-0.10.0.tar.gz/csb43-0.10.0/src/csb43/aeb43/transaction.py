#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Main transaction record.

[es] Registro principal de movimientos
"""

from __future__ import annotations
from typing import Iterator
from types import MappingProxyType
import dataclasses
import enum
import weakref

from ..utils import messages as msg
from ..i18n import tr as _
from .record import (
    Record,
    RecordManifest,
    Aeb43Context,
    RegexValidator,
    chain_validator,
    CompositeRecordMixin,
)
from .record.errors import ValidationException
from .record.context import InformationMode
from .fields.string import String, string_validator, Trim
from .fields.integer import Integer, IntegerValidator
from .fields.date import Date, date_validator
from .fields.money import Money, money_validator, money_mode_validator
from .fields.nested import (
    NestedRecord,
    RecordCollection,
    NestedCollection,
    NestedContextual,
)
from .fields.information_mode import OnModeValidator
from .exchange import Exchange
from .item import Item, MIN_ITEMS, MAX_ITEMS
from .sepa_transfer import SepaTransfer
from .sepa_debit import SepaDebit


class Field(enum.Enum):
    "field identifiers for Transaction record"
    PADDING = enum.auto()
    BRANCH_CODE = enum.auto()
    TRANSACTION_DATE = enum.auto()
    VALUE_DATE = enum.auto()
    SHARED_ITEM = enum.auto()
    OWN_ITEM = enum.auto()
    EXPENSE_OR_INCOME = enum.auto()
    AMOUNT = enum.auto()
    DOCUMENT_NUMBER = enum.auto()
    REFERENCE1 = enum.auto()
    REFERENCE2 = enum.auto()


_branch_code_val23 = RegexValidator(br"^\d{4}$", warning=True)


def validate_reference1(context: Aeb43Context, value: bytes) -> tuple[None, str | None]:
    "reference1 validation for information mode 3"
    if context.information_mode != InformationMode.THIRD:
        return None, None
    digits = value.strip(b" ").decode(context.encoding)

    try:
        control = int((digits or '0')[-1])
        res = (
            sum(
                int(digit) * ((idx % 8) + 2)
                for (idx, digit) in enumerate(reversed(digits[:-1]))
            ) % 11
        ) % 10
    except ValueError:
        res = -1
        control = -2

    if res == control:
        return None, None
    return None, _("Validation failed for reference '{ref}'. Unexpected control digit.").format(
        ref=value
    )


@dataclasses.dataclass
class ItemCollection(RecordCollection[Item]):
    "Nested record collection for complementary items"
    parent: "Transaction" | None = None

    def _process_item(self, item: Item) -> Item:
        assert self.parent
        if item in self._data:
            self.parent.get_context().emit_validation_error(
                _("the appended optional item already exists")
            )
        if self.parent.sepa_transfer:
            self.parent.get_context().emit_validation_error(_("a SEPA transfer exists"))
        if self.parent.sepa_debit:
            self.parent.get_context().emit_validation_error(_("a SEPA debit exists"))
        size = len(self._data)
        if size == MAX_ITEMS:
            self.parent.get_context().emit_validation_error(
                _("there can only be {max_items:d} optional items").format(max_items=MAX_ITEMS)
            )
        next_record = size + MIN_ITEMS
        if item.record_code != next_record:
            self.parent.get_context().emit_validation_warning(
                _(
                    "`record_code` should be {next:d} but found {code:d}. "
                    "The wrong value will be fixed"
                ).format(next=next_record, code=item.record_code)
            )
            item.record_code = next_record
        return item

    def _post_append(self):
        assert self.parent
        if self.parent.get_context().sepa and (len(self._data) == MAX_ITEMS):
            self.parent.to_sepa()


def _create_item_collection(record, initial_values) -> ItemCollection:
    "complementary item factory"
    assert isinstance(record, Transaction)
    return ItemCollection(
        context_f=record.get_context,
        record_type=Item,
        parent=weakref.proxy(record),
        initial_data=initial_values
    )


@dataclasses.dataclass(frozen=True)
class SepaTransferField(NestedContextual):
    "nested SEPA transfer field"

    def _set_value(self, this, value):
        assert isinstance(this, Transaction)
        if this.optional_items:
            this.get_context().emit_error(_(
                "trying to set a SEPA transfer while the transaction "
                "contains some standard optional items"
            ))
        if this.sepa_debit:
            this.get_context().emit_error(_(
                "trying to set a SEPA transfer while the transaction "
                "contains a SEPA Direct Debit record set"
            ))
        super()._set_value(this, value)


@dataclasses.dataclass(frozen=True)
class SepaDebitField(NestedContextual):
    "nested SEPA direct debit field"

    def _set_value(self, this, value):
        assert isinstance(this, Transaction)
        if this.optional_items:
            this.get_context().emit_error(_(
                "trying to set a SEPA transfer while the transaction "
                "contains some standard optional items"
            ))
        if this.sepa_transfer:
            this.get_context().emit_error(_(
                "trying to set a SEPA transfer while the transaction "
                "contains a SEPA Transfer record set"
            ))
        super()._set_value(this, value)


@dataclasses.dataclass(frozen=True)
class BranchCode(String):
    "String for branch code: info mode 1 allows an empty field"

    def adapt(self, this: Record, value: str) -> str:
        if this.get_context().information_mode == InformationMode.FIRST:
            if (value is None) or isinstance(value, (bytes, str)):
                str_value = (value or "").strip()
                if not str_value:
                    return " " * this.manifest.size_for(self.field_id)
        return super().adapt(this, value)

    def to_field(self, this: Record) -> str:
        if this.get_context().information_mode != InformationMode.FIRST:
            return super().to_field(this)
        value = this.get_field(self.field_id)
        if not value.strip():
            return ""
        return super().to_field(this)


_ref1_val12 = string_validator(12)


# pylint: disable=too-many-instance-attributes
@dataclasses.dataclass
class Transaction(CompositeRecordMixin, Record):
    """
    **COD 22**

    Main transaction record

    [es] Registro principal de movimientos

    See [n43_2012]_ Appendix 1, section 1.2

    Fields
    ------
    padding : String[4]
        padding / libre uso
    branch_code : String[4]
        branch code / clave de oficina origen
    document_number : String[10]
        document number / número de documento
    transaction_date : Date
        date of transaction / fecha de operación
    value_date : Date
        effective date / fecha de valor
    shared_item : Integer[0..99]
        shared item / concepto común
    own_item : Integer[0..999]
        own item / concepto propio
    amount : Money[12.2]
        transaction amont / importe
    reference1 : String[12]
        reference 1 / referencia 1
    reference2 : String[16]
        reference 2 / referencia 2
    """
    manifest = RecordManifest(
        code=b"22",
        sections={
            Field.PADDING: (slice(2, 6), string_validator(4)),
            Field.BRANCH_CODE: (slice(6, 10), OnModeValidator(
                RegexValidator(br"^\d{4}| {4}$", warning=True),
                _branch_code_val23,
                _branch_code_val23
            )),
            Field.TRANSACTION_DATE: (slice(10, 16), date_validator()),
            Field.VALUE_DATE: (slice(16, 22), date_validator()),
            Field.SHARED_ITEM: (slice(22, 24), IntegerValidator(2, warning=True)),
            Field.OWN_ITEM: (slice(24, 27), IntegerValidator(3, warning=True)),
            Field.EXPENSE_OR_INCOME: (slice(27, 28), money_mode_validator()),
            Field.AMOUNT: (slice(28, 42), money_validator()),
            Field.DOCUMENT_NUMBER: (slice(42, 52), IntegerValidator(10, warning=True)),
            Field.REFERENCE1: (
                slice(52, 64),
                OnModeValidator(
                    _ref1_val12,
                    _ref1_val12,
                    chain_validator(
                        IntegerValidator(12, warning=True),
                        validate_reference1
                    )
                )
            ),
            Field.REFERENCE2: (slice(64, 80), string_validator(16)),
        }
    )

    padding: String = dataclasses.field(
        default=String(Field.PADDING),
        metadata={"i18n": msg.T_PADDING}
    )
    branch_code: String = dataclasses.field(
        default=BranchCode(
            Field.BRANCH_CODE, padding=b"0", trim=Trim.BOTH_BLANK, align_left=False
        ),
        metadata={"i18n": msg.T_BRANCH_CODE}
    )
    document_number: String = dataclasses.field(
        default=String(
            Field.DOCUMENT_NUMBER, padding=b"0", trim=Trim.BOTH_BLANK, align_left=False
        ),
        metadata={"i18n": msg.T_DOCUMENT_NUMBER}
    )
    transaction_date: Date = dataclasses.field(
        default=Date(Field.TRANSACTION_DATE),
        metadata={"i18n": msg.T_TRANSACTION_DATE}
    )
    value_date: Date = dataclasses.field(
        default=Date(Field.VALUE_DATE),
        metadata={"i18n": msg.T_VALUE_DATE}
    )
    shared_item: Integer = dataclasses.field(
        default=Integer(Field.SHARED_ITEM),
        metadata={"i18n": msg.T_SHARED_ITEM}
    )
    own_item: Integer = dataclasses.field(
        default=Integer(Field.OWN_ITEM),
        metadata={"i18n": msg.T_OWN_ITEM}
    )
    amount: Money = dataclasses.field(
        default=Money(value_id=Field.AMOUNT, mode_id=Field.EXPENSE_OR_INCOME),
        metadata={"i18n": msg.T_AMOUNT}
    )
    reference1: String = dataclasses.field(
        default=String(
            Field.REFERENCE1,
            mode=MappingProxyType({
                InformationMode.THIRD: {
                    "padding": b"0", "trim": Trim.BOTH_BLANK, "align_left": False
                }
            })
        ),
        metadata={"i18n": msg.T_REFERENCE_1}
    )
    reference2: String = dataclasses.field(
        default=String(Field.REFERENCE2),
        metadata={"i18n": msg.T_REFERENCE_2}
    )
    exchange: NestedRecord[Exchange] = NestedRecord(Exchange, optional=True)
    optional_items: NestedCollection[Item] = NestedCollection(_create_item_collection)
    sepa_transfer: SepaTransferField = SepaTransferField(SepaTransfer, optional=True)
    sepa_debit: SepaDebitField = SepaDebitField(SepaDebit, optional=True)

    def to_sepa(self) -> None:
        "convert complementary items to a SEPA debit/transfer object"
        if self.sepa_transfer or self.sepa_debit:
            return
        if not self.get_context().sepa:
            self.get_context().emit_validation_error(_("SEPA mode is disabled"))
        if not self.optional_items:
            return
        # pylint: disable=not-an-iterable
        items = [bytes(x) for x in self.optional_items]
        debit: SepaDebit | None = None
        transfer: SepaTransfer | None = None
        try:
            debit = SepaDebit.new(*items, context=self.get_context())
        except ValidationException:
            try:
                transfer = SepaTransfer.new(*items, context=self.get_context())
            except ValidationException:
                return
        if debit or transfer:
            # pylint: disable=no-member
            self.optional_items.clear()
        if debit:
            self.sepa_debit = debit
        elif transfer:
            self.sepa_transfer = transfer

    # pylint: disable=not-an-iterable
    def __iter__(self):
        yield bytes(self)
        if self.exchange:
            yield bytes(self.exchange)
        for item in self.optional_items:
            yield bytes(item)
        if self.sepa_transfer:
            yield from self.sepa_transfer
        if self.sepa_debit:
            yield from self.sepa_debit

    def accepts_nested_codes(self, record: bytes) -> bool:
        if not self.exchange and record.startswith(Exchange.manifest.code):
            return True

        assert self.optional_items is not None
        return (
            (not self.sepa_transfer or not self.sepa_debit)
            and (len(self.optional_items) < MAX_ITEMS)
            and record.startswith(Item.manifest.code)
        )

    def append(self, raw: bytes):
        if raw.startswith(Exchange.manifest.code):
            if self.exchange:
                self.get_context().emit_validation_error(
                    _("adding another exchange record will replace the existing record")
                )
            self.exchange = raw
        elif raw.startswith(Item.manifest.code):
            # pylint: disable=no-member
            assert self.optional_items is not None
            self.optional_items.append(raw)
        else:
            self.get_context().emit_validation_error(
                _("unknown or illegal record: {record}").format(record=raw)
            )

    def to_dict(self, translated=True):
        # pylint: disable=no-member
        data = super().to_dict(translated)
        if self.exchange:
            k_ex = msg.T_EXCHANGE if translated else "exchange"
            data[k_ex] = self.exchange.to_dict(translated)
        if self.optional_items:
            k_oi = msg.T_OPTIONAL_ITEMS if translated else "optional_items"
            data[k_oi] = [
                item.to_dict(translated)
                for item in self.optional_items
            ]
        if self.sepa_debit:
            k_sd = msg.T_SEPA_DEBIT if translated else "sepa_debit"
            data[k_sd] = self.sepa_debit.to_dict(translated)
        if self.sepa_transfer:
            k_sd = msg.T_SEPA_TRANSFER if translated else "sepa_transfer"
            data[k_sd] = self.sepa_transfer.to_dict(translated)
        return data

    def iter_optional_items(self) -> Iterator[str]:
        "iterate optional items fields"
        if not self.optional_items:
            return
        for item in self.optional_items:
            yield item.item1
            yield item.item2


# items - conceptos comunes
# See [n43_2012] Appendix 2, section 1. CONCEPTOS COMUNES
CONCEPTOS = {
    '01': "TALONES - REINTEGROS",
    '02': "ABONARES - ENTREGAS - INGRESOS",
    '03': "DOMICILIADOS - RECIBOS - LETRAS - PAGOS POR SU CUENTA",
    '04': "GIROS - TRANSFERENCIAS - TRASPASOS - CHEQUES",
    '05': "AMORTIZACIONES, PRESTAMOS, CREDITOS, ETC.",
    '06': "REMESAS, EFECTOS",
    '07': "SUSCRIPCIONES - DIV. PASIVOS - CANJES",
    '08': "DIV. CUPONES - PRIMA JUNTA - AMORTIZACIONES",
    '09': "OPERACIONES DE BOLSA Y/O COMPRA/VENTA VALORES",
    '10': "CHEQUES GASOLINA",
    '11': "CAJERO AUTOMATICO",
    '12': "TARJETAS DE CREDITO - TARJETAS DE DEBITO",
    '13': "OPERACIONES EXTRANJERO",
    '14': "DEVOLUCIONES E IMPAGADOS",
    '15': "NOMINAS - SEGUROS SOCIALES",
    '16': "TIMBRES - CORRETAJE - POLIZA",
    '17': "INTERESES - COMISIONES - CUSTODIA - GASTOS E IMPUESTOS",
    '98': "ANULACIONES - CORRECCIONES ASIENTO",
    '99': "VARIOS"
}
