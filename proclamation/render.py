#!/usr/bin/env python3 -i
# Copyright 2019-2020 Collabora, Ltd.
#
# SPDX-License-Identifier: Apache-2.0
"""Use Jinja2 to render an addition to the CHANGES file.

This should be the only file that needs to import Jinja2,
so if you want to do something else for templating, you can.
"""

import logging

from jinja2 import (ChoiceLoader, Environment, FileSystemLoader, PackageLoader,
                    TemplateSyntaxError)


def render_template(project, project_version):
    """Render the CHANGES template for a project.

    Returns the rendered text.
    """
    log = logging.getLogger(__name__)
    search_path = [project.default_base]
    log.debug(
        "Template search path is %s, followed by built-in templates.",
        str(search_path))
    loader = ChoiceLoader([
        FileSystemLoader(search_path),
        PackageLoader("proclamation", "templates")
    ])

    env = Environment(trim_blocks=True, autoescape=False, loader=loader)
    try:
        template = env.get_template(project.template)
    except TemplateSyntaxError as e:
        print("template syntax error during parse: {}:{} error: {}".
              format(e.filename, e.lineno, e.message))
        raise RuntimeError("Jinja2 template syntax error")

    log.info("Loaded template %s from %s", project.template, template.filename)
    try:
        return template.render({
            "project_name": project.name,
            "project_version": project_version,
            "sections": project.sections
        })
    except TemplateSyntaxError as e:
        print("template syntax error during render: {}:{} error: {}".
              format(e.filename, e.lineno, e.message))
        raise RuntimeError("Jinja2 template syntax error")
