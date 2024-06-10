#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""
OFX BankAccount structure
"""
from __future__ import annotations
import dataclasses
from deprecated.sphinx import deprecated

from .base import (
    text_to_str,
    OfxObject,
)


#: account type
TYPE = ("CHECKING", "SAVINGS", "MONEYMRKT", "CREDITLINE")


@dataclasses.dataclass
class BankAccount(OfxObject):
    '''
    A bank account

    See [OFX]_ 11.3.1 Banking Account

    Fields
    ------
    bank_id
        `BANKID` bank identifier (Spain: banco, entidad)
    branch_id
        `BRANCHID` branch identifier (Spain: sucursal, oficina)
    id
        `ACCTID` account identifier
    type
        `ACCTTYPE` type of account.
    key
        `ACCTKEY` checksum (Spain: digitos de control)
    '''
    tag_name: str = "bankaccfrom"
    bank_id: str | None = None
    branch_id: str | None = None
    id: str | None = None
    type: str = TYPE[1]
    key: str | None = None

    def _get_content(self) -> str:
        elem = self._elem_f

        str_content = elem("bankid", text_to_str(self.bank_id))
        str_content += elem("branchid", text_to_str(self.branch_id))
        str_content += elem("acctid", text_to_str(self.id))
        str_content += elem("accttype", self.type)
        str_content += elem("acctkey", text_to_str(self.key))

        return str_content

    @deprecated(version="0.10.0", reason="use attribute `type`")
    def get_type(self) -> str:
        '''
        :rtype: :class:`str` -- type of account. See :class:`TYPE` (default \
        *'SAVINGS'*)
        '''
        if self.type is None:
            return TYPE[1]
        return self.type

    @deprecated(version="0.10.0", reason="use attribute `key`")
    def get_key(self) -> str | None:
        '''
        :rtype: :class:`str` -- checksum (Spain: digitos de control)
        '''
        return self.key

    @deprecated(version="0.10.0", reason="use attribute `type`")
    def set_type(self, value: str):
        '''
        :param value: type of account
        :type  value: :class:`str`
        '''
        self.type = value

    @deprecated(version="0.10.0", reason="use attribute `key`")
    def set_key(self, value: str):
        '''
        :param value: checksum
        '''
        self.key = value

    @deprecated(version="0.10.0", reason="use attribute `bank_id`")
    def get_bank(self) -> str | None:
        '''
        :rtype: :class:`str` -- bank identifier (Spain: banco, entidad)
        '''
        return self.bank_id

    @deprecated(version="0.10.0", reason="use attribute `branch_id`")
    def get_branch(self) -> str | None:
        '''
        :rtype: :class:`str` -- branch identifier (Spain: sucursal, oficina)
        '''
        return self.branch_id

    @deprecated(version="0.10.0", reason="use attribute `id`")
    def get_id(self) -> str | None:
        '''
        :rtype: :class:`str` -- account identifier
        '''
        return self.id

    @deprecated(version="0.10.0", reason="use attribute `bank_id`")
    def set_bank(self, value: str):
        '''
        :param value: bank identifier
        '''
        self.bank_id = value

    @deprecated(version="0.10.0", reason="use attribute `branch_id`")
    def set_branch(self, value: str):
        '''
        :param branch: branch identifier
        '''
        self.branch_id = value

    @deprecated(version="0.10.0", reason="use attribute `id`")
    def set_id(self, value: str):
        '''
        :param value: account id
        '''
        self.id = value
