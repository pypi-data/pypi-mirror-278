# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
tests for CLI script
"""

import json
import yaml

import pytest


from ..utils import cmd
from .. import aeb43


def write_batch(batch: aeb43.Batch, tmp_path_factory, name: str):
    "write batch to file"
    fname = tmp_path_factory.mktemp("csb43") / f"{name}.csb"
    with open(fname, "wb") as stream:
        stream.write(batch.dump())
    return fname

@pytest.fixture(name="doc1", scope="session")
def fixture_doc1(aeb43sample1, tmp_path_factory):
    "doc1"
    return write_batch(aeb43sample1, tmp_path_factory, "doc1"), True


@pytest.fixture(name="doc2", scope="session")
def fixture_doc2(bytes_sample, tmp_path_factory):
    "doc2"
    return write_batch(bytes_sample, tmp_path_factory, "doc2"), False


@pytest.fixture(name="parser")
def fixture_parser():
    "return command line argument parser"
    return cmd.get_parser()


def check_convert_to_json(parser, doc, tmp_path):
    "check cmd with json"
    finput, strict = doc
    output = tmp_path / "output"
    args = []
    if strict:
        args += ["--strict"]
    args += ["-f", "json", str(finput), str(output)]
    cmd.convert(parser.parse_args(args))
    with open(output, encoding="utf-8") as stream:
        json.load(stream)


def test_convert_to_json1(parser, doc1, tmp_path):
    "test cli script with json"
    check_convert_to_json(parser, doc1, tmp_path)


def test_convert_to_json2(parser, doc2, tmp_path):
    "test cli script with json"
    check_convert_to_json(parser, doc2, tmp_path)


def check_convert_to_yaml(parser, doc, tmp_path):
    "check cmd with yaml"
    finput, strict = doc
    output = tmp_path / "output"
    args = []
    if strict:
        args += ["--strict"]
    args += ["-f", "json", str(finput), str(output)]
    cmd.convert(parser.parse_args(args))
    with open(output, encoding="utf-8") as stream:
        yaml.safe_load(stream)


def test_convert_to_yaml1(parser, doc1, tmp_path):
    "test cli script with yaml"
    check_convert_to_yaml(parser, doc1, tmp_path)


def test_convert_to_yaml2(parser, doc2, tmp_path):
    "test cli script with yaml"
    check_convert_to_yaml(parser, doc2, tmp_path)


@pytest.fixture(name="format_", params=[
    "homebank",
    "csv",
    "tsv",
    "xlsx",
    "xls",
    "ods",
])
def fixture_format(request):
    "an output format"
    return request.param


def check_convert_to_format(parser, doc, tmp_path, format_):
    "check format conversion"
    finput, strict = doc
    output = tmp_path / "output"
    args = []
    if strict:
        args += ["--strict"]
    args += ["-f", format_, str(finput), str(output)]
    cmd.convert(parser.parse_args(args))


def test_convert_to_format1(parser, doc1, tmp_path, format_):
    "test cli script with output formats (doc1)"
    check_convert_to_format(parser, doc1, tmp_path, format_)


def test_convert_to_format2(parser, doc2, tmp_path, format_):
    "test cli script with output formats (doc2)"
    check_convert_to_format(parser, doc2, tmp_path, format_)
