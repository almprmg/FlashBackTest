
from Order import orders


class Best_Test_small(orders):
    _position = False
   
    def __init__(self) -> None:
        super().__init__()


    
    def trade(self):
        self._process_order()

        if self._date_tp != None and self._date_sl != None  :
            if (self._date_tp < self._date_sl and self._type == 1) :
                self._close_order(1,self._date_tp)  
            elif (self._date_tp < self._date_sl):
                 self._close_order(2,self._date_tp)
            elif (self._date_tp > self._date_sl and self._type == 1) :
                self._close_order(0,self._date_sl)
            elif (self._date_tp > self._date_sl and self._type == 2): 
                self._close_order(0,self._date_sl)
        elif  self._date_tp == None and self._date_sl != None :
            if self._type:
                self._close_order(0,self._date_sl)
            else : 
                self._close_order(0,self._date_sl)
        elif self._date_tp != None and self._date_sl == None :
            if self._type:
                self._close_order(1,self._date_tp)
            else : 
                self._close_order(2,self._date_tp)

    



     
