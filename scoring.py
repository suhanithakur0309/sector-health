#Importing all metrics
from pipeline import *
#Defining function to normalise metrics to ensure uniformity and easy readibility
def normalize(series):
  Z=(series-series.mean())/series.std()
  return Z
norm_rolling_30=normalize(rolling_30)
norm_rolling_90=normalize(rolling_90)
norm_volatility=normalize(-Volatility)
norm_momentum=normalize(momentum)
norm_Relative_Strength=normalize(relative_strength)
#Defining a combined weighted health score according to importance
health_score=(0.25*norm_rolling_30)+(0.20*norm_rolling_90)+(0.20*Volatility)+(0.20*norm_momentum)+(0.15*norm_Relative_Strength)
health_score=health_score.drop(columns=['^NSEI'])
#Scaling the health for ease of comparision
health_score_scaled=(health_score-health_score.min())/(health_score.max()-health_score.min())*100
#Assigning rating according to the health score of each sector
def get_rating(score):
  if score>65:
    return "Strong"
  elif score<=65 and score>=40:
    return "Neutral"
  else:
    return "Weak"
for i in health_score_scaled.tail(1):
  print(f"{i} : {get_rating(health_score_scaled.iloc[-1][i])}")
#Creating a dataframe for each sectors heath score and rating
scores=health_score_scaled.iloc[-1]
df_scores=pd.DataFrame({'Scores' :scores, 'Rating' :scores.apply(get_rating)})
df_scores.reset_index(inplace=True)
df_scores.sort_values(by='Scores',axis=0,ascending=False,inplace=True)