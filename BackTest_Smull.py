


from Order import orders


class Best_Test_small(orders):
    _position = False
    Type = None
    Date_TP = None 
    Date_SL = None
    def __init__(self) -> None:
        super().__init__()
        self.data_low = None
        self.Date_ende_order = None

    
    def Trade(self):
        self.Check_position()

        if self.Date_TP != None and self.Date_SL != None  :
            if (self.Date_TP < self.Date_SL and self.Type == 1) :
                self.saveTpOrdersBuy(self.Date_TP)  
            elif (self.Date_TP < self.Date_SL):
                self.saveTpOrdersSell(self.Date_TP)
            elif (self.Date_TP > self.Date_SL and self.Type == 1) :
                self.saveSlOrdersBuy(self.Date_SL)
            elif (self.Date_TP > self.Date_SL and self.Type == 2): 
                self.saveSlOrdersSell(self.Date_SL)
        elif  self.Date_TP == None and self.Date_SL != None :
            if self.Type:
                self.saveSlOrdersBuy(self.Date_SL)
            else : 
                self.saveSlOrdersSell(self.Date_SL)
        elif self.Date_TP != None and self.Date_SL == None :
            if self.Type:
                self.saveTpOrdersBuy(self.Date_TP)
            else : 
                self.saveTpOrdersSell(self.Date_TP)
    def swap(self):

         self.Type= self.order['Type'][0]
         if self.Type == 2 :
            temp = self.tp 
            self.tp = self.sl
            self.sl = temp
         

    
    def Check_position(self):
       
            self.swap()
            Dhigh =  self.data_low.loc[self.data_low.High >= self.tp]
            DLow =  self.data_low.loc[self.data_low.Low <= self.sl] 
            self.Date_TP = Dhigh.index[0] if  not Dhigh.empty else None
            self.Date_SL = DLow.index[0] if not DLow.empty  else None
            if not self.Type:
                temp =  self.Date_TP
                self.Date_TP =self.Date_SL
                self.Date_SL = temp
       

     
