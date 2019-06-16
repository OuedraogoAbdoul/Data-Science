from pandas_datareader import data
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np


currentDate = datetime.datetime.now()
startDate = datetime.datetime(2013, 5, 28)
endDate = datetime.datetime(currentDate.year, currentDate.month, currentDate.day)
dateRange = pd.date_range(startDate, endDate)

#List the cryptocurrentcy symbols
BTC = data.DataReader("BTC-USD", 'yahoo', startDate)
ETH = data.DataReader("ETH-USD", 'yahoo', startDate)
XRP = data.DataReader("XRP-USD", 'yahoo', startDate)
LTC = data.DataReader("LTC-USD", 'yahoo', startDate)
BCH = data.DataReader("BCH-USD", 'yahoo', startDate)

# Ploting top five crypto Adj Close price
BTC["Adj Close"].plot(label='BTC',title="Adj Closing Prices",figsize=(16,6))
ETH["Adj Close"].plot(label="ETH")
XRP["Adj Close"].plot(label="XRP")
LTC["Adj Close"].plot(label="LTC")
BCH["Adj Close"].plot(label="BCH")
plt.legend()
plt.grid()
# plt.show()
plt.savefig('AdjClose.png')


# Ploting top five crypto volume price
BTC["Volume"].plot(label='BTC',title="Volume Prices",figsize=(16,6))
ETH["Volume"].plot(label="ETH")
XRP["Volume"].plot(label="XRP")
LTC["Volume"].plot(label="LTC")
BCH["Volume"].plot(label="BCH")
plt.legend()
plt.grid()
# plt.show()
plt.savefig('Volume.png')


# Print highest price and data
print("BTC Highest Price: ",BTC["Adj Close"].max())
print("BTC date of highest bull: ",BTC["Adj Close"].idxmax(), '\n')

print("ETH Highest Price: ",ETH["Adj Close"].max())
print("ETH date of highest bull: ",ETH["Adj Close"].idxmax(), '\n')

print("XRP Highest Price: ",XRP["Adj Close"].max())
print("XRP date of highest bull: ",XRP["Adj Close"].idxmax(), '\n')

print("BCH Highest Price: ",BCH["Adj Close"].max())
print("BCH date of highest bull: ",BCH["Adj Close"].idxmax(), '\n')

print("LTC Highest Price: ",LTC["Adj Close"].max())
print("LCT date of highest bull: ",LTC["Adj Close"].idxmax(), '\n')


# Compute BTC and LTC 10Days and 200days moving average
BTC["10MA"] = BTC["Adj Close"].rolling(10).mean()
BTC["200MA"] = BTC["Adj Close"].rolling(200).mean()
BTC[["Adj Close", "10MA", "200MA"]].plot(title="BTC Adj Close 10MA and 200MA",figsize=(16,8))
plt.savefig('BTC_10MA_200MA.png')

LTC["10MA"] = LTC["Adj Close"].rolling(10).mean()
LTC["200MA"] = LTC["Adj Close"].rolling(200).mean()
LTC[["Adj Close", "10MA", "200MA"]].plot(title="LTC Adj Close 10MA and 200MA",figsize=(16,8))
plt.savefig('LTC_10MA_200MA.png')


# Look for relationship between the the five cryptocurrentcy
btc = 'BTC-USD'
eth = 'ETH-USD'
ripple = 'XRP-USD'
litecoin = 'LTC-USD'
bitcoinCash = 'BCH-USD'
symbols = [eth, ripple, bitcoinCash, litecoin]

# Create an empy dataframe

df = pd.DataFrame(index=dateRange)

# Get the BTC data
df_btc = data.DataReader(btc, 'yahoo', startDate)
df_btc = pd.DataFrame(df_btc)
df_btc = df_btc.rename(columns={'Adj Close': btc})
df_btc = df_btc[btc]

# Join BTC to the empty dataFrame
df = df.join(df_btc, how='inner')

# Get the extra dataset
for sym in symbols:
	df_merge = data.DataReader(sym, 'yahoo', startDate)
	df_merge = pd.DataFrame(df_merge)
	df_merge = df_merge.rename(columns={'Adj Close': sym})
	df_merge = df_merge[sym]
	df = df.join(df_merge)

# plotting the scatter scatter_matrix
# scatter_matrix(df, figsize=(10,10))
# plt.savefig("scatter_matrix.png")
# df_corr = df.corr("pearson")
# print("Pearson correlation: ", df_corr)
# df_corr.to_csv("CrytoCorr.csv")
#


# Compute Daily Percentage
BTC["Daily_return"] = BTC["Adj Close"].pct_change(1)
ETH["Daily_return"] = ETH["Adj Close"].pct_change(1)
LTC["Daily_return"] = LTC["Adj Close"].pct_change(1)
XRP["Daily_return"] = XRP["Adj Close"].pct_change(1)
BCH["Daily_return"] = BCH["Adj Close"].pct_change(1)

# Which Crypto is more volatile
d_return = (df / df.shift(1)) -1
d_return.iloc[0, :] = 0
ax = d_return.plot(title="Daily Return", figsize=(10,8))
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.grid()
plt.savefig('Daily_return.png')

# Daily retrun histogram
d_return.hist()


d_return = (df / df.shift(1)) -1
d_return.iloc[0, :] = 0
ax = d_return.plot(kind='kde',title="kde Daily Return", figsize=(10,8))
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.grid()
plt.savefig('Daily_returnkde.png')


# Compute cumulitive return
cum_return = (1+d_return).cumprod()
ax = cum_return.plot(title="Cumulitive Return")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.grid()
plt.savefig('Cumulitive_return.png')

# Check how LTC and ETH perform with respect to BTC
# Alpha value tells us how well one preform over the other bigger alpha
# beta tells us how the other crypto moves with respect to BTC
# greater beta means it is more reactive
beta_ltc, alpha_ltc = np.polyfit(df[btc], df[litecoin], 1)
print("Beta LTC",beta_ltc)
print("Alpha LTC",alpha_ltc)

beta_eth, alpha_eth = np.polyfit(df[btc], df[eth], 1)
print("Beta ETH",beta_eth)
print("Alpha ETH",alpha_eth)
