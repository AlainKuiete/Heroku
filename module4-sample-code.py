#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# This module we'll be looking at the New York City tree census. This data was provided by a volunteer driven census in 2015, and we'll be accessing it via the socrata API. The main site for the data is [here](https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh), and on the upper right hand side you'll be able to see the link to the API.
# 
# The data is conveniently available in json format, so we should be able to just read it directly in to Pandas:

# In[2]:


url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
trees = pd.read_json(url)
trees.head(10)


# Looks good, but lets take a look at the shape of this data:

# In[3]:


trees.shape


# 1000 seems like too few trees for a city like New York, and a suspiciously round number. What's going on?
# 
# Socrata places a 1000 row limit on their API. Raw data is meant to be "paged" through for applications, with the expectation that a UX wouldn't be able to handle a full dataset. 
# 
# As a simple example, if we had a mobile app with limited space that only displayed trees 5 at a time, we could view the first 5 trees in the dataset with the url below:

# In[4]:


firstfive_url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=5&$offset=0'
firstfive_trees = pd.read_json(firstfive_url)
firstfive_trees


# If we wanted the next 5, we would use this url:

# In[5]:


nextfive_url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=5&$offset=5'
nextfive_trees = pd.read_json(nextfive_url)
nextfive_trees


# You can read more about paging using the Socrata API [here](https://dev.socrata.com/docs/paging.html)
# 
# In these docs, you'll also see more advanced functions (called `SoQL`) under the "filtering and query" section. These functions should be reminding you of SQL.
# 
# Think about the shape you want your data to be in before querying it. Using `SoQL` is a good way to avoid the limits of the API. For example, using the below query I can easily obtain the count of each species of tree in the Bronx:

# In[6]:


boro = 'Bronx'
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +        '$select=spc_common,count(tree_id)' +        '&$where=boroname=\'Bronx\'' +        '&$group=spc_common').replace(' ', '%20')
soql_trees = pd.read_json(soql_url)

soql_trees


# This behavior is very common with web APIs, and I think this is useful when thinking about building interactive data products. When in a Jupyter Notebook or RStudio, there's an expectation that (unless you're dealing with truly large datasets) the data you want can be brought in memory and manipulated.
# 
# Dash and Shiny abstract away the need to distinguish between client side and server side to make web development more accessible to data scientists. This can lead to some unintentional design mistakes if you don't think about how costly your callback functions are (for example: nothing will stop you in dash from running a costly model triggered whenever a dropdown is called.)
# 
# The goal of using the Socrata is to force you to think about where your data operations are happening, and not resort to pulling in the data and performing all operations in local memory.
# 
# ----------
# 
# **NOTE**: One tip in dealing with URLs: you may need to replace spaces with `'%20'`. I personally just write out the url and then follow the string with a replace:

# In[10]:


'https://api-url.com/?query with spaces'.replace(' ', '%20')


# In[ ]:




