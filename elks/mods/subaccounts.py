from elks.helpers import elksapi
import json

def main(args):
    if args.usagelimit:
        change_usagelimit(args)
    elif args.new:
        create_subaccount(args)
    else:
        list_subaccounts(args)

def create_subaccount(args):
    details = elksapi(args,
        endpoint='subaccounts',
        data={'name': args.new})
    print('Created subaccount %s with id %s' % (details['name'], details['id']))

def list_subaccounts(args):
    subaccounts = elksapi(args, endpoint='subaccounts')['data']

    if args.id:
        subaccounts = list(filter(lambda s: (s['id'] == args.id or
            s['name'] == args.id), subaccounts))
    
    if not subaccounts:
        print('Did not find any matching subaccounts')
        return

    for account in subaccounts:
        if args.short:
            print('%s %s' % (account.get('name', 'Unnamed'), account['id']))
        else:
            print(account.get('name', 'Unnamed'))
            print('\tIdentifier: %s' % account['id'])
            print('\tSecret: %s' % account.get('secret'))
            print('\tCreated: %s' % account.get('created', 'Unknown'))
            print('\tUsagelimit: %s' % account.get('usagelimit'))
            print('\tBalance Used: %s' % account.get('balanceused'))

def change_usagelimit(args):
    if not args.id:
        print('Setting usage limit requires you to specify a subaccount')

    try:
        response = elksapi(args, endpoint='subaccounts/%s' % args.id,
                data={'usagelimit': args.usagelimit})
    except Exception as e:
        print('Failed updating usagelimit')
        print(e)
        return
    print('Changed usagelimit on account %s to %s' % (response.get('name'),
        response.get('usagelimit')))

def parse_arguments(parser):
    parser.add_argument('id', nargs='?',
            help='Act only on the subaccounts with matching id or name')
    parser.add_argument('--new', metavar='NAME',
            help='Create a new subaccount')
    parser.add_argument('-s', '--short', action='store_true',
            help='Display single-row information on every subaccount')
    parser.add_argument('--usagelimit', type=int,
            help='Set the new usagelimit of the subaccount (requires id)')
