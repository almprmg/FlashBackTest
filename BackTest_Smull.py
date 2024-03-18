

import pandas as pd


class Bacl_Test_smunll:
    _postin = False
    def __init__(self) -> None:
        self.data_low = None
        self.tp = None
        self.sl = None
        self.limet =None
        self.order = pd.DataFrame({"DateStart":[0] ,"Enter":[0] ,"tp":[0],"ls":[0] , "Targit":[0],"EndDate":[0]})
        
        self.Date_ende_order = None
    
    def Trade(self):
        try:
            high =  self.data_low[self.data_low.High >= self.tp].index[0][0]
            Low =  self.data_low[self.data_low.Low <= self.sl].index[0][0]

            
            

        except Exception as ex :
            print(ex)
            high =None
            Low =None
            


        if high == None and Low == None:
            self.Date_ende_order = self.data_low.Date[-1] 
            self._postin =False
        if high != None and Low != None :
            check = high < Low
            if check  :
                self.order[[ "Targit","EndDate"]] = [1,high]

                self.Date_ende_order = high
                self._postin =False
    
            else:
                self.order[[ "Targit","EndDate"]] = [0,Low]
                self.Date_ende_order = Low
                self._postin =False
    
        
    