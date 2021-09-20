from core.client import Trading

#################  BITSTAMP API  #################
userName = '556778'
key_ = 'w01yVvWA8oPUQ7egVLV4hYndkGnb66Hu'
secret_ = 'whqWdzeHyHiejuiq1YFBA8bu79icsnDy'
rest_client = Trading(username=userName, key=key_, secret=secret_)
base_asset = 'XRP'
quote_asset = 'USD'
tradePercentage = 0.6
buyAmount = float(rest_client.account_balance(base=base_asset,quote=quote_asset)['{}_available'.format(quote_asset.lower())]) * tradePercentage
sellAmount = float(rest_client.account_balance(base=base_asset,quote=quote_asset)['{}_available'.format(base_asset.lower())])
timeFrame = '30MIN'  #--> changed
trade = True
sellSleepTime = 2
tradeCycle =15 #Check after x Minutes

#################  COIN API  #################
coinapi_key = 'B9AA57E6-6F7C-479C-8463-252B9567213F'

#################  KLINE SETTINGS  #################
# period = timeFrame

#################  HULL MA  #################
hullPeriod1 = 9
hullPeriod2 = 9

#################  ICHIMOKU CLOUD  #################
leadLine1Period = 9 #title="Conversion Line Periods
# basePeriods = 26,  #title="Base Line Periods")
leadLine2Period = 49 #minval=1, title="Lagging Span 2 Periods")
# displacement = 26 # title="Displacement"

#################  MACD  #################
MACD_fastLength = 12
MACD_slowLength = 26
MacdPeriod = 10
#################  SL/TP  #################

"""here needed a percentage of sl and tp"""

Stop_Loss = 75
Target_Point = 90
