#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 46elks AB <hello@46elks.com>
# Developed in 2016 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from elks.helpers import elksapi
from elks.formatting import kv_print, credits_to_currency
import json

def main(args):
    if args.usagelimit:
        change_usagelimit(args)
    elif args.new:
        create_subaccount(args)
    else:
        list_subaccounts(args)

def create_subaccount(args):
    details = elksapi(args,
        endpoint='subaccounts',
        data={'name': args.new})
    print('Created subaccount %s with id %s' % (details['name'], details['id']))

def list_subaccounts(args):
    subaccounts = elksapi(args, endpoint='subaccounts')['data']
    me = elksapi(args, endpoint='me')
    currency = me.get('currency')

    if args.id:
        subaccounts = list(filter(lambda s: (s['id'] == args.id or
            s['name'] == args.id), subaccounts))

    if not subaccounts:
        print('Did not find any matching subaccounts')
        return

    for account in subaccounts:
        if args.short:
            print('%s %s' % (account.get('name', 'Unnamed'), account['id']))
        else:
            usagelimit = account.get('usagelimit')
            if usagelimit and args.pretty:
                usagelimit = credits_to_currency(usagelimit, currency)
            balanceused = account.get('balanceused', 0)
            if args.pretty:
                balanceused = credits_to_currency(balanceused, currency)

            print(account.get('name', 'Unnamed'))
            kv_print('Identifier', account['id'])
            kv_print('Secret', account.get('secret'))
            kv_print('Created', account.get('created', 'Unknown'))
            kv_print('Currency', account.get('currency'))
            kv_print('Usagelimit', usagelimit)
            kv_print('Balance Used', balanceused,
                show_empty=True)

def change_usagelimit(args):
    if not args.id:
        print('Setting usage limit requires you to specify a subaccount')

    try:
        response = elksapi(args, endpoint='subaccounts/%s' % args.id,
                data={'usagelimit': args.usagelimit})
    except Exception as e:
        print('Failed updating usagelimit')
        print(e)
        return
    print('Changed usagelimit on account %s to %s' % (response.get('name'),
        response.get('usagelimit')))

def parse_arguments(parser):
    parser.add_argument('id', nargs='?',
            help='Act only on the subaccounts with matching id or name')
    parser.add_argument('--new', metavar='NAME',
            help='Create a new subaccount')
    parser.add_argument('-s', '--short', action='store_true',
            help='Display single-row information on every subaccount')
    parser.add_argument('--usagelimit', type=int,
            help='Set the new usagelimit of the subaccount (requires id)')
