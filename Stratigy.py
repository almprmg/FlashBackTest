
from abc import ABCMeta,abstractmethod
from BackTest_Smull import BestTestLow

class Strategy(BestTestLow,metaclass=ABCMeta):
    """
    A trading strategy base class. Extend this class and
    override methods
    `fastbacktesting.fastbacktesting.Strategy.init` and
    `fastbacktesting.fastbacktesting.Strategy.next` to define
    your own strategy.
    """

    def buy(self, limit:float,tp: float,sl:float)-> None:
        """
        Place a new long order. For explanation of parameters, see `Order` and its properties.

        See also `Strategy.sell()`.
        """
        if not self.is_position():
            self.limit =limit
            self.sl = sl
            self.tp =tp
            self._type =1
            self._open_order()
    def sell(self, limit:float,tp: float,sl:float):
        """
        Place a new short order. For explanation of parameters, see `Order` and its properties.

        See also `Strategy.buy()`.
        """
        if not self.is_position():
            self.limit =limit
            self.sl = sl
            self.tp =tp
            self._type =2
            self._open_order()
    @abstractmethod
    def next(self)-> None:
        """
        Initialize the strategy.
        Override this method.
        Declare indicators (with `fastbacktesting.fastbacktesting.Strategy.I`).
        Precompute what needs to be precomputed or can be precomputed
        in a vectorized fashion before the strategy starts.

        If you extend composable strategies from `fastbacktesting.lib`,
        make sure to call:

            super().init()
        """
    @abstractmethod
    def init(self)-> None:
        """ 
        Main strategy runtime method, called as each new
        `fastbacktesting.fastbacktesting.Strategy.data`
        instance (row; full candlestick bar) becomes available.
        This is the main method where strategy decisions
        upon data precomputed in `fastbacktesting.fastbacktesting.Strategy.init`
        take place.

        If you extend composable strategies from `fastbacktesting.lib`,
        make sure to call:

            super().next()
        """