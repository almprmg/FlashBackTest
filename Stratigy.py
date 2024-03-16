

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
            low_limt =  data.loc[data.Low <= limet,'Low']
            low_tp =  data.loc[data.Low <= self.tp,'Low']
            check = low_limt.index[0] < low_tp.index[0]
            if not check:
                self.data_low=self.data_low.loc[self.data_low.Date > pd.Timestamp(data_low.Date[low_tp.index[0]])]
                

           


            
            
    def Check_Order(self):
            self.Date_ende_order = super().next()

import pandas as pd
timeframe = "1h"
timeflow = "5m"
symbol = "AGLDUSDT"
data = pd.read_csv(f'C:/Users/dell/Desktop/module Python for Analysis Tradr/data/{timeframe}/{symbol}.csv',index_col=0)
data.Date  = pd.to_datetime(data.Date ,unit='ms')
data_low = pd.read_csv(f'C:/Users\dell/Desktop/module Python for Analysis Tradr/data/{timeflow}/{symbol}.csv',index_col=0)
data_low.Date  = pd.to_datetime(data_low.Date ,unit='ms')
st = Stratigy(data,data_low)
st.buy(0.347,0.38535,0.335)
st.Check_Order()
print(st.Date_ende_order)