from elks.helpers import (
    elksapi, 
    parser_inject_generics
)

from elks.formatting import kv_print

descr = """\
Lists calls"""

def main(args):
    query = {}
    response = elksapi(args, 'calls', query = query)
    for call in response['data']:
        pretty_print_call(call)

def parse_arguments(parser):
    parser.description = descr
    parser_inject_generics(parser)

def pretty_print_call(call):
    print(call.keys())
    print(call['id'])
    kv_print('Duration:', call.get('duration'))
