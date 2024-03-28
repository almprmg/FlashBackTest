from abc import ABCMeta ,abstractmethod
import pandas as pd

class Money:
    """_summary_
    """
    def __init__(self,cash,ratio_entry ,fees ) -> None:
        self.cash =  cash
        self.amount : float
        self.ratio_entry = ratio_entry
        self.retail = int
        self.rate_fees =fees

    def init_cash(self):
        """init cash
        """
        self.retail = 100 / self.ratio_entry
        self.amount = self.cash /  self.retail

    def fees(self,row):
        """rival fess

        Args:
            row (_type_): _description_

        Returns:
            flute: _description_
        """
        fees_ = row * self.rate_fees
        return abs(fees_)
class CalculatorProfit(metaclass=ABCMeta):
    """
    First discrete difference of element.
        .......et
    Parameters
    ----------
    Cash
    RatioEntry
    CP = cumulative profit
    """
    @staticmethod
    def different(func) -> pd.DataFrame :
        """_summary_

        Args:
            func (_type_): _description_

        Returns:
            pd.DataFrame: _description_
        """
        def fuc_wrapper(self,result):
            result['different'] =  result['PriceEndOrder'] - result['Enter'] if result['Type'] == 1\
                else  result['Enter'] - result['PriceEndOrder']
            result = func(self,result)
            return result
        return fuc_wrapper

    @staticmethod
    def quantity_symbol(func) -> pd.DataFrame:
        """_summary_

        Args:
            func (_type_): _description_

        Returns:
            pd.DataFrame: _description_
        """
        def fuc_wrapper(self,result):
            self.initCash()
            result['FeesOpen'] = self.fees(self.amount)
            result['Quantity'] =  self.amount / result['Enter']
            result= func(self,result)
            return result
        return fuc_wrapper
    @staticmethod

    def profit_trade(func)-> pd.DataFrame:
        """_summary_

        Args:
            func (_type_): _description_

        Returns:
            pd.DataFrame: _description_
        """
        def fuc_wrapper(self,result):
            result['ProfitTrade'] = round(result['Quantity'] * result['different'],3)
            result['FeesClose'] =  round(self.fees(result['ProfitTrade'] + self.amount),3)
            result['ProfitTrade']= result['ProfitTrade'] - result['FeesClose']
            result = func(self,result)
            return result
        return fuc_wrapper

    @abstractmethod
    def price_end(self,func)-> None:
        """_summary_.
        """
    @abstractmethod
    def cumulative_profit(self,result)-> None:
        """_summary_.
        """

class UnCumulativeTradeProfit(CalculatorProfit,Money):
    """There is no need to override 'price_end' it has the same
        signature as the implementation in CalculatorProfit.

    Args:
        CalculatorProfit (_type_): _description_
        Money (_type_): _description_
    Parameters
    ----------
    Cash
    RatioEntry
    CP = cumulative profit
    """
    def price_end(self,func):
        def fuc_wrapper(self,result) :
            result['PriceEndOrder']  = \
                [row["tp"] if row['Target'] != 0 else row["sl"] for _,row in result.iterrows() ]
            return func(self,result)
        return fuc_wrapper
    @price_end
    @CalculatorProfit.different
    @CalculatorProfit.quantity_symbol
    @CalculatorProfit.profit_trade
    def cumulative_profit(self,result : pd.DataFrame)-> pd.DataFrame:

        result['CumProfit'] = result['ProfitTrade'].cumsum() +  self.cash
        result['PctProfit'] = result[["Enter",
                                    "PriceEndOrder"]]\
                                    .pct_change(axis="columns",periods=1)["PriceEndOrder"] * 100
        return result
    def profit(self,result):
        """_summary_

        Args:
            result (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.cumulative_profit(result)

class CumulativeTradeProfit(CalculatorProfit,Money):
    """There is no need to override 'price_end' it has the same
        signature as the implementation in CalculatorProfit.
        .......et
    Parameters
    ----------
    Cash
    RatioEntry
    CP = cumulative profit.
    """
    def price_end(self,func):

        def fuc_wrapper(self,result):
            result['PriceEndOrder']  =  result["tp"] if result['Target'] != 0 else result["sl"]
            return func(self,result)
        return fuc_wrapper

    @price_end
    @CalculatorProfit.different
    @CalculatorProfit.quantity_symbol
    @CalculatorProfit.profit_trade
    def cumulative_profit(self,result:pd.DataFrame) -> pd.DataFrame:
        self.cash += result['ProfitTrade']
        result['CumProfit'] =self.cash
        result['PctProfit'] = result[["Enter",
                                      "PriceEndOrder"]]\
                                          .pct_change(periods=1)["PriceEndOrder"]*100
        return  result
    def profit(self,result)-> pd.DataFrame:
        """_summary_

        Args:
            result (_type_): _description_

        Returns:
            pd.DataFrame: _description_
        """
        return result.apply(self.cumulative_profit ,axis = 1 )
    