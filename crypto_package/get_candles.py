from datetime import datetime
from crypto_package.conf import service_config as conf
import requests
from time import time
import pandas


def get_candles(exchange: str, currency_pair: str, ticker: str, time_start=None, time_end=None, last_n_candles=None):
    """Gets required candles.

        Parameters:
            exchange : str
                exchange name (Binance, Bitbay)
            currency_pair : str
                string performing name of the pair (eg. UDT/STH)
            ticker : str
                i dont know but maybe you knows ;)
            time_start: datetime [OPTIONAL]
                from what time you want to get candles (time is a timestamp)
            time_end: datetime [OPTIONAL]
                to which time you want to get candles (time is a timestamp)
                IMPORTANT: If you pass time_start and don't pass time_end value, time_end would be current time
            last_n_candles: int [OPTIONAL]
                if you want to get last n candles pass a number of candles to get

        Returns:
            pandas DataFrame with candles data
    """

    args = _make_get_candles_args(exchange, currency_pair, ticker, time_start, time_end, last_n_candles)
    try:
        res = requests.get(conf.CANDLE_DATA_SERVICE + conf.EP_CANDLES, args)
    except requests.ConnectionError as e:
        print("CONNECTION ERROR OCCURRED "+str(e))
        return None

    if res.status_code != 200:
        print("Some exception occurred while connecting to server."+str(res))
        return None

    candles = pandas.DataFrame(res.json()['data'])

    return candles


def _make_get_candles_args(exchange, currency_pair, ticker, time_start, time_end, last_n_candles):
    args = {"exchange": exchange,
            "currency_pair": currency_pair,
            "candle_size": ticker,
            }

    args = _add_time_values(args, time_start, time_end)
    args = _add_last_candles_values(args, last_n_candles)

    return args


def _add_time_values(args, time_start, time_end):
    if time_start is not None:
        if type(time_start) is not datetime:  # do we check whether user gave int value or are we adults? xd
            raise TypeError("time_start has to be datetime")
        if time_end is not None and type(time_end) is not datetime:
            raise TypeError("time_start has to be datetime")

        args["time_start"] = time_start.timestamp()
        args["time_end"] = _check_time(time_start, time_end) if time_end is not None else time()

    elif time_start is None and time_end is not None:
        raise ValueError("you cannot pass time_end without time_start")

    return args


def _check_time(time_start, time_end):
    assert time_end.timestamp() > time_start.timestamp(), "time_end has to be after time_start"
    return time_end.timestamp()


def _add_last_candles_values(args, last_n_candles):
    if last_n_candles is not None:
        if type(last_n_candles) is not int:
            raise TypeError("last_n_candles has to be int")
        args["last_n_candles"] = last_n_candles

    return args
