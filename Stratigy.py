
from abc import ABCMeta,abstractmethod
from BackTest_Smull import Trade

class Strategy(Trade,metaclass=ABCMeta):
    """
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
        if not self.is_position():
            self.limit =limit
            self.sl = sl
            self.tp =tp
            self._open_order(1)
    def sell(self, limit:float,tp: float,sl:float):
        """
        Place a new short order. For explanation of parameters, see `Order` and its properties.

        See also `Strategy.buy()`.
        """
        if not self.is_position():
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