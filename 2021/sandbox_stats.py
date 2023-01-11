# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 12:37:43 2021

@author: Alex.Kayal
"""

import yfinance as yf
import datetime as dt
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ta
import pandas_datareader.data as web

# Checking pct on hourly/daily/monthly etc
ticker = "MSFT"
ohlcv = yf.download(ticker,
                    dt.date.today()-dt.timedelta(250),
                    dt.datetime.today(),
                    interval="1h")

ohlcv['pct'] = np.nan
for i in range(1,len(ohlcv)):
    ohlcv['pct'][i] = (ohlcv['Adj Close'][i]/ohlcv['Adj Close'][i-1]-1)*100
    
print(np.nansum(abs(ohlcv['pct']))/len(ohlcv['pct']))

abs(ohlcv['pct']).plot()

# candle range in pips

ticker = "EURUSD=X"
ohlcv = yf.download(ticker,
                    dt.date.today()-dt.timedelta(1000),
                    dt.datetime.today(),
                    interval="1wk")

ohlcv['candleRange'] = np.nan
for i in range(0,len(ohlcv)):
    ohlcv['candleRange'][i] = (ohlcv['High'][i] - ohlcv['Low'][i])*10E3
    
print(np.nansum(ohlcv['candleRange'])/len(ohlcv['candleRange']))

ohlcv['candleRange'].plot()

# volume info

# just for reference
# ohlcv = web.DataReader(ticker, 'quandl', '2015-01-01', '2015-01-05')

ohlcv = pd.read_csv(os.path.join(os.getcwd(),'Downloads', 'Quant', 'CSVData',
                                 'EURUSD_H1_202004010000_202104011200.csv'),
                    delimiter='\t')

ohlcv['Weekday'] = '' 
ohlcv['DateObj'] = pd.to_datetime(ohlcv['<DATE>'], format = '%Y.%m.%d')
for i in range(0,len(ohlcv)):
    ohlcv['Weekday'][i] = ohlcv['DateObj'][i].weekday()

df = ohlcv.groupby(['Weekday', '<TIME>']).mean()
df = df.sort_values(by=['<TICKVOL>'], ascending=False)
    
df['<TICKVOL>'].plot()

df = ohlcv.groupby(['Weekday']).mean()
df = df.sort_values(by=['<TICKVOL>'], ascending=False)

df = ohlcv.groupby(['<TIME>']).mean()
df = df.sort_values(by=['<TICKVOL>'], ascending=False)

# average candle length, per weekday/hour

ohlcv = pd.read_csv(os.path.join(os.getcwd(),'Downloads', 'Quant', 'CSVData',
                                 'EURUSD_H1_202004010000_202104011200.csv'),
                    delimiter='\t')

ohlcv['Weekday'] = '' 
ohlcv['DateObj'] = pd.to_datetime(ohlcv['<DATE>'], format = '%Y.%m.%d')
for i in range(0,len(ohlcv)):
    ohlcv['Weekday'][i] = ohlcv['DateObj'][i].weekday()

ohlcv['candleRange'] = np.nan
for i in range(0,len(ohlcv)):
    ohlcv['candleRange'][i] = (ohlcv['<HIGH>'][i] - ohlcv['<LOW>'][i])*10E3
    
df = ohlcv.groupby(['Weekday', '<TIME>']).mean()
df['candleRange'].plot()
df['<TICKVOL>'].plot()