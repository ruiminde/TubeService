# -*- coding: utf-8 -*-

__author__ = 'Rui'

import unittest
from unittest import TestCase
import logging

from metro_lisboa import LineStatus
import json_backend


_RESPONSE_BODY_ALL_OK = """
{"amarela":" Ok","azul":" Ok","verde":" Ok","vermelha":" Ok","tipo_msg_am":"0","tipo_msg_az":"0","tipo_msg_vd":"0","tipo_msg_vm":"0"}
"""

_RESPONSE_UNKNOWN_STATUS = """
{"amarela":" abc","azul":"def","verde":"ghi","vermelha":" Ok","tipo_msg_am":"0","tipo_msg_az":"0","tipo_msg_vd":"0","tipo_msg_vm":"0"}
"""

logging.basicConfig(level=logging.INFO)


class TestJSONBackend(TestCase):
    def test_parse_response_invalid(self):
        try:
            json_backend.parse_response("NOT JSON")
        except json_backend.ParseError:
            pass

    def test_parse_response_all_ok(self):
        expected = {
            LineStatus.LINE_RED: (LineStatus.STATUS_OK, None),
            LineStatus.LINE_YELLOW: (LineStatus.STATUS_OK, None),
            LineStatus.LINE_BLUE: (LineStatus.STATUS_OK, None),
            LineStatus.LINE_GREEN: (LineStatus.STATUS_OK, None),
        }

        actual = json_backend.parse_response(_RESPONSE_BODY_ALL_OK)
        self.assertDictEqual(expected, actual)

    def test_parse_response_unknown_status(self):
        expected = {
            LineStatus.LINE_RED: (LineStatus.STATUS_OK, None),
            LineStatus.LINE_YELLOW: (LineStatus.STATUS_UNKNOWN, None),
            LineStatus.LINE_BLUE: (LineStatus.STATUS_UNKNOWN, None),
            LineStatus.LINE_GREEN: (LineStatus.STATUS_UNKNOWN, None),
        }

        actual = json_backend.parse_response(_RESPONSE_UNKNOWN_STATUS)
        self.assertDictEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
