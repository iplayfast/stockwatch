#!/usr/bin/env python3
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
from playsound import playsound
from os import path
import time
indexrange = 10
prices = {}
maxPrices = {}
minPrices = {}
lastsaid = time.time() 

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
    name = swapname(symbol)
    for index in range(indexrange):
        v = v + checkprices(symbol, index)
    if v == -indexrange:
        sayit(f'. Alert {name} is heading up')
    if v == indexrange:
        sayit(f'. Alert {name} is heading down')
    d = '-'
    if v>0:
        d = 'D'
    if v<0:
        d = 'U'
    print("\t",symbol," trend is ",d,' ',round(prices[symbol][indexrange],3),end=' ')

def sayit(mytext):
    global lastsaid
    output = mytext
    output = output.replace(',','')
    output = output.replace('.','')
    output = output.strip()
    print(output)
    output = output.replace(' ','_')
    output = mytext + '.mp3';
    if not path.exists(output):
        language = "en"
        myobj = gTTS(text=mytext,lang=language,slow=False)
        myobj.save(output)
    else:
        #print(time.time() - lastsaid)
        if (time.time()-lastsaid<30):#we wait 30 seconds before talking again
            return
        else:
            lastsaid = time.time()
            
    if os.name=='posix':
        #linux
        output = 'mpg321 -q -4 ' + output
        os.system(output)
    else:
        #windows
        playsound(output)

def swapname(symbol):
    if symbol=='tsla':
        return 'tesla'
    if symbol=='pltr':
        return 'palentir'; 
    if symbol=='bmo':
        return 'bank of montreal'
    if symbol=='sndl':
        return 'sundial'
    if symbol=='cgx':
        return 'galaxy'
    if symbol=='arkk':
        return 'ark k '
    if symbol=='twtr':
        return 'twitter'
    if symbol=='pep':
        return 'pepsi'
    if symbol=='hpq':
        return 'hp'
    if symbol=='tlry':
        return 'Tilray'
    return symbol

def runonce(indexrange):
    #print('finding following stocks:', str(sys.argv[1:]), toDowHourMin())
    try:
        for symbol in sys.argv[1:]:
            try:
                price = stock_info.get_live_price(symbol)
            except:
                return
            if len(prices[symbol])<indexrange:
                indexrange = len(prices[symbol])
            for i in range(indexrange-1):
                prices[symbol][i] = prices[symbol][i+1]
            prices[symbol][indexrange-1] = price
            stockname = swapname(symbol)
            if (minPrices[symbol]==-1):
                minPrices[symbol]=price
            if minPrices[symbol]>price:
                minPrices[symbol]=price
                sayit(f'. Alert {stockname} has new minimum price')
            if (maxPrices[symbol]==-1):
                maxPrices[symbol]=price
            if (maxPrices[symbol]<price):
                maxPrices[symbol]=price
                sayit(f', Alert {stockname} has new maximum price')
            checkpricesrange(symbol, indexrange)
    except AssertionError as error:
        print(f'error looking up {symbol} {error}')
        time.sleep(6)
    time.sleep(1)

for symbol in sys.argv[1:]:
    prices[symbol] = []
    maxPrices[symbol]=-1
    minPrices[symbol]=-1

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
            sayit("After hours, so sleeping ")
            time.sleep(60 * 60 * 24)  # sleep a day
        for symbol in sys.argv[1:]: # new day, start fresh
            maxPrices[symbol]=-1
            minPrices[symbol]=-1

