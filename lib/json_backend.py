# -*- coding: utf-8 -*-

__author__ = 'Rui'

import logging
import json

from tubeservice.datacontract import *


_LINE_NAMES_MAP = {
    'azul': LINE_BLUE,
    'verde': LINE_GREEN,
    'amarela': LINE_YELLOW,
    'vermelha': LINE_RED,
}

_STATUS_MAP = {
    '0': STATUS_OK,
    '1': STATUS_DELAY,
    '3': STATUS_HALT,
    '__NO__MATCH__': STATUS_UNKNOWN
}

_REASON_MAP = {
    'existem perturbações na circulação. O tempo de espera pode ser superior ao normal.': REASON_LINE_TROUBLES,
    'Devido a incidente com passageiro': REASON_PASSENGER_INCIDENT,
    'Devido a avaria de comboio': REASON_TRAIN_PROBLEM,
    ' Ok': REASON_NO_PROBLEM,
}

_STATUS_LINE_MAP = {
    LINE_BLUE: 'tipo_msg_az',
    LINE_YELLOW: 'tipo_msg_am',
    LINE_GREEN: 'tipo_msg_vd',
    LINE_RED: 'tipo_msg_vm',
}


def parse_response(json_text):
    status = {}
    try:
        json_object = json.loads(json_text)

        for source_line_name, line_name in _LINE_NAMES_MAP.items():
            reason_code = json_object[source_line_name]
            status_code = json_object[_STATUS_LINE_MAP[line_name]]
            line_status = _get_status(status_code)
            reason = _get_reason(reason_code)

            status[line_name] = (line_status, reason)

    except (Exception, ValueError):
        logging.error("Parse failed: {}".format(json_text))
        raise ParseError()

    return status


def _get_reason(reason_code):
    for reason_key, reason in _REASON_MAP.items():
        if reason_key in reason_code:
            return reason
    else:
        return REASON_UNKNOWN


def _get_status(status_code):
    return _STATUS_MAP.get(status_code.strip(), STATUS_UNKNOWN)


class ParseError(Exception):
    pass
