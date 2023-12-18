#!/usr/bin/env python3 -i
# Copyright 2020-2023 Collabora, Ltd. and the Proclamation contributors
#
# SPDX-License-Identifier: Apache-2.0
#
# Original author: Rylie Pavlik <rylie.pavlik@collabora.com>

import logging
from pathlib import Path
from typing import List, Optional, Set, Tuple

from .utils import remove_files
from .types import Fragment, Reference, ReferenceParser

_LOG = logging.getLogger(__name__)


class MegaFragment:
    """
    Accumulates references and bullet points to create a single file.
    """

    def __init__(self):
        self.refs: List[Reference] = []
        self.refs_set: Set[Tuple] = set()
        self.bullet_points: List[str] = []
        self._log = _LOG.getChild("MegaFragment")

    @property
    def ref(self):
        """Get the first reference used for a fragment, which becomes an ID."""
        return self.refs[0]

    def add_fragment(self, fragment: Fragment):
        """
        Accumulate a single fragment.
        """
        self._log.info("Adding text: %s", fragment.text)
        self.bullet_points.append(fragment.text)
        for ref in fragment.refs:
            if ref.as_tuple() not in self.refs_set:
                self._log.info("Adding reference: %s", repr(ref))
                self.refs.append(ref)
                self.refs_set.add(ref.as_tuple())

    def add_file(self, filename: Path, ref_parser: ReferenceParser):
        """Accumulate all fragments defined by a file."""
        fragment_ref = ref_parser.parse(filename.name)
        if not fragment_ref:
            # Actually not a fragment?
            self._log.warning("Not actually a fragment: %s", filename)
            return

        fragment = Fragment(filename, fragment_ref, ref_parser)
        extras = fragment.parse_file()
        self.add_fragment(fragment)
        for extra in extras:
            self.add_fragment(extra)

    def export(self, ref_parser: ReferenceParser) -> str:
        """
        Return the string contents of a file with all combined fragments.
        """
        lines = ["---"]
        for ref in self.refs:
            ref_str = ref_parser.unparse(ref)
            lines.append(f"- {ref_str}")
        lines.append("---")
        for item in self.bullet_points:
            lines.append(f"- {item.rstrip()}")
        return "\n".join(lines) + "\n"


def merge_fragments(filenames: List[Path], ref_parser: Optional[ReferenceParser]):
    """
    Merge fragments from one or more files into a single file.
    """
    if ref_parser is None:
        ref_parser = ReferenceParser()

    mega = MegaFragment()
    for fn in filenames:
        mega.add_file(fn, ref_parser)

    out_fn = filenames[0]
    remove_fns = filenames[1:]
    with open(out_fn, "w", encoding="utf-8") as fp:
        fp.write(mega.export(ref_parser))

    remove_files(remove_fns)
