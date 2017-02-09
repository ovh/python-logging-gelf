:mod:`logging_gelf.formatters` --- Formatters
=============================================

.. module:: logging_gelf.formatters
:synopsis: Formatters specify the layout of log records into GELF.

.. moduleauthor:: Cedric Dumay <cedric.dumay@gmail.com>
.. sectionauthor:: Cedric Dumay <cedric.dumay@gmail.com>


.. class:: GELFFormatter

    A subclass of :class:`logging.Formatter` to format LogRecord into GELF.

    .. method:: __init__(schema=<logging_gelf.schemas.GelfSchema>, null_character=False, JSONEncoder=json.JSONEncoder)

        A GELF formatter to format a :class:`logging.LogRecord` into GELF.

        :param logging_gelf.schemas.GelfSchema schema: The marshmallow schema to use to format data.
        :param bool null_character: Append a '\0' at the end of the string. It depends on the input used.
            :param json.JSONEncoder JSONEncoder: A custom json encoder to use.

        .. method:: format(record)

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

The next example uses marshmallow and a custom JSONEncoder which transform all list, tuple or dict to strings:

.. code-block:: python

    >>> import logging
    >>> import sys
    >>> from logging_gelf.formatters import GELFFormatter, StringJSONEncoder
    >>> from marshmallow import fields, Schema
    >>> from logging_gelf.schemas import GelfSchema
    >>>
    >>> class Person(GelfSchema):
    ...     lastname = fields.String()
    ...     father = fields.Nested(Person)
    ...     firstname = fields.List(fields.String)
    ...
    >>>
    >>> me = dict(lastname="Dumay", firstname=["Cedric", "Julien"])
    >>>
    >>> logger = logging.getLogger("gelf")
    >>> logger.setLevel(logging.DEBUG)
    >>>
    >>> handler = logging.StreamHandler(sys.stdout)
    >>> handler.setFormatter(
    ...     GELFFormatter(schema=Person, JSONEncoder=StringJSONEncoder))
    >>> logger.addHandler(handler)
    >>>
    >>> logger.debug("A marshmallow example with Nested", extra=me)
    {"host": "host.example.com", "_firstname": "['Cedric', 'Julien']", "file": "<stdin>", "version": "1.1", "short_message": "A marshmallow example with Nested", "timestamp": 1486643773.3877068, "level": 7, "line": 1, "_lastname": "Dumay"}

As we can see, firstname is not an array.

.. seealso::

    `Formatter Objects <https://docs.python.org/3/library/logging.html#formatter-objects>`_
        Official python documentation
