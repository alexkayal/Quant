# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 12:11:39 2021

@author: Alex.Kayal
"""
# Optimizer

#%%

import os
import pandas as pd
import numpy as np

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

#ohlcv = ohlcv[ohlcv.index.isin(range(18001,21000))]
#ohlcv = ohlcv.reset_index(drop=True)

sma_fast = 14
sma_slow = 21
label = 'Close'
TP = 25
SL = 25

ohlcv['sma_fast'] = ohlcv[label].rolling(window=sma_fast).mean()
ohlcv['sma_slow'] = ohlcv[label].rolling(window=sma_slow).mean()

open_position = 'none'
entry_value = np.nan
prev_entry_value = np.nan
entry_row = np.nan
prev_entry_row = np.nan

ohlcv['signal'] = 'none' #buy, sell, TP, SL, none
ohlcv['outcome'] = 0 # pips won or lost

def get_signal(i):
    
    global open_position, entry_value, entry_row
    if open_position == 'none':
    
        #upcross
        if ohlcv['sma_fast'][i] > ohlcv['sma_slow'][i] and ohlcv['sma_fast'][i-1] < ohlcv['sma_slow'][i-1]:
            open_position = 'buy'
            entry_value = ohlcv['Close'][i]
            entry_row = i
            return 'buy'
        
        # downcross
        elif ohlcv['sma_fast'][i] < ohlcv['sma_slow'][i] and ohlcv['sma_fast'][i-1] > ohlcv['sma_slow'][i-1]:
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
                ohlcv['outcome'][entry_row] = TP
                entry_row = np.nan
                return 'TP'
            # downcross
            elif ohlcv['sma_fast'][i] < ohlcv['sma_slow'][i] and ohlcv['sma_fast'][i-1] > ohlcv['sma_slow'][i-1]:
                ohlcv['outcome'][entry_row] = int((ohlcv['Close'][i] - entry_value)*10000)
                open_position = 'sell'
                entry_value = ohlcv['Close'][i]
                entry_row = i
                return 'SL'
            
        
        # close sell
        elif open_position == 'sell':
            #upcross
            if ohlcv['sma_fast'][i] > ohlcv['sma_slow'][i] and ohlcv['sma_fast'][i-1] < ohlcv['sma_slow'][i-1]:
                ohlcv['outcome'][entry_row] = int((entry_value - ohlcv['Close'][i])*10000)
                open_position == 'buy'
                entry_value = ohlcv['Close'][i]
                entry_row = i
                return 'SL'
            elif ohlcv['Low'][i] <= (entry_value - TP/10000):
                open_position = 'none'
                entry_value = np.nan
                ohlcv['outcome'][entry_row] = TP
                entry_row = np.nan
                return 'TP'
        
        else:
            return 'none'

optimize = pd.DataFrame(columns=['TP', 'result'])
ohlcv = ohlcv.iloc[21:]
for TP in [x for x in range(1,201) if x%5==0]:
    print(TP)
    for i, r in ohlcv.iterrows():
        if i > 21:
            ohlcv['signal'][i] = get_signal(i)
    print(sum(ohlcv['outcome']))    
    #optimize.append({'TP': TP, 'result': sum(ohlcv['outcome'])}, ignore_index=True)