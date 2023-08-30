from gecko_functions import GeckoFunctions
import datetime
import time

# child class to gecko_functions
class MyFunctions(GeckoFunctions):

#convert to unix time
    def unix_time(self, year, month, day, hour, second):
        date_time = datetime.datetime(year, month, day, hour, second)
        return time.mktime(date_time.timetuple())

#convert to human timestamp       coingecko's timestamp is in miliseconds but unix time is in seconds therefore need to divide by 1000
    def human_time(self, unix_time):
        return datetime.datetime.fromtimestamp(unix_time/1000)

# This is not working - might be becuase not all pages can be analysed
    def total_crypto_market_cap(self, currency, fromPage, toPage):
        marketCap = 0
        for i in range(fromPage, toPage):
            data_page = GeckoFunctions.coin_market(self, currency, i)
            for j in data_page:
                marketCap += j['market_cap']
        print(format(marketCap, ',.0f'))

# prints total number of cryptos, returns int
    def total_number_of_cryptos(self):
        data = GeckoFunctions.search_crypto(self)
        return len(data['coins'])

# prints a list of all cryptos : marketcap rank, id, name, symbol
    def list_of_cryptos(self):
        data = GeckoFunctions.search_crypto(self)
        coinlist = []
        templist = []
        for i in data['coins']:                                                 # making list of lists
            templist.append(i['market_cap_rank'])
            templist.append(i['id'])
            templist.append(i['name'])
            templist.append(i['symbol'])
            coinlist.append(templist)
            templist = []
        # print(f"{'Rank':5s} {'ID':25s} {'Name':20} {'Symbol'} \n" + "="*80)
        # for i in coinlist:
        #     if i[0] == None:
        #         continue
        #     elif i[0] <= 100:                                                   # select number of cryptos to be printed out (cmd can only print a finite number)
        #         print(f"{str(i[0]):5s} {str(i[1]):25s} {str(i[2]):20s} {str(i[3])}")

        return coinlist


# prints details on 1 single crypto with num=rank : id, name, api_symbol, symbol, market_cap_rank, thumb, large
    def select_single_crypto(self, num):
        data = GeckoFunctions.search_crypto(self)
        print(data['coins'][num])

# prints total number of exchanges, returns int
    def total_number_of_exchanges(self):
        data = GeckoFunctions.search_crypto(self)
        return len(data['exchanges'])

# prints all exchanges : id, name
    def list_of_exchanges(self):
        data = GeckoFunctions.search_crypto(self)
        exchlist = []
        templist = []
        for i in data['exchanges']:
            templist.append(i['id'])
            templist.append(i['name'])
            exchlist.append(templist)
            templist = []
        print(f"{'ID':60s} {'Name':20s}")
        for i in exchlist:
            print(f"{str(i[0]):40s} {str(i[1]):20s}")

# returns price, market_cap, 24hr volume, 24hr change, last updated      FOR A SINGLE CRYPTO.
    def get_current_attr_mf(self, crypto, currency, B_marketCap, B_24_Volume, B_24_Change, B_timestamp):
        data = GeckoFunctions.get_current_attr(self, crypto, currency, B_marketCap, B_24_Volume, B_24_Change, B_timestamp)
        price = data[crypto[0]]['usd']
        market_cap = format(data[crypto[0]]['usd_market_cap'], ',.0f')
        vol_24h = format(data[crypto[0]]['usd_24h_vol'], ',.0f')
        change_24h = format(data[crypto[0]]['usd_24h_change'], '.2f')
        update_time = data[crypto[0]]['last_updated_at']
        print(f"{crypto[0] + ' Price':15s} {'Market Cap':20s} {'24hr Volume':20} {'24hr Change':20s} {'last updated':20s} \n" + "="*90)
        print(f"{'$' + str(price):15s} {str(market_cap):20s} {str(vol_24h):20} {str(change_24h + '%'):20s} {str(MyFunctions.human_time(self, update_time*1000)):20s}")

# creates a list of cryptos with id, symbol, current_price, market_cap, market_cap_rank, total_volume, price_percentage_change_24h with all elements
# sorted to price percentage change. This function is used by the three functions below. leaves out crypto with NoneType values for price_percentage_change_24h
    def create_crypto_price_percentage_change_24h(self, currency, fromPage, toPage):
        percentageList = []
        templist = []
        for i in range(fromPage, toPage):
            data_page = GeckoFunctions.coin_market(self, currency, i)
            for j in data_page:
                if j['price_change_percentage_24h'] is not None:
                    templist.append(j['id'])
                    templist.append(j['symbol'])
                    templist.append(j['current_price'])
                    templist.append(format(j['market_cap'], ',.0f'))
                    templist.append(j['market_cap_rank'])
                    templist.append(format(j['total_volume'], ',.0f'))
                    templist.append(format(j['price_change_percentage_24h'], '.2f'))
                    percentageList.append(templist)
                    templist = []
        percentageList.sort(key = lambda x:float(x[6]))     # sorts in ascending order so biggest losers will be appended firs and biggest gainers will be last
        return percentageList

# prints out list of biggest gainers and losers across 10 pages of coingecko
    def crypto_price_percentage_change_24h(self, currency, fromPage, toPage):
        percentageList = self.create_crypto_price_percentage_change_24h( currency, fromPage, toPage)
        print(f"{'ID':35s} {'Symbol':10s} {'Current Price':15} {'Market Cap':20s} {'Rank':5s} {'Total Volume':20s} {'Price Percentage change 24h':20s} \n" + "="*155)
        for i in percentageList:
            print(f"{str(i[0]):35s} {str(i[1]):10s} {str(i[2]):15} {str(i[3]):20s} {str(i[4]):5s} {str(i[5]):20s} {str(i[6]) + ' %':20s}")

# prints top 20 cryptos with highest gains over past 24h
    def biggest_gainers_24h(self, currency, fromPage, toPage):
        percentageList = self.create_crypto_price_percentage_change_24h(currency, fromPage, toPage)
        top_gainers = percentageList[-20:]
        top_gainers.sort(reverse=True)
        print(f"{'ID':35s} {'Symbol':10s} {'Current Price':15} {'Market Cap':20s} {'Rank':5s} {'Total Volume':20s} {'Price Percentage change 24h':20s} \n" + "="*155)
        for i in top_gainers:
            print(f"{str(i[0]):35s} {str(i[1]):10s} {str(i[2]):15} {str(i[3]):20s} {str(i[4]):5s} {str(i[5]):20s} {str(i[6]) + ' %':20s}")

# prints top 20 cryptos with largest drop over past 24h
    def biggest_losers_24h(self, currency, fromPage, toPage):
        percentageList = self.create_crypto_price_percentage_change_24h(currency, fromPage, toPage)
        top_losers = percentageList[:20]
        print(f"{'ID':35s} {'Symbol':10s} {'Current Price':15} {'Market Cap':20s} {'Rank':5s} {'Total Volume':20s} {'Price Percentage change 24h':20s} \n" + "="*155)
        for i in top_losers:
            print(f"{str(i[0]):35s} {str(i[1]):10s} {str(i[2]):15} {str(i[3]):20s} {str(i[4]):5s} {str(i[5]):20s} {str(i[6]) + ' %':20s}")





    # def test1(self):
    #     data_page = GeckoFunctions.spot_data(self, 'bitcoin')
    #     cryptoID = GeckoFunctions.search_crypto(self)
    #
    #     for i in cryptoID['coins']:
    #             data = GeckoFunctions.spot_data(self, i['id'])
    #             print(i['id'])


    # def percentage_change_7d(self, no_days=6):
    #     cryptoID = GeckoFunctions.search_crypto(self)
    #     price7days = []
    #     templist = []
    #
    #     for i in cryptoID['coins']:
    #         data = GeckoFunctions.get_coin_data_days(self, i['id'], 'usd', no_days=no_days)
    #         print(i['id'])
    #         templist.append(data['prices'][0][0])                               # [start_time, start_price, end_time, end_price]
    #         templist.append(data['prices'][0][1])
    #         templist.append(data['prices'][-1][0])
    #         templist.append(data['prices'][-1][1])

    # def percentage_change_7d(self, crypto, currency, no_days=6):
    #     data = GeckoFunctions.get_coin_data_days(self, crypto, currency, no_days=no_days)
    #     for i in data['prices']:
    #         print(str(self.human_time(i[0]).strftime('%d %m %Y %H:%M:%S')) + '\t' + str(format(i[1], '.12f')))
    #     print()
    #     start_time = data['prices'][0][0]
    #     start_price = data['prices'][0][1]
    #     print(str(self.human_time(start_time).strftime('%d %m %Y %H:%M:%S')) + '\t' + str(format(start_price, '.12f')))
    #
    #     end_time = data['prices'][-1][0]
    #     end_price = data['prices'][-1][1]
    #     print(str(self.human_time(end_time).strftime('%d %m %Y %H:%M:%S')) + '\t' + str(format(end_price, '.12f')))
    #
    #     percentage = ((end_price - start_price) / start_price) * 100
    #     print(percentage)















"""
================================================================================
Use for later
================================================================================

for i in range(1,7):
    data_page = gf.coin_market('usd',i)
    for j in data_page:
        if j['price_change_percentage_24h'] == None:
            continue
        elif j['price_change_percentage_24h'] >= 40.0:
            print(f"{j['name']:20s} {str(j['market_cap_rank']):20s} {str(j['price_change_percentage_24h']):20s}")

print('7 days worth of price data \n============================\n' )
datay = gf.get_data_between_dates('bitcoin', 'usd', gf.unix_time(2023,6,15,0,0), gf.unix_time(2023,6,22,0,0))
for i in datay['prices']:
    print(gf.human_time(i[0]))

"""
