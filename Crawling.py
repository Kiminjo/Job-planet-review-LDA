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
import webbrowser

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
            """
            remove word 'following', empty space and (str) using regular expression
            """
            company_name = re.compile('[a-z]{9}').sub('', company_name)
            company_name = re.compile('\s+').sub('', company_name)
            company_name = re.compile('\(.\)').sub('', company_name)
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
            """
            remove all empty space and remain first numbers
            """
            num_of_review = review.getText()
            num_of_review = re.compile('\s+').sub('', num_of_review)
            num_of_review = re.compile('^[0-9]{1,}').search(num_of_review).group()
            review_list.append(int(num_of_review))

    return review_list
    

def target_company(num_of_company=50) :
    
    company_list = get_company_list(last_page=7)
    company_list['number_of_review'] = get_number_of_reviews_per_company(last_page=7)
    
    """
    As a prior knowledge, '구카카오' is a non-existent, so remove it 
    Remove companies with more than 200 review
    Extract top 50 companies
    """
    company_list = company_list[company_list['name'] != '구카카오']    
    company_list = company_list[company_list['number_of_review'] < 200].iloc[:50, :]
        
    return company_list


if __name__ == "__main__" :
    target_companies = target_company()
    
    # for test, opening the list of top '페이스북 코리아'
    url = 'https://www.jobplanet.co.kr/companies/{}/reviews/{}'.format(target_companies.id[0], target_companies.name[0])
    webbrowser.open(url, new=1)