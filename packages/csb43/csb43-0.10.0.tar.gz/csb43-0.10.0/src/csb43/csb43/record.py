# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

# -*- coding: utf-8 -*-
'''
@license: GNU Lesser General Public License v3.0 (see LICENSE)
'''
from typing import (
    Dict,
    Any,
    Optional,
    Union,
)

import numbers
import re
import datetime
from decimal import (
    Decimal,
    InvalidOperation,
)

from deprecated.sphinx import deprecated

from .. import utils
from ..utils import (
    messages as msg,
    currencyISOByLetter,
    currencyISO,
    isCurrency,
    b_left_pad,
    raiseCsb43Exception,
    BytesMixin,
)
from ..i18n import tr as _


@deprecated(
    version="0.10.0",
    reason="use csb43.aeb43.context.check_compatible_encoding"
)
def check_compatible_encoding(encoding: str) -> bool:
    "returns True if 'encoding' is compatible"
    return (
        (b"\x20" == " ".encode(encoding))
        and (b"\x30" == "0".encode(encoding))
    )


@deprecated(
    version="0.10.0",
    reason="use records, fields and contexts from csb43.aeb43"
)
class RecordSequence(BytesMixin):
    '''
    Generic record in a CSB43 file
    '''

    ENCODING = "latin1"
    DECIMAL = utils.DECIMAL

    CUR_NUM = re.compile(r'^\d{3}$')
    CUR_LET = re.compile(r'^[a-zA-Z]{3}$')

    def __init__(
        self,
        strict=True,
        decimal=utils.DECIMAL,
        yearFirst=True,
        encoding=ENCODING,
        silent=False,
        file_context=None,
    ):
        '''
        Constructor
        '''
        if not check_compatible_encoding(encoding):
            raiseCsb43Exception(
                _("Encoding %s is not compatible with the AEB43 field padding character.") % repr(encoding),
                strict=strict,
                silent=silent
            )

        self._s_decimal = decimal
        self._s_year_first = yearFirst
        self._s_encoding = encoding
        self._file_context = file_context
        self.__strict = strict
        self.__silent = silent

    def _settings(self) -> Dict[str, Any]:
        return {
            "decimal": self._s_decimal,
            "yearFirst": self._s_year_first,
            "encoding": self._s_encoding,
            "file_context": self._file_context,
            "strict": self.strict_mode,
            "silent": self.silent_mode,
        }

    def _get_file_line(self) -> int:
        return self._file_context.line if self._file_context else None

    @property
    def str_encoding(self) -> str:
        return self._s_encoding

    def set_decimal_precision(self, decimal: int):
        self._s_decimal = decimal

    def set_year_first(self, yearFirst=True):
        self._s_year_first = yearFirst

    @property
    def strict_mode(self) -> bool:
        return self.__strict

    @property
    def silent_mode(self) -> bool:
        return not self.__strict and self.__silent

    def _get_check_args(self) -> Dict[str, Any]:
        return {
            "strict": self.strict_mode,
            "silent": self.silent_mode,
            "line": self._get_file_line(),
        }

    def _format_date(self, value: str) -> datetime.date:
        '''
        Args:
            value (str) -- CSB date
        Return:
            (datetime.date)  -- date object
        '''
        return utils.raw2date(value, self._s_year_first)

    def _unformat_date(self, value: datetime.date) -> str:
        '''
        Args:
            value (datetime.date) -- date object
        Return:
            (str)            -- CSB date
        '''
        return utils.date2raw(value, self._s_year_first)

    def _format_currency(self, value: str, debit=b'2') -> Decimal:
        '''
        Args:
            value (str)     -- CSB raw amount
            debit (r'[12]') -- flag to indicate credit or debit
        Return:
            (int)           -- formatted numeric amount
        '''
        return utils.raw2currency(value, self._s_decimal, debit)

    def _unformat_currency(self, value: Decimal):
        '''
        Args:
            value (int) -- amount
        Return:
            pair (raw amount), (debit [2] or credit [1])
        '''
        return utils.currency2raw(value, self._s_decimal)

    def str_encode(
        self,
        value: Optional[Union[str, bytes]],
        valnone=b'',
        **kwargs
    ) -> bytes:
        if value is None:
            return valnone
        if isinstance(value, str):
            value = value.encode(self._s_encoding)
        elif not isinstance(value, bytes):
            value = bytes(value)
        return value

    def str_decode(
        self,
        value: Optional[Union[str, bytes]]
    ) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, str):
            return value
        return value.decode(self._s_encoding)

    def _to_decimal(self, value) -> Decimal:
        if isinstance(value, Decimal):
            return value
        elif isinstance(value, bytes):
            value = value.decode(self._s_encoding)

        try:
            return Decimal(value)
        except InvalidOperation as exc:
            raise ValueError(value) from exc

    def _text2field(self, value, **kwargs) -> bytes:
        if value and not isinstance(value, (str, bytes)):
            value = str(value)

        return self.str_encode(value, **kwargs)

    def _enc_left_pad(self, value, **kwargs) -> bytes:
        out = self._text2field(value, **kwargs)
        if isinstance(value, numbers.Number):
            return b_left_pad(out, **kwargs)
        return out

    def __unicode__(self) -> str:
        out = self.str_decode(self.__bytes__())
        if out is None:
            raise ValueError()
        return out

    def _parse_currency_code(self, value):
        out = None
        try:
            if isCurrency(value):
                out = value.numeric
            else:
                if isinstance(value, numbers.Number):
                    val = "%03d" % value
                else:
                    val = self.str_decode(self.str_encode(value))
                obj = None
                if self.CUR_NUM.match(val):
                    obj = currencyISO(val)
                    if not obj:
                        raise KeyError(val)
                elif self.CUR_LET.match(val):
                    obj = currencyISOByLetter(val.upper())
                    if not obj:
                        raise KeyError(val)
                else:
                    raiseCsb43Exception(
                        msg.T_CURRENCY_EXPECTED.format(obj=val),
                        strict=True
                    )
                if obj:
                    out = obj.numeric
        except KeyError:
            raiseCsb43Exception(msg.T_CURRENCY_EXPECTED.format(obj=value), strict=True)

        if out is not None:
            return self.str_encode(out)
        return out

    def _raise_error(self, message):
        args = self._get_check_args()
        raiseCsb43Exception(message, **args)
