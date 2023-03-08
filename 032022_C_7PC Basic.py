#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('python -m pip install openpyxl')


# In[5]:


get_ipython().system('python -m pip install xlrd')


# In[2]:


import pandas as pd
import os

file_name = [i for i in os.listdir() if '.xlsx' in i][0]
print(file_name)
xlsx = pd.ExcelFile(file_name)
worksheet_names = xlsx.sheet_names
print(worksheet_names[0])


# In[3]:


df = pd.read_excel(file_name, sheet_name=worksheet_names[0],usecols="A:T", skiprows=[0,1], header=0,index_col='Level')
df=df.fillna(0)
df.info()
df.dtypes.unique()[1]


# In[4]:


float_columns = df.columns[df.dtypes == df.dtypes.unique()[1]].tolist()
df[float_columns[0]]


# In[5]:


df[float_columns] = df[float_columns].apply(lambda x: x.astype(int))
df


# In[6]:


import matplotlib.pyplot as plt
plt.figure(figsize=(10,5))
yval=[y for y in df[1] if y!=0]
plt.plot(df.index.values[:len(yval)],yval,color='red',marker='o',linestyle='--'
            ,markersize=4,linewidth=0.2)
plt.text(df.index.values[:len(yval)][-1]+.2,yval[-1],str(1)+'-Level',fontsize=6,rotation=15)    
plt.grid()
plt.ylabel('Basic Pay',fontname='Century Gothic',fontsize=16,fontweight='bold')
plt.xlabel('Stages Within Level',fontname='Century Gothic',fontsize=16,fontweight='bold')
plt.show()


# This code uses a list comprehension to create the list of 18 random colors. Inside the list comprehension, it uses a nested for loop. The outer loop runs 18 times, and the inner loop generates a random 6-character string made up of characters from the set '0123456789ABCDEF', which are the characters that can appear in a HTML color code. The outer loop combines these 6-character strings with a "#" to create the full color code.

# In[14]:


import random
import matplotlib.pyplot as plt

colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(df.columns))]
# create a figure and axes
fig, ax = plt.subplots()
fig.set_size_inches(14,1)
# plot the bars
ax.bar(range(len(colors)), [.5 for _ in range(len(colors))], color=colors)

# set the x-axis labels
ax.set_xticks(range(len(colors)))
ax.set_xticklabels(colors,rotation=60)
# display the plot
plt.show()


# In[15]:


plt.figure(figsize=(10,5))
for col in df.columns.to_list():
    yval=[y for y in df[col] if y!=0]
    plt.plot(df.index.values[:len(yval)],yval,color=colors[df.columns.to_list().index(col)],marker='o',linestyle='--'
            ,markersize=4,linewidth=0.2)
    plt.text(df.index.values[:len(yval)][-1]+.2,yval[-1],str(col)+'-Level',fontsize=6,rotation=15)    
plt.legend(df.columns.to_list(),bbox_to_anchor=(1.2,1.02),loc='upper right')
plt.grid()
plt.ylabel('Basic Pay',fontname='Century Gothic',fontsize=16,fontweight='bold')
plt.xlabel('Stages Within Level',fontname='Century Gothic',fontsize=16,fontweight='bold')
plt.show()


# # Takeaways
# * Level-13 is a huge jump
# * Level-1 to 5 very little change in Salary
# * The graphs appear to be parabolic instead of straight lines-This is to be investigated by taking a log

# In[16]:


import numpy as np
logy=np.log(df[10]).to_list()
plt.figure(figsize=(2.5,2.5))
plt.plot([i for i in range(len(logy))],logy,color=colors[10],marker='*',markersize=2,linestyle='')
plt.show()
slope=(100*(logy[len(logy)-1]-logy[0])/len(logy))
print(f'The SLOPE of the line, which corresponds to annual increment is {round(slope,1)}')


# # Assuming the Approx. log(1+r)=r
# * Holds for small r
# * log(1+r)=r-r^2/2+r^3/3 and so on
# * here .3^2/2 is .09/2 or .045- Basically too small

# In[17]:


df.tail()


# In[18]:


#Creating another dataframe
logdf=df
for col in float_columns:
    max_val=logdf[col].max()
    logdf[col].replace(0,max_val,inplace=True)
plt.figure(figsize=(20,20))
for col in logdf.columns.to_list():    
    plt.plot(logdf.index.values,logdf[col],color=colors[logdf.columns.to_list().index(col)],marker='o',linestyle='--'
            ,markersize=10,linewidth=0.2)
    if ((logdf.columns.to_list().index(col))<11):
        plt.text(logdf.index.values[39]+0.5,logdf.loc[40,col],str(col)+'-Level',fontsize=16,rotation=0)
    else:
        plt.text(logdf.index.values[0]-3.5,logdf.loc[1,col],str(col)+'-Level',fontsize=16,rotation=0)
plt.legend(logdf.columns.to_list(),prop={'size': 25},bbox_to_anchor=(1.2,1),loc='upper right')
plt.grid()
plt.ylabel('Basic Pay',fontname='Century Gothic',fontsize=30,fontweight='bold')
plt.xlabel('Stages Within Level',fontname='Century Gothic',fontsize=30,fontweight='bold')
plt.xticks(np.arange(0,41,1),fontsize=16)
plt.yticks(np.arange(15000,260000,10000),fontsize=16)
plt.xlim((-5, 45))
plt.ylim(logdf.min().min()-5000,logdf.max().max()+10000)
plt.show()


# # Log Graphs of all the Pay Levels

# In[19]:


import numpy as np
#Copy to avoid changing the orginal DF
slope_df = logdf
slope_df = slope_df.apply(np.log)

plt.figure(figsize=(20,20))
for col in slope_df.columns.to_list():
    slope_index=slope_df.columns.to_list().index(col)
    plt.plot(slope_df.index.values,slope_df[col],color=colors[slope_index],marker='o',linestyle='--'
            ,markersize=10,linewidth=0.2)
    if (slope_index<11):
        plt.text(slope_df.index.values[39]+0.5,slope_df.loc[40,col],str(col)+'-Level',fontsize=16,rotation=0)
        #Plotting the Slope
        slope=(100*(slope_df.loc[40,col]-slope_df.loc[1,col])/40)
        plt.text(slope_df.index.values[15]-0.5,slope_df.loc[15,col]+.04,'Slope is:'+str(round(slope,1)),
                 fontsize=10,rotation=100-round(np.rad2deg(np.arctan(3)),0))
        
    else:
        plt.text(slope_df.index.values[0]-3.5,slope_df.loc[1,col],str(col)+'-Level',fontsize=16,rotation=0) 

plt.legend(slope_df.columns.to_list(),prop={'size': 25},bbox_to_anchor=(1.2,1),loc='upper right')
plt.grid()
plt.ylabel('Log of Basic Pay',fontname='Century Gothic',fontsize=30,fontweight='bold')
plt.xlabel('Stages Within Level',fontname='Century Gothic',fontsize=30,fontweight='bold')
plt.xticks(np.arange(0,41,1),fontsize=16)
plt.yticks(np.arange(9.6,12.5,0.1),fontsize=16)
plt.xlim((-5, 45))
plt.ylim((9.6,12.5))
plt.show()

