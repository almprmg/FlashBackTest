

import pandas as pd
from BackTest_Smull import Bacl_Test_smunll 


class Stratigy(Bacl_Test_smunll):

    
    
    
    def __init__(self,data_low:type[pd.DataFrame],Date) -> None:
        super().__init__()
        self.Date_Start_order = Date
        self.Data : type[pd.DataFrame]
        self.data_low = data_low.loc[data_low.index >= self.Date_Start_order]
    
    def update(self)-> None:
        self.Trade()
        self.Save_order()
        self.Data = self.Data.iloc[self.Data.index >  self.Date_ende_order,:]
        self.Data
        data = self.Data.loc[self.Data.Signal == 1]
        if self.Date_ende_order != self.data_low.index[-1] and len(data) !=0 :
            self.Date_Start_order =data.index[0]
            self.data_low = self.data_low.iloc[self.data_low.index >=  self.Date_Start_order,:]
    
    def next(self)-> None:...
    
    def init(self)-> None:...