__author__ = 'Rui'

from datetime import datetime
import logging

import requests


class Status(object):
    _requests = None
    _status = {'red': None, 'green': None, 'blue': None, 'yellow': None}
    _last_update = None

    def __init__(self, requests):
        self._requests = requests

    def update_from_remote_site(self, destination_url):
        result = self._requests.get(destination_url)
        if result.status_code == requests.codes.ok:
            self._last_update = datetime.now()
            logging.debug(result.text)

    def get_latest(self):
        return self._status