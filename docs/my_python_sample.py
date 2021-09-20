import requests
import math
import pandas as pd
import numpy as np
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import datetime


def xrp():
    urlb = "https://www.bitstamp.net/api/v2/ticker/"
    currency = "xrpusd"
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    responseb = requests.get(urlb + currency, verify=True)
    json_verisi = responseb.json()
    price = json_verisi['last']
    return float(price)


def wma(n):
    data2[:n]
    weights = np.arange(1, n + 1)
    weights = -np.sort(-weights)
    result = np.dot(data2[:n], weights) / weights.sum()
    return result


def wma1(n):
    data2[1:n + 1]
    weights = np.arange(1, n + 1)
    weights = -np.sort(-weights)
    result = np.dot(data2[1:n + 1], weights) / weights.sum()
    return result


def ema(n):
    k = 2 / (n + 1)
    data2[:n]
    result = data2[:n][0] * k + data2[:n - 1].mean() * (1 - k)
    return result

   
def emam(n):
    k = 2 / (n + 1)
    result = MACD * k + data2[:n - 1].mean() * (1 - k)
    return result


while True:

    url = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_XRP_USD/latest?period_id=30MIN&limit=100'
    headers = {'X-CoinAPI-Key': ''}
    response = requests.get(url, headers=headers, verify=True)
    if not response.status_code == 200:
        raise Exception('Status code not 200')
    data = response.json()
    data1 = pd.DataFrame.from_dict(data, orient='columns', dtype=np.float)
    data2 = data1['price_close']

    ot = 0
    keh = 9
    dt = 0.0001
    n2ma = 2 * wma(int(round(keh / 2, 0)))
    nma = wma(int(round(keh)))
    diff = n2ma - nma
    sqn = int(round(math.sqrt(keh), 0))
    n2ma1 = 2 * wma1(int(round(keh / 2, 0)))
    nma1 = wma1(int(round(keh)))
    diff1 = n2ma1 - nma1
    sqn1 = int(round(math.sqrt(keh), 0))
    n1 = np.dot(diff, sqn) / 6
    n2 = np.dot(diff1, sqn) / 6
    confidance = (data2[0] - data2[1]) / data2[1]
    conversionPeriods = 9
    basePeriods = 26
    laggingSpan2Periods = 49
    LS = data2[26]

    conversionLine = (data2[:conversionPeriods].max() + data2[:conversionPeriods].min()) / 2
    baseLine = (data2[:basePeriods].max() + data2[:basePeriods].min()) / 2
    leadLine1 = (conversionLine + baseLine) / 2
    leadLine2 = (data2[:laggingSpan2Periods].max() + data2[:laggingSpan2Periods].min()) / 2

    MACD_Length = 9
    MACD_fastLength = 12
    MACD_slowLength = 26
    ema12 = pd.DataFrame.ewm(data2,span=MACD_fastLength).mean()
    ema26 = pd.DataFrame.ewm(data2,span=MACD_slowLength).mean()
    MACD = ema12 - ema26
    aMACD = pd.DataFrame.ewm(MACD,span=MACD_Length).mean()

    usd_amount = 2000
    xrp = 0

    long = ot == 0 and n1 > n2 and confidance > dt and data2[0] > n2 and leadLine1 > leadLine2 and data1['price_open'][0] < LS and MACD.mean() > aMACD.mean()
    close = ot == 1 and n1 < n2 and data2[0] < n2 and confidance < dt

    if long:
      add = 1
      ot += add
      usd_amount -= usd_amount*0.60
      xrp += (usd_amount*0.60)/data2[0]
      print('*****Buy Condition Met*****', data2[0],datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'), data1['time_close'][0])

    elif close:
      add = 1
      ot -= add
      usd_amount += xrp * data2[0]
      xrp -= xrp
      print('*****Sell Condition Met*****', data2[0],datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'), data1['time_close'][0])

    else:
      print('conditions not met: ', data2[0], datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'), data1['time_close'][0])
    time.sleep(900)
