import matplotlib.pyplot as plt
import pandas as pd

#read data from csv
performances = pd.read_csv("./resources/performances.csv", delimiter=',')
#format date column
performances['date'] = pd.to_datetime(performances['EndDate'], format='%Y-%m').dt.strftime('%Y-%m')
#plot perf over time
performances.plot(x ='date', y='perf')
plt.gcf().autofmt_xdate()
plt.show()