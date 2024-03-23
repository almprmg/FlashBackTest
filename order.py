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

    
    def OpenOrder(self):
        pass

    def CloseOrder(self,goal:bool,Date):
        self.order[[ "Target","EndDate"]] = [goal,Date]
        self.Date_end_order = Date
        self._position =False
        self.result_orders = pd.concat([self.result_orders,self.order ] ,axis=0,ignore_index=True) 
    #def saveSlOrdersBuy(self,Date_SL):
    #    self.order[[ "Target","EndDate"]] = [0,Date_SL]
    #    self.Date_end_order = Date_SL
    #    self._position =False
    #def saveTpOrdersSell(self,Date_TP):
    #    self.order[[ "Target","EndDate"]] = [2,Date_TP]
    #    self.Date_end_order = Date_TP
    #    self._position =False
    #def saveSlOrdersSell(self,Date_SL):
    #    self.order[[ "Target","EndDate"]] = [0,Date_SL]
    #    self.Date_end_order = Date_SL
    #    self._position =False
    #def Save_order(self):
       

