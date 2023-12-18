# Changelog for Proclamation, the changelog combiner

<!--
SPDX-License-Identifier: CC0-1.0
SPDX-FileCopyrightText: 2020-2023 Collabora, Ltd. and the Proclamation contributors
-->

## Proclamation 2.0.0 (2023-12-18)

This is mainly a usability release, changing default behavior of the CLI to make
it more ergonomic given several years' experience of using this tool. It also
adds a new CLI subcommand, `merge`, to help project maintainers at release time
combine things that do not actually require their own changelog item after all.
(It is assumed that the merged fragment will be edited by the maintainer prior
to building the updated changelog, often by combining the content of the two
bullet points.)

**Please be aware of the breaking changes: they may affect your workflow as well as your configuration!**

- Script
  - **Breaking change**: Change the parameters and defaults of the CLI interface so
    that the most common base is default. This makes `build` overwrite and remove
    fragments by default, primarily.
    ([!29](https://gitlab.com/proclamation/proclamation/merge_requests/29))
  - Add a new `merge` subcommand, for combining changelog fragment files.
    ([!30](https://gitlab.com/proclamation/proclamation/merge_requests/30))
- API
  - **Breaking change**: Most references to "NEWS" in the API have been removed or changed to
    "changelog".
    ([!32](https://gitlab.com/proclamation/proclamation/merge_requests/32))
- Templates
  - No significant changes
- Misc
  - **Breaking change**: The default "news" filename is now `CHANGELOG.md`. If you were
    using the default, you will need to update your project config.
    ([!32](https://gitlab.com/proclamation/proclamation/merge_requests/32))
  - Migrate to using `flit` instead of `setuptools`/`setup.py` for the build
    system.
    ([!28](https://gitlab.com/proclamation/proclamation/merge_requests/28))
  - Switch from `autopep8` to `black` for the code formatter.
    ([!31](https://gitlab.com/proclamation/proclamation/merge_requests/31))

## Proclamation 1.2.2 (2023-11-06)

This is a minor release, primarily to update URLs and names.

This release also no longer works with Python 3.6, which has been end-of-life
for a long time by now.

- Script
  - Clean up formatting and warnings from newer versions of Python tooling.
    ([!23](https://gitlab.com/proclamation/proclamation/merge_requests/23),
    [!26](https://gitlab.com/proclamation/proclamation/merge_requests/26))
  - Fix minor bug in logging.
    ([!25](https://gitlab.com/proclamation/proclamation/merge_requests/25))
- Templates
  - No significant changes
- Misc
  - Update URL for project (now its own GitLab organization) and author name.
    ([!23](https://gitlab.com/proclamation/proclamation/merge_requests/23))
  - Remove Python 3.6 from support/test list, add through 3.12 to tests.
    ([!23](https://gitlab.com/proclamation/proclamation/merge_requests/23))
  - Improve respectful language in code.
    ([!24](https://gitlab.com/proclamation/proclamation/merge_requests/24),
    [!26](https://gitlab.com/proclamation/proclamation/merge_requests/26))
  - Update README.
    ([!27](https://gitlab.com/proclamation/proclamation/merge_requests/27))

## Proclamation 1.2.1 (2021-10-25)

This is a very minor release to improve ease of installation.

- Script
  - Mark as compatible with click version 8: no code changes required.
    ([!22](https://gitlab.com/proclamation/proclamation/merge_requests/22))

## Proclamation 1.2.0 (2021-07-15)

This version has a minor API change (return value from `Fragment.parse_file`) to
support the new user-facing feature: multiple fragments in a single file using
bullets. This was added because I kept seeing people try this approach in
projects I maintain, so it made sense to simply support it.

This release also no longer works with Python 3.5, which has been end-of-life
for over six months by now.

- Script
  - Be able to strip bullets from content lines.
    ([!20](https://gitlab.com/proclamation/proclamation/merge_requests/20),
    [#14](https://gitlab.com/proclamation/proclamation/issues/14))
  - Generate multiple fragments from a fragment file with multiple bullets.
    ([!20](https://gitlab.com/proclamation/proclamation/merge_requests/20),
    [#14](https://gitlab.com/proclamation/proclamation/issues/14))
- Templates
  - No significant changes
- Misc
  - Proclamation now requires Python 3.6 or greater, as some modern type
    annotations have been added in the codebase for ease of development.
    ([!20](https://gitlab.com/proclamation/proclamation/merge_requests/20))
  - A sample `.markdownlint.yaml` file is included, which you may wish to
    copy into your own project's `changes` directory.
    ([!21](https://gitlab.com/proclamation/proclamation/merge_requests/21))

## Proclamation 1.1.1 (2020-07-28)

This adds one major new feature (`sort_by_prefix`), a public JSON schema, and a
variety of smaller improvements.

(Version 1.1.0 was briefly tagged but never published to PyPI, 1.1.1 replaces it
entirely.)

- Script
  - Add section setting `sort_by_prefix` to allow optionally sorting by a colon-
    delimited prefix in fragment text (or the first word if no colon exists).
    ([!16](https://gitlab.com/proclamation/proclamation/merge_requests/16))
  - Report an error if a project name is specified but not found in the config
    file, and add tests for `ProjectCollection`.
    ([!18](https://gitlab.com/proclamation/proclamation/merge_requests/18),
    [#12](https://gitlab.com/proclamation/proclamation/issues/12))
- Templates
  - Start fragment references on a new line, and only place one reference per line
    (manually wrapped). This keeps the wrapping filter from mangling the Markdown-
    formatted links.
    ([!15](https://gitlab.com/proclamation/proclamation/merge_requests/15))
- Misc
  - docs: Mention the emerging practice of starting your fragment with a component,
    subsection, or change type (feature or bug fix), followed by a colon, like this
    entry.
    ([!15](https://gitlab.com/proclamation/proclamation/merge_requests/15))
  - Improve API documentation.
    ([!16](https://gitlab.com/proclamation/proclamation/merge_requests/16))
  - Add more tests for `Project`, `Fragment` (including parsing from disk), and
    `SectionSettings`.
    ([!16](https://gitlab.com/proclamation/proclamation/merge_requests/16))
  - Add a JSON Schema for config files. To use, add
    `"$schema": "https://proclamation.gitlab.io/proclamation/proclamation.schema.json"`
    to the root of your config file. Some editors will use this to provide
    editing help.
    ([!17](https://gitlab.com/proclamation/proclamation/merge_requests/17))
  - The name of the default branch has been changed to `main`.

## Proclamation 1.0.2.2 (2020-03-23)

Packaging release: no functional change if you run from source or have your own
template. Otherwise, upgrade recommended.

- Fix `MANIFEST.in` to properly package the base template.

## Proclamation 1.0.2.1 (2020-03-18)

Brown-paper-bag release: no functional change, no need to upgrade from 1.0.2.

- Fix reuse.software metadata. No functional change.
  ([!14](https://gitlab.com/proclamation/proclamation/merge_requests/14))

## Proclamation 1.0.2 (2020-03-18)

- Script
  - Remove redundant code from reference parsing, and improve docstrings/doctests.
    ([!8](https://gitlab.com/proclamation/proclamation/merge_requests/8))
  - Sort fragments in each section based on the tuple-ized form of their first
    reference (from the filename). This will keep MR's in a section in numerical
    order, etc. ([!9](https://gitlab.com/proclamation/proclamation/merge_requests/9),
    [#4](https://gitlab.com/proclamation/proclamation/issues/4))
  - Error out if we can't parse a front-matter line as a reference, instead of
    silently swallowing the error.
    ([!11](https://gitlab.com/proclamation/proclamation/merge_requests/11))
  - Support comment lines in per-fragment (YAML-like) front matter: a line with `#`
    followed by anything, optionally preceded by whitespace.
    ([!11](https://gitlab.com/proclamation/proclamation/merge_requests/11),
    [#8](https://gitlab.com/proclamation/proclamation/issues/8))
- Templates
  - No significant changes
- Misc
  - Adjust copyright and license notices, placing documentation, config file, and
    templates under CC0-1.0 so they may be re-used in other projects that use
    Proclamation.
    ([!7](https://gitlab.com/proclamation/proclamation/merge_requests/7))
  - Changes to ensure compliance with version 3.0 of the
    [REUSE](https://reuse.software) specification as well as [standard-
    readme](https://github.com/RichardLitt/standard-readme)
    ([!7](https://gitlab.com/proclamation/proclamation/merge_requests/7))
  - Split some content from `README.md` into a `USAGE.md` designed for reuse in
    projects that use Proclamation.
    ([!7](https://gitlab.com/proclamation/proclamation/merge_requests/7))
  - Add Sphinx documentation, connected to read-the-docs.
    ([!8](https://gitlab.com/proclamation/proclamation/merge_requests/8))
  - Update `setup.py` to specify that we need `click` version 7.
    ([!10](https://gitlab.com/proclamation/proclamation/merge_requests/10),
    [#7](https://gitlab.com/proclamation/proclamation/issues/7))
  - Fix spelling errors/typos, and add `codespell` to tox and CI.
    ([!12](https://gitlab.com/proclamation/proclamation/merge_requests/12),
    [#6](https://gitlab.com/proclamation/proclamation/issues/6))
  - Start testing against Python 3.8 as well.
    ([!13](https://gitlab.com/proclamation/proclamation/merge_requests/13))
  - Note in USAGE that you can append a `.2`, `.3`, etc. before the extension of a
    filename if you want more than one changelog item for a single "main"
    reference.
    ([!13](https://gitlab.com/proclamation/proclamation/merge_requests/13))

## Proclamation 1.0.1 (2020-03-04)

- Script
  - Handle missing directories more carefully. If a directory is found to be
    missing during `draft`, we continue with a warning, skipping only that
    project. However, if a directory is found to be missing during `build`, we
    error out and modify no changelogs.
    ([!1](https://gitlab.com/proclamation/proclamation/merge_requests/1))
  - Fix remove-fragments subcommand.
    ([#1](https://gitlab.com/proclamation/proclamation/issues/1),
    [!4](https://gitlab.com/proclamation/proclamation/merge_requests/4))
  - Fix the functioning of the `--delete-fragments` option of the `build`
    subcommand. ([!5](https://gitlab.com/proclamation/proclamation/merge_requests/5),
    [#2](https://gitlab.com/proclamation/proclamation/issues/2))
  - Ensure that a new changelog portion always ends with a blank line.
    ([!6](https://gitlab.com/proclamation/proclamation/merge_requests/6),
    [#3](https://gitlab.com/proclamation/proclamation/issues/3))
  - Pass project `base_url` from settings to template. (bug fix)
    ([!2](https://gitlab.com/proclamation/proclamation/merge_requests/2))
- Templates
  - Fix a number of issues with the base template: missed leftover renaming errors,
    spacing errors, duplicated parentheses around references.
    ([!3](https://gitlab.com/proclamation/proclamation/merge_requests/3))
  - Further fix spacing in default template, and add a test for correct behavior of
    the template in simple scenarios.
    ([!6](https://gitlab.com/proclamation/proclamation/merge_requests/6),
    [#3](https://gitlab.com/proclamation/proclamation/issues/3))

## Proclamation 1.0.0 (2020-02-24)

Initial release.
