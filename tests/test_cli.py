import subprocess

WAIT_TIMEOUT = 3


def test_single_message():
    subscriber = subprocess.Popen(['zepusu', 'sub'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

    publish = subprocess.Popen(['zepusu', 'pub', 'hello', 'world'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    publish.wait(WAIT_TIMEOUT)
    assert 0 == publish.returncode
    assert b'' == publish.stdout.read()
    assert b'' == publish.stderr.read()

    subscriber.wait(WAIT_TIMEOUT)
    assert 0 == subscriber.returncode
    assert b'hello world\n' == subscriber.stdout.read()
    assert b'' == subscriber.stderr.read()

    for proc in (publish, subscriber):
        for attr in ('stdout', 'stderr'):
            getattr(proc, attr).close()
