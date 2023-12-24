import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime
from datetime import timedelta


def get_portfolio():
    stock_list = [] # Store Portfolio Stock Symbols
    share_list = [] # Store how many shares of each stock we have

    while True:
        stock_symbol = input("Input Stock Ticker Symbol (Example: Apple -> AAPL) or enter lowercase 'q': ")
        if stock_symbol == "q":
            break
        try:
            stock_shares = float(input("Input amount of stocks you hold in shares: "))
        except ValueError:
            print("Invalid input. Defaulting to 1 share.")
            stock_shares = 1
        stock_list.append(stock_symbol)
        share_list.append(stock_shares)
        
    return stock_list, share_list
    
def stock_simulation(stock_list, share_list):
    today = datetime.today().strftime('%Y-%m-%d')
    ten_years_past = (datetime.today() - timedelta(days=365*10)).strftime('%Y-%m-%d')

    #today = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    #ten_years_past = (datetime.today() - timedelta(days=365*11)).strftime('%Y-%m-%d')
    
    current_port_price = 0
    potential_price = 0

    for i, stock_symbol in enumerate(stock_list):
        try:
            stock = yf.Ticker(stock_symbol)
            stock_shares = share_list[i]

            # Get the historic data of the past ten years for the stock
            stock_hist = stock.history(start=ten_years_past ,end=today)

            # Add the percent change value into the data frame
            stock_hist["Daily Return"] = stock_hist["Close"].pct_change()

            # Calculate the values needed for the geometric Brownian motion calculation
            expected_return = stock_hist["Daily Return"].mean()
            expected_volatility = stock_hist["Daily Return"].std()

            # Plotting the closing prices
            plt.figure(figsize=(12, 6))
            plt.plot(stock_hist.index, stock_hist['Close'], label=f'{stock_symbol} Closing Price')
            plt.title(f'{stock_symbol} Closing Price Over Time')
            plt.xlabel('Date')
            plt.ylabel('Closing Price (USD)')
            plt.legend()

            # Save the plot as a PNG image with a customized file name
            plt.savefig(f'{stock_symbol}_closing_price.png')
            plt.close()  # Close the plot to prevent it from being displayed

            todayPrice = stock_hist["Close"].iloc[-1]
            stock_value = todayPrice * stock_shares
            current_port_price += stock_value

            simulatedPrice = np.zeros((100, 1 + 365))
            simulatedPrice[:, 0] = todayPrice

            dt = 1

            for j in range(100):
                for k in range(365):
                    drift = expected_return * dt
                    shock = expected_volatility * np.sqrt(dt) * np.random.normal()
                    simulatedPrice[j, k+1] = simulatedPrice[j, k] * np.exp(drift + shock)
                    
            # Calculate the average of all simulations at each time step
            average_simulated_price = np.mean(simulatedPrice, axis=0)

            # Print the last value of the average_simulated_price
            last_value = average_simulated_price[-1]
            simulated_value = last_value * stock_shares
            potential_price += simulated_value
            pct_change = (simulated_value / stock_value) * 100
            print()
            print("Last Value of Average Simulated Price:", last_value)
            print(stock_symbol, ": Todays Value = ", stock_value, " Simulated Value in 1 year = ", simulated_value, "Percent Change = ", pct_change, "%")
            print()

            # Plotting the simulated price paths
            plt.figure(figsize=(12, 6))
            plt.plot(np.arange(0, 365 + 1) * dt, simulatedPrice.T, color='blue', alpha=0.1)
            plt.plot(np.arange(0, 365 + 1) * dt, average_simulated_price, color='red', label='Average Simulation')
            plt.title(f'{stock_symbol} Closing Price Over Time')
            plt.xlabel('Time Steps')
            plt.ylabel('Simulated Stock Price')

            # Save the plot as a PNG image with a customized file name
            plt.savefig(f'{stock_symbol}_monte_carlo_simulation.png')
            plt.close()  # Close the plot to prevent it from being displayed
        except Exception as e:
            print(f"An error occurred while processing {stock_symbol}: {e}")
    return current_port_price, potential_price


def main():
    stock_list, share_list = get_portfolio()
    
    current_port_price, potential_price = stock_simulation(stock_list, share_list)

    print()
    print("Your Current Portfolio Value = ", current_port_price)
    print("Potential Portfolio Value in 1 Year = ", potential_price)
    print("Percent Change: ", (potential_price / current_port_price) * 100, "%")

if __name__ == "__main__":
    main()