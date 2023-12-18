#!/usr/bin/env python3
# Copyright 2020-2023 Collabora, Ltd. and the Proclamation contributors
#
# SPDX-License-Identifier: Apache-2.0
#
# Original author: Rylie Pavlik <rylie.pavlik@collabora.com>


from typing import Iterable
from pathlib import Path
import logging


def remove_files(files: Iterable[Path]):
    """
    Remove the given files, if possible.
    Do not fail if they are not found.
    """
    log = logging.getLogger(__name__)
    for f in files:
        try:
            f.unlink()
            log.info("Removed %s", f)
        except FileNotFoundError:
            log.info("Skipping %s, not found", f)
