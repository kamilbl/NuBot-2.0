#!/usr/bin/env python
# -*- coding: utf-8 -*-
from binance.client import Client
import decimal
import datetime
import pandas as pd
import numpy as np
import key
import json
import talib
import math as m
import time

#Binance Api data
api_key = key.api_key
api_secret = key.api_secret

#connect Binance
client = Client(api_key, api_secret)

interval_candles = "1m"
mylimit = 500
minimal = 1.005
fee = 0.1

markets = ['APPCBTC','GVTBTC', 'SYSBTC', 'AGIBTC', 'NEBLBTC', 'FTTBTC', 'LINKBTC', 'LSKBTC', 'ARPABTC', 'TRXBTC']
def getCandles():

    from talib import MA_Type
    dfM = pd.DataFrame(columns= ['Market','Total profit'])
    i=1
    while i<len(markets):
        for market in markets:
            print("NuBot 2.0 " + str(market) + " interval:" + interval_candles + " " + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            df = pd.DataFrame(columns= ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'Taker Volume', 'Maker Volume'])
            dfSS = pd.DataFrame(columns= ['STATUS', 'Timestamp', 'Close', 'PriceBUY', 'PriceSELL', 'Volume'])
            #candles = client.get_klines(symbol=market, interval=interval_candles, limit = mylimit)
            candles = client.get_historical_klines(str(market), interval_candles, "15 day ago UTC")
            opentime, lopen, lhigh, llow, lclose, lvol, closetime, tvol, mvol = [], [], [], [], [], [], [], [], []
            for candle in candles:
                candle[0] = datetime.datetime.fromtimestamp(candle[0]/1000)
                opentime.append(candle[0])
                lopen.append(candle[1])
                lhigh.append(candle[2])
                llow.append(candle[3])
                lclose.append(candle[4])
                lvol.append(candle[5])
                candle[6] = datetime.datetime.fromtimestamp(candle[6]/1000)
                tvol.append(candle[9])
                closetime.append(candle[6])

            df['Timestamp'] = opentime
            df['Open'] = np.array(lopen).astype(np.float)
            df['Open'] = df['Open'].map('{:.8f}'.format)
            df['High'] = np.array(lhigh).astype(float)
            df['High'] = df['High'].map('{:.8f}'.format)
            df['Low'] = np.array(llow).astype(float)
            df['Low'] =  df['Low'].map('{:.8f}'.format)
            df['Close'] = np.array(lclose).astype(float)
            df['Volume'] = np.array(lvol).astype(float)
            df['Close_time'] = closetime
            df['Taker Volume'] = np.array(tvol).astype(float)
            df['Maker Volume'] = df['Volume'] - df['Taker Volume']
            df['Volume'] =  df['Volume'].map('{:.0f}'.format)
            df['Close1000'] = df['Close'] * 10000

            #-------------------------------------------------------TA--------------------------------------------------------------
            # https://github.com/mrjbq7/ta-lib
            #-----------------------------------------------------------------------------------------------------------------------

            df['FAST_EMA'] = talib.EMA(df['Close'], timeperiod=12)
            df['SLOW_EMA'] = talib.EMA(df['Close'], timeperiod=26)
            df['SIGNAL_EMA'] = talib.EMA(df['Close'], timeperiod=9)
            df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
            df['RSI'] =  df['RSI'].map('{:.1f}'.format)
            df['BBupper'], df['BBmiddle'], df['BBlower']= talib.BBANDS(df['Close1000'], timeperiod=14, nbdevup=2, nbdevdn=2, matype=0)
            df['BBupper'] = df['BBupper']/10000
            df['BBupper'] =  df['BBupper'].map('{:.8f}'.format)
            df['BBmiddle'] = df['BBmiddle']/10000
            df['BBmiddle'] =  df['BBmiddle'].map('{:.8f}'.format)
            df['BBlower'] = df['BBlower']/10000
            df['BBlower'] =  df['BBlower'].map('{:.8f}'.format)
            df['SAR'] = talib.SAR(df['High'], df['Low'], 0.02, 0.2)
            df['SAR'] =  df['SAR'].map('{:.8f}'.format)
            df['MACD'] = df['SLOW_EMA'] - df['FAST_EMA']
            df['MACD'] =  df['MACD'].map('{:.8f}'.format)
            df['Close'] =  df['Close'].map('{:.8f}'.format)
            df['FAST_EMA'] =  df['FAST_EMA'].map('{:.8f}'.format)
            df['SLOW_EMA'] =  df['SLOW_EMA'].map('{:.8f}'.format)
            df['SIGNAL_EMA'] =  df['SIGNAL_EMA'].map('{:.8f}'.format)

            status = "BUY"
            profit = 0
            total_profit = 0
            x=0
            total_rows = len(df.index)
            while x < total_rows:
                if df.loc[x, 'SLOW_EMA'] != "NaN1":
                    if float(df.loc[x, 'FAST_EMA']) > float(df.loc[x, 'BBmiddle']) and float(df.loc[x, 'MACD']) > 0 and float(df.loc[x, 'RSI']) > 50 and float(df.loc[x, 'SAR']) < float(df.loc[x, 'Close']) and status == "BUY":            #Sygnal zakupu
                        status = "SELL"
                        xprice = df.loc[x, 'Close']
                        sell_price = float(xprice) * minimal
                        lendfSS = len(dfSS.index)
                        dfSS.loc[lendfSS, 'STATUS'] = "BUY"
                        dfSS.loc[lendfSS, 'Timestamp'] = df.loc[x, 'Timestamp']
                        dfSS.loc[lendfSS, 'Close'] = df.loc[x, 'Close']
                        dfSS.loc[lendfSS, 'PriceBUY'] =  xprice
                        dfSS.loc[lendfSS, 'Volume'] = "%.2f" % float(df.loc[x, 'Volume'])
                        dfSS.loc[lendfSS, 'RSI'] = df.loc[x, 'RSI']
                        dfSS.loc[lendfSS, 'SAR'] = df.loc[x, 'SAR']
                        dfSS.loc[lendfSS, 'MACD'] = df.loc[x, 'MACD']
                        dfSS.loc[lendfSS, 'BBmiddle'] = df.loc[x, 'BBmiddle']
                        dfSS.loc[lendfSS, 'FAST_EMA'] = df.loc[x, 'FAST_EMA']
                        y = x
                        while y < total_rows:
                            if  float(df.loc[y, 'FAST_EMA']) < float(df.loc[y, 'BBmiddle']) and float(df.loc[y, 'MACD']) < 0 and float(df.loc[y, 'RSI']) < 50 and float(df.loc[y, 'SAR']) > float(df.loc[y, 'Close']) and status == "SELL" and float(df.loc[y, 'Close']) > float(sell_price):   #Sygnał sprzedaży
                                status = "BUY"
                                yprice = df.loc[y, 'Close']
                                profit = float(yprice) / float(xprice) - 1
                                total_profit = round(total_profit - 2*float(fee) + profit * 100, 2)
                                lendfSS = len(dfSS.index)
                                dfSS.loc[lendfSS, 'Timestamp'] = df.loc[y, 'Timestamp']
                                dfSS.loc[lendfSS, 'Close'] = df.loc[y, 'Close']
                                dfSS.loc[lendfSS, 'PriceSELL'] =  yprice
                                dfSS.loc[lendfSS, 'Volume'] =  "%.2f" % float(df.loc[y, 'Volume'])
                                dfSS.loc[lendfSS, 'RSI'] = df.loc[y, 'RSI']
                                dfSS.loc[lendfSS, 'SAR'] = df.loc[y, 'SAR']
                                dfSS.loc[lendfSS, 'MACD'] = df.loc[y, 'MACD']
                                dfSS.loc[lendfSS, 'BBmiddle'] = df.loc[y, 'BBmiddle']
                                dfSS.loc[lendfSS, 'FAST_EMA'] = df.loc[y, 'FAST_EMA']
                                dfSS.loc[lendfSS, 'Profit'] = str(float(profit)*100)[0:5] + "%"
                                dfSS.loc[lendfSS, 'Total profit'] = float(total_profit)
                                dfSS.loc[lendfSS, 'STATUS'] = "SELL"
                                x = y
                                break
                            else:
                                y += 1
                    else:
                        x +=1
                else:
                    x += 1

            lendfM = len(dfM.index)
            dfM.loc[lendfM, 'Market'] = str(market)
            dfM.loc[lendfM, 'Total profit'] = str(total_profit)
            dfM.sort_values(by=['Total profit'])
            print(dfSS)
            print("*********************************************************************************************************************************")
            print(dfM)
            print("*********************************************************************************************************************************")
            with pd.ExcelWriter(str(market) + '_Scalping_Strategy_TEST.xlsx') as writer:
                dfSS.to_excel(writer, sheet_name=str(market))
                writer.save()
                writer.close()
            #time.sleep(3)
            i+=1

getCandles()




