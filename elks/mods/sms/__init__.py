#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 46elks AB <hello@46elks.com>
# Developed in 2016 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import importlib

submodules = ['list', 'new']

def parse_arguments(parser):
    parser.description = (
        'Send and receive SMS'
    )
    subparsers = parser.add_subparsers(help='Sub-commands',
        dest='sms_subparser')
    for module in submodules:
        mod = importlib.import_module('.%s' % module, 'elks.mods.sms')
        mod.parse_arguments(subparsers.add_parser(module))

def main(args):
    if args.sms_subparser in submodules:
        mod = importlib.import_module('.%s' % args.sms_subparser,
                'elks.mods.sms')
        mod.main(args)
    else:
        print (
            'The SMS Module\n\n',
            'Sub-commands:\n',
            '- new\n',
            '- list\n\n',
            'Handle SMS on your 46elks account'
        )
    
