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
df = pd.read_csv('D:/GoogleDriveSync/011. Unstructured data analysis/프로젝트/UnstructuredData_Project/data.csv')
#%% 전처리
df.rename(columns={'Unnamed: 0': 'reviewidx'}, inplace=True)
df.replace('width:100%;', 5, inplace=True)
df.replace('width:80%;', 4, inplace=True)
df.replace('width:60%;', 3, inplace=True)
df.replace('width:40%;', 2, inplace=True)
df.replace('width:20%;', 1, inplace=True)
pros = df['pros']
pros_j = '. '.join([_ for _ in df['pros']])
pros_j = pros_j.replace('\r', '')
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
kkma = Kkma()
d = {
     'pros':[]
     }
for i, _ in enumerate(df['pros']):
    print(i)
    tokens = kkma.pos(_)
    # print(tokens)
    d['pros'].append(' '.join([n[0] for n in tokens if n[1].startswith('N')]))
#%%
from konlpy.corpus import kobill
docs_ko = [kobill.open(i).read() for i in kobill.fileids()]
docs_ko
#%%
from konlpy.tag import Twitter; t = Twitter()
pos = lambda d: ['/'.join(p) for p in t.pos(d, stem=True, norm=True)]
texts_ko = [pos(doc) for doc in docs_ko]
print(texts_ko[0])
#%%
from gensim import corpora
dictionary_ko = corpora.Dictionary(texts_ko)
dictionary_ko.save('ko.dict')  # save dictionary to file for future use
#%%
from gensim import models
tf_ko = [dictionary_ko.doc2bow(text) for text in texts_ko]
tfidf_model_ko = models.TfidfModel(tf_ko)
tfidf_ko = tfidf_model_ko[tf_ko]
corpora.MmCorpus.serialize('ko.mm', tfidf_ko) # save corpus to file for future use

# print first 10 elements of first document's tf-idf vector
print(tfidf_ko.corpus[0][:10])
# print top 10 elements of first document's tf-idf vector
print(sorted(tfidf_ko.corpus[0], key=lambda x: x[1], reverse=True)[:10])
# print token of most frequent element
print(dictionary_ko.get(414))
#%%
import numpy as np; np.random.seed(42)  # optional
lda_ko = models.ldamodel.LdaModel(tfidf_ko, id2word=dictionary_ko, num_topics=ntopics)
print(lda_ko.print_topics(num_topics=ntopics, num_words=nwords))
#%%
ntopics, nwords = 3, 5
#%%
bow = tfidf_model_ko[dictionary_ko.doc2bow(texts_ko[0])]
print(sorted(lda_ko[bow], key=lambda x: x[1], reverse=True))
#%%
bow = tfidf_model_ko[dictionary_ko.doc2bow(texts_ko[1])]
print(sorted(lda_ko[bow], key=lambda x: x[1], reverse=True))
    
