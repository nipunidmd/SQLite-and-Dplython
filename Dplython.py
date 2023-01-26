#!/usr/bin/env python
# coding: utf-8

# In[1]:

# load packages
from dplython import (DplyFrame, X, diamonds, select, count, sift,
  sample_n, sample_frac, head, arrange, mutate, group_by,
  summarize, DelayFunction)


# In[2]:


import pandas as pd


# In[3]:

# read in data
names = ['AAGE',  'ACLSWKR', 'ADTIND', 'ADTOCC','AHGA', 'AHRSPAY', 'AHSCOL','AMARITL',  'AMJIND', 'AMJOCC', 'ARACE','AREORGN', 'ASEX', 'AUNMEM','AUNTYPE',  'AWKSTAT', 'CAPGAIN', 'CAPLOSS','DIVVAL', 'FILESTAT', 'GRINREG','GRINST',  'HDFMX', 'HHDREL', 'MARSUPWT','MIGMTR1', 'MIGMTR3', 'MIGMTR4','MIGSAME',  'MIGSUN', 'NOEMP', 'PARENT','PEFNTVTY', 'PEMNTVTY', 'PENATVTY','PRCITSHP',  'SEOTR', 'VETQVA', 'VETYN','WKSWORK', 'YEAR', 'TRGT']
df = pd.read_csv('census-income.data',sep=',', names=names)


# In[4]:


df


# In[5]:

# adding SS_ID
df = df.reset_index()
df = df.rename(columns={"index":"SS_ID"})
df['SS_ID'] = df.index + 1
df


# In[6]:

# convert to DplyFrame object
info = DplyFrame(df)


# In[7]:

# Question 3
(info >>group_by(X.ARACE,X.ASEX)>>count(X.ASEX))


# In[8]:

# Question 4
annual_inc_race = info>>group_by(X.ARACE)>>sift(X.AHRSPAY!=0) >> mutate(annual_inc=(X.WKSWORK*X.AHRSPAY*40).mean()//1)
annual_inc_race


# In[9]:

# Question 5 - 1
Person = df[['SS_ID', 'AAGE', 'AHGA', 'ASEX', 'PRCITSHP', 'PARENT', 'GRINST', 'GRINREG', 'AREORGN', 'AWKSTAT']].copy()


# In[10]:


Person


# In[11]:

# Question 5 - 2
Job = df[['SS_ID', 'ADTIND', 'ADTOCC', 'AMJOCC', 'AMJIND']].copy()


# In[12]:


Job


# In[13]:

# Question 5 - 3
Pay = df[['SS_ID', 'AHRSPAY', 'WKSWORK']].copy()


# In[14]:


Pay


# In[15]:

# Combine dataframes
df_com = pd.concat([Person, Job, Pay], axis=1)


# In[16]:

# avoid duplicate columns
df_com = df_com.loc[:,~df_com.columns.duplicated()]


# In[17]:


df_com


# In[18]:

# convert to Dplyframe object
info_com = DplyFrame(df_com)


# In[19]:

# Question 6-1
info_com >> group_by(X.GRINST)>> summarize(highest_hourly_wage = X.AHRSPAY.max(),no_of_people = X.GRINST.count(),job_type=X.ADTIND.max(),major_industry=X.ADTOCC.max())


# In[ ]:

# Question 6-2
info_com >> group_by(X.AMJIND,X.AHGA)>>arrange(X.AHGA)>>sift((X.AREORGN.isin(["Cuban", "Mexican-American","Central or South American","Puerto Rican","Other Spanish","Mexican (Mexicano)"]))&(X.AHGA.isin(["Bachelors degree(BA AB BS)", "Masters degree(MA MS MEng MEd MSW MBA)","Doctorate degree(PhD EdD)"])))>>summarize(avg_hourly_pay = X.AHRSPAY.mean()//1,avg_weeks_work = X.WKSWORK.mean()//1,hispanic_count=X.AREORGN.count())

