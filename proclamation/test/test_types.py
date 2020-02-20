#!/usr/bin/env python3 -i
# Copyright 2020 Collabora, Ltd.
#
# SPDX-License-Identifier: Apache-2.0

from ..types import Chunk, ReferenceParser

from io import StringIO


def test_ref_parse():
    parser = ReferenceParser()
    assert(parser.parse("issue.54.md").item_type == "issue")
    assert(parser.parse("issue.54.md").number == 54)

    assert(parser.parse("issue.54").item_type == "issue")
    assert(parser.parse("issue.54").number == 54)

    assert(parser.parse("issue.54").as_tuple() ==
           parser.parse("issue.54.md").as_tuple())


CHUNK = """---
- issue.55
- mr.23
pr.25
issue.54
---
This is content.
"""


def test_chunk():
    parser = ReferenceParser()
    fn = "issue.54.md"
    chunkio = StringIO(CHUNK)
    chunk = Chunk(fn, ref_parser=parser, io=chunkio)
    assert(str(chunk.filename) == fn)
    assert(len(chunk.refs) == 1)
    chunk.parse_file()
    assert("content" in chunk.text)

    # duplicates don't get added
    assert(len(chunk.refs) == 4)
