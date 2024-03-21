import pandas as pd
from BackTest_bisc import BackTest
from Stratigy import Strategy

timeframe = "1h"
timeflow = "5m"
symbol = "AGLDUSDT"
data_low = pd.read_csv(f'C:/Users\dell/Desktop/module Python for Analysis Tradr/data/{timeflow}/{symbol}.csv',index_col=0)
df1= pd.read_csv(r'C:\Users\dell\Desktop\module Python for Analysis Tradr\Backtest_orders\data.csv',index_col=0)
data_low.index = pd.to_datetime(data_low.index)

df1["Date"]  = pd.to_datetime(df1["Date"] ,unit='ms')
df1 = df1.set_index('Date')
class myClass(Strategy):
    def init(self) -> None:
       super().init()
       self.highest_bot = df1.highest_bot
       self.highest_top = df1.highest_top

    def next(self) -> None:
        super().next()
        data = self.Data.loc[self.Data.Signal == 1]
        signal =  data.index[0] if not data.empty else None

        if signal != None and self.Data.Signal[signal] == 1  :
            self.limet = self.highest_top[signal]
            highest_bot =self.highest_bot[signal]
            self.sl =  highest_bot - ((self.limet - highest_bot) *2) 
            self.tp =  highest_bot + ((self.limet - highest_bot) *10) 
            
            self.buy(limit=self.limet ,tp=self.tp,sl= self.sl )
        elif signal != None and  self.Data.Signal[signal]== 2:
            self.Data = self.Data.loc[self.Data.index > signal[0] ]

bt = BackTest(df1,data_low,myClass)
bt.run()
print(bt.result)

