# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 22:24:11 2020

@author: Admin
"""
#%% 패키지 import
import os
import pandas as pd
from konlpy.tag import Kkma, Twitter, Hannanum
from collections import Counter
from gensim import models
print(os.getcwd())
#%% 데이터 불러오기
high_df = pd.read_csv('D:/GoogleDriveSync/011. Unstructured data analysis/프로젝트/UnstructuredData_Project/data.csv')
low_df = pd.read_csv('D:/GoogleDriveSync/011. Unstructured data analysis/프로젝트/UnstructuredData_Project/data_low_comp.csv')
#%% high corporation 전처리
high_df.rename(columns={'Unnamed: 0': 'reviewidx'}, inplace=True)
high_df.replace('width:100%;', 5, inplace=True)
high_df.replace('width:80%;', 4, inplace=True)
high_df.replace('width:60%;', 3, inplace=True)
high_df.replace('width:40%;', 2, inplace=True)
high_df.replace('width:20%;', 1, inplace=True)
# pros = df['pros']
# pros_j = '. '.join([_ for _ in df['pros']])
# pros_j = pros_j.replace('\r', '')

#%% low corporation 전처리
low_df.rename(columns={'Unnamed: 0': 'reviewidx'}, inplace=True)
low_df.replace('width:100%;', 5, inplace=True)
low_df.replace('width:80%;', 4, inplace=True)
low_df.replace('width:60%;', 3, inplace=True)
low_df.replace('width:40%;', 2, inplace=True)
low_df.replace('width:20%;', 1, inplace=True)
# pros = df['pros']
# pros_j = '. '.join([_ for _ in df['pros']])
# pros_j = pros_j.replace('\r', '')
#%%
pos_taggers = [('kkma', Kkma()), ('twitter', Twitter()), ('hannanum', Hannanum())]
for name, tagger in pos_taggers:
    tokens = tagger.pos(pros_j)
    counter = Counter(tokens)
    counter = {word:freq for word, freq in counter.items() if (freq >= 4) and (word[1][:1] == 'N')}
    print(sorted(counter.items(), key=lambda x:x[1], reverse=True)[:50])
    compare.append(sorted(counter.items(), key=lambda x:x[1], reverse=True)[:50])

#%%
for name, tagger in pos_taggers:
    tokens = tagger.pos(pros_j)
    # print([n for n in pos_kkma if n[1].startswith('N')])
    Counter(tokens)
    print(tokens[])
counter = Counter(tokens[0])

pprint(sorted(counter.items(), key=lambda x:x[1], reverse=True))
#%%
high_pros = high_df.groupby('name')['pros'].apply(lambda x: ','.join(x))
low_pros = low_df.groupby('name')['pros'].apply(lambda x: ','.join(x))
high_cons = high_df.groupby('name')['cons'].apply(lambda x: ','.join(x))
low_cons = low_df.groupby('name')['cons'].apply(lambda x: ','.join(x))
#%%

kkma = Kkma()
twitter = Twitter()
high_dict = {
     'pros':[],
     'cons':[]
     }
low_dict = {
     'pros':[],
     'cons':[]
     }
for i, _ in enumerate(high_pros):
    print(i)
    tokens = twitter.pos(_)
    # print(tokens)
    high_dict['pros'].append([n[0] for n in tokens if n[1].startswith('N') or n[1].startswith('A')])
for i, _ in enumerate(low_pros):
    print(i)
    tokens = twitter.pos(_)
    # print(tokens)
    low_dict['pros'].append([n[0] for n in tokens if n[1].startswith('N') or n[1].startswith('A')])
for i, _ in enumerate(high_cons):
    print(i)
    tokens = twitter.pos(_)
    # print(tokens)
    high_dict['cons'].append([n[0] for n in tokens if n[1].startswith('N') or n[1].startswith('A')])
for i, _ in enumerate(low_cons):
    print(i)
    tokens = twitter.pos(_)
    # print(tokens)
    low_dict['cons'].append([n[0] for n in tokens if n[1].startswith('N') or n[1].startswith('A')])
#%%
from gensim import corpora
dictionary_high_cons = corpora.Dictionary(high_dict['pros'])
#%%
from gensim import models
tf_high_cons = [dictionary_high_cons.doc2bow(text) for text in high_dict['pros']]
tfidf_model_high_cons = models.TfidfModel(tf_high_cons)
tfidf_high_cons = tfidf_model_high_cons[tf_high_cons]
print(tfidf_high_cons.corpus[3][:10])
print(sorted(tfidf_high_cons.corpus[0], key=lambda x: x[1], reverse=True)[:10])
print(dictionary_high_cons.get(1))
#%%
ntopics, nwords = 3, 5
#%%
import numpy as np; np.random.seed(42)  # optional
lda_ko = models.ldamodel.LdaModel(tfidf_high_cons, id2word=dictionary_high_cons, num_topics=ntopics)
print(lda_ko.print_topics(num_topics=ntopics, num_words=nwords))

#%%
bow = tfidf_model_high_cons[dictionary_high_cons.doc2bow(high_dict['pros'][0])]
print(sorted(lda_ko[bow], key=lambda x: x[1], reverse=True))
#%%
bow = tfidf_model_high_cons[dictionary_high_cons.doc2bow(high_dict['pros'][1])]
print(sorted(lda_ko[bow], key=lambda x: x[1], reverse=True))
    



















































































































































