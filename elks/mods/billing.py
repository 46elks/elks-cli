#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 46elks AB <hello@46elks.com>
# Developed in 2016 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
from elks.helpers import elksapi, parser_inject_generics

def main(args):
    response = elksapi(args, 'billing')
    user = elksapi(args, 'Me')
    billing_data = response['data']

    if args.id:
        billing_data = filter(lambda record: record['id'] == args.id,
            billing_data)
  
    if args.sum:
        show_summaries(billing_data, user)
    else:
        show_billing_rows(billing_data, user)

def parse_arguments(parser):
    parser.add_argument('id', nargs='?',
        help='Examine a specific billing row')
    parser.add_argument('--sum', action='store_true',
        help='Get an overview of where your credits are used')
    parser_inject_generics(parser)
    

def show_billing_rows(rows, user):
    for row in rows:
        print(row['id'])
        print('\tCreated: %s' % row['created'])
        print('\tReference: %s' % row['reference'])

        cost = row.get('cost')
        currency = user['currency']
        if cost:
            print('\tCost: %s' % format_sum(currency, cost))
        else:
            print('\tCost: None')
        
        if 'subaccount' in row:
            print('\tSubaccount: %s' % row['subaccount'])

def show_summaries(rows, user):
    categories = {}
    total = 0
    items = 0
    start_date = None
    end_date = None
    currency = None

    for row in rows:
        items += 1
        total += row['cost']
        if start_date:
            start_date = min(row['created'], start_date)
        else:
            start_date = row['created']
        if end_date:
            end_date = max(row['created'], end_date)
        else:
            end_date = row['created']
        if not currency:
            currency = user['currency']
        ref = row['reference']
        cat = ref.split('/')[1]
        if not cat in categories:
            categories[cat] = row['cost']
        else:
            categories[cat] += row['cost']

    percentage = lambda part: float(part)/float(total)*100.

    if not (start_date or end_date):
        print('No billing information found')
        return

    print('Statistics for %d billings between %s and %s' % (items,
        start_date[:10],
        end_date[:10]))

    category_list = []
    for category in categories:
        category_sum = format_sum(currency, categories[category])
        part_of_total = percentage(categories[category])
        print_category_row = '%-10s%s (%6.2f%%)' % ('%s' % category,
            category_sum,
            part_of_total
        )

        category_list.append((categories[category], print_category_row))

    category_list = sorted(category_list, key=lambda cat: -cat[0])
    for category in category_list:
        print(category[1])

    print('%-10s%s' % ('Total', format_sum(currency, total)))

def format_sum(currency, cost):
    return '%s %5d.%04d' % (currency, cost / 10000, cost % 10000)
