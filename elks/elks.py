#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 46elks AB <hello@46elks.com>
# Developed in 2016 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License

import argparse
import sys
from elks.__init__ import __version__ as VERSION

modules = sorted([
    'billing',
    'list-sms',
    'new-sms',
    'numbers',
    'status',
    'subaccounts'
])

def import_module(mod):
    elks = __import__('elks.%s' % mod)
    return getattr(elks, mod)

def main():
    if sys.version_info < (3,):
      print('elks requires Python 3 to run')
      exit(-1)
    global modules
    parser = argparse.ArgumentParser(prog='elks')
    parser.add_argument('--version', action='store_true',
        help='Display elks version')
    parser.add_argument('-c', '--config', dest='configfile', action='store_true',
        help='Location of elks/elkme conffile')
    subparsers = parser.add_subparsers(help='Sub-commands', dest='subparser_name')
    for module in modules:
        mod = import_module(module)
        try:
            mod.parse_arguments(subparsers.add_parser(module))
        except NotImplementedError as e:
            print(e)
            print('\nThat must be why we\'re not shipping elks yet')
            print('You\'ve reached a feature which isn\'t implemented yet!')
    args = parser.parse_args()

    if args.version:
        version()
        exit(0)

    if args.subparser_name in modules:
        mod = import_module(args.subparser_name)
        try:
            mod.main(args)
        except NotImplementedError as e:
            print(e)
            print('\nThat must be why we\'re not shipping elks yet')
            print('You\'ve reached a feature which isn\'t implemented yet!')

def version():
    print('elks command line intermooface v%s' % VERSION)
    print('2016 46elks AB <hello@46elks.com>')

if __name__ == '__main__':
  main()
