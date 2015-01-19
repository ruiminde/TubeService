# -*- coding: utf-8 -*-

__author__ = 'Rui'

import logging
import json

LINE_YELLOW = 'yellow'
LINE_RED = 'red'
LINE_GREEN = 'green'
LINE_BLUE = 'blue'

STATUS_UNKNOWN = None
STATUS_OK = 'ok'
STATUS_DELAY = 'delay'
STATUS_HALT = 'halt'
STATUS_PARTIAL_HALT = 'partial_halt'

REASON_UNKNOWN = None
# REASON_TROUBLES = "There's a flood"
#REASON_PARTIAL_HALT = "Yo mama's so fat..."
#REASON_HALT = "No electricity"

_LINE_NAMES_MAP = {
    'azul': LINE_BLUE,
    'verde': LINE_GREEN,
    'amarela': LINE_YELLOW,
    'vermelha': LINE_RED,
}

_STATUS_MAP = {
    'Ok': STATUS_OK,
    '__NO__MATCH__': STATUS_UNKNOWN
}

_REASON_MAP = {
    '0': REASON_UNKNOWN
}

_REASON_LINE_MAP = {
    LINE_BLUE: 'tipo_msg_am',
    LINE_YELLOW: 'tipo_msg_az',
    LINE_GREEN: 'tipo_msg_vd',
    LINE_RED: 'tipo_msg_vm',
}


def parse_response(json_text):
    status = {}
    try:
        json_object = json.loads(json_text)

        for source_line_name, line_name in _LINE_NAMES_MAP.items():
            status_code = json_object[source_line_name]
            reason_code = json_object[_REASON_LINE_MAP[line_name]]
            line_status = _get_status(status_code)
            reason = _get_reason(reason_code)

            status[line_name] = (line_status, reason)

    except (Exception, ValueError):
        logging.error("Parse failed: {}".format(json_text))
        raise ParseError()

    return status


def _get_reason(reason_code):
    return _REASON_MAP.get(reason_code, REASON_UNKNOWN)


def _get_status(status_code):
    return _STATUS_MAP.get(status_code.strip(), STATUS_UNKNOWN)


class ParseError(Exception):
    pass
