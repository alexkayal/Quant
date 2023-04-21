import backtrader as bt
import backtrader.feeds as btfeeds
from datetime import datetime

class MyStrategy(bt.Strategy):
    
    params = (
        ('fast_period', 10),
        ('slow_period', 20)
    )
    
    def __init__(self):
        self.fast_sma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.params.fast_period
        )
        
        self.slow_sma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.params.slow_period
        )
        
        self.crossover = bt.indicators.CrossOver(
            self.fast_sma,
            self.slow_sma
        )
    
    def next(self):
        if self.position.size == 0 and self.crossover > 0:
            self.buy()
        elif self.position.size > 0 and self.crossover < 0:
            self.sell()

cerebro = bt.Cerebro()

forex_data = btfeeds.GenericCSVData(
    dataname='../CSVData/EURUSD_H1_201704030000_202104010000.csv',
    dtformat=('%Y.%m.%d'),
    tmformat=('%H:%M:%S'),
    separator='\t',
    #timeframe=bt.TimeFrame.Days, 
    #compression=1,
    datetime=0,
    time=1,
    high=3, 
    low=4, 
    open=2, 
    close=5, 
    volume=7, 
    openinterest=-1
)

# Add the forex data to cerebro
cerebro.adddata(forex_data)

# Add the strategy to cerebro
cerebro.addstrategy(MyStrategy)

# Run the backtest
cerebro.run(writer=True, verbose=2)

# Print the final portfolio value
print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")