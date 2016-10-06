from elks.helpers import elksapi, parser_inject_generics

def main(args):
    response = elksapi(args, 'billing')
    billing_data = response['data']

    if args.id:
        billing_data = filter(lambda record: record['id'] == args.id,
            billing_data)
  
    if args.sum:
        show_summaries(billing_data)
    else:
        show_billing_rows(billing_data)

def parse_arguments(parser):
    parser.add_argument('id', nargs='?',
        help='Examine a specific billing row')
    parser.add_argument('--sum', action='store_true',
        help='Get an overview of where your credits are used')
    parser_inject_generics(parser)
    

def show_billing_rows(rows):
    for row in rows:
        print(row['id'])
        print('\tCreated: %s' % row['created'])
        print('\tReference: %s' % row['reference'])

        cost = row.get('cost')
        if cost:
            print('\tCost: %s' % format_sum(row['currency'], cost))
        else:
            print('\tCost: None')
        
        if 'subaccount' in row:
            print('\tSubaccount: %s' % row['subaccount'])

def show_summaries(rows):
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
            currency = row['currency']
        ref = row['reference']
        cat = ref.split('/')[1]
        if not cat in categories:
            categories[cat] = row['cost']
        else:
            categories[cat] += row['cost']

    percentage = lambda part: part/total*100.

    if not (start_date or end_date):
        print('No billing information found')
        return

    print('Statistics for %d billings between %s and %s' % (items,
        start_date[:10],
        end_date[:10]))

    for category in categories:
        print('%-10s%s (%6.2f%%)' % ('%s' % category,
            format_sum(currency, categories[category]),
            percentage(categories[category])))

    print('%-10s%s' % ('Total', format_sum(currency, total)))

def format_sum(currency, cost):
    return '%s %5d.%04d' % (currency, cost / 10000, cost % 10000)
