#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 46elks AB <hello@46elks.com>
# Developed in 2016 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License

import sys
import argparse
import elks.__init__
VERSION = elks.__init__.__version__

modules = sorted([
    'billing',
    'images',
    'list-calls',
    'list-sms',
    'new-sms',
    'numbers',
    'recordings',
    'status',
    'subaccounts'
])

modules_help = """\
Communication
    numbers         Manage your 46elks numbers
    list-sms        Display incoming and outgoing SMS
    new-sms         Create and send a new outgoing SMS
    list-calls      List voice calls for your 46elks numbers

Media
    recordings      List and listen to recordings
    images          List and display image attachments

Account management
    billing         See the billing history of your 46elks account
    subaccounts     Manage your 46elks subaccounts
    status          Information about your 46elks account (including balance)
"""

def import_module(mod):
    elks = __import__('elks.%s' % mod)
    return getattr(elks, mod)

def main(argv):
    global modules
    parser = argparse.ArgumentParser(prog='elks',
            description=modules_help,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--version', action='store_true',
        help='Display elks version')
    parser.add_argument('-c', '--config', dest='configfile',
        help='Location of elks/elkme conffile'),
    parser.add_argument('-a', '--subaccount',
        help='Subaccount to use for the request')
    parser.add_argument('--donotpost', action='store_true',
        help='Will try to not do anything costly with your account')
    subparsers = parser.add_subparsers(help='Sub-commands',
        dest='subparser_name')
    for module in modules:
        mod = import_module(module)
        try:
            mod.parse_arguments(subparsers.add_parser(module))
        except NotImplementedError as e:
            print(e)
            print('\nThat must be why we\'re not shipping elks yet')
            print('You\'ve reached a feature which isn\'t implemented yet!')
    args = parser.parse_args(argv)

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

def run():
    argv = sys.argv[1:]
    main(argv)

if __name__ == '__main__':
    run()
