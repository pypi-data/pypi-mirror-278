#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2024 The DSM Authors, All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dependence-sync",
    version="0.2",
    author="Song Zhao",
    author_email="zhaosonggo@163.com",
    description="Code Dependency Synchronization Management Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/zhaosong-lmm_admin/depend-sync",
    packages=setuptools.find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'dsm=dsm.app:main'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)