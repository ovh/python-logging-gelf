#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import socket
import ssl
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

    def makeSocket(self, timeout=1, after_idle_sec=1, interval_sec=3,
                   max_fails=5):
        """makeSocket"""
        sock = SocketHandler.makeSocket(self, timeout=timeout)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)

        if self.use_tls is True:
            return ssl.wrap_socket(
                sock, cert_reqs=self.cert_reqs, ca_certs=self.ca_certs
            )
        return sock

    def makePickle(self, record):
        return bytes(self.format(record) + "\n", "UTF-8")
