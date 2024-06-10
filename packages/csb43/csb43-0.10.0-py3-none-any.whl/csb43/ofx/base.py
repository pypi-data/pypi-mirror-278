#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""
Base tools from building OFX structures
"""
from __future__ import annotations
from typing import Callable, Any
from datetime import datetime, date
import dataclasses
from xml.sax.saxutils import escape

from deprecated.sphinx import deprecated


DATEFORMAT = "%Y%m%d"  # short date OFX format


def xml_element(name: str, content: Any | None) -> str:
    '''
    Build a *name* XML element with *content* as body.

    Args:
        name    -- tag name
        content -- content of the node
    Return:
        (str) <NAME>content</NAME>

    >>> xml_element("hello", 12)
    '<HELLO>12</HELLO>'
    '''
    if name and (content is not None):
        return "<{tag}>{body}</{tag}>".format(tag=name.upper(), body=content)
    return ""


def xml_aggregate(*args, **kwargs) -> str:
    '''
    Build a *name* XML aggregate with *content* as body.

    Args:
        name    -- tag name
        content -- content of the node
    Return:
        (str) <NAME>content</NAME>

    >>> xml_aggregate("hello", 12)
    '<HELLO>12</HELLO>'
    '''
    return xml_element(*args, **kwargs)


def sgml_element(name: str, content: Any | None) -> str:
    '''
    Build a *name* SGML element with *content* as body.

    Args:
        name    -- tag name
        content -- content of the node
    Return:
        (str) <NAME>content

    >>> sgml_element("hello", 12)
    '<HELLO>12'
    '''
    if name and (content is not None):
        return f"<{name.upper()}>{content}"
    return ""


def sgml_aggregate(name: str, content: Any | None) -> str:
    '''
    Build a *name* SGML aggregate with *content* as body.

    Args:
        name    -- tag name
        content -- content of the node
    Return:
        (str) <NAME>content</NAME>

    >>> sgml_aggregate("hello", 12)
    '<HELLO>12</HELLO>'
    '''
    if name and (content is not None):
        return "<{tag}>{body}</{tag}>".format(tag=name.upper(), body=content)
    return ""


def date_to_str(field: datetime | date | None) -> str | None:
    '''
    Format a date as specified by OFX

    Args:
        field (datetime)
    Return:
        (str)
    '''
    return field.strftime(DATEFORMAT) if field else None


def bool_to_str(field: bool | None) -> str | None:
    '''
    Format a boolean as specified by OFX

    Args:
        field (bool)
    Return:
        (str)
    '''
    if field is not None:
        return "Y" if field else "N"
    return None


def currency_to_str(field) -> str | None:
    '''
    Format a ISO-4217 currency entity as specified by OFX

    Args:
        field (pycountry.Currency)
    Return:
        (str)
    '''
    if field is not None:
        # ISO-4217
        return field.alpha_3
    return None


def text_to_str(field: str | None) -> str | None:
    '''
    Format a string as specified by OFX, that is, characters '&', '>' and '<'
    are XML escaped.
    '''
    if field is not None:
        return escape(f"{field}")
    return None


@dataclasses.dataclass
class OfxObject:
    """
    OFX object

    Attributes:
        tag_name (str)
            name for the XML tag
        sgml (bool)
            convert to SGML instead of XML
    """
    tag_name: str = "tag"
    sgml: bool = False
    _elem_f: Callable[[str, Any | None], str] = xml_element
    _aggr_f: Callable[[str, Any | None], str] = xml_aggregate

    def __post_init__(self):
        if self.sgml:
            self._elem_f = sgml_element
            self._aggr_f = sgml_aggregate

    def _get_content(self) -> str:
        '''
        :rtype: the xml representation of this object
        '''
        return ""

    @deprecated(version="0.10.0", reason="use attribute `sgml`")
    def is_sgml(self) -> bool:
        "return True if SGML mode is on"
        return self.sgml

    @deprecated(version="0.10.0", reason="use attribute `tag_name`")
    def get_tag_name(self) -> str:
        '''
        :rtype: the XML tag name
        '''
        return self.tag_name

    @deprecated(version="0.10.0", reason="use attribute `tag_name`")
    def set_tag_name(self, name: str):
        '''
        Set a XML tag name for this object

        :param name: name for the XML tag
        :type name: :class:`str`
        '''
        self.tag_name = name

    def __str__(self) -> str:
        '''
        :rtype: XML representation of the object
        '''
        # return xml_element(self._tag_name, self._get_content())
        return self._get_content()
