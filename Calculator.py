import pandas as pd


class Calculator_Traded:
    def different (result: type[pd.DataFrame]):
        result['Order_end']  =  [row["tp"] if row['Target'] == 1 else abs(row["sl"])  for row in result]
        result['different'] = result[['Enter','Order_end']].diff(axis=1)
        return result
    def Quantum_(result: type[pd.DataFrame]):
        Enter = result['Enter']



