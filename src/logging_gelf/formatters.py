#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>

Formatters specify the layout of log records in the final output (GELF).
"""
import json
import logging
from logging_gelf.schemas import GelfSchema


class GELFFormatter(logging.Formatter):
    """A GELF formatter to format a :class:`logging.LogRecord` into GELF.

    :param logging_gelf.schemas.GelfSchema schema: The marshmallow schema to use to format data.
    :param bool null_character: Append a '\0' at the end of the string. It depends on the input used.

    """

    def __init__(self, schema=GelfSchema, null_character=False):
        if not issubclass(schema, GelfSchema):
            raise ValueError("Schema MUST inherit from 'GelfSchema'")

        self.schema = schema
        self.null_character = null_character
        logging.Formatter.__init__(self)

    def format(self, record):
        """Format the specified record into json using the schema which MUST inherit from :class:`logging_gelf.schemas.GelfSchema`.

        :param logging.LogRecord record: Contains all the information pertinent to the event being logged.
        :return: A JSON dump of the record.
        :rtype: str
        """
        out = json.dumps(self.schema().dump(record).data)
        if self.null_character is True:
            out += '\0'
        return out
