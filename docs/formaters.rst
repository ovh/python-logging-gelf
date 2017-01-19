:mod:`logging_gelf.formatters` --- Formatters
=============================================

.. module:: logging_gelf.formatters
    :synopsis: Formatters specify the layout of log records into GELF.

.. moduleauthor:: Cedric Dumay <cedric.dumay@gmail.com>
.. sectionauthor:: Cedric Dumay <cedric.dumay@gmail.com>


.. class:: GELFFormatter

    A subclass of :class:`logging.Formatter` to format LogRecord into GELF.

.. method:: GELFFormatter.__init__(schema=<logging_gelf.schemas.GelfSchema>, null_character=False)

    A GELF formatter to format a :class:`logging.LogRecord` into GELF.

    :param logging_gelf.schemas.GelfSchema schema: The marshmallow schema to use to format data.
    :param bool null_character: Append a '\0' at the end of the string. It depends on the input used.

.. method:: GELFFormatter.format(record)

    Format the specified record into json using the schema which MUST inherit from :class:`logging_gelf.schemas.GelfSchema`.

    :param logging.LogRecord record: Contains all the information pertinent to the event being logged.
    :return: A JSON dump of the record.
    :rtype: str

Testing the output
------------------

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

.. seealso::

    `Formatter Objects <https://docs.python.org/3/library/logging.html#formatter-objects>`_
        Official python documentation
