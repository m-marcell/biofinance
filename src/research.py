import matplotlib.pyplot as plt
import pandas as pd

# STOXX 600, RIC: .STOXX, ISIN: EU0009658202, Ticker: SXXP
# stock data closing prices from 2020-09-01 to 2026-09-01

df = pd.read_excel("../data/stoxx600_esg_biodiv_raw.xlsx")
stock_data = pd.read_csv("../data/close_prices.csv")

print(df.head())
print(stock_data.head())
