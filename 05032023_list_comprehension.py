#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
random.randint(1,5)


# In[2]:


x=[]
for _ in range(0,10):
    x.append(random.randint(1,5))
x    


# In[3]:


x=[random.randint(1,5) for _ in range(0,10)]
x


# In[4]:


y=[]
for val in x:
    if val<3:
        y.append(val)
y        


# In[5]:


y=[val for val in x if val<3]
y


# In[6]:


import os
excel=[i for i in os.listdir() if '.xlsx' in i]
excel[0]


# In[7]:


import pandas as pd
pd.ExcelFile(excel[0]).sheet_names[0]


# In[8]:


df = pd.read_excel(excel[0], sheet_name=pd.ExcelFile(excel[0]).sheet_names[0],usecols="A:T", skiprows=[0,1], header=0,index_col='Level')
df.columns


# ### Join in Python is an in-built method used to join an iterable’s elements, separated by a string separator, which is specified by you. Thus, whenever you want to join the elements of an iterable and make it a string, you can use the string join in Python.

# In[14]:


import random
col_list=['#'+''.join([random.choice('0123456789ABCDEF') for _ in range(0,6)]) for _ in range(0,19)]
len(col_list)


# In[10]:


import matplotlib.pyplot as plt
fig,ax=plt.subplots()
fig.set_size_inches(14,4)
range(len(col_list))
ax.bar(range(len(col_list)),[10 for _ in range(len(col_list))],color=col_list)


# In[11]:


x1=[random.randint(1,5) for _ in range(0,10)]
x2=[random.randint(1,5) for _ in range(0,10)]
x3=[random.randint(1,5) for _ in range(0,10)]
plt.plot(x1,col_list[0])
plt.plot(x2,col_list[1])
plt.plot(x3,col_list[2])
plt.legend([x1,x2,x3])
plt.show()


# In[12]:


df.columns
df.loc[:,1]
y=[yval for yval in df[2] if pd.isna(yval)==False]
x=df[2].index.values[:len(y)]
plt.plot(x,y,linestyle='--',marker='o',linewidth=0.2,color=col_list[2])


# In[29]:


temp=df.columns.to_list()
for col in df.columns:
    y=[yval for yval in df[col] if pd.isna(yval)==False]
    x=df[col].index.values[:len(y)]    
    plt.plot(x,y,linestyle='--',marker='o',linewidth=0.2,color=col_list[temp.index(col)])
plt.legend(df.columns,prop={'family':'Century Gothic','size': 9},bbox_to_anchor=(1.2,1),loc='upper right')    
plt.show()
len(temp)

