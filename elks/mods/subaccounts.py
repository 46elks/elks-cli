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
import re

def main(args):
    if args.usagelimit or args.active:
        update_subaccount(args)
    elif args.new:
        create_subaccount(args)
    else:
        list_subaccounts(args)

def create_subaccount(args):
    details = elksapi(args,
        endpoint='subaccounts',
        data={'name': args.new})
    print('Created subaccount %s with id %s' % (details['name'], details['id']))

def list_subaccounts(args, hide_secret=False):
    subaccounts = elksapi(args, endpoint='subaccounts')['data']
    me = elksapi(args, endpoint='me')
    currency = me.get('currency')

    if not subaccounts:
        print('Did not find any matching subaccounts')
        return

    if args.id:
        subaccounts = filter(lambda s: (s['id'] == args.id or
            s['name'] == args.id), subaccounts)
    elif args.all:
        pass
    elif args.show_inactive:
        subaccounts = filter(lambda s: (s.get('active') == 'no'), subaccounts)
    else:
        subaccounts = filter(lambda s: (s.get('active') != 'no'), subaccounts)

    subaccounts = list(subaccounts)

    for account in subaccounts:
        if args.short:
            print('%s %s' % (account.get('name', 'Unnamed'), account['id']))
        else:
            usagelimit = account.get('usagelimit')
            if usagelimit != None and args.pretty:
                usagelimit = credits_to_currency(usagelimit, currency)
            balanceused = account.get('balanceused', 0)
            if args.pretty:
                balanceused = credits_to_currency(balanceused, currency)

            print(account.get('name', 'Unnamed'))
            kv_print('Identifier', account['id'])
            kv_print('Active', account.get('active', 'yes'))
            if not hide_secret:
                kv_print('Secret', account.get('secret'))
            kv_print('Created', account.get('created', 'Unknown'))
            kv_print('Currency', account.get('currency'))
            kv_print('Usagelimit', usagelimit, show_empty=True)
            kv_print('Balance Used', balanceused,
                show_empty=True)

def update_subaccount(args):
    if not args.id:
        print('Updating requires you to specify a subaccount by id')

    query = {}
    if args.active:
        query['active'] = args.active
    elif args.usagelimit != None:
        usagelimit = args.usagelimit.strip().lower()
        if re.match(r'[+-]?\d+|none', usagelimit):
            if usagelimit[0] in ['+', '-']:
                curr_ul = elksapi(args,
                        endpoint='subaccounts/{}'.format(
                            args.id
                        )).get('usagelimit')
                if curr_ul and usagelimit[0] == '+':
                    usagelimit = str(curr_ul + int(usagelimit[1:]))
                elif curr_ul and usagelimit[0] == '-':
                    usagelimit = str(curr_ul - int(usagelimit[1:]))
            query['usagelimit'] = usagelimit
        else:
            print('Usagelimit must be an integer or literal \'none\'')
            return

    if not query:
        print('Updated nothing')
        return

    try:
        response = elksapi(args, endpoint='subaccounts/%s' % args.id,
                data=query)
    except Exception as e:
        print('Failed updating subaccount')
        print(e)
        return
    list_subaccounts(args, hide_secret=True)

def parse_arguments(parser):
    parser.add_argument('id', nargs='?',
            help='Act only on the subaccounts with matching id or name')
    parser.add_argument('--new', metavar='NAME',
            help='Create a new subaccount')
    parser.add_argument('-s', '--short', action='store_true',
            help='Display single-row information on every subaccount')
    parser.add_argument('--active', choices=['yes', 'no'],
            help='Activate a disabled account')
    parser.add_argument('--all', action='store_true',
            help='Show all subaccounts, including deactivated')
    parser.add_argument('--show-inactive', action='store_true',
            help='Show only inactive accounts')
    parser.add_argument('--usagelimit', type=str,
            help='Set the new usagelimit of the subaccount (requires id)')
