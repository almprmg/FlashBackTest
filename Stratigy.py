

import pandas as pd
from BackTest_Smull import Bacl_Test_smunll


class Stratigy(Bacl_Test_smunll):
    tp = None
    sl =None
    limet =None
    def __init__(self,data,data_low) -> None:
        self.data_low = data_low.loc[data_low.Date > pd.Timestamp('2022-09-02 17:00:00')]
        self.data=data 
        self._postin = False
        self.Date_ende_order = None
  
        
        
    def buy(self, limet,tp: float,sl:float):
        if not self._postin:
            self.tp: float =tp 
            self.sl: float =sl
            self.limet: float =limet
            data = self.data_low.loc[self.data_low.Date < pd.Timestamp('2022-09-02 18:00:00')]
            low_limt =  data_low.loc[data.High >= limet,'Low']
            low_tp =  data_low.loc[data_low.Low >= self.tp,'Low']
            self.check = low_limt.index[0] < low_tp.index[0]
           


            
            
    def Check_Order(self):
        self.Date_ende_order = super().next()

