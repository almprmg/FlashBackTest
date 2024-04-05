from dataclasses import dataclass, field
from pandas import DataFrame,Series
from pandas import Timestamp , to_datetime


class _unit:
    @staticmethod
    def swap(first,secund):
        return  secund ,first


class hlepper_data:
    def __init__(self ,
                 data: DataFrame ,
                 data_low: DataFrame ,
                 ) -> None:
        self.__data = data.copy()
        self.data_low = data_low #.loc[data_low.index >= self.date_start_order]
        self.data = data.head(1)
    def __update_data(self,index_end_order):
        self.__data = self.__data.loc[self.__data.index > index_end_order,:]

        if self.is_data_finsh():
            self.data   = self.__data.head(1)


    def is_data_finsh(self):
        return  len(self.__data) !=0
    def refresh_data_low(self,index_start_order):
        self.data_low = self.data_low.iloc[self.data_low.index >  index_start_order,:]

    def refresh_data(self,last_index):
        self.data = self.__data.loc[ : last_index,:]
    def update(self,index_end_order)-> None:

        self.__update_data(index_end_order)

@dataclass
class DataOrder:
    type_order: int =None
    position : bool = False
    date_starting: Timestamp = None
    #symbol: str
    #quantity: float = None
    price: float = None
    tp: float = None
    sl: float = None
    success: int = None
    date_end: Timestamp = None
    def get_order(self) -> list:
        """Function ."""
        return  [
                self.type_order ,
                self.date_starting ,
                self.price ,
                self.tp ,
                self.sl ,
                self.success ,
                self.date_end ,
                ]


@dataclass
class DataOrders:

    __orders: list = field(default_factory=list)

    def add_order(self, order : DataOrder ) -> None:
        self.__orders.append(order)
    def to_dataframe(self) -> DataFrame :
        return DataFrame([order.__dict__ for order in self.__orders])

class Orders(hlepper_data):
    def __init__(self,date_start_order,
                 data: DataFrame ,
                 data_low: DataFrame ,) -> None:
        super().__init__(data,data_low)
        self.data_orders = DataOrders()
        self.__order = DataOrder()
        self._type = None
        self._date_tp = None
        self._date_sl = None
        self.tp = None
        self.sl = None
        self.limit =None
        self._date_start_order = date_start_order
        self.date_end_order  =date_start_order


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

    def check_empty(self ,series_data):

        return False if series_data.empty else series_data.index[-1]

    def is_empty(self,date_target , date_loss ):
    
        self._date_tp = date_target.index[0] if self.check_empty(date_target) else self.check_empty(date_loss)
        self._date_sl = date_loss.index[0] if self.check_empty(date_loss)  else self.check_empty(date_target)
        return not (self._date_tp or self._date_sl)

    def date_finish_order(self):
        date_target =  self.data_low.loc[self.data_low.High >= self.tp]
        date_loss   =   self.data_low.loc[self.data_low.Low <= self.sl]
        if (self.is_empty(date_target ,date_loss )):
             self.__order.position = False



    def _open_order(self ):
        self.refresh_start_order()
        self.refresh_data_low(self._date_start_order)
        self.__new_order()



    def _close_order(self,goal:bool ,date_end : Timestamp) -> None :
        self.__finish_position(goal,date_end)
        self.refresh_end_order(date_end)
        self.update(date_end)
        return self.is_position()



    def refresh_end_order(self,index) -> None:

        self.date_end_order = index

    def refresh_start_order(self) -> None:

        self._date_start_order = self.data.index[-1]

    def get_alorder(self):

        return self.data_orders.to_dataframe()

    def is_position(self):

        return self.__order.position

    def __new_order(self):
        self.__order =  DataOrder(
                     type_order = self._type,
                     position = True,
                     date_starting = self._date_start_order,
                     price = self.limit ,
                     tp = self.tp,
                     sl = self.sl,
                     )
    def __finish_position(self,goal , date_end):
        self.__order.success  = goal
        self.__order.date_end = date_end
        self.__order.position = False
        self.data_orders.add_order(self.__order)


