#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
# Copyright 2019 The logging-gelf Authors. All rights reserved.

"""
Formatters specify the layout of log records in the final output (GELF).
"""

import json
import logging
import re

from logging_gelf.schemas import GelfSchema


class StringJSONEncoder(json.JSONEncoder):
    def encode(self, o):
        """description of encode"""
        res = dict()
        for key, value in o.items():
            if isinstance(value, (list, tuple, dict)):
                res[key] = str(value)
            else:
                res[key] = value
        return json.JSONEncoder.encode(self, res)


class GELFFormatter(logging.Formatter):
    """A GELF formatter to format a :class:`logging.LogRecord` into GELF.

    :param logging_gelf.schemas.GelfSchema schema: The marshmallow schema to
    use to format data.
    :param bool null_character: Append a '\0' at the end of the string. It
    depends on the input used.
    :param list|None exclude_patterns: List of regexp used to exclude keys.
    """

    def __init__(self, schema=GelfSchema, null_character=False,
                 JSONEncoder=json.JSONEncoder, exclude_patterns=None):
        if not issubclass(schema, GelfSchema):
            raise ValueError("Schema MUST inherit from 'GelfSchema'")

        self.schema = schema
        self.null_character = null_character
        self._encoder_cls = JSONEncoder
        exclude_patterns = exclude_patterns if exclude_patterns else list()
        self.exclude_patterns = ['^_{}'.format(x) for x in exclude_patterns]
        logging.Formatter.__init__(self)

    def serialize_record(self, record):
        """Serialize logging record into a dict

        :param logging.LogRecord record: Contains all the information pertinent
        to the event being logged.
        :return: A dict dump of the record.
        :rtype: dict
        """
        # exc_info, exc_text and stack_info logic stolen from the standard library
        # https://github.com/python/cpython/blob/3.8/Lib/logging/__init__.py#L655

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        record.message = record.getMessage() % vars(record)

        record.full_message = ""

        if record.exc_text:
            if record.msg[-1:] != "\n":
                record.full_message = record.full_message + "\n"
            record.full_message = record.full_message + record.exc_text

        if record.stack_info:
            if record.full_message[-1:] != "\n":
                record.full_message = record.full_message + "\n"
            record.full_message = record.full_message + self.formatStack(
                record.stack_info)

        if record.full_message != "":
            record.full_message = record.message + "\n" + record.full_message

        return self.filter_keys(self.schema().dump(record))

    def format(self, record):
        """Format the specified record into json using the schema which MUST
        inherit from :class:`logging_gelf.schemas.GelfSchema`.

        :param logging.LogRecord record: Contains all the information pertinent
        to the event being logged.
        :return: A JSON dump of the record.
        :rtype: str
        """
        out = json.dumps(self.serialize_record(record), cls=self._encoder_cls)
        if self.null_character is True:
            out += '\0'
        return out

    def filter_keys(self, data):
        """Filter GELF record keys using exclude_patterns

        :param dict data: Log record has dict
        :return: the filtered log record
        :rtype: dict
        """
        if self.exclude_patterns is None:
            return data

        keys = list(data.keys())
        for pattern in self.exclude_patterns:
            for key in keys:
                if re.match(pattern, key):
                    keys.remove(key)

        return dict(filter(lambda x: x[0] in keys, data.items()))
