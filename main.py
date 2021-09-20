from payload.payload import Payload
from datetime import datetime
import time
import settings

def main():

    logic = Payload(
        baseAsset=settings.base_asset,
        quoteAsset=settings.quote_asset,
        settings=settings,
        timeFrame=settings.timeFrame
    )

    while True:

        try:
            if logic.buy_logic():
                logic.sell_logic()

        except Exception as e:
            print(e)
            time.sleep(15)

        while float(datetime.utcnow().strftime("%M.%S")) % settings.tradeCycle != 0:
            time.sleep(1)


if __name__ == '__main__':
    main()
