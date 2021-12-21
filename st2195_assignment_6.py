#!/usr/bin/env python
# coding: utf-8

# # Practice Assignment 6

# ## 1. Load and merge the dataset

# In[4]:


import pandas as pd


# Loading "speeches.csv" into data frame. 
# We want to keep only the "date" and "contents" columns.
# Merging multiple rows for the same day in "speeches".

# In[5]:


speeches = pd.read_csv("speeches.csv", sep='|', usecols=['date','contents'])
speeches.dropna(inplace=True)
speeches = speeches.groupby("date")['contents'].apply(lambda x: " ".join(x.astype(str))).reset_index()
speeches


# Loading "fx.csv" into data frame.

# In[6]:


fx = pd.read_csv("fx.csv", skiprows=4, na_values=['-'])
fx.columns = ["date","exchange_rate"]
fx


# Merging the data together.

# In[9]:


df = pd.merge(fx, speeches, how='left')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace= True)
df


# ## 2. Remove entries with obvious outliers or mistakes

# We first see if there is any obvious outliers or mistakes by plotting the data:

# In[10]:


df.plot(kind="line", xlabel="date", ylabel="EUR/USD reference exchange rate")


# And look at the summary statistics:

# In[11]:


df.describe()


# The data does not seem to have obvious outliers or mistakes, but there are 62 missing data.

# In[12]:


df.isna().sum()
#for missing exchange rate values, we don't delete it. 
#use bfill to fill the NA values - fill NA with the previous value


# ## 3.	Handle missing observations
# 
# Fill in the exchange rate with the latest information available.
# There is no more missing data for exchange rate.

# In[13]:


df.exchange_rate.fillna(method='bfill', inplace=True)
df.isna().sum()


# 
# ## 4. Calculate the exchange rate return
# 
# Get the return by using the formula: $R_{t} = \frac{P_{t}-P_{t-1}}{P_{t-1}}$

# In[14]:


df['return'] = df.exchange_rate.diff(-1)/df.exchange_rate


# Extend the original dataset with the variables "good_news" and "bad_news":

# In[15]:


df['good_news'] = (df['return'] > 0.5/100).astype(int)
df['bad_news'] = (df['return'] < -0.5/100).astype(int)


# In[16]:


df


# ## 5. Remove the entries for which contents is NA

# In[17]:


df.dropna(inplace=True)
df


# ## 5a/b. Generate and store `good_indicators` and `bad_indicators`
# 
# Load in some stop words, which are words that used to form a sentence but does not add much meaning to a sentence. Example of stop words are "a", "the" "does", "i", etc. 

# In[22]:


#conda install nltk 
#nltk - natural language organizer
#nltk.download('stopwords')

import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
stop_words


# The function below get the most common words (excluding stop_words) related to `good_news` and `bad_news`:

# In[24]:


import string
import collections

#tokenizing here

#num_words=number of words u want to return
def get_word_freq(contents, stop_words, num_words):
    freq = dict()    #create a dictionary called "freq"
    for word in contents.split():
        word = word.strip(string.punctuation+'–')
        word = word.lower()                            #convert into lower case 
        if word not in stop_words and len(word):
            if word in freq:
                #value is the count of the word in the dictionary
                freq[word] += 1
            else:
                freq[word] = 1
    freq = dict(sorted(freq.items(), key = lambda item: -item[1]))    #sort in descending order
    return list(freq.keys())[:num_words]      #return list from 0 to 19


# Use the function above to get the 20 most common words associated with `good_news` and `bad_news`

# In[25]:


# get the contents related to "good_news" and "bad_news"
good_news_contents = df.contents[df.good_news==1].str.cat(sep=' ')  #cat: joining with a separator
bad_news_contents = df.contents[df.bad_news==1].str.cat(sep=' ')

good_indicators = get_word_freq(good_news_contents, stop_words, num_words = 20)
bad_indicators = get_word_freq(bad_news_contents, stop_words, num_words = 20)


# In[26]:


good_indicators


# In[27]:


bad_indicators


# ##### use write() to write these into a csv file

# Note that many terms appear in both, and the results are not the same as R. It may because the `word_tokenizer()` in R may not work the same way as `split()` with `strip()`.
