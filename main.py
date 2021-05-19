import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors 
import yfinance as yf

class ChangeSD():
    def __init__(self,ticker):
        self.ticker=ticker
        self.hist=self.ticker.history(period='1y')
        self.myfile=self.hist.drop(['Open','High','Low','Volume','Dividends','Stock Splits'],axis=1)
        self.df=pd.DataFrame(self.myfile)
        self.close=self.df['Close'].tolist()
        
    """get daily price changes"""
    def daily_changes(self):
        changes=[]
        for i in range(1,len(self.myfile)):
            change=self.close[i]-self.close[i-1]
            changes.append(change)
        return changes

    """get log price changes"""
    def log_changes(self):
        logchanges=[]
        for i in range(1,len(self.myfile)):
            logchange=np.log(self.close[i]/self.close[i-1])
            logchanges.append(logchange)
        return logchanges

    """get volatility on a 20-day moving window"""
    def volatility(self):
        b=self.log_changes()
        vols=[]
        for i in range(19,len(b)):
            vol=np.std(b[i-20:i],dtype=np.float64)
            vols.append(vol)
        return vols

    """find rolling one standard deviation move"""
    def one_sd(self):
        c=self.volatility()
        devs=[]
        for i in range(len(c)):
            dev=c[i]*self.close[i+20]
            devs.append(dev)
        return devs

    """find daily spike in standard deviations"""
    def spike(self):
        a=self.daily_changes()
        d=self.one_sd()
        spikes=[]
        for i in range(len(d)):
            spike=a[i+19]/d[i]
            spikes.append(spike)
        return spikes
class OptionsProb():
    def __init__(self,csv):
        self.csv=csv
        self.myfile=pd.read_csv(csv,skiprows=11,usecols=['BID','ASK','Exp','Strike','BID.1','ASK.1'])
        self.myfile2=pd.read_csv(csv,skiprows=3,usecols=['LAST'],skipfooter=len(self.myfile)-5)
        self.df=pd.DataFrame(self.myfile)
        self.pf=pd.DataFrame(self.myfile2)
        self.underlying=self.pf['LAST'].tolist()
        self.call_bid=self.df['BID'].tolist()
        self.call_ask=self.df['ASK'].tolist()
        self.put_bid=self.df['BID.1'].tolist()
        self.put_ask=self.df['ASK.1'].tolist()
        self.strike_prices=self.df['Strike'].tolist()

    """Create midpoints"""
    def put_mid(self):
        midpoints=[]
        for i in range(len(self.myfile)):
            midpoint=((self.put_bid[i]+self.put_ask[i])/2)
            midpoints.append(midpoint)
        return midpoints 

    def call_mid(self):
        midpoints=[]
        for i in range(len(self.myfile)):
            midpoint=(self.call_bid[i]+self.call_ask[i])/2
            midpoints.append(midpoint)
        return midpoints

    """Obtain butterfly spreads"""
    def put_butterfly(self):
        a=self.put_mid()
        butterflies=[]
        for i in range(len(a)):
            if float(self.strike_prices[i+1])>=float(self.underlying[0]):
                break
            else:
                butterfly=np.round(a[i]-2*a[i+1]+a[i+2],3)
                butterflies.append(butterfly)
        return butterflies

    def call_butterfly(self):
        old_list=self.call_mid()
        b=[x for x in old_list if pd.isnull(x)==False]
        butterflies=[]
        for i in range(len(b)-1):
            if float(self.strike_prices[i])<float(self.underlying[0]):
                continue
            else:
                butterfly=np.round(b[i-1]-2*b[i]+b[i+1],3)
                butterflies.append(butterfly)
        return butterflies

    """Get deltas"""
    def put_deltas(self):
        strikes=[x for x in self.strike_prices if pd.isnull(x)==False]
        deltas=[]
        for i in range(len(strikes)):
            if i==0 or float(self.strike_prices[i])>=float(self.underlying[0]):
                continue
            else:
                delta=float(self.strike_prices[i]-self.strike_prices[i-1])
                deltas.append(delta)
        return deltas

    def call_deltas(self):
        strikes=[x for x in self.strike_prices if pd.isnull(x)==False]
        deltas=[]
        for i in range(-1*len(strikes),-1):
            if float(self.strike_prices[i])<float(self.underlying[0]):
                continue
            else:
                delta=float(self.strike_prices[i]-self.strike_prices[i-1])
                deltas.append(delta)
        return deltas
    
    """Get option implied probabilities"""
    def implied_probability(self):
        c=self.put_butterfly()
        d=self.call_butterfly()
        e=self.put_deltas()
        f=self.call_deltas()
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
    def clean_data(self):
        prob=self.implied_probability()
        cleaned=[]
        for i in range(len(prob)):
            if self.call_bid[i]==0 or self.call_ask[i]==0 or self.put_bid[i]==0 or self.put_ask[i]==0:
                cleaned.append(0)
            else:
                clean=prob[i]
                cleaned.append(clean)
        return cleaned
        
    #get same amount of values for x and y axis
    def clean_strikes(self):
        strikes=[x for x in self.strike_prices if pd.isnull(x)==False]
        cleaned=strikes[-1*len(strikes):-2]
        return cleaned

def main():
    #csv input
    ticker=yf.Ticker(input('Enter ticker: '))
    csv=input('Enter csv file: ')
    #OptionsProb and changeSD objects
    changes=ChangeSD(ticker)
    option=OptionsProb(csv)

    """plot data"""
    #x and y for ChangeSD
    x=np.arange(len(changes.spike()))
    y=changes.spike()
    #x and y for OptionsProb
    prob1=option.clean_data()
    strikes1=option.clean_strikes()

    #plot OptionsProb
    plt.figure(0)
    option1=plt.bar(strikes1,prob1,width=0.2,align='center',color='black')
    plt.xlabel('Strikes')
    plt.ylabel('Probability')
    plt.title('Option Implied Probability')
    mplcursors.cursor(option1,hover=True)
    
    #plot ChangeSD
    plt.figure(1)
    changes1=plt.bar(x,y,width=0.5,align='center',color='black')
    plt.ylabel('standard deviations')
    plt.title('Changes is SD')
    mplcursors.cursor(changes1,hover=True)


    plt.show()

if __name__=='__main__':
    main()
