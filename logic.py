
# get price
# if price is 5% higher than current stop limit 
    # raise stop limit 2%

CHANGE = 0.03
SELL_UNDER_STOP = 0.01

usdt_amount = 100

coins = {
    'ETH' : {
        'amount' : 1,
        'bought' : 200,
        'stop' : 194
    }
}

def update(coin, value):
    try:
        # the value is above what we bought it for
        # and the potential new stoplimit is above the old one
        if coins[coin].bought < value and value-value*CHANGE > coins[coin].stop:
            coins[coin].stop = value - value*CHANGE
        elif value <= stop:
            sell(coin)
    except KeyError:
        print("We don't own any of ", coin)

def update_balances():
    updated = {"ETH":{"available":"5.015","onOrders":"0","btcValue":"0.078"},"USDT":{"available":"10","onOrders":"0","btcValue":"0.078"}}
    for k,v in updated.iteritems():
        if k == 'USDT':
            usdt_amount = v['available']
        elif v['available'] > 0:
            coins[k]['amount'] = v['available']
        elif k in coins:
            del(coins[k])

def sell(coin):
    sell_price = coins[coin].stop - coins[coin].stop*SELL_UNDER_STOP
    print("Selling ", coins[coin], "of ", coin, " at ", sell_price)
    # sell for sell price
    sell_order = {
        "orderNumber":31226040,
        "resultingTrades":[{
            "amount":"338.8732",
            "date":"2014-10-18 23:03:21",
            "rate":"0.00000173",
            "total":"0.00058625",
            "tradeID":"16164",
            "type":"sell"
        },
        {
            "amount":"300",
            "date":"2014-10-18 23:03:21",
            "rate":"0.0000015",
            "total":"0.00045",
            "tradeID":"16164",
            "type":"sell"
        }]
    }

    sold_amount = 0

    for trade in sell_order:
        sold_amount += trade.amount
    
    if sold_amount >= coins[coin].amount:
       del(coins[coin])
    
    update_balances()
    

def buy(coin, price, amount):
    buy_order = {
        "orderNumber":31226040,
        "resultingTrades":[{
            "amount":"338.8732",
            "date":"2014-10-18 23:03:21",
            "rate":"0.00000173",
            "total":"0.00058625",
            "tradeID":"16164",
            "type":"buy"
        }]
    }

    total_amount = 0
    total_price = 0

    for trade in buy_order.resultingTrades:
        total_amount += trade.amount
        total_price += trade.total
    
    price = total_price/total_amount

    coins[coin] = {
        'amount' : total_amount,
        'bought' : price,
        'stop' : price-price*CHANGE
    }

if __name__ == "__main__":
    print(coins)
    update_balances()
    print(coins)