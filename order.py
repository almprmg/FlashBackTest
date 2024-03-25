import pandas as pd


class orders:

    def __init__(self) -> None:
        self._result_orders = pd.DataFrame({"IdOrder":[],"Type":[],"DateStart":[] ,"Enter":[] ,"tp":[],"sl":[] , "Target":[],"EndDate":[]})
        self.__order = pd.DataFrame({"IdOrder":[0],"Type":[0],"DateStart":[0] ,"Enter":[0] ,"tp":[0],"sl":[0] , "Target":[0],"EndDate":[0]})
        self._type = None
        self._date_tp = None 
        self._date_sl = None
        self.tp = None
        self.sl = None
        self.limit =None
        self.Date_Start_order =None
        self.Date_end_order = None
        self._position =False
        self.data_low = None



    def _process_order(self):
       
            self.swap()
            Dhigh =  self.data_low.loc[self.data_low.High >= self.tp]
            DLow =  self.data_low.loc[self.data_low.Low <= self.sl] 
            self._date_tp = Dhigh.index[0] if  not Dhigh.empty else None
            self._date_sl = DLow.index[0] if not DLow.empty  else None
            if not self._type:
                temp =  self._date_tp
                self._date_tp =self._date_sl
                self._date_sl = temp
    def _open_order(self,type_order,limit,tp,sl):
        self.__order[["IdOrder","Type","DateStart","Enter","tp","sl"]] = [type_order+str(len( self._result_orders)),1,self.Date_Start_order,limit,tp,sl]

 

    def _close_order(self,goal:bool,Date):
        self.__order[[ "Target","EndDate"]] = [goal,Date]
        self.Date_end_order = Date
        self._position =False
        self._result_orders = pd.concat([self._result_orders,self.__order ] ,axis=0,ignore_index=True)        

    def swap(self):

         self._type= self.__order['Type'][0]
         if self._type == 2 :
            temp = self.tp 
            self.tp = self.sl
            self.sl = temp
         