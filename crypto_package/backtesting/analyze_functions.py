from datetime import datetime
from random import randint
from typing import List


from crypto_package.candles.get_candles import get_candles
from pandas import DataFrame, to_datetime
import plotly.graph_objects as go
from .models import AnalysisResult, Trade


def get_candles_and_plot(exchange: str, pair: str, candle_size: str, time_start: datetime = None,
                         time_end: datetime = None, last_n_candles: int = None, trades: AnalysisResult = None,
                         width: int = 1000, height: int = 600):
    candles, _ = get_candles(exchange, pair, candle_size, last_n_candles=last_n_candles, time_start=time_start,
                                time_end=time_end)

    # candles = candles.rename(columns={"time": "date"})
    # candles["date"] = to_datetime(candles["date"], unit='s')

    plot_candles(candles, trades, pair, width, height)
    # return fig
    return candles


def plot_candles(candles: DataFrame, trades: AnalysisResult = None, pair=None, width: int = 1000, height: int = 650):
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

    if trades is not None:
        res = trades.trades

        if pair is not None:
            res = [t for t in trades.trades if t.pair == pair]

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
    # return fig

def plot_indicators(indicators_df: DataFrame, indicators: List[str], width: int = 1000,
                    height: int = 650, fig_type:str='lines'):  # indicators_df contains columns with indicators and column "date" with datetime
    if "time" in indicators_df.columns:
        indicators_df = indicators_df.rename(columns={"time": "date"})
    if type(indicators_df["date"][0]) is not datetime:
        indicators_df["date"] = to_datetime(indicators_df["date"], unit='s')

    for ind in indicators:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=indicators_df['date'],
            y=indicators_df[ind],
            mode=fig_type,
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

def plot_indicators_on_candles(indicators_df: DataFrame, indicators: List[str], width: int = 1000,
                    height: int = 650):  # indicators_df contains columns with indicators and column "date" with datetime
    if "time" in indicators_df.columns:
        indicators_df = indicators_df.rename(columns={"time": "date"})
    if type(indicators_df["date"][0]) is not datetime:
        indicators_df["date"] = to_datetime(indicators_df["date"], unit='s')

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=indicators_df['date'],
        open=indicators_df['open'],
        high=indicators_df['high'],
        low=indicators_df['low'],
        close=indicators_df['close']))

    for ind in indicators:
        fig.add_trace(go.Scatter(
            x=indicators_df['date'],
            y=indicators_df[ind],
            mode='markers',
            marker=dict(
                color=randint(1,500),
                line_width=2,
                size=7,
            ),
            name=ind,
        ))
    fig.update_layout(
        title="Indicators on candles",
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
    sell_costs = 0
    buy_costs = 0

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

            sell_costs += trade.amount * trade.price
            buy_costs += trade.amount * oldest_buy.price
            profit = (sell_costs - buy_costs) / buy_costs
            # profit = ((trade.amount * trade.price) - (trade.amount * oldest_buy.price)) / (
            #             trade.amount * oldest_buy.price)

            y_v.append(profit)
            x_v.append(trade.timestamp)

    x_v.append(end_datetime)
    y_v.append(profit)

    return x_v, y_v


def plot_profit(trades: AnalysisResult, width: int = 1000, height: int = 650):
    x, y = calculate_profit_from_trades(trades.trades, trades.start_datetime, trades.end_datetime)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        name="profit",
    ))
    fig.update_layout(
        title='BacktestingBots profit',
        xaxis_title="time",
        yaxis_title="value [%]",
        width=width,
        height=height
    )
    fig.show()

    # return fig


def plot_profit_per_pair(trades: AnalysisResult, pairs: List[str] = None, width: int = 1000, height: int = 650):
    pair_trades = {}

    if pairs is None:
        for trade in trades.trades:
            uptrades = pair_trades.get(trade.pair) if trade.pair in pair_trades.keys() else []
            uptrades.append(trade)
            pair_trades.update({trade.pair: uptrades})
    else:
        for trade in trades.trades:
            if trade.pair in pairs:
                uptrades = pair_trades.get(trade.pair) if trade.pair in pair_trades.keys() else []
                uptrades.append(trade)
                pair_trades.update({trade.pair: uptrades})

    fig = go.Figure()
    for pair, transactions in pair_trades.items():
        x, y = calculate_profit_from_trades(transactions, trades.start_datetime, trades.end_datetime)
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            name=str(pair),
        ))

    calc_pairs = [item for item in pair_trades.keys()]
    fig.update_layout(
        title='BacktestingBots profit per pair ' + str(calc_pairs),
        xaxis_title="time",
        yaxis_title="value [%]",
        width=width,
        height=height
    )
    fig.show()

