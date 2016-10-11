#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 46elks AB <hello@46elks.com>
# Developed in 2016 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import sys
import argparse
import importlib
import elks.mods
import elks.__init__
import signal
VERSION = elks.__init__.__version__

modules = sorted([
    'billing',
    'images',
    'calls',
    'numbers',
    'recordings',
    'setup',
    'sms',
    'status',
    'subaccounts'
])

modules_help = """\
Communication
    numbers         Manage your 46elks numbers
    sms             List and compose SMS
    calls           List and make voice calls

Media
    recordings      List and listen to recordings
    images          List and display image attachments

Account management
    billing         See the billing history of your 46elks account
    subaccounts     Manage your 46elks subaccounts
    status          Information about your 46elks account (including balance)
"""

def main(argv):
    global modules
    parser = argparse.ArgumentParser(prog='elks',
            description=modules_help,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--version', action='store_true',
        help='Display elks version')
    parser.add_argument('-p', '--pretty', action='store_true',
            help='Print human friendly numbers')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Print detailed information')
    parser.add_argument('-c', '--config', dest='configfile',
        help='Location of elks/elkme conffile'),
    parser.add_argument('-a', '--subaccount',
        help='Subaccount to use for the request')
    parser.add_argument('--donotpost', action='store_true',
        help='Will try to not do anything costly with your account')
    subparsers = parser.add_subparsers(help='Commands',
        dest='subparser_name')
    for module in modules:
        mod = importlib.import_module('.%s' % module, 'elks.mods')
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
        mod = importlib.import_module('.%s' % args.subparser_name, 'elks.mods')
        try:
            mod.main(args)
        except NotImplementedError as e:
            print(e)
            print('\nThat must be why we\'re not shipping elks yet')
            print('You\'ve reached a feature which isn\'t implemented yet!')
        except Exception as e:
            exctype, value = sys.exc_info()[:2]
            arguments = ''
            if len(sys.argv) > 1:
                arguments = map(lambda x: '"%s"' % x if ' ' in x else x,
                        sys.argv[1:])
                arguments = ' '.join(arguments)
            print('--8>-------------------------------------------------8<--',
                    file=sys.stderr)
            print('Called %s with arguments `elks %s`' % (mod.__name__,
                arguments),
                    file=sys.stderr)
            print('%s:' % exctype.__name__, value, file=sys.stderr)
            print(('==========\nThis is a bug in elks. Please report at '
                'https://github.com/46elks/elks/issues\n'
                'or directly to emil@46elks.com'), file=sys.stderr)
            print('--8>-------------------------------------------------8<--',
                    file=sys.stderr)
    else:
        parser.print_help()
        sys.exit(2)

def version():
    print('elks command line intermooface v%s' % VERSION)
    print('2016 46elks AB <hello@46elks.com>')

def run():
    argv = sys.argv[1:]
    main(argv)

ctrlc = False

def ctrlc_handler(signal, frame):
    global ctrlc
    if ctrlc:
        print('')
        sys.exit(0)
    else:
        ctrlc = True
        print('\nctrl+c detected, press again to force quit', file=sys.stderr)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, ctrlc_handler)
    run()
