#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations

import pytest

from ..aeb43.record.context import (
    Aeb43Context,
    get_current_context,
    CONTEXT,
    InformationMode,
)
from ..aeb43.record.errors import (
    ValidationException,
    ValidationWarning,
)


@pytest.fixture(name="information_mode", scope="session", params=[
    InformationMode.FIRST,
    InformationMode.SECOND,
    InformationMode.THIRD,
], ids=lambda x: f"information_mode={x}")
def fixture_information_mode(request) -> InformationMode:
    "information mode"
    return request.param


@pytest.fixture(
    name="cache_fields", scope="session",
    params=[True, False], ids=lambda x: f"cache_fields={x}"
)
def fixture_cache_fields(request) -> bool:
    "use_cache"
    return request.param


@pytest.fixture(
    name="sepa_mode", scope="session",
    params=[True, False], ids=lambda x: f"sepa_mode={x}"
)
def fixture_sepa_mode(request) -> bool:
    "sepa"
    return request.param


@pytest.fixture(
    name="strict", scope="session",
    params=[True, False], ids=lambda x: f"strict={x}"
)
def fixture_strict(request) -> bool:
    "strict"
    return request.param


@pytest.fixture(name="global_context", scope="session")
def fixture_global_context() -> Aeb43Context:
    "default context"
    return get_current_context()


@pytest.fixture(name="strict_context", scope="session")
def fixture_strict_context(
    information_mode: InformationMode,
    cache_fields: bool,
    sepa_mode: bool
) -> Aeb43Context:
    "a strict context"
    return Aeb43Context(
        strict=True,
        information_mode=information_mode,
        cache_fields=cache_fields,
        sepa=sepa_mode
    )


@pytest.fixture(name="non_strict_context", scope="session")
def fixture_non_strict_context(
    information_mode: InformationMode,
    cache_fields: bool,
    sepa_mode: bool
) -> Aeb43Context:
    "a non strict context"
    return Aeb43Context(
        strict=False,
        information_mode=information_mode,
        cache_fields=cache_fields,
        sepa=sepa_mode
    )


@pytest.fixture(name="mode1_context", scope="session")
def fixture_mode1_context(
    strict: bool,
    cache_fields: bool,
    sepa_mode: bool
) -> Aeb43Context:
    "a non strict context"
    return Aeb43Context(
        strict=strict,
        information_mode=InformationMode.FIRST,
        cache_fields=cache_fields,
        sepa=sepa_mode
    )


@pytest.fixture(name="mode2_context", scope="session")
def fixture_mode2_context(
    strict: bool,
    cache_fields: bool,
    sepa_mode: bool
) -> Aeb43Context:
    "a non strict context"
    return Aeb43Context(
        strict=strict,
        information_mode=InformationMode.SECOND,
        cache_fields=cache_fields,
        sepa=sepa_mode
    )


@pytest.fixture(name="mode3_context", scope="session")
def fixture_mode3_context(
    strict: bool,
    cache_fields: bool,
    sepa_mode: bool
) -> Aeb43Context:
    "a non strict context"
    return Aeb43Context(
        strict=strict,
        information_mode=InformationMode.THIRD,
        cache_fields=cache_fields,
        sepa=sepa_mode
    )


@pytest.fixture(name="context", scope="session")
def fixture_context(
    strict: bool,
    information_mode: InformationMode,
    cache_fields: bool,
    sepa_mode: bool
) -> Aeb43Context:
    "a context"
    return Aeb43Context(
        strict=strict,
        information_mode=information_mode,
        cache_fields=cache_fields,
        sepa=sepa_mode
    )


def test_emit_error(strict_context: Aeb43Context):
    "check if strict context raises an exception"
    with pytest.raises(ValidationException):
        strict_context.emit_validation_error("test")


def test_error_emits_warning(non_strict_context: Aeb43Context):
    "check if non strict context emits a warning"
    with pytest.warns(ValidationWarning):
        non_strict_context.emit_validation_error("test")


def test_scope(context: Aeb43Context, global_context):
    "test context scope"
    with context.scope():
        assert CONTEXT.get() is context
    assert CONTEXT.get() is global_context
