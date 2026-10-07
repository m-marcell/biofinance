import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# LSEG Worlspace API
#
# import lseg_download
# lseg_download.download(output="../data/close_prices.csv")

# STOXX 600, RIC: .STOXX, ISIN: EU0009658202, Ticker: SXXP
# stock data closing prices from 2020-09-01 to 2026-09-01

stock_info = pd.read_excel("../data/stoxx600_esg_biodiv_raw.xlsx")
stock_data = pd.read_csv("../data/close_prices.csv")

# missing values
stock_data.ffill(inplace=True)
stock_info.dropna(
    subset=["LSEG ESG Score Plus 2026"], inplace=True
)  # drop stocks where lseg esg 2026 is null
stock_data.dropna(
    axis=1, inplace=True
)  # drop stocks where there is no data for the 6y period
usd_drop = stock_info[stock_info["Currency of Exchange"] == "USD"].index
stock_info.drop(usd_drop, inplace=True)

stock_info["Biodiversity Targets"] = stock_info["Biodiversity Targets"].astype("bool")
stock_info["Biodiversity Impact Reduction"] = stock_info[
    "Biodiversity Impact Reduction"
].astype("bool")
stock_info["Biodiversity Risk Assessment"] = stock_info[
    "Biodiversity Risk Assessment"
].astype("bool")
stock_info["Biodiversity Risk Management Integration"] = stock_info[
    "Biodiversity Risk Management Integration"
].astype("bool")
stock_info["Biodiversity Due Diligence"] = stock_info[
    "Biodiversity Due Diligence"
].astype(
    "bool"
)  # concert to boolean

stock_data["Date"] = pd.to_datetime(stock_data["Date"])

# index changes
stock_data.set_index("Date", inplace=True)
stock_info.set_index("RIC", inplace=True)


ric_list_data = sorted(stock_data.columns.values.tolist())
ric_list_info = sorted(stock_info.index.tolist())
present_in_both = list(set(ric_list_data) & set(ric_list_info))

print(f"Number of RICs in both:\n{len(present_in_both)}")
print(stock_info.value_counts("Currency of Exchange"))

print(stock_info.info())

##### PLOTTING #####

labels = np.arange(6)
a2026 = stock_info.value_counts("Biodiversity Theme Score 2026", sort=True)
a2025 = stock_info.value_counts("Biodiversity Theme Score 2025", sort=True)
a2024 = stock_info.value_counts("Biodiversity Theme Score 2024", sort=True)

plt.bar(labels - 0.2, a2024, 0.2)
plt.bar(labels, a2025, 0.2)
plt.bar(labels + 0.2, a2026, 0.2)
plt.xlabel("Biodiversity Theme Score")
plt.ylabel("Number of data points")
plt.legend(["2024","2025","2026"])

plt.savefig("../src/plots/biodiv_theme.pdf")
