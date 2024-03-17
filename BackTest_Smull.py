

import pandas as pd


class Bacl_Test_smunll:
    def __init__(self) -> None:
        self.data_low = None
        self.tp = None
        self.sl = None
        self.order = None
        self._postin = False
        self.Date_ende_order = None
    def Trade(self):
        high =  self.data_low.loc[self.data_low.High >= self.tp].index[0]
        Low =  self.data_low.loc[self.data_low.Low <= self.sl].index[0]
        if high.empty and Low.empty:
            self.Date_ende_order = self.data_low.index[-1] + pd.Timestamp(day=1,unit='ms')
        check = high < Low
        if check :
            self.order.append(1)
            self.order.append(high)
            self.Date_ende_order = high

        else:
            self.order.append(0)
            self.order.append(Low)
            self.Date_ende_order = high
      
    