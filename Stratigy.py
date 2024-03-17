

import pandas as pd
from BackTest.BackTest_Smull import Bacl_Test_smunll


class Stratigy(Bacl_Test_smunll):

    
    order_ = []

    def __init__(self,data_low) -> None:
        self.Date = type[pd.Timestamp]
        self.Data : type[pd.DataFrame]
        self.data_low = self.data_low.loc[data_low.index >= pd.Timestamp(self.Date)]
        
       
      

        
        
        
    def buy(self, limet:float,tp: float,sl:float)-> None:
        if not self._postin:
            self.sl = sl
            self.tp =tp
            self.order = [self.Date,limet,tp,sl]
            self._postin = True
            self.update(self)
            

            
    def sell(self, limet:float,tp: float,sl:float):
        if not self._postin:
            self.sl = sl
            self.tp =tp
            self.order = [self.Date,limet,tp,sl]
            self._postin = True

    def update(self)-> None:
        self.Trade()
        self.Data = self.Data.loc[self.Data.index >=  self.Date_ende_order]
        self.Date = self.Data.loc[self.Data.Signal != 0].index[0]
    
    def next(self)-> None:...
    def init(self)-> None:...