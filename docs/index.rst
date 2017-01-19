.. logging-gelf documentation master file, created by
   sphinx-quickstart on Wed Jan 18 17:11:49 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

logging-gelf
============

A python 3 logging bundle to send logs in Graylog Extended Lenght Format (GELF)
. This is a rewrote of `Djehouty <https://github.com/ovh/djehouty>`_.

The following example shows how to send log in Graylog TCP input

.. code-block:: python

    import logging
    from logging_gelf.formatters import GELFFormatter
    from logging_gelf.handlers import GELFTCPSocketHandler

    logger = logging.getLogger("gelf")
    logger.setLevel(logging.DEBUG)

    handler = GELFTCPSocketHandler(host="127.0.0.1", port=12201)
    handler.setFormatter(GELFFormatter(null_character=True))
    logger.addHandler(handler)
    logger.debug("hello !")

Get It Now
----------

First, install logging-gelf using `pip <https://pip.pypa.io/en/stable/>`_::

    pip install -U logging-gelf


Documentation content
---------------------

.. toctree::
   :maxdepth: 1

   api_focus.rst
   guides.rst


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

