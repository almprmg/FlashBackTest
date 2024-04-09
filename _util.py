from pandas import Series

def is_empty(date_target :Series , date_loss :Series ) -> bool:

        return (date_target or date_loss)

def check_empty(series_data : Series):

        return False if series_data.empty else series_data.index[-1]
def adding_threezero(num1):


    return int(f"{num1}{0}{0}{0}")