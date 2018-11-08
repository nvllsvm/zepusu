zepusu
======

|Version| |CI|

A minimalist ZeroMQ pub-sub command line client.

Features:

* Publish messages to 0 through ∞ subscribers.
* Subscribe to all messages or filter by one or more topics.
* Exits after receiving a single message or subscribed indefinitely.
* Built with scripting in mind.


Installation
------------

.. code::

    $ pip install zepusu


Example
-------

Begin by starting a subscriber in follow mode.

.. code::

    $ zepusu sub -f


Publish a few messages.

.. code::

    $ zepusu pub hello world
    $ zepusu pub greetings galaxy

The subscriber outputs both messages.

.. code::

    $ zepusu sub -f
    hello world
    greetings galaxy


Usage
-----

.. code:: shell

    usage: zepusu [-h] [--version] [-p PORT] {pub,sub} ...

    ZeroMQ pub-sub command line client

    positional arguments:
      {pub,sub}

    optional arguments:
      -h, --help  show this help message and exit
      --version   show program's version number and exit
      -p PORT


.. |Version| image:: https://img.shields.io/pypi/v/zepusu.svg?
   :target: https://pypi.org/project/zepusu/

.. |CI| image:: https://gitlab.com/nvllsvm/zepusu/badges/master/pipeline.svg?
   :target: https://gitlab.com/nvllsvm/zepusu/commits/master
