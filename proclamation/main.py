#!/usr/bin/env python3
# Copyright (c) 2020 Collabora, Ltd.
#
# SPDX-License-Identifier: Apache-2.0
"""Main entry point."""

import logging

import click

from .project import Project
from .render import render_template
from .settings import settings_from_json_file


class ProjectCollection:
    def __init__(self, config_file, project_name, default_base,
                 ref_factory=None):
        self.project_name = project_name
        self.default_base = default_base
        settings = settings_from_json_file(config_file)
        self.projects = []
        log = logging.getLogger(__name__).getChild("ProjectCollection")
        for project_settings in settings.projects:
            if not self.should_process_project(project_settings.name):
                log.info("Skipping project %s, not selected on command line")
                continue

            log.debug("Initializing project %s", project_settings.name)
            self.projects.append(Project(project_settings,
                                         default_base=default_base,
                                         ref_factory=ref_factory))

    def should_process_project(self, proj_name):
        if self.project_name is None:
            return True
        return self.project_name == proj_name


pass_project_collection = click.make_pass_decorator(ProjectCollection)


@click.group()
@click.option("-c", "--config",
              "config_file",
              type=click.Path(file_okay=True, dir_okay=False, readable=True),
              default=".proclamation.json",
              show_default=True,
              help="Config filename")
@click.option("-p", "--project",
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
              help="Show verbose info messages. Repeat for more verbosity.")
@click.pass_context
def cli(ctx, config_file, project_name, default_base, verbose):
    """Proclamation builds your NEWS files from chunks."""
    fmt = "[%(levelname)s:%(name)s]  %(message)s"
    if verbose >= 2:
        logging.basicConfig(format=fmt, level=logging.DEBUG)
        logging.getLogger(__name__).debug("Debug logging enabled.")
    elif verbose == 1:
        logging.basicConfig(format=fmt, level=logging.INFO)
        logging.getLogger(__name__).info("Verbose logging enabled.")
    else:
        logging.basicConfig(format=fmt)
    ctx.obj = ProjectCollection(config_file, project_name, default_base)


@cli.command()
@click.argument("project_version", metavar="VERSION")
@click.pass_context
@pass_project_collection
def draft(project_collection, ctx, project_version, ref_factory=None):
    """Preview the new VERSION portion of your NEWS file(s) to stdout."""

    if project_version is None:
        ctx.fail("Draft creation requires a version to be specified")
    for project in project_collection.projects:
        project.populate_sections(ref_factory)
        print(render_template(project, project_version))


@cli.command()
@click.argument("project_version", metavar="VERSION")
@click.option("-d", "--delete-chunks",
              "delete_chunks",
              is_flag=True,
              help="Delete processed chunks when complete")
@click.pass_context
@pass_project_collection
def build(project_collection, ctx, project_version, delete_chunks,
          ref_factory=None):
    """Build your new NEWS file."""
    if len(project_collection.projects) != 1:
        raise click.UsageError(
            "You may only build a single project at a time: "
            "please specify --project-name",
            ctx)
    project = project_collection.projects[0]
    project.populate_sections(ref_factory)
    print(render_template(project, project_version))

    if delete_chunks:
        remove_files(project.chunk_filenames)


@cli.command()
@click.confirmation_option()
@click.pass_context
@pass_project_collection
def remove_chunks(project_collection, ctx, ref_factory=None):
    """Remove NEWS chunks associated with all projects (or specified projects).

    If you only have one project, or your projects don't share sections,
    you may consider using the --delete-chunks option of "build" instead.
    """
    all_files = set()
    for project in project_collection.projects:
        project.populate_sections(ref_factory)
        all_files += set(project.chunk_filenames)
    remove_files(all_files)


def remove_files(files):
    log = logging.getLogger(__name__)
    for f in files:
        try:
            f.unlink()
            log.info("Removed %s", f)
        except FileNotFoundError:
            log.info("Skipping %s, not found", f)
