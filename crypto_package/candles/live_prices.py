import pandas
import requests

from crypto_package.conf import service_config as conf


def get_live_price(exchange: str, currency_pairs: [str]):
    """Gets prices of defined currencies.

        Parameters:
            exchange : str
                exchange name (Binance, Bitbay)
            currency_pairs : [str]
                list of strings performing name of the pair (eg. UDT/STH)

        Returns:
            1. dictionary containing pairs as keys
            2. pandas DataFrame which rows are titled by pair name and columns are value names
    """
    args = _make_get_price_args(exchange, currency_pairs)
    try:
        res = requests.post(conf.CANDLE_DATA_SERVICE + conf.EP_LIVE_PRICES, json=args)
    except requests.ConnectionError as e:
        print("CONNECTION ERROR OCCURRED "+str(e))
        raise e


    if res.status_code != 200:
        print("Some exception occurred while connecting to server."+str(res))
        raise Exception(str(res)+ " "+str(res.reason))

    res = res.json()['data'][0]['data']
    pandas_res = pandas.DataFrame(res).T

    return res, pandas_res


def _make_get_price_args(exchange, pairs):
    args = {"exchanges": [
                {
                "name": exchange,
                "pairs": pairs
                }
            ]
            }
    return args

if __name__ == '__main__':
    get_live_price('binance', ['BTC/USDT','DOT/USDT'])