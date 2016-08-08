from elks.helpers import elksapi, parser_inject_generics

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
    print('%s %s \u2192 %s' % (sms['direction'], sms['from'], sms['to']))
    if summary:
        return

    print('\tCreated: %s' % sms['created'])
    print('\tSMS id: %s' % sms['id'])
    print('\tDirection: %s' % sms['direction'])
    print('\tSender: %s' % sms['from'])
    print('\tRecipient: %s' % sms['to'])
    if 'status' in sms:
        print('\tStatus: %s' % sms['status'])
    if 'delivered' in sms:
        print('\tDelivered on: %s' % sms['delivered'])
    if 'cost' in sms:
        print('\tCost: %s' % sms['cost'])
    if 'parts' in sms:
        print('\tParts: %s' % sms['parts'])
    if 'flashsms' in sms:
        print('\tFlash SMS: %s' % sms['flashsms'])
    if 'message' in sms:
        print('\tMessage: %s' % sms['message'])

