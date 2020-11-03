# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 22:19:19 2020

@author: Injo Kim

Seoultech data science 
Unstructured data class project

Crawling reviews from top 50 companies with high satisfaction in Job planet
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

"""""""""""""""""
Get top 50 companies list with high satisfaction.
13 companies are excluded from the analsis, so crawling up to 63rd.(crawling to page 7)
"""""""""""""""""

def get_company_list(last_page) :

    company_list = []
    company_id = []
    for page in range(1,last_page+1) :
        
        url = 'https://www.jobplanet.co.kr/companies?sort_by=review_avg_cache&industry_id=700&page='
        request = requests.get(url+str(page)).text
        soup = BeautifulSoup(request, 'html.parser')
        
        for company in soup.body.find_all('dt', class_='us_titb_l3') :
            company_name = company.getText()
            company_list.append(company_name)
            company_id.append(company.button['data-company_id'])
    
    companies = pd.DataFrame({'name' : company_list, 'id' : company_id})
            
    return companies



def get_number_of_reviews_per_company(last_page) :
    
    review_list = []
    for page in range(1, last_page+1) :
        
        url = 'https://www.jobplanet.co.kr/companies?sort_by=review_avg_cache&industry_id=700&page='
        request = requests.get(url+str(page)).text
        soup = BeautifulSoup(request, 'html.parser')
        
        for review in soup.body.find_all('dd', class_='row_end') :
            review_list.append(review.getText())

    return review_list
    

    
    
    

company_list= get_company_list(last_page=7)
review_list = get_number_of_reviews_per_company(last_page=7)
