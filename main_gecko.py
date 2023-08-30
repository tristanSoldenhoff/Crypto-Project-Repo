"""
API Tutorial websites:
https://algotrading101.com/learn/coingecko-api-guide/                           (use this site)
https://analyzingalpha.com/coingecko-api-python-tutorial

"""

from pycoingecko import CoinGeckoAPI
import datetime
import time
import pandas as pd
from gecko_functions import GeckoFunctions
from my_functions import MyFunctions
from my_visualization import MyVisualization


gf = GeckoFunctions()
mf = MyFunctions()
mv = MyVisualization()

all_crypto = gf.search_crypto()

#-------------------------------------- GeckoFunctions -------------------------

# print(all_crypto)
#print(gf.get_crypto_price('bitcoin', 'usd'))
#print(gf.get_multi_crypto_price(['bitcoin','ethereum','tether'], 'usd'))
#print(gf.get_current_attr(['bitcoin'], 'usd', True, True, True, True))
#print(gf.get_coin_data('bitcoin', '05-06-2023'))
#print(gf.get_coin_data_days('bitcoin', 'usd', '2'))
#print(gf.get_data_between_dates('bitcoin', 'usd', gf.unix_time(2023,6,1,0,0), gf.unix_time(2023,6,8,0,0)))
#print(gf.coin_list())
#print(gf.coin_market('usd', 1))
#print(gf.spot_data('bitcoin'))
#print(gf.coin_ticker('bitcoin'))
#print(gf.trend())
#print(gf.exchange())
#gf.markets()
#print(gf.exchange_volume('binance'))
#data = gf.exchange_volume('binance')
#print(gf.exchange_data('gdax'))
#-------------------------------------- NOT WORKING --------------------------- print(gf.sss())
#-------------------------------------- NOT WORKING --------------------------- print(gf.ddd('Binance', 2))
#print(gf.derivatives())
#print(gf.exchange_derivatives())
# print(gf.exchange_derivatives_by_id('binance_futures'))
# print(gf.exchange_derivatives_list())
#-------------------------------------- NOT WORKING --------------------------- print(gf.events())



#-------------------------------------- My_Functions --------------------------

#mf.total_crypto_market_cap('usd',1,11)
# print('Total number of cryptos right now are: ' + str(mf.total_number_of_cryptos()))
#mf.list_of_cryptos()
# print('Total number of cryptos right now are: ' + str(mf.total_number_of_exchanges()))
# mf.list_of_exchanges()
# mf.select_single_crypto(0)
# print(mf.get_current_attr_mf(['bitcoin'], 'usd', True, True, True, True))
#mf.crypto_price_percentage_change_24h('usd',1,11)
#mf.biggest_gainers_24h('usd',1,11)
#mf.biggest_losers_24h('usd',1,11)



#mf.percentage_change_7d('bitcoin', 'usd')
#mf.percentage_change_7d()
#mf.percentage_change_7d('ishares-msci-world-etf-tokenized-stock-defichain', 'usd')

#mf.test1()


#-------------------------------------- My_Visualization -----------------------

mv.plotGraph()








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
