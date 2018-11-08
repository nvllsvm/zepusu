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


def _start_subscriber(port, topics):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f'tcp://localhost:{port}')
    for topic in topics:
        socket.setsockopt(zmq.SUBSCRIBE, topic.encode())
    _wait()
    return socket


def _start_publisher(port):
    context = zmq.Context()
    socket = context.socket(zmq.XPUB)
    socket.bind(f'tcp://*:{port}')
    _wait()
    return socket


def _wait():
    time.sleep(0.25)


def _publish(socket, data):
    data = data.encode()
    socket.send(data)


def _receive(socket):
    data = socket.recv()
    print(data.decode())
    return data


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
        payload = ' '.join(args.payload)
        server = _start_publisher(args.port)
        _publish(server, payload)
    elif args.mode == 'sub':
        topics = args.topic or ['']
        socket = _start_subscriber(args.port, topics)
        if args.follow:
            while True:
                _receive(socket)
        else:
            _receive(socket)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
