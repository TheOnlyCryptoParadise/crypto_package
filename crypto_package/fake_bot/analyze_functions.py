# from datetime import timedelta
#
# import matplotlib.pyplot as plt
# from models import Trade, AnalysisResult
# import matplotlib.dates as mdates
#
# def plot_balance(res: AnalysisResult):
#
#     x_v = [ t.timestamp for t in res.trades]
#     x_v.insert(0, res.start_datetime)
#     y_v = [res.start_balance]
#     balance = res.start_balance
#     for t in res.trades:
#         if t.is_buy:
#             balance -= t.price * t.amount
#         else:
#             balance += t.price * t.amount
#         y_v.append(balance)
#
#     ax = plt.gca()
#     formatter = mdates.DateFormatter("%Y-%m-%d")
#     ax.xaxis.set_major_formatter(formatter)
#
#
#     locator = mdates.DayLocator()
#
#     # set locator
#
#     ax.xaxis.set_major_locator(locator)
#
#
#     plt.plot(x_v, y_v)
#     plt.show()
#
#
# def plot_profit(res: AnalysisResult, time_period=60, pair=None): #time in seconds
#     t = res.start_datetime
#     x_v=[]
#
#     while t != res.end_datetime:
#         x_v.append(t)
#         t = t + timedelta(seconds=time_period)
#
#     x_v.append(t)
#     print(x_v)
#
#     transactions = res.trades
#     if pair is not None:
#         transactions = [tr for tr in res.trades if tr.pair==pair]
#
#     over_profit = 0
#     for i in range(1,len(x_v)):
#         start = x_v[i-1]
#         end = x_v[i]
#         for j in range(0, len(transactions)):
#             if start <= transactions[i].timestamp < end and not transactions[i].is_buy:
#
#
#
#         sell_trades = [tr for tr in transactions if start <= tr.timestamp < end and not tr.is_buy]
#         for trade in sell_trades:
#
#
#
#     y_v = [res.start_balance]
#
#
#     ax = plt.gca()
#     formatter = mdates.DateFormatter("%Y-%m-%d")
#     ax.xaxis.set_major_formatter(formatter)
#
#     locator = mdates.DayLocator()
#
#     # set locator
#
#     ax.xaxis.set_major_locator(locator)
#
#     plt.plot(x_v, y_v)
#     plt.show()
