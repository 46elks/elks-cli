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
    if args.usagelimit or args.active or args.secret:
        update_subaccount(args)
    elif args.new:
        create_subaccount(args)
    else:
        list_subaccounts(args)

def get_subaccounts(args):
    subaccounts = elksapi(args, endpoint='subaccounts')['data']

    if not subaccounts:
        raise Exception('Did not find any matching subaccounts')

    if args.id:
        subaccounts = filter(lambda s: (s['id'] == args.id or
            s['name'] == args.id), subaccounts)
    return subaccounts

def create_subaccount(args):
    details = elksapi(args,
        endpoint='subaccounts',
        data={'name': args.new})
    print('Created subaccount %s with id %s' % (details['name'], details['id']))

def list_subaccounts(args, hide_secret=False):
    try:
        subaccounts = get_subaccounts(args)
    except Exception as e:
        print(e)
        return
    me = elksapi(args, endpoint='me')
    currency = me.get('currency')

    if args.all:
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

    try:
        accs = get_subaccounts(args)
    except Exception as e:
        print(e)
        return
    if len(accs) < 1:
        print('Multiple subaccounts matched :(')
        return
    args.id = accs[0].get('id')
    curr_ul = accs[0].get('usagelimit')
    balance_used = accs[0].get('balanceused')

    query = {}
    if args.active:
        query['active'] = args.active
    
    if args.usagelimit != None:
        usagelimit = args.usagelimit.strip().lower()
        if re.match(r'[+-:.]?\d+|none', usagelimit):
            if usagelimit[0] in '+-:.':
                if curr_ul and usagelimit[0] == '+':
                    usagelimit = str(curr_ul + int(usagelimit[1:]))
                elif curr_ul and usagelimit[0] == '-':
                    usagelimit = str(curr_ul - int(usagelimit[1:]))
                elif balance_used and usagelimit[0] == '.':
                    new_ul = balance_used + int(usagelimit[1:])
                    usagelimit = str(max(new_ul, curr_ul))
                elif balance_used and usagelimit[0] == ':':
                    usagelimit = str(balance_used + int(usagelimit[1:]))
                elif usagelimit[0] in ':.':
                    usagelimit = usagelimit[1:]
            query['usagelimit'] = usagelimit
        else:
            print('Usagelimit must be an integer or literal \'none\'')
            return
    
    if args.secret:
        query['secret'] = args.secret

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
    parser.add_argument('--usagelimit', metavar='LIMIT', type=str,
            help="""Set the new usagelimit of the subaccount (requires id).
            Set to "none" to unset the usage limit. You may add to the current
            limit by writing '+<sum>', subtract by writing '-<sum>'
            where <sum> is a positive integer. You may also use ':<sum>' to
            set the usagelimit to (balance used + <sum>) or '.<sum>' to set the
            usagelimit to the greatest of (balance used + <sum>) and current
            usagelimit
            """)
    parser.add_argument('--secret',
            help='Set new secret')
