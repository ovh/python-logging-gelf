************
Logging GELF
************

.. image:: https://travis-ci.org/cdumay/logging-gelf.svg?branch=master
   :target: https://travis-ci.org/cdumay/logging-gelf
   :alt: Latest version


.. image:: https://readthedocs.org/projects/logging-gelf/badge/?version=latest
   :target: http://logging-gelf.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


A python logging bundle to send logs using GELF. This is a rewrote of `Djehouty <https://github.com/ovh/djehouty>`_

Quickstart
==========

First, install logging-gelf using `pip <https://pip.pypa.io/en/stable/>`_::

    pip install -U logging-gelf

The following example shows how to send log in Graylog TCP input

.. code-block:: python

    import logging
    from logging_gelf.formatters import GELFFormatter
    from logging_gelf.handlers import GELFTCPSocketHandler

    logger = logging.getLogger("gelf")
    logger.setLevel(logging.DEBUG)

    handler = GELFTCPSocketHandler(host="127.0.0.1", port=12201)
    handler.setFormatter(GELFFormatter(schema=MyGelfSchema, null_character=True))
    logger.addHandler(handler)
    logger.debug("hello !")

Documentation
=============

Logging adapter, extra, custom schema and many other stuff are available in the full documentation available at http://logging-gelf.readthedocs.io/ .

Requirements
============

- Python >= 3.3

Project Links
=============

- Docs: http://logging-gelf.readthedocs.io/
- PyPI: https://pypi.python.org/pypi/logging-gelf
- Issues: https://github.com/cdumay/logging-gelf/issues

License
=======

Apache License 2.0