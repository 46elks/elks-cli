#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 46elks AB <hello@46elks.com>
# Developed in 2016 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import importlib

submodules = ['list']
import_module = lambda mod: importlib.import_module('.%s' % mod,
    'elks.mods.calls')

def parse_arguments(parser):
    parser.description = (
        'List and make calls'
    )
    subparsers = parser.add_subparsers(help='Sub-commands',
        dest='calls_subparser')
    for module in submodules:
        mod = import_module(module)
        mod.parse_arguments(subparsers.add_parser(module))

def main(args):
    if args.calls_subparser in submodules:
        mod = import_module(args.calls_subparser)
        mod.main(args)
    else:
        print (
            'The Calls Module\n\n',
            'Sub-commands:\n',
            '- list\n\n',
            'Handle incoming and outgoing calls on your 46elks account'
        )

