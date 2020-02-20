#!/usr/bin/env python3 -i
# Copyright 2020 Collabora, Ltd.
#
# SPDX-License-Identifier: Apache-2.0

from ..types import Chunk, ReferenceFactoryBase

from io import StringIO


def test_parse_refs():
    factory = ReferenceFactoryBase()
    assert(factory.parse("issue.54.md").item_type == "issue")
    assert(factory.parse("issue.54.md").number == 54)

    assert(factory.parse("issue.54").item_type == "issue")
    assert(factory.parse("issue.54").number == 54)

    assert(factory.parse("issue.54").as_tuple() ==
           factory.parse("issue.54.md").as_tuple())


CHUNK = """---
- issue.55
- mr.23
pr.25
issue.54
---
This is content.
"""


def test_chunk():
    factory = ReferenceFactoryBase()
    fn = "issue.54.md"
    chunkio = StringIO(CHUNK)
    ref = factory.parse(fn)
    chunk = Chunk(fn, ref, ref_factory=factory, io=chunkio)
    assert(chunk.filename == fn)
    assert(len(chunk.refs) == 1)
    chunk.parse_file()
    assert("content" in chunk.text)

    # duplicates don't get added
    assert(len(chunk.refs) == 4)
