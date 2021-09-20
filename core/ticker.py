from core.client import Public


def ticker(Base, Quote):
    public_client = Public()
    return float(public_client.ticker(base = Base, quote = Quote)['last'])




