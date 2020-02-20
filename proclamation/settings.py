#!/usr/bin/env python3 -i
# Copyright 2020 Collabora, Ltd.
#
# SPDX-License-Identifier: Apache-2.0
"""Project settings."""


class SectionSettings:
    """Settings for a single Section."""

    def __init__(self, name, directory):
        """Construct a section settings object."""
        self.name = name
        """Section name."""
        self.directory = directory
        """Directory where changelog chunks for this section can be found."""


class ProjectSettings:
    """Project settings class.

    Often parsed from JSON with a similar structure.
    """

    def __init__(self, project_name, template):
        """Construct a settings object."""
        self.name = project_name
        """Name of the project."""
        self.template = template
        """Filename of the changelog template."""
        self.sections = []
        """List of SectionSettings."""


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


def _parse_project(proj):
    proj_settings = ProjectSettings(proj["project_name"], proj["template"])
    for section_name, section_info in proj["sections"].items():
        proj_settings.sections.append(SectionSettings(
            section_name, section_info["directory"]))
    return proj_settings


def settings_from_json_io(io):
    """Load settings from json in an IO like a file or StringIO."""
    import json
    config = json.load(io)
    settings = Settings()

    # Having multiple projects at top level is optional.
    projects = config.get("projects")
    if projects:
        for project in projects:
            settings.add_project(_parse_project(project))
    else:
        settings.add_project(_parse_project(config))

    return settings


def settings_from_json_file(fn):
    """Load settings from a JSON file."""
    with open(str(fn), 'r', encoding='utf-8') as fp:
        return settings_from_json_io(fp)
