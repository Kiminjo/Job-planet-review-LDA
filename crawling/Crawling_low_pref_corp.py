# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 13:36:47 2020

@author: Admin
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

#%%
all_corp = pd.read_csv('all_corp.csv')

low_corps = all_corp.loc[(all_corp['cor_rating'] <= 2.1) & (all_corp['nreview'] >= 50), :][:50]
low_corps.reset_index(drop=True, inplace=True)
#%%
with open('account.json') as f:
    account = json.load(f)
#%%
member_data = {'user[email]': account['id'], 'user[password]': account['password']}
with requests.Session() as s:
    request = s.post('https://www.jobplanet.co.kr/users/sign_in?_nav=gb', data=member_data)
target_page = 'https://www.jobplanet.co.kr/companies/{}/reviews/{}?page={}&review_type=|D=cardchan@naver.com'
#%%
pattern_title = re.compile(r'\"(.+)\"')
d2 = {
      'name': [],
      'total_score': [],
      'duty': [],
      'work_status': [],
      'date': [],
      'title': [],
      'pros': [],
      'cons': [],
      'wish': [],
      'like': []
      }

for _ in range(len(low_corps)):
    page_num = low_corps['nreview'][_]//5 + 1
    for page in range(page_num):
        url = target_page.format(low_corps['cor_id'][_], low_corps['cor_name'][_], page+1)
        request = s.get(url)
        dom = BeautifulSoup(request.text, 'html.parser')
        print(dom.select_one('.company_info_box .company_name').text.strip(), page+1)
        # print(url)
        name = dom.select_one('.company_info_box a').text
        for box in dom.select('.content_wrap'):
            d2['name'].append(name)
            d2['total_score'].append(box.select_one('.star_score')['style'])
            d2['duty'].append(box.select_one('.content_top_ty2 > span:nth-of-type(2)').text)
            d2['work_status'].append(box.select_one('.content_top_ty2 > span:nth-of-type(4)').text)
            d2['date'].append(box.select_one('.content_top_ty2 .txt2').text)
            d2['title'].append(pattern_title.search(box.select_one('.us_label').text).group(1))
            d2['pros'].append(box.select_one('.merit + .df1').text.strip())
            d2['cons'].append(box.select_one('.disadvantages + .df1').text.strip())
            d2['wish'].append(box.select_one('.content_body_ty1 dd:nth-of-type(3)').text.strip())
            d2['like'].append(box.select_one('.notranslate').text)

#%%
data_low_comp = pd.DataFrame(d2)
data_low_comp.to_csv('data_low_comp.csv', encoding='utf-8-sig')




















































































































































































