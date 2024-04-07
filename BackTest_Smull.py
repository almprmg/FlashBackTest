
from order import Orders, _unit


class Trade(Orders):

    def trading(self):
        if self.is_position():
            gols ,date_end = self.date_finish_order()
            self._close_order(gols ,date_end )
    def trade_order(self):
        date_target =  self.data_low.loc[self.data_low.High >= self.tp]
        date_loss   =   self.data_low.loc[self.data_low.Low <= self.sl]
        date_tp = date_target.index[0] if self.check_empty(date_target) else self.check_empty(date_loss)
        date_sl = date_loss.index[0] if self.check_empty(date_loss)  else self.check_empty(date_target)
        return date_tp ,date_sl

    def is_win(self,date_tp,date_sl):
        return date_tp < date_sl
    def is_loss(self,date_tp,date_sl):
        return not self.is_win(date_tp,date_sl)

    def date_finish_order(self):
        date_tp,date_sl = self.long_order() if self.is_long() else self.short_order()
        if (self.is_empty(date_tp,date_sl)) :
            return [1,date_tp] if self.is_win(date_tp,date_sl) else [0,date_sl]
        return [None,None]
    def long_order(self):
        return self.trade_order()
    def short_order(self):
        self.tp,self.sl= _unit.swap(self.tp,self.sl)
        date_tp,date_sl= self.trade_order()
        return _unit.swap(date_tp,date_sl)

