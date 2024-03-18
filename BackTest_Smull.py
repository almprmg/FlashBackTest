

import pandas as pd


class Bacl_Test_smunll:
    _postin = False
    def __init__(self) -> None:
        self.data_low = None
        self.tp = None
        self.sl = None
        self.limet =None
        self.order = None
        
        self.Date_ende_order = None
    
    def Trade(self):
        try:
            high =  self.data_low.loc[self.data_low.High >= self.tp].index[0]
            Low =  self.data_low.loc[self.data_low.Low <= self.sl].index[0]
        except Exception as ex :
            print(ex)
            high =None
            Low =None
            


        if high == None and Low == None:
            self.Date_ende_order = self.data_low.index[-1] 
            self._postin =False
        if high != None and Low != None :
            check = high < Low
            if check  :
                self.order.append(1)
                self.order.append(high)
                self.Date_ende_order = high
                self._postin =False
    
            else:
                self.order.append(0)
                self.order.append(Low)
                self.Date_ende_order = Low
                self._postin =False
    
        
    