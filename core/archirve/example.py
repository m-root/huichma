from core.coinapi_rest_v1 import CoinAPIv1

from settings import coinapi_key
api = CoinAPIv1(coinapi_key)

def klines(base_pair, cross_pair):
    ohlcv_latest = api.ohlcv_latest_data('BITSTAMP_SPOT_{}_{}'.format(base_pair, cross_pair), {'period_id': '15MIN'})
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

print(klines(base_pair='BTC', cross_pair='USD'))