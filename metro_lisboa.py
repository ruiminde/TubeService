# -*- coding: utf-8 -*-

__author__ = 'Rui'

from datetime import datetime
import logging

import requests
import requests.exceptions


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

    _http_connector = None
    _backend = None
    _last_update = None

    _status = {
        LINE_BLUE: STATUS_UNKNOWN,
        LINE_GREEN: STATUS_UNKNOWN,
        LINE_YELLOW: STATUS_UNKNOWN,
        LINE_RED: STATUS_UNKNOWN,
    }

    def __init__(self, http_connector, backend):
        """

        :type http_connector: Requests
        :param backend: Module to be used to process the content from the metro website
        """
        self._http_connector = http_connector
        self._backend = backend

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
            self._status = self._backend.parse_response(response.text)

        except (DownloadPageError, requests.exceptions.RequestException) as exception:
            logging.error("Failed the GET request to {url}".format(url=destination_url))
            logging.error("{0}".format(exception))

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


class DownloadPageError(Exception):
    pass
