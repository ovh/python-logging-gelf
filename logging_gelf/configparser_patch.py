#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import json
import logging
from logging import config
from logging_gelf.formatters import GELFFormatter
from logging_gelf.schemas import GelfSchema


def _create_formatters(cp):
    """Create and return formatters"""
    flist = cp["formatters"]["keys"]
    if not len(flist):
        return {}
    flist = flist.split(",")
    flist = config._strip_spaces(flist)
    formatters = {}
    for form in flist:
        sectname = "formatter_%s" % form
        fclass = logging.Formatter
        class_name = cp[sectname].get("class")
        if class_name:
            fclass = config._resolve(class_name)
        if issubclass(fclass, GELFFormatter):
            exclude_patterns = cp.get(
                sectname, "exclude_patterns", raw=True, fallback=None
            )
            if exclude_patterns:
                exclude_patterns = eval(exclude_patterns, vars(logging))
            f = fclass(
                config._resolve(cp.get(
                    sectname, "schema", raw=True,
                    fallback="logging_gelf.schemas.GelfSchema"
                )),
                cp.getboolean(
                    sectname, "null_character", raw=True, fallback=False
                ),
                config._resolve(cp.get(
                    sectname, "JSONEncoder", raw=True,
                    fallback="json.JSONEncoder"
                )),
                exclude_patterns
            )
        else:
            fs = cp.get(sectname, "format", raw=True, fallback=None)
            dfs = cp.get(sectname, "datefmt", raw=True, fallback=None)
            stl = cp.get(sectname, "style", raw=True, fallback='%')
            f = fclass(fs, dfs, stl)
        formatters[form] = f
    return formatters


config._create_formatters = _create_formatters
