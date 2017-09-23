import requests as r
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as md
from threading import Timer

from datetime import datetime
from scipy import stats
from decimal import Decimal

draw_graphs = False

def api_query(command):
    """
    query the poloniex api
    docs here -> https://poloniex.com/support/api/
    """
    resp = r.get('https://poloniex.com/public?command={}'.format(command))
    if resp.status_code != 200:
        return None
    
    return resp.json()


dates = []
lowestAsks = []

if draw_graphs:
    plt.xticks(rotation=25)
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    lastPrice = None

data = []
mpa = []
max_points = 80
mpa_points = 6

def update(i):
    # fetch the current ticker
    ticker_json = api_query('returnTicker')
    if ticker_json is None:
        print('api error occured')
        exit(0)
    
    # add the current time to the x axis
    dates.append(datetime.now())

    # add the lowest ask for usdt -> btc to the y axis
    lowestAsk = ticker_json['BTC_DOGE']['lowestAsk']
    lowestAskRound = float(lowestAsk)
    lowestAsks.append(lowestAskRound)
    global lastPrice

    data.append((datetime.now(), float(lowestAskRound)))

    total = 0
    val = 0

    for i in range(mpa_points):
        try:
            total += lowestAsks[-(i+1)]
        except IndexError:
            val = total/(i)
            break

    if val == 0:
        val = total/mpa_points

    mpa.append(float(val))

    if len(data) >= max_points:
        dates.pop(0)
        data.pop(0)
        mpa.pop(0)
        lowestAsks.pop(0)

    print("Recent value: "+str(lowestAsks[-1]))
    print("Moving gradient: "+str((mpa[-1]-mpa[0])/mpa_points))

    if draw_graphs:
        # clear the subplot
        ax1.clear()
    
        # plot the graph
        ax1.plot(dates, lowestAsks, color="blue")
        ax1.plot(dates, mpa, color="red", label="Moving Point Average", linestyle="dashed")

        # make sure date formatting is correct
        plt.gcf().autofmt_xdate()

def run_timer():
    t = Timer(1, run_timer)
    t.start()
    update(0)

if draw_graphs:
    ani = animation.FuncAnimation(fig, update, interval=1000)
else:
    run_timer()

try:
    while(1):
        pass
except KeyboardInterrupt:
    pass

if draw_graphs:
    plt.show()