# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 13:36:38 2021

@author: Alex.Kayal
"""

# Neural networks test #1

import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import ta

from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

def timeseries_df(X, label, n):
    
    df = X[[label]]
  
    for i in range(n):
        df[label+'_'+str(i+1)] = df[label].shift(periods=i+1)
    
    df = df.drop([label], axis=1)
    df = df.iloc[n:]
    
    return df

# Download historical data for required stocks
ticker = "EURUSD=X"
ohlcv = yf.download(ticker,dt.date.today()-dt.timedelta(2000),dt.datetime.today())
ohlcv['Median'] = (ohlcv['High'] + ohlcv['Low'])/2

##
label = 'Close'
n = 20
X = timeseries_df(ohlcv, label, n)
y = ohlcv[[label]].iloc[n:]
##

##
label = 'Close'
n = 8
rsi14  = ta.momentum.rsi(ohlcv[label], window=14, fillna=False)

mv3 = ohlcv[label].rolling(window=3).mean().shift(periods=1)
#mv5 = ohlcv[label].rolling(window=5).mean().shift(periods=1)
mv8 = ohlcv[label].rolling(window=8).mean().shift(periods=1)
mv20 = ohlcv[label].rolling(window=20).mean().shift(periods=1)

X = pd.concat([mv3, mv8], axis=1)[n:]
y = ohlcv[[label]].iloc[n:]
##

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=False)

#regr = MLPRegressor(hidden_layer_sizes=3, tol=0.0001,
#                    max_iter=500, n_iter_no_change=10, 
#                    verbose=True).fit(X_train, y_train)

regr = MLPRegressor(hidden_layer_sizes=[200, 100], 
                    max_iter=1000, n_iter_no_change=500, verbose=True)
regr.fit(X_train, y_train.to_numpy().ravel())

predicted = regr.predict(X_test)

diff = predicted - y_test[label]
diff_df = pd.DataFrame({'Actual': y_test[label], 
                        'Predicted': predicted,
                        'Difference': diff})

print('Average diff: ' + str(sum(abs(diff))*10000/len(diff)) + ' pips')

plt.plot(diff)

## plotting

plt.figure(figsize=(12,5))
plt.xlabel('Actual vs. Predicted')

ax1 = pd.DataFrame(predicted).plot(color='blue', grid=True, label='Predicted')
ax2 = y_test[['Close']].plot(color='red', grid=True, secondary_y=True, label='Actual')

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()

plt.legend(h1+h2, l1+l2, loc=2)
plt.show()
