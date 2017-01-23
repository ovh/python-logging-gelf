#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>

Schema allow to specify a mapping for :class:`logging.LogRecord`. It based on :class:`marshmallow.Schema`. All schema MUST inherit from :class:`logging_gelf.schemas.GelfSchema`.
"""
import socket
import time
from marshmallow import Schema, fields
from logging_gelf import SYSLOG_LEVELS
from marshmallow import post_dump

GELF_1_1_FIELDS = [
    'version', 'host', 'short_message', 'full_message', 'timestamp', 'level',
    'line', 'file'
]


class GelfSchema(Schema):
    version = fields.Constant("1.1")
    host = fields.String(required=True, default=socket.gethostname)
    short_message = fields.Method('to_message')
    full_message = fields.String()
    timestamp = fields.Method('to_timestamp')
    level = fields.Method('to_syslog_level')
    lineno = fields.Integer(dump_to="line")
    pathname = fields.String(dump_to="file")

    @classmethod
    def to_syslog_level(cls, value):
        """description of to_syslog_level"""
        return SYSLOG_LEVELS.get(value.levelno, 1)

    @classmethod
    def to_timestamp(cls, value):
        """to_timestamp"""
        if value.created:
            return value.created
        else:
            return time.time()

    @classmethod
    def to_message(cls, value):
        """description of to_message"""
        return value.getMessage() % vars(value)

    @staticmethod
    def key_path(*args):
        """description of key_path"""
        return "_".join(args)

    @staticmethod
    def to_flat_dict(prefix, data):
        flat_result = dict()
        for dkey, dvalue in data.items():
            path = GelfSchema.key_path(prefix, dkey)
            if isinstance(dvalue, dict):
                flat_result.update(GelfSchema.to_flat_dict(path, dvalue))
            else:
                flat_result[path] = dvalue
        return flat_result

    @post_dump
    def fix_additional_fields(self, data):
        """description of fix_additional_fields"""
        result = dict()
        for key, value in data.items():
            rkey = key if key in GELF_1_1_FIELDS else '_{}'.format(key)
            if isinstance(value, dict):
                result.update(self.to_flat_dict(rkey, value))
            else:
                result[rkey] = value
        return result
