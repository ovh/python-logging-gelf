.. _use-LoggerAdapter:

Use :class:`logging.LoggerAdapter`
==================================

To use logger adapter, you need like the extra on logging event, a custom schema to serialize extra data (see: :ref:`logging-extra`).

.. code-block:: python

    >>> import sys
    >>> import logging
    >>> from logging_gelf.formatters import GELFFormatter
    >>> from logging_gelf.schemas import GelfSchema
    >>> from marshmallow import fields
    >>>
    >>> # we create a custom schema
    ... class MyGelfSchema(GelfSchema):
    ...     username = fields.String()
    ...
    >>> # we create the logger
    ... logger = logging.getLogger("gelf")
    >>> logger.setLevel(logging.DEBUG)
    >>>
    >>> # we use StreamHandler to display the result
    ... handler = logging.StreamHandler(sys.stdout)
    >>> handler.setFormatter(GELFFormatter(schema=MyGelfSchema))
    >>> logger.addHandler(handler)
    >>>
    >>> # we create an adapter
    ... adapter = logging.LoggerAdapter(logger=logger, extra=dict(username="C.Dumay"))
    >>> adapter.debug("hello !")
    {"version": "1.1", "_username": "C.Dumay", "line": 1, "level": 7, "file": "<stdin>", "timestamp": 1484904968.390859, "short_message": "hello !", "host": "host.example.com"}


.. note::

    LoggerAdapter extra set at initialization can be overwitten

    .. code-block:: python

        >>> logger.debug("hello !", extra=dict(username="Dude"))
        {"version": "1.1", "_username": "Dude", "line": 1, "level": 7, "file": "<stdin>", "timestamp": 1484905204.7358975, "short_message": "hello !", "host": "host.example.com"}


.. seealso::

    `LoggerAdapter Objects <https://docs.python.org/3/library/logging.html?highlight=loggeradapter#loggeradapter-objects>`_
        Full python documentation