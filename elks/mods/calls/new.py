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

def parse_arguments(parser):
    parser.description = ('Initialize new outgoing call')
    parser.add_argument('-t', '--to',
            help='Call this phone')
    parser.add_argument('-f', '--from', dest='sender',
            help='Call from this phone number')
    parser.add_argument('data', nargs='*',
            help='46elks JSON structure for calls')

def main(args):
    if not args.data:
        print('Missing 46elks call JSON')
        return

    config = read_conf(args)

    payload = {
        'to': args.to or config['to'],
        'from': args.sender or config['callfrom'] or config['from'],
        'voice_start': parse_voice(args.data)
    }
    try:
        response = elksapi(args,
            endpoint='calls',
            data=payload)
    except:
        print('Something went wrong')
        return
    print('Called %s executing %s from %s' % (
          payload['to'],
          payload['voice_start'],
          payload['from'])
    )

def parse_voice(payload):
    if not isinstance(payload, str):
        payload = ' '.join(payload)

    try:
        json.loads(payload)
    except ValueError:
        payload = payload.strip()
        kv = payload.split(' ', 1)
        if len(kv) > 1:
            payload = '{"%s": "%s"}' % (kv[0], kv[1])
        else:
            payload = '%s' % kv[0]

    return payload

