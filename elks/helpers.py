import elkme.config
import json
import sys
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
    if args.configfile:
        conffile = os.path.expanduser(args.configfile)
    else:
        conffile = elkme.config.default_config_location()

    conf = elkme.config.read_config(conffile)
    return (conf.get('username'), conf.get('password'))

def open_elksconn(args):
    """ Create a connection class to 46elks and return it """
    return elkme.elks.Elks(get_auth(args))

def elks_download_media(args, endpoint):
    elksconn = elkme.elks.Elks()
    url = elksconn.api_url % endpoint

    res = requests.get(
        url,
        auth = get_auth(args)
    )

    return res.text

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
    rv= elksconn.query_api(endpoint=url, data = data)
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
    """ Get month and year information """
    date = datetime.now()
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)

    if args.year:
        date = date.replace(year=args.year)
        if not args.month:
            end = date.replace(month = 1)
            start = date.replace(month = 12)
    if args.month:
        if args.month == months[0]:
            date = date.replace(day = 1)
        else:
            new_month = months.index(args.month)
            if new_month > date.month and not args.year:
                date = date.replace(year = date.year - 1)
            date = date.replace(month=new_month, day = 1)

        end = date
        start = date.replace(month=date.month % 12 + 1) + timedelta(seconds=-1)
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

def kv_print(key, value, indentlevel = 1):
    tabular = '\t' * indentlevel
    print('%s%-10s %-20s' % (tabular, key, value))
