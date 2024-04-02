from BackTest_Smull import BestTestLow

class Strategy(BestTestLow):

    def update(self,)-> None:

        self.__update_data(self.data)
        self.data = self.data.loc[self.data.Signal != 0]
        index_start_new_order = self.data.index[0]
        if self.is_data_finsh() :
            self.refresh_start_order(index_start_new_order)
            self.refresh_data_low(index_start_new_order)
    def update_no_signall(self,data)-> None:

        self.__update_data(data)
        if self.is_data_finsh() :
            self.refresh_data_low(self.date_end_order)

    def __update_data(self,data):
       self.data  = data.loc[data.index > self.date_end_order,:]

    def is_data_finsh(self):
        return self.date_end_order != self.data_low.index[-1] and len(self.data) !=0

    def refresh_data_low(self,index):
        self.data_low = self.data_low.iloc[self.data_low.index >  index,:]

    def refresh_data(self,data,index):
        self.data = data.loc[ : index,:]

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