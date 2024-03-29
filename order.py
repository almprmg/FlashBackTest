import pandas as pd

class _unit:
    @staticmethod
    def swap(first,secund):
        return  secund ,first

class Orders:
    def __init__(self,date_start_order,data,data_low) -> None:
        self.result_orders = pd.DataFrame({"IdOrder":[] ,
                                            "Type":[] ,
                                            "DateStart":[],
                                            "Enter":[] ,
                                            "tp":[]
                                            ,"sl":[] ,
                                            "Target":[],
                                            "EndDate":[]
                                            })
        self.__order = pd.DataFrame({"IdOrder":[0],
                                     "Type":[0],
                                     "DateStart":[0] ,
                                     "Enter":[0] ,
                                     "tp":[0],
                                     "sl":[0] ,
                                     "Target":[0],
                                     "EndDate":[0]
                                     })
        self._type = None
        self._date_tp = None
        self._date_sl = None
        self.tp = None
        self.sl = None
        self.limit =None
        self.date_start_order = date_start_order
        self.date_end_order   = None
        self._position =False
        self.data_low = data_low.loc[data_low.index >= self.date_start_order]
        self.data = data



    def _process_order(self):
            if self.is_long():
                return self.long_order()
            self.short_order()

    def long_order(self):
        self.date_finish_order()

    def short_order(self):
        self.tp,self.sl= _unit.swap(self.tp,self.sl)
        self.date_finish_order()
        self._date_tp,self._date_sl = _unit.swap(self._date_tp,self._date_sl)

    def is_long(self):
        return self._type == 1
    def is_short(self): # is order short or long
        return not self.is_long()

    def check_empty(self ,date_target , date_loss ):
        self._date_tp = date_target.index[0] if  not date_target.empty else False
        self._date_sl = date_loss.index[0] if not date_loss.empty  else False

    def date_finish_order(self):
        date_target =  self.data_low.loc[self.data_low.High >= self.tp]
        date_loss   =   self.data_low.loc[self.data_low.Low <= self.sl]
        self.check_empty(date_target ,date_loss )

    def _open_order(self ,type_order ,limit ,tp ,sl ):
        self._position = True
        self._type =type_order
        self.__order[["IdOrder" ,
                      "Type",
                      "DateStart" ,
                      "Enter" ,
                      "tp" ,
                      "sl"]] = [str(type_order)+str(len( self.result_orders)),
                                type_order,self.date_start_order,limit,tp,sl]

    def _close_order(self,goal:bool ,date : pd.Timestamp) -> None :
        self.__order[[ "Target","EndDate"]] = [goal,date]
        self.date_end_order = date
        self._position =False
        self.result_orders = pd.concat([self.result_orders,self.__order ] ,axis=0,ignore_index=True)