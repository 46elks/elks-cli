import argparse

descr = """\
SMS module is not yet implemented.
You should try out the `elkme` command though. It\'s already installed!"""

def main(args):
    raise NotImplementedError(descr)

def parse_arguments(parser):
    parser.description = descr

