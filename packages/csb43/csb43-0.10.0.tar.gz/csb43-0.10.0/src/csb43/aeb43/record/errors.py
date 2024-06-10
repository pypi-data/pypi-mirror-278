#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
errors and warnings
"""

from __future__ import annotations
import warnings


def message_error(value, line: int | None = None) -> str:
    "a message error for a context line"
    if line is not None:
        return f"[{line:04d}] {value}"
    return str(value)


class ValidationException(ValueError):
    "exception raised when a field does not validate"

    def __init__(self, value, line: int | None = None):
        super().__init__(message_error(value, line))


class ValidationWarning(UserWarning):
    "warning issued when a field does not validate"

    def __init__(self, value, line: int | None = None):
        super().__init__(message_error(value, line))


def raise_validation_exception(
    value,
    strict=False,
    silent=False,
    line: int | None = None,
):
    "raise an exception if `strict` is true, otherwise issue a warning"
    if strict:
        raise ValidationException(value, line)
    if not silent:
        warnings.warn(ValidationWarning(value, line))
