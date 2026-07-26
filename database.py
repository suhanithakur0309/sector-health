#Importing all metrics
from pipeline import *
from scoring import *
import pandas as pd
#Importing and establishing connection with sqlite3
import sqlite3
conn=sqlite3.connect('sector_health.db')
cursor=conn.cursor()
#Creating tables SECTOR_METRICS AND SECTOR_SCORES
cursor.execute('''CREATE TABLE IF NOT EXISTS SECTOR_METRICS('Date' date,'Sector Name' text,'
               Daily Return' real, 'Volatility' real,'Rolling 30' real,'Rolling 60' real,
               'Rolling 90' real,'Momentum' real,'Rolling Strength' real)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS SECTOR_SCORES('Date' date,'Sector Name' text,'
               Health Score' real,'Rating' real)''')
conn.commit()
#Creating CSV files
df_scores.to_csv('sector_scores.csv', index=False)
df_scores['Date'] = pd.Timestamp.today().date()
df_scores.reset_index(inplace=True)
df_scores=df_scores[['Date','Ticker','Scores','Rating']]
df_scores=list(df_scores.itertuples(index=False))
#Inserting values into the table using executemany
cursor.executemany("INSERT INTO SECTOR_SCORES VALUES(?,?,?,?)",df_scores)
conn.commit()
#Melting dataset to further merge into one table
dr_m=pd.melt(daily_returns.reset_index(),id_vars=['Date'],var_name='Sector',value_name='Daily_Return')
r_30_m=pd.melt(rolling_30.reset_index(),id_vars=['Date'],var_name='Sector',value_name='Rolling_30')
r_60_m=pd.melt(rolling_60.reset_index(),id_vars=['Date'],var_name='Sector',value_name='Rolling_60')
r_90_m=pd.melt(rolling_90.reset_index(),id_vars=['Date'],var_name='Sector',value_name='Rolling_90')
m_m=pd.melt(momentum.reset_index(),id_vars=['Date'],var_name='Sector',value_name='Momentum')
rs_m=pd.melt(relative_strength.reset_index(),id_vars=['Date'],var_name='Sector',value_name='Relative_Strength')
#Merging to create one table with all metrics
x=pd.merge(dr_m,r_30_m,on=['Date','Sector'],how='outer')
y=pd.merge(x,r_60_m,on=['Date','Sector'],how='outer')
z=pd.merge(y,r_90_m,on=['Date','Sector'],how='outer')
a=pd.merge(z,m_m,on=['Date','Sector'],how='outer')
b=pd.merge(a,rs_m,on=['Date','Sector'],how='outer')
b['Volatility'] = b['Sector'].map(Volatility)
b['Sector'] = b['Sector'].map(sector_names)
b['Date'] = b['Date'].astype(str)
DF=list(b.itertuples(index=False))
#Using executemany to insert data into table
cursor.executemany('INSERT INTO SECTOR_METRICS VALUES(?,?,?,?,?,?,?,?,?)',DF)
conn.commit()
#Converting to csv file
b.to_csv('sector_metrics.csv', index=False)
import os
os.getcwd()
health_score_scaled = health_score_scaled.rename(columns=sector_names)
health_score_scaled = health_score_scaled.drop(columns=['NIFTY50'], errors='ignore')
health_score_scaled.to_csv('historical_scores.csv', index=False)
import os
os.getcwd()
