#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2024 The DSM Authors, All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree

import os

class Deps:
    def __init__(self, path):
        deps_file_path = os.path.join(path, 'DEPS')
        with open(deps_file_path, 'r') as deps_file:
            local_env = {}
            exec(deps_file.read(), local_env)
        self.deps_meta_data = local_env['deps']
