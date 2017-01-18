#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import json
import logging
from logging_gelf.schemas import GelfSchema


class GELFFormatter(logging.Formatter):
    """GELFFormatter"""

    def __init__(self, schema=GelfSchema, null_character=False):
        if not issubclass(schema, GelfSchema):
            raise ValueError("Schema MUST inherit from 'GelfSchema'")

        self.schema = schema
        self.null_character = null_character
        logging.Formatter.__init__(self)

    def format(self, record):
        """format"""
        out = json.dumps(self.schema().dump(record).data)
        if self.null_character is True:
            out += '\0'
        return out
