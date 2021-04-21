import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors 
import yfinance as yf

ticker=yf.Ticker(input("Enter ticker: "))

"""Read csv file and remove unwanted columns"""
hist=ticker.history(period='1y')
myfile=hist.drop(['Open','High','Low','Volume','Dividends','Stock Splits'],axis=1)
#create dataframe object
df=pd.DataFrame(myfile)
#retrieve list of closing prices
close=df['Close'].tolist()
"""get daily price changes"""
def daily_changes():
    changes=[]
    for i in range(1,len(myfile)):
        change=close[i]-close[i-1]
        changes.append(change)
    return changes
"""get log price changes"""
a=daily_changes()
def log_changes():
    logchanges=[]
    for i in range(1,len(myfile)):
        logchange=np.log(close[i]/close[i-1])
        logchanges.append(logchange)
    return logchanges
b=log_changes()
"""get volatility on a 20-day moving window"""
def volatility():
    vols=[]
    for i in range(19,len(b)):
        vol=np.std(b[i-20:i],dtype=np.float64)
        vols.append(vol)
    return vols
c=volatility()
"""find rolling one standard deviation move"""
def one_sd():
    devs=[]
    for i in range(len(c)):
        dev=c[i]*close[i+20]
        devs.append(dev)
    return devs
"""find daily spike in standard deviations"""
d=one_sd()
def spike():
    spikes=[]
    for i in range(len(d)):
        spike=a[i+19]/d[i]
        spikes.append(spike)
    return spikes
e=spike()
"""Graph price changes in standard deviations"""
x=np.arange(len(e))
y=e
fig,ax=plt.subplots()
bar=ax.bar(x,y,width=0.5,align='center',color='black')
ax.set_ylabel('standard deviations')

mplcursors.cursor(bar,hover=True)

plt.show()