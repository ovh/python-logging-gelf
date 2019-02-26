#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>

Schema allow to specify a mapping for :class:`logging.LogRecord`. It based on
:class:`marshmallow.Schema`. All schema MUST inherit from
:class:`logging_gelf.schemas.GelfSchema`.
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

    @staticmethod
    def _forge_key(key, value):
        return key

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
        # noinspection PyBroadException
        try:
            return value.getMessage() % vars(value)
        except Exception:
            return value.getMessage()

    @staticmethod
    def key_path(*args):
        """description of key_path"""
        return "_".join(args)

    @classmethod
    def to_flat_dict(cls, prefix, data):
        flat_result = dict()
        for dkey, dvalue in data.items():
            path = cls.key_path(prefix, cls._forge_key(dkey, dvalue))
            if isinstance(dvalue, dict):
                flat_result.update(cls.to_flat_dict(path, dvalue))
            else:
                flat_result[path] = dvalue
        return flat_result

    @post_dump
    def fix_additional_fields(self, data):
        """description of fix_additional_fields"""
        result = dict()
        for key, value in data.items():
            if key in GELF_1_1_FIELDS:
                rkey = key
            else:
                rkey = '_{}'.format(self._forge_key(key, value))

            if isinstance(value, dict):
                result.update(self.to_flat_dict(rkey, value))
            else:
                result[rkey] = value
        return result
