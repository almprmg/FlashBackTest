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
 
    def __init__(self,Cash : int = 1000 ,RatioEntry :int =100 ,Fees : int = None, CP : bool = False ) -> None:
        
        self.Cash =  Cash
        self.amount : float
        self.RatioEntry = RatioEntry
        self.CP = CP
        self.Retail = int
        self.Fees =Fees
        
    def initCash(self):
        self.Retail = 100 / self.RatioEntry 
        self.amount = self.Cash /  self.Retail

    def fees(self):
        Fees = self.amount * self.Fees
        self.amount = self.amount -Fees
    def different(self,result: type[pd.DataFrame]):
        result['PriceEndOrder']  =  [row["tp"] if row['Target'] == 1 else row["sl"]  for _,row in result.iterrows()]
        result['different'] = result[['Enter','PriceEndOrder']].diff(axis=1)['PriceEndOrder']
        return result
    
    
    def quantitySymbol(self,result: type[pd.DataFrame]):
        result['Quantity'] = result['Enter'] * self.amount
        return result

    def profit(self,result: type[pd.DataFrame]):
        result['Profit'] = result['Quantity'] * result['different']
        return result




