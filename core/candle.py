from core.coinapi_rest_v1 import CoinAPIv1

from settings import coinapi_key
api = CoinAPIv1(coinapi_key)

def klines(base_pair, cross_pair, period):
    ohlcv_latest = api.ohlcv_latest_data('BITSTAMP_SPOT_{}_{}'.format(base_pair, cross_pair), {'period_id': period})
    '''
    tohlcv
    '''
    return [
    [period['time_period_end'] for period in ohlcv_latest][::-1],
    [period['price_open'] for period in ohlcv_latest][::-1],
    [period['price_high'] for period in ohlcv_latest][::-1],
    [period['price_low'] for period in ohlcv_latest][::-1],
    [period['price_close'] for period in ohlcv_latest][::-1],
    [period['volume_traded'] for period in ohlcv_latest][::-1],
    ]

#from pyti import moving_average_convergence_divergence as macd, exponential_moving_average as ema
#print(ema.exponential_moving_average(macd.moving_average_convergence_divergence(data=klines(base_pair='BTC', cross_pair='USD', period='15MIN')[4], short_period=10, long_period=20), 20))
#print(macd.moving_average_convergence_divergence(data=klines(base_pair='BTC', cross_pair='USD', period='15MIN')[4], short_period=10, long_period=20)[-1])

# print(klines(base_pair='BTC', cross_pair='USD', period = '15MIN'))