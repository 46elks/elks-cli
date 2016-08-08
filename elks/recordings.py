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
    if args.recording_id:
        response = [elksapi(args, 'recordings/%s' % args.recording_id)]
        if args.play:
            pretty_print_recording(response[0], pretty = args.pretty)
            print('Downloading recording')
            wav = elks_download_media(args,
                'recordings/%s.wav' % args.recording_id)
            filedest = '/tmp/elks-%s.wav' % args.recording_id
            with open(filedest, 'w') as f:
                f.write(wav)
            print('Downloaded recording')

            print('Playing recording')
            # TODO Cross-platform and fix macOS playback
            subprocess.call(['open', filedest])
            print('Played recording')
            os.remove(filedest)
            return
    else:
        response = elksapi(args, 'recordings')['data']
        if args.play:
            print('Cannot play multiple recordings. Please set recording_id')
            exit(1)
    for recording in response:
        pretty_print_recording(recording, pretty = args.pretty)
        if args.verbose:
            call_res = elksapi(args, 'calls/%s' % recording['callid'])
            kv_print('From:', call_res['from'])
            kv_print('To:', call_res['to'])
            kv_print('Actions:', json.dumps(call_res['actions']))

def parse_arguments(parser):
    parser.description = descr
    parser.add_argument('-p', '--pretty', action='store_true',
            help='Print human friendly numbers')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Print detailed information')
    parser.add_argument('recording_id', nargs='?',
            help='Select a specific recording')
    parser.add_argument('--play', action='store_true',
            help='Try to play the selected recording (PRETTY MUCH BROKEN)')
    parser_inject_generics(parser)

def pretty_print_recording(recording, pretty = False):
    if pretty:
        size = bytes_to_human(recording['bytes'])
    else:
        size = recording['bytes']

    if pretty:
        duration = duration_to_human(recording['duration'])
    else:
        duration = recording['duration']

    print('%s %s %s %s' % (
        recording['created'],
        recording['id'],
        duration,
        size
    ))

def bytes_to_human(size):
    si_bytes = ('B', 'kB', 'MB', 'GB', 'TB', 'PB', 'ZB', 'YB')
    si_magnitude = int(math.floor(math.log10(size)) / 3)
    return '%.2f %s' % (size / pow(10, si_magnitude*3), si_bytes[si_magnitude])

def duration_to_human(length):
    seconds = length % 60
    minutes = length / 60
    hours = minutes / 60
    return '%dh%dm%ds' % (hours, minutes, seconds)

