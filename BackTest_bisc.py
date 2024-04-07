from numbers import Number
import numpy as np
import pandas as pd
from Stratigy import Strategy
from Calculator import UnCumulativeTradeProfit,CumulativeTradeProfit
class  FastBackTesting:
    """
    fastbacktesting a particular (parameterized) strategy
    on particular data.

    Upon initialization, call method 
    `fastbacktesting.fastbacktesting.BackTest.run` to run a backtest
    instance
    """
    def __init__(self,
                 data: pd.DataFrame ,
                 data_small: pd.DataFrame ,
                 strategy:type[Strategy] ,
                 cash: int = 1000 ,
                 ratio_entry:int = 1000 ,
                 fees: float = 0.001 ,
                 cp: bool = False ) -> None:

        if not (isinstance(strategy, type) and issubclass(strategy, Strategy)):
            raise TypeError('`strategy` must be a Strategy sub-type')
        if not isinstance(data, pd.DataFrame):
            raise TypeError("`data` must be a pandas.DataFrame with columns")
        if not isinstance(data_small, pd.DataFrame):
            raise TypeError("`data` must be a pandas.DataFrame with columns")
        if not isinstance(cash, Number):
            raise TypeError('`Cash` must be a float value, percent of '
                            'entry order price')
        data = data.copy(deep=False)

        # Convert index to datetime index
        if (not isinstance(data.index, pd.DatetimeIndex) and
            not isinstance(data.index, pd.RangeIndex) and
            # Numeric index with most large numbers
            (data.index.is_numeric() and
             (data.index > pd.Timestamp('1975').timestamp()).mean() > .8)):
            try:
                data.index = pd.to_datetime(data.index, infer_datetime_format=True)
            except ValueError:
                pass

        if 'Volume' not in data:
            data['Volume'] = np.nan

        if len(data) == 0:
            raise ValueError('OHLC `data` is empty')
        if len(data.columns.intersection({'Open', 'High', 'Low', 'Close', 'Volume'})) != 5:
            raise ValueError("`data` must be a pandas.DataFrame with columns "
                             "'Open', 'High', 'Low', 'Close', and (optionally) 'Volume'")
        if data[['Open', 'High', 'Low', 'Close']].isnull().values.any():
            raise ValueError('Some OHLC values are missing (NaN). '
                             'Please strip those lines with `df.dropna()` or '
                             'fill them in with `df.interpolate()` or whatever.')
        self.__ishave_signal =  "Signal" in data.columns
        self.result = pd.DataFrame


        self.choose_iscp(cash, ratio_entry, fees, cp)

        if self.__ishave_signal:
            data = data.loc[data.Signal != 0]
            date = data.index[0]
        else:
            date = data.index[1]
            self.__index = data.index
        self.strategy = strategy(date ,data ,data_small)




    def choose_iscp(self, cash, ratio_entry, fees, cp):
        """Choose if you want to set the strategy with the cumulative profit or a fixed amount.
        """
        if cp:
            self.cal_traded = CumulativeTradeProfit(cash ,ratio_entry ,fees)
        else:
            self.cal_traded = UnCumulativeTradeProfit(cash ,ratio_entry ,fees)


    def run(self) :

        """Run the backtest. Returns `int Return [%] strategy` with results and statistics.
        """
        if self.__ishave_signal:

            while self.strategy.is_data_finsh() :
                self.strategy.next()
                self.strategy.trading()
            self.result = self.cal_traded.profit(self.strategy.get_alorder())
            return
        for index in  self.__index :
            if index > self.strategy.date_end_order and self.strategy.is_data_finsh():
                self.strategy.refresh_data(index)
                self.strategy.next()
                if self.strategy.is_position():
                    self.strategy.trading()
        self.result =  self.cal_traded.profit(self.strategy.get_alorder())