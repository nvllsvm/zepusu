import subprocess
import unittest

WAIT_TIMEOUT = 3


class CLITests(unittest.TestCase):
    def test_single_message(self):
        subscriber = subprocess.Popen(['zepusu', 'sub'],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

        publish = subprocess.Popen(['zepusu', 'pub', 'hello', 'world'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        publish.wait(WAIT_TIMEOUT)
        self.assertEqual(0, publish.returncode)
        self.assertEqual(b'', publish.stdout.read())
        self.assertEqual(b'', publish.stderr.read())

        subscriber.wait(WAIT_TIMEOUT)
        self.assertEqual(0, subscriber.returncode)
        self.assertEqual(b'hello world\n', subscriber.stdout.read())
        self.assertEqual(b'', subscriber.stderr.read())

        for proc in (publish, subscriber):
            for attr in ('stdout', 'stderr'):
                getattr(proc, attr).close()
