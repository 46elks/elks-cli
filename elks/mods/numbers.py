#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 46elks AB <hello@46elks.com>
# Developed in 2016 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import argparse
from elks.helpers import elksapi, input_yes_no
import json
import readline
from time import sleep

import elkme.elks

def main(args):
    if args.new:
        allocate_numbers(args)
        # raise NotImplementedError('Cannot allocate number at this point')
        return

    numbers = filter_numbers(args)
    if not numbers:
        return

    if args.sms_url or args.mms_url or args.voice:
        if not args.number:
            print('Must select a specific number to update')
            return
        update_number(args, numbers[0])
    elif args.deactivate and args.number:
        for number in numbers:
            deactivate(args, number)
    elif args.deactivate:
        print('Select a specific number to deactivate')
        return
    else:
        numberinfo(args, numbers)

def allocate_numbers(args):
    request = {}
    capabilities = []

    if args.number:
        request['number'] = args.number

    if args.country:
        request['country'] = args.country
    else:
        print('Please enter the desired 2 letter country-code for the country')
        print('where you wish to allocate your number.')
        request['country'] = input('Country (2 letter CC) > ')

    opt_sms = input_yes_no('Do you need SMS support?', True)
    opt_mms = input_yes_no('Do you need MMS support?', False)
    opt_voice = input_yes_no('Do you need voice support?', True)

    if opt_sms:
        capabilities.append('sms')
    if opt_mms:
        capabilities.append('mms')
    if opt_voice:
        capabilities.append('voice')

    request['capabilities'] = ','.join(capabilities)

    json_response = elksapi(args, 'numbers', data = request)
    numberinfo(args, [json_response])

def filter_numbers(args):
    numbers = elksapi(args, 'numbers')
    numbers = numbers['data']

    number_is_active = lambda n: not n.get('active', 'no') == 'no'

    if args.number:
        num = args.number
        if ',' in args.number:
            num = args.number.split(',')
        num_filter = lambda n: (n['number'] in num or n['id'] in num)
        numbers = list(filter(num_filter, numbers))
        if len(numbers) > 0 and numbers[0]['id'] == args.number:
            args.all = True # If matched by id, show even when deactivated

    if args.country:
        numbers = list(filter(lambda n: (n['country'].lower() ==
            args.country.lower()), numbers))

    if not args.all and not args.inactive:
        numbers = list(filter(number_is_active, numbers))

    if args.inactive:
        numbers = list(filter(lambda n: not number_is_active(n), numbers))

    if not numbers:
        print('No numbers found.')
        if not args.all:
            print('Try again with `--inactive` to show inactive numbers')
        return
    return numbers

def update_number(args, number):
    update = {}
    if args.sms_url:
        update['sms_url'] = args.sms_url
    if args.mms_url:
        update['mms_url'] = args.mms_url
    if args.voice:
        update['voice_start'] = args.voice
    try:
        response = elksapi(args,
            endpoint='numbers/%s' % number['id'],
            data=update)
    except:
        print('Something went wrong')
        return
    print('Updated %s' % number['number'])

def deactivate(args, number):
    try:
        response = elksapi(args,
            endpoint='numbers/%s' % number['id'],
            data={'active': 'no'})
    except:
        print('Something went wrong')
        return
    print('Deactivated number %s' % number['number'])

def numberinfo(args, numbers):
    for number in numbers:
        print(number['number'])
        if not args.summary:
            print('\tIdentifier: %s' % number.get('id'))
            print('\tAllocated: %s' % number.get('allocated'))
            if 'deallocated' in number:
                print('\tDeallocated: %s' % number['deallocated'])
            print('\tCapabilities: %s' % ", ".join(
                number.get('capabilities', ['None'])
            ))
            print('\tCountry: %s' % number.get('country', 'None').upper())
            print('\tActive: %s' % number.get('active', 'Unknown'))
            if 'capabilities' in number:
                if 'sms' in number['capabilities']:
                    print('\tSMS URL: %s' % number.get('sms_url'))
                if 'mms' in number['capabilities']:
                    print('\tMMS URL: %s' % number.get('mms_url'))
                if 'voice' in number['capabilities']:
                    print('\tVoice start: %s' % number.get('voice_start'))

def parse_arguments(parser):
    parser.add_argument('-a', '--all', action='store_true',
            help='Show all numbers, even deactivated')
    parser.add_argument('--inactive', action='store_true',
            help='Show deactivated numbers only')
    parser.add_argument('-s', '--summary', action='store_true',
            help='Show only number')
    parser.add_argument('number', nargs='?',
            help='Select a specific number or number id')
    parser.add_argument('--sms_url', '--sms',
            help='Try to set a new SMS URL for the number')
    parser.add_argument('--mms_url', '--mms',
            help='Try to set a new MMS URL for the number')
    parser.add_argument('--voice', '--voice_start',
            help='Try to set an action to perform on voice start')
    parser.add_argument('--deactivate', action='store_true',
            help='Deactivate the choosen number [WARNING. DESTRUCTIVE]')
    parser.add_argument('--country', metavar='CC',
            help='Limit selection to country with country code CC')

    parser.add_argument('--new', action='store_true',
            help='Try to activate a new number')

