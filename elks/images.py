import math
import json
import subprocess
import os
from elks.helpers import (
    elksapi,
    parser_inject_generics,
    kv_print,
    elks_download_media
)

descr = """\
Handle phone call recordings"""

def main(args):
    raise NotImplementedError('Images subsystem is not yet done')

    if args.image_id:
        response = [elksapi(args, 'images/%s' % args.recording_id)]
        if args.open:
            pretty_print_recording(response[0], pretty = args.pretty)
            print('Downloading image')
            image = elks_download_media(args,
                'recordings/%s.jpg' % args.image_id)
            filedest = '/tmp/elks-%s.jpg' % args.image_id
            with open(filedest, 'w') as f:
                f.write(wav)
            print('Downloaded image')

            print('Opening image')
            # TODO Cross-platform and fix macOS playback
            subprocess.call(['open', filedest])
            print('Opened image')
            os.remove(filedest)
            return
    else:
        response = elksapi(args, 'images')['data']
        if args.open:
            print('Cannot open multiple images. Please set image_id')
            exit(1)
    for image in response:
        print(image)

def parse_arguments(parser):
    parser.description = descr
    parser.add_argument('-p', '--pretty', action='store_true',
            help='Print human friendly numbers')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Print detailed information')
    parser.add_argument('image_id', nargs='?',
            help='Select a specific recording')
    parser.add_argument('--open', action='store_true',
            help='Try to play the selected recording (PRETTY MUCH BROKEN)')
    parser_inject_generics(parser)

def bytes_to_human(size):
    si_bytes = ('B', 'kB', 'MB', 'GB', 'TB', 'PB', 'ZB', 'YB')
    si_magnitude = int(math.floor(math.log10(size)) / 3)
    return '%.2f %s' % (size / pow(10, si_magnitude*3), si_bytes[si_magnitude])

def duration_to_human(length):
    seconds = length % 60
    minutes = length / 60
    hours = minutes / 60
    return '%dh%dm%ds' % (hours, minutes, seconds)

