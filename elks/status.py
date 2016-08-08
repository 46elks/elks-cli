from elks.helpers import elksapi

def main(args):
    response = elksapi(args, 'me')
    print(response)

def parse_arguments(parser):
    pass
