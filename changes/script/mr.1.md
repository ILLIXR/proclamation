Handle missing directories more carefully. If a directory is found to be missing
during `draft`, we continue with a warning. However, if a directory is found to
be missing during `build`, we error out and modify no changelogs.
