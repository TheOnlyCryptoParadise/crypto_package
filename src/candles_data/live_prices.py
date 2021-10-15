import pandas

import service_config as conf
import requests

def get_live_price_full(exchange: str, currency_pairs: [str]):
    """Gets prices of defined currencies.

        Parameters:
            exchange : str
                exchange name (Binance, Bitbay)
            currency_pairs : [str]
                list of strings performing name of the pair (eg. UDT/STH)
    """
    args = _make_get_price_args(exchange, currency_pairs)
    res = requests.post(conf.CANDLE_DATA_SERVICE + conf.EP_LIVE_PRICES, json=args)

    if res.status_code != 200:
        raise Exception("Some exception occurred while connecting to server."+str(res))
    res = res.json()['data'][0]
    print(pandas.DataFrame(res.json()['data'][0]))
    # price = [x for x.json() in res.json()
    return res

def get_live_price(exchange: str, currency_pairs: [str]):
    full = get_live_price_full(exchange,currency_pairs)

def _make_get_price_args(exchange, pairs):
    args = {"exchanges": [
                {
                "name": exchange,
                "pairs": pairs
                }
            ]
            }
    print(args)
    return args

if __name__ == '__main__':
    get_live_price_full('binance', ['BTC/USDT','DOT/USDT'])