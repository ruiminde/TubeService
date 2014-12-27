from unittest import TestCase
from unittest.mock import MagicMock
import logging

import requests.exceptions

from metro_lisboa import LineStatus


__author__ = 'Rui'

_RESPONSE_BODY_ALL_OK = """
<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<meta charset="UTF-8" />
<script type="text/javascript" src="jquery-1.4.2.min.js"></script>
<script type="text/javascript" src="jquery.li-scroller.1.0.js"></script>
<link rel="stylesheet" href="li-scroller.css" type="text/css" media="screen">
<script type="text/javascript"> $(function(){ $("ul#ticker01").liScroll({travelocity: 0.03});
$("ul#ticker02").liScroll({travelocity: 0.03});
$("ul#ticker03").liScroll({travelocity: 0.03});
$("ul#ticker04").liScroll({travelocity: 0.03});
});
</script>
<SCRIPT>
function refreshPeriodic() {
   // Reload the page every 60 seconds
   location.reload();
   timerID = setTimeout("refreshPeriodic()",60000);
}
timerID = setTimeout("refreshPeriodic()",60000);
</SCRIPT>
</head>
<body>
<table cellpadding=0 cellspacing=0 style="font-family:Arial;">
<tr><td style="color:white;background-color:#FDB813;padding-left:3px;" width=120><b>Linha Amarela</b></td><td style="align">
<ul class="semperturbacao"><li>Circula&ccedil;&atilde;o normal</li></ul></td></tr>
<tr><td style="color:white;background-color:#4E84C4;padding-left:3px;height: 20px;"><b>Linha Azul</b></td><td><ul class="semperturbacao"><li>Circula&ccedil;&atilde;o normal</li></ul></td></tr>
<tr><td style="color:white;background-color:#00A9A6;padding-left:3px;height: 20px;"><b>Linha Verde</b></td><td><ul class="semperturbacao"><li>Circula&ccedil;&atilde;o normal</li></ul></td></tr>
<tr><td style="color:white;background-color:#ED2B74;padding-left:3px;height: 20px;"><b>Linha Vermelha</b></td><td><ul class="semperturbacao"><li>Circula&ccedil;&atilde;o normal</li></ul></td></tr></table></body>
"""

_RESPONSE_BODY_PROBLEMS_BLUE = """
<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<meta charset="UTF-8" />
<script type="text/javascript" src="jquery-1.4.2.min.js"></script>
<script type="text/javascript" src="jquery.li-scroller.1.0.js"></script>
<link rel="stylesheet" href="li-scroller.css" type="text/css" media="screen">
<script type="text/javascript"> $(function(){ $("ul#ticker01").liScroll({travelocity: 0.03});
$("ul#ticker02").liScroll({travelocity: 0.03});
$("ul#ticker03").liScroll({travelocity: 0.03});
$("ul#ticker04").liScroll({travelocity: 0.03});
});
</script>
<SCRIPT>
function refreshPeriodic() {
   // Reload the page every 60 seconds
   location.reload();
   timerID = setTimeout("refreshPeriodic()",60000);
}
timerID = setTimeout("refreshPeriodic()",60000);
</SCRIPT>
</head>
<body>
<table cellpadding=0 cellspacing=0 style="font-family:Arial;">
<tr><td style="color:white;background-color:#FDB813;padding-left:3px;" width=120><b>Linha Amarela</b></td><td style="align">
<ul class="semperturbacao"><li>Circula&ccedil;&atilde;o normal</li></ul></td></tr>
<tr><td style="color:white;background-color:#4E84C4;padding-left:3px;height: 20px;"><b>Linha Azul</b></td><td><ul id="ticker02"><li>existem perturbações na circulação. O tempo de espera pode ser superior ao normal. Pedimos desculpa pelo incómodo causado</li></ul></td></tr>
<tr><td style="color:white;background-color:#00A9A6;padding-left:3px;height: 20px;"><b>Linha Verde</b></td><td><ul class="semperturbacao"><li>Circula&ccedil;&atilde;o normal</li></ul></td></tr>
<tr><td style="color:white;background-color:#ED2B74;padding-left:3px;height: 20px;"><b>Linha Vermelha</b></td><td><ul class="semperturbacao"><li>Circula&ccedil;&atilde;o normal</li></ul></td></tr></table></body>
"""

logging.basicConfig(level=logging.INFO)

class TestLineStatus(TestCase):
    metro_lisboa = None
    url = "http://metrolisboa.pt/status_linha"

    def setUp(self):
        self.metro_lisboa = LineStatus(MagicMock())

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

    def test_get_status_all_ok(self):
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.text = _RESPONSE_BODY_ALL_OK
        self.metro_lisboa._http_connector.get.return_value = response_mock

        self.metro_lisboa._update_from_remote_site(self.url)

        self.metro_lisboa._http_connector.get.assert_called_once_with(self.url)
        self.assertIsNotNone(self.metro_lisboa._last_update)

        expected = {
            LineStatus.LINE_RED: LineStatus.STATUS_OK,
            LineStatus.LINE_YELLOW: LineStatus.STATUS_OK,
            LineStatus.LINE_BLUE: LineStatus.STATUS_OK,
            LineStatus.LINE_GREEN: LineStatus.STATUS_OK,
        }

        self.assertDictEqual(expected, self.metro_lisboa._status)

    def test_get_status_problems_blue(self):
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.text = _RESPONSE_BODY_PROBLEMS_BLUE
        self.metro_lisboa._http_connector.get.return_value = response_mock

        self.metro_lisboa._update_from_remote_site(self.url)

        self.metro_lisboa._http_connector.get.assert_called_once_with(self.url)
        self.assertIsNotNone(self.metro_lisboa._last_update)

        expected = {
            LineStatus.LINE_RED: LineStatus.STATUS_OK,
            LineStatus.LINE_YELLOW: LineStatus.STATUS_OK,
            LineStatus.LINE_BLUE: LineStatus.STATUS_DELAY,
            LineStatus.LINE_GREEN: LineStatus.STATUS_OK,
        }

        self.assertDictEqual(expected, self.metro_lisboa._status)

    def test_parse_response_all_ok(self):
        expected = {
            LineStatus.LINE_RED: LineStatus.STATUS_OK,
            LineStatus.LINE_YELLOW: LineStatus.STATUS_OK,
            LineStatus.LINE_BLUE: LineStatus.STATUS_OK,
            LineStatus.LINE_GREEN: LineStatus.STATUS_OK,
        }
        actual = LineStatus._parse_response(_RESPONSE_BODY_ALL_OK)
        self.assertDictEqual(expected, actual)

    def test_parse_response_problems_blue(self):
        expected = {
            LineStatus.LINE_RED: LineStatus.STATUS_OK,
            LineStatus.LINE_YELLOW: LineStatus.STATUS_OK,
            LineStatus.LINE_BLUE: LineStatus.STATUS_DELAY,
            LineStatus.LINE_GREEN: LineStatus.STATUS_OK,
        }
        actual = LineStatus._parse_response(_RESPONSE_BODY_PROBLEMS_BLUE)
        self.assertDictEqual(expected, actual)

    def test_get_latest(self):
        self.fail("Test not implemented")