__author__ = 'Rui'

from datetime import datetime
import logging

import requests


class Status(object):
    _http_connector = None
    _status = {'red': None, 'green': None, 'blue': None, 'yellow': None}
    _last_update = None

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
        result = self._http_connector.get(destination_url)
        if result.status_code != requests.codes.ok:
            logging.error("Failed the GET request to {url}".format(url=destination_url))
            logging.error("HTTP status {status}".format(status=result.status_code))
            logging.debug(result.text)
            return

        else:
            logging.info("Content downloaded")
            self._last_update = datetime.now()
            logging.debug(result.text)
            self._update_status(result.text)

    def _update_status(self, page_content):
        pass

    def get_latest(self, destination_url):
        """
        Returns the latest status of the subway lines
        :rtype : Dict
        :param destination_url: URL of the Metro de Lisboa page displaying the status of the metro lines
        :return: Status of the lines
        """
        self._update_from_remote_site(destination_url)
        return self._status