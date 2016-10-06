from __future__ import print_function
from elks.helpers import elksapi
from elks.formatting import kv_print, credits_to_currency

def main(args):
    response = elksapi(args, 'me')
    if not args.subaccount:
        print_user(response)
    else:
        from elks.elks import main as entrypoint
        entrypoint(['-a', args.subaccount, 'subaccounts', args.subaccount])

def parse_arguments(parser):
    pass

def print_user(user):
    print(user['displayname'], '|', user['email'], '|', user['mobilenumber'])
    kv_print('Id:', user['id'], indentlevel=0)
    if 'currency' in user:
        kv_print('Credits:',
            credits_to_currency(user.get('balance', 0), user['currency']),
            indentlevel=0
        )
        kv_print('Cost Type:', user.get('costtype'))
        if 'creditlimit' in user:
            kv_print('Creditlimit:',
                credits_to_currency(user.get('creditlimit', 0),
                    user['currency']),
            )
        if 'creditalert' in user:
            kv_print('Credit Alert level:',
                    credits_to_currency(user.get('creditalert', 0),
                        user['currency']),
                )
        kv_print('Invoicing:', user.get('invoicing'))
    else:
        print('Currency not set, please contact help@46elks.com to get started')
    kv_print('Restricted:', user.get('restricted'))
