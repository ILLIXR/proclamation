#!/usr/bin/env python3 -i
# Copyright 2020 Collabora, Ltd.
#
# SPDX-License-Identifier: Apache-2.0

from ..render import split_news_contents, get_split_news_file
from ..settings import ProjectSettings

NEWS_FILE_1 = """# Sample NEWS file

## Previous

## More previous

"""


def test_split_news():
    proj_settings = ProjectSettings("Test")
    before, after = split_news_contents(proj_settings, NEWS_FILE_1)
    assert("Sample" in before)
    assert("Previous" in after)
    assert(after.startswith("##"))


def test_missing_news_file():
    proj_settings = ProjectSettings("Test", news_filename="nonexistent-file")
    before, after = get_split_news_file(proj_settings)
    assert(after == "")
    assert(before.endswith("\n"))
