#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""
test OFX data 
"""

from __future__ import annotations

import os
from pathlib import Path
from lxml import etree
import pytest

from .. import aeb43
from ..ofx import converter as ofx


@pytest.fixture(name="ofx_schema_path", scope="session")
def fixture_ofx_schema_path() -> Path | None:
    "find XSD for OFX2"
    filename = "OFX2_Protocol.xsd"
    paths: list[Path] = [
        Path(__file__).parent / "schemas" / filename,
        Path(".ofx_schemas") / filename,
        Path(os.environ.get("OFX_SCHEMA_PATH", "")) / filename,
    ]
    valid_paths = [p for p in paths if p.is_file()]

    return valid_paths[0] if valid_paths else None


@pytest.fixture(name="ofx_doc1")
def fixture_ofx_doc1(aeb43sample1: aeb43.Batch) -> str:
    "convert to ofx"
    return str(ofx.convert_from_aeb43(aeb43sample1))


@pytest.fixture(name="ofx_doc2")
def fixture_odx_doc2(bytes_sample: aeb43.Batch) -> str:
    "convert to ofx"
    return str(ofx.convert_from_aeb43(bytes_sample))


def check_unique_fitid(doc: str):
    "check fitid for a OFX document"
    xml = etree.fromstring(doc.encode("UTF-8"))
    fitid = [node.text for node in xml.xpath("//STMTTRN/FITID")]
    assert len(fitid) == len(set(fitid)), "all FITID content must be unique within an OFX file"


def test_unique_fitid1(ofx_doc1: str):
    """
    fitid field has a unique constraint
    """
    check_unique_fitid(ofx_doc1)


def test_unique_fitid2(ofx_doc2: str):
    """
    fitid field has a unique constraint
    """
    check_unique_fitid(ofx_doc2)


def check_v211_xsd_validation(ofx_schema_path: Path | None, doc: str):
    """
    XSD
    """
    if not ofx_schema_path:
        pytest.skip("OFX 2.1.1 Schema not found")

    xsd = etree.XMLSchema(file=ofx_schema_path)

    doc = (
        doc.replace(
            "<OFX>",
            '<ofx:OFX xmlns:ofx="http://ofx.net/types/2003/04">'
        ).replace("</OFX>", "</ofx:OFX>")
    )

    root = etree.fromstring(doc.encode("UTF-8"))

    xsd.assert_(root)


def test_v211_xsd_validation1(ofx_schema_path: Path | None, ofx_doc1: str):
    """
    XSD
    """
    check_v211_xsd_validation(ofx_schema_path, ofx_doc1)


def test_v211_xsd_validation2(ofx_schema_path: Path | None, ofx_doc2: str):
    """
    XSD
    """
    check_v211_xsd_validation(ofx_schema_path, ofx_doc2)
