import argparse
import os
import subprocess
import sys

PARSER = argparse.ArgumentParser(description='')
PARSER.add_argument('--separator', type=str, help='How to join path components', default='/')
PARSER.add_argument('--preview', type=str, help='Show a preview of nodes with this command')
PARSER.add_argument(
    '--shell', action='store_true', default=False,
    help='Use shell to execute get_children. {} is replaced with current path.')
PARSER.add_argument('root', type=str, help='Where to start searching from')
PARSER.add_argument(
    'get_children', type=str,
    help='Program to get children',
    nargs='*')

class Tee:
    def __init__(self, stream):
        self._stream = stream
        self._buffer = None
        self._read_event = threading.Event()
        self._new_pusher_out, self._new_pusher_in = os.pipe()

    def run(self):
        self._buffer = self._stream.read()
        while True:
            fd = self._new_pusher_in.readline()
            stream = os.fdopen(fd)
            stream.write(self._buffer)

    def open(self):
        reader, writer = os.pipe()
        return reader


UP_CHILD = b'* up'
SELECT_CHILD = b'* select'
def main():
    args = PARSER.parse_args()
    path = [args.root.encode('utf8')]
    while True:
        separator = args.separator.encode('utf8')
        if args.shell:
            children = subprocess.check_output(
                ' '.join(args.get_children)
                .format(separator.join(path).decode('utf8'))
                .encode('utf8'), shell=True)
        else:
            children = subprocess.check_output(args.get_children + [separator.join(path)])

        ACTIONS = [UP_CHILD, SELECT_CHILD]
        path_bytes = separator.join(path)
        preview_args = [b'--preview', args.preview.encode('utf8') + b' %s%s{}' % (path_bytes, separator)] if args.preview else []
        child = subprocess.check_output(['fzf', '--prompt', path_bytes] + preview_args, input=children.strip(b'\n') + b'\n' + b'\n'.join(ACTIONS)).strip(b'\n')
        if child == UP_CHILD:
            path.pop()
        elif child == SELECT_CHILD:
            sys.stdout.buffer.write(seperator.join(path) + b'\n')
            return
        else:
            path.append(child)
