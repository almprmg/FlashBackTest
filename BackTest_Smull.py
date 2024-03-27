
from order import orders


class Best_Test_small(orders):
    _position = False
   
    def __init__(self) -> None:
        super().__init__()


    
    def trade(self):
        self._process_order()
        self._date_tp != None or self._date_sl != None
        if self._date_tp != None or self._date_sl != None:
            if self.is_unknown() :
                    if self.is_win():
                            return 
                    self.is_loss()
                



    def is_unknown(self):
        if self._date_tp == None and self._date_sl != None  :
            self._close_order(0,self._date_sl)
            return False
        elif self._date_tp == self._date_sl:
            self._close_order(0,self._date_sl)
            return False
        return True

    def is_win(self):
            if  self._date_tp != None and self._date_sl == None:
                self._close_order(1,self._date_tp)
                return True
            elif self._date_tp < self._date_sl :
                self._close_order(1,self._date_tp)
                return True
            return False
            

    def is_loss(self):
        if  self._date_tp > self._date_sl:
            self._close_order(0,self._date_sl) # mean 0 close order loss 
            return True
        return False
        

    



     
