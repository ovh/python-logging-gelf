#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import ssl
import logging
from logging.handlers import SocketHandler


class GELFTCPSocketHandler(SocketHandler):
    """GELFTCPSocketHandler"""

    def __init__(self, host, port, use_tls=False, cert_reqs=ssl.CERT_NONE,
                 ca_certs=None):
        """description of __init__"""
        SocketHandler.__init__(self, host, port)
        self.ca_certs = ca_certs
        self.cert_reqs = cert_reqs
        self.use_tls = use_tls

    def makeSocket(self, timeout=1):
        """makeSocket"""
        sock = SocketHandler.makeSocket(self, timeout=timeout)
        if self.use_tls is True:
            return ssl.wrap_socket(
                sock, cert_reqs=self.cert_reqs, ca_certs=self.ca_certs
            )
        return sock

    def makePickle(self, record):
        return bytes(self.format(record) + "\n", "UTF-8")
