# do next() on the 1m timeframe
# buy if top of 1h/1d timeframe, set tp to certain value
# close if closing criteria met (past full 1h/1d candle, 0 profit/loss)
# try using same timeframe with simulated sell knowing we hit the price
# simulate

import backtrader as bt
from datetime import datetime
import pandas as pd

class MyStrategy(bt.Strategy):
    params = (
        ('sma_period', 20),  # Period for the moving average
    )

    def __init__(self):
        self.data_hourly = self.datas[0].resample('1H')  # Resample to 1-hour data
        self.sma_hourly = bt.indicators.SimpleMovingAverage(
            self.data_hourly.close, period=self.params.sma_period
        )

    def next(self):
        if len(self.data_hourly) < self.params.sma_period:
            return  # Not enough data for the moving average

        if self.data_hourly.datetime.datetime().hour == 0:
            print("Current hour is 0")

        if self.data.close[0] > self.sma_hourly[0]:
            self.buy()

        elif self.data.close[0] < self.sma_hourly[0]:
            self.sell()

cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)

# Load 1-minute data
data = bt.feeds.YahooFinanceData(dataname='AAPL',
                                 fromdate=datetime(2022, 1, 1),
                                 todate=datetime(2022, 12, 31)
                                 )

cerebro.adddata(data)

cerebro.run()
