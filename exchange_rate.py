from currency_converter import CurrencyConverter
import datetime
import csv
import itertools
import ssl

def currency_conversion_module(base_currency:str = 'EUR',source_currencies:list=['USD'],start_date:datetime.datetime=datetime.date.today(), end_date:datetime.datetime= (datetime.date.today() + datetime.timedelta(days=1)),file_path:str='', append:bool=False, add_header:bool=False, header:list=[]) -> None:
    """
    Aguments:
    base_currency - 

    """
    ssl._create_default_https_context = ssl._create_unverified_context
    c = CurrencyConverter('http://www.ecb.int/stats/eurofxref/eurofxref-hist.zip',fallback_on_missing_rate=True,fallback_on_missing_rate_method="last_known")


    currencies=[]
    exchange_rates=[]
    dates=[]
    def fetch_currency_exchange_rates(dates,source_currencies,currencies,exchange_rates,start_date, end_date)->object:
        """ 
        This function returns variable that contains exchange rates, dates, currencies and country version ids, for a range of dates
        """
        def daterange(start_date, end_date)->range:
            """ 
            This function receives start and end date and returns a date range
            """
            for n in range(int ((end_date - start_date).days)):
                yield start_date + datetime.timedelta(n)

        calender_dates=[]
        for single_date in daterange(start_date, end_date):
            
            calender_dates.append(single_date) #saves the date range as an array into a variable calender_dates
        #print(calender_dates)

        for date in calender_dates: #loop that iterates through each date
            for source_currency in source_currencies: # for each date this loop iterates through all the currencies in countries_currencies variable
                if date.isoweekday() in (6,7):
                    date_no_weekend=date - datetime.timedelta(days=date.isoweekday()-5)
                else:
                    date_no_weekend=date
                exchange_rates.append(c.convert(1, source_currency, base_currency,date_no_weekend)) # gets the exchange rate through api
                dates.append(date)
                currencies.append(source_currency)

        data=list(zip(dates,itertools.repeat(base_currency),currencies,exchange_rates)) # puts all the data togehter into a data variable
        return data


    data=fetch_currency_exchange_rates(dates,source_currencies,currencies,exchange_rates,start_date,end_date) #enable daily update. Calls the update_today function and stores the result in data variable
    if append:
        mode='a+'
    else:
        mode='w'

    with open(file_path, mode, newline='') as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    if add_header and mode=='w':
                        filewriter.writerow(header)
                    else:
                        pass
                    for value in data:
                        filewriter.writerow(value)

start_date = datetime.date(2021, 5, 31) #define start date of the date range
end_date = datetime.date(2021, 6, 1) # define end date of the date range (it should be desired end date + 1 day)
header=['Date','Base Currency','Source Currency','Exchange rate']
currency_conversion_module(file_path='/Users/michaelkorotkov/my-dev/test_exchange_rate.csv',start_date=start_date,end_date=end_date, add_header=True, header=header, append=True)