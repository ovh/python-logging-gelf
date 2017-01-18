#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import json
import logging
from logging_gelf.schemas import GelfSchema


class GELFFormatter(logging.Formatter):
    """A GELF formatter to format a :class:logging.LogRecord into Graylog Extended Lenght Format (GELF)

    """

    def __init__(self, schema=GelfSchema, null_character=False):
        if not issubclass(schema, GelfSchema):
            raise ValueError("Schema MUST inherit from 'GelfSchema'")

        self.schema = schema
        self.null_character = null_character
        logging.Formatter.__init__(self)

    def format(self, record):
        """Format the specified record into json using the schema which MUST inherit from :class:`GelfSchema`.

        :param logging.LogRecord record: Contains all the information pertinent to the event being logged.
        :return: A JSON dump of the record.
        :rtype: str
        """
        out = json.dumps(self.schema().dump(record).data)
        if self.null_character is True:
            out += '\0'
        return out
