# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 11:07:30 2021

@author: Alex.Kayal
"""
#%%

import os
import pandas as pd
import numpy as np
import ta

# read data
ohlcv = pd.read_csv(os.path.join(os.getcwd(),
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
rsi_slow_period = 50
rsi_med_period = 15
rsi_fast_period = 14
adx_period = 14
label = 'Close'
TP = 50
SL = 100

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
        if ohlcv['rsi_fast'][i] < 30 and ohlcv['rsi_slow'][i] < 30:
            open_position = 'buy'
            entry_value = ohlcv['Close'][i]
            entry_row = i
            return 'buy'
        
        # downcross
        elif ohlcv['rsi_fast'][i] > 70 and ohlcv['rsi_slow'][i] > 70:
            open_position = 'sell'
            entry_value = ohlcv['Close'][i]
            entry_row = i
            return 'sell'
        
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
