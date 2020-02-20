#!/usr/bin/env python3 -i
# Copyright 2020 Collabora, Ltd.
#
# SPDX-License-Identifier: Apache-2.0
"""Project settings."""

from importlib import import_module



class SectionSettings:
    """Settings for a single Section."""

    def __init__(self, name, directory, extra_data=None):
        """Construct a section settings object."""
        self.name = name
        """Section name."""

        self.directory = directory
        """Directory where changelog chunks for this section can be found."""

        if extra_data is None:
            extra_data = {}
        self.extra_data = extra_data
        """Extra data for use by your template."""


class ProjectSettings:
    """Project settings class.

    Often parsed from JSON with a similar structure.
    """

    def __init__(self, project_name, template=None, base_url=None,
                 extra_data=None):
        """Construct a settings object."""
        self.name = project_name
        """Name of the project."""

        if template is None:
            template = "base.md"
        self.template = template
        """Filename of the changelog template."""

        self.sections = []
        """List of SectionSettings."""

        self.base_url = base_url
        """Base URL of project management."""

        if extra_data is None:
            extra_data = {}
        self.extra_data = extra_data
        """Extra data for use by your template."""


class Settings:
    """Top-level settings class.

    Often parsed from JSON with a similar structure.
    """

    def __init__(self):
        """Construct a top-level settings."""
        self.projects = []
        """List of ProjectSettings."""

    def add_project(self, project_settings):
        """Add a ProjectSettings object to this settings."""
        self.projects.append(project_settings)


def parse_section(section_name, section_info):
    return SectionSettings(section_name, section_info["directory"])


def parse_project(proj):
    proj_settings = ProjectSettings(
        proj["project_name"],
        proj["template"],
        proj.get("base_url"),
        proj.get("extra_data"))
    for section_name, section_info in proj["sections"].items():
        proj_settings.sections.append(
            parse_section(section_name, section_info))
    return proj_settings


def parse_settings(config):
    """Take settings from a dict into a Settings object."""
    settings = Settings()
    # Having multiple projects at top level is optional.
    projects = config.get("projects")
    if projects:
        for project in projects:
            settings.add_project(parse_project(project))
    else:
        settings.add_project(parse_project(config))
    return settings

def settings_from_json_io(io):
    """Load settings from json in an IO like a file or StringIO."""
    import json
    config = json.load(io)
    return parse_settings(config)

def settings_from_json_file(fn):
    """Load settings from a JSON file."""
    with open(str(fn), 'r', encoding='utf-8') as fp:
        return settings_from_json_io(fp)
