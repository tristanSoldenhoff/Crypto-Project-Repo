from gecko_functions import GeckoFunctions
import datetime
import time

# from datetime import datetime


# child class to gecko_functions
class DataProcessingFunctions(GeckoFunctions):

    def btc_halving_dates(self):
        dates_list = ['2012/11/28', '2016/07/09', '2020/05/11', '2024/04/25']
        halving_datetime = []
        for i in dates_list:
            halving_datetime.append(datetime.datetime.strptime(i, '%Y/%m/%d'))
        return halving_datetime

#convert to unix time
    def unix_time(self, year, month, day, hour, second):
        date_time = datetime.datetime(year, month, day, hour, second)
        return time.mktime(date_time.timetuple())

#convert to human timestamp       coingecko's timestamp is in miliseconds but unix time is in seconds therefore need to divide by 1000
    def human_time(self, unix_time):
        return datetime.datetime.fromtimestamp(unix_time/1000)

# creates a list of cryptos with id, symbol, current_price, market_cap, market_cap_rank, total_volume, price_percentage_change_24h with all elements
# sorted to price percentage change. This function is used by the three functions below. leaves out crypto with NoneType values for price_percentage_change_24h
    def tree_view_data(self, currency, fromPage, toPage):
        treeviewList = []
        templist = []
        for i in range(fromPage, toPage):
            data_page = GeckoFunctions.coin_market(self, currency, i)
            for j in data_page:
                templist.append(j['market_cap_rank'])
                templist.append(j['id'])
                templist.append(j['symbol'])
                templist.append(format(j['market_cap'], ',.0f'))
                templist.append(format(j['total_volume'], ',.0f'))
                templist.append(format(j['price_change_percentage_24h'], '.2f'))
                templist.append(j['current_price'])
                treeviewList.append(templist)
                templist = []
        treeviewList.sort(key = lambda x:float(x[0]))
        return treeviewList
