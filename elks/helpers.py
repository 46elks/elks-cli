import elkme.config
import elkme.elks
import json
import sys
import os
import requests

from urllib.parse import urlencode
from argparse import ArgumentParser
from datetime import datetime, timedelta

months = ['now', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep',
          'oct', 'nov', 'dec']
years = range(2011, datetime.now().year+1)

timeformat = lambda t: t.strftime('%Y-%m-%dT%H:%M:%S.%f')

def get_auth(args):
    """ Get the elkme 46elks authentication details in a requests
        friendly format """
    conf = read_conf(args)
    auth = (conf.get('username'), conf.get('password'))
    if args.subaccount:
        elksconn = elkme.elks.Elks(auth, api_url = get_api_url(args))
        url = '/Subaccounts/%s' % args.subaccount
        subaccount = elksconn.query_api(endpoint=url)
        subaccount = json.loads(subaccount)
        auth = (args.subaccount, subaccount['secret'])
    return auth

def get_api_url(args):
    return read_conf(args).get('api_url')

def read_conf(args):
    if args.configfile:
        conffile = os.path.expanduser(args.configfile)
    else:
        conffile = elkme.config.default_config_location()

    conf = elkme.config.read_config(conffile)
    return conf

def open_elksconn(args):
    """ Create a connection class to 46elks and return it """
    return elkme.elks.Elks(get_auth(args), api_url = get_api_url(args))

def elks_download_media(args, endpoint):
    elksconn = open_elksconn(args)
    url = elksconn.api_url % endpoint

    res = requests.get(
        url,
        auth = get_auth(args)
    )

    return res.content

def elks_store_media(args, endpoint, destination):
    print('[Downloading...]')
    image = elks_download_media(args, endpoint)
    with open(destination, 'wb') as f:
        f.write(image)
    print('[Downloaded]')

def elksapi(args, endpoint, query = {}, data = None):
    """ Access a specific endpoint for the 46elks API in a
        object format. Supports fetching everything between
        two dates and any number 1-10 000 elements"""
    elksconn = open_elksconn(args)
    try:
        if args.limit:
            query['limit'] = args.limit
        elif args.month or args.year:
            query['end'], query['start'] = format_date(args)
    except AttributeError:
        pass
    if query.keys():
        url = '%s?%s' % (endpoint, urlencode(query))
    else:
        url = endpoint
    if data and args.donotpost:
        raise Exception('Attempted POST request with donotpost flag. Aborting')
    rv = elksconn.query_api(endpoint=url, data = data)
    rv = json.loads(rv)
    response = rv
    if 'data' in rv:
        rv['data'] = reversed(rv['data'])
    if not 'limit' in query and 'end' in query:
        rv['data'] = list(rv['data'])
        while ('next' in response and
               response['next'] < query.get('start',
                   timeformat(datetime.now()))):
            query['start'] = response['next']
            url = '%s?%s' % (endpoint, urlencode(query))
            response = json.loads(elksconn.query_api(endpoint=url))
            for item in response['data']:
                rv['data'].insert(0, item)
    return rv

def format_date(args):
    """ Read the list of arguments and creates the date range for the
    specified month/year
    """
    date = datetime.now()
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)

    if args.year:
        date = date.replace(year=args.year)
        if not args.month:
            end = date.replace(month = 1, day = 1)
            start = date.replace(
                month = 12,
                day = 31,
                hour = 23,
                minute = 59,
                second = 59,
                microsecond = 999999)
    if args.month:
        if args.month == months[0]: # 'now'
            date = date.replace(day = 1)
        else:
            new_month = months.index(args.month)

            # If month hasn't started yet this year, assume last year
            if new_month > date.month and not args.year:
                date = date.replace(year = date.year - 1)
            date = date.replace(month=new_month, day = 1)

        end = date

        # Fetch last second of month
        start = date.replace(month=date.month % 12 + 1) + timedelta(seconds=-1)
        # Iff december, previous line causes year to be last year
        if date.month == 12:
            start = start.replace(year=start.year + 1)
    return (timeformat(end), timeformat(start))

def parser_inject_generics(parser):
    parser.add_argument('--limit', type=int,
        help='Set maximum number of items to fetch')
    parser.add_argument('--month', choices=months,
        help='Examine objects for a specific month')
    parser.add_argument('--year', choices=years, type=int,
        help='Examine objects for a specific year')

