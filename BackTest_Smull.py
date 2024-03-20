

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
            date = self.data_low.index
            high =  self.data_low.loc[self.data_low.High >= self.tp]
            Low =  self.data_low.loc[self.data_low.Low <= self.sl]
            high = high.index[0] if  not high.empty else Low.index[1]
            Low = Low.index[0] if not Low.empty  else high
               
            
            
            
            
            
            

        except Exception as ex :
      
            print(ex)

            


        if high == None and Low == None:
            self.Date_ende_order = self.data_low.index[-1] 
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
    
        
    