# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 02:49:14 2020

@author: Admin
"""

import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from requests.compat import urlparse, urljoin
import pandas as pd
import re
from requests.exceptions import HTTPError
import time
#%%


def canfetch(url, agent='*', path='/'):
    robot = RobotFileParser(urljoin(url, '/robots.txt'))
    robot.read()
    return robot.can_fetch(agent, urlparse(url)[2])


def download(url, params={}, headers={}, method='GET', limit=3):
    if canfetch(url) is False:
        print('[Error] ' + url)
#     else:
    try:
        resp = requests.request(method,
                                url,
                                params=params if method == 'GET' else {},
                                data=params if method == 'POST' else {},
                                headers=headers)
        resp.raise_for_status()
    except HTTPError as e:
        if limit > 0 and e.response.status_code >= 500:
            print(limit)
            time.sleep(1)  # => random
            resp = download(url, params, headers, method, limit-1)
        else:
            print('[{}] '.format(e.response.status_code) + url)
            print(e.response.status_code)
            print(e.response.reason)
            print(e.response.headers)
    return resp
#%%


url = 'https://www.jobplanet.co.kr/companies'
params = {
    'sort_by': 'review_avg_cache',
    'industry_id': '700',
    'page': ''
    }
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/\
    537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
resp = download(url, params, headers, 'GET')
dom = BeautifulSoup(resp.content, 'html.parser')
#%%
pages_last = 113
d = {
    'cor_ids': [],
    'cor_names': [],
    'cor_ratings': [],
    'nreviews': []
    }
pattern_d = re.compile(r'[\d]+')

for p in range(1, pages_last+1):
    params['page'] = str(p)
    resp = download(url, params, headers, 'GET')
    dom = BeautifulSoup(resp.content, 'html.parser')
    print(p)
    for _ in dom.select('.content_wrap'):
        d['cor_ids'].append(_.select_one('.btn_heart1')['data-company_id'])
        d['cor_names'].append(_.select_one('.us_titb_l3 > a').text)  # 기업명
        d['cor_ratings'].append(float(_.select_one('.gfvalue').text))  # 평점
        nreview_s = _.select_one('.row_end a').text  # 리뷰 수 문자열(ex. 137 기업리뷰)
        d['nreviews'].append(int(pattern_d.search(nreview_s).group()))  # 리뷰 수(137, int형)
        
#%%
all_corp = pd.DataFrame(d)
# all_corp.to_csv('all_corp.csv', encoding='utf-8-sig')