
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
        retail = 100 / self.ratio_entry
        return self.cash /  retail




class CalcutatorPofit():
    def __init__(self, cash, ratio_entry, rate_fees,cp) -> None:
        self.wallet = Wallet( cash, ratio_entry)
        self.rate_fees : float = rate_fees
        self.__cp = cp
    def fees(self,amount:int | pd.Series) -> int | pd.Series:
        return self.rate_fees * amount

    def quantity(self,enter_price :float | pd.Series) -> float | pd.Series:
        return self.wallet.amount / enter_price

    def pnl(self,pct_cheng: float | pd.Series) -> float | pd.Series :
        return self.wallet.amount * pct_cheng

    def fixed_result(self,result:pd.DataFrame):
        result["CumProfit"] -= (result["FeesClose"] + result["FeesOpen"])
        result.drop(columns=["FeesClose","FeesOpen"],inplace=True)
        result["CumProfit"] /=1000
        result["PnL"] /=1000
        result["Quantity"] /=1000
        return result
    def unCumulative(self,result:pd.DataFrame) -> pd.DataFrame:
        result["FeesOpen"] = self.fees(self.wallet.amount)
        result["Quantity"] = self.quantity( result.enter_price)
        result['PnL'] = self.pnl(result['pct'])
        result['FeesClose'] = self.fees(result['PnL']+self.wallet.amount)
        result['CumProfit'] = result['PnL'].cumsum() + self.wallet.cash
        return result

    def cumulative(self ,result:pd.DataFrame) -> pd.DataFrame:
        """There is no need to override 'price_end' it has the same
            signature as the implementation in CalculatorProfit.
        """
        result["FeesOpen"] = self.fees(self.wallet.amount)
        result["Quantity"] = self.quantity( result.enter_price)
        result['PnL'] = self.pnl(result['pct'])
        result['FeesClose'] = self.fees(result['PnL']+self.wallet.amount)
        self.wallet.cash += result['PnL']
        result['CumProfit'] = self.wallet.cash
        return result

    def profit(self,trade:pd.DataFrame)-> pd.DataFrame:
        trade =  trade.apply(self.cumulative ,axis = 1) if  self.__cp else (self.unCumulative(trade))
        return self.fixed_result(trade)
    def finaly_result(self,result_trade,ohlc_data):

        return compute_stats(self.profit(result_trade),ohlc_data)



