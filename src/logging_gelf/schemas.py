#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
# Copyright 2019 The logging-gelf Authors. All rights reserved.

"""
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

    @classmethod
    def _forge_key(cls, key, _value):
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

    @classmethod
    def format_key(cls, xpath, key, value):
        if key in GELF_1_1_FIELDS:
            return key
        elif key in (None, ""):
            return ""
        elif xpath in (None, ""):
            return "_{}".format(cls._forge_key(key, value))
        else:
            return "{}_{}".format(xpath, cls._forge_key(key, value))

    @classmethod
    def to_flat_dict(cls, xpath, key, value):
        parts = dict()
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                parts.update(cls.to_flat_dict(
                    cls.format_key(xpath, key, value), subkey, subvalue
                ))
        elif isinstance(value, (list, tuple)):
            if len(value) < 20:
                for idx in range(len(value)):
                    parts.update(cls.to_flat_dict(
                        cls.format_key(xpath, key, value), idx, value[idx]
                    ))
            else:
                try:
                    parts[cls.format_key(xpath, key, value)] = str(value)
                except Exception:
                    pass
        else:
            parts[cls.format_key(xpath, key, value)] = value
        return parts

    @post_dump
    def fix_additional_fields(self, data, **kwargs):
        """description of fix_additional_fields"""
        return self.to_flat_dict("", "", data)
