.. _logging-extra:

Forward logging extra to Graylog
================================

To forward extra send in :class:`logging.LogRecord`, we need customize the marshmallow serializer used in the :class:`logging_gelf.formatters.GELFFormatter`:

.. code-block:: python

    >>> import sys
    >>> import logging
    >>> from logging_gelf.formatters import GELFFormatter
    >>> from logging_gelf.schemas import GelfSchema
    >>> from marshmallow import fields

    # we create a custom schema
    >>> class MyGelfSchema(GelfSchema):
    ...     username = fields.String()
    ...

    # we create the logger
    >>> logger = logging.getLogger("gelf")
    >>> logger.setLevel(logging.DEBUG)

    # we use StreamHandler to display the result
    >>> handler = logging.StreamHandler(sys.stdout)
    >>> handler.setFormatter(GELFFormatter(schema=MyGelfSchema))
    >>> logger.addHandler(handler)

    # we send a log entry
    >>> logger.debug("hello !", extra=dict(username="C.Dumay"))
    {"level": 7, "_username": "C.Dumay", "timestamp": 1484842992.1332045, "host": "host.example.com", "version": "1.1", "short_message": "hello !", "file": "<stdin>", "line": 1}

.. note::

    As we can see, the extra var *username* is append as an additional value (prefixed by '_')
