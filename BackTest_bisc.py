from numbers import Number
import pandas as pd 
import numpy as np
from Stratigy import Strategy
from Calculator import unCumulative_Trade_profit,cumulative_trade_profit



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
                 strategy :type[Strategy],Cash : int = 1000 ,
                 RatioEntry :int =1000 ,Fees : float = 0.001,
                cp : bool = False ) -> None:

        
        if not (isinstance(strategy, type) and issubclass(strategy, Strategy)):
            raise TypeError('`strategy` must be a Strategy sub-type')
        if not isinstance(data, pd.DataFrame):
            raise TypeError("`data` must be a pandas.DataFrame with columns")
        if not isinstance(data_small, pd.DataFrame):
            raise TypeError("`data` must be a pandas.DataFrame with columns")
        if not isinstance(Cash, Number):
            raise TypeError('`Cash` must be a float value, percent of '
                            'entry order price')
        
        
        if cp:
            self.CalTraded = cumulative_trade_profit(Cash ,RatioEntry ,Fees)
        else:
            self.CalTraded = unCumulative_Trade_profit(Cash ,RatioEntry ,Fees)
            

        self.data = data
        self.data_small = data_small  
        self.Strategy = strategy
        self.endDate =self.data.index[-1]
  

    def run(self):
        
        Strategy = self.Strategy(self.data_small,self.data.loc[self.data.Signal != 0 ].index[0])
        Strategy.init()
        Strategy.Data = self.data
        if "Signal" in self.data.columns:

            #not Strategy.Data[ Strategy.Data.Signal != 0 ].empty
            while not Strategy.Data[ Strategy.Data.Signal != 0 ].empty :

                Strategy.next()
                Strategy.trade()
                Strategy.update()
        self.result = self.CalTraded.profit(Strategy._result_orders)


    