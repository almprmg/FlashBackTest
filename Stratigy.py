

import pandas as pd
from BackTest_Smull import Bacl_Test_smunll


class Stratigy(Bacl_Test_smunll):

    
    result_orders = []

    def __init__(self,data_low:type[pd.DataFrame],Date) -> None:
        super()
        self.Date = Date
        self.Data : type[pd.DataFrame]
        self.data_low = data_low.loc[data_low.index >= self.Date]
        
       
      

        
        
        
    def buy(self, limet:float,tp: float,sl:float)-> None:
        if not self._postin:
            self.sl = sl
            self.tp =tp
            self.limet =limet
            self.order = [self.Date,limet,tp,sl]
            self._postin = True
            self.Trade()
            self.add_order()
            self.update()
            

            
    def sell(self, limet:float,tp: float,sl:float):
        if not self._postin:
            self.sl = sl
            self.tp =tp
            self._postin = True
    def add_order(self):
        self.result_orders.append(self.order)
    
    def update(self)-> None:
        self.Data = self.Data.loc[self.Data.index >=  self.Date_ende_order]
        if self.Date_ende_order != self.data_low.index[-1]:
            self.Date = self.Data.loc[self.Data.Signal != 0].index[0]
            self.data_low = self.data_low.loc[self.data_low.index >=  self.Date]
        
    def next(self)-> None:...
    def init(self)-> None:...