import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime
from datetime import timedelta

today = datetime.today().strftime('%Y-%m-%d')
ten_years_past = (datetime.today() - timedelta(days=365*10)).strftime('%Y-%m-%d')

#today = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
#ten_years_past = (datetime.today() - timedelta(days=365*11)).strftime('%Y-%m-%d')

aapl = yf.Ticker('AAPL')

aapl_hist = aapl.history(start=ten_years_past ,end=today)

aapl_hist["Daily Return"] = aapl_hist["Close"].pct_change()

expected_return = aapl_hist["Daily Return"].mean()
print(expected_return)
expected_volatility = aapl_hist["Daily Return"].std()
print(expected_volatility)

print(aapl_hist.head(10))
print(aapl_hist.tail(10))

# Plotting the closing prices
plt.figure(figsize=(12, 6))
plt.plot(aapl_hist.index, aapl_hist['Close'], label='AAPL Closing Price')
plt.title('AAPL Closing Price Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price (USD)')
plt.legend()
plt.show()

todayPrice = aapl_hist["Close"].iloc[-1]

simulatedPrice = np.zeros((100, 1 + 365))
simulatedPrice[:, 0] = todayPrice

dt = 1

for i in range(100):
    for j in range(365):
        drift = expected_return * dt
        shock = expected_volatility * np.sqrt(dt) * np.random.normal()
        simulatedPrice[i, j+1] = simulatedPrice[i, j] * np.exp(drift + shock)
        
# Calculate the average of all simulations at each time step
average_simulated_price = np.mean(simulatedPrice, axis=0)

# Print the last value of the average_simulated_price
last_value = average_simulated_price[-1]
print("Last Value of Average Simulated Price:", last_value)

# Plotting the simulated price paths
plt.figure(figsize=(12, 6))
plt.plot(np.arange(0, 365 + 1) * dt, simulatedPrice.T, color='blue', alpha=0.1)
plt.plot(np.arange(0, 365 + 1) * dt, average_simulated_price, color='red', label='Average Simulation')
plt.title('Monte Carlo Simulation of AAPL Stock Price Paths')
plt.xlabel('Time Steps')
plt.ylabel('Simulated Stock Price')
plt.show()