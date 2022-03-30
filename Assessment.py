#import pip packages
import pandas as pd
import requests
import csv
import math

#Api Call Function
def callapi(link):
    resp = requests.get(link)
    return resp.json()

jsondata = callapi("https://datausa.io/api/data?drilldowns=State&measures=Population")["data"]

#Creating a DataFrame with Json Response from given Api using Pandas
df = pd.DataFrame(jsondata)

#Creating a CSV File of the same
df.to_csv('Population_Data.csv',index=False)

#Creating Year-wise, Prime-Factorisation Report for all states
rep_list = []
sidlist = df['ID State'].unique()
ylist = sorted(df['Year'].unique().tolist())

#Iterating through states and creating year-wise report for each state
for sid in sidlist:
    #Sub-dataframe for each state 
    sdf = df[df['ID State'] == sid]
    idic = {}
    idic['State'] = sdf['State'].iloc[0]   
    
    #Creating dictionary of each state yearwise data and adding it to a list
    for pos,y in enumerate(ylist,0):
        curpop = sdf[sdf['Year']==y].iloc[0]['Population']
        if pos == 0:
            idic[y] = str(curpop)
        else:
            prepop = sdf[sdf['Year']==ylist[pos-1]].iloc[0]['Population']
            idic[y] = str(sdf[sdf['Year']==y].iloc[0]['Population']) +' ('+str(round(((curpop - prepop)/curpop)*100,2))+'%)'
    rep_list.append(idic)

#Creating a dataframe with all the states yearwise report  
repdf = pd.DataFrame(rep_list)

#Creating a function for primefactorials 
def primefactors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    retstr = ''
    for each in factors:
        retstr += str(each)+';'
    return retstr[:-1]

#Finding prime-factorials for final year population using lambda and primefactors function
repdf[ylist[-1] + ' Factors'] = repdf.apply(lambda x: primefactors(int(x[ylist[-1]].split(' ')[0])),axis = 1)

#Creating CSV file for writing year-over-year population-change and primefactorisation data
repdf.to_csv('Yearwise_Popln_Chng_Data.csv',index=False)
