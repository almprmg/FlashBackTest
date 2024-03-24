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

    

class CalculatorTraded(Money):
    """
    First discrete difference of element.
        .......et
    Parameters
    ----------
    Cash 
    RatioEntry
    CP = cumulative profit
    """
    def __init__(self,Cash,RatioEntry ,Fees , cp ) -> None:
        super().__init__(Cash,RatioEntry ,Fees  )
        self.__cp = cp
        


    def priceEnd(func):
        def fuc_wrapper(self,result):
            result = result
            if self.__cp:
                result['PriceEndOrder']  =  result["tp"] if result['Target'] == 1 else result["sl"]
            else:
                result['PriceEndOrder']  =  [row["tp"] if row['Target'] == 1 else row["sl"]  for _,row in result.iterrows() ]
            result = func(self,result) 
            return result
        return fuc_wrapper

    def different(func):
        def fuc_wrapper(self,result):
  
            result['different'] =  result['PriceEndOrder'] - result['Enter']
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
    @priceEnd
    @different
    @quantitySymbol
    def __profit(self,result):
        result['ProfitTrade'] = round(result['Quantity'] * result['different'],3)
        result['FeesClose'] =  round(self.fees(result['ProfitTrade'] + self.amount),3)
        result['ProfitTrade']= result['ProfitTrade'] - result['FeesClose']
        
        if self.__cp:
            self.Cash += result['ProfitTrade'] 
            result['CumProfit'] =self.Cash
            result['PctProfit'] = result[["Enter","PriceEndOrder"]].pct_change(periods=1)["PriceEndOrder"]*100

        else:
            result['CumProfit'] = result['ProfitTrade'].cumsum() +  self.Cash
            result['PctProfit'] = result[["Enter","PriceEndOrder"]].pct_change(axis="columns",periods=1)["PriceEndOrder"]*100
        
        return result

    def profit(self,result):
        if  self.__cp:
            
            return result.apply(self.__profit, axis = 1)
        else:
            return self.__profit(result)




