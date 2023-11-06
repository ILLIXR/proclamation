#!/usr/bin/env python3
# Copyright (c) 2020-2023 Collabora, Ltd. and the Proclamation contributors
#
# SPDX-License-Identifier: Apache-2.0
"""Setup."""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="proclamation",
    version="1.2.2",
    author="Rylie Pavlik",
    author_email="rylie.pavlik@collabora.com",
    description="A CHANGES/NEWS file creator",
    license="Apache-2.0 AND CC0-1.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/proclamation/proclamation",
    project_urls={
        "Source Code and Issue Tracker":
            "https://gitlab.com/proclamation/proclamation",
        "Documentation": "https://proclamation.readthedocs.io",
    },
    packages=setuptools.find_packages(),
    install_requires=["jinja2", "click>=7,<9"],
    include_package_data=True,
    entry_points={"console_scripts": ["proclamation=proclamation.main:cli"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
