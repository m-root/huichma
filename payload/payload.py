import time
from datetime import datetime

from engine import trading_logic
from core import ticker, client


####################################
#              PAYLOAD             #
####################################

class Payload(object):

    def __init__(self, baseAsset=None, quoteAsset=None, settings=None, timeFrame=None):
        self.settings = settings
        self.baseAsset = baseAsset
        self.quoteAsset = quoteAsset
        self.pair = self.baseAsset + self.quoteAsset
        self.timeFrame = timeFrame
        self.rest_client = settings.rest_client
        self.publicClient = client.Public()
        self.tradingInfo = self.publicClient.trading_pairs_info()
        #print('===================================')
        #print(
            #client.Public().trading_pairs_info()
            #[g['minimum_order'] for g in client.Public().trading_pairs_info() if g['url_symbol'] == self.baseAsset + self.quoteAsset]

        #)
        #print(self.baseAsset + self.quoteAsset)
        #print(float([g['minimum_order'] for g in self.tradingInfo if
                                      #g['url_symbol'] == (self.baseAsset + self.quoteAsset).lower()][0][:-3]))
        # print('===================================')
        self.minimumTradeAmt = float([g['minimum_order'] for g in self.tradingInfo if
                                      g['url_symbol'] == (self.baseAsset + self.quoteAsset).lower()][0][:-3])
        self.entry_price = []

    def buy_logic(self):
        '''

        ====== ENTRY =======
        longCondition = n1>n2 and
        strategy.opentrades<ot Open Trades is True
        confidence>dt
        close>n2
        leadLine1>leadLine2
        open<LS
        MACD>aMACD
        :return:
        '''
        print(trading_logic.hullMaLogic(
                basePair=self.baseAsset,
                quotePair=self.quoteAsset,
                timeFrame=self.timeFrame,
                hullPeriod1=self.settings.hullPeriod1,
                hullPeriod2=self.settings.hullPeriod2))

        print(
                trading_logic.ichimokuLogic(
                    basePair=self.baseAsset,
                    quotePair=self.quoteAsset,
                    timeFrame=self.timeFrame,
                    leadLine1Period=self.settings.leadLine1Period,
                    leadLine2Period=self.settings.leadLine2Period)
               )


        print('macd')

        print(
                trading_logic.macdLogic(
                    basePair=self.baseAsset,
                    quotePair=self.quoteAsset,
                    timeFrame=self.timeFrame,
                    shortPeriod=self.settings.MACD_fastLength,
                    longPeriod=self.settings.MACD_slowLength,
                    MacdPeriod=self.settings.MacdPeriod
                ))
        print(trading_logic.hullMaLogic(
                basePair=self.baseAsset,
                quotePair=self.quoteAsset,
                timeFrame=self.timeFrame,
                hullPeriod1=self.settings.hullPeriod1,
                hullPeriod2=self.settings.hullPeriod2) and \
                trading_logic.ichimokuLogic(
                    basePair=self.baseAsset,
                    quotePair=self.quoteAsset,
                    timeFrame=self.timeFrame,
                    leadLine1Period=self.settings.leadLine1Period,
                    leadLine2Period=self.settings.leadLine2Period) and \
                trading_logic.macdLogic(
                    basePair=self.baseAsset,
                    quotePair=self.quoteAsset,
                    timeFrame=self.timeFrame,
                    shortPeriod=self.settings.MACD_fastLength,
                    longPeriod=self.settings.MACD_slowLength,
                    MacdPeriod=self.settings.MacdPeriod
                ))



        if trading_logic.hullMaLogic(
                basePair=self.baseAsset,
                quotePair=self.quoteAsset,
                timeFrame=self.timeFrame,
                hullPeriod1=self.settings.hullPeriod1,
                hullPeriod2=self.settings.hullPeriod2) and \
                trading_logic.ichimokuLogic(
                    basePair=self.baseAsset,
                    quotePair=self.quoteAsset,
                    timeFrame=self.timeFrame,
                    leadLine1Period=self.settings.leadLine1Period,
                    leadLine2Period=self.settings.leadLine2Period) and \
                trading_logic.macdLogic(
                    basePair=self.baseAsset,
                    quotePair=self.quoteAsset,
                    timeFrame=self.timeFrame,
                    shortPeriod=self.settings.MACD_fastLength,
                    longPeriod=self.settings.MACD_slowLength,
                    MacdPeriod=self.settings.MacdPeriod
                ):

            if self.settings.trade:

                balance = self.rest_client.account_balance(base=self.baseAsset, quote=self.quoteAsset)
                '''
                Check if the amount is enough to execute a trade            
                '''
                if balance > self.minimumTradeAmt:
                    self.entry_price = ticker.ticker(Base=self.baseAsset, Quote=self.quoteAsset)
                    self.rest_client.buy_market_order(
                        amount=self.settings.buyAmount,
                        base=self.settings.base,
                        quote=self.settings.quote
                    )
                    print('*****Buy Condition Met*****', ticker.ticker(Base=self.baseAsset, Quote=self.quoteAsset),
                          datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'),
                          )
                    return True

            else:
                print('conditions not met: ', ticker.ticker(Base=self.baseAsset, Quote=self.quoteAsset),
                      datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))
                return False

        else:
            print('conditions not met: ', ticker.ticker(Base=self.baseAsset, Quote=self.quoteAsset),
                  datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))
            return False

    ####################################
    #          SELL ENTRY LOGIC        #
    ####################################
    def sell_logic(self):

        while not (ticker.ticker(Base=self.baseAsset, Quote=self.quoteAsset) <= self.entry_price[0] - \
                   self.settings.Stop_Loss or \
                   ticker.ticker(Base=self.baseAsset, Quote=self.quoteAsset) >= self.entry_price[0] + \
                   self.settings.Target_Point):
            print('*****Sell Condition Not Yet Met*****', ticker.ticker(Base=self.baseAsset, Quote=self.quoteAsset),
                  datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))

            if ticker.ticker(Base=self.baseAsset, Quote=self.quoteAsset) <= self.entry_price[0] - \
                    self.settings.Stop_Loss or \
                    ticker.ticker(Base=self.baseAsset, Quote=self.quoteAsset) >= self.entry_price[0] + \
                    self.settings.Target_Point:
                self.rest_client.sell_market_order(
                    amount=self.settings.sellAmount,
                    base=self.settings.base,
                    quote=self.settings.quote
                )
                print('*****Sell Condition Met*****', ticker.ticker(Base=self.baseAsset, Quote=self.quoteAsset),
                      datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))


            time.sleep(self.settings.sellSleepTime)






