from pandas import Series
def swap(first,secund):
        return  secund ,first

def is_empty(date_target :Series , date_loss :Series ) -> bool:

        return (date_target or date_loss)

def check_empty(series_data : Series):

        return False if series_data.empty else series_data.index[-1]
def adding_number(num1,num2):
    num1 = str(num1)
    num2 = str(num2)
    return int(num1+num2)