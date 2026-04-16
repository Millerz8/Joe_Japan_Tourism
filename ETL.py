import requests
import numpy as np
import pandas as pd
import io
response = requests.get('https://www.tourism.jp/wp/wp-content/uploads/2026/03/JTM_inbound_20260304eng.xlsx')
df = pd.read_excel(io.BytesIO(response.content))
df = df.iloc[2:]
df.columns = ["Month", "Total Visitors", "%Change", "Notes"]
df = df.reset_index()
df.drop(columns = ["index"], inplace = True)

mindex = df[df["Total Visitors"].isna()].index.min() # Making sure null data is not represented
df = df.iloc[:mindex]

full_cycle = int((df.shape[0] / 48))
full_cycle_remainder = df.shape[0] % 48
days_leap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
days_nonleap = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
days = days_leap + days_nonleap * 3
total_days = days * full_cycle + days[:full_cycle_remainder] # change based on number of yeas

df["Days"] = total_days


df["Month"] = df["Month"].str.rstrip()
df["Year"] = df["Month"].str[:-4]
df["Month"] = df["Month"].str[-4:-1]
df['Year'] = df['Year'].ffill()
df["Year"] = df["Year"].str.rstrip()

df["Total_Visitors"] = df["Total Visitors"].astype(int)
df["Year"].replace("", np.nan, inplace = True)
df["Year"] = df["Year"].ffill()
df["Date"] = df["Month"] + " " + df["Year"]
df["Date"] = df["Date"].str.strip()

df["Date"] = pd.to_datetime(df["Date"])
df["Daily_Visitors"] = df["Total Visitors"]/df["Days"] # Want to make a column of daily visitors because that is a better example of "crowdedness" than total visitors
df = df[["Year", "Month", "Days", "Date", "Total_Visitors", "Daily_Visitors", "%Change", "Notes"]]

df.to_csv('data/Japan_Visitor_Data.csv', index = False)


