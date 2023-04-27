#!/usr/bin/env python
# coding: utf-8

# # Agent Loan Decisioning

# In[1]:


import sys
import datetime
from datetime import date,timedelta
import numpy as np
import pandas as pd
import camelot
import matplotlib.pyplot as plt


# In[10]:


sys.maxsize
# 2147483647


# 
# Qualifying Matrix
# 
# 1.	Agent Length of Service - 3 months
# 
# 2.	Agent Frequency of use/activity - >= 65 transactions(count) in total
# 
# 3.	Agent Frequency of rebalance - >= 45 inbound(count) in total
# 
# 4.	Median Cash-In for last 90 days - avg. txn amnt - ghs5000 
# 
# 5.	Mode Cash-In for last 90 days - lowest amnt cash in - ghs1000 
# 
# 6.	Median Cash-Out for last 90 days - avg. txn amnt - ghs5000
# 
# 7.	Mode Cash-Out for last 90 days - lowest amnt cash out - ghs1000 

# In[2]:


##### full pdf reading

# tables = camelot.read_pdf(r'C:\Users\Chakdahah\MomoStatementReport.pdf',pages='all') #emma data
tables = camelot.read_pdf(r'C:\Users\Chakdahah\MomoStatement2.pdf',pages='all') #prince momo agent2
# tables = camelot.read_pdf(r'C:\Users\Chakdahah\momopages2.pdf',pages='all') # 2 pages prince
# tables = camelot.read_pdf(r'C:\Users\Chakdahah\Momopages3.pdf',pages='all') #50 pages prince
# tables = camelot.read_pdf(r'C:\Users\Chakdahah\momo3pages.pdf',pages='all') # 3 pages prince containig each month

tables



# tables[j].parsing_report #check parsing report to see accuracy of parsing and other details

# append to one csv file

table_fin = tables[0].df #convert first table to df and assign to variable 

for i in range(1,len(tables)-1): # skip 0-nth of tables
    print(i)
    t = tables[i].df 
    t.drop(t.index[0], inplace = True) # drop first row of df
    table_fin = pd.concat([table_fin, t], axis = 0)
    

    print(t)


# In[3]:


# Assign tables into momo data variable

momo_data = table_fin
momo_data


# In[4]:


momo_data[~momo_data.iloc[:,0].str.contains("\n")]


# In[5]:


momo_data.columns = momo_data.iloc[0] #set column names equal to values in row index position 0
momo_data = momo_data[1:] # remove first row from DataFrame


# In[6]:


momo_data.reset_index(drop=True, inplace=True)


# In[7]:


momo_data


# In[8]:


#Reading data from csv file

# momo_data = pd.read_csv(r'\Users\Chakdahah\Cleaned_Momo.csv', skipinitialspace = True)

# Clean whitespaces in colunn name and entire dataframe

momo_data =momo_data.rename(columns=lambda x: x.strip())
momo_data =momo_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

momo_data.head()


# In[9]:


# remove unwanted characters from end of column names
# mmomo_data.rename(columns=lambda x: x.strip('.'),inplace =True)

# remove all unwanted characters in column names
momo_data.rename(columns=lambda s: s.replace(".", ""), inplace=True)

# replace whitespaces with underscore
momo_data.rename(columns=lambda s: s.replace(" ", "_"), inplace=True)


# In[11]:


# cast appropriate data types
momo_data['AMOUNT'] = pd.to_numeric(momo_data['AMOUNT'],errors='coerce')
momo_data['BAL_BEFORE'] = pd.to_numeric(momo_data['BAL_BEFORE'],errors='coerce')
momo_data['BAL_AFTER'] = pd.to_numeric(momo_data['BAL_AFTER'],errors='coerce')
momo_data['F_ID'] = pd.to_numeric(momo_data['F_ID'],errors='coerce')


# In[12]:


momo_data.info(all)


# In[13]:


#Suppressing any scientific notation in entire csv file.

pd.set_option('display.float_format', lambda x: '%.0f' % x)


# In[14]:


momo_data.head()


# In[15]:


m =momo_data['TRANSACTION_DATE'].str.split(' ', expand=True)


# In[16]:


momo_data['TRANSACTION_DATE'] = m[0]
momo_data['TRANSACTION_TIME'] = m[1]


# In[17]:


# shift column 'C' to first position
first_column = momo_data.pop('TRANSACTION_TIME')
  
# insert column using insert(position,column_name,first_column) function
momo_data.insert(1, 'TRANSACTION_TIME', first_column)
  


# In[18]:


momo_data.info(all)


# In[19]:


momo_data.tail()


# In[20]:


momo_data =momo_data.dropna()


# In[21]:


momo_data['TRANSACTION_DATE'] = pd.to_datetime(momo_data['TRANSACTION_DATE'])


# In[22]:


## convert momo_data to csv
momo_data.to_csv(r'C:\Users\Chakdahah\Downloads\Django-main\Django-main\analytics_project\StrippedMomotoCSV200.csv',date_format='%d/%m/%Y')

momo_data.to_excel("StrippedMomotoXLS.xlsx")


# In[23]:


# Set empty list and dict
masterData = []
userData= {}


# # Calculation of scoring parameters

# In[24]:


rows = momo_data.count()[0] # Agent Frequency of use
userData["freq_of_active"] = rows



MOMO=momo_data[(momo_data == 'CASH_IN').any(axis=1)] # frequency of rebalance
MOMOR = MOMO.count()[0]
userData["freq_of_repl"] = MOMOR



meadnie = momo_data.loc[momo_data['TRANS_TYPE']=='CASH_IN','AMOUNT'].median() #Median Cash-In for last 90days
# userData["mead_cash_in"] = meadnie
# userData["mead_cash_in"]
userData["mead_cash_in_calc"] = meadnie*4


modnie = momo_data.loc[momo_data['TRANS_TYPE']=='CASH_IN','AMOUNT'].mode() # Mode Cash-In for last 90 days
userData["modnie_cash_in_calc"] = modnie*4
userData["modnie_cash_in_calc"] = userData["modnie_cash_in_calc"]*4
userData["modnie_cash_in_calc"] = max(userData["modnie_cash_in_calc"])


meadniout = momo_data.loc[momo_data['TRANS_TYPE']=='CASH_OUT','AMOUNT'].median() # Median Cash-Out for last 90 days
# userData["mead_cash_out"] = meadniout
# userData["mead_cash_out"]
userData["mead_cash_out_calc"] = meadniout*4


modno = momo_data.loc[momo_data['TRANS_TYPE']=='CASH_OUT','AMOUNT'].mode() # Mode Cash-Out for last 90 days
userData["modno_cash_out_calc"] = modno*4 
userData["modno_cash_out_calc"] = userData["modno_cash_out_calc"]*4
userData["modno_cash_out_calc"] = max(userData["modno_cash_out_calc"])




# # Scoring Criteria Calculation

# In[25]:


user_copy = userData.copy()
masterData.append(user_copy)


# In[26]:


### scoring

inelligible = []
elligible = []
score_table = []
scoring_table = {}


# In[27]:


Credit_score = 100

# default 3 months
scoring_table["Length of Service"] = 100


for index in range(len(masterData)):

    ## Frequency of use  >= 65 transactions(count) in total

    if masterData[index]["freq_of_active"]> 65 and masterData[index]["freq_of_active"] <= 75:
        user_copy = masterData[index]
#         print(user_copy)
        Credit_score += 50
        scoring_table["Frequency of Activity"] = 50
    elif masterData[index]["freq_of_active"]> 75:
        elig_copy = masterData[index]
        Credit_score+= 100
        scoring_table["Frequency of Activity"] = 100
    else:
        scoring_table["Frequency of Activity"] = 0


        

        
        
#Agent Frequency of rebalance - >= 45 inbound(count) in total

    if masterData[index]["freq_of_repl"]>= 45 and masterData[index]["freq_of_repl"] <= 54:
        user_copy = masterData[index]
        Credit_score += 50 
        scoring_table["Frequency of Rebalance"] = 50
    elif masterData[index]["freq_of_active"]> 54:
        elig_copy = masterData[index]
        Credit_score+= 100
        scoring_table["Frequency of Rebalance"] = 100
    else:
        scoring_table["Frequency of Rebalance"] = 0
        

        
        
        # Median Cash-In for last 90 days - avg. txn amnt - ghs5000 

        
    if masterData[index]["mead_cash_in_calc"] >= 5000:
        user_copy = masterData[index]
        Credit_score += 50
        scoring_table["Median Cash In"] = 50
    else:
        Credit_score+= 0
        scoring_table["Median Cash In"] = 0

        
        
          # Mode Cash-In for last 90 days - lowest amnt cash in - ghs1000 

        
    if masterData[index]["modnie_cash_in_calc"] >= 1000:
        user_copy = masterData[index]
        Credit_score += 50 
        scoring_table["Mode Cash In"] = 50
        
    else:
        elig_copy = masterData[index]
        Credit_score+= 0
        scoring_table["Mode Cash Out"] = 0
        
        
        
       # Median Cash-Out for last 90 days - avg. txn amnt - ghs5000


    if masterData[index]["mead_cash_out_calc"] > 5000:
        user_copy = masterData[index]
        Credit_score += 50 
        scoring_table["Median Cash Out"] = 50
    else:
        elig_copy = masterData[index]
        Credit_score+= 0
        scoring_table["Median Cash Out"] = 0
        
#     Mode Cash-Out for last 90 days - lowest amnt cash out - ghs1000 
        
    if masterData[index]["modno_cash_out_calc"] >= 1000:
        user_copy = masterData[index]
        Credit_score += 50 
        scoring_table["Mode Cash Out"] = 50
    else:
        elig_copy = masterData[index]
        Credit_score+= 0   
        scoring_table["Mode Cash Out"]
    

#         print(elig_copy)
elligible.append(elig_copy)
score_table.append(scoring_table)        
        
        
        
print("Inelligble", inelligible)
print('\n')
print("Elligible", elligible)
    
    


# In[28]:


score_table = pd.DataFrame.from_dict(score_table)
score_table


# In[29]:


score_table.to_csv(r'C:\Users\Chakdahah\Downloads\Django-main\Django-main\analytics_project\scoretable200.csv')


# In[30]:


type(elligible)


# In[31]:


### convert dict to df

elligible = pd.DataFrame.from_dict(elligible)
elligible


# In[32]:


type(elligible)


# In[33]:


elligible.to_csv(r'C:\Users\Chakdahah\Downloads\Django-main\Django-main\analytics_project\elligible200.csv')


# In[34]:


Credit_score


# # Applying scores to Merchants

# In[35]:


if Credit_score >= 200 and Credit_score <= 250:
    print("You qualify for a GHS 1000 loan")

elif Credit_score >= 251 and Credit_score <= 350:
    print("You qualify for a GHS 2000 loan")

elif Credit_score >= 351 and Credit_score <= 400:
    print("You qualify for a GHS 3000 loan")

elif Credit_score >= 401 and Credit_score <= 500:
    print("You qualify for a GHS 5000 loan")




# # Score and risk grade table 

# In[36]:


details = {
    'Risk Ranking' : ['RR-1', 'RR-2', 'RR-3', 'RR-4'],
    'Minimum Score' : [200,251,351,401],
    'Maximum Score' : [250,350,400,500],
    'Qualifying Amount(GHS)':[1000,2000,3000,5000]
}
  
# creating a Dataframe object 
df = pd.DataFrame(details)
df

