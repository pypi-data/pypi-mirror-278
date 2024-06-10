#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2024 The DSM Authors, All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree

import argparse
from dsm.deps import Deps
from dsm.sync import Sync
from dsm.env import init_env
from dsm.init_project import InitProject

def main():
    parser = argparse.ArgumentParser(description='dependences sync manager(DSM)')
    subparsers = parser.add_subparsers(dest='command', help='Subcommands')
    init_parser = subparsers.add_parser('init', help='init workspace')
    init_parser.add_argument('path', type=str, help='Directory need to be inited')
    sync_parser = subparsers.add_parser('sync', help='Sync subcommand')
    sync_parser.add_argument('-f', '--force', action='store_true', help='Forcefully re-pull and overwrite existing contentc')
    sync_parser.add_argument('deps_dir', type=str, help='Directory where DEPS file is located')
    args = parser.parse_args()
    if args.command is not None:
        if args.command == 'init':
            InitProject().create(args)
        elif args.command == 'sync':
            init_env()
            deps = Deps(args.deps_dir)
            Sync(args).run(deps)
        else:
            raise Exception(f'Unsupport command {args.command}')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()


