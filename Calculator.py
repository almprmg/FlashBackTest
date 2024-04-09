from abc import ABCMeta ,abstractmethod
import pandas as pd
from dataclasses import dataclass,field
from _util import adding_threezero
@dataclass
class Wallet:

    cash : int =  field(default_factory= int)
    ratio_entry : int = field(default_factory= int)
    rate_fees : float = field(default_factory= float)
    amount : int = field(default_factory= int)
    def __post_init__(self):
        self.cash = adding_threezero(self.cash)


    def init_cash(self):
        retail = 100 / self.ratio_entry
        self.amount = self.cash /  retail

    def fees(self,row) ->int:

        return int(abs(row * self.rate_fees))
class InitDataTraded():
    @staticmethod
    def different(func) -> pd.DataFrame :
        """_summary_

        Args:
            func (_type_): _description_z

        Returns:
            pd.DataFrame: _description_
        """
        def fuc_wrapper(self,result):
            result['different'] =  result['PriceEndOrder'] - result['price'] if result['type_order'] == 1 else  result['price'] - result['PriceEndOrder']
            result = func(self,result)
            return result
        return fuc_wrapper

    @staticmethod
    def quantity_symbol(func) -> pd.DataFrame:
        def fuc_wrapper(self,result):
            self.wallet.init_cash()
            result['FeesOpen'] = self.wallet.fees(self.wallet.amount)
            result['Quantity'] =  self.wallet.amount / result['price']
            return  func(self,result)
        return fuc_wrapper
    @staticmethod

    def profit_trade(func)-> pd.DataFrame:

        def fuc_wrapper(self,result):
            result['ProfitTrade'] = int(result['Quantity'] * result['different'])
            result['FeesClose'] =   self.wallet.fees(result['ProfitTrade'] + self.wallet.amount)
            result['ProfitTrade']= result['ProfitTrade'] - result['FeesClose']
            return func(self,result)
        return fuc_wrapper
    @staticmethod
    def price_end(result: pd.DataFrame =None ) -> list:
        return [row["tp"] if row['success'] != 0 else row["sl"] for _,row in result.iterrows()]

class CalcutatorPofit(metaclass=ABCMeta):
    def __init__(self, cash, ratio_entry, fees) -> None:
        self.wallet = Wallet( cash, ratio_entry, fees)

    @abstractmethod
    def howto_win(self,result)-> None:
        """_summary_.
        """
    @abstractmethod
    def profit(self,result)-> None:
        """profit.

        """
    def fixed(self,result):
        result["CumProfit"] /=1000
        result["FeesClose"] /=1000
        result["FeesOpen"] /=1000
        result["ProfitTrade"] /=1000
        result["Quantity"] /=1000
        return result

class UnCumulativeTradeProfit(CalcutatorPofit):


    @InitDataTraded.different
    @InitDataTraded.quantity_symbol
    @InitDataTraded.profit_trade
    def howto_win(self,result:pd.DataFrame) -> pd.DataFrame:

        result['CumProfit'] = result['ProfitTrade'].cumsum() +  self.wallet.cash
        ep_result = result[["price","PriceEndOrder"]]
        result['PctProfit'] = ep_result.pct_change(axis="columns",periods=1)["PriceEndOrder"] * 100
        return result
    def profit(self,result: pd.DataFrame) -> pd.DataFrame:
        """_summary_
        """
        result['PriceEndOrder'] = InitDataTraded.price_end(result)
        return self.fixed(self.howto_win(result))

class CumulativeTradeProfit(CalcutatorPofit):
    """There is no need to override 'price_end' it has the same
        signature as the implementation in CalculatorProfit.
    """
    InitData =InitDataTraded
    @InitData.different
    @InitData.quantity_symbol
    @InitData.profit_trade
    def howto_win(self ,result:pd.DataFrame) -> pd.DataFrame:
        self.wallet.cash += result['ProfitTrade']
        result['CumProfit'] = self.wallet.cash
        ep_result = result[["price" ,"PriceEndOrder"]]
        result['PctProfit'] = ep_result.pct_change(periods=1)["PriceEndOrder"]*100
        return  result

    def profit(self ,result : pd.DataFrame)-> pd.DataFrame:
        """_summary_

        Args:
            result (_type_): _description_

        Returns:
            pd.DataFrame: _description_
        """
        result['PriceEndOrder'] = InitDataTraded.price_end(result)
        return  self.fixed(result.apply(self.howto_win ,axis = 1 ))