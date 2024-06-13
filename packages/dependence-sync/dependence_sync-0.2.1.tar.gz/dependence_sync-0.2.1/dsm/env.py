#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2024 The DSM Authors, All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree

import os

class Env:
    env_map = {}

    @staticmethod
    def get_env(key):
        return Env.env_map[key]
    
    @staticmethod
    def set_env(key, value):
        Env.env_map[key] = value


def init_env():
    current_dir = os.getcwd()
    file_name = '.dsm'
    result = None
    while True:
        files = os.listdir(current_dir)
        if file_name in files:
            result =  current_dir
            break
        parent_dir = os.path.dirname(current_dir)
        if current_dir == parent_dir:
            raise Exception('You have not initialized the DSM environment yet. You can initialize the workspace using dsm init -p.')
        current_dir = parent_dir
    Env.set_env('root_path', result)