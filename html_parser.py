# -*- coding: utf-8 -*-

__author__ = 'XEST167'

from bs4 import BeautifulSoup


def get_line_status(html_content):
    """
    :rtype : dict
    :param html_content: HTML content to be parsed
    :return: the dictionary with the lines
    """
    soup = BeautifulSoup(html_content)

    yellow_line_tr = soup.table.tr
    assert 'Linha Amarela' == next(
        yellow_line_tr.td.stripped_strings), "Parsing html failed on 'Linha Amarela' assertion"
    yellow_line_status = next(yellow_line_tr.td.next_sibling.stripped_strings)

    blue_line_tr = yellow_line_tr.next_sibling.next_sibling
    assert 'Linha Azul' == next(blue_line_tr.td.stripped_strings), "Parsing html failed on 'Linha Azul' assertion"
    blue_line_status = next(blue_line_tr.td.next_sibling.stripped_strings)

    green_line_tr = blue_line_tr.next_sibling.next_sibling
    assert 'Linha Verde' == next(green_line_tr.td.stripped_strings), "Parsing html failed on 'Linha Verde' assertion"
    green_line_status = next(green_line_tr.td.next_sibling.stripped_strings)

    red_line_tr = green_line_tr.next_sibling.next_sibling
    assert 'Linha Vermelha' == next(
        red_line_tr.td.stripped_strings), "Parsing html failed on 'Linha Vermelha' assertion"
    red_line_status = next(red_line_tr.td.next_sibling.stripped_strings)

    return {
        'Linha Amarela': yellow_line_status,
        'Linha Azul': blue_line_status,
        'Linha Verde': green_line_status,
        'Linha Vermelha': red_line_status
    }