#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Piemonte data downloader and parser
"""

import pandas as pd
import re
import urllib

from bs4 import BeautifulSoup


def get_PM10_csv():
    """
    Return a csv containing the latest 10 days of measurament of Piemonte air quality (PM10)

    Data origin: ARPA Piemonte
    Website: http://www.arpa.piemonte.it/approfondimenti/temi-ambientali/aria/aria/dati-giornalieri-di-particolato-pm10
    """

    url = 'http://www.arpa.piemonte.it/rischinaturali/dati_stazioni_pm10.html'
    html_doc = urllib.request.urlopen(url).read()

    html_soup = BeautifulSoup(html_doc, "lxml")
    table_script = html_soup.findAll("script")[4]
    js_table = re.search("(?<=TabellaQaPM10Dati_var = ).*?(?=;)", table_script.text).group()

    # TODO: Refactor/beautify
    js_table = js_table.replace('<rows>', '<table>')
    js_table = js_table.replace('</rows>', '</table>')
    js_table = js_table.replace('<row>', '<tr>')
    js_table = js_table.replace('</row>', '</tr>')
    js_table = js_table.replace('<cell>', '<td>')
    js_table = js_table.replace('</cell>', '</td>')
    pd_table = pd.read_html(js_table)[0]
    pd_table = pd_table.drop(pd_table.columns[[0, 2, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]], axis=1)
    pd_table = pd_table.drop(pd_table.index[[-1]])
    pd_table.at[0, 1] = 'Stazione'
    header = pd_table.iloc[0]
    pd_table = pd_table[1:]
    pd_table = pd_table.rename(columns=header)

    return pd_table.to_csv()
