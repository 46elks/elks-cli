import math
import json
import subprocess
from elks.helpers import (
    elksapi,
    parser_inject_generics,
    elks_store_media
)

from elks.formatting import kv_print, bytes_to_human

descr = """\
This module displays information about images stored within 46elks
and makes it possible to downlaod and manage single images"""

def main(args):
    #raise NotImplementedError('Images subsystem is not yet done')

    if args.image_id:
        response = [elksapi(args, 'images/%s' % args.image_id)]
        if args.open:
            image_src = 'images/%s.jpg' % args.image_id
            filetype = response[0].get('filetype', 'jpg')
            filedest = '/tmp/elks-%s.%s' % (args.image_id, filetype)
            elks_store_media(args, image_src, filedest)

            print('Opening image')
            # TODO Cross-platform and fix macOS playback
            subprocess.call(['open', filedest])
            print('Opened image')
            return
    else:
        response = elksapi(args, 'images')['data']
        if args.open:
            print('Cannot open multiple images. Please set image_id')
            exit(1)
    digests = []
    for image in response:
        if args.squash:
            if 'digest' not in image:
                pass
            elif image['digest'] in digests:
                continue
            else:
                digests.append(image['digest'])
        size = image.get('bytes')
        if args.pretty:
            size = bytes_to_human(size)

        kv_print('Identifier', image['id'], indentlevel=0)
        kv_print('Created', image.get('created'))
        kv_print('MMS', image.get('mmsid'))
        kv_print('Digest', image.get('digest'))
        kv_print('Filetype', image.get('filetype'))
        kv_print('Size', size)

def parse_arguments(parser):
    parser.description = descr
    parser.add_argument('-p', '--pretty', action='store_true',
            help='Print human friendly numbers')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Print detailed information')
    parser.add_argument('--squash', action='store_true',
            help='Display a single image once only despite appearing multiple\
 times')
    parser.add_argument('image_id', nargs='?',
            help='Select a specific recording')
    parser.add_argument('--open', action='store_true',
            help='Try to play the selected recording')
    parser_inject_generics(parser)

