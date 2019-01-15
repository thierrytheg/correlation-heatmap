import os, sys
import numpy as np
import pandas as pd
import datetime
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import time
import csv, json


sys.__stdout__=sys.stdout

sns.set(style="dark")

x=time.time()
currdate=datetime.datetime.fromtimestamp(x).strftime('%m-%d-%Y')

KEY='DEMO'

"""
ETF=['QQQ','FXE','SPY','IWM','TLT',
     'GLD','EWZ','XLE','FXI','DIA',
     'EEM','AAPL','AMZN','BABA','BBY',
     'BIDU','C','CMG','COST','EBAY',
     'FB','GOOG','GS','IBM','MCD',
     'MSFT','NFLX','NKE','TSLA']
"""

ETF=['SPY','QQQ']

for a in ETF:
    dailyprice='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&apikey=%s&outputsize=compact' %(a,KEY)

    first=requests.get(dailyprice)
    info=json.loads(first.text)
    date=info['Time Series (Daily)']
    df =pd.DataFrame(columns=['Date','Price'])
    liste1={}
    for eachdate in date:
        details=date[eachdate]
        close=details['4. close']
        liste1.update({eachdate:close})
    listekey=[]
    listevalue=[]
    for key in sorted(liste1.keys()):
        df=df.append({'Date':key,'Price':(round(float((liste1[key])),2))},ignore_index=True)
        save=a+'.csv'
        df.to_csv(save)
        listekey.append(key)
        listevalue.append(liste1[key])
    time.sleep(15)

df=(pd.DataFrame())
for file in os.listdir(os.getcwd()):
    nfile=file.split('.')[0]
    handle=open(file,'r')

    close=[]

    for x in handle:
        print(x)
        content=(((x.split('\n'))[0]).split(','))[2]
        try:
            close.insert(0,float(content))         
            
        except Exception:
            pass
        
    df.insert(loc=0,column=nfile,value=close)

corr=df.corr()

f, ax = plt.subplots(1,1,figsize=(11, 9))
f.suptitle("Correlation heatmap-compact data",fontsize=14, fontweight="bold")

sns.heatmap(corr, mask=None, cmap='seismic_r', vmin=-1, vmax=1, center=0,
            annot=None,fmt='.3f',square=True, linewidths=1,
            cbar_kws={"shrink": .5})

plt.yticks(rotation=0)
fig=plt.gcf()
#a=fig.savefig('heatmap.png')
plt.show()
