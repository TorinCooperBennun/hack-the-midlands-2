import requests as r
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as md
from datetime import datetime
from scipy import stats
from decimal import Decimal

import purchase
import logic


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
plt.xticks(rotation=25)

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
lastPrice = None

data = []
mpa = []
max_points = 80
mpa_points = 10

def update(i):
    # fetch the current ticker
    ticker_json = api_query('returnTicker')
    if ticker_json is None:
        print('api error occured')
        exit(0)
    
    # add the current time to the x axis
    dates.append(datetime.now())

    # add the lowest ask for usdt -> btc to the y axis
    lowestAsk = ticker_json['USDT_BTC']['lowestAsk']
    lowestAskRound = float(round(Decimal(lowestAsk), 2))
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

    # clear the subplot
    ax1.clear()
    
    # plot the graph
    ax1.plot(dates, lowestAsks, color="blue")
    ax1.plot(dates, mpa, color="red", label="Moving Point Average", linestyle="dashed")

    # make sure date formatting is correct
    plt.gcf().autofmt_xdate()

    # use linear regression to calculate if price is going up
    dateseconds = [t.timestamp() for t in dates]

    #if len(dates) > 10:
        #print(stats.linregress(dateseconds[-10:], [float(a) for a in lowestAsks[-10:]]).slope)
    
    
        

ani = animation.FuncAnimation(fig, update, interval=1000)

plt.show()