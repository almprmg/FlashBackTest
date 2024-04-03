
from BackTest_Smull import BestTestLow

class Strategy(BestTestLow):


    def buy(self, limit:float,tp: float,sl:float)-> None:
        if not self.is_position():
            self.limit =limit
            self.sl = sl
            self.tp =tp
            self._type =1
            self._open_order()
    def sell(self, limit:float,tp: float,sl:float):
        if not self.is_position():
            self.limit =limit
            self.sl = sl
            self.tp =tp
            self._type =2
            self._open_order()
    def next(self)-> None:...
    def init(self)-> None:...