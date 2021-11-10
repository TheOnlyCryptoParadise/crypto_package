import requests
from crypto_package.conf import service_config as conf


def subscribe_on_topics(currency_pairs:[str], ticker:str, exchange:str):
    args = _make_sub_args(currency_pairs, ticker, exchange)
    res = requests.post(conf.CANDLE_DATA_SERVICE + conf.EP_SUBSCRIBE, json=args)

    if res.status_code != 200:
        raise Exception("Some exception occurred while connecting to server." + str(res))

    return True


def unsubscribe_on_topics(currency_pairs: [str], ticker: str, exchange: str):
    args = _make_sub_args(currency_pairs, ticker, exchange)
    res = requests.post(conf.CANDLE_DATA_SERVICE + conf.EP_UNSUBSCRIBE, json=args)

    if res.status_code != 200:
        raise Exception("Some exception occurred while connecting to server." + str(res))

    return True


def _make_sub_args(currency_pairs: [str], ticker: str, exchange: str):
    return {'exchanges': {
        exchange: {
            ticker: currency_pairs
        }
    }
    }
