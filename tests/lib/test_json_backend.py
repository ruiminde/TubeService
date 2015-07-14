# -*- coding: utf-8 -*-

__author__ = 'Rui'

import unittest
from unittest import TestCase
import logging

from tubeservice.datacontract import *
from lib import json_backend

_RESPONSE_BODY_ALL_OK = """
{"amarela":" Ok","azul":" Ok","verde":" Ok","vermelha":" Ok","tipo_msg_am":"0","tipo_msg_az":"0","tipo_msg_vd":"0","tipo_msg_vm":"0"}
"""

_RESPONSE_BODY_ALL_PROBLEMS1 = """
{"amarela":" Ok","azul":" Ok","verde":" existem perturba\u00e7\u00f5es na circula\u00e7\u00e3o. O tempo de espera pode ser superior ao normal. Pedimos desculpa pelo inc\u00f3modo causado.","vermelha":" Ok","tipo_msg_am":"0","tipo_msg_az":"0","tipo_msg_vd":"1","tipo_msg_vm":"0"}
"""

_RESPONSE_BODY_ALL_PROBLEMS2 = """
{"amarela":" Ok","azul":" existem perturba\u00e7\u00f5es na circula\u00e7\u00e3o. O tempo de espera pode ser superior ao normal. Pedimos desculpa pelo inc\u00f3modo causado.","verde":" Ok","vermelha":" Ok","tipo_msg_am":"0","tipo_msg_az":"1","tipo_msg_vd":"0","tipo_msg_vm":"0"}
"""

_RESPONSE_BODY_ALL_PROBLEMS3 = """
{"amarela":" Ok","azul":" Ok","verde":" Ok","vermelha":" existem perturba\u00e7\u00f5es na circula\u00e7\u00e3o. O tempo de espera pode ser superior ao normal. Pedimos desculpa pelo inc\u00f3modo causado.","tipo_msg_am":"0","tipo_msg_az":"0","tipo_msg_vd":"0","tipo_msg_vm":"1"}
"""

_RESPONSE_BODY_ALL_PROBLEMS4 = """
{"amarela":" Devido a incidente com passageiro, a circula\u00e7\u00e3o est\u00e1 interrompida desde as 17:05. O tempo de reposi\u00e7\u00e3o poder\u00e1 ser superior a 15 minutos. Pedimos desculpa pelo inc\u00f3modo.","azul":" Ok","verde":" Ok","vermelha":" Ok","tipo_msg_am":"3","tipo_msg_az":"0","tipo_msg_vd":"0","tipo_msg_vm":"0"}
"""

_RESPONSE_BODY_ALL_PROBLEMS5 = """
{"amarela":" Ok","azul":" Ok","verde":" Devido a avaria de comboio, a circula\u00e7\u00e3o est\u00e1 interrompida desde as 20:55. Esperamos retomar a circula\u00e7\u00e3o num per\u00edodo inferior a 15 minutos. Pedimos desculpa pelo inc\u00f3modo.","vermelha":" Ok","tipo_msg_am":"0","tipo_msg_az":"0","tipo_msg_vd":"1","tipo_msg_vm":"0"}
"""

_RESPONSE_BODY_ALL_PROBLEMS6 = """
{"amarela":" Ok","azul":" Ok","verde":" devido a avaria de comboio, a circula\u00e7\u00e3o encontra-se com perturba\u00e7\u00f5es. O tempo de espera pode ser superior ao normal. Pedimos desculpa pelo inc\u00f3modo.","vermelha":" Ok","tipo_msg_am":"0","tipo_msg_az":"0","tipo_msg_vd":"1","tipo_msg_vm":"0"}
"""

_RESPONSE_UNKNOWN_STATUS = """
{"amarela":" abc","azul":"def","verde":"ghi","vermelha":" Ok","tipo_msg_am":"y","tipo_msg_az":"x","tipo_msg_vd":"z","tipo_msg_vm":"0"}
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
            LINE_RED: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_YELLOW: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_BLUE: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_GREEN: (STATUS_OK, REASON_NO_PROBLEM),
        }

        actual = json_backend.parse_response(_RESPONSE_BODY_ALL_OK)
        self.assertDictEqual(expected, actual)

    def test_parse_response_unknown_status(self):
        expected = {
            LINE_RED: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_YELLOW: (STATUS_UNKNOWN, " abc"),
            LINE_BLUE: (STATUS_UNKNOWN, "def"),
            LINE_GREEN: (STATUS_UNKNOWN, "ghi"),
        }

        actual = json_backend.parse_response(_RESPONSE_UNKNOWN_STATUS)
        self.assertDictEqual(expected, actual)

    def test_parse_response_problems1(self):
        expected = {
            LINE_RED: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_YELLOW: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_BLUE: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_GREEN: (STATUS_DELAY, REASON_LINE_TROUBLES),
        }

        actual = json_backend.parse_response(_RESPONSE_BODY_ALL_PROBLEMS1)
        self.assertDictEqual(expected, actual)

    def test_parse_response_problems2(self):
        expected = {
            LINE_RED: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_YELLOW: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_BLUE: (STATUS_DELAY, REASON_LINE_TROUBLES),
            LINE_GREEN: (STATUS_OK, REASON_NO_PROBLEM),
        }

        actual = json_backend.parse_response(_RESPONSE_BODY_ALL_PROBLEMS2)
        self.assertDictEqual(expected, actual)

    def test_parse_response_problems3(self):
        expected = {
            LINE_RED: (STATUS_DELAY, REASON_LINE_TROUBLES),
            LINE_YELLOW: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_BLUE: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_GREEN: (STATUS_OK, REASON_NO_PROBLEM),
        }

        actual = json_backend.parse_response(_RESPONSE_BODY_ALL_PROBLEMS3)
        self.assertDictEqual(expected, actual)

    def test_parse_response_problems4(self):
        expected = {
            LINE_RED: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_YELLOW: (STATUS_HALT, REASON_PASSENGER_INCIDENT),
            LINE_BLUE: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_GREEN: (STATUS_OK, REASON_NO_PROBLEM),
        }

        actual = json_backend.parse_response(_RESPONSE_BODY_ALL_PROBLEMS4)
        self.assertDictEqual(expected, actual)

    def test_parse_response_problems5(self):
        expected = {
            LINE_RED: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_YELLOW: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_BLUE: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_GREEN: (STATUS_DELAY, REASON_TRAIN_PROBLEM),
        }

        actual = json_backend.parse_response(_RESPONSE_BODY_ALL_PROBLEMS5)
        self.assertDictEqual(expected, actual)

    def test_parse_response_problems6(self):
        expected = {
            LINE_RED: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_YELLOW: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_BLUE: (STATUS_OK, REASON_NO_PROBLEM),
            LINE_GREEN: (STATUS_DELAY, REASON_TRAIN_PROBLEM),
        }

        actual = json_backend.parse_response(_RESPONSE_BODY_ALL_PROBLEMS6)
        self.assertDictEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
