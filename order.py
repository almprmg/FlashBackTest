
import pandas as pd

class _unit:
     
    @staticmethod
    def swap(_from,to):
            return  to,_from

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
        self.x = 0



    def _process_order(self):
            if self.is_long():
                return self.long_order()
            self.short_order()

    def long_order(self):
        self.Date_finish_order()
    def short_order(self):
        self.tp,self.sl= _unit.swap(self.tp,self.sl)
        self.Date_finish_order()
        self._date_tp,self._date_sl = _unit.swap(self._date_tp,self._date_sl)

    def is_long(self):
        return self._type == 1
    def is_short(self): # is order short or long
        return not self.is_long() 
    

    def check_empty(self, DHigh, DLow ): 
        self._date_tp = DHigh.index[0] if  not DHigh.empty else None
        self._date_sl = DLow.index[0] if not DLow.empty  else None
        
    def Date_finish_order(self):
        DHigh =  self.data_low.loc[self.data_low.High >= self.tp]
        DLow =  self.data_low.loc[self.data_low.Low <= self.sl]
        self.check_empty(DHigh,DLow)

    def _open_order(self,type_order,limit,tp,sl):
        self._type =type_order
        self.__order[["IdOrder","Type","DateStart","Enter","tp","sl"]] = [str(type_order)+str(len( self._result_orders)),type_order,self.Date_Start_order,limit,tp,sl]



    def _close_order(self,goal:bool,Date):
        self.x +=1
        if self.x == 15 :
            print(self.x)     
        
        self.__order[[ "Target","EndDate"]] = [goal,Date]
        self.Date_end_order = Date
        self._position =False
        self._result_orders = pd.concat([self._result_orders,self.__order ] ,axis=0,ignore_index=True)        

         