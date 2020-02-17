# NuBot-2.0

1) StrategyScalpingBacktest <=== Backtest Strategy Scalping for cryptocurrencies.

    **Main assumptions:**
    
    #LongPosition:
    - Fast EMA[12] > BBmiddle[14]
    - MACD > 0
    - RSI[14] > 50
    - SAR < Close
    
    #ShortPosition:
    - Fast EMA[12] < BBmiddle[14]
    - MACD < 0
    - RSI[14] < 50
    - SAR > Close
    - Close > Sell_Price(Buy_Price * MinProfit)
    
    We can add a few crypto pairs:
    
    `markets = ['APPCBTC','GVTBTC', 'SYSBTC', 'AGIBTC', 'NEBLBTC', 'FTTBTC', 'LINKBTC', 'LSKBTC', 'ARPABTC', 'TRXBTC']`
    
    Change interval candles and limit time:
    
    `candles = client.get_historical_klines(str(market), interval_candles, "15 day ago UTC")`
    
    Export to Excel:
    
    ```
    with pd.ExcelWriter(str(market) + '_Scalping_Strategy_TEST.xlsx') as writer:
                dfSS.to_excel(writer, sheet_name=str(market))`
                writer.save()
                writer.close()
    ```
                
    ![ScreenShot](https://github.com/kamilbl/NuBot-2.0/blob/master/StrategyScalpingBacktest.PNG)
    
