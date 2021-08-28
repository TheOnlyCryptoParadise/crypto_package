import config as conf
import requests


def get_candles(exchange: str, currency_pair: str, ticker: str, **kwargs: int):
    """Gets required candles.

        Parameters:
            exchange : str
                exchange name (Binance, Bitbay)
            currency_pair : str
                string performing name of the pair (eg. UDT/STH)
            ticker : str
                i dont know but maybe you knows ;)
            [OPTIONAL] time_start: int
                from what hour you want to get candles # ASK hour?
            [OPTIONAL] time_end: int
                to which hour you want to get candles # ASK hour?
                IMPORTANT: you need to pass both time_start with start_end! You cannot pass only one of them!
            [OPTIONAL] last_n_candles: int
                if you want to get last n candles pass a number of candles to get

    """
    time_start = kwargs.get("time_start")
    time_end = kwargs.get("time_end")
    last_n_candles = kwargs.get("last_n_candles")

    # TODO checking data corectness?
    args = _make_get_candles_args(exchange, currency_pair, ticker, time_start, time_end, last_n_candles)
    candles = requests.get(conf.CANDLE_DATA_SERVICE + conf.EP_CANDLES, args)

    # TODO some operations on candles

    return candles


def _make_get_candles_args(exchange, currency_pair, ticker, time_start, time_end, last_n_candles):
    args = {"exchange": exchange,
            "currency_pair": currency_pair,
            "ticker": ticker,
            }

    if time_start is not None or time_end is not None:  # ASK do we assume that user has to put time_end while he ads time_start?
        _check_time(time_start, time_end)
        args["time_start"] = time_start
        args["time_end"] = time_end

    if last_n_candles is not None:
        args["last_n_candles"] = last_n_candles

    return args


def _check_time(time_start, time_end):
    try:
        time_start + time_end  # check whether one of them is None
    except:
        raise Exception("You have to define both - time_start and time-end values")

    assert time_end > time_start, "time_end has to be after time_start"
