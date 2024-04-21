
import pandas as pd
from dataclasses import dataclass,field
from _util import adding_threezero
from _stats import compute_stats
@dataclass
class Wallet:

    cash : int =  field(default_factory= int)
    ratio_entry : int = field(default_factory= int)


    def __post_init__(self):
        self.cash = adding_threezero(self.cash)

    @property
    def amount(self):
        """amount cash a open order."""
        retail = 100 / self.ratio_entry
        return self.cash /  retail

class CalculatorProfit:
    """Calculator profit trade of ech order."""
    def __init__(self, cash, ratio_entry, rate_fees,cp,data_ohlc) -> None:
        self.wallet = Wallet( cash, ratio_entry)
        self.rate_fees : float = rate_fees
        self.__cp = cp
        self.__data_ohlc = data_ohlc
    def fees(self,amount:int | pd.Series) -> int | pd.Series:
        """fess trade open,close."""
        return self.rate_fees * amount

    def quantity(self,enter_price :float | pd.Series) -> float | pd.Series:
        """Size symbol of order."""
        return self.wallet.amount / enter_price

    def pnl(self,pct_cheng: float | pd.Series) -> float | pd.Series :
        """Return PnL cash."""
        return self.wallet.amount * pct_cheng

    def fixed_result(self,orders:pd.DataFrame):
        orders["CumProfit"] -= (orders["FeesClose"] + orders["FeesOpen"])
        orders.drop(columns=["FeesClose","FeesOpen"],inplace=True)
        orders["CumProfit"] /=1000
        orders["PnL"] /=1000
        orders["Quantity"] /=1000
        return orders
    def uncumulative(self,orders:pd.DataFrame) -> pd.DataFrame:
        """There is no need to override 'price_end' it has the same
            signature as the implementation in UnCalculatorProfit.
        """
        orders["FeesOpen"] = self.fees(self.wallet.amount)
        orders["Quantity"] = self.quantity( orders.enter_price)
        orders['PnL'] = self.pnl(orders['pct'])
        orders['FeesClose'] = self.fees(orders['PnL']+self.wallet.amount)
        orders['CumProfit'] = orders['PnL'].cumsum() + self.wallet.cash
        return orders

    def cumulative(self ,order:pd.DataFrame) -> pd.DataFrame:
        """There is no need to override 'price_end' it has the same
            signature as the implementation in CalculatorProfit.
        """
        order["FeesOpen"] = self.fees(self.wallet.amount)
        order["Quantity"] = self.quantity( order.enter_price)
        order['PnL'] = self.pnl(order['pct'])
        order['FeesClose'] = self.fees(order['PnL']+self.wallet.amount)
        self.wallet.cash += order['PnL']
        order['CumProfit'] = self.wallet.cash
        return order

    def profit(self,trade:pd.DataFrame)-> pd.DataFrame:
        trade =  trade.apply(self.cumulative ,axis = 1) if  self.__cp else (self.uncumulative(trade))
        return self.fixed_result(trade)
    def result(self,result_trade):

        return compute_stats(self.profit(result_trade),
                             self.__data_ohlc)



