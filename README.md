# proclamation

[![pipeline status](https://gitlab.com/ryanpavlik/proclamation/badges/master/pipeline.svg)](https://gitlab.com/ryanpavlik/proclamation/-/commits/master)
[![coverage report](https://gitlab.com/ryanpavlik/proclamation/badges/master/coverage.svg)](https://gitlab.com/ryanpavlik/proclamation/-/commits/master)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md)

A tool for building CHANGES/NEWS files from fragments.

Inspired by [towncrier][], but completely language-agnostic and markup-agnostic.

## About Proclamation and Usage Instructions

The "proclamation" tool assembles changelogs, which incorporate fragments of
changelog text added by the author of a change in a specific location and
format.

### Fragments

Each change should add a changelog fragment file, whose contents are
Markdown-formatted text describing the change briefly. Reference metadata will
be used to automatically add links to associated issues/merge requests/pull
requests, so no need to add these in your fragment text. The simplest changelog
fragment just contains one line of Markdown text describing the change:

```md
Here the author of a change has written some text about it.
```

### References

The changelog fragment system revolves around "references" - these are issue
reports, pull requests, or merge requests associated with a
change. Each fragment must have at least one of these, which forms the main part
of the filename. If applicable, additional can be added within the file - see
below for details.

This portion of the proclamation system is intentionally left very flexible,
since there are very many ways of organizing and managing a project. By default,
references are delimited by the `.` character. The first two fields have some
conventional meaning, while any additional fields are up to the user and are
only used if a custom template is supplied by a project.

The format of references in general is:

```txt
<ref_type>.<number>
```

where

- `ref_type` is "issue", "mr", or "pr"
- `number` is the issue, MR, or PR number
- any additional `.`-delimited tokens are passed on to the template in the
  `service_params` list.

Your changelog fragment filename is simply the "main" reference with the `.md`
extension added. (You can also use `.rst` or `.txt` as your extension in your
project.)

To specify additional references in a file, prefix the contents of the changelog
fragment with a block delimited above and below by `---`, with one reference on
each line. (This can be seen as a very minimal subset of "YAML Front Matter", if
you're familiar with that concept.) For example:

```md
---
- issue.35
- mr.93
---
Here the author of a change has written some text about it.
```

There are provisions for providing your own reference parser if this format is
entirely unusable, but they're underdeveloped. If this functionality is
interesting to you, get involved and help finish it!

### Sections

Changelog fragments are organized into sections, each of which should have its
own directory. These might be "type-of-change" sections (e.g. new feature,
bugfix, etc). Alternately, they might be logical sub-projects - it's permissable
to have multiple projects configured in one config file and repo with
partially-overlapping sections. (This is actually a part of one of the
originally motivating use cases for this tool.)

Every file whose filename parses and meets some basic checks will be used!
Having a `changes/your_section_name` directory for each section is recommended.
You can provide a `README.md` file with a modified subset of this file in that
directory, as guidance to contributors to your project. (`README.md` won't parse
as a reference, so it will not be treated as a changelog fragment.)

Use whatever works for your project. Right now, all changelog fragments must be
in a section, sections must be a single directory, and sections may not be
nested. If you'd like to loosen these assumptions, get involved and help!

## Installation

Proclamation is available on [pypi][], so you can install it for your local user with:

```sh
pip3 install --user proclamation
```

Alternately, you can install from this repository. If you do this, it's
recommended to install this in a virtualenv. Something like this will work on
*nix-like systems, adjusted for your shell usage.

```bash
# Create a virtualenv in `venv`
python3 -m venv venv

# Activate it
. venv/bin/activate

# Install a link to this package in the venv.
pip install --editable .
```

If you follow those instructions, the virtualenv will refer to the source
instead of copying the source, so updating your local clone of this repo will
also update the virtualenv. Omit the `--editable` if you want other behavior.

Note that the `venv/bin/proclamation` script can be run from outside the venv,
through the magic of setuptools, so if you want to be able to use it elsewhere
on your system, you might symlink it into a directory that's in your PATH.

[pypi]: https://pypi.org/project/proclamation/

## Configuration

Your project should have a configuration file: the default name is
`.proclamation.json`. The top level object can either be a project config object
directly, or contain a member named "projects" with an array of project config
objects.

You can look at the config file for this project for guidance, since it's a
pretty simple use case of this tool. (proclamation was designed to handle more
elaborate use-cases than this.)

- Project attributes:
  - `project_name` - Required. Used to form the heading in the default template,
    etc.
  - `base_url` - Technically optional, but required if you're using the default
    template. Passed to the template which may use it to form reference links.
  - `news_filename` - Optional, in case your changelog isn't called NEWS.
  - `sections` - Required: contains an object. The key names are the section
    names (used by the default template for section headers), while the values
    are objects. Sections might be logical sub-projects, or alternately
    categories of changes (feature, bug fix, etc), it's up to you.
    - The only key valid right now in the child of the section is `directory`,
      which indicates the directory to search for changelog fragments.
  - `template` - Optional. The name of a Jinja2 template for a single release's
    changelog section. `base.md` comes with proclamation and is used by default.
    Your custom template might inherit from this if you only need to change a
    few small details. Evaluated relative to the current working directory when
    you run proclamation.
  - `insert_point_pattern` - Useful mainly if you're not using the default
    template. The first match of this regex will be considered the first line of
    a release entry, and your new release will be put in your changelog file
    above it. Default works with the default template (looks for a second-level
    Markdown heading).
  - `extra_data` - Any extra data you'd like to pass along to your custom
    template.

## Sample Usage Workflow

Note that the base `proclamation` script and all its subcommands have help,
accessible through `-h` or `--help`. The guidance in this section of the README
is intentionally minimal, to avoid contradicting the online help which remains
up-to-date implicitly. This is also only the simplest, minimal way to perform
these operations: if your project is more complex, there may already be more
features to support your needs in the command line help.

### During Development

As changes get submitted to your project, have each change author create a
changelog fragment file. Since these are all separate files, with names made
unique by your issue/repo tracker, there won't be merge conflicts no matter what
order they're merged in. (This is the central benefit of proclamation, and its
inspiration, towncrier, over having each contributor edit CHANGES as part of
their submission.)

At any time you can run `proclamation draft` to preview the release portion that
would be added to your changelog if you released at that time.

### Preparing for a Release

When you're ready to perform a release, you'll want to run proclamation to
update your changelog, then remove the fragments that you've incorporated into
the regular changelog. You can use a command like the following:

```sh
proclamation build YOUR_NEW_VERSION
```

to preview the full file on screen. When you're ready to actually perform the
update, run something like:

```sh
proclamation build YOUR_NEW_VERSION --delete-fragments --overwrite
```

to overwrite your changelog file with the updated one and delete the used
changelog fragments.

You're welcome to manually edit the new (or old!) changelog entries as desired:
as long as the `insert_point_pattern` (by default, `^## .*`) can still match,
proclamation will not be confused.

Finally, make sure the deletion of the fragments and the update of the changelog
has been checked in to your version control system.

## Development of proclamation

You can use the same installation instructions above to locally install a link in a virtualenv.

- Run `pytest-3` or similar to run the automated tests.
- Run `autopep8 proclamation/*.py proclamation/test/*.py --in-place` to
  automatically format the source code with [autopep8][].
- Use [`tox`][tox] to run flake8 as well as tests for multiple Python versions.
  - e.g. on Debian Buster, you can run `tox -e py35,py37,flake8`
- When submitting a change, be sure to create your changelog fragment in the changes directory! :)

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By
participating in this project you agree to abide by its terms.

[towncrier]: https://github.com/hawkowl/towncrier
[tox]: https://tox.readthedocs.io/en/latest/
[flake8]: https://flake8.pycqa.org/en/latest/
[autopep8]: https://github.com/hhatto/autopep8
