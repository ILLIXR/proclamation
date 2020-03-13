# Changelog for proclamation, the changelog combiner

```txt
SPDX-License-Identifier: CC0-1.0
SPDX-FileCopyrightText: 2020 Collabora, Ltd. and the Proclamation contributors
```

## proclamation 1.0.1 (2020-03-04)

- Script
  - Handle missing directories more carefully. If a directory is found to be
    missing during `draft`, we continue with a warning, skipping only that
    project. However, if a directory is found to be missing during `build`, we
    error out and modify no changelogs.
    ([!1](https://gitlab.com/ryanpavlik/proclamation/merge_requests/1))
  - Fix remove-fragments subcommand.
    ([#1](https://gitlab.com/ryanpavlik/proclamation/issues/1),
    [!4](https://gitlab.com/ryanpavlik/proclamation/merge_requests/4))
  - Fix the functioning of the `--delete-fragments` option of the `build`
    subcommand. ([!5](https://gitlab.com/ryanpavlik/proclamation/merge_requests/5),
    [#2](https://gitlab.com/ryanpavlik/proclamation/issues/2))
  - Ensure that a new changelog portion always ends with a blank line.
    ([!6](https://gitlab.com/ryanpavlik/proclamation/merge_requests/6),
    [#3](https://gitlab.com/ryanpavlik/proclamation/issues/3))
  - Pass project `base_url` from settings to template. (bug fix)
    ([!2](https://gitlab.com/ryanpavlik/proclamation/merge_requests/2))
- Templates
  - Fix a number of issues with the base template: missed leftover renaming errors,
    spacing errors, duplicated parentheses around references.
    ([!3](https://gitlab.com/ryanpavlik/proclamation/merge_requests/3))
  - Further fix spacing in default template, and add a test for correct behavior of
    the template in simple scenarios.
    ([!6](https://gitlab.com/ryanpavlik/proclamation/merge_requests/6),
    [#3](https://gitlab.com/ryanpavlik/proclamation/issues/3))

## proclamation 1.0.0 (2020-02-24)

Initial release.
