# Some of the code should be given credit to sentdex
from pandas_datareader import data
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np


currentDate = datetime.datetime.now()
startDate = datetime.datetime(2013, 5, 28)
endDate = datetime.datetime(currentDate.year, currentDate.month, currentDate.day)
dateRange = pd.date_range(startDate, endDate)
#List the cryptocurrentcy symbole
btc = "BTC-USD"
eth = "ETH-USD"
ripple = "XRP-USD"
litecoin = "LTC-USD"
bitcoinCash = "BCH-USD"
eos = "EOS-USD"
xmr = "XMR-USD"
ethc = "ETC-USD"
dash = "DASH-USD"
binance = "BNB-USD"
symbols = [btc, eth, ripple, bitcoinCash, litecoin, eos, xmr, ethc, dash, binance]

# Create an empy dataframe

df = pd.DataFrame(index=dateRange)

# Get the BTC data
for sym in symbols:
	df_temp = data.DataReader(sym, 'yahoo', startDate)
	df_temp.rename(columns={"Adj Close": f"{sym}_close", "Volume": f"{sym}_volume"}, inplace=True)
	df_temp = df_temp[[f"{sym}_close", f"{sym}_volume"]] 
	
	if (df.empty):
		df = df_temp
	else:
		df = df.join(df_temp)
		
# Fill in missimng data
#Fixing missing data. Best practice fill forward and fill backward
df.fillna(method="ffill", inplace=True)
df.fillna(method="bfill", inplace=True)


# Setting up for the LSTM Model
sequence_length = 60  # Last minutes 
prediction_sym = symbols[1]
length_prediction = 3 # future prediction in mnitues


# Create a method that shift future price by the length_prediction

def futurePriceClassifier(current_price, future_price):
	if(future_price > current_price):
		return 1
	else:
		return 0

df['future_price'] = df[f'{prediction_sym}_close'].shift(-length_prediction)

df['target_price'] = list(map(futurePriceClassifier, df[f'{prediction_sym}_close'], df['future_price']))
# df.dropna(inplace=True)
df.to_csv("hello.csv")


# Sklearn for data preprocessing
#Scalling the data
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

scaler = MinMaxScaler()
scalled_feature = df.drop(columns=['target_price'])
scalled_feature = scaler.fit_transform(scalled_feature)

# Split the data
from sklearn.model_selection import TimeSeriesSplit

print(len(train_df), len(test_df))
print(train_df)