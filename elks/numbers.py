import argparse
from elks.helpers import elksapi
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
            print('You must specify what number you wish to update with -n')
            return
        update_number(args, numbers[0])
    elif args.deactivate and args.number:
        deactivate(args, numbers[0])
    else:
        numberinfo(args, numbers)

def allocate_numbers(args):
    request = {}

    if args.number:
        request['number'] = args.number

    if args.country:
        request['country'] = args.country
    else:
        print('Please enter the desired 2 letter country-code for the country')
        print('where you wish to allocate your number.')
        request['country'] = input('Country (2 letter CC) > ')

    elksconn = elksapi(args, 'numbers', data = request)
    print(json_response)

def filter_numbers(args):
    numbers = elksapi(args, 'numbers')
    numbers = numbers['data']
    

    number_is_active = lambda n: not n.get('active', 'no') == 'no'

    if args.number:
        num_filter = lambda n: (n['number'] == args.number or
                n['id'] == args.number)
        numbers = list(filter(num_filter, numbers))

    if args.country:
        numbers = list(filter(lambda n: (n['country'].lower() ==
            args.country.lower()), numbers))

    if not args.all:
        numbers = list(filter(number_is_active, numbers))

    if not numbers:
        print('No numbers found.')
        if not args.all:
            print('Try again with `--all` for inactive numbers')
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
        if not args.short:
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

