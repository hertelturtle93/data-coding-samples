#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Here I wanted to provide an example of importing, cleaning, and merging data. I used two census sources, at the 'place' level to create a new table of income and education data.


# In[2]:


import pandas as pd
income = pd.read_csv('IncomeData.csv',header=1)
income = income.filter(regex = "^Geo|^Estimate!!Households!!M")
income[['City','State']] = income['Geographic Area Name'].apply(lambda x: pd.Series(str(x).split(",")))
income.columns = income.columns.str.replace('Estimate!!','')
income.columns = income.columns.str.replace('!!Total!!',' ')
income.columns = income.columns.str.replace(':','')
income.columns = income.columns.str.replace('!!',' ')
income = income.astype({'Households Median income (dollars)':'int'})
income.dtypes


# In[3]:


income['Households Mean income (dollars)'] = pd.to_numeric(income['Households Mean income (dollars)'],errors = 'coerce')
income.dtypes


# In[4]:


education = pd.read_csv('EducationData.csv',header=1)
education = education.filter(regex = "^Geo|^Estimate!!Total!!AGE")
education = education.drop(columns = ['Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 18 to 24 years','Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 25 years and over',
 'Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Less than 9th grade',
 'Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 25 years and over!!9th to 12th grade, no diploma',
 'Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate (includes equivalency)',
 'Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Some college, no degree',
 "Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Associate's degree",
 "Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Bachelor's degree",
 'Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Graduate or professional degree',
 'Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate or higher',
 "Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Bachelor's degree or higher",
 'Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 25 to 34 years', 'Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 25 to 34 years', 'Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 35 to 44 years', 'Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 45 to 64 years', 'Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population 65 years and over',])


# In[5]:


education[['City','State']] = education['Geographic Area Name'].apply(lambda x: pd.Series(str(x).split(",")))
education.columns = education.columns.str.replace('Estimate!!Total!!AGE BY EDUCATIONAL ATTAINMENT!!Population ','')
list(education.columns)


# In[6]:


cols = ['18 to 24 years!!Less than high school graduate',
 '18 to 24 years!!High school graduate (includes equivalency)',
 "18 to 24 years!!Some college or associate's degree",
 "18 to 24 years!!Bachelor's degree or higher",
 '25 to 34 years!!High school graduate or higher',
 "25 to 34 years!!Bachelor's degree or higher",
 '35 to 44 years!!High school graduate or higher',
 "35 to 44 years!!Bachelor's degree or higher",
 '45 to 64 years!!High school graduate or higher',
 "45 to 64 years!!Bachelor's degree or higher",
 '65 years and over!!High school graduate or higher',
 "65 years and over!!Bachelor's degree or higher"]
education[cols] = education[cols].apply(pd.to_numeric, errors ='coerce')


# In[7]:


education["High School Grad or Higher"] = education['18 to 24 years!!High school graduate (includes equivalency)'] + education['25 to 34 years!!High school graduate or higher'] + education['35 to 44 years!!High school graduate or higher'] + education['45 to 64 years!!High school graduate or higher'] + education['65 years and over!!High school graduate or higher']
education["Bachelor's Degree or Higher"] = education["18 to 24 years!!Bachelor's degree or higher"] + education["25 to 34 years!!Bachelor's degree or higher"] + education["35 to 44 years!!Bachelor's degree or higher"] + education["45 to 64 years!!Bachelor's degree or higher"] + education["65 years and over!!Bachelor's degree or higher"]
education["Some College"] = education["18 to 24 years!!Some college or associate's degree"]
education["Less than High School"] = education['18 to 24 years!!Less than high school graduate']


# In[8]:


education = education.iloc[:,[0,14,15,16,17,18,19]]


# In[9]:


incomeedu = pd.merge(income,education,how = 'outer',on = 'Geography')
incomeedu = incomeedu.drop(columns = ['City_x','State_x','Geographic Area Name'])


# In[10]:


cols = ["Households Median income (dollars)","Households Mean income (dollars)","High School Grad or Higher","Bachelor's Degree or Higher","Some College","Less than High School"]


# In[11]:


bystate = incomeedu.groupby('State_y')[cols].sum()


# In[12]:


bystate


# In[ ]:




