#!/usr/bin/env python3
# Copyright (c) 2020 Collabora, Ltd.
#
# SPDX-License-Identifier: Apache-2.0
"""Main entry point."""

from .settings import settings_from_json_file
from .project import Project
from .render import render_template

import click


class ProjectCollection:
    def __init__(self, config_file, project_name, default_base,
                 ref_factory=None):
        self.project_name = project_name
        self.default_base = default_base
        settings = settings_from_json_file(config_file)
        self.projects = []
        for project_settings in settings.projects:
            if not self.should_process_project(project_settings.name):
                continue

            self.projects.append(Project(project_settings,
                                         default_base=default_base,
                                         ref_factory=ref_factory))

    def should_process_project(self, proj_name):
        if self.project_name is None:
            return True
        return self.project_name == proj_name


pass_project_collection = click.make_pass_decorator(ProjectCollection)


@click.group()
@click.option("--config",
              "config_file",
              type=click.Path(file_okay=True, dir_okay=False, readable=True),
              default=".proclamation.json",
              show_default=True,
              help="Config filename")
@click.option("--project",
              "project_name",
              metavar="NAME",
              default=None,
              help="Specify a single project from the config to process. "
              "If omitted, all projects in the config will be processed.")
@click.option("--default-base",
              "default_base",
              default=None,
              type=click.Path(file_okay=False, dir_okay=True),
              help="Specify a different default base directory to search.")
@click.option("-v", "--verbose",
              "verbose",
              count=True,
              help="Show verbose info messages. Repeat for even more verbosity.")
@click.pass_context
def cli(ctx, config_file, project_name, default_base, verbose):
    """Proclamation builds your NEWS files from chunks."""
    import logging
    if verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger(__name__).debug("Debug logging enabled.")
    elif verbose == 1:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger(__name__).info("Verbose logging enabled.")
    ctx.obj = ProjectCollection(config_file, project_name, default_base)


@cli.command()
@click.option("--version", "project_version",
              help="Render changelog template using provided version.")
@click.pass_context
@pass_project_collection
def draft(project_collection, ctx, project_version, ref_factory=None):
    """Preview the new portion of your NEWS file(s) to stdout."""

    if project_version is None:
        ctx.fail("Draft creation requires a version to be specified")
    for project in project_collection.projects:
        project.populate_sections(ref_factory)
        print("Rendered template for " + project.name)
        print(render_template(project, project_version))
