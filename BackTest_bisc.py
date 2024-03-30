from numbers import Number
import pandas as pd
from Stratigy import Strategy
from Calculator import UnCumulativeTradeProfit,CumulativeTradeProfit



class  BackTest:
    """
    First discrete difference of element.
        .......et
    Parameters
    ----------
    Cash
    RatioEntry
    cp = cumulative profit
    """
    def __init__(self,
                 data : pd.DataFrame,data_small :  pd.DataFrame,
                 strategy :type[Strategy] ,cash : int = 1000 ,
                 ratio_entry :int = 1000 ,fees : float = 0.001 ,
                 cp : bool = False ) -> None:

        if not (isinstance(strategy, type) and issubclass(strategy, Strategy)):
            raise TypeError('`strategy` must be a Strategy sub-type')
        if not isinstance(data, pd.DataFrame):
            raise TypeError("`data` must be a pandas.DataFrame with columns")
        if not isinstance(data_small, pd.DataFrame):
            raise TypeError("`data` must be a pandas.DataFrame with columns")
        if not isinstance(cash, Number):
            raise TypeError('`Cash` must be a float value, percent of '
                            'entry order price')
        if cp:
            self.cal_traded = CumulativeTradeProfit(cash ,ratio_entry ,fees)
        else:
            self.cal_traded = UnCumulativeTradeProfit(cash ,ratio_entry ,fees)
        self.end_date = data.index[-1]
        self.columns = data.columns
        date = data.loc[data.Signal != 0 ].index[0]

        self.strategy = strategy(date ,data ,data_small)
        self.strategy.init()
        self.result = pd.DataFrame


    def run(self) :

        if "Signal" in self.columns:

            #not Strategy.Data[ Strategy.Data.Signal != 0 ].empty
            while not self.strategy.data[ self.strategy.data.Signal != 0 ].empty :
                self.strategy.next()
                self.strategy.trade()
                self.strategy.update()
        self.result = self.strategy.get_result() #self.cal_traded.profit()
