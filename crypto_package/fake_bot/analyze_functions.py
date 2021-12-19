from datetime import timedelta, datetime
from typing import List

import pandas as pd
import matplotlib.pyplot as plt
from .models import AnalysisResult, Trade


def get_candles_and_plot(exchange: str, pair: str, candle_size: str, time_start: datetime = None,
                         time_end: datetime = None, last_n_candles: int = None, trades: AnalysisResult = None,
                         width: int = 1000, height: int = 600):
    candles, _ = cp.get_candles(exchange, pair, candle_size, last_n_candles=last_n_candles, time_start=time_start,
                                time_end=time_end)

    # candles = candles.rename(columns={"time": "date"})
    # candles["date"] = to_datetime(candles["date"], unit='s')

    fig = plot_candles(candles, trades, width, height)
    # return fig
    return candles


def plot_candles(candles: DataFrame, trades: AnalysisResult = None, width: int = 1000, height: int = 650):
    if "time" in candles.columns:
        candles = candles.rename(columns={"time": "date"})
    if type(candles["date"][0]) is not datetime:
        candles["date"] = to_datetime(candles["date"], unit='s')

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=candles['date'],
        open=candles['open'],
        high=candles['high'],
        low=candles['low'],
        close=candles['close']))

    if trades != None:
        res = trades.trades
        buy_trades_price = [tr.price for tr in res if tr.is_buy]
        buy_trades_time = [tr.timestamp for tr in res if tr.is_buy]

        sell_trades_price = [tr.price for tr in res if not tr.is_buy]
        sell_trades_time = [tr.timestamp for tr in res if not tr.is_buy]

        fig.add_trace(go.Scatter(
            x=buy_trades_time,
            y=buy_trades_price,
            mode='markers',
            name='buy trades',
            marker_symbol='diamond',
            marker=dict(
                color='blue',
                line_width=2,
                size=7,

            )
        ))

        fig.add_trace(go.Scatter(
            x=sell_trades_time,
            y=sell_trades_price,
            mode='markers',
            name='sell trades',
            marker_symbol='square',
            marker=dict(
                color='yellow',
                line_width=2,
                size=7
            )
        ))

    fig.update_layout(
        title="Candles",
        xaxis_title="time",
        yaxis_title="price",
        width=width,
        height=height
    )

    fig.show()

    def plot_indicators(indicators_df: DataFrame, indicators: List[str], width: int = 1000,
                        height: int = 650):  # indicators_df contains columns with indicators and column "date" with datetime
        if "time" in indicators_df.columns:
            indicators_df = indicators_df.rename(columns={"time": "date"})
        if type(indicators_df["date"][0]) is not datetime:
            indicators_df["date"] = to_datetime(indicators_df["date"], unit='s')

        for ind in indicators:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=indicators_df['date'],
                y=indicators_df[ind],
                mode='lines',
                name=ind,
            ))
            fig.update_layout(
                title=ind,
                xaxis_title="time",
                yaxis_title="value",
                width=width,
                height=height
            )
            fig.show()


def calculate_profit_from_trades(transactions: List[Trade], start_datetime, end_datetime):
    transactions.sort(key=lambda x: x.timestamp)
    tr_buy_amount = {}
    start = 0
    end = len(transactions)
    profit = 0

    x_v = [start_datetime]
    y_v = [profit]

    for trade_id in range(start, end):
        trade = transactions[trade_id]
        results = []
        if trade.amount in tr_buy_amount.keys():
            results = tr_buy_amount.get(trade.amount)

        if trade.is_buy:
            if len(results) == 0:
                results = [trade]
            else:
                results.append(trade)
            tr_buy_amount.update({trade.amount: results})
        else:
            oldest_buy = results.pop(0)
            if len(results) > 0:
                tr_buy_amount.update({trade.amount: results})
            else:
                tr_buy_amount.pop(trade.amount)

            profit = ((trade.amount * trade.price) - (trade.amount * oldest_buy.price)) / (
                    trade.amount * oldest_buy.price)

            y_v.append(profit)
            x_v.append(trade.timestamp)

        x_v.append(end_datetime)
        y_v.append(profit)

    return x_v, y_v

def calculate_block_profit(transactions: List[Trade], start_datetime, end_datetime, days=0, hours=0, minutes=0,
                           seconds=0):
    t = start_datetime
    x_v = []

    if hours == minutes == seconds == days == 0:
        print("Define hours, minutes, seconds, or days")
        return -1;

    while t <= end_datetime:
        x_v.append(t)
        t = t + timedelta(hours=hours, minutes=minutes, seconds=seconds)

    # sort by time
    transactions.sort(key=lambda x: x.timestamp)

    # divide for time blocks
    trades_in_time_ids = [0]
    last = 0
    for i in range(1, len(x_v)):
        end = x_v[i]
        while last < len(transactions) and transactions[last].timestamp <= end:
            last += 1
        trades_in_time_ids.append(last)

    tr_buy_amount = {}
    y_v = [0]
    x_ids = []
    i = 0
    # calc profit for blocks
    block_profit_sum = 0
    block_buy_sum = 0
    for end_id in range(1, len(trades_in_time_ids)):
        start = trades_in_time_ids[end_id - 1]
        end = trades_in_time_ids[end_id]

        for trade_id in range(start, end):
            trade = transactions[trade_id]
            results = []
            if trade.amount in tr_buy_amount.keys():
                results = tr_buy_amount.get(trade.amount)

            if trade.is_buy:
                if len(results) == 0:
                    results = [trade]
                else:
                    results.append(trade)
                tr_buy_amount.update({trade.amount: results})
            else:
                oldest_buy = results.pop(0)
                if len(results) > 0:
                    tr_buy_amount.update({trade.amount: results})
                else:
                    tr_buy_amount.pop(trade.amount)

                block_profit_sum += (trade.amount * trade.price)
                block_buy_sum += trade.amount * oldest_buy.price

        if block_buy_sum != 0:
            y_v.append((block_profit_sum - block_buy_sum) / block_buy_sum)
        else:
            y_v.append(0)

        # x_ids.append(datetime.fromtimestamp(int((transactions[start].timestamp.timestamp()+transactions[end-1].timestamp.timestamp())/2)))
        x_ids.append(x_v[i] + timedelta(hours=hours / 2, minutes=minutes / 2, seconds=seconds / 2))
        i += 1

    return x_ids, y_v

def plot_profit(trades: AnalysisResult, width: int = 1000, height: int = 650, days=None):
    x, y = calculate_block_profit(trades.trades, trades.start_datetime, trades.end_datetime, days=days)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        name="profit",
    ))
    fig.update_layout(
        title='BacktestingBots profit',
        xaxis_title="time",
        yaxis_title="value",
        width=width,
        height=height
    )
    fig.show()

def plot_profit_per_pair(trades: AnalysisResult, width: int = 1000, height: int = 650, pairs: List[str] = None):
    pair_trades = {}
    if pairs == None:
        for trade in trades.trades:
            pair_trades[trade.pair].append(trade)
    else:
        for trade in trades.trades:
            if trade.pair in pairs:
                uptrades = pair_trades[trade.pair] if trade.pair in pait_trades.keys() else []
                pair_trades.update({trade.pair: uptrades})
    print(pair_trades)

    fig = go.Figure()
    for pair, transactions in pair_trades.items():
        x, y = calculate_profit_from_trades(trades.trades, trades.start_datetime, trades.end_datetime)
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            name=str(pair),
        ))
    fig.update_layout(
        title='BacktestingBots profit per pair',
        xaxis_title="time",
        yaxis_title="value",
        width=width,
        height=height
    )
    fig.show()

