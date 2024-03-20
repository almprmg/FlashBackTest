

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

        if self.Date_TP != None and self.Date_SL != None  :
            if (self.Date_TP < self.Date_SL and self.Type == 1) :
                self.TpOredes_Buy(self.Date_TP)  
            elif (self.Date_TP < self.Date_SL):
                self.TpOredes_Sell(self.Date_TP)
            elif (self.Date_TP > self.Date_SL and self.Type == 1) :
                self.SlOredes_Buy(self.Date_SL)
            elif (self.Date_TP > self.Date_SL and self.Type == 2): 
                self.SlOredes_Sell(self.Date_SL)
        elif  self.Date_TP == None and self.Date_SL != None :
            if self.Type:
                self.SlOredes_Buy(self.Date_SL)
            else : 
                self.SlOredes_Sell(self.Date_SL)
        elif self.Date_TP != None and self.Date_SL == None :
            if self.Type:
                self.TpOredes_Buy(self.Date_TP)
            else : 
                self.TpOredes_Sell(self.Date_TP)
    def swap(self):

         self.Type= self.order['Type'][0]
         if self.Type == 2 :
            temp = self.tp 
            self.tp = self.sl
            self.sl = temp
         

    
    def Check_postion(self):
       
            self.swap()
            Dhigh =  self.data_low.loc[self.data_low.High >= self.tp]
            DLow =  self.data_low.loc[self.data_low.Low <= self.sl] 
            self.Date_TP = Dhigh.index[0] if  not Dhigh.empty else None
            self.Date_SL = DLow.index[0] if not DLow.empty  else None
            if not self.Type:
                temp =  self.Date_TP
                self.Date_TP =self.Date_SL
                self.Date_SL = temp
       

     
