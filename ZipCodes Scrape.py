#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#I made this code to scrape zip codes from a statistical atlas website, then created a table where each column represents a legislative district, and is populated with the zip codes in that district.


# In[1]:


from bs4 import BeautifulSoup
az_urls = ['https://statisticalatlas.com/state-lower-legislative-district/Montana/State-House-District-22/Overview',
          'https://statisticalatlas.com/state-lower-legislative-district/Montana/State-House-District-51/Overview',
          'https://statisticalatlas.com/state-lower-legislative-district/Montana/State-House-District-52/Overview',
          'https://statisticalatlas.com/state-lower-legislative-district/Montana/State-House-District-64/Overview',
          'https://statisticalatlas.com/state-lower-legislative-district/Montana/State-House-District-67/Overview',
          'https://statisticalatlas.com/state-lower-legislative-district/Montana/State-House-District-93/Overview']
districts = ['22','51','52','64','67','93']


# In[2]:


zipcodes = []
import requests
import re
for url in az_urls:
    page = requests.get(url)
    html_doc = page.content
    soup = BeautifulSoup(html_doc, 'html.parser')
    test = soup.get_text()
    listedzip = re.findall('\d{5}',test)
    zipcodes.append(listedzip)


# In[3]:


import pandas as pd
df = pd.DataFrame(zipcodes)
df = df.transpose()
df.columns = districts
df.to_csv('MT Senate.csv')


# In[ ]:




