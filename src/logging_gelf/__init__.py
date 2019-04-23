#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
# Copyright 2019 The logging-gelf Authors. All rights reserved.

import logging

SYSLOG_LEVELS = {
    logging.CRITICAL: 2, logging.ERROR: 3, logging.WARNING: 4, logging.INFO: 6,
    logging.DEBUG: 7,
}


# monkey patch
def process(self, msg, kwargs):
    """
    Process the logging message and keyword arguments passed in to
    a logging call to insert contextual information. You can either
    manipulate the message itself, the keyword args or both. Return
    the message and kwargs modified (or not) to suit your needs.

    Normally, you'll only need to override this one method in a
    LoggerAdapter subclass for your specific needs.
    """
    extra = dict(self.extra)
    extra.update(kwargs.get('extra', dict()))
    kwargs["extra"] = extra
    return msg, kwargs


# noinspection PyPep8
from logging import LoggerAdapter

LoggerAdapter.process = process
