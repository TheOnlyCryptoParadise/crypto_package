import service_config as conf
import requests

def get_live_price(exchange: str, currency_pairs: [str]):
    """Gets prices of defined currencies.

        Parameters:
            exchange : str
                exchange name (Binance, Bitbay)
            currency_pairs : [str]
                list of strings performing name of the pair (eg. UDT/STH)
    """
    args = _make_get_price_args(exchange, currency_pairs)
    res = requests.post(conf.CANDLE_DATA_SERVICE + conf.EP_LIVE_PRICES, args)

    if res.status_code != 200:
        raise Exception("Some exception occurred while connecting to server."+str(res))
    print(res.text)
    # price = [x for x.json() in res.json()
    return res



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
    get_live_price('binance', ['BTC/USDT','BTC/USDT'])