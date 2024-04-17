from numbers import Number
from typing import Union
from pandas import Series
from pandas import Timedelta

def is_empty(date_target :Series , date_loss :Series ) -> bool:

        return (date_target or date_loss)

def check_empty(series_data : Series):

        return False if series_data.empty else series_data.index[-1]
def adding_threezero(num1):


    return int(f"{num1}{0}{0}{0}")

def _data_period(index) -> Union[Timedelta, Number]:
    """Return data index period as pd.Timedelta"""
    values = Series(index[-100:])
    return values.diff().dropna().median()