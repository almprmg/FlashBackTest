

import pandas as pd
from BackTest.BackTest_Smull import Bacl_Test_smunll


class Stratigy(Bacl_Test_smunll):
    order = None
    
    order_ ={"DateStart" : [],"Enter" : [] ,"Tp" : [],"Sl" : [] ,"Targit" : [],"DateEnd" : []}
    def __init__(self,data_low,Date) -> None:
        self.data_low = self.data_low.loc[data_low.index >= pd.Timestamp(Date)]
        self.Date = Date
        self._postin = False
        self.Date_ende_order = None
        
        super()
        
        
    def buy(self, limet,tp: float,sl:float):
        if not self._postin:
            self.order = [self.Date,limet,tp,sl]
            
    def sell(self, limet:float,tp: float,sl:float):
        if not self._postin:
            self.order = [self.Date,limet,tp,sl]
               
    def Check_Order(self):
        self.Date_ende_order = super().next()

