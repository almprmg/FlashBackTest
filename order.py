from dataclasses import dataclass, field
import pandas as pd

class _unit:
    @staticmethod
    def swap(first,secund):
        return  secund ,first
@dataclass
class DataOrder:
    id: int = None
    type_: int =None
    date_starting: pd.Timestamp = None
    #symbol: str
    #quantity: float = None
    price: float = None
    tp: float = None
    sl: float = None
    success: int = None
    date_end: pd.Timestamp = None
    def get_order(self) -> list:
        """Function ."""
        return  [self.id ,
                self.type_ ,
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
    def lenorders(self)-> int:
        return len(self.__orders)
    def add_orders(self, order : DataOrder ) -> None:
        self.__orders.append(order)
    def to_dataframe(self) -> pd.DataFrame :
        return pd.DataFrame([t.__dict__ for t in self.__orders])

class Orders:
    def __init__(self,date_start_order,data,data_low) -> None:
        self.data_orders = DataOrders()

        self.__order : DataOrder
        self._type = None
        self._date_tp = None
        self._date_sl = None
        self.tp = None
        self.sl = None
        self.limit =None
        self.date_start_order = date_start_order
        self.date_end_order   = None
        self._position =False
        self.data_low = data_low.loc[data_low.index >= self.date_start_order]
        self.data = data



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

    def check_empty(self ,date_target , date_loss ):
        self._date_tp = date_target.index[0] if  not date_target.empty else False
        self._date_sl = date_loss.index[0] if not date_loss.empty  else False

    def date_finish_order(self):
        date_target =  self.data_low.loc[self.data_low.High >= self.tp]
        date_loss   =   self.data_low.loc[self.data_low.Low <= self.sl]
        self.check_empty(date_target ,date_loss )

    def _open_order(self ,type_order ,limit ,tp ,sl ):
        self._position = True
        self._type =type_order
        self.__order =  DataOrder(str(type_order)+str( self.data_orders.lenorders()),
                     type_order,
                     self.date_start_order,limit
                     ,tp,
                     sl,)

    def _close_order(self,goal:bool ,date_end : pd.Timestamp) -> None :
        self.__order.success,self.__order.date_end = goal , date_end
        self.date_end_order = date_end
        self._position =False
        self.data_orders.add_orders( self.__order)
    def get_result(self):
        return self.data_orders.to_dataframe()
