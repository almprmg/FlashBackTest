
from order import Orders


class BestTestLow(Orders):

    def trade(self):
        self._process_order()
        if self._date_tp or self._date_sl :
            if self.is_unknown() :
                if self.is_win():
                    return
                self.is_loss()
    def is_unknown(self):
        if not self._date_tp  and self._date_sl :
            self._close_order(0,self._date_sl)
            return False
        elif self._date_tp == self._date_sl:
            self._close_order(0,self._date_sl)
            return False
        return True

    def is_win(self):
        if  self._date_tp and not self._date_sl :
            self._close_order(1 ,self._date_tp)
            return True
        elif self._date_tp < self._date_sl :
            self._close_order(1 ,self._date_tp)
            return True
        return False

    def is_loss(self):
        if  self._date_tp > self._date_sl:
            self._close_order(0 ,self._date_sl)
            return True
        return False