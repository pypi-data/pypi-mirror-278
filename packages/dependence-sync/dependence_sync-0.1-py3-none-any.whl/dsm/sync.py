#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2024 The DSM Authors, All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree
import os

from dsm.deps import Deps
from dsm.fetcher import FetcherFactory
from dsm.env import Env

class Sync:
    def __init__(self, args):
        self.force = args.force

    def need_fetch(self, target):
        target_path = os.path.join(Env.get_env('root_path'), target)
        return self.force or not os.path.exists(target_path) or not any(os.scandir(target_path))

    def run(self, deps: Deps):
        ignore_files = []
        for target in deps.deps_meta_data.keys():
            meta_data = deps.deps_meta_data[target]
            if not self.need_fetch(target):
                continue
            FetcherFactory.generate(meta_data['type']).fetch(meta_data).move(target)
            if meta_data['ignore']:
                ignore_files.append(target)
        self.set_ignore(ignore_files)
    
    def set_ignore(self, ignored_files):
        exclude_file = os.path.join(Env.get_env('root_path'), '.git', 'info', 'exclude')
        if not os.path.exists(os.path.dirname(exclude_file)):
            # os.mkdirs(os.path.dirname(exclude_file))
            return
        if os.path.exists(exclude_file):
            with open(exclude_file, 'r') as f:
                ignored_files = set(ignored_files + [line.strip() for line in f.readlines() if line.strip()])
        with open(exclude_file, 'w') as f:
            f.write('\n'.join(ignored_files) + '\n')
