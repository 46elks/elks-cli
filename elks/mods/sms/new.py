#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 46elks AB <hello@46elks.com>
# Developed in 2016 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from elks.helpers import elksapi, read_conf
import json
import sys

def main(args):
    if not args.message:
        print('Usage: elks sms new -t +46700000000 -f elks <MESSAGE>',
            file=sys.stderr)
        return

    config = read_conf(args)
    payload = {
        'to': args.to or config.get('to'),
        'from': args.sender or config.get('from'),
        'message': args.message
    }

    if not isinstance(payload['message'], str):
        payload['message'] = " ".join(payload['message'])

    response = elksapi(args,
        endpoint='sms',
        data=payload)
    print('Sent SMS to %s containing the message "%s" from %s' % (
          payload['to'],
          payload['message'],
          payload['from'])
    )


def parse_arguments(parser):
    parser.description = ('Send SMS\n\n'
            'Send SMS using the elks command-line interface. Use `elkme` for '
            '\n all features')
    parser.add_argument('-t', '--to',
            help='Call this phone')
    parser.add_argument('-f', '--from', dest='sender',
            help='Call from this phone number')
    parser.add_argument('message', metavar='message', type=str, nargs='*',
            help='Message to be sent')

