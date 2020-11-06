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

class top50_companies :    
    
    def get_company_list(self, last_page) :
    
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
    
    
    
    def get_number_of_reviews_per_company(self, last_page) :
        
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
        
    
    def target_company(self, num_of_company=50) :
        
        company_list = self.get_company_list(last_page=7)
        company_list['number_of_review'] = self.get_number_of_reviews_per_company(last_page=7)
        
        """
        '구카카오', '구글 코리아', '오케이몰', '데브시스터즈' and '유디피' remove.
        Remove companies with more than 200 review
        Extract top 50 companies
        """
        company_list = company_list[company_list['name'] != '구카카오']
        company_list = company_list[company_list['name'] != '구글코리아']
        company_list = company_list[company_list['name'] != '유디피']
        company_list = company_list[company_list['name'] != '오케이몰']       
        company_list = company_list[company_list['name'] != '데브시스터즈']               
        company_list = company_list[company_list['number_of_review'] < 200].iloc[:num_of_company, :]
        company_list = company_list.reset_index(drop=True)
        
        company_list['number_of_review_page'] = [0] * len(company_list)
        for idx in range(len(company_list)) :
            company_list['number_of_review_page'][idx] = company_list['number_of_review'][idx]//5 + 1
        
        return company_list



class crawling_reviews :
    
    def __init__(self, companies):
        self.email = 'cardchan@naver.com'
        self.pw = 'fjrzlaos22'
        self.target_page = 'https://www.jobplanet.co.kr/companies/{}/reviews/{}?page={}&review_type=|D=cardchan@naver.com'
        self.companies = companies
        self.total_score_list = []
        self.duty_list = []
        self.work_status_list = []
        self.date_list = []
        self.title_list = []
        self.pros_list = []
        self.cons_list = []
        self.wish_list = []
        self.like_list = []
        
        
    def list_initialize(self) :
        self.total_score_list = []
        self.duty_list = []
        self.work_status_list = []
        self.date_list = []
        self.title_list = []
        self.pros_list = []
        self.cons_list = []
        self.wish_list = []
        self.like_list = []
                
        
    def login(self) :
        member_data = {'user[email]' : self.email, 'user[password]' : self.pw}

        with requests.Session() as s :
            request = s.post('https://www.jobplanet.co.kr/users/sign_in?_nav=gb', data = member_data)
        
        return request, s
    
    def total_score(self, req, total_score_list) :
        total_score_list.append(req.find_all('div', class_='star_score')[0]['style'])
        return total_score_list
            
    
    def get_duties(self, req, duty_list) :
        duty_list.append(req.find_all('span', class_='txt1')[0].getText())
        return duty_list
    
    
    def get_work_status(self, req, work_status_list) :
        work_status_list.append(req.find_all('span', class_='txt1')[1].getText())
        return work_status_list
    
    def get_date(self, req, date_list) :
        date_list.append(req.find_all('span', class_='txt2')[0].getText())
        return date_list
    
    def get_title(self, req, title_list) :
        title_list.append(req.find_all('h2', class_='us_label')[0].getText())
        return title_list
    
    def get_pros(self, req, pros_list) :
        pros_list.append(req.find_all('dd', class_='df1')[0].getText())
        return pros_list
    
    def get_cons(self, req, cons_list) :
        cons_list.append(req.find_all('dd', class_='df1')[1].getText())
        return cons_list
    
    def get_wish_list(self, req, wish_list) :
        wish_list.append(req.find_all('dd', class_='df1')[2].getText())
        return wish_list
    
    def get_like(self, req, like_list) :
        like_list.append(req.find_all('span', class_='notranslate')[0].getText())
        return like_list
    
    
    def crawling(self) :
        
        request, s = self.login()
        data = pd.DataFrame(columns = ['name' ,'total_score' ,'duty' ,'work_state'  ,'date' ,'title' ,'pros' ,'cons', 
                                       'wish', 'like'])
        
        for company_idx in range(len(self.companies)) :
            self.list_initialize()
            
            for page in range(self.companies.number_of_review_page[company_idx]) :
                request = self.target_page.format(self.companies.id[company_idx], self.companies.name[company_idx], page+1)
                request = s.get(request)
                soup = BeautifulSoup(request.text, 'html.parser')
                
                if page+1 < self.companies.number_of_review_page[company_idx] :
                    for idx in range(5) :
                        review_box = soup.find_all('div', class_='content_wrap')[idx]
                        print('0--------------------------- {}'.format(self.companies.name[company_idx]))
                    
                        self.total_score_list = self.total_score(review_box, self.total_score_list)
                        self.duty_list = self.get_duties(review_box, self.duty_list)
                        self.work_status_list = self.get_work_status(review_box, self.work_status_list)
                        self.date_list = self.get_date(review_box, self.date_list)
                        self.title_list = self.get_title(review_box, self.title_list)
                        self.pros_list = self.get_pros(review_box, self.pros_list)
                        self.cons_list = self.get_cons(review_box, self.cons_list)
                        self.wish_list = self.get_wish_list(review_box, self.wish_list)
                        self.like_list = self.get_like(review_box, self.like_list)
                
                else :
                    for idx in range(self.companies.number_of_review[company_idx]%5) :
                        review_box = soup.find_all('div', class_='content_wrap')[idx]
                        print('1--------------------------{}'.format(self.companies.name[company_idx]))
                        
                        self.total_score_list = self.total_score(review_box, self.total_score_list)
                        self.duty_list = self.get_duties(review_box, self.duty_list)
                        self.work_status_list = self.get_work_status(review_box, self.work_status_list)
                        self.date_list = self.get_date(review_box, self.date_list)
                        self.title_list = self.get_title(review_box, self.title_list)
                        self.pros_list = self.get_pros(review_box, self.pros_list)
                        self.cons_list = self.get_cons(review_box, self.cons_list)
                        self.wish_list = self.get_wish_list(review_box, self.wish_list)
                        self.like_list = self.get_like(review_box, self.like_list)
            

    
            df = pd.DataFrame({'name' : self.companies.name[company_idx], 'total_score' : self.total_score_list, 
                               'duty' : self.duty_list, 'work_state' : self.work_status_list,'date' : self.date_list, 
                               'title' : self.title_list, 'pros' : self.pros_list, 'cons' : self.cons_list,
                               'wish' : self.wish_list, 'like' : self.like_list})
            
            data = pd.concat([data, df], axis=0)
        
        return data
    

if __name__ == "__main__" :
    top50 = top50_companies()
    target_companies = top50.target_company()
    
    crawling = crawling_reviews(target_companies)
    data = crawling.crawling()
    



"""""""""""
승진 기회 및 가능성, 복지 및 급여, 업무와 삶의 균형 등을 크롤링하면 안되는 이유
"""""""""""

url = 'https://www.jobplanet.co.kr/companies/90364/reviews/%ED%8E%98%EC%9D%B4%EC%8A%A4%EB%B6%81%EC%BD%94%EB%A6%AC%EC%95%84?page=3&review_type='
req = requests.get(url).text
soup = BeautifulSoup(req, 'html.parser')

        
soup.find_all('div', class_='bl_score')[0]
soup.find_all('div', class_='star_score')[3]

