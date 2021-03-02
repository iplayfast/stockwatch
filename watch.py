"""
http://theautomatic.net/2019/04/17/how-to-get-options-data-with-python/
"""
import os
import sys
from datetime import datetime
import time
import math
import dateutil.parser
from gtts import gTTS
from yahoo_fin import stock_info
indexrange = 10
prices = {}


def cleanInt(i):
    if i == '-':
        return int(0)
    return int(i)


def cleanPercent(series):
    if series == '-':
        return float(0.0)
    series = series.replace("%", "")
    series = series.replace(",", "")

    return float(series)


def tomysqlDate(datestr):
    t = dateutil.parser.parse(datestr)
    return t.strftime('%Y-%m-%d')


def tomysqlDateTime(datestr):
    t = dateutil.parser.parse(datestr)
    return t.strftime('%Y-%m-%d %H:%M:%S')


def toDowHourMin():
    t = datetime.now()
    return t.strftime('%w'), t.strftime('%H:%M')


def tomysqlDateTimeHash(c, i):
    t = dateutil.parser.parse(c['Last Trade Date'][i])
    strike = c['Last Price'][i].astype(float)
    ms = int(strike * 100)

    t = t.replace(microsecond=int(ms))
    return t.strftime('%Y-%m-%d %H:%M:%S.%f')


def GetOptionData(c, i):
    return c['Strike'][i].astype(float), c['Last Price'][i].astype(float), c['Bid'][i].astype(float), c['Ask'][
        i].astype(float), cleanPercent(c['% Change'][i]), cleanInt(c['Volume'][i]), cleanInt(
        c['Open Interest'][i]), cleanPercent(c['Implied Volatility'][i])


def checkprices(symbol, index):
    if prices[symbol][index] < prices[symbol][index + 1]:
        return -1
    if prices[symbol][index] > prices[symbol][index + 1]:
        return 1
    return 0


def checkpricesrange(symbol, indexrange):
    v = 0
    indexrange = indexrange - 1
    for index in range(indexrange):
        v = v + checkprices(symbol, index)
    if v == -indexrange:
        sayit(f'. Alert {symbol} is heading up')
    if v == indexrange:
        sayit(f'. Alert {symbol} is heading down')
    d = '-'
    if v>0:
        d = 'D'
    if v<0:
        d = 'U'
    print("\t",symbol,"avg last ",indexrange," checks is ",d,' ',round(prices[symbol][indexrange-1],3),end=' ')

def sayit(mytext):
    language = "en"
    myobj = gTTS(text=mytext,lang=language,slow=False)
    myobj.save('sayit.mp3')
    os.system('mpg321 sayit.mp3')


def runonce(indexrange):
    #print('finding following stocks:', str(sys.argv[1:]), toDowHourMin())
    try:
        for symbol in sys.argv[1:]:
            price = stock_info.get_live_price(symbol)
            for i in range(indexrange-1):
                prices[symbol][i] = prices[symbol][i+1]
            prices[symbol][indexrange-1] = price
            checkpricesrange(symbol, indexrange)
    except:
        time.sleep(60)
    time.sleep(1)

for symbol in sys.argv[1:]:
    prices[symbol] = []
    for i in range(indexrange):
        prices[symbol].append(0)
while True:
    dow, hm = toDowHourMin()
    if dow > '0' and dow < '6' and hm > '09:30' and hm < '16:00':
        print('')
        print(hm,end=' ')
        runonce(indexrange)
    else:
        if dow > '0' and dow < '6':  # in right day but not right time
            time.sleep(60)  # sleep 1 minute
        else:
            time.sleep(60 * 60 * 24)  # sleep a day
