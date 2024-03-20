

import pandas as pd

from order import orders


class Bacl_Test_smunll(orders):
    _postin = False
    Type = None
    Date_TP = None 
    Date_SL = None
    def __init__(self) -> None:
        super().__init__()
        self.data_low = None
        self.Date_ende_order = None
    
    def Trade(self):
        self.Check_postion()
        checkTpNone = self.Date_TP == None and self.Date_SL != None
        if self.Date_TP != None and self.Date_SL != None  :
            if (self.Date_TP < self.Date_SL and self.Type) :
                self.TpOredes_Buy()  
            elif (self.Date_TP < self.Date_SL):
                self.TpOredes_Sell()
            elif (self.Date_TP > self.Date_SL and self.Type) :
                self.SlOredes_Buy()
            else : 
                self.SlOredes_Sell()
        elif  checkTpNone :
            if self.Type:
                self.SlOredes_Buy()
            else : 
                self.SlOredes_Sell()
        elif not checkTpNone :
            if self.Type:
                self.SlOredes_Buy()
            else : 
                self.SlOredes_Sell()
    def swap(self):
         self.Type= self.order[-1][1]
         if not self.Type :
            temp = self.tp 
            self.tp = self.sl
            self.sl = temp
         

    @swap
    def Check_postion(self):
        try:


           
            Dhigh =  self.data_low.loc[self.data_low.High >= self.tp]
            DLow =  self.data_low.loc[self.data_low.Low <= self.sl] 
            self.Date_TP = Dhigh.index[0] if  not Dhigh.empty else None
            self.Date_SL = DLow.index[0] if not DLow.empty  else None
            if not self.Type:
                temp =  self.Date_TP
                self.Date_TP =self.Date_SL
                self.Date_SL = temp
        except Exception as ex :
            print(ex)         

     
