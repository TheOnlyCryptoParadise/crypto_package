# Crypto package

### Available functionality:
* **get_candles**(exchange: str, currency_pair: str, ticker: str, time_start=None, time_end=None, last_n_candles=None):
```
Gets required candles.
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
```

* **get_live_price**(exchange: str, currency_pairs: [str]):
```
Gets prices of defined currencies.

        Parameters:
            exchange : str
                exchange name (Binance, Bitbay)
            currency_pairs : [str]
                list of strings performing name of the pair (eg. UDT/STH)

        Returns:
            1. dictionary containing pairs as keys
            2. pandas DataFrame which rows are titled by pair name and columns are value names
```