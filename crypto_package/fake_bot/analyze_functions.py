from datetime import timedelta

import matplotlib.pyplot as plt
from models import Trade, AnalysisResult
import matplotlib.dates as mdates

def plot_balance(res: AnalysisResult):

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

    ax = plt.gca()
    formatter = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)


    locator = mdates.DayLocator()

    # set locator

    ax.xaxis.set_major_locator(locator)


    plt.plot(x_v, y_v)
    plt.show()


def plot_profit(res: AnalysisResult, pair=None): #time in seconds
    # t = res.start_datetime
    x_v=[]

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
    transactions.sort(key=lambda x:x.timestamp)

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
        results = tr_buy_amount.get(trade.amount) if trade.amount in tr_buy_amount else []

        if trade.is_buy:
            tr_buy_amount.update({trade.amount: results.append(trade)})
        else:
            oldest_buy = results.pop(0)
            tr_buy_amount.update({trade.amount: results})
            profit = ((trade.amount*trade.price) - (trade.amount*oldest_buy.price))/(trade.amount*oldest_buy.price)

            y_v.append(profit)
            x_v.append(trade.timestamp)



    ax = plt.gca()
    formatter = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)

    locator = mdates.DayLocator()

    # set locator

    ax.xaxis.set_major_locator(locator)

    plt.plot(x_v, y_v)
    plt.show()
