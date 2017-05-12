.. _logging-ldp:

Send logs to OVH LDP
====================

You can easly send logs to the `OVH Logs Data Platform service <https://www.ovh.com/fr/data-platforms/logs/>`_
using a custom :class:`logging_gelf.formatters.GELFFormatter` with your stream token.

Example
-------

The following example show how send structured log records (see: :ref:`logging-extra`) with the token
**483fea61-1886-4ec8-93b4-a8d7d05af8af** on the UDP input of the cluster **gra1.logs.ovh.com**.

.. code-block:: python

    import logging
    from logging_gelf.formatters import GELFFormatter
    from marshmallow import fields, Schema
    from logging_gelf.schemas import GelfSchema
    from logging_gelf.handlers import GELFUDPSocketHandler

    # a "generic" object
    class User(object):
        def __init__(self, firstname, lastname):
            self.firstname = firstname
            self.lastname = lastname

    # Marshmallow schemas used by formatters
    class UserSchema(Schema):
        firstname = fields.String()
        lastname = fields.String()

    class LDPSchema(GelfSchema):
        user = fields.Nested(UserSchema)
        age_num = fields.Integer(default=42)
        token = fields.Constant(
            "483fea61-1886-4ec8-93b4-a8d7d05af8af", dump_only=True,
            dump_to="X-OVH-TOKEN"
        )

    # logger setup
    logger = logging.getLogger("gelf-udp-example")
    logger.setLevel(logging.DEBUG)

    handler = GELFUDPSocketHandler("gra1.logs.ovh.com", 2202)
    handler.setFormatter(GELFFormatter(schema=LDPSchema))
    logger.addHandler(handler)

    # an object to log
    currentuser =  User("Cedric", "Dumay")
    # send it!
    logger.info("A marshmallow example with Nested", extra=dict(user=currentuser))

.. note::

    In this example, we set the suffix **_num** to the field **age** to force
    casting type in LDP (see: `The field naming convention <https://docs.ovh.com/gb/en/mobile-hosting/logs-data-platform/field-naming-conventions/#id2>`_)

Log entry in Graylog
--------------------

.. image:: _static/ldp.png