#
from elks.helpers import elksapi, parser_inject_generics
from elks.formatting import kv_print

descr = """\
Displays your incoming and outgoing SMS"""

def main(args):
    query = {}
    if args.to:
        query['to'] = args.to
    response = elksapi(args, 'sms', query = query)
    for sms in response['data']:
        pretty_print_sms(sms, args.summary)

def parse_arguments(parser):
    parser.description = descr
    parser.add_argument('-s', '--summary', action='store_true',
        help='Get an overview of where your credits are used')
    parser.add_argument('--to', help='Filter on recipient')
    parser_inject_generics(parser)

def pretty_print_sms(sms, summary = False):
    print(u'%s %s \u2192 %s' % (sms['direction'], sms['from'], sms['to']))

    if summary:
        return
    kv_print('Created:', sms['created'])
    kv_print('SMS id:', sms['id'])
    kv_print('Direction:', sms['direction'])
    kv_print('Sender:', sms['from'])
    kv_print('Recipient:', sms['to'])
    kv_print('Status:', sms.get('status'))
    kv_print('Delivered on:', sms.get('delivered'))
    kv_print('Cost:', sms.get('cost'))
    kv_print('Parts:', sms.get('parts'))
    kv_print('Flash SMS:', sms.get('flashsms'))
    kv_print('Message:', sms.get('message'))

