from datetime import timedelta, datetime
from typing import List

import pandas as pd
import matplotlib.pyplot as plt
from models import AnalysisResult


def generate_balance(res: AnalysisResult):
    x_v = [ t.timestamp for t in res.trades]
    x_v.insert(0, res.start_datetime)
    y_v = [res.start_balance]
    balance = res.start_balance
    for t in res.trades:
        if t.is_buy:
            balance -= t.price * t.amount
        else:
            balance += t.price * t.amount
        y_v.append(balance)
    return x_v, y_v

def plot_balance(res: AnalysisResult):
    x_v, y_v = generate_balance(res)
    idx = pd.to_datetime(x_v)
    df = pd.Series(y_v, index=idx)
    df.plot()
    plt.title("Bot's balance")
    plt.show()
    # plt.savefig("balance_graph.png")


def generate_profit(res:AnalysisResult, pair:None):
    # t = res.start_datetime
    x_v = []

    # while t != res.end_datetime:
    #     x_v.append(t)
    #     t = t + timedelta(seconds=time_period)
    #
    # x_v.append(t)
    # print(x_v)

    transactions = res.trades
    if pair is not None:
        transactions = [tr for tr in res.trades if tr.pair in pair]

    # sort by time
    transactions.sort(key=lambda x: x.timestamp)

    # # divide for time blocks
    # trades_in_time_ids = [0]
    # last = 0
    # for i in range(1,len(x_v)):
    #     end = x_v[i]
    #     while transactions[last].timestamp < end:
    #         last+=1
    #     trades_in_time_ids.append(last)

    tr_buy_amount = {}

    # calc profit for blocks
    # for end_id in range(1,len(trades_in_time_ids)):
    #     start = trades_in_time_ids[end_id-1]
    #     end = trades_in_time_ids[end_id]

    start = 0
    end = len(transactions)
    x_v = []
    y_v = []

    profit = 0

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

    return x_v, y_v

def generate_block_profit(res:AnalysisResult, seconds=60, minutes=0, hours=0,  pair=None):
    t = res.start_datetime
    x_v = []

    while t < res.end_datetime:
        x_v.append(t)
        t = t + timedelta(hours=hours, minutes=minutes, seconds=seconds)

    # x_v.append(t)
    print(x_v)

    transactions = res.trades
    if pair is not None:
        transactions = [tr for tr in res.trades if tr.pair in pair]

    # sort by time
    transactions.sort(key=lambda x: x.timestamp)

    # divide for time blocks
    trades_in_time_ids = [0]
    last = 0
    for i in range(1,len(x_v)):
        end = x_v[i]
        while last < len(transactions) and transactions[last].timestamp < end:
            last+=1
        trades_in_time_ids.append(last)

    tr_buy_amount = {}
    y_v = []
    x_ids = []
    i=0
    # calc profit for blocks
    for end_id in range(1,len(trades_in_time_ids)):
        start = trades_in_time_ids[end_id-1]
        end = trades_in_time_ids[end_id]
        block_profit_sum = 0
        block_buy_sum = 0

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
            y_v.append((block_profit_sum-block_buy_sum)/block_buy_sum)
        else:
            y_v.append(0)

        # x_ids.append(datetime.fromtimestamp(int((transactions[start].timestamp.timestamp()+transactions[end-1].timestamp.timestamp())/2)))
        x_ids.append(x_v[i]+timedelta(hours=hours/2, minutes=minutes/2, seconds=seconds/2))
        i+=1

    return x_ids, y_v

def plot_profit(res: AnalysisResult, pair=None): #time in seconds
    (x_v, y_v) = generate_profit(res, pair)

    idx = pd.to_datetime(x_v)
    # idx = pd.Series(x_v)
    df = pd.Series(y_v, index=idx)
    df.plot()
    plt.title("Bot's profit")
    plt.show()
    # plt.savefig("profit_graph.png")

def plot_block_profit(res: AnalysisResult, seconds=0, minutes=0, hours=0,  pair=None): #time in seconds
    (x_v, y_v) = generate_block_profit(res, seconds, minutes, hours, pair)

    print(x_v)
    print(y_v)
    # idx = pd.to_datetime(x_v)
    idx = pd.Series(x_v)
    df = pd.Series(y_v, index=idx)
    df.plot()
    plt.title("Bot's profit")
    plt.show()
    # plt.savefig("profit_graph.png")

def plot_pairs_profit(res: AnalysisResult, pairs:List, seconds=0, minutes=0, hours=1): #time in seconds
    # fig,ax = plt.subplots()
    data = {}
    idx = []
    for pair in pairs:
        (x_v, y_v) = generate_block_profit(res, seconds, minutes, hours, pair)
        # ax.plot(x_v, y_v, label=str(pair))
        idx = pd.to_datetime(x_v)
        data[pair] = y_v

    print(data)

    # print(idx)
    # df = pd.Series(y_v, index=idx,label=pair)
    df = pd.DataFrame(data=data, index=idx)
    print(df)
    df.plot(label=pair)
    plt.plot(idx, y_v, label=str(pair))

    # ax.legend(loc='best')
    plt.title("Profit for each pair")
    plt.show()
    # plt.savefig("profit_graph.png")
