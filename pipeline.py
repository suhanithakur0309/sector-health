import yfinance as yf
import pandas as pd
import numpy as np
#Downloading data of 11 primary sectors of NSE for the last 2 years
data=yf.download(["^NSEBANK","^CNXIT","^CNXPHARMA","^CNXAUTO","^CNXFMCG","^CNXREALTY","^CNXENERGY",
                  "^CNXMETAL","^CNXMEDIA","^CNXINFRA","^NSEI"],period="2y")
df=pd.DataFrame(data['Close'])
#Checking for null values
print(df.isnull().sum())
#Filling null values with the previous day's closing price
df.ffill(inplace=True)
#Calculating daily returns for each sector
#(gain or loss in one day)
DR=df.pct_change()*100
daily_returns=pd.DataFrame(DR)
#Calculating votality for each sector
#(how wildly prices move and down)
Volatility=daily_returns.std()
Volatility.sort_values(ascending=False,inplace=True)
#Calculating rolling average for the last 30, 60 and 90 days
#(avg price of the last N days)
rolling_30=daily_returns.rolling(30).mean()
rolling_60=daily_returns.rolling(60).mean()
rolling_90=daily_returns.rolling(90).mean()
#Calculating momentum of each sector
#(whether a sector is accelerating or deaccelerating)
momentum=rolling_30-rolling_90
#Calculating Relative Strength
#(performance of a sector compared to the overall market)
relative_strength=rolling_30.sub(rolling_30['^NSEI'],axis=0)
