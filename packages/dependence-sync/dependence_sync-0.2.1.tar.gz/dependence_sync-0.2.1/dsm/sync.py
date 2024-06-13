#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2024 The DSM Authors, All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree
import os
import subprocess

from dsm.deps import Deps
from dsm.fetcher import FetcherFactory
from dsm.env import Env

class NeedSync:
    def __init__(self, target, meta_data, force):
        self.target_path = os.path.join(Env.get_env('root_path'), target)
        self.force = force
        self.meta_data = meta_data
    
    def __bool__(self):
        return self.force or not os.path.exists(self.target_path) or not any(os.scandir(self.target_path))
    
class GitNeedSync(NeedSync):
    def __init__(self, target, meta_data, force):
        super().__init__(target, meta_data, force)
    
    def __bool__(self):
        result_from_super = super().__bool__()
        if result_from_super:
            return result_from_super
        commit = self.meta_data['commit']
        current_path = os.getcwd()
        os.chdir(self.target_path)
        result = False
        try:
            current_commit = subprocess.check_output('git rev-parse HEAD', shell=True).decode('utf-8').strip()
            if current_commit != commit:
                print(current_commit, commit)
                result = True
        except Exception as e:
            # if have any exception, should sync resource again.
            result = True
        finally:
            os.chdir(current_path)
            return result
        
class PackageNeedSync(NeedSync):
    def __init__(self, target, meta_data, force):
        super().__init__(target, meta_data, force)
    
    def __bool__(self):
        result_from_super = super().__bool__()
        if result_from_super:
            return result_from_super
        result = False
        sha256 = self.meta_data['sha256']
        current_path = os.getcwd()
        os.chdir(self.target_path)
        try:
            with open('SHA256', 'r') as f:
                if sha256 != f.read():
                    result = True
        except Exception as e:
            result = True
        finally:
            os.chdir(current_path)
            return result

def NeedSyncFactory(type, target, meta_data, force):
    if type == 'git':
        return GitNeedSync(target, meta_data, force)
    elif type == 'package':
        return PackageNeedSync(target, meta_data, force)
    else:
        raise Exception(f'Need Sync not support for type {type}')

class Sync:
    def __init__(self, args):
        self.force = args.force

    def run(self, deps: Deps):
        ignore_files = []
        for target in deps.deps_meta_data.keys():
            meta_data = deps.deps_meta_data[target]
            if not NeedSyncFactory(meta_data['type'], target, meta_data, self.force):
                continue
            FetcherFactory.generate(meta_data['type']).fetch(meta_data).move(target)
            if 'ignore' not in meta_data or meta_data['ignore']:
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
