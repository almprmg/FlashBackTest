from numbers import Number
from abc import ABCMeta,abstractmethod
from dataclasses import dataclass, field
import numpy as np
from pandas import DataFrame
from pandas import RangeIndex
from pandas import to_datetime
from pandas import DatetimeIndex
from pandas import Timestamp
from Calculator import CalcutatorProfit
from _util import is_empty,check_empty




class hlepper_data:
    def __init__(self ,
                 data: DataFrame ,
                 data_low: DataFrame ,
                 ) -> None:
        self.__data = data.copy()
        self.data_low = data_low #.loc[data_low.index >= self.date_start_order]
        self.data = data.head(1)

    @property
    def is_data_finish(self) -> bool:
        """True if the data is length = 0 """
        return  len(self.__data) !=0

    def __update_data(self,index_end_order : Timestamp ) -> None:
        """ update data OCHL from last order closed to end data."""
        self.__data = self.__data.loc[self.__data.index > index_end_order,:]
        self.data_dump()

    def data_dump(self) -> None :
        if self.is_data_finish:
            self.data   = self.__data.head(1)
    def refresh_data_low(self,index_start_order : Timestamp) -> None:
        """remove data OCHL after start time order opening start for start trade."""
        self.data_low = self.data_low.iloc[self.data_low.index >  index_start_order,:]

    def refresh_data(self,last_index)-> None:
        """append last row to data trade."""
        self.data = self.__data.loc[ : last_index,:]

    def update(self,index_end_order)-> None:
        self.__update_data(index_end_order)
@dataclass
class TradesClose:

    type_position : int = 0
    enter_price   : float = field(default=None)
    exit_price   : float = field(default=None)
    enter_time    : Timestamp = field(default=None)
    exit_time     : Timestamp = field(default=None)
    pct : float = field(default=None)
    deferent : float = field(default=None)

@dataclass
class OrderInfo:
    type_order: int = 0
    position : bool = False
    enter_price: float = field(default=None)
    tp: float = field(default=None)
    sl: float = field(default=None)
    success: int = field(default=None)
    enter_time: Timestamp = field(default=None)
    exit_time: Timestamp = field(default=None)


    @property
    def exit_price(self):
        return self.tp if self.success == 1 else self.sl
    @property
    def deferent(self):
        return (self.exit_price - self.enter_price) if self.type_order ==1 else (self.enter_price - self.exit_price)
    @property
    def pct(self):
        return (self.exit_price -self.enter_price)/ self.enter_price if self.type_order ==1 else -(self.exit_price -self.enter_price)/ self.enter_price
    @property
    def close_order(self) -> TradesClose:
        return TradesClose(self.type_order,
                self.enter_price
                ,self.exit_price
                ,self.enter_time
                ,self.exit_time,
                self.pct,
                self.deferent)


@dataclass
class ClosedOrders:

    __orders: list[TradesClose] = field(default_factory=list)

    def append_(self, crades_close : OrderInfo ) -> None:
        """add info order closed to list orders."""
        self.__orders.append(crades_close.close_order)
    @property
    def get_orders(self) -> DataFrame :
        return DataFrame([order.__dict__ for order in self.__orders])




class Orders(hlepper_data):
    def __init__(self,date_start_order,
                 data: DataFrame ,
                 data_low: DataFrame ,) -> None:
        super().__init__(data,data_low)
        self.data_orders = ClosedOrders()
        self.__order = OrderInfo()
        self.tp = None
        self.sl = None
        self.limit =None
        self._date_start_order = date_start_order
        self.date_end_order  =date_start_order

    @property
    def is_long(self):
        "True if the type order is long (type order  is 1). "
        return self.__order.type_order == 1
    @property
    def is_short(self):
        "True if the type order is short ( not type order  is long). "
        return not self.is_long


    @property
    def get_alorder(self) ->DataFrame:
        """Dataframe of orders (see orders) withing empty data """
        return self.data_orders.get_orders
    @property
    def is_position(self) -> bool:
        """Instance of `backtesting.strategy.Position`."""
        return self.__order.position
    def refresh_end_order(self,index) -> None:
        """time end last order close for update data from it"""
        self.date_end_order = index

    def refresh_start_order(self) -> None:
        """time start last order opened, for update data from it."""
        self._date_start_order = self.data.index[-1]

    def __new_order(self,type_order) -> None:
        self.__order =  OrderInfo(
                     type_order = type_order,
                     position = True,
                     enter_time = self._date_start_order,
                     enter_price = self.limit ,
                     tp = self.tp,
                     sl = self.sl,
                     )
    def __finish_position(self,goal :int , date_end:Timestamp) -> None :
        self.__order.success  = goal
        self.__order.exit_time = date_end
        self.__order.position = False
        self.data_orders.append_(self.__order)

    def _open_order(self,type_order ):
        self.refresh_start_order()
        self.refresh_data_low(self._date_start_order)
        self.__new_order(type_order)


    def _close_order(self,goal:bool ,date_end : Timestamp) -> None :
        self.__finish_position(goal,date_end)
        self.refresh_end_order(date_end)
        self.update(date_end)
        return self.is_position




class Trade(Orders):
    """when is order opened ,is start back taste """
    def trade(self) -> None:
        """start finding result order"""
        if self.is_position:
            gols ,date_end = self.date_finish_order()
            self._close_order(gols ,date_end )
    def trade_order(self) -> tuple:
        date_target , date_loss = self.long_order() if self.is_long else self.short_order()
        date_tp = date_target.index[0] if check_empty(date_target) else check_empty(date_loss)
        date_sl = date_loss.index[0] if check_empty(date_loss)  else check_empty(date_target)
        return date_tp ,date_sl

    def is_win(self,date_tp,date_sl) -> bool:
        return date_tp < date_sl
    def is_loss(self,date_tp,date_sl) -> bool:
        return not self.is_win(date_tp,date_sl)

    def date_finish_order(self)-> list:
        date_tp,date_sl = self.trade_order()
        if (is_empty(date_tp,date_sl)) :
            return [1,date_tp] if self.is_win(date_tp,date_sl) else [0,date_sl]
        return [None,None]
    def long_order(self) -> tuple:
        date_target =  self.data_low.loc[self.data_low.High >= self.tp]
        date_loss   =   self.data_low.loc[self.data_low.Low <= self.sl]
        return date_target , date_loss
    def short_order(self) -> tuple:
        date_target =  self.data_low.loc[self.data_low.Low <= self.tp]
        date_loss   =   self.data_low.loc[self.data_low.High >= self.sl]
        return date_target , date_loss




class Strategy(Trade,metaclass=ABCMeta):
    """
    This code and  comment is inspired by the backtesting library: [https://github.com/kernc/backtesting.py.git]
    A trading strategy base class. Extend this class and
    override methods
    `FlashBackTesting.FlashBackTesting.Strategy.init` and
    `FlashBackTesting.FlashBackTesting.Strategy.next` to define
    your own strategy.
    """

    def buy(self, limit:float,tp: float,sl:float)-> None:
        """
        Place a new long order. For explanation of parameters, see `Order` and its properties.

        See also `Strategy.sell()`.
        """
        if not self.is_position:
            self.limit =limit
            self.sl = sl
            self.tp =tp
            self._open_order(1)
    def sell(self, limit:float,tp: float,sl:float) -> None:
        """
        Place a new short order. For explanation of parameters, see `Order` and its properties.

        See also `Strategy.buy()`.
        """
        if not self.is_position:
            self.limit =limit
            self.sl = sl
            self.tp =tp
            self._open_order(2)
    @abstractmethod
    def next(self)-> None:
        """
        Initialize the strategy.
        Override this method.
        Declare indicators (with `FlashBackTesting.FlashBackTesting.Strategy.I`).
        Precompute what needs to be precomputed or can be precomputed
        in a vectorized fashion before the strategy starts.

        If you extend composable strategies from `FlashBackTesting.lib`,
        make sure to call:

            super().init()
        """
    @abstractmethod
    def init(self)-> None:
        """ 
        Main strategy runtime method, called as each new
        `FlashBackTesting.FlashBackTesting.Strategy.data`
        instance (row; full candlestick bar) becomes available.
        This is the main method where strategy decisions
        upon data precomputed in `FlashBackTesting.FlashBackTesting.Strategy.init`
        take place.

        If you extend composable strategies from `FlashBackTesting.lib`,
        make sure to call:

            super().next()
        """
class  FlashBackTesting:
    """"
    This code and comment  is inspired by the backtesting library: [https://github.com/kernc/backtesting.py.git]
    
    FlashBackTesting a particular (parameterized) strategy
    on particular data.

    Upon initialization, call method
    `FlashBackTesting.FlashBackTesting.BackTest.run` to run a backtest
    instance
    """
    def __init__(self,
                 data: DataFrame ,
                 data_small: DataFrame ,
                 strategy:type[Strategy] ,
                 cash: int = 1000 ,
                 ratio_entry:int = 1000 ,
                 fees: float = 0.001 ,
                 cp: bool = False ) -> None:

        if not (isinstance(strategy, type) and issubclass(strategy, Strategy)):
            raise TypeError('`strategy` must be a Strategy sub-type')
        if not isinstance(data, DataFrame):
            raise TypeError("`data` must be a pandas.DataFrame with columns")
        if not isinstance(data_small, DataFrame):
            raise TypeError("`data` must be a pandas.DataFrame with columns")
        if not isinstance(cash, Number):
            raise TypeError('`Cash` must be a float value, percent of '
                            'entry order price')
        data = data.copy(deep=False)

        # Convert index to datetime index
        if (not isinstance(data.index, DatetimeIndex) and
            not isinstance(data.index, RangeIndex) and
            # Numeric index with most large numbers
            (data.index.is_numeric() and
             (data.index > Timestamp('1975').timestamp()).mean() > .8)):
            try:
                data.index = to_datetime(data.index, infer_datetime_format=True)
            except ValueError:
                pass

        if 'Volume' not in data:
            data['Volume'] = np.nan

        if len(data) == 0:
            raise ValueError('OHLC `data` is empty')
        if len(data.columns.intersection({'Open', 'High', 'Low', 'Close', 'Volume'})) != 5:
            raise ValueError("`data` must be a pandas.DataFrame with columns "
                             "'Open', 'High', 'Low', 'Close', and (optionally) 'Volume'")
        if data[['Open', 'High', 'Low', 'Close']].isnull().values.any():
            raise ValueError('Some OHLC values are missing (NaN). '
                             'Please strip those lines with `df.dropna()` or '
                             'fill them in with `df.interpolate()` or whatever.')
        self.__ishave_signal =  "Signal" in data.columns
        self.result : DataFrame
        self.calculator_traded = CalcutatorProfit(cash, ratio_entry, fees, cp)
        self.__data = data.copy(deep=False)
        if self.__ishave_signal:
            data = data.loc[data.Signal != 0]
            date = data.index[0]
        else:
            date = data.index[1]
            self.__index = data.index

        self.strategy = strategy(date ,data ,data_small)

    def run(self) -> None:

        """
        Run the backtest. Returns `pd.Series` with results and statistics.
        
        Keyword arguments are interpreted as strategy parameters.

            >>> Backtest(AGLDUSDT,AGLDUSDT_Low_frame, Rsi).run()
            Start                    2022-08-26 18:00:00
            End                      2023-08-26 17:00:00
            Duration                   364 days 23:00:00
            Equity Final [$]                  782.198334
            Equity Peak [$]                  1013.011602
            Return [%]                        -22.463471
            Buy & Hold Return [%]              38.636364
            Max. Drawdown [%]                 -25.033789
            # Trades                                  71
            Win Rate [%]                       50.704225
            Best Trade [%]                     15.873016
            Worst Trade [%]                   -27.142857
            Avg. Trade [%]                     -2.049075
            Max. Trade Duration         27 days 17:00:00
            Avg. Trade Duration          2 days 03:00:00
            Profit Factor                       0.624392
            Expectancy [%]                     -1.647243
            SQN                                -1.609426
            _trades                            Size  ...
            dtype: obj
        """
        if self.__ishave_signal:

            while self.strategy.is_data_finish:
                self.strategy.next()
                self.strategy.trade()
        else:
            for index in  self.__index :
                if index > self.strategy.date_end_order and self.strategy.is_data_finish:
                    self.strategy.refresh_data(index)
                    self.strategy.next()
                    if self.strategy.is_position:
                        self.strategy.trade()
        self.result = self.calculator_traded.finaly_result(self.strategy.get_alorder,self.__data)
        return self.result