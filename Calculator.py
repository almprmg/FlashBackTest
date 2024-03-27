from abc import ABCMeta ,abstractmethod
import pandas as pd

class Money:
    def __init__(self,Cash,RatioEntry ,Fees ) -> None:
        
        self.Cash =  Cash
        self.amount : float
        self.RatioEntry = RatioEntry
        self.Retail = int
        self.Fees =Fees

    def initCash(self):
        self.Retail = 100 / self.RatioEntry 
        self.amount = self.Cash /  self.Retail

    def fees(self,row):
        Fees = row * self.Fees
        return abs(Fees)

    


class Calculator_profit(metaclass=ABCMeta):
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
    def different(func):
        def fuc_wrapper(self,result):
            result['different'] =  result['PriceEndOrder'] - result['Enter'] if result['Type'] == 1  else  result['Enter'] - result['PriceEndOrder']
            result = func(self,result) 
            return result
        return fuc_wrapper

    @staticmethod
    def quantitySymbol(func):
        def fuc_wrapper(self,result):
            self.initCash()
            result['FeesOpen'] = self.fees(self.amount)
            result['Quantity'] =  self.amount / result['Enter']
            result= func(self,result)
            return result
        return fuc_wrapper
    @staticmethod
    def profit_Trade(func):
        def fuc_wrapper(self,result):
            result['ProfitTrade'] = round(result['Quantity'] * result['different'],3)
            result['FeesClose'] =  round(self.fees(result['ProfitTrade'] + self.amount),3)
            result['ProfitTrade']= result['ProfitTrade'] - result['FeesClose'] 
            result = func(self,result)
            return result
        return fuc_wrapper

    @abstractmethod
    def priceEnd(self)-> None:
        pass

    @abstractmethod
    def cumulative_profit(self)-> None:
        pass

    

       

class unCumulative_Trade_profit(Calculator_profit,Money):

    def __init__(self,Cash,RatioEntry ,Fees ) -> None:
        super().__init__(Cash,RatioEntry ,Fees )
        
    @staticmethod
    def different(func):
        def fuc_wrapper(self,result):
            result['different'] =  result['PriceEndOrder'] - result['Enter'] if result['Type'] == 1  else  result['Enter'] - result['PriceEndOrder']
            result = func(self,result) 
            return result
        return fuc_wrapper

    @staticmethod
    def quantitySymbol(func):
        def fuc_wrapper(self,result):
            self.initCash()
            result['FeesOpen'] = self.fees(self.amount)
            result['Quantity'] =  self.amount / result['Enter']
            result= func(self,result)
            return result
        return fuc_wrapper
    @staticmethod
    def profit_Trade(func):
        def fuc_wrapper(self,result):
            result['ProfitTrade'] = round(result['Quantity'] * result['different'],3)
            result['FeesClose'] =  round(self.fees(result['ProfitTrade'] + self.amount),3)
            result['ProfitTrade']= result['ProfitTrade'] - result['FeesClose'] 
            result = func(self,result)
            return result
        return fuc_wrapper
    
    def priceEnd(func):

        def fuc_wrapper(self,result):
            super().priceEnd()     
            result = result
            result['PriceEndOrder']  =  [row["tp"] if row['Target'] != 0 else row["sl"]  for _,row in result.iterrows() ]
            result = func(self,result) 
            return result
        return fuc_wrapper



    def cumulative_profit(self,result):
        super().cumulative_profit()
        result['CumProfit'] = result['ProfitTrade'].cumsum() +  self.Cash
        result['PctProfit'] = result[["Enter","PriceEndOrder"]].pct_change(axis="columns",periods=1)["PriceEndOrder"]*100
        
        return result
    @priceEnd
    @Calculator_profit.different
    @Calculator_profit.quantitySymbol
    @Calculator_profit.profit_Trade
    def cumulative_profit(self, result):
        super().cumulative_profit()
        result['PctProfit'] = result[["Enter","PriceEndOrder"]].pct_change(axis="columns",periods=1)["PriceEndOrder"]*100
        result['CumProfit'] = result['ProfitTrade'].cumsum() +  self.Cash
        
        return result
    def profit(self,result):
            return self.cumulative_profit(result)

class cumulative_trade_profit(Calculator_profit,Money):
    """
    First discrete difference of element.
        .......et
    Parameters
    ----------
    Cash 
    RatioEntry
    CP = cumulative profit
    """
    def __init__(self,Cash,RatioEntry ,Fees ) -> None:
        super().__init__(Cash,RatioEntry ,Fees  )

    def priceEnd(func):
        def fuc_wrapper(self,result):
            super().priceEnd()
            result = result
            result['PriceEndOrder']  =  result["tp"] if result['Target'] != 0 else result["sl"]
            result = func(self,result)
            return result
        return fuc_wrapper
    



    @priceEnd
    @Calculator_profit.different
    @Calculator_profit.quantitySymbol
    @Calculator_profit.profit_Trade
    def cumulative_profit(self,result):
        super().cumulative_profit()
        self.Cash += result['ProfitTrade'] 
        result['CumProfit'] =self.Cash
        result['PctProfit'] = result[["Enter","PriceEndOrder"]].pct_change(periods=1)["PriceEndOrder"]*100 
        return  result
    
    def profit(self,result):
            return result.apply(self.cumulative_profit, axis = 1)






