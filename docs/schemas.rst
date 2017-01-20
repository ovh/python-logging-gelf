:mod:`logging_gelf.schemas` --- Schemas
=======================================

.. module:: logging_gelf.schemas
    :synopsis: Marshmallow schemas used to serialize log record data

.. moduleauthor:: Cedric Dumay <cedric.dumay@gmail.com>
.. sectionauthor:: Cedric Dumay <cedric.dumay@gmail.com>

.. class:: GelfSchema

    Schema which allow to specify a mapping for :class:`logging.LogRecord`. It based on :class:`marshmallow.Schema`. All schema MUST inherit from this.

    .. attribute:: version

        The const *version* specify the GELF version.

    .. attribute:: host

        Hostname which emitted the log record. If not set, :code:`socket.gethostname()` will be used.

    .. attribute:: short_message

        Plain message.

    .. attribute:: full_message

        Extended message

    .. attribute:: timestamp

        :class:`logging.LogRecord` creation time. If :attr:`record.created` is not set, current timestamp will be set.

    .. attribute:: level

        Syslog level representation

    .. attribute:: lineno

        Origine line number. This value will be dump into `line` to match GELF spec.

    .. attribute:: pathname

        Origine file pathe. This value will be dump into `file` to match GELF spec.

    .. classmethod:: to_syslog_level(value)

        Map :attr:`value.levelno` into syslog level.

        :param logging.LogRecord value: log record to serialize.
        :return: syslog level
        :rtype: int

    .. classmethod:: to_timestamp(value)

        Returns `value.created` or :code:`time.time()`

        :param logging.LogRecord value: log record to serialize.
        :return: timestamp
        :rtype: float

    .. classmethod:: to_message(value)

        Returns the :class:`logging.LogRecord` formatted message.

        :param logging.LogRecord value: log record to serialize.
        :return: entry message
        :rtype: str

    .. method:: fix_additional_fields(data)

        A "post dump" method which finalize data by prefixing with a "_" the additionals fields.

.. note::

    Only fields set in the model will be serilialized.

Example
-------

.. code-block:: python

    >>> import logging
    >>> from logging_gelf.schemas import GelfSchema
    >>> rec = logging.LogRecord(
    ...  name="test-gelf", level=logging.DEBUG, pathname=None,
    ...  lineno=None, msg="test", args=list(), exc_info=None
    )
    >>> GelfSchema().dump(rec).data
    {'level': 7, 'line': None, 'host': 'host.example.com', 'short_message': 'test', 'version': '1.1', 'file': None, 'timestamp': 1484831977.3012216}


Nested fields
-------------

As Graylog doesn't support objects, Nested marshmallow fields are "flat unpacked" using a pseudo path in keys:

.. code-block:: python

    >>> import logging
    >>> import sys
    >>> from logging_gelf.formatters import GELFFormatter
    >>> from marshmallow import fields, Schema
    >>> from logging_gelf.schemas import GelfSchema

    >>> class Person(Schema):
    ...     firstname = fields.String()
    ...
    >>> class Familly(GelfSchema):
    ...     lastname = fields.String()
    ...     father = fields.Nested(Person)
    ...
    >>> familly = dict(lastname="Dumay", father=dict(firstname="Cedric"))
    >>> logger = logging.getLogger("gelf")
    >>> logger.setLevel(logging.DEBUG)
    >>> handler = logging.StreamHandler(sys.stdout)
    >>> handler.setFormatter(GELFFormatter(schema=Familly))
    >>> logger.addHandler(handler)
    >>> logger.debug("A marshmallow example with Nested", extra=familly)
    {"level": 7, "_father_firstname": "Cedric", "short_message": "A marshmallow example with Nested", "_lastname": "Dumay", "file": "<stdin>", "host": "host.example.com", "timestamp": 1484919251.3890517, "version": "1.1", "line": 1}

.. note::

    As we can see :code:`familly['father']['firstname']` produce a GELF attribute `_father_firstname`
