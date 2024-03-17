import pandas as pd 
import numpy as np
from Stratigy import Stratigy



class BackTest:
    def __init__(self,data : pd.DataFrame,data_smull,Strutigy :type[Stratigy] ) -> None:
        self.data1 = data
        self.data = None
        self.data_smull = data_smull  
        self.Strutigy = Strutigy
        if not isinstance(data,pd.DataFrame):
            raise
        if not isinstance(data.index,pd.Timestamp()):
            raise
         

    def run(self):
        self.Strutigy.inint
        for index in range(0,len(self.data1)-1):
            self.data = self.data1[:index,:]
            self.Strutigy.next()
            

    

    