import pandas as pd 
import numpy as np
from Stratigy import Strategy



class BackTest:
    def __init__(self,data : pd.DataFrame,data_small,Strategy :type[Strategy] ) -> None:
        self.data = data
        self.data_small = data_small  
        self.Strategy = Strategy
        self.endDate =self.data.index[-1]
        
        if not isinstance(data,pd.DataFrame):
            raise
        #if not isinstance(data.index,pd.Timestamp):
        #    raise
         

    def run(self):
        
        Strategy = self.Strategy(self.data_small,self.data.loc[self.data.Signal != 0 ].index[0])
        Strategy.init()
        Strategy.Data = self.data
        if "Signal" in self.data.columns:

            #not Strategy.Data[ Strategy.Data.Signal != 0 ].empty
            while not Strategy.Data[ Strategy.Data.Signal == 1 ].empty :

                Strategy.next()
                Strategy.update()

        self.result = Strategy.result_orders

    