

from BackTest.BackTest_Smull import Bacl_Test_smunll


class Stratigy(Bacl_Test_smunll):
    tp = None
    sl =None
    def __init__(self,data,data_low) -> None:
        self.data=data
        self.data_low = data_low
        self._postin = False
        
        
    def buy(self, limet,tp: float,sl:float):
        if not self._postin:
            pass
    def Check_Order(self):
        super().next()
        
        
