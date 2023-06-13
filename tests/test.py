import unittest
import logging
import io
import json

from logging_gelf.formatters import GELFFormatter


class TestFormatter(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger("gelf")
        self.logger.setLevel(logging.INFO)
        self.log_stream = io.StringIO()

        handler = logging.StreamHandler(self.log_stream)
        handler.setFormatter(GELFFormatter())
        self.logger.addHandler(handler)

        super().setUp()

    def test_handle_format_exception(self):
        self.logger.info("hello %s!", "beautiful world!")

        log = json.loads(self.log_stream.getvalue())
        self.assertNotEqual(log, "")

    def test_has_host(self):
        self.logger.info("hello %s!", "world")

        log = json.loads(self.log_stream.getvalue())
        self.assertIn("host", log)
        self.assertNotEqual("", log["host"])

    def test_short_message(self):
        self.logger.info("hello %s!", "world")

        log = json.loads(self.log_stream.getvalue())
        self.assertEqual("hello world!", log["short_message"])

    def test_exception(self):
        try:
            raise Exception("failed to xxx")
        except Exception:
            self.logger.exception("hello!")

        log = json.loads(self.log_stream.getvalue())
        self.assertIn("failed to xxx", log["full_message"])
        self.assertIn("hello!", log["full_message"])

    def test_no_exception(self):
        self.logger.info("hello!")

        log = json.loads(self.log_stream.getvalue())
        self.assertNotIn("full_message", log)

    def test_stack_info(self):
        self.logger.info("hello!", stack_info=True)

        log = json.loads(self.log_stream.getvalue())
        self.assertIn("full_message", log)

    def test_no_stack_info(self):
        self.logger.info("hello!")

        log = json.loads(self.log_stream.getvalue())
        self.assertNotIn("full_message", log)
