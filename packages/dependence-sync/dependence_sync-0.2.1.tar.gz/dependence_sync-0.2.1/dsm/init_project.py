#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2024 The DSM Authors, All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree

import os

class InitProject:
    def __init__(self):
        pass

    def create(self, args):
        path = os.path.join(args.path, '.dsm')
        if os.path.exists(path):
            print('The repository has already been initialized, no need to initialize again.')
        else:
            with open(path, 'w') as file:
                pass
        