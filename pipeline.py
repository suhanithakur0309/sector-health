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
DR=df.pct_change()*100
daily_returns=pd.DataFrame(DR)
#Calculating votality for each sector
vortaility=daily_returns.std()
vortaility.sort_values(ascending=False,inplace=True)
#Calculating rolling returns for the last 30, 60 and 90 days
rolling_30=daily_returns.rolling(30).sum()
rolling_60=daily_returns.rolling(60).sum()
rolling_90=daily_returns.rolling(90).sum()
#Calculating momentum of each sector
momentum=rolling_30-rolling_90
#Calculating Relative Strength
#(performance of a sector compared to the overall market)
relative_strength=rolling_30.sub(rolling_30['^NSEI'],axis=0)
relative_strength.head()