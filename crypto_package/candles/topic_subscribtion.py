import requests

from crypto_package.conf import service_config as conf


def subscribe_on_topics(currency_pairs:[str], ticker:str, exchange:str):
    args = _make_sub_args(currency_pairs, ticker, exchange)
    try:
        res = requests.post(conf.CANDLE_DATA_SERVICE + conf.EP_SUBSCRIBE, json=args)
    except requests.ConnectionError as e:
        print("CONNECTION ERROR OCCURRED "+str(e))
        return False

    if res.status_code != 200:
        print("Some exception occurred while connecting to server." + str(res))
        return False

    return True


def unsubscribe_on_topics(currency_pairs: [str], ticker: str, exchange: str):
    args = _make_sub_args(currency_pairs, ticker, exchange)
    try:
        res = requests.post(conf.CANDLE_DATA_SERVICE + conf.EP_UNSUBSCRIBE, json=args)
    except requests.ConnectionError as e:
        print("CONNECTION ERROR OCCURRED "+str(e))
        return False

    if res.status_code != 200:
        print("Some exception occurred while connecting to server." + str(res))
        return False

    return True


def _make_sub_args(currency_pairs: [str], ticker: str, exchange: str):
    return {'exchanges': {
        exchange: {
            ticker: currency_pairs
        }
    }
    }
