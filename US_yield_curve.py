import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
# from pathlib import Path
# import os.path

datpath = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2022/' \
          'all?type=daily_treasury_yield_curve&field_tdr_date_value=2022&page&_format=csv'
datpath23 = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/' \
            '2023/all?type=daily_treasury_yield_curve&field_tdr_date_value=2023&page&_format=csv'
data = pd.read_csv(datpath)
db22 = data.loc[:, ['Date', '1 Mo', '2 Mo', '3 Mo', '6 Mo', '1 Yr', '2 Yr', '3 Yr', '5 Yr', '7 Yr', '10 Yr', '20 Yr',
                    '30 Yr']]
data23 = pd.read_csv(datpath23)
db23 = data23.loc[:, ['Date', '1 Mo', '2 Mo', '3 Mo', '6 Mo', '1 Yr', '2 Yr', '3 Yr', '5 Yr', '7 Yr', '10 Yr', '20 Yr',
                    '30 Yr']]
db = pd.concat([db23, db22])
db = db.reset_index(drop=True)

# Get data of different dates
today = pd.melt(db.iloc[0:1, ], id_vars='Date')
tday = today['Date'].iloc[0]
tday = tday.replace("/", "-")
yesterday = pd.melt(db.iloc[1:2, ], id_vars='Date')
yday = yesterday['Date'].iloc[0]
yday = yday.replace("/", "-")
lastweek = pd.melt(db.iloc[4:5, ], id_vars='Date')
last30days = pd.melt(db.iloc[29:30, ], id_vars='Date')
q3 = db.loc[db['Date'] == '09/30/2022']
q3 = pd.melt(q3, id_vars='Date')
q2 = db.loc[db['Date'] == '06/30/2022']
q2 = pd.melt(q2, id_vars='Date')
q1 = db.loc[db['Date'] == '03/31/2022']
q1 = pd.melt(q1, id_vars='Date')
beginning22 = db.loc[db['Date'] == '01/03/2022']
beginning22 = pd.melt(beginning22, id_vars='Date')

# newdb = newdb.sort_values(by=['Date','variable'], ascending=[False,True])

# Calculate the 10Y - 2Y
yest10v2 = float(yesterday.loc[yesterday['variable'] == '10 Yr', 'value']) - \
           float(yesterday.loc[yesterday['variable'] == '2 Yr', 'value'])
# yest10v2 = round(yest10v2, 3)
today10v2 = float(today.loc[today['variable'] == '10 Yr', 'value']) - \
            float(today.loc[today['variable'] == '2 Yr', 'value'])
# today10v2 = round(today10v2,3)
lastweek10v2 = float(lastweek.loc[lastweek['variable'] == '10 Yr', 'value']) - \
               float(lastweek.loc[lastweek['variable'] == '2 Yr', 'value'])
# lastweek10v2 = round(lastweek10v2,3)


# Plot1
fig, ax = plt.subplots()
ax.plot('variable', 'value', data=today, linestyle='-', color='k', marker='+', label=tday)
ax.plot('variable', 'value', data=yesterday, linestyle='-', color='r', marker='h', label=yday)
ax.plot('variable', 'value', data=lastweek, linestyle='--', color='b', label='Last week')
ax.plot('variable', 'value', data=last30days, linestyle='-.', color='y', label='Last month')
# ax.plot('variable', 'value', data=q3, linestyle='-', marker='o',  color='k', label='09-30-2022')
ax.plot('variable', 'value', data=q2, linestyle='-', marker='v', color='c', label='06-30-2022')
# ax.plot('variable', 'value', data=q1, linestyle='-', marker='h', color='r', label='03-31-2022')
ax.plot('variable', 'value', data=beginning22, linestyle='-', marker='_', color='m', label='Beginning 2022')
plt.title('US Yield Curve')
plt.xlabel('Maturities')
ax.text(0.1, 3, "10Y vs 2Y: \n" + f'Today: {today10v2:.2f} \n' +
        f'Yesterday: {yest10v2:.2f} \n' + f'Last-week: {lastweek10v2:.2f}', bbox={'facecolor': 'white'}, weight='bold',
        fontsize=8)
# plt.ylim(0,5,0.5)
plt.ylabel('Yield %')
plt.legend()
plt.savefig('US_yield-curve_'+tday+'.png')
plt.show(block=True)

# Calculate 10Y vs 2Y, 30Y vs 10Y and 30Y vs 2Y charts
db['Y10-Y2'] = round(db['10 Yr']-db['2 Yr'], 2)
db['Y30-Y2'] = round(db['30 Yr']-db['2 Yr'], 2)
db['Y30-Y10'] = round(db['30 Yr']-db['10 Yr'], 2)

# Sort db by date
db = db.sort_index(ascending=False)

# Create row numbers
db['row_num'] = np.arange(len(db))
db['Dates'] = pd.to_datetime(db['Date'])
db['Dates'] = db['Dates'].dt.strftime("%b-%y")
yrmonth = db['Dates'].drop_duplicates()
db['Date'] = pd.to_datetime(db['Date'])
db['Date'] = db['Date'].dt.strftime("%b-%d-%y")


# Plot2
fig, ax = plt.subplots()
ax.plot('Date', 'Y10-Y2', data=db, linestyle='-', color='k', label='10Y vs 2Y')
ax.plot('Date', 'Y30-Y2', data=db, linestyle='--', color='b', label='30Y vs 2Y')
ax.plot('Date', 'Y30-Y10', data=db, linestyle='-', color='m', label='30Y vs 10Y')
ax.tick_params(axis='x', rotation=45)
plt.title('Yield Curves (10Y vs 2Y, 30Y vs 2Y, 30Y vs 10Y) \n' + f'FY2022 to {tday}', weight='bold')
plt.xlabel('Days')
ax.xaxis.set_major_locator(plt.MaxNLocator(len(yrmonth)))
ax.tick_params(labelsize=7)
# ax.set_xticks(np.arange(0, len(yrmonth), 1))
# ax.set_xticklabels(yrmonth)
# ax.xaxis.set_minor_locator(plt.MultipleLocator(len(yrmonth)))
ax.text(5, -0.8, "Lowest num: \n" + f'10Y vs 2Y: {min(db["Y10-Y2"]):.2f} \n' +
        f'30Y vs 2Y: {min(db["Y30-Y2"]):.2f} \n' + f'30Y vs 10Y: {min(db["Y30-Y10"]):.2f} \n' + "Current: \n" +
        f'10Y vs 2Y: {db["Y10-Y2"].iloc[-1]:.2f} \n' + f'30Y vs 2Y: {db["Y30-Y2"].iloc[-1]:.2f} \n' +
        f'30Y vs 10Y: {db["Y30-Y10"].iloc[-1]:.2f}', bbox={'facecolor': 'white'}, weight='bold', fontsize=8)
# plt.ylim(0,5,0.5)
plt.ylabel('Yield %')
plt.legend()
plt.savefig('/US_yield-curve_comparison_'+tday+'.png')
plt.show(block=True)


