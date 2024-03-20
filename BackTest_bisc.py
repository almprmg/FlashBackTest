import pandas as pd 
import numpy as np
from Stratigy import Stratigy



class BackTest:
    def __init__(self,data : pd.DataFrame,data_smull,Stratigy :type[Stratigy] ) -> None:
        self.data = data
        self.data_smull = data_smull  
        self.Strutigy = Stratigy
        self.endDate =self.data.index[-1]
        
        if not isinstance(data,pd.DataFrame):
            raise
        #if not isinstance(data.index,pd.Timestamp):
        #    raise
         

    def run(self):
        
        Stratigy = self.Strutigy(self.data_smull,self.data.loc[self.data.Signal != 0 ].index[0])
        Stratigy.init()
        Stratigy.Data = self.data
        if "Signal" in self.data.columns:

            #not Stratigy.Data[ Stratigy.Data.Signal != 0 ].empty
            while not Stratigy.Data[ Stratigy.Data.Signal == 1 ].empty :

                Stratigy.next()
                Stratigy.update()

        self.result = Stratigy.result_orders

    