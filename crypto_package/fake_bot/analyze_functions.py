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