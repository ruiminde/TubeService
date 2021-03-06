# -*- coding: utf-8 -*-
__author__ = 'Rui'

import unittest
from unittest import TestCase
import logging

from tubeservice.datacontract import *
from lib import html_backend


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

_RESPONSE_BODY_PROBLEMS_STATION1 = """
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
<tr><td style="color:white;background-color:#00A9A6;padding-left:3px;height: 20px;"><b>Linha Verde</b></td><td><ul id="ticker03"><li>Devido a anomalia na estação está interrompida a circulação na linha entre as estações  Cais do Sodré e Martim Moniz. Não é possível prever a duração da interrupção, que poderá ser prolongada. Pedimos desculpa pelo incómodo causado</li></ul></td></tr>
<tr><td style="color:white;background-color:#ED2B74;padding-left:3px;height: 20px;"><b>Linha Vermelha</b></td><td><ul class="semperturbacao"><li>Circula&ccedil;&atilde;o normal</li></ul></td></tr></table></body>
"""

_RESPONSE_BODY_PROBLEMS_STATION2 = """
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
<tr><td style="color:white;background-color:#ED2B74;padding-left:3px;height: 20px;"><b>Linha Vermelha</b></td><td><ul id="ticker04"><li>Devido a causa alheia ao Metro está interrompida a circulação. Não é possível prever a duração da interrupção, que poderá ser prolongada. Pedimos desculpa pelo incómodo causado</li></ul></td></tr></table></body>
"""

_RESPONSE_BODY_PROBLEMS_STATION3 = """
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
<tr><td style="color:white;background-color:#4E84C4;padding-left:3px;height: 20px;"><b>Linha Azul</b></td><td><ul id="ticker02"><li>Devido a avaria na sinalização está interrompida a circulação. Não é possível prever a duração da interrupção, que poderá ser prolongada. Pedimos desculpa pelo incómodo causado</li></ul></td></tr>
<tr><td style="color:white;background-color:#00A9A6;padding-left:3px;height: 20px;"><b>Linha Verde</b></td><td><ul class="semperturbacao"><li>Circula&ccedil;&atilde;o normal</li></ul></td></tr>
<tr><td style="color:white;background-color:#ED2B74;padding-left:3px;height: 20px;"><b>Linha Vermelha</b></td><td><ul class="semperturbacao"><li>Circula&ccedil;&atilde;o normal</li></ul></td></tr></table></body>
"""

_RESPONSE_BODY_PROBLEMS_STATION4 = """
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
<tr><td style="color:white;background-color:#4E84C4;padding-left:3px;height: 20px;"><b>Linha Azul</b></td><td><ul id="ticker02"><li>devido a avaria na sinalização, a circulação encontra-se com perturbações. O tempo de espera pode ser superior ao normal. Pedimos desculpa pelo incómodo</li></ul></td></tr>
<tr><td style="color:white;background-color:#00A9A6;padding-left:3px;height: 20px;"><b>Linha Verde</b></td><td><ul class="semperturbacao"><li>Circula&ccedil;&atilde;o normal</li></ul></td></tr>
<tr><td style="color:white;background-color:#ED2B74;padding-left:3px;height: 20px;"><b>Linha Vermelha</b></td><td><ul class="semperturbacao"><li>Circula&ccedil;&atilde;o normal</li></ul></td></tr></table></body>
"""

_RESPONSE_BODY_PROBLEMS_STATION5 = """
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
<tr><td style="color:white;background-color:#4E84C4;padding-left:3px;height: 20px;"><b>Linha Azul</b></td><td><ul id="ticker02"><li>Devido a incidente com passageiro, a circulação está interrompida desde as 07:50. Esperamos retomar a circulação num período inferior a 15 minutos. Pedimos desculpa pelo incómodo</li></ul></td></tr>
<tr><td style="color:white;background-color:#00A9A6;padding-left:3px;height: 20px;"><b>Linha Verde</b></td><td><ul class="semperturbacao"><li>Circula&ccedil;&atilde;o normal</li></ul></td></tr>
<tr><td style="color:white;background-color:#ED2B74;padding-left:3px;height: 20px;"><b>Linha Vermelha</b></td><td><ul class="semperturbacao"><li>Circula&ccedil;&atilde;o normal</li></ul></td></tr></table></body>
"""

logging.basicConfig(level=logging.INFO)


class TestHTMLBackend(TestCase):
    def test_parse_response_all_ok(self):
        expected = {
            LINE_RED: (STATUS_OK, None),
            LINE_YELLOW: (STATUS_OK, None),
            LINE_BLUE: (STATUS_OK, None),
            LINE_GREEN: (STATUS_OK, None),
        }

        actual = html_backend.parse_response(_RESPONSE_BODY_ALL_OK)
        self.assertDictEqual(expected, actual)

    def test_parse_response_problems_blue(self):
        expected = {
            LINE_RED: (STATUS_OK, None),
            LINE_YELLOW: (STATUS_OK, None),
            LINE_BLUE: (STATUS_DELAY, html_backend.REASON_TROUBLES),
            LINE_GREEN: (STATUS_OK, None),
        }
        actual = html_backend.parse_response(_RESPONSE_BODY_PROBLEMS_BLUE)
        self.assertDictEqual(expected, actual)


    def test_parse_response_station_problems1(self):
        expected = {
            LINE_RED: (STATUS_OK, None),
            LINE_YELLOW: (STATUS_OK, None),
            LINE_BLUE: (STATUS_OK, None),
            LINE_GREEN: (STATUS_PARTIAL_HALT, html_backend.REASON_PARTIAL_HALT),
        }

        actual = html_backend.parse_response(_RESPONSE_BODY_PROBLEMS_STATION1)
        self.assertDictEqual(expected, actual)


    def test_parse_response_station_problems2(self):
        expected = {
            LINE_RED: (STATUS_HALT, html_backend.REASON_HALT),
            LINE_YELLOW: (STATUS_OK, None),
            LINE_BLUE: (STATUS_OK, None),
            LINE_GREEN: (STATUS_OK, None),
        }

        actual = html_backend.parse_response(_RESPONSE_BODY_PROBLEMS_STATION2)
        self.assertDictEqual(expected, actual)

    def test_parse_response_station_problems3(self):
        expected = {
            LINE_RED: (STATUS_OK, None),
            LINE_YELLOW: (STATUS_OK, None),
            LINE_BLUE: (STATUS_HALT, html_backend.REASON_HALT),
            LINE_GREEN: (STATUS_OK, None),
        }

        actual = html_backend.parse_response(_RESPONSE_BODY_PROBLEMS_STATION3)
        self.assertDictEqual(expected, actual)


    def test_parse_response_station_problems4(self):
        expected = {
            LINE_RED: (STATUS_OK, None),
            LINE_YELLOW: (STATUS_OK, None),
            LINE_BLUE: (STATUS_DELAY, html_backend.REASON_TROUBLES),
            LINE_GREEN: (STATUS_OK, None),
        }

        actual = html_backend.parse_response(_RESPONSE_BODY_PROBLEMS_STATION4)
        self.assertDictEqual(expected, actual)

    def test_parse_response_station_problems5(self):
        expected = {
            LINE_RED: (STATUS_OK, None),
            LINE_YELLOW: (STATUS_OK, None),
            LINE_BLUE: (STATUS_HALT, html_backend.REASON_HALT),
            LINE_GREEN: (STATUS_OK, None),
        }

        actual = html_backend.parse_response(_RESPONSE_BODY_PROBLEMS_STATION5)
        self.assertDictEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
