

import pandas as pd


class Bacl_Test_smunll:
    def __init__(self) -> None:
        self.data_low = None
        self.tp = None
        self.sl = None
        self.order = None
        self._postin = False
    def Trade(self):
        high =  self.data_low.loc[self.data_low.High >= self.tp,'High']
        Low =  self.data_low.loc[self.data_low.Low <= self.sl,'Low']
        check = high.index[0] < Low.index[0]
        if check :
            self.order.append(1)
            self.order.append(high.index[0])

        else:
            self.order.append(0)
            self.order.append(Low.index[0])
      
    