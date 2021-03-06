import logging
from datetime import datetime, timedelta
from random import randint

# from pprint import pprint
# from numpy import double
import yaml

import crypto_package
# from .analyze_functions import plot_profit, plot_pairs_profit, plot_block_profit
# from crypto_package.backtesting import plot_profit
from crypto_package.backtesting.models import Trade, AnalysisResult


# import talib.abstract as ta


def candle_size_to_seconds(cs):
    num = int(cs[:-1])
    s = cs[-1]
    if s == "m":
        return num * 60
    elif s == "h":
        return num * 3600
    elif s == "d":
        return num * 3600 * 24
    elif s == "w":
        return num * 3600 * 24 * 7
    elif s == "M":
        return num * 3600 * 24 * 30


class BacktestingBot():
    def __init__(self, config_path):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        self._logger.info("starting")
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f.read())

    def _reset_state(self, start_balance):
        self._current_balance = start_balance
        self._start_balance = start_balance
        self._open_trades = {p:[] for p in self.config['currency_pairs']}
        self._all_trades = []
        self._buy_signals = []
        self._sell_signals = []

    def test_strategy(self, calc_ind_f, buy_sig_f, sell_sig_f, start_balance=1000, time_start=None, time_end=None, last_n_days=None):
        self._reset_state(start_balance)
        if last_n_days and not time_end and not time_start:
            time_end = datetime.now()
            time_start = time_end - timedelta(days=last_n_days)
        elif not time_end and time_start:
            time_end = datetime.now()
            if type(time_start) is str:
                time_start = datetime.fromisoformat(time_start)
            elif type(time_start) is not datetime:
                raise ValueError("time_start has to be a sting or a datetime")
        # elif time_end and time_start:
        #     if type(time_start) is str:
        #         time_start = datetime.fromisoformat(time_start)
        #     elif type(time_start) is not datetime:
        #         raise ValueError("time_start has to be a sting or a datetime")
        #     if type(time_end) is str:
        #         time_end = datetime.fromisoformat(time_end)
        #     elif type(time_end) is not datetime:
        #         raise ValueError("time_end has to be a sting or a datetime")
        else:
            raise ValueError("You need to provide at least time_start or last_n_days")

        time_start = time_start - timedelta(seconds=self.config['last_n_candles']*candle_size_to_seconds(self.config['timeframe'])) # TODO check

        all_candles = {}
        for pair in self.config['currency_pairs']:
            all_candles[pair] = crypto_package.get_candles(self.config['exchange'], pair, self.config['timeframe'], time_start, time_end)[0]

        self._logger.debug(f"download necessary candles: " + str({k: v.shape for k, v in all_candles.items()}))
        no_candles = all_candles[self.config['currency_pairs'][0]].shape[0]

        for i in range(self.config['last_n_candles'], no_candles):
            for k, v in all_candles.items():
                candles_portion = v.iloc[0:i]
                self._logger.debug("Candles range: "+str(i-self.config['last_n_candles'])+ " to "+ str(i)) #TODO check
                self._process_candles(calc_ind_f, buy_sig_f, sell_sig_f, k, candles_portion)
        return AnalysisResult(trades=self._all_trades, start_balance=self._start_balance, end_balance=self._current_balance, start_datetime=time_start, end_datetime=time_end,
                              sell_signals=self._sell_signals, buy_signals = self._buy_signals)
        # return {"trades": self._all_trades, "balance": self._current_balance, "start_balance": self._start_balance}


    def _process_candles(self, calc_ind_f, buy_sig_f, sell_sig_f, currency_pair, df):
        self._logger.debug(df)
        indicators = calc_ind_f(df)
        if buy_sig_f(indicators):
            self._buy_signals.append((df.iloc[-1]['close'], datetime.fromtimestamp(df.iloc[-1]['time'])))

            amount = self.config['transaction_amount'] / df.iloc[-1]['close']
            if self.config['max_open_trades'] > len(self._open_trades):
                trade = Trade(is_buy=True, pair=currency_pair, amount=amount, price=df.iloc[-1]['close'], timestamp=datetime.fromtimestamp(df.iloc[-1]['time']))
                self._try_buy(trade)

        if sell_sig_f(indicators):
            self._sell_signals.append((df.iloc[-1]['close'], datetime.fromtimestamp(df.iloc[-1]['time'])))
            if self.config['sell_all']:
                for btrade in self._open_trades[currency_pair]:
                    self._sell_open_trade(btrade, df.iloc[-1]['close'], timestamp=datetime.fromtimestamp(df.iloc[-1]['time']))
            elif len(self._open_trades[currency_pair])>0:
                buy_trade = self._open_trades[currency_pair][0]
                self._sell_open_trade(buy_trade, df.iloc[-1]['close'],
                                      timestamp=datetime.fromtimestamp(df.iloc[-1]['time']))


    def _try_buy(self, trade):
        if self._current_balance >= trade.amount*trade.price:
            self._logger.debug(f"bought {trade.pair} price:{trade.price} amount:{trade.amount} value:{trade.amount*trade.price}")
            self._current_balance -= trade.amount*trade.price
            self._open_trades[trade.pair].append(trade)
            self._all_trades.append(trade)
        else:
            self._logger.debug("insufficient balance")


    def _sell(self, trade):
        self._logger.debug("sold  {trade.pair} price:{trade.price} amount:{trade.amount} value:{trade.amount*trade.price}")
        self._all_trades.append(trade)
        self._current_balance += trade.amount * trade.price

    def _sell_open_trade(self, open_trade, price, timestamp):
        trade = Trade(is_buy=False, pair=open_trade.pair, amount=open_trade.amount, price=price, timestamp=timestamp)
        self._sell(trade)
        self._open_trades[open_trade.pair].remove(open_trade)




if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    #
    # def calc_indicators_patterns_1(candles):
    #     candles['eng'] = ta.CDLENGULFING(candles)
    #     candles['hammer'] = ta.CDLHAMMER(candles)
    #     candles['invhammer'] = ta.CDLINVERTEDHAMMER(candles)
    #     candles['morning'] = ta.CDLMORNINGSTAR(candles)
    #
    #     candles['hang'] = ta.CDLHANGINGMAN(candles)
    #     candles['shoot'] = ta.CDLSHOOTINGSTAR(candles)
    #     candles['evening'] = ta.CDLEVENINGSTAR(candles)
    #
    #     return candles
    #
    #
    # def check_buy_signals_patterns_1(indicators):
    #     buy = False
    #
    #     if indicators.iloc[-2]['eng'] == 100 and indicators.iloc[-1]['eng'] == 100:
    #         buy = True
    #     elif (indicators.iloc[-1]['hammer'] == 100 and
    #           indicators.iloc[-1]['open'] < indicators.iloc[-1]['close'] and  # zielona
    #           indicators.iloc[-2]['open'] > indicators.iloc[-2]['close'] and  # czerwona
    #           indicators.iloc[-3]['open'] > indicators.iloc[-3]['close']):  # czerwona
    #         buy = True
    #     elif (indicators.iloc[-1]['morning'] == 100 and
    #           indicators.iloc[-2]['open'] < indicators.iloc[-2]['close']):  # zielona
    #         buy = True
    #     elif indicators.iloc[-1]['invhammer'] == 100:
    #         buy = True
    #
    #     return buy
    #
    #
    # def check_sell_signals_patterns_1(indicators):
    #     sell = False
    #
    #     if (indicators.iloc[-1]['hang'] == -100 and
    #             indicators.iloc[-2]['open'] < indicators.iloc[-2]['close'] and  # zielona
    #             indicators.iloc[-3]['open'] < indicators.iloc[-3]['close']):  # zielona
    #         sell = True
    #     elif (indicators.iloc[-2]['eng'] == -100 and
    #           indicators.iloc[-1]['open'] > indicators.iloc[-1]['close'] and  # czerwona
    #           indicators.iloc[-3]['open'] < indicators.iloc[-3]['close'] and  # zielona
    #           indicators.iloc[-4]['open'] < indicators.iloc[-4]['close']):  # zielona
    #         sell = True
    #     elif (indicators.iloc[-2]['evening'] == -100 and
    #           indicators.iloc[-1]['open'] > indicators.iloc[-1]['close']):
    #         sell = True
    #
    #     return sell

    # def calc_ind(dataframe):
    #     # dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
    #     return dataframe
    #
    # def buy_sig(dataframe):
    #     r = randint(0,10)
    #     if r>8:
    #     # if dataframe.iloc[-1]['rsi'] > 70:
    #         return True
    #     else:
    #         return False
    #
    # def sell_sig(dataframe):
    #     # if dataframe.iloc[-1]['rsi'] < 30:
    #     r = randint(0, 10)
    #     if r > 1:
    #         return True
    #     else:
    #         return False
    #
    # # fbot = FakeBot("../work/bot1/config.yml")
    # fbot = BacktestingBot("C:/Users/natalia/Desktop/studia/inzynierka/backend/bot/bot_app/user_files/example_config.yml")
    # res = fbot.test_strategy(calc_ind, buy_sig, sell_sig, last_n_days=3)
    # # plot_balance(res)
    # plot_profit(res)
    # plot_pairs_profit(res,fbot.config["currency_pairs"] )
    # plot_block_profit(res, hours=1)

