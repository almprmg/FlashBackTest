from BackTest_Smull import BestTestLow

class Strategy(BestTestLow):

    def update(self)-> None:

        self.data = self.data.iloc[self.data.index >  self.date_end_order,:]
        self.data
        data = self.data.loc[self.data.Signal != 0]
        if self.date_end_order != self.data_low.index[-1] and len(data) !=0 :
            self.date_start_order =data.index[0]
            self.data_low = self.data_low.iloc[self.data_low.index >=  self.date_start_order,:]
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