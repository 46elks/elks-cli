#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 46elks AB <hello@46elks.com>
# Developed in 2016 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from elks.helpers import (
    elksapi, 
    parser_inject_generics
)

from elks.formatting import kv_print, duration_to_human

descr = """\
Lists calls"""

def main(args):
    query = {}
    response = elksapi(args, 'calls', query = query)
    for call in response['data']:
        if args.pretty:
            call['duration'] = duration_to_human(call.get('duration', 0))
        else:
            call['duration'] = call.get('duration', 0)
        pretty_print_call(call)

def parse_arguments(parser):
    parser.description = descr
    parser.add_argument('-p', '--pretty', action='store_true')
    parser_inject_generics(parser)

def pretty_print_call(call):
    print(call['id'])
    kv_print('Created:', call.get('created'))
    kv_print('Duration:', call['duration'])
    kv_print('Direction:', call.get('direction', 'Unknown'))
    kv_print('From:', call.get('from'))
    kv_print('To:', call.get('to'))
    kv_print('State:', call.get('state'))
    kv_print('Actions:', call.get('actions'))
    if 'legs' in call:
        kv_print('Legs:', call['legs'])
    if 'recordings' in call:
        print('\tRecordings:')
        for recording in call['recordings']:
            kv_print('Recording', recording, indentlevel = 2)
