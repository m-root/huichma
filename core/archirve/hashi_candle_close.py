import numpy as np
from datetime import datetime, timedelta, timezone
from pyti import exponential_moving_average as ema, smoothed_moving_average as sma


def candles(symbol, interval, rest_client):
    klines = rest_client.klines(symbol=symbol, interval=interval)
    cand = []

    for kline in klines:
        f = [
            (datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=kline.open_time / 1000)),
            (datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=kline.close_time/ 1000)),
            kline.open,
            kline.high,
            kline.low,
            kline.close,
            kline.volume
            # OHLC
        ]
        cand.append(f)

    return[
        [float(d[2]) for d in cand],
        [float(d[3]) for d in cand],
        [float(d[4]) for d in cand],
        [float(d[5]) for d in cand]
        ]





def heikin_ashi(df):

    HA_Open_Arr = []
    HA_Close = (df['open'] + df['high'] + df['low'] + df['close']) / 4

    for i in range(len(df['open'])):
        # print(i)

        if i == 0:
            HA_Open = df['open'][0]
            HA_Open_Arr.append(HA_Open)

        else:
            HA_Open = (df['open'][i-1] + df['close'][i-1]) / 2
            HA_Open_Arr.append(HA_Open)

    HACLOSE = np.array(HA_Close)
    HAOPEN = np.array(HA_Open_Arr)
    data = np.array([HAOPEN, HACLOSE])
    return data






from m_run.crypto_signals.settings import rest_client
candle = candles('ETHUSDT','15m', rest_client)
candle2 = candles('ETHUSDT','2h', rest_client)

dff =  {'open' : np.array(candle[0]), 'high' : np.array(candle[1]), 'low' : np.array(candle[2]), 'close' : np.array(candle[3])}
dff2 =  {'open' : np.array(candle2[0]), 'high' : np.array(candle2[1]), 'low' : np.array(candle2[2]), 'close' : np.array(candle2[3])}



# slowma = ema.exponential_moving_average(heikin_ashi(dff)[1], 30)
slowma1 = ema.exponential_moving_average(heikin_ashi(dff)[1], 30)
slowma = sma.smoothed_moving_average(heikin_ashi(dff)[1], 30)
fastma = ema.exponential_moving_average(heikin_ashi(dff2)[1], 4)


print(slowma1)
print('Buy : {} \t :\t{} \t>\t {}'.format(fastma[-1] > slowma[-1], fastma[-1], slowma[-1]))
print('Sell : {} \t :\t{} \t<\t {}'.format(fastma[-1] < slowma[-1], fastma[-1], slowma[-1]))




#
#
#
# buylist = []
# selllist = []
# balm = []
# balc = []
# bal = 100
# i = 0
#
# while i < len(candle[0]):
#
#
#
#     if i >= 45:
#         a = heikin_ashi(dff)[1][:i]
#         b = heikin_ashi(dff2)[1][:i]
#
#
#         slowma = ema.exponential_moving_average(heikin_ashi(dff)[1][:i], 30)
#         fastma = ema.exponential_moving_average(heikin_ashi(dff2)[1][:i], 1)
#         if slowma[-1] < fastma[-1] and len(buylist) <= 0:
#             balm.append(bal)
#             print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#             print('Buy  : ')
#             print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#             print()
#             print()
#             print()
#             print()
#
#             bal = bal / candle[3][i]
#             print(bal)
#             print(candle[3][i])
#
#
#             balm.append(bal)
#
#             print(balm)
#             buylist.append('pair')
#             if len(selllist) >= 1:
#
#                 del selllist[:]
#
#         if slowma[-1] > fastma[-1] and len(selllist) <= 0:
#
#             print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#             print('Sell  :  ')
#             print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#             print()
#             print()
#             print()
#             print()
#             bal = bal * candle[3][i]
#             print(bal)
#             print(candle[3][i])
#
#             balc.append(bal)
#             print(bal)
#             selllist.append('pair')
#             if len(buylist) >= 1:
#                 buylist.remove('pair')
#                 del buylist[:]
#
#             print()
#             print()
#
#     i += 1
#
# print(slowma[-104:-97])
# print(fastma[-14])
# print()
# print()
#
#
#
# print(slowma[-96:-89])
# print(fastma[-13])
# print()
# print()
#
#
#
# print(slowma[-88:-81])
# print(fastma[-12])
# print()
# print()
#
#
#
# print(slowma[-80:-73])
# print(fastma[-11])
# print()
# print()
#
#
#
# print(slowma[-72:-65])
# print(fastma[-10])
# print()
# print()
#
#
#
#
#
#
#
#
#
#
# print(slowma[-64:-57])
# print(fastma[-9])
# print()
# print()
# print(slowma[-56:-49])
# print(fastma[-8])
# print()
# print()
# print(slowma[-48:-41])
# print(fastma[-7])
# print()
# print()
# print(slowma[-40:-33])
# print(fastma[-6])
# print()
# print()
# print(slowma[-32:-25])
# print(fastma[-5])
# print()
# print()
# print(slowma[-24:-17])
# print(fastma[-4])
# print()
# print()
# print(slowma[-16:-9])
# print(fastma[-3])
# print()
# print()
# print(slowma[-8:])
# print(fastma[-2])
# print()
# print()
# print(fastma[-14:])
# print(fastma[-1])
# print()
# print()
# print('Buy : {} \t :\t{} \t>\t {}'.format(fastma[-1] > slowma[-1], fastma[-1], slowma[-1]))
# print('Sell : {} \t :\t{} \t<\t {}'.format(fastma[-1] < slowma[-1], fastma[-1], slowma[-1]))