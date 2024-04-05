
from order import Orders


class BestTestLow(Orders):

    def trade(self):
        self._process_order()

        if self.is_position() and self.is_unknown() :
            if self.is_win():
                return
            self.is_loss()
    def is_unknown(self):
        is_unknown = self._date_tp == self._date_sl
        if is_unknown:
            return  not  self._close_order(0,self._date_sl)
        return True

    def is_win(self):
        is_done_tp = self._date_tp < self._date_sl
        if is_done_tp:
            return not self._close_order(1 ,self._date_tp)
        return False

    def is_loss(self):
        is_done_sl = self._date_tp > self._date_sl
        if  is_done_sl :
            return not self._close_order(0,self._date_sl)
        return False