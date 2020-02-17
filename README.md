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
    
    We can add a few crypto pairs and export to Excel. 
    ![ScreenShot](https://github.com/kamilbl/NuBot-2.0/blob/master/StrategyScalpingBacktest.PNG)
    
