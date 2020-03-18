#!/usr/bin/env python3 -i
# Copyright 2020 Collabora, Ltd. and the Proclamation contributors
#
# SPDX-License-Identifier: Apache-2.0

from ..types import Fragment, ReferenceParser, Section

from io import StringIO


def test_ref_parse():
    parser = ReferenceParser()
    assert(parser.parse("issue.54.md").item_type == "issue")
    assert(parser.parse("issue.54.md").number == 54)

    assert(parser.parse("issue.54").item_type == "issue")
    assert(parser.parse("issue.54").number == 54)

    assert(parser.parse("issue.54").as_tuple() ==
           parser.parse("issue.54.md").as_tuple())

    assert(parser.parse(".gitignore") is None)
    assert(parser.parse(".git-keep") is None)


def test_ref_parse_filename():
    parser = ReferenceParser()
    assert(parser.parse_filename("issue.54.md").item_type == "issue")
    assert(parser.parse_filename("issue.54.md").number == 54)
    assert(parser.parse_filename("issue.54") is None)
    assert(parser.parse_filename(".gitignore") is None)
    assert(parser.parse_filename(".git-keep") is None)


FRAGMENT = """---
- issue.55
- mr.23
pr.25
issue.54
---
This is content.
"""


def test_fragment():
    fn = "issue.54.md"
    fragmentio = StringIO(FRAGMENT)
    fragment = Fragment(fn, io=fragmentio)
    assert(str(fragment.filename) == fn)
    assert(len(fragment.refs) == 1)
    fragment.parse_file()
    assert("content" in fragment.text)
    assert("---" not in fragment.text)

    # duplicates don't get added
    assert(len(fragment.refs) == 4)


FRAGMENT_ERROR = """---
- issue.55
- mr.23
pr.25
issue.54
err
---
This is content.
"""


def test_fragment_with_error():
    fn = "issue.54.md"
    fragmentio = StringIO(FRAGMENT_ERROR)
    fragment = Fragment(fn, io=fragmentio)
    try:
        fragment.parse_file()
    except RuntimeError as e:
        assert("Could not parse line" in str(e))
        return
    assert(False)  # We expect an error.


SIMPLE_FRAGMENT = """This is a simple fragment content.
"""


def test_simple_fragment():
    fn = "issue.54.md"
    fragmentio = StringIO(SIMPLE_FRAGMENT)
    fragment = Fragment(fn, io=fragmentio)
    assert(str(fragment.filename) == fn)
    assert(len(fragment.refs) == 1)
    fragment.parse_file()
    assert(len(fragment.refs) == 1)
    assert("content" in fragment.text)


FRAGMENT_WITH_COMMENTS = """---
# comment
- issue.55
- mr.23
   # comment
pr.25
# comment
---
This is content.
"""


def test_fragment_with_comment():
    fn = "issue.54.md"
    fragmentio = StringIO(FRAGMENT_WITH_COMMENTS)
    fragment = Fragment(fn, io=fragmentio)
    assert(str(fragment.filename) == fn)
    assert(len(fragment.refs) == 1)
    fragment.parse_file()
    # skips comments
    assert(len(fragment.refs) == 4)
    assert("---" not in fragment.text)
    assert("comment" not in fragment.text)
    print(fragment.refs)


def test_fragment_sorting():
    section = Section("MySection")

    frag_b = Fragment("issue.2.md")
    section.add_fragment(frag_b)
    assert(section.fragments[0] == frag_b)

    frag_a = Fragment("issue.1.md")
    section.add_fragment(frag_a)
    assert(section.fragments[0] == frag_a)
    assert(section.fragments[1] == frag_b)

    frag_c = Fragment("issue.2.2.md")
    section.add_fragment(frag_c)
    assert(section.fragments[0] == frag_a)
    assert(section.fragments[1] == frag_b)
    assert(section.fragments[2] == frag_c)
