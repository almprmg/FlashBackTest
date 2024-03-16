

import pandas as pd
from BackTest.BackTest_Smull import Bacl_Test_smunll


class Stratigy(Bacl_Test_smunll):
    tp = None
    sl =None
    limet =None
    def __init__(self,data,data_low) -> None:
        self.data_low = self.data_low.loc[data_low.Date >= pd.Timestamp(data.Date[-1])]
        self.data=data 
        self._postin = False
        self.Date_ende_order = None
        super()
        
        
    def buy(self, limet,tp: float,sl:float):
        if not self._postin:
            self.tp: float =tp 
            self.sl: float =sl
            self.limet: float =limet
            
            
    def Check_Order(self):
        self.Date_ende_order = super().next()

