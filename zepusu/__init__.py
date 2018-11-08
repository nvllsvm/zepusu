import argparse
import signal
import sys
import time

import pkg_resources
import zmq

try:
    __version__ = pkg_resources.get_distribution('zepusu').version
except pkg_resources.DistributionNotFound:
    __version__ = 'unknown'


signal.signal(signal.SIGINT, lambda *_: sys.exit(1))


def _subscribe(port, topics):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f'tcp://localhost:{port}')
    # Nothing will be received otherwise
    if topics is None:
        topics = ['']
    for topic in topics:
        socket.setsockopt(zmq.SUBSCRIBE, topic.encode())
    _create_wait()
    while True:
        yield socket.recv()


def _publish(port, messages):
    context = zmq.Context()
    socket = context.socket(zmq.XPUB)
    socket.bind(f'tcp://*:{port}')
    _create_wait()
    for message in messages:
        socket.send(message.encode())


def _create_wait():
    # TODO: should REQ/REP be used too?
    """
    Wait before returning a socket back for use.

    Publishing and subscribing often fails with values lower than 0.25 seconds
    """
    time.sleep(0.25)


def main():
    parser = argparse.ArgumentParser(
        description='ZeroMQ pub-sub command line client'
    )
    parser.set_defaults(mode=None)
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('-p', '--port', type=int, default=5556)

    sp = parser.add_subparsers()

    sp_pub = sp.add_parser('pub', description='Publish')
    sp_pub.set_defaults(mode='pub')
    sp_pub.add_argument('payload', nargs='*')

    sp_sub = sp.add_parser('sub', description='Subscribe')
    sp_sub.set_defaults(mode='sub')
    sp_sub.add_argument('-t', '--topic', action='append')
    sp_sub.add_argument('-f', '--follow', action='store_const', const=True)

    args = parser.parse_args()

    if args.mode == 'pub':
        _publish(args.port, [' '.join(args.payload)])
    elif args.mode == 'sub':
        messages = _subscribe(args.port, args.topic)
        if args.follow:
            for message in messages:
                print(message.decode())
        else:
            print(next(messages).decode())
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
