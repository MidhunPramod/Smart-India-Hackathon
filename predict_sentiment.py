#!/usr/bin/env python
# coding: utf-8

# In[1]:


import keras 
from keras.models import load_model
model = load_model('final_model.h5')


# In[11]:


import nltk
from nltk.corpus import stopwords
import re
# import joblib
from keras.preprocessing.text import Tokenizer
import gensim
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
# from keras.layers import Embedding
# from keras.models import Sequential
# from keras.layers import Dense,LSTM,Dropout
# from sklearn.metrics import confusion_matrix,accuracy_score,classification_report
# import numpy as np # linear algebra
# import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
# import matplotlib.pyplot as plt
import pickle
import json
# %matplotlib inline
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os


# In[12]:


stop_words=set(stopwords.words('english'))
for w in ['not',"couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]:
    stop_words.remove(w)


# In[13]:


w2v_model = gensim.models.word2vec.Word2Vec(size=300, 
                                            window=7, 
                                            min_count=10, 
                                            workers=8)


# In[14]:


# w2v_model.build_vocab(documents)
with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)


# In[20]:


def preprocess(text):
    review=re.sub('@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+',' ',text)
    review=review.lower()
    review=review.split()
    review=[word for word in review if not word in stop_words]
#     print(review)
    review=pad_sequences(tokenizer.texts_to_sequences([review]), maxlen=300)
    return review


# In[21]:


def prediction(review):
    review=preprocess(review)
    score=model.predict(review)
    score=score[0]
    if score<0.4:
        print("Angry")
        return "Angry"
    elif score>0.4 and score<0.6:
        print("Sad")
        return "Sad"
    else:
        print("Neutral")
        return "Neutral"
    print(score)




# In[22]:


text = "Most of the New Jedi Order books focus on the Solo kids, to the extent that some are viewed as \"Jacen books\" or \"Jania books.\" The novella Ylesia is if anything a book starring Thrackan Sal-Solo. Thrackan is forcibly recruited by the Yuuzhan Vong to become president of the Peace Brigade Republic. However, the New Republic forces also choose to attack Ylesia. There's nothing new or terribly exciting in the novel, but it's a nice side story. It's written in a similar style as&nbsp;<a data-hook=\"product-link-linked\" class=\"a-link-normal\" href=\"/Destiny-s-Way-Star-Wars-The-New-Jedi-Order-Book-14/dp/0345428749/ref=cm_cr_arp_d_rvw_txt?ie=UTF8\">Destiny's Way (Star Wars: The New Jedi Order, Book 14)</a>, which isn't surprising as they're both by the same author. This short story actually takes place during the novel, so I'd recommend reading the novel first so Ylesia doesn't spoil any surprises."


# In[23]:


# text = preprocess(text)
"It's rare that I completely abandon a book these days. And when I do, it almost always happens on page fifty, once I've had more than enough of whatever piece of the structure I can't take any more. That didn't happen with Hades' Daughter, in part because when I reached page fifty I was locked out of the house and had no other reading material. In any case, over the past nine months, I have struggled my way through one hundred eighty-eight pages of this monstrosity, or about a third of the first book in a series, before the prose got the best of me. I can't really quote you a passage to show you why, because there aren't many passages that don't involve the kinds of subjects that would get a review censored in the places one normally posts a review. Which, honestly, usually means that book is right up my alley; have can you go wrong with almost six hundred pages of sex, violence, and combinations of the two? In short, by writing a Harlequin romance that's too violent (and long) for Harlequin to publish. The premise is interesting, but the execution leaves a great deal to be desired. I'd like to see a really, really good romance author take this on (Marjorie Liu would be a fine choice, I think), but as it stands, it's just plain silly. (zero)"


# In[26]:


#prediction(" I am highly disappointed in this institutuion, the faculty are inexperienced, they do not know how to teach. The exams were conducted in a haphazard manner")


# In[ ]:





# In[ ]:




