#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyam

get_ipython().run_line_magic('matplotlib', 'inline')


# In[5]:


df = pyam.IamDataFrame(data='tutorial_AR5_data.csv', encoding='utf-8')


# In[6]:


df.models()


# In[7]:


df.regions()


# In[8]:


df.variables(include_units=True)


# In[9]:


df.filter(model='MESSAGE').models()


# In[10]:


df.filter(model='MESSAGE*')[['model', 'scenario']].drop_duplicates()


# In[11]:


df.filter(region="World", keep=False).regions()


# In[12]:


df.filter(variable='Emissions|*').variables()


# In[13]:


df.filter(variable='Emissions|*', level=1).variables()


# In[14]:


df.filter(variable='Emissions|*', level='1-').variables()


# In[15]:


df.filter(level='1-').variables()


# In[16]:


get_ipython().run_line_magic('pinfo', 'df.filter')


# In[17]:


(df
 .filter(scenario='AMPERE3-450', variable='Primary Energy|Coal', region='World')
 .timeseries()
)


# In[18]:


(df
 .filter(variable='Primary Energy', region='World')
 .pivot_table(index=['year'], columns=['scenario'], values='value', aggfunc='sum')
)


# In[19]:


df.head()


# In[20]:


df.filter(variable='Emissions|CO2', region='World').line_plot(legend=False)


# In[21]:


df.require_variable(variable='Primary Energy')


# In[22]:


df.validate(criteria={'Primary Energy': {'up': 515, 'year': 2010}})


# In[23]:


pyam.validate(df.filter(region='World', scenario='AMPERE*'),
              criteria={'Primary Energy|Coal': {'up': 400, 'year': 2050}}
)


# In[24]:


v = 'Temperature|Global Mean|MAGICC6|MED'
df.filter(region='World', variable=v).line_plot(legend=False)


# In[25]:


df.set_meta(meta='uncategorized', name='Temperature')


# In[26]:


df.categorize(
    'Temperature', 'Below 1.6C',
    criteria={v: {'up': 1.6, 'year': 2100}},
    color='cornflowerblue'
)


# In[27]:


df.categorize(
    'Temperature', 'Below 2.0C',
    criteria={'Temperature|Global Mean|MAGICC6|MED': {'up': 2.0, 'lo': 1.6, 'year': 2100}},
    color='forestgreen'
)


# In[28]:


df.categorize(
    'Temperature', 'Below 2.5C',
    criteria={v: {'up': 2.5, 'lo': 2.0, 'year': 2100}},
    color='gold'
)


# In[29]:


df.categorize(
    'Temperature', 'Below 3.5C',
     criteria={v: {'up': 3.5, 'lo': 2.5, 'year': 2100}},
     color='firebrick'
)


# In[30]:


df.categorize(
    'Temperature', 'Above 3.5C',
    criteria={v: {'lo': 3.5, 'year': 2100}},
    color='magenta'
)


# In[31]:


df.require_variable(variable=v, exclude_on_fail=False)


# In[32]:


df.filter(variable=v).line_plot(color='Temperature', legend=True)


# In[33]:


fig, ax = plt.subplots()
(df
 .filter(variable='Emissions|CO2', region='World')
 .line_plot(ax=ax, color='Temperature', legend=True)
)
fig.savefig('co2_emissions.png')


# In[34]:


eoc = 'End-of-century-temperature'
df.set_meta_from_data(name='End-of-century-temperature', variable=v, year=2100)


# In[35]:


peak = 'Peak-temperature'
df.set_meta_from_data(name='Peak-temperature', variable=v, method=np.max)


# In[36]:


overshoot = df.meta[peak] - df.meta[eoc]


# In[37]:


df.set_meta(name='Overshoot', meta=overshoot)


# In[38]:


df.filter(Temperature='Below 2.0C').meta.head()


# In[40]:


df.to_excel('tutorial_export.xlsx')
df.export_metadata('tutorial_metadata.xlsx')

