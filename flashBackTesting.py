from numbers import Number
from abc import ABCMeta,abstractmethod
from dataclasses import dataclass, field
import numpy as np
from pandas import DataFrame
from pandas import RangeIndex
from pandas import to_datetime
from pandas import DatetimeIndex
from pandas import Timestamp
from Calculator import CalculatorProfit
from _util import is_empty,check_empty




class HelperData:
    def __init__(self ,
                 data: DataFrame ,
                 data_low: DataFrame ,
                 ) -> None:
        self.__data = data.copy()
        self._data_low = data_low.copy() #.loc[data_low.index >= self.date_start_order]
        self.data_low = data_low.copy()
        self.data = data.head(1)




    def update_data_low(self,index_start_order : Timestamp) -> None:
        """remove data OCHL after start time order opening start for start trade."""
        self.data_low = self._data_low.loc[ index_start_order : ,:]
    def is_data_next(self,exit_data):
        return self.data.index[-1] >=exit_data
    def update(self,index) :
        self.data = self.__data.loc[ :index,:]
        self.update_data_low(index)

    @property
    def last_date(self) -> None:
        """time start last order opened, for update data from it."""
        return self.data.index[-1]


@dataclass
class Order:
    type_position : int = field(default=None)
    enter_price : float = field(default=None)
    tp : float = field(default=None)
    sl : float = field(default=None)
    enter_time : Timestamp = field(default=None)

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
class OrderTrader:
    _order : Order
    position = True
    exit_time : Timestamp =field(default=None)
    success: int = field(default=None)


    @property
    def type_order(self):
        return self._order.type_position
    @property
    def enter_price(self):
        return self._order.enter_price
    @property
    def tp(self):
        return self._order.tp
    @property
    def sl(self):
        return self._order.sl
    @property
    def enter_time(self):
        return self._order.enter_time

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
    def info(self):
        return TradesClose(self.type_order,
                self.enter_price
                ,self.exit_price
                ,self.enter_time
                ,self.exit_time,
                self.pct,
                self.deferent)
    
    def close(self,success,exit_time) -> TradesClose:
        self.position =False
        self.success = success
        self.exit_time =  exit_time

    @property
    def is_long(self):
        "True if the type order is long (type order  is 1). "
        return self.type_order == 1
    @property
    def is_short(self):
        "True if the type order is short ( not type order  is long). "
        return not self.is_long

class Trade:
    """when is order opened ,is start back taste """
    def __init__(self,helper_data,max_order) -> None:
        self.helper_data :HelperData = helper_data
        self.order_trade : list[OrderTrader] = []
        self.trades_closed : list[TradesClose] = []
        self.__max_orders: int = max_order
    def new_order(self,type_position,limit,sl,tp) -> None:
        """appending order"""
        if len( self.order_trade) <= self.__max_orders:
            order = Order(
                    type_position = type_position,
                    enter_price= limit ,
                    tp = tp,
                    sl = sl,
                    enter_time = self.helper_data.last_date,
                    )
            self._open_order(order)

    def _open_order(self , order: Order ):
        order_open = OrderTrader(order)
        self.order_trade.append(order_open)
    def _close_order(self , order: Order ):
            self.trades_closed.append(order.info)
            self.order_trade.remove(order)

    def trade_order(self,order) -> tuple[int | None ,Timestamp | None]:
        """get first date time tp and sl for know ho came first one """
        date_target , date_loss = self.long_order(order) if order.is_long else self.short_order(order)
        date_tp = date_target.index[0] if check_empty(date_target) else  check_empty(date_loss)
        date_sl = date_loss.index[0] if check_empty(date_loss)  else  check_empty(date_target)

        return self.date_finish_order(date_tp ,date_sl)

    def is_win(self,date_tp,date_sl) -> bool:
        """condition mean tp came before sl thats mean win  """
        return date_tp < date_sl
    def is_loss(self,date_tp,date_sl) -> bool:
        """ condition mean  sl came before  thats mean loss  """
        return not self.is_win(date_tp,date_sl)

    def date_finish_order(self,date_tp,date_sl)-> list:
        """Return datetime and order win or not"""

        if (is_empty(date_tp,date_sl)) :
            return [1,date_tp] if self.is_win(date_tp,date_sl) else [0,date_sl]
        return [None,None]

    def long_order(self ,order: OrderTrader) -> tuple:
        """Return all datetime fulfill the condition"""
        data_low = self.helper_data.data_low
        date_target =  data_low.loc[data_low.High >= order.tp]
        date_loss   =  data_low.loc[data_low.Low <= order.sl]
        return date_target , date_loss
    def short_order(self,order: OrderTrader) -> tuple:
        """Return all datetime fulfill the condition"""
        data_low = self.helper_data.data_low
        date_target =  data_low.loc[data_low.Low <= order.tp]
        date_loss   =   data_low.loc[data_low.High >= order.sl]
        return date_target , date_loss
    def start_trading(self) -> None:
        """start finding result order """

        for order in self.order_trade:
            if order.position:
                succuss ,date_end = self.trade_order(order)
                if date_end is not None :
                    order.close(succuss ,date_end)
            else :
                if self.helper_data.is_data_next(order.exit_time):
                    self._close_order(order)






class Strategy(metaclass=ABCMeta):
    """
    This code and  comment is inspired by the backtesting library: [https://github.com/kernc/backtesting.py.git]
    A trading strategy base class. Extend this class and
    override methods
    `FlashBackTesting.FlashBackTesting.Strategy.init` and
    `FlashBackTesting.FlashBackTesting.Strategy.next` to define
    your own strategy.
    """

    def __init__(self,trade,helper_data) -> None:
       self.trade : Trade = trade
       self._helper_data : HelperData = helper_data


    def buy(self, limit:float,tp: float,sl:float)-> None:
        """
        Place a new long order. For explanation of parameters, see `Order` and its properties.

        See also `Strategy.sell()`.
        """
        if tp <sl:
            raise TypeError("Error :buy tp < sl")
        self.trade.new_order(1,limit,sl,tp)
    def sell(self, limit:float,tp: float,sl:float) -> None:
        """
        Place a new short order. For explanation of parameters, see `Order` and its properties.

        See also `Strategy.buy()`.
        """
        if tp > sl:
            raise TypeError("Error :sell tp > sl")
        self.trade.new_order(2,limit,sl,tp)
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
    @property
    def data(self):
        return self._helper_data.data

    @property
    def position(self):
        """Argument of `flashbacktesting.flashbacktesting.flashbacktesting.Trade`."""
        return len(self.trade.order_trade) > 0
    @property
    def trades(self):
        return self.trade.order_trade

    @property
    def get_trade(self):
        return DataFrame([order.__dict__ for order in self.trade.trades_closed])

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
        if ratio_entry > 100:
            raise ValueError("ValueError : ratio_entry >  100 should to be <= 100  ")
        self.__index =  data.index
        max_order = cash // ((ratio_entry*0.01) * cash)
        helper_data = HelperData(data=data.copy(deep= False),
                                 data_low=data_small.copy(deep= False))
        self._helper_data = helper_data
        self._trade =Trade(helper_data, max_order)
        self.strategy = strategy(self._trade,helper_data,)
        self.calculator_traded = CalculatorProfit(cash, ratio_entry, fees, cp,data)
        self.result : DataFrame




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

        for index in self.__index:
            self.strategy.next()
            self._helper_data.update(index)
            if self.strategy.position:
                self.strategy.trade.start_trading()

        self.result = self.calculator_traded.result(self.strategy.get_trade)
        return self.result
