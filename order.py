import pandas as pd


class orders:
    result_orders = pd.DataFrame({"IdOrder":[],"Type":[],"DateStart":[] ,"Enter":[] ,"tp":[],"sl":[] , "Target":[],"EndDate":[]})
    order = pd.DataFrame({"IdOrder":[0],"Type":[0],"DateStart":[0] ,"Enter":[0] ,"tp":[0],"sl":[0] , "Target":[0],"EndDate":[0]})
    
    def __init__(self) -> None:
        self.tp = None
        self.sl = None
        self.limit =None
        self.Date_Start_order =None
        self.Date_end_order = None
        self._position =False

        
    def buy(self, limit:float,tp: float,sl:float)-> None:
        if not self._position:
            self.sl = sl
            self.tp =tp
            self.limit =limit
            self.order[["IdOrder","Type","DateStart","Enter","tp","sl"]] = ['1'+str(len( self.result_orders)),1,self.Date_Start_order,limit,tp,sl]
            self._position = True

            

            
    def sell(self, limit:float,tp: float,sl:float):
        if not self._position:
            self.sl = sl
            self.tp =tp
            self.limit =limit
            self.order[["IdOrder","Type","DateStart","Enter","tp","sl"]] = ['0'+str(len( self.result_orders)),2,self.Date_Start_order,limit,tp,sl]
            self._position = True



    def saveTpOrdersBuy(self,Date_TP):
        self.order[[ "Target","EndDate"]] = [1,Date_TP]
        self.Date_end_order = Date_TP
        self._position =False
    def saveSlOrdersBuy(self,Date_SL):
        self.order[[ "Target","EndDate"]] = [0,Date_SL]
        self.Date_end_order = Date_SL
        self._position =False
    def saveTpOrdersSell(self,Date_TP):
        self.order[[ "Target","EndDate"]] = [2,Date_TP]
        self.Date_end_order = Date_TP
        self._position =False
    def saveSlOrdersSell(self,Date_SL):
        self.order[[ "Target","EndDate"]] = [0,Date_SL]
        self.Date_end_order = Date_SL
        self._position =False
    def Save_order(self):
       self.result_orders = pd.concat([self.result_orders,self.order ] ,axis=0,ignore_index=True) 

