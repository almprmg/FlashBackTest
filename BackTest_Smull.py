

import pandas as pd


class Bacl_Test_smunll:
    def __init__(self) -> None:
        self.data_low = None
        self.tp = None
        self.sl = None
    def next(self):
        high =  self.data_low.loc[self.data_low.High >= self.tp,'High']
        Low =  self.data_low.loc[self.data_low.Low <= self.sl,'Low']
        check = high.index[0] < Low.index[0]
        if check :
            return self.data_low.Date[high.index[0]] 
        else:
            return self.data_low.Date[Low.index[0]] 
    