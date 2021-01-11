from bitmex_websocket import BitMEXWebsocket
import numpy as np
import matplotlib.pyplot as plt

ws = BitMEXWebsocket(endpoint="wss://www.bitmex.com/realtime", symbol="XBTUSD", api_key=None,
                     api_secret=None)

price = 0
size = 1
rangeOfPricesVisible = 200
while True:
    bid = []
    ask = []
    marketDepth = ws.market_depth()
    lastPrice = ws.recent_trades()[0]["price"]

    for rows in marketDepth:
        if lastPrice-rangeOfPricesVisible < rows["price"] and rows["price"] < lastPrice+rangeOfPricesVisible:
            if rows["side"] == "Sell":
                ask.append([float(rows["price"]), int(rows["size"])])
            elif rows["side"] == "Buy":
                bid.append([float(rows["price"]), int(rows["size"])])

    bid.sort(key=lambda lmd: lmd[price])
    ask.sort(key=lambda lmd: lmd[price])

    bidCumsum = list.copy(bid)
    askCumsum = list.copy(ask)

    bidCumsum = np.delete(bidCumsum, price, 1)
    askCumsum = np.delete(askCumsum, price, 1)

    bidCumsum = np.cumsum(bidCumsum[::-1])[::-1]
    askCumsum = np.cumsum(askCumsum)
    bid = np.array(bid)
    ask = np.array(ask)
    plt.cla()
    plt.plot(bid[:, price], bidCumsum)
    plt.plot(ask[:, price], askCumsum)
    plt.pause(0.001)
