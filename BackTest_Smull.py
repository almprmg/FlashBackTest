

class Bacl_Test_smunll:
    def __init__(self,Start_Date,data_low) -> None:
        self.data_low = data_low.loc[Start_Date]
        self.tp = None
        self.sl - None
    def next(self):
        high =  self.data_low.loc[self.data_low.High >= self.tp,'High']
        Low =  self.data_low.loc[self.data_low.Low >= self.sl,'Low']
        check = high.index[0] < Low.index[0]
        if check :
            return self.data_low.Date[high.index[0]] 
        else:
            return self.data_low.Date[Low.index[0]] 
    