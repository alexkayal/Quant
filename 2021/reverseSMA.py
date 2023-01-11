# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 11:48:14 2021

@author: Alex.Kayal
"""
## strategy simulator: reverse SMA crossover

#%%

import os
import pandas as pd
import numpy as np
import ta

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder

# read data
ohlcv = pd.read_csv(os.path.join(os.getcwd(),
                                 'Downloads',
                                 'Quant',
                                 'CSVData',
                                 'EURUSD_H1_201704030000_202104010000.csv'),
                                  delimiter='\t')

ohlcv = ohlcv.rename(columns = {'<DATE>': 'Date',
                                '<TIME>': 'Time',
                                '<OPEN>': 'Open',
                                '<HIGH>': 'High',
                                '<LOW>': 'Low',
                                '<CLOSE>': 'Close',
                                '<TICKVOL>': 'Volume'}, inplace = False)


ohlcv = ohlcv.drop(['<VOL>', '<SPREAD>'], axis='columns', inplace=False)

sma_fast = 5
sma_slow = 10
rsi_slow_period = 34
rsi_med_period = 21
rsi_fast_period = 14
adx_period = 14
label = 'Close'
TP = 25
SL = 50

ohlcv['sma_fast'] = ohlcv[label].rolling(window=sma_fast).mean()
ohlcv['sma_slow'] = ohlcv[label].rolling(window=sma_slow).mean()
ohlcv['rsi_slow'] = ta.momentum.rsi(ohlcv[label], window=rsi_slow_period, fillna=False)
ohlcv['rsi_med'] = ta.momentum.rsi(ohlcv[label], window=rsi_med_period, fillna=False)
ohlcv['rsi_fast'] = ta.momentum.rsi(ohlcv[label], window=rsi_fast_period, fillna=False)
ohlcv['adx'] = ta.trend.adx(ohlcv['High'], ohlcv['Low'], ohlcv['Close'],
                            window=adx_period, fillna=False)

open_position = 'none'
entry_value = np.nan
entry_row = np.nan

ohlcv['signal'] = 'none' #buy, sell, TP, SL, none
ohlcv['outcome'] = 'none' #win, loss, none

def get_signal(i):
    
    global open_position, entry_value, entry_row
    if open_position == 'none':
    
        #upcross
        if ohlcv['sma_fast'][i] > ohlcv['sma_slow'][i] and ohlcv['sma_fast'][i-1] < ohlcv['sma_slow'][i-1]:
            open_position = 'sell'
            entry_value = ohlcv['Close'][i]
            entry_row = i
            return 'sell'
        
        # downcross
        elif ohlcv['sma_fast'][i] < ohlcv['sma_slow'][i] and ohlcv['sma_fast'][i-1] > ohlcv['sma_slow'][i-1]:
            open_position = 'buy'
            entry_value = ohlcv['Close'][i]
            entry_row = i
            return 'buy'
        
        else:
            return 'none'
        
    else:
        # close buy
        if open_position == 'buy':
            if ohlcv['High'][i] >= (entry_value + TP/10000):
                open_position = 'none'
                entry_value = np.nan
                ohlcv['outcome'][entry_row] = 'win'
                entry_row = np.nan
                return 'TP'
            elif ohlcv['Low'][i] <= (entry_value - SL/10000):
                open_position = 'none'
                entry_value = np.nan
                ohlcv['outcome'][entry_row] = 'loss'
                entry_row = np.nan
                return 'SL'
        
        # close sell
        elif open_position == 'sell':
            if ohlcv['High'][i] >= (entry_value + SL/10000):
                open_position = 'none'
                entry_value = np.nan
                ohlcv['outcome'][entry_row] = 'loss'
                entry_row = np.nan
                return 'SL'
            elif ohlcv['Low'][i] <= (entry_value - TP/10000):
                open_position = 'none'
                entry_value = np.nan
                ohlcv['outcome'][entry_row] = 'win'
                entry_row = np.nan
                return 'TP'
        
        else:
            return 'none'
        
ohlcv = ohlcv.iloc[33:]

for i, r in ohlcv.iterrows():
    if i > 33:
        ohlcv['signal'][i] = get_signal(i)
        
df = ohlcv['outcome'].value_counts()
print (df)