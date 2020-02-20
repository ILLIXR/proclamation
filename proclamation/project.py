#!/usr/bin/env python3 -i
# Copyright 2020 Collabora, Ltd.
#
# SPDX-License-Identifier: Apache-2.0
"""Loading data for a project."""

from .types import Section, ReferenceFactoryBase
from pathlib import Path


def _resolve_with_base(base_dir, path):
    path = Path(path)
    return (base_dir / path).resolve()


class Project:
    """A project has sections and chunks."""

    def __init__(self, settings, ref_factory=None, default_base=None):
        """Construct a project.

        settings: a ProjectSettings object.
        ref_factory: optional, a reference factory if the default is not
        suitable.
        default_base: optional, default base directory. If unset, defaults to
        the current working directory.
        """
        super().__init__()
        if default_base is None:
            default_base = Path(".").resolve()
        self.default_base = default_base

        if ref_factory is None:
            ref_factory = ReferenceFactoryBase()
        self.ref_factory = ref_factory

        self.name = settings.name
        self.template = settings.template

        self.sections = []
        sections = self.sections
        for section_settings in settings.sections:
            section = Section(section_settings.name,
                              section_settings.directory)
            sections.append(section)

    def populate_sections(self, ref_factory=None):
        """Load chunks associated with each section."""
        if ref_factory is None:
            ref_factory = self.ref_factory
        for section in self.sections:
            directory = _resolve_with_base(
                self.default_base, section.relative_directory)
            section.populate_from_directory(directory, ref_factory)
