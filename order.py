import pandas as pd


class orders:
    result_orders = pd.DataFrame({"IdOrder":[],"DateStart":[] ,"Enter":[] ,"tp":[],"ls":[] , "Targit":[],"EndDate":[]})
    def __init__(self) -> None:
        self.order = pd.DataFrame({"IdOrder":[0],"Type":[0],"DateStart":[0] ,"Enter":[0] ,"tp":[0],"ls":[0] , "Targit":[0],"EndDate":[0]})
        self.tp = None
        self.sl = None
        self.limet =None
        self.Date_Start_order =None
        self.Date_ende_order = None
        self._postin =False

        
    def buy(self, limet:float,tp: float,sl:float)-> None:
        if not self._postin:
            self.sl = sl
            self.tp =tp
            self.limet =limet
            self.order[["IdOrder","Type","DateStart","Enter","tp","ls"]] = [0+len( self.result_orders),1,self.Date_Start_order,limet,tp,sl]
            self._postin = True

            

            
    def sell(self, limet:float,tp: float,sl:float):
        if not self._postin:
            self.sl = sl
            self.tp =tp
            self.limet =limet
            self.order[["IdOrder","Type","DateStart","Enter","tp","ls"]] = [0+len( self.result_orders),2,self.Date_Start_order,limet,tp,sl]
            self._postin = True



    def TpOredes_Buy(self,Date_TP):
        self.order[[ "Targit","EndDate"]] = [1,Date_TP]
        self.Date_ende_order = Date_TP
        self._postin =False
    def SlOredes_Buy(self,Date_SL):
        self.order[[ "Targit","EndDate"]] = [0,Date_SL]
        self.Date_ende_order = Date_SL
        self._postin =False
    def TpOredes_Sell(self,Date_TP):
        self.order[[ "Targit","EndDate"]] = [2,Date_TP]
        self.Date_ende_order = Date_TP
        self._postin =False
    def SlOredes_Sell(self,Date_SL):
        self.order[[ "Targit","EndDate"]] = [0,Date_SL]
        self.Date_ende_order = Date_SL
        self._postin =False
    def Save_order(self):
       self.result_orders = pd.concat([self.result_orders,self.order ] ,axis=0,ignore_index=True) 

