from pyti import hull_moving_average as hma, \
    ichimoku_cloud as icloud, \
    moving_average_convergence_divergence as macd, \
    exponential_moving_average as ema

from core.candle import klines

def hullMa(basePair, quotePair, timeFrame, hullPeriod):
    return hma.hull_moving_average(
        data=klines(
            base_pair=basePair,
            cross_pair=quotePair,
            period=timeFrame)[4],
        period=hullPeriod
    )


def hullMaLogic(basePair, quotePair, timeFrame, hullPeriod1, hullPeriod2):
    print('Into Hull Ma')
    print( hullMa(basePair, quotePair, timeFrame, hullPeriod1)[-1] > hullMa(basePair, quotePair, timeFrame, hullPeriod2)[
        -1])
    return hullMa(basePair, quotePair, timeFrame, hullPeriod1)[-1] > hullMa(basePair, quotePair, timeFrame, hullPeriod2)[
        -1]



def ichimoku(basePair, quotePair, timeFrame, leadLine1Period, leadLine2Period):
    print('for Ich')
    Closedata = klines(
            base_pair=basePair,
            cross_pair=quotePair,
            period=timeFrame)[4]

    leadLine1 = icloud.tenkansen(
        data=Closedata,
        period=leadLine1Period)  # TenkanSen (Conversion Line)

    leadLine2 = icloud.senkou_b(
        data=Closedata,
        period=leadLine2Period)  # Senkou B (Leading Span B)
    return [leadLine1[-1], leadLine2[-1]]


def ichimokuLogic(basePair, quotePair, timeFrame, leadLine1Period, leadLine2Period):
    data = ichimoku(basePair, quotePair, timeFrame, leadLine1Period, leadLine2Period)
    print(data)
    return data[0] > data[1]


def macD(basePair, quotePair, timeFrame, shortPeriod, longPeriod):
    print('for macd')
    return macd.moving_average_convergence_divergence(
        data=klines(
            base_pair=basePair,
            cross_pair=quotePair,
            period=timeFrame)[4],
        short_period=shortPeriod,
        long_period=longPeriod
    )


def macdLogic(basePair, quotePair, timeFrame, shortPeriod, longPeriod, MacdPeriod):
    MACD = macD(basePair, quotePair, timeFrame, shortPeriod, longPeriod)
    aMACD = ema.exponential_moving_average(data=MACD, period=MacdPeriod)
    return MACD[-1] > aMACD[-1]
