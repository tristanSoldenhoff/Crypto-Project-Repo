from pycoingecko import CoinGeckoAPI
import datetime
import time
#import pandas as pd
#import plotly.graph_objects as go
#from plotly.offline import plot

class GeckoFunctions:

    def __init__(self):
        self.cg = CoinGeckoAPI()

#====================== Time ===================================================

#convert to unix time
    def unix_time(self, year, month, day, hour, second):
        date_time = datetime.datetime(year, month, day, hour, second)
        return time.mktime(date_time.timetuple())

#convert to human timestamp       coingecko's timestamp is in miliseconds but unix time is in seconds therefore need to divide by 1000
    def human_time(self, unix_time):
        return datetime.datetime.fromtimestamp(unix_time/1000)

#====================== List of cryptocurrencies - Gecko API ===================

# returns all cryptocurrencies        (from rank 1 - whatever crypto rank, all cryptocurrencies)
    def search_crypto(self):
        return self.cg.search(query = "")

#====================== Pricing Data - Gecko API ===============================

#return single crypto price vs currency
    def get_crypto_price(self, crypto, currency):
        return self.cg.get_price(ids=crypto, vs_currencies=currency)

#returns as many crypto prices as you want      eg:     get_multi_crypto_price(['bitcoin','ethereum','tether'], 'usd')
    def get_multi_crypto_price(self, list, currency):
        return self.cg.get_price(ids=list, vs_currencies=currency)

#does the same as both def's above but with more details eg: market cap, volume, 24hr change, 24hr update        eg: B_marketCap = True
    def get_current_attr(self, crypto, currency, B_marketCap, B_24_Volume, B_24_Change, B_timestamp):
        return self.cg.get_price(ids=crypto, vs_currencies=currency, include_market_cap=B_marketCap, include_24hr_vol=B_24_Volume,
         include_24hr_change=B_24_Change, include_last_updated_at=B_timestamp)

#returns lots of information like price, volume, market cap, community data etc            see below for dictionary structure
    def get_coin_data(self, crypto, date):
        return self.cg.get_coin_history_by_id(id=crypto,date=date, localization='false')

#get_coin_data_days(string, string, string/int)         see below for structure and description
    def get_coin_data_days(self, crypto, currency, no_days):
        return self.cg.get_coin_market_chart_by_id(id=crypto,vs_currency=currency,days=no_days)

# returns price data between 2 specified dates        KEEP IN MIND: provides daily data from 2013 - 2019. provides hourly data from 2019 - present.
    def get_data_between_dates(self, crypto, currency, from_timestamp, to_timestamp):
        return self.cg.get_coin_market_chart_range_by_id(id=crypto,vs_currency=currency,from_timestamp=from_timestamp,to_timestamp=to_timestamp)

#====================== xxxxxxxxxxxxxxxxxxxxxxxx ===============================

# This just returns     {'id': 'bitcoin', 'symbol': 'btc', 'name': 'Bitcoin'}    for all crypto's (10 004 crypto's at this point in time)
    def coin_list(self):
        return self.cg.get_coins_list()

# returns OHLC, price, volume, rank, market cap, price change 24h etc ... see below.      bare in mind - parameter 'page' is used to search
# crypto data through search page in the coingecko site.
    def coin_market(self, vs_currency, page):
        return self.cg.get_coins_markets(vs_currency=vs_currency, page=page)

# return massive amounts of info
    def spot_data(self, id):
        return self.cg.get_coin_by_id(id=id)

# returns info regarding exchanges, tickers (btc to usd or eth etc), volumes       (NEED TO ANALYSE THIS MORE)
    def coin_ticker(self, id):
        return self.cg.get_coin_ticker_by_id(id=id)

# return all trending crypto's (not too sure how thats arranged from coingecko)
    def trend(self):
        return self.cg.get_search_trending()

#====================== Exchange Data ==========================================

    def exchange(self):
        return self.cg.get_exchanges_list()

# returns supported markets with a list of id and name
    def markets(self):
        data_id = self.cg.get_exchanges_id_name_list()
        for i in data_id:
            print(f"{i['id']:40s} {i['name']:20s}")

# return exchange volume and top 100 ticker from a specific exchange such as binance, coinbase etc
    def exchange_volume(self, exchange):
        return self.cg.get_exchanges_by_id(exchange)

# returns exchange data such as volume for a range of tickers for one particular exchange
    def exchange_data(self, exchange):
        return self.cg.get_exchanges_tickers_by_id(id=exchange)

#====================== NOT WORKING ============================================
    # def sss(self):
    #     return self.cg.get_exchanges_status_updates_by_id(id='Binance')

    # def ddd(self, exchange, daysxxx):
    #     return self.cg.get_exchanges_volume_chart_by_id(id=exchange, days=daysxxx)
#====================== NOT WORKING ============================================

#====================== Derivatives ============================================

    def derivatives(self):
        return self.cg.get_derivatives()

    def exchange_derivatives(self):
        return self.cg.get_derivatives_exchanges()

    def exchange_derivatives_by_id(self, exchange):
        return self.cg.get_derivatives_exchanges_by_id(id=exchange)

    def exchange_derivatives_list(self):
        return self.cg.get_derivatives_exchanges_list()

#====================== Events =================================================

    #functions listed below aren't working - coingecko might have changed their api calls

    #cg.get_events()
    #data_countries=cg.get_events_countries()
    #cg.get_events_types()









"""

===========================================================structure of         cg.search(query = "")

{ 'coins' : [{'':'', '':'', '':'', '':'',,,} , {'':'', '':'', '':'', '':'',,,} , {'':'', '':'', '':'', '':'',,,}] ,
'exchanges' : [{'':'', '':'', '':'', '':'',,,} , {'':'', '':'', '':'', '':'',,,} , {'':'', '':'', '':'', '':'',,,}] ,
'icos' : [{'':'', '':'', '':'', '':'',,,} , {'':'', '':'', '':'', '':'',,,} , {'':'', '':'', '':'', '':'',,,}] ,
'categories' : [{'':'', '':'', '':'', '':'',,,} , {'':'', '':'', '':'', '':'',,,} , {'':'', '':'', '':'', '':'',,,}] ,
'nfts' : [{'':'', '':'', '':'', '':'',,,} , {'':'', '':'', '':'', '':'',,,} , {'':'', '':'', '':'', '':'',,,}] }

coins
[ {'id': 'bitcoin', 'name': 'Bitcoin', 'api_symbol': 'bitcoin', 'symbol': 'BTC', 'market_cap_rank': 1,
'thumb': 'https://assets.coingecko.com/coins/images/1/thumb/bitcoin.png', 'large': 'https://assets.coingecko.com/coins/images/1/large/bitcoin.png'} .......]
exchanges
[ { id , name, market_type, thumb, large} ]
icos
[]
categories
[ { id, name} ]
nfts
[ { id, name, sybol, thumb } ]

===========================================================structure of         data = get_coin_price('bitcoin', '05-06-2023')

{'id' : 'bitcoin',
'symbol' : 'btc',
'name' : 'Bitcoin',
'image' : {'thumb' : 'https//www......', 'small' : 'https//www........'},
'market_data' : {           'current_price' : {'usd':27000, 'zar':52000, 'gbp':23000, ...},
                            'market_data' : {'usd':2700000000, 'zar':52000000000, 'gbp':2300000000, ...},
                            'total_volume' : {'usd':2700000, 'zar':5200000, 'gbp':2300000, ...} },
'community_data' : {'facebook_likes':None, 'Twitter_followers':4865468, ........},
'developer_data' : {'forks':34523, 'stars':678568, 'subscribers':399293, 'code_additions_deletions_4_weeks': {'additions': 2348, 'deletions': -1655} },
'public_interest_stats': {'alexa_rank': None, 'bing_matches': None} }

===========================================================Structure of         print(gf.get_coin_data_days('bitcoin', 'usd', '2'))

for 0 days:  return data in within last 5 minutes
for 1 day:   return data in 5 minute intervals
for 2 days:  returns data in 1 hour intervals
for 91 days: returns data in 1 day interals

{ 'prices' : [ [timestamp, price] , [timestamp, price] , [timestamp, price] , [timestamp, price] , ....... ] ,
  'market_caps' : [ [timestamp, market_cap] , [timestamp, market_cap] , [timestamp, market_cap] , ........ ] ,
  'total_volumes' : [ [timestamp, volume] , [timestamp, volume] , [timestamp, volume] , ....] }

see below to access particular columns of data:

datax = gf.get_coin_data_days('bitcoin', 'usd', '90')
for i in datax['prices']:
    print(gf.human_time(i[0]) )

===========================================================Structure of         gf.get_data_between_dates('bitcoin', 'usd', gf.unix_time(2023,6,1,0,0), gf.unix_time(2023,6,8,0,0))

HAS SAME STRUCTURE AS ABOVE: gf.get_coin_data_days('bitcoin', 'usd', '2')

see below to access particular columns of data:

datay = gf.get_data_between_dates('bitcoin', 'usd', gf.unix_time(2023,1,1,0,0), gf.unix_time(2023,1,2,0,0))
for i in datay['prices']:
    print(gf.human_time(i[0]))

===========================================================Structure of         coin_market(self, vs_currency, page):

coin_market(self, vs_currency, page) - parameter 'page' is used to search crypto data through search page in the coingecko site.
(see coingecko website) ===== https://apiguide.coingecko.com/getting-started/10-min-tutorial-guide/1-get-data-by-id-or-address

list of dictionaries:
id, symbol, name, image, current_price, market_cap, market_cap_rank, fully_diluted_valuation, total_volume, high_24h, low_24h, price_change_24h,
price_change_24h_percentage, market_cap_change_24h, market_cap_change_percentage_24h, circulating_supply, total_supply, max_supply,
ath (all time high), ath_change_percentage, ath_date, atl (all time low), atl_change_percentage, atl_date, roi : {times, currency, percentage},
last_updated

[{ : }, { : }, { : }]

Use code below to find crypto whos 24h price percentage change is above 10% from pages 1 - 7 in CoinGecko

===========================================================Structure of         a = gf.spot_data('bitcoin')

returns:
id, symbol, name, asset_platform_id, platforms, detail_platforms, block_time_in_minutes, hashing_algorithm, catagories, public_notice,
additional_notices, localization, description, links, image, country_origin, genesis_date, sentiment_votes_up_percentage,
sentiment_votes_down_percentage, watchlist_portfolio_users, market_cap_rank, coingecko_rank, coingecko_score, developer_score,
community_score, liquidity_score, public_interest_score, market_data, community_data, developer_data, public_interest_stats,
status_updates, last_updated, tickers

within list of parameters above there are some parameter that hold even further information listed below:
market_data, tickers:

market_data:
current_price, total_value_locked, mcap_to_tvl_ratio, fdv_to_tvl_ratio, roi, ath, ath_change_percentage, ath_date, atl, atl_change_percentage
atl_date, market_cap, market_cap_rank, fully_diluted_valuation, total_volume, high_24h, low_24h, price_change_24h, price_change_percentage_24h,
price_change_percentage_7d, price_change_percentage_14d, price_change_percentage_30d, price_change_percentage_60d, price_change_percentage_200d,
price_change_percentage_1y, market_cap_change_24h, market_cap_change_percentage_24h, price_change_24h_in_currency, price_change_percentage_1h_in_currency,
price_change_percentage_24h_in_currency, price_change_percentage_7d_in_currency, price_change_percentage_14d_in_currency, price_change_percentage_30d_in_currency,
price_change_percentage_60d_in_currency, price_change_percentage_200d_in_currency, price_change_percentage_1y_in_currency, market_cap_change_24h_in_currency,
market_cap_change_percentage_24h_in_currency, total_supply, max_supply, circulating_supply, last_updated

tickers: below is just one out of many dictionaries - seems to give exchange data on where money is moving:
{'base': 'ETH', 'target': 'BTC', 'market': {'name': 'Coinbase Exchange', 'identifier': 'gdax', 'has_trading_incentive': False},
'last': 0.06711, 'volume': 2639.66387648, 'converted_last': {'btc': 1.0, 'eth': 14.891685, 'usd': 25976},
'converted_volume': {'btc': 177.148, 'eth': 2638, 'usd': 4601559}, 'trust_score': 'green', 'bid_ask_spread_percentage': 0.014905,
'timestamp': '2023-06-14T12:43:39+00:00', 'last_traded_at': '2023-06-14T12:43:39+00:00', 'last_fetch_at': '2023-06-14T12:43:39+00:00',
'is_anomaly': False, 'is_stale': False, 'trade_url': 'https://pro.coinbase.com/trade/ETH-BTC', 'token_info_url': None, 'coin_id': 'ethereum',
'target_coin_id': 'bitcoin'}

===========================================================Structure of         cg.get_coin_ticker_by_id(id='bitcoin')

NEED TO ANALYSE THIS MORE

===========================================================Structure of         cg.get_search_trending()

return all trending crypto's (not too sure how thats arranged from coingecko)
Each trending item also includes a trust score which is graded by trading activity, cybersecurity, web traffic, order book spread and depth,
liquidity, technical expertise etc. more can be found out on https://www.coingecko.com/en/methodology

===========================================================Structure of         cg.get_exchanges_list()

prints out all exchanges with name, country, URL, trust_score, trust_rank, trade volumes

Use code below to print out pandas dataframe:

exchange_data = gf.exchange()
df = pd.DataFrame(exchange_data, columns = ['name', 'trust_score', 'trust_score_rank'])
df.set_index('name', inplace=True)
print(df)

===========================================================Structure of         cg.get_exchanges_id_name_list()

provides a list of supported markets by name and id.
markets will include things like a uniswap token which can be used to trade other tokens and therefore creating a market.
other market examples are: sushiswap, terraswap, pancakeswap etc.

===========================================================Structure of         cg.get_exchanges_by_id(exchange)

return exchange volume and top 100 ticker from a specific exchange such as binance, coinbase etc

df_binance =pd.DataFrame(data_binance['tickers'], columns=['base','target','volume'])
print(df_binance)

===========================================================Structure of         cg.get_exchanges_tickers_by_id(id='gdax')

# returns exchange data such as volume for a range of tickers for one particular exchange

===========================================================Structure of         cg.get_derivatives()

returns
market, symbol, index_id, price, price_percentage_change_24h, contract_type, index, basis, spread, funding_rate, open_interest,
volume_24h, last_traded_at, expired_at

===========================================================Structure of         cg.get_derivatives_exchanges()

returns exchange data:
name, id, open_interest_btc, trade_volume_24h_btc, number_of_perpetual_pairs, number_of_futures_pairs,
image, year_established, country, description, URL













===========================================================TUTORIAL
https://algotrading101.com/learn/coingecko-api-guide/                           (use this site)
https://analyzingalpha.com/coingecko-api-python-tutorial
===========================================================COINGECKO WEBSITE
https://github.com/man-c/pycoingecko/blob/master/pycoingecko/api.py
https://apiguide.coingecko.com/getting-started/10-min-tutorial-guide/1-get-data-by-id-or-address


"""
