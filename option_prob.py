#import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

csv=input('Enter csv path: ')

"""read csv file and remove unwanted columns"""
#skiprows= skips first 13 rows of file
#usecols= uses columns with given names
#skipfooter= skips last 24 rows of file
myfile=pd.read_csv(csv,skiprows=13,usecols=['BID','ASK','Exp','Strike','BID.1','ASK.1'])
myfile2=pd.read_csv(csv,skiprows=5,usecols=['LAST'],skipfooter=len(myfile)-7)
#create a dataframe object
df=pd.DataFrame(myfile)
pf=pd.DataFrame(myfile2)
underlying=pf['LAST'].tolist()
"""obtain midpoints for bid/ask spreads"""
#retrieve list of bid and asks
call_bid=df['BID'].tolist()
call_ask=df['ASK'].tolist()
put_bid=df['BID.1'].tolist()
put_ask=df['ASK.1'].tolist()
strike_prices=df['Strike'].tolist()
#create the midpoints
def put_mid():
    midpoints=[]
    for i in range(len(myfile)):
        midpoint=((put_bid[i]+put_ask[i])/2)
        midpoints.append(midpoint)
    return midpoints 
a=put_mid()

def call_mid():
    midpoints=[]
    for i in range(len(myfile)):
        midpoint=(call_bid[i]+call_ask[i])/2
        midpoints.append(midpoint)
    return midpoints
#takes out the nan values from csv (values after last strike)
old_list=call_mid()
b=[x for x in old_list if pd.isnull(x)==False]
b.append(0)
"""Obtain butterfly spreads"""
def put_butterfly():
    butterflies=[]
    for i in range(len(put_mid())):
        if float(strike_prices[i+1])>=float(underlying[0]):
            break
        else:
            butterfly=np.round(a[i]-2*a[i+1]+a[i+2],3)
            butterflies.append(butterfly)
    return butterflies
c=put_butterfly()

def call_butterfly():
    butterflies=[]
    for i in range(-1*len(call_mid()),-1):
        if float(strike_prices[i])<float(underlying[0]):
            continue
        else:
            butterfly=np.round(b[i-1]-2*b[i]+b[i+1],3)
            butterflies.append(butterfly)
    return butterflies
d=call_butterfly()

"""Get deltas"""
def put_deltas():
    deltas=[]
    for i in range(len(strike_prices)):
        if i==0 or float(strike_prices[i])>=float(underlying[0]):
            continue
        else:
            delta=float(strike_prices[i]-strike_prices[i-1])
            deltas.append(delta)
    return deltas
e=put_deltas()

def call_deltas():
    deltas=[]
    for i in range(-1*len(strike_prices),-1):
        if float(strike_prices[i])<float(underlying[0]):
            continue
        else:
            delta=float(strike_prices[i]-strike_prices[i-1])
            deltas.append(delta)
    return deltas
f=call_deltas()
"""Get option implied probabilities"""
def implied_probability():
    distribution=[]
    for i in range(len(c)):
        a=np.round((c[i]/(e[i]**2))*e[i],3)
        distribution.append(a)
    for i in range(len(d)):
        q=np.round((d[i]/(f[i]**2))*f[i],3)
        distribution.append(q)
    return distribution
"""Plot the points as a distribution"""
#initialize x and y values
prob=implied_probability()
strikes=strike_prices[-1*len(strike_prices):-2]
x=strikes

#plot distribution
fig,ax=plt.subplots()
bar=ax.bar(x,prob,width=0.5,align='center',color='black')
ax.set_xlabel('Strikes')
ax.set_ylabel('Probability')
ax.set_title('Option Implied Probability')

mplcursors.cursor(bar,hover=True)

plt.show()
