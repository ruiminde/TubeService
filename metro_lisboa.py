__author__ = 'Rui'

from datetime import datetime
import logging

import requests
import requests.exceptions

import html_parser


class LineStatus(object):
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
        'está interrompida a circulação na linha entre as estações': STATUS_PARTIAL_HALT,
        'está interrompida a circulação.': STATUS_HALT,
        '__NO__MATCH__': STATUS_UNKNOWN
    }

    _REASON_KEYWORDS_MAP = {
        'existem perturbações na circulação': REASON_TROUBLES,
        'está interrompida a circulação na linha entre as estações': REASON_PARTIAL_HALT,
        'está interrompida a circulação.': REASON_HALT,
        '__NO__MATCH__': REASON_UNKNOWN
    }

    _LINE_NAMES_MAP = {
        'Linha Azul': LINE_BLUE,
        'Linha Verde': LINE_GREEN,
        'Linha Amarela': LINE_YELLOW,
        'Linha Vermelha': LINE_RED,
    }
    _http_connector = None
    _last_update = None

    _status = {
        LINE_BLUE: STATUS_UNKNOWN,
        LINE_GREEN: STATUS_UNKNOWN,
        LINE_YELLOW: STATUS_UNKNOWN,
        LINE_RED: STATUS_UNKNOWN,
    }

    def __init__(self, http_connector):
        """

        :type http_connector: Requests
        """
        self._http_connector = http_connector

    def _update_from_remote_site(self, destination_url):
        """
        Makes the HTTP request to the Metro de Lisboa website in order to get the latest status of the metro lines
        :param destination_url: URL of the Metro de Lisboa page displaying the status of the metro lines
        """

        try:
            response = self._http_connector.get(destination_url)
            logging.info("Content downloaded")

            if response.status_code != requests.codes.ok:
                raise DownloadPageError("Status code: {0}".format(response.status_code))

            self._last_update = datetime.now()
            logging.debug(response.text)
            self._status = LineStatus._parse_response(response.text)

        except (DownloadPageError, requests.exceptions.RequestException) as exception:
            logging.error("Failed the GET request to {url}".format(url=destination_url))
            logging.error("{0}".format(exception))

    @classmethod
    def _parse_response(cls, page_content):
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

        result = {cls._LINE_NAMES_MAP[parsed_line]: (
        cls._match_status_keyword(parsed_status), cls._match_reason_keyword(parsed_status))
                  for parsed_line, parsed_status in parsed.items()}
        return result

    @classmethod
    def _match_status_keyword(cls, status_message):
        for keyword, status in cls._STATUS_KEYWORDS_MAP.items():
            if keyword in status_message:
                return status
        else:
            return cls.STATUS_UNKNOWN

    @classmethod
    def _match_reason_keyword(cls, status_message):
        for keyword, reason in cls._REASON_KEYWORDS_MAP.items():
            if keyword in status_message:
                return reason
        else:
            return cls.REASON_UNKNOWN


    def get_latest(self, destination_url, line=None):
        """
        Returns the latest status of the subway lines
        :rtype : dict
        :param destination_url: URL of the Metro de Lisboa page displaying the status of the metro lines
        :return: Status of the lines
        """

        self._update_from_remote_site(destination_url)

        if line is None:
            return self._status
        else:
            return {line: self._status[line]}


class ParseError(Exception):
    pass


class DownloadPageError(Exception):
    pass
