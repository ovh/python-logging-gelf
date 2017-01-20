:mod:`logging_gelf.handlers` --- Handlers
=========================================

.. module:: logging_gelf.handlers
    :synopsis: Handlers send the log records (created by loggers) to the appropriate GELF inputs.

.. moduleauthor:: Cedric Dumay <cedric.dumay@gmail.com>
.. sectionauthor:: Cedric Dumay <cedric.dumay@gmail.com>

.. class:: GELFTCPSocketHandler

    The :class:`GELFTCPSocketHandler`, which inherit from :class:`logging.handlers.SocketHandler`, sends logging output to a TCP network socket.

    .. method:: __init__(host, port, use_tls=False, cert_reqs=<ssl.CERT_NONE>, ca_certs=None)

        Returns a new instance of the :class:`GELFTCPSocketHandler` class intended to
        communicate with a remote machine whose address is given by *host* and *port* over TCP.

        :param bool use_tls: Enable TLS communication.
        :param enum.IntEnum cert_reqs: SSL context virify mode. This attribute must be one of :const:`ssl.CERT_NONE`, :const:`ssl.CERT_OPTIONAL` or :const:`ssl.CERT_REQUIRED` (see `ssl doc <https://docs.python.org/3/library/ssl.html#constants>`_).
        :param str ca_certs: File which contains a set of concatenated "certification authority" certificates, which are used to validate certificates passed from the other end of the connection.

    .. method:: makeSocket(timeout=1, after_idle_sec=1, interval_sec=3, max_fails=5)

        Returns the socket used to send log records.

        :param float timeout: Set a timeout on blocking socket operations, can be a nonnegative floating point number expressing seconds.
        :param int after_idle_sec: Activates TCP keepalive after *after_idle_sec* second of idleness.
        :param int interval_sec: Sends a keepalive ping once every *interval_sec* seconds.
        :param int max_fails: Closes the connection after *max_fails* failed ping (= *max_fails* * *interval_sec*).
        :return: a TCP socket.
        :rtype: `socket.socket <https://docs.python.org/3/library/socket.html#socket.socket>`_

    .. method:: makePickle(record)

        Pickles the record’s attribute dictionary in binary format.

        :param logging.LogRecord record: record to format
        :rtype: bytes


Basic TCP example
-----------------

.. code-block:: python

    >>> import logging
    >>> from logging_gelf.handlers import GELFTCPSocketHandler

    # we create the logger
    >>> logger = logging.getLogger("gelf")
    >>> logger.setLevel(logging.DEBUG)
    >>> handler = GELFTCPSocketHandler(host="127.0.0.1", port=12201, level=logging.DEBUG)
    >>> logger.addHandler(handler)

.. seealso::

    `Logging handlers <https://docs.python.org/3/library/logging.handlers.html>`_
        Logging documentation

    `Socket Objects <https://docs.python.org/3/library/socket.html#socket-objects>`_
        Python socket documentation

