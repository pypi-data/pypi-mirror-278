#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2024 The DSM Authors, All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree

import random
import string
import os
import subprocess
import shutil
import requests
from dsm.env import Env

class Fetcher:
    def __init__(self):
        self.root_path = Env.get_env('root_path')
        self.tmp_path = os.path.join(self.root_path, 'TMP_' + ''.join(random.choices(string.ascii_letters + string.digits, k=10)))

    def fetch(self, meta_data):
        return self

    def move(self, target):
        target = os.path.join(self.root_path, target)
        parent_path = os.path.dirname(target)
        if os.path.exists(target):
            shutil.rmtree(target)
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)
        subprocess.check_call(f'mv -f {self.tmp_path} {target}', shell=True)


class GitFetcher(Fetcher):
    def __init__(self):
        super().__init__()

    def fetch(self, meta_data):
        repo = meta_data['repo']
        commit = meta_data['commit']
        os.makedirs(self.tmp_path)
        os.chdir(self.tmp_path)
        subprocess.check_call('git init', shell=True)
        subprocess.check_call(f'git remote add origin {repo}', shell=True)
        subprocess.check_call(f'git fetch origin {commit}', shell=True)
        subprocess.check_call(f'git checkout {commit}', shell=True)
        os.chdir(self.root_path)
        return self
    

class PackageFetcher(Fetcher):
    def __init__(self):
        super().__init__()
    
    def fetch(self, meta_data):
        url = meta_data['url']
        name = meta_data['name']
        decompress = meta_data['decompress']
        os.makedirs(self.tmp_path)
        os.chdir(self.tmp_path)
        print(f"fetching package from {url} to {name}")        
        response = requests.get(url)
        with open(name, "wb") as file:
            file.write(response.content)
        
        if decompress:
            subprocess.check_call(f'tar -zxf {name}', shell=True)
            subprocess.check_call(f'rm -rf {name}', shell=True)
        os.chdir(self.root_path)
        return self

    

class FetcherFactory:
    @staticmethod
    def generate(type):
        if type == 'git':
            return GitFetcher()
        elif type == 'package':
            return PackageFetcher()
        else:
            return Fetcher()
