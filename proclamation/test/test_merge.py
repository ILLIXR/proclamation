#!/usr/bin/env python3 -i
# Copyright 2020-2023, Collabora, Ltd. and the Proclamation contributors
#
# SPDX-License-Identifier: Apache-2.0
#
# Original author: Rylie Pavlik <rylie.pavlik@collabora.com>

from io import StringIO

from ..types import Fragment
from ..merge import MegaFragment

FRAGMENT = """---
- issue.55
- mr.23
pr.25
issue.54
---
This is content.
"""


def _make_fragment():
    fn = "issue.54.md"
    fragment = Fragment(fn, io=StringIO(FRAGMENT))
    extras = fragment.parse_file()
    assert not extras
    return fragment


SIMPLE_FRAGMENT = """This is a simple fragment content.
"""


def _make_simple_fragment():
    fn = "issue.54.md"
    fragment = Fragment(fn, io=StringIO(SIMPLE_FRAGMENT))
    extras = fragment.parse_file()
    assert not extras
    return fragment


def test_merge():
    mega = MegaFragment()
    assert len(mega.bullet_points) == 0

    frag = _make_fragment()
    mega.add_fragment(frag)
    assert len(mega.bullet_points) == 1
    assert mega.bullet_points[0]
    assert len(mega.refs) == 4

    simple_frag = _make_simple_fragment()

    mega.add_fragment(simple_frag)
    assert len(mega.bullet_points) == 2
    assert mega.bullet_points[0]
    assert mega.bullet_points[1]
    assert len(mega.refs) == 4
