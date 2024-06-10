#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Context object for reading AEB43 records
"""

from __future__ import annotations
from typing import Protocol
import dataclasses
import enum
from contextvars import (
    ContextVar,
#    Token,
)
import contextlib
from . import errors

from ...i18n import tr as _


def check_compatible_encoding(encoding: str) -> bool:
    "returns True if 'encoding' is compatible with n43 records"
    return (
        (b"\x20" == " ".encode(encoding))
        and (b"\x30" == "0".encode(encoding))
    )


class InformationMode(enum.IntEnum):
    """information mode

    [es] modalidad de información

    See [n43_2012]_ Appendix 1
    """
    FIRST = 1
    SECOND = 2
    THIRD = 3


@dataclasses.dataclass
class BatchContext:
    """
    line context
    """
    line: int | None = None

    @contextlib.contextmanager
    def scope(self):
        "create a scope for this context"
        token = BATCH_CONTEXT.set(self)
        yield self
        BATCH_CONTEXT.reset(token)


BATCH_CONTEXT: ContextVar["BatchContext" | None] = ContextVar(
    "BATCH_CONTEXT", default=BatchContext()
)


def get_batch_context() -> BatchContext:
    "get the context for the current scope"
    context = BATCH_CONTEXT.get()
    if not context:
        raise ValueError("no context found")
    return context


@dataclasses.dataclass(frozen=True)
class Aeb43Context:
    """
    settings for encoded AEB43 records

    Fields
    ------
    strict : bool
        raise exception when a validation fails if `strict=True`
    silent : bool
        if `silent=True`, validation warnings are not emitted
    encoding : str
        string encoding use when transforming from binary files
    sepa : bool
        when `sepa=True`, transactions trie to interpret optional items
        as SEPA transfer or direct debits
    cache_fields : bool
        cache values from setters/getters
    decimal : int
        number of decimal places used in money amounts
    information_mode : InformationMode
        information mode to use in nested records. Accounts will change this value.
    """
    strict: bool = False
    silent: bool = False
    encoding: str = "latin1"
    sepa: bool = True
    year_first: bool = True
    cache_fields: bool = True
    decimals: int = 2
    information_mode: InformationMode = InformationMode.THIRD

    def __post_init__(self):
        if not check_compatible_encoding(self.encoding):
            self.emit_validation_error(
                _(
                    "Encoding {encoding} is not compatible with "
                    "the AEB43 field padding character."
                ).format(encoding=self.encoding)
            )

    def error_message(self, message: str) -> str:
        "get a new error message in a batch context"
        return errors.message_error(message, line=get_batch_context().line)

    def emit_validation_error(self, message: str) -> None:
        """raise ValidationException if strict or emits
        a ValidationWarning if not strict and not silent"""
        errors.raise_validation_exception(
            message, strict=self.strict, silent=self.silent, line=get_batch_context().line
        )

    def emit_validation_warning(self, message: str) -> None:
        "emit a warning"
        errors.raise_validation_exception(
            message, strict=False, silent=self.silent, line=get_batch_context().line
        )

    def new_validation_error(self, message: str) -> errors.ValidationException:
        """create a new validation error with `message`

        Context line is added to the Exception
        """
        return errors.ValidationException(message, line=get_batch_context().line)

    def to_string(self, value) -> str:
        "convert value to string"
        if value is None:
            return ""
        if isinstance(value, (bytes, bytearray)):
            return value.decode(self.encoding)
        return str(value)

    @contextlib.contextmanager
    def scope(self, **kwargs):
        "create a scope for this context"
        if kwargs:
            instance = dataclasses.replace(self, **kwargs)
        else:
            instance = self
        token = CONTEXT.set(instance)
        yield instance
        CONTEXT.reset(token)


# Global ContextVar object for Aeb43Context
CONTEXT: ContextVar["Aeb43Context" | None] = ContextVar("CONTEXT", default=Aeb43Context())


def get_current_context() -> Aeb43Context:
    "get the context for the current scope"
    context = CONTEXT.get()
    if not context:
        raise ValueError("no context found")
    return context


# pylint: disable=too-few-public-methods
class Contextual(Protocol):
    "protocol for any class that has a context property"
    context: Aeb43Context | None

    def get_context(self) -> Aeb43Context: ...


class ContextualMixin:
    "provides a method that always returns a context"
    context: Aeb43Context | None

    def get_context(self) -> Aeb43Context:
        "get the context for the current scope"
        return self.context or get_current_context()
