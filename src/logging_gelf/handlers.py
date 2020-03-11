#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
# Copyright 2019 The logging-gelf Authors. All rights reserved.

import socket
import ssl
from logging.handlers import SocketHandler, DatagramHandler
import platform


class GELFTCPSocketHandler(SocketHandler):
    """GELFTCPSocketHandler"""

    def __init__(self, host, port, use_tls=False, cert_reqs=ssl.CERT_NONE,
                 ca_certs=None):
        """description of __init__"""
        SocketHandler.__init__(self, host, port)
        self.ca_certs = ca_certs
        self.cert_reqs = cert_reqs
        self.use_tls = use_tls

    def makeSocket(self, timeout=1, **kwargs):
        """makeSocket"""
        sock = SocketHandler.makeSocket(self, timeout=timeout)
        sock.setsockopt(
            socket.SOL_SOCKET, socket.SO_KEEPALIVE, kwargs.get('keep_alive', 1)
        )
        if platform.system() in ('Linux', 'Windows'):
            sock.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_KEEPIDLE,
                kwargs.get('after_idle_sec', 1)
            )
            sock.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_KEEPINTVL,
                kwargs.get('interval_sec', 3)
            )
            sock.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_KEEPCNT,
                kwargs.get('max_fails', 5)
            )

        if self.use_tls is True:
            return ssl.wrap_socket(
                sock, cert_reqs=self.cert_reqs, ca_certs=self.ca_certs
            )
        return sock

    def makePickle(self, record):
        return bytes(self.format(record) + "\n", "UTF-8")


class GELFUDPSocketHandler(DatagramHandler):
    def makePickle(self, record):
        return bytes(self.format(record) + "\n", "UTF-8")
