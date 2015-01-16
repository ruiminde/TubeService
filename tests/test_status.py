from unittest import TestCase
from unittest.mock import MagicMock
import logging

import requests.exceptions

from metro_lisboa import LineStatus


__author__ = 'Rui'

logging.basicConfig(level=logging.INFO)

class TestLineStatus(TestCase):
    metro_lisboa = None
    url = "http://metrolisboa.pt/status_linha"

    def setUp(self):
        self.metro_lisboa = LineStatus(MagicMock(), MagicMock())

    def test_get_status_404(self):
        response_mock = MagicMock()
        response_mock.status_code = 404
        response_mock.text = None

        self.metro_lisboa._http_connector.get.return_value = response_mock

        previous_status = self.metro_lisboa._status
        self.metro_lisboa._update_from_remote_site(self.url)

        self.assertEqual(previous_status, self.metro_lisboa._status)

    def test_get_status_requests_exception(self):
        response_mock = MagicMock()
        response_mock.status_code = None
        response_mock.text = None

        self.metro_lisboa._http_connector.get.side_effect = requests.exceptions.ConnectTimeout(
            "Requests: Connection timeout")

        previous_status = self.metro_lisboa._status
        self.metro_lisboa._update_from_remote_site(self.url)

        self.assertEqual(previous_status, self.metro_lisboa._status)


