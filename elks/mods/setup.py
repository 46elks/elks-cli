#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 46elks AB <hello@46elks.com>
# Developed in 2016 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
import elkme.config
import sys

def parse_arguments(parser):
    parser.description = ('Setup your 46elks account (interactive)')

def main(args):
    if sys.version_info < (3,):
        print('elks setup is currently not available for Python 2.x 😞')
        exit(-1)

    print('Setup elks and elkme account')
    print(('Log in to https://dashboard.46elks.com/ and copy your '
        'API username and password\n'))
    username = input('API username > ')
    password = input('API password > ')

    if args.configfile:
        conffile = os.path.expanduser(args.configfile)
    else:
        conffile = elkme.config.default_config_location()

    conf = elkme.config.read_config(conffile)

    if username:
        conf['username'] = username
    if password:
        conf['password'] = password

    try:
        with open(conffile, 'w') as fdest:
            settings = elkme.config.generate_config(conf)
            settings.write(fdest)
    except IOError as e:
        print(e)

