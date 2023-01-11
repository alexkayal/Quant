import numpy as np

def timeseries_df(X, label, n):
    
    df = X[[label]]
  
    for i in range(n):
        df[label+'_'+str(i+1)] = df[label].shift(periods=i+1)
    
    df = df.drop([label], axis=1)
    df.index = X.index
    df = df.iloc[n:]
    
    return df


def get_hitrate(df):
    df['hit'] = np.nan
    for index, row in df.iterrows():
        if df['y_pred'][index] >= df['low'][index] and df['y_pred'][index] <= df['high'][index]:
            df['hit'][index] = True
        else:
            df['hit'][index] = False
    return df, sum(df['hit'])/len(df['hit'])


def get_direction(df):
    df['direction'] = np.nan
    for index, row in df.iterrows():
        if df['y_pred'][index] >= df['open'][index] and df['close'][index] >= df['open'][index]:
            df['direction'][index] = True
        elif df['y_pred'][index] <= df['open'][index] and df['close'][index] <= df['open'][index]:
            df['direction'][index] = True
        else:
            df['direction'][index] = False
    return df, sum(df['direction'])/len(df['direction'])


def get_OR(df):
    df['OR'] = np.nan
    for index, row in df.iterrows():
        if df['hit'][index] == True or df['direction'][index] == True:
            df['OR'][index] = True
        else:
            df['OR'][index] = False
    return df, sum(df['OR'])/len(df['OR'])


def get_pips(df, multiplier):
    df['pips'] = np.nan
    for index, row in df.iterrows():
        if df['hit'][index] == True:
            df['pips'][index] = abs(df['y_pred'][index] - df['open'][index])*multiplier
        elif df['hit'][index] == False and df['direction'][index] == True:
            df['pips'][index] = abs(df['close'][index] - df['open'][index])*multiplier
        else:
            df['pips'][index] = abs(df['close'][index] - df['open'][index])*-multiplier
    return df, sum(df['pips'])


def download_tickers(folder, tickers):
    for ticker in tickers:
        ohlcv_d = yf.download(ticker, period='12y', interval="1d")
        ohlcv_w = yf.download(ticker, period='12y', interval="1wk")
        ohlcv_d.to_csv(folder+'/'+ticker+'_12y_daily.csv')
        ohlcv_w.to_csv(folder+'/'+ticker+'_12y_weekly.csv')


def prep_metatrader_data(ohlcv):
    ohlcv = ohlcv.rename(columns = {'<DATE>': 'Date',
                                    '<TIME>': 'Time',
                                    '<OPEN>': 'Open',
                                    '<HIGH>': 'High',
                                    '<LOW>': 'Low',
                                    '<CLOSE>': 'Close',
                                    '<TICKVOL>': 'Volume'}, inplace = False)


    ohlcv = ohlcv.drop(['<VOL>', '<SPREAD>'], axis='columns', inplace=False)
    
    if 'Time' in ohlcv.columns:    
        ohlcv['DateTime'] = ohlcv['Date'] + ' ' + ohlcv['Time']
        ohlcv = ohlcv.drop(['Date', 'Time'], axis='columns', inplace=False)
        ohlcv = ohlcv.set_index('DateTime')
    
    else:
        ohlcv = ohlcv.set_index('Date')
    ohlcv['Median'] = (ohlcv['High'] + ohlcv['Low'])/2
    return ohlcv