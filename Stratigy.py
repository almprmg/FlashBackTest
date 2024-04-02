
from BackTest_Smull import BestTestLow

class Strategy(BestTestLow):


    def buy(self, limit:float,tp: float,sl:float)-> None:
        if not self._position:
            self.limit =limit
            self._open_order(1,limit,tp,sl)
    def sell(self, limit:float,tp: float,sl:float):
        if not self._position:
            self.sl = sl
            self.tp =tp
            self.limit =limit
            self._position = True
            self._open_order(2,limit,tp,sl)
    def next(self)-> None:...
    def init(self)-> None:...