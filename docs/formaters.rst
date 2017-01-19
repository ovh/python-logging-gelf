Formatters
==========

.. automodule:: logging_gelf.formatters

.. autoclass:: logging_gelf.formatters.GELFFormatter

    .. automethod:: logging_gelf.formatters.GELFFormatter.format

Examples
--------

You can use the :class:`logging.StreamHandler` to test your formatter:

.. code-block:: python

    >>> import sys
    >>> import logging
    >>> from logging_gelf.formatters import GELFFormatter
    # we create the logger
    >>> logger = logging.getLogger("gelf")
    >>> logger.setLevel(logging.DEBUG)
    # we use StreamHandler to display the result
    >>> handler = logging.StreamHandler(sys.stdout)
    >>> handler.setFormatter(GELFFormatter())
    >>> logger.addHandler(handler)
    # we send a log entry
    >>> logger.debug("hello !")
    {"version": "1.1", "host": "host.example.com", "file": "<stdin>", "short_message": "hello !", "timestamp": 1484820522.4268215, "level": 7, "line": 1}

