import pandas as pd


class Calculator_Traded:
    """
    First discrete difference of element.
        .......et
    Parameters
    ----------
    Cash 
    RatioEntry
    CP = cumulative profit
    """
    amount :float
    def __init__(self,Cash : int = 1000 ,RatioEntry :int =1000 ,Fees : int = None, CP : bool = False ) -> None:
        
        self.Cash =  Cash
        self.amount : float
        self.RatioEntry = RatioEntry
        self.CP = CP
        self.Retail = int
        self.Fees =Fees

    def initCash(self):
        self.Retail = 100 / self.RatioEntry 
        self.amount = self.Cash /  self.Retail

    def fees(self,row):
        Fees = row * self.Fees
        return abs(Fees)

    def different(func):
        def fuc_wrapper(self,result):
            
            result['PriceEndOrder']  =  [row["tp"] if row['Target'] == 1 else row["sl"]  for _,row in result.iterrows()]
            result['different'] = result[['Enter','PriceEndOrder']].diff(axis=1)['PriceEndOrder']
            result = func(self,result) 
            return result
        return fuc_wrapper
    
    
    def quantitySymbol(func):
        def fuc_wrapper(self,result):

            self.initCash()
            result['FeesOpen'] = self.fees(self.amount)
            result['Quantity'] =  self.amount / result['Enter']
            result= func(self,result)
            return result
        return fuc_wrapper
    @different
    @quantitySymbol
    def profit(self,result):

        result['ProfitTrade'] = round(result['Quantity'] * result['different'],3)
        result['FeesClose'] =  result['ProfitTrade'].add(self.amount).apply(self.fees)
        result['ProfitTrade']= result[['ProfitTrade','FeesClose']].diff(axis=1,periods=-1)['ProfitTrade'].round(3)
        result['CumProfit'] = result['ProfitTrade'].cumsum()
        result['PctProfit'] = result[["Enter","PriceEndOrder"]].pct_change(axis="columns",periods=1)["PriceEndOrder"]*100
        
        return result




