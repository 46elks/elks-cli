#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 46elks AB <hello@46elks.com>
# Developed in 2016 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
from elks.helpers import (elksapi,
        parser_inject_generics,
        pretty_time)

from elks.formatting import (kv_print, credits_to_currency)

def main(args):
    response = elksapi(args, 'transactions')
    user = elksapi(args, 'Me')
    transactions = response['data']

    if args.id:
        transactions = filter(lambda record: record['id'].startswith(args.id),
            transactions)

    if args.sum:
        show_summaries(transactions, user)
    else:
        show_transaction_rows(transactions, user)

def parse_arguments(parser):
    parser.add_argument('id', nargs='?',
        help='Examine a specific billing row')
    parser.add_argument('--sum', action='store_true',
        help='Get an overview of where your credits are used')
    parser_inject_generics(parser)

def show_transaction_rows(transactions, user):
    currency = user.get('currency', '???')
    for event in transactions:
        print(event['id'])
        print('\t{}'.format(event.get('details')))
        kv_print('Created',
                pretty_time(
                    event.get('created', '1970-01-01T00:00:00.00000')))
        kv_print('Sum',
                credits_to_currency(
                    event.get('amount', 0), currency))

def show_summaries(transactions, user):
    currency = user.get('currency', '???')
    total = 0
    items = 0
    start_date = None
    end_date = None

    for event in transactions:
        items += 1
        total += event.get('amount', 0)
        start_date = (min(event['created'], start_date)
                if start_date else event['created'])
        end_date = (max(event['created'], end_date)
                if end_date else event['created'])

    if items == 0:
        print("No transactions for the given time period")
    elif items == 1:
        print("1 transaction on {}".format(pretty_time(start_date)))
    else:
        print("{} transactions between {} and {}".format(
            items, pretty_time(start_date), pretty_time(end_date)))

    print("Transaction sum for the period:\n\t{}".format(
        credits_to_currency(total, currency)))
