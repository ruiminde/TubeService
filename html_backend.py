# -*- coding: utf-8 -*-

__author__ = 'Rui'

import logging

import html_parser


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
REASON_TROUBLES = "There's a flood"
REASON_PARTIAL_HALT = "Yo mama's so fat..."
REASON_HALT = "No electricity"

_STATUS_KEYWORDS_MAP = {
    'Circulação normal': STATUS_OK,
    'existem perturbações na circulação': STATUS_DELAY,
    'a circulação encontra-se com perturbações': STATUS_DELAY,
    'está interrompida a circulação na linha entre as estações': STATUS_PARTIAL_HALT,
    'está interrompida a circulação.': STATUS_HALT,
    'a circulação está interrompida': STATUS_HALT,
    '__NO__MATCH__': STATUS_UNKNOWN
}

_REASON_KEYWORDS_MAP = {
    'existem perturbações na circulação': REASON_TROUBLES,
    'a circulação encontra-se com perturbações': REASON_TROUBLES,
    'está interrompida a circulação na linha entre as estações': REASON_PARTIAL_HALT,
    'está interrompida a circulação.': REASON_HALT,
    'a circulação está interrompida': REASON_HALT,
    '__NO__MATCH__': REASON_UNKNOWN
}

_LINE_NAMES_MAP = {
    'Linha Azul': LINE_BLUE,
    'Linha Verde': LINE_GREEN,
    'Linha Amarela': LINE_YELLOW,
    'Linha Vermelha': LINE_RED,
}


def parse_response(page_content):
    """
    Parse the HTML text and return the dictionary with the status of the lines
    :rtype : dict
    :param page_content: HTML text to be parsed
    """

    try:
        parsed = html_parser.get_line_status(str(page_content))

    except Exception:
        raise ParseError()

    if not isinstance(parsed, dict):
        logging.error("Parse failed")
        raise ParseError()

    result = {_LINE_NAMES_MAP[parsed_line]: (
        _match_status_keyword(parsed_status), _match_reason_keyword(parsed_status))
              for parsed_line, parsed_status in parsed.items()}
    return result


def _match_status_keyword(status_message):
    for keyword, status in _STATUS_KEYWORDS_MAP.items():
        if keyword in status_message:
            return status
    else:
        return STATUS_UNKNOWN


def _match_reason_keyword(status_message):
    for keyword, reason in _REASON_KEYWORDS_MAP.items():
        if keyword in status_message:
            return reason
    else:
        return REASON_UNKNOWN


class ParseError(Exception):
    pass
