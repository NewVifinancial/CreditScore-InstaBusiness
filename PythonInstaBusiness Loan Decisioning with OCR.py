#!/usr/bin/env python
# coding: utf-8

# # Agent Loan Decisioning

# In[ ]:


import sys
import datetime
from datetime import date,timedelta
import numpy as np
import pandas as pd
import camelot
import matplotlib.pyplot as plt
import logging


# In[ ]:


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Code Begin')


# In[ ]:


# sys.maxsize
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

# In[ ]:


##### full pdf reading

# tables = camelot.read_pdf(r'C:\Users\Chakdahah\MomoStatementReport.pdf',pages='all') #emma data
# tables = camelot.read_pdf(r'C:\Users\Chakdahah\momopages2.pdf',pages='all') # 2 pages prince
# tables = camelot.read_pdf(r'C:\Users\Chakdahah\Momopages3.pdf',pages='all') #50 pages prince
# tables = camelot.read_pdf(r'C:\Users\Chakdahah\lastlast.pdf',pages='all') # 5 pages prince containig each month 
# tables = camelot.read_pdf(r'C:\Users\Chakdahah\MomoStatement98.pdf',pages='all') # 98 pages prince containig each month 26mi
# tables = camelot.read_pdf(r'C:\Users\Chakdahah\MomoStatementmax.pdf',pages='all') # maxwell 235 pages 
# tables = camelot.read_pdf(r'C:\Users\Chakdahah\MomoStatement256.pdf',pages='all') # maxwell 256 pages 
tables = camelot.read_pdf(r'C:\Users\Chakdahah\MomoStatement298.pdf',pages='all') # amokoaa regina 298 pages  

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


# In[ ]:


# Assign tables into momo data variable

momo_data = table_fin
momo_data


# In[ ]:


momo_data[~momo_data.iloc[:,0].str.contains("\n")]


# In[ ]:


momo_data.columns = momo_data.iloc[0] #set column names equal to values in row index position 0
momo_data = momo_data[1:] # remove first row from DataFrame


# In[ ]:


momo_data.reset_index(drop=True, inplace=True)


# In[ ]:


momo_data


# In[ ]:


#Reading data from csv file

# momo_data = pd.read_csv(r'\Users\Chakdahah\Cleaned_Momo.csv', skipinitialspace = True)

# Clean whitespaces in colunn name and entire dataframe

momo_data =momo_data.rename(columns=lambda x: x.strip())
momo_data =momo_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

momo_data.head()


# In[ ]:


# remove unwanted characters from end of column names
# mmomo_data.rename(columns=lambda x: x.strip('.'),inplace =True)

# remove all unwanted char acters in column names
momo_data.rename(columns=lambda s: s.replace(".", ""), inplace=True)

# replace whitespaces with underscore
momo_data.rename(columns=lambda s: s.replace(" ", "_"), inplace=True)


# In[ ]:


# cast appropriate data types
momo_data['AMOUNT'] = pd.to_numeric(momo_data['AMOUNT'],errors='coerce')
momo_data['BAL_BEFORE'] = pd.to_numeric(momo_data['BAL_BEFORE'],errors='coerce')
momo_data['BAL_AFTER'] = pd.to_numeric(momo_data['BAL_AFTER'],errors='coerce')
momo_data['F_ID'] = pd.to_numeric(momo_data['F_ID'],errors='coerce')


# In[ ]:


momo_data.info(all)


# In[ ]:


#Suppressing any scientific notation in entire csv file.

pd.set_option('display.float_format', lambda x: '%.0f' % x)


# In[ ]:


momo_data.head()


# In[ ]:


m =momo_data['TRANSACTION_DATE'].str.split(' ', expand=True)


# In[ ]:


momo_data['TRANSACTION_DATE'] = m[0]
momo_data['TRANSACTION_TIME'] = m[1]


# In[ ]:


# shift column 'C' to first position
first_column = momo_data.pop('TRANSACTION_TIME')
  
# insert column using insert(position,column_name,first_column) function
momo_data.insert(1, 'TRANSACTION_TIME', first_column)
  


# In[ ]:


momo_data.info(all)


# In[ ]:


momo_data['FROM_NAME'] = momo_data.FROM_NAME.str.replace('\n',' ')


# In[ ]:


momo_data.tail()


# In[ ]:


num=momo_data.loc[momo_data['TRANS_TYPE'] == 'CASH_IN', 'FROM_NO'].iloc[0]
num


# In[ ]:


name=momo_data.loc[momo_data['TRANS_TYPE'] == 'CASH_IN', 'FROM_NAME'].iloc[0]
name


# In[ ]:


momo_data[~momo_data.iloc[:,0].str.contains("\n")]


# In[ ]:


df3=momo_data.loc[momo_data['TRANS_TYPE'] == 'CASH_IN', 'FROM_NAME'].iloc[0]
df3


# In[ ]:


momo_data =momo_data.dropna()


# In[ ]:


# store date as object for later use
mi = momo_data['TRANSACTION_DATE']


# In[ ]:


momo_data['TRANSACTION_DATE'] = pd.to_datetime(momo_data['TRANSACTION_DATE'])


# # Converting PDF to CSV and XLSX
# 

# In[ ]:


## convert momo_data to csv
momo_data.to_csv(r'C:\Users\Chakdahah\Downloads\Django-main\Django-main\analytics_project\StrippedMomotoCSV298.csv',date_format='%d/%m/%Y')

momo_data.to_excel("StrippedMomotoXLS298.xlsx")


# In[ ]:


# Set empty list and dict
masterData = []
userData= {}


# # Calculation of scoring parameters

# In[ ]:


rows = momo_data.count()[0] # Agent Frequency of use
userData["freq_of_active"] = rows



MOMO=momo_data[(momo_data == 'CASH_IN').any(axis=1)] # frequency of rebalance
MOMOR = MOMO.count()[0]
userData["freq_of_repl"] = MOMOR


meadnie = momo_data.loc[momo_data['TRANS_TYPE']=='CASH_IN','AMOUNT'].median() #Median Cash-In for last 90days
# userData["mead_cash_in"] = meadnie
# userData["mead_cash_in"]
userData["median_cash_in_calc"] = meadnie*4


modnie = momo_data.loc[momo_data['TRANS_TYPE']=='CASH_IN','AMOUNT'].mode() # Mode Cash-In for last 90 days
userData["mode_cash_in_calc"] = modnie*4
userData["mode_cash_in_calc"] = max(userData["mode_cash_in_calc"]) #for converting from bool to int for processing


meadniout = momo_data.loc[momo_data['TRANS_TYPE']=='CASH_OUT','AMOUNT'].median() # Median Cash-Out for last 90 days
# userData["mead_cash_out"] = meadniout
# userData["mead_cash_out"]
userData["median_cash_out_calc"] = meadniout*4


modno = momo_data.loc[momo_data['TRANS_TYPE']=='CASH_OUT','AMOUNT'].mode() # Mode Cash-Out for last 90 days
userData["mode_cash_out_calc"] = modno*4 
userData["mode_cash_out_calc"] = max(userData["mode_cash_out_calc"])




# In[ ]:


# momo_data.loc[momo_data['TRANS_TYPE']=='CASH_OUT','AMOUNT'].mode() # Mode Cash-Out for last 90 days


# In[ ]:


# print(modnie)
# userData["mode_cash_in_calc"] = modnie*4
# print(userData["mode_cash_in_calc"])
# # userData["mode_cash_out_calc"] = userData["mode_cash_out_calc"]*4

# # print(max(userData["mode_cash_in_calc"]))


# In[ ]:


# print(max(userData["mode_cash_in_calc"]))


# # Scoring Criteria Calculation

# In[ ]:


user_copy = userData.copy()
masterData.append(user_copy)


# In[ ]:


### scoring

inelligible = []
elligible = []
score_table = []
scoring_table = {}
combined = []


# In[ ]:


scoring_table["Agent Number"] = num
scoring_table["Agent Name"] = name


# In[ ]:


## Agent Length of Service - 3 months

for i in mi:
    u = mi.str.extract('([a-zA-Z ]+)', expand=False).str.strip()
    monthcount = u.drop_duplicates()
print(monthcount)

if len(monthcount)>=3:
    scoring_table["Length of Service"] = 100
    Credit_score = 100
else:
    scoring_table["Length of Service"] = 0
    Credit_score = 0


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

        
    if masterData[index]["median_cash_in_calc"] >= 5000:
        user_copy = masterData[index]
        Credit_score += 50
        scoring_table["Median Cash In"] = 50
    else:
        Credit_score+= 0
        scoring_table["Median Cash In"] = 0

        
        
          # Mode Cash-In for last 90 days - lowest amnt cash in - ghs1000 

        
    if masterData[index]["mode_cash_in_calc"] >= 1000:
        user_copy = masterData[index]
        Credit_score += 50 
        scoring_table["Mode Cash In"] = 50
        
    else:
        elig_copy = masterData[index]
        Credit_score+= 0
        scoring_table["Mode Cash In"] = 0
        
        
        
       # Median Cash-Out for last 90 days - avg. txn amnt - ghs5000


    if masterData[index]["median_cash_out_calc"] > 5000:
        user_copy = masterData[index]
        Credit_score += 50 
        scoring_table["Median Cash Out"] = 50
    else:
        elig_copy = masterData[index]
        Credit_score+= 0
        scoring_table["Median Cash Out"] = 0
        
#     Mode Cash-Out for last 90 days - lowest amnt cash out - ghs1000 
        
    if masterData[index]["mode_cash_out_calc"] >= 1000:
        user_copy = masterData[index]
        Credit_score += 50 
        scoring_table["Mode Cash Out"] = 50
    else:
        elig_copy = masterData[index]
        Credit_score+= 0   
        scoring_table["Mode Cash Out"] = 0
    

#         print(elig_copy)
scoring_table["Credit Score"] = Credit_score
score_table.append(scoring_table)        
        
    


# In[ ]:


elligible.append(elig_copy)


# # Applying scores to Merchants

# In[ ]:


if Credit_score >= 200 and Credit_score <= 250:
    print("You qualify for a GHS 1000 loan")
    scoring_table["Eligibility"] = 1000

elif Credit_score >= 251 and Credit_score <= 350:
    print("You qualify for a GHS 2000 loan")
    scoring_table["Eligibility"] = 2000

elif Credit_score >= 351 and Credit_score <= 400:
    print("You qualify for a GHS 3000 loan")
    scoring_table["Eligibility"] = 3000


elif Credit_score >= 401 and Credit_score <= 500:
    print("You qualify for a GHS 5000 loan")
    scoring_table["Eligibility"] = 5000



# # Combining Eligibility and Score Tables

# In[ ]:


comb = scoring_table | elig_copy
comb


# In[ ]:


combined.append(comb)


# In[ ]:


print("Elligible", elligible)


# In[ ]:


Credit_score


# # Converting and saving Score Table

# In[ ]:


score_table = pd.DataFrame.from_dict(score_table)
score_table


# In[ ]:


score_table.to_csv(r'C:\Users\Chakdahah\Downloads\Django-main\Django-main\analytics_project\scoretable298.csv')


# # Converting and saving Eligibility Table

# In[ ]:


### convert dict to df

elligible = pd.DataFrame.from_dict(elligible)
elligible


# In[ ]:


type(elligible)


# In[ ]:


elligible.to_csv(r'C:\Users\Chakdahah\Downloads\Django-main\Django-main\analytics_project\elligible298.csv')


# # Converting and saving Combined Table

# In[ ]:


combined_table = pd.DataFrame.from_dict(combined)
combined_table


# In[ ]:


combined_table.to_csv(r'C:\Users\Chakdahah\Downloads\Django-main\Django-main\analytics_project\combtable298.csv')


# In[ ]:


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('End of Code')


# # Score and risk grade table 

# In[ ]:


details = {
    'Risk Ranking' : ['RR-1', 'RR-2', 'RR-3', 'RR-4'],
    'Minimum Score' : [200,251,351,401],
    'Maximum Score' : [250,350,400,500],
    'Qualifying Amount(GHS)':[1000,2000,3000,5000]
}
  
# creating a Dataframe object 
df = pd.DataFrame(details)
df

