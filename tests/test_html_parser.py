__author__ = 'XEST167'

from unittest import TestCase

import html_parser


_RESPONSE_ALL_OK = """
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

_RESPONSE_PROBLEMS_BLUE = """
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

_RESPONSE_BODY_PROBLEMS_STATION = """
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


class TestHTMLParser(TestCase):
    def test_get_line_status_all_ok(self):
        expected = {
            'Linha Vermelha': 'Circulação normal',
            'Linha Amarela': 'Circulação normal',
            'Linha Azul': 'Circulação normal',
            'Linha Verde': 'Circulação normal'
        }

        actual = html_parser.get_line_status(_RESPONSE_ALL_OK)
        self.assertDictEqual(expected, actual)

    def test_get_line_status_problem_blue(self):
        expected = {
            'Linha Vermelha': 'Circulação normal',
            'Linha Amarela': 'Circulação normal',
            'Linha Azul': 'existem perturbações na circulação. O tempo de espera pode ser superior ao normal. Pedimos desculpa pelo incómodo causado',
            'Linha Verde': 'Circulação normal'
        }

        actual = html_parser.get_line_status(_RESPONSE_PROBLEMS_BLUE)
        self.assertDictEqual(expected, actual)

    def test_get_line_status_problem_station(self):
        expected = {
            'Linha Vermelha': 'Circulação normal',
            'Linha Amarela': 'Circulação normal',
            'Linha Azul': 'Circulação normal',
            'Linha Verde': 'Devido a anomalia na estação está interrompida a circulação na linha entre as estações  Cais do Sodré e Martim Moniz. Não é possível prever a duração da interrupção, que poderá ser prolongada. Pedimos desculpa pelo incómodo causado'
        }

        actual = html_parser.get_line_status(_RESPONSE_BODY_PROBLEMS_STATION)
        self.assertDictEqual(expected, actual)