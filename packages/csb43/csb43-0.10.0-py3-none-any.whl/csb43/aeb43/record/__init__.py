#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Base tools for building bytes chars records
"""

from __future__ import annotations
from typing import (
    Any,
    Callable,
    ClassVar,
    Generic,
    Iterable,
    Iterator,
    Mapping,
    NamedTuple,
    Pattern,
    Tuple,
    TypeVar,
    Union,
)
import dataclasses
import re

from .context import (
    Aeb43Context,
    ContextualMixin,
)
from ...i18n import tr as _
from ...utils import messages as msg
from ... import utils


AnyBytes = Union[bytes, bytearray]
AnyStr = TypeVar("AnyStr", bytes, str)
TValidator = Callable[[Aeb43Context, AnyBytes], Tuple[Union[str, None], Union[str, None]]]


def create_bytes_record(manifest: "RecordManifest") -> bytes:
    "create a default bytes record"
    return manifest.code + b" " * (manifest.size - len(manifest.code))


TRecordCreator = Callable[["RecordManifest"], bytes]


@dataclasses.dataclass
class RecordManifest:
    "a record configuration"
    code: bytes
    sections: Mapping[Any, tuple[slice, TValidator | None]]
    size: int = 80
    default_factory: TRecordCreator = dataclasses.field(
        default=create_bytes_record
    )

    def create_record(self) -> AnyBytes:
        "create a default record"
        return self.default_factory(self)

    def validate_size(self, record: AnyBytes) -> bool:
        "validate record size"
        return len(record) == self.size

    def validate_code(self, record: AnyBytes) -> bool:
        "validate record code"
        return record.startswith(self.code)

    def validator_for(self, field_id) -> TValidator | None:
        "get validator for a field identified by `field_id`"
        return self.sections[field_id][1]

    def slice_for(self, field_id) -> slice:
        "get slice for a field idenfified by `field_id`"
        return self.sections[field_id][0]

    def size_for(self, field_id) -> int:
        "get size for a field identified by `field_id`"
        offset = self.slice_for(field_id)
        return offset.stop - offset.start


class FieldValue(NamedTuple):
    "an identified field value"
    field_id: Any
    value: bytes


class BytesMixin:
    "implements required methods for a bytes record"

    _raw: AnyBytes

    def __bytes__(self) -> bytes:
        return bytes(self._raw)

    def accepts_nested_codes(self, record: bytes) -> bool:
        "return True if the record accepts this nested `record`"
        raise NotImplementedError()


class SingleRecordMixin(BytesMixin):
    "implements required methods for a bytes record that contains no other records"

    def __iter__(self) -> Iterator[bytes]:
        yield bytes(self)

    def accepts_nested_codes(self, record: bytes) -> bool:
        return False


class CompositeRecordMixin(BytesMixin):
    "implements required methods for composite bytes records"

    def append(self, raw: AnyBytes):
        "append a bytes record to the collection of dependent records"
        raise NotImplementedError()


@dataclasses.dataclass
class Record(ContextualMixin):
    "an AEB43 record"
    manifest: ClassVar[RecordManifest]
    context: Aeb43Context | None = None
    _raw: AnyBytes = dataclasses.field(repr=False, init=False)
    raw: dataclasses.InitVar[AnyBytes | None] = None

    def _create_record(self) -> tuple[AnyBytes, list[FieldValue]]:
        raw: AnyBytes | None = self.manifest.create_record()
        changes = []
        for _key, __, variable in self._iter_fields():
            # default value
            value = variable.default_factory()
            changes.extend(variable.to_bytes(self, value))
        # apply changes from default factories
        raw = self.update_fields(*changes, raw=raw)
        if raw is None:
            raise ValueError()
        return raw, changes

    def _accepted_fields(self, changes: Iterable[FieldValue]):
        pass

    def __post_init__(self, raw):
        if not self.context:
            self.context = self.get_context()
        if raw is None:
            self._raw, changes = self._create_record()
        else:
            changes = self.from_raw(raw)
        self._accepted_fields(changes)

    def __bytes__(self) -> bytes:
        raise NotImplementedError()

    def from_raw(self, raw: AnyBytes) -> list[FieldValue]:
        "set a new record"
        self._check_code(raw)
        self._check_size(raw)
        # validate fields
        changes = []
        for field_id, (offset, validator) in self.manifest.sections.items():
            field = raw[offset]
            self._validate_field(field_id, field, validator)
            changes.append(FieldValue(field_id, field))
        self._raw = raw
        return changes

    def get_field(self, field_id) -> AnyBytes:
        "get raw field"
        return self._raw[self.manifest.slice_for(field_id)]

    def _check_code(self, record: AnyBytes):
        if not self.manifest.validate_code(record):
            raise self.get_context().new_validation_error(msg.BAD_RECORD(record))

    def __iter__(self) -> Iterator[bytes]:
        raise NotImplementedError()

    def _iter_fields(self) -> Iterator[tuple[str, str, Any]]:
        variables = vars(type(self))
        for field in dataclasses.fields(type(self)):
            key = field.name
            if key.startswith("_"):
                continue
            if key not in variables:
                continue
            variable = variables[key]
            if not hasattr(variable, "default_factory") or not hasattr(variable, "to_bytes"):
                continue
            i18n = field.metadata.get("i18n", key)
            yield key, i18n, variable

    def _iter_value_fields(self, translated=True) -> Iterator[tuple[str, Any]]:
        if translated:
            fields = ((i18n, getattr(self, key)) for key, i18n, _ in self._iter_fields())
        else:
            fields = ((key, getattr(self, key)) for key, _, _ in self._iter_fields())

        for key, value in fields:
            if utils.currency.is_currency(value):
                yield key, utils.currency.simplify_currency(value)
            else:
                yield key, value

    def to_dict(self, translated=True) -> dict[str, Any]:
        "return fields as a dict of typed values"
        return dict(self._iter_value_fields(translated))

    def _check_size(self, record: AnyBytes):
        if not self.manifest.validate_size(record):
            raise self.get_context().new_validation_error(
                _("a {size:d}-sized bytes record is required").format(size=self.manifest.size)
            )

    def _validate_field(self, field_id, field: bytes, validator: TValidator | None) -> None:
        if not validator:
            return
        error, warning = validator(self.get_context(), field)
        if error:
            raise self.get_context().new_validation_error(f"{error} {field_id}]")
        if warning:
            self.get_context().emit_validation_error(f"{warning} [{field_id}]")

    def _check_field_size(self, offset: slice, value: bytes) -> None:
        size = offset.stop - offset.start
        if size != len(value):
            raise self.get_context().new_validation_error(
                _("wrong field size: {valid_size:d} != {size:d} ({value})").format(
                    valid_size=size,
                    size=len(value),
                    value=value
                )
            )

    def _update_field(self, raw: AnyBytes, offset: slice, value: bytes) -> bytearray:
        "update a slice of the raw record"
        if not isinstance(raw, bytearray):
            raw = bytearray(raw)
        self._check_field_size(offset, value)
        raw[offset] = value
        return raw

    def update_fields(self, *changes: FieldValue, raw: AnyBytes | None = None) -> AnyBytes | None:
        "update a field identified by `field_id`"
        inplace = False
        if raw is None:
            inplace = True
            if not hasattr(self, "_raw"):
                return None
            raw = self._raw
        updates = []
        for change in changes:
            offset, validator = self.manifest.sections[change.field_id]
            self._check_field_size(offset, change.value)
            self._validate_field(change.field_id, change.value, validator)
            updates.append((offset, change.value))
        for offset, value in updates:
            raw = self._update_field(raw, offset, value)
        if inplace:
            self._raw = raw
        self._accepted_fields(changes)
        return raw


@dataclasses.dataclass
class RegexValidator(Generic[AnyStr]):
    "Validator for matching regex patterns"
    pattern: dataclasses.InitVar[AnyStr]
    search: bool = False  # use re.search insted of re.match
    warning: bool = False
    regex: Pattern[AnyStr] = dataclasses.field(init=False)

    def __post_init__(self, pattern: AnyStr):
        self.regex = re.compile(pattern)

    def __call__(self, _context, field: AnyStr) -> tuple[str | None, str | None]:
        match = self.regex.match(field) if not self.search else self.regex.search(field)
        if not match:
            message = _(
                "Bad format: content {content!r} mismatches the "
                "expected format r{pattern!r} for this field"
            ).format(content=field, pattern=self.regex.pattern)
            if self.warning:
                return None, message
            return message, None
        return None, None


def chain_validator(
    *validators: TValidator
) -> Callable[[Aeb43Context, Any], tuple[str | None, str | None]]:
    "chained validation sequence"

    def inner(context: Aeb43Context, field) -> tuple[str | None, str | None]:
        error: str | None = None
        warnings: list[str] = []
        for validator in validators:
            error, warning = validator(context, field)
            if warning:
                warnings.append(warning)
            if error:
                break
        return error, "; ".join(warnings) if warnings else None

    return inner
