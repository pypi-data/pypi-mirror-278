#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Descriptor field for Currency type representation
"""
from __future__ import annotations
from typing import (
    Any,
    Iterator,
    Union,
    Callable,
)
import dataclasses
from numbers import Number

from ..record import (
    FieldValue,
    Record,
    RegexValidator,
)
from . import (
    Field,
    as_string,
)
from ...utils.currency import (
    AnyCurrency,
    CurrencyLite,
    currency_from_iso_number,
    currency_from_iso_code,
    is_currency,
)
from ...utils import messages as msg


def euro_currency():
    "return euro currency"
    # EURO
    return currency_from_iso_number("978")


@dataclasses.dataclass(frozen=True)
class Currency(Field[AnyCurrency, Union[str, Number, AnyCurrency]]):
    "currency code"
    field_id: Any
    factory: Callable[[], AnyCurrency] = euro_currency

    def default_factory(self) -> AnyCurrency:
        return self.factory()

    def adapt(self, this: Record, value: str | Number | AnyCurrency) -> AnyCurrency:
        if is_currency(value):
            assert not isinstance(value, (str, Number))
            return value

        if isinstance(value, Number):
            val = f"{value:03d}"
        else:
            val = this.get_context().to_string(value).upper()
        out = currency_from_iso_code(val)
        if out is None:
            raise this.get_context().new_validation_error(
                msg.T_CURRENCY_EXPECTED.format(obj=value)
            )
        return out

    def to_bytes(self, this: Record, value: str | Number | AnyCurrency) -> Iterator[FieldValue]:
        assert not isinstance(value, (str, Number))
        if value.numeric is None:
            raise this.get_context().new_validation_error(
                msg.T_CURRENCY_EXPECTED.format(obj=value)
            )
        yield FieldValue(
            self.field_id,
            value.numeric.encode(this.get_context().encoding)
        )

    def to_field(self, this: Record) -> AnyCurrency:
        value = as_string(this, self.field_id)
        currency = currency_from_iso_number(value)
        if not currency:
            currency = CurrencyLite(alpha_3=None, numeric=value)
        return currency


def currency_validator(warning=False) -> RegexValidator:
    "validator for currency numeric code"
    return RegexValidator(pattern=br"^\d{3}$", warning=warning)
