import argparse
import pathlib
import signal
import sys
import tempfile
import time

import pkg_resources
import zmq

try:
    __version__ = pkg_resources.get_distribution('zepusu').version
except pkg_resources.DistributionNotFound:
    __version__ = 'unknown'

signal.signal(signal.SIGINT, lambda *_: sys.exit(1))


def _subscribe(socket_path, topics):
    """
    Return a generator which subscribes to and yields from a queue

    :param int port: local port
    :param iterable or None topics: topics to subscribe to. None for all

    :rtype: generator yielding bytes
    """
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f'ipc://{socket_path}')
    # Nothing will be received otherwise
    if topics is None:
        topics = ['']
    for topic in topics:
        socket.setsockopt(zmq.SUBSCRIBE, topic.encode())
    _create_wait()
    while True:
        yield socket.recv()


def _publish(socket_path, messages):
    """
    Publish messages to a queue

    :param int port: local port
    :param iterable of bytes messages: messages to publish
    """
    context = zmq.Context()
    socket = context.socket(zmq.XPUB)
    socket.bind(f'ipc://{socket_path}')
    _create_wait()
    for message in messages:
        socket.send(message)


def _create_wait():
    # TODO: should REQ/REP be used too?
    """
    Wait before returning a socket back for use.

    Publishing and subscribing often fails with values lower than 0.25 seconds
    """
    time.sleep(0.25)


def main():
    parser = argparse.ArgumentParser(
        description='ZeroMQ pub-sub command line client')
    parser.set_defaults(mode=None)
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument(
        '-n', dest='name', default='zepusu', help='Socket name')

    sp = parser.add_subparsers()

    sp_pub = sp.add_parser('pub', description='Publish')
    sp_pub.set_defaults(mode='pub')
    sp_pub.add_argument('payload', nargs='*', help='Message to publish')

    sp_sub = sp.add_parser('sub', description='Subscribe')
    sp_sub.set_defaults(mode='sub')
    sp_sub.add_argument(
        '-t', dest='topic', action='append', help='Filter by topic')
    sp_sub.add_argument(
        '-f',
        dest='follow',
        action='store_const',
        const=True,
        help='Subscribe until process exists')

    args = parser.parse_args()

    socket_path = pathlib.Path(tempfile.gettempdir(), f'zepusu_{args.name}')
    socket_path = str(socket_path.absolute())

    if args.mode == 'pub':
        _publish(socket_path, [' '.join(args.payload).encode()])
    elif args.mode == 'sub':
        messages = _subscribe(socket_path, args.topic)
        if args.follow:
            for message in messages:
                print(message.decode())
        else:
            print(next(messages).decode())
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
