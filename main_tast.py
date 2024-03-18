import pandas as pd
from BackTest_bisc import BackTest
from Stratigy import Stratigy

timeframe = "1h"
timeflow = "5m"
symbol = "AGLDUSDT"
data_low = pd.read_csv(f'C:/Users\dell/Desktop/module Python for Analysis Tradr/data/{timeflow}/{symbol}.csv',index_col=0)
df1= pd.read_csv(r'C:\Users\dell\Desktop\module Python for Analysis Tradr\Backtest_orders\data.csv',index_col=0)
data_low.Date = pd.to_datetime(data_low.Date,unit='ms')
data_low.index = data_low.set_index(data_low.Date)
df1.Date = pd.to_datetime(df1.Date,unit='ms')
df1.index = df1.set_index(df1.Date)
class myClass(Stratigy):
    def init(self) -> None:
       super().init()
       self.highest_bot = df1.highest_bot
       self.highest_top = df1.highest_top

    def next(self) -> None:
        super().next()
        signal =  self.Data.loc[self.Data.Signal == 1].index[0]
        if self.Data.Signal[signal] == 1 :
            self.limet = self.highest_top[signal]
            highest_bot =self.highest_bot[signal]
            self.sl = highest_bot- ((self.limet - highest_bot) *3) 
            self.tp =  highest_bot + ((self.limet - highest_bot) *5) 
            
            self.buy(limet=self.limet ,tp=self.tp,sl= self.sl )
        elif signal.values[0] == 2:
            self.Data = self.Data.loc[self.Data.index > signal.index[0] ]


            
BackTest(df1,data_low,myClass).run()  
