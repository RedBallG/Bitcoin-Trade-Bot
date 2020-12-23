import robin_stocks as r
from time import sleep
import tulipy as ti
import numpy as np

r.login("email","password")
enteredTrade = True
buying = 0 #Must reach 2
selling = 0 #Must reach 2
buyingpower = 30
pricebought = 9343.88
currentbtc = 0


def getRSI(symbol):
    historicals = r.crypto.get_crypto_historical(symbol, "15second", "hour", "24_7", info=None)
    closePrices = []
    rsiPeriod = 14
    currentIndex = 0
    for key in historicals["data_points"]:
        if (currentIndex >= len(historicals["data_points"]) - (rsiPeriod + 1)):
            closePrices.append(float(key["close_price"]))
        currentIndex += 1
    DATA = np.array(closePrices)
    rsi = ti.rsi(DATA, period=rsiPeriod)[0]
    return rsi

def getSupport(symbol):
    historicals = r.crypto.get_crypto_historical(symbol, "15second", "hour", "24_7", info=None)
    currentIndex = 0
    currentSupport = 0
    for key in historicals["data_points"]:
        if (currentIndex >= len(historicals["data_points"]) - (60)):
            if (float(key["close_price"]) < currentSupport or currentSupport == 0):
                currentSupport = float(key["close_price"])
        currentIndex += 1
    return currentSupport

def getResistance(symbol):
    historicals = r.crypto.get_crypto_historical(symbol, "15second", "hour", "24_7", info=None)
    currentIndex = 0
    currentResistance = 0
    for key in historicals["data_points"]:
        if (currentIndex >= len(historicals["data_points"]) - (60)):
            if (float(key["close_price"]) > currentResistance):
                currentResistance = float(key["close_price"])
        currentIndex += 1
    return currentResistance

def getCurrentPrice(symbol):
    quote = r.crypto.get_crypto_quote(symbol, info=None)
    return float(quote["mark_price"])

while True:
    rsi = getRSI("BTC")
    support = getSupport("BTC")
    resistance = getResistance("BTC")
    currentPrice = getCurrentPrice("BTC")
    for crypto in r.crypto.get_crypto_positions()[0]["cost_bases"]:
        if crypto["currency_id"] == "1072fc76-1862-41ab-82c2-485837590762":
            currentbtc = crypto["direct_quantity"]
            break
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("                                                                                                 Current Statistics                                                                                        ")
    print(f"RSI (14): {rsi}, Current Support: {support}, Current Resistance: {resistance}, Current Price: {currentPrice}, Price Bought At: {pricebought}, Trade Entered: {enteredTrade}, Current Bitcoin: {currentbtc}")
    #print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")


    if enteredTrade:
        #Selling
        print("Reasons not to sell: ")
        if rsi >= 70:
            selling += 1
        else:
            print("RSI was not above the 70 selling threshold.")
        if currentPrice >= resistance and resistance > 0:
            selling += 1
        else:
            print("The current price was not greater than the resistance.")

        if selling >= 2 and currentPrice >= pricebought:
            r.orders.order_sell_crypto_by_quantity('BTC',currentbtc)
            print("\n\n\n")
            print(f"Sold all Bitcoin at {currentPrice} and made ${round(currentPrice-pricebought,2)} worth of profit!")
            print("\n\n\n")
            pricebought = 0
            enteredTrade = False
        
        selling = 0


    else:
        #Buying
        print("Reasons not to buy: ")
        if rsi <= 30:
            buying += 1
        else:
            print("RSI was not below the 30 buying threshold.")
        if currentPrice <= support:
            buying += 1
        else:
            print("The current price waas not less than the support.")

        if buying >= 2:
            r.order_buy_crypto_by_price('BTC',buyingpower)
            pricebought = currentPrice
            print("\n\n\n")
            print(f"Bought ${buyingpower} worth of Bitcoin at {pricebought}!")
            print("\n\n\n")
            enteredTrade = True
        
        buying = 0

        
    sleep(2)