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
btc = 'BTC-USD'
eth = 'ETH-USD'
ripple = 'XRP-USD'
litecoin = 'LTC-USD'
bitcoinCash = 'BCH-USD'
eos = 'EOS-USD'
xmr = 'XMR-USD'
ethc = 'ETC-USD'
dash = 'DASH-USD'
zcash = 'ZEC-USD'
symbols = [eth, ripple, bitcoinCash, litecoin, eos, xmr, ethc, dash, zcash]

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


# Fill in missimng data
#Fixing missing data. Best practice fill forward and fill backward
df.fillna(method="ffill", inplace=True)
df.fillna(method="bfill", inplace=True)

#Plot all the dataset
ax = df.plot(title= "Ten cryptocurrency Plot")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.grid()
plt.show()

df.hist()

#Let's compute statistics on all the dataset
# Compute the mean
mean = df.mean()
#Compute median
median = df.median()
#Compute Standard Deviation
std = df.std()

# Let's compute moving statistics
#Compute the rolling of BTC symbol
df_btc = df[btc]
# pd.rolling_mean(df3, 20)
rm = df_btc.rolling(20).mean()
# Compute rolling std
rstd =df_btc.rolling(20).std()

#Add the rolling mean plot to the plot above
plt.title("Rolling mean and Rolling Std")
plt.plot(df_btc, label="orginal graph")
plt.plot(rm, label="Rolling mean")
plt.plot(rstd, label="Rolling std")
plt.legend()
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.grid()
plt.show()

# Compute Boilinger band (R) by using 2 std above and below the mean
upper_band = rm + rstd * 2
lower_band = rm - rstd * 2
plt.title("Boilinger Band (R)")
plt.plot(df_btc, label=btc)
plt.plot(upper_band, label="upper_band")
plt.plot(rm, label="Rolling mean")
plt.plot(lower_band, label="lower_band")
plt.legend()
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.grid()
plt.show()


#Compute daily return which is total price devided by yesterday minus one
# Can be used to compare how two symbole moves as compare to the other.
d_return = (df / df.shift(1)) -1
# d_return = df.copy()
# d_return[1:] = (df[1:] / df[:-1].values) - 1
d_return.ix[0, :] = 0
ax = d_return.plot(title="Daily Return")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.grid()
plt.show()

# Daily retrun histogram
d_return.hist()

# Compute cumulitive return
cum_return = (1+d_return).cumprod()
ax = cum_return.plot(title="Cumulitive Return")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.grid()
plt.show()

# Plotting scatter plot
df.plot(kind='scatter', x=btc, y=litecoin) #btc vs ltc
plt.show()

df.plot(kind='scatter', x=btc, y=eth) #btc vs ETH
plt.show()


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


# Compute correlation
print(df.corr(method='pearson'))

# print("df_clean:", cum_return)  # higher standard deviation mean the price flucate a lot over time
