# -*- coding: utf-8 -*-
"""
Created on Mon May  3 19:26:29 2021

@author: yatsk
"""
import requests
import json
from bs4 import BeautifulSoup

import pandas as pd



url = 'https://fbref.com/en/squads/8e306dc6/Gotham-FC-Stats'
soup = BeautifulSoup(requests.get(url).content, 'html.parser')

table = soup.select_one('table[id^="stats_standard"]')
ptab = pd.read_html(url, header=1)[0]