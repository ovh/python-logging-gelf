#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>

Formatters specify the layout of log records in the final output (GELF).
"""
import re
import json
import logging
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

    def format(self, record):
        """Format the specified record into json using the schema which MUST
        inherit from :class:`logging_gelf.schemas.GelfSchema`.

        :param logging.LogRecord record: Contains all the information pertinent
        to the event being logged.
        :return: A JSON dump of the record.
        :rtype: str
        """
        data = self.filter_keys(self.schema().dump(record))
        out = json.dumps(data, cls=self._encoder_cls)
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
