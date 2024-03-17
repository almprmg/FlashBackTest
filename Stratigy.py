

import pandas as pd
from BackTest.BackTest_Smull import Bacl_Test_smunll


class Stratigy(Bacl_Test_smunll):

    
    order_ = []
    def __init__(self,data_low,Date) -> None:
        
        self.data_low = self.data_low.loc[data_low.index >= pd.Timestamp(Date)]
        self.Date = Date
        self.Date_ende_order = None

        
        
        
    def buy(self, limet:float,tp: float,sl:float):
        if not self._postin:
            self.sl = sl
            self.tp =tp
            self.order = [self.Date,limet,tp,sl]
            self._postin = True
            
    def sell(self, limet:float,tp: float,sl:float):
        if not self._postin:
            self.sl = sl
            self.tp =tp
            self.order = [self.Date,limet,tp,sl]
            self._postin = True
          
    def next(self)-> None:...
    def init(self)-> None:...