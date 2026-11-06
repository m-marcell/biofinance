import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import esgsr
import markowitz

# LSEG Worlspace API
#
# import lseg_download
# lseg_download.download(output="../data/close_prices.csv")

# STOXX 600, RIC: .STOXX, ISIN: EU0009658202, Ticker: SXXP
# stock data closing prices from 2019-09-02 to 2026-09-01

download_date = datetime.date(2026, 9, 27)
stock_info = pd.read_excel("../data/stoxx600_esg_biodiv_raw.xlsx")
stock_data = pd.read_csv("../data/close_prices_new.csv")

# missing values, filtering
stock_data.ffill(inplace=True)
stock_info.dropna(subset=["LSEG ESG Score Plus 2026"], inplace=True)
stock_info.dropna(subset=["LSEG ESG Score Plus 2025"], inplace=True)
stock_info.dropna(subset=["LSEG ESG Score Plus 2024"], inplace=True)
stock_info.dropna(subset=["Company Market Cap EUR"], inplace=True)

stock_data.dropna(
    axis=1, inplace=True
)  # drop stocks where there is no data for the 6y period
usd_drop = stock_info[stock_info["Currency of Exchange"] == "USD"].index
print(f"{len(usd_drop)} USA stocks dropped")
stock_info.drop(index=usd_drop, inplace=True)

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
].astype("bool")

stock_data["Date"] = pd.to_datetime(stock_data["Date"], unit="D", origin="1899-12-30")

# index changes
stock_data.set_index("Date", inplace=True)
stock_info.set_index("RIC", inplace=True)

# Only keep EUR stocks
stock_info = stock_info[stock_info["Currency of Exchange"] == "EUR"]

# Only keep RIC's present in both datasets after filtering
ric_list_data = sorted(stock_data.columns.values.tolist())
ric_list_info = sorted(stock_info.index.tolist())
present_in_both = list(set(ric_list_data) & set(ric_list_info))
delete_from_data = list(set(ric_list_data) - set(present_in_both))

print(f"Number of RICs in both:\n{len(present_in_both)}")

stock_info = stock_info[stock_info.index.isin(present_in_both)]
stock_data.drop(delete_from_data, axis=1, inplace=True)

if sorted(stock_info.index.tolist()) == sorted(stock_data.columns.values.tolist()):
    print(True)


##### FIRST RESULTS
print(stock_info.info())
print(stock_info.value_counts("Currency of Exchange"))
print(stock_info.value_counts("Biodiversity Theme Score 2026"))
print(f"Biodiv 2026 average: {stock_info["Biodiversity Theme Score 2026"].mean()}")
print(
    stock_info.groupby("GICS Sector Name")["Biodiversity Theme Score 2026"]
    .mean()
    .to_latex(caption="Biodiverzitási mutatók átlaga iparáganként")
)


prices2026 = stock_data["2019-09-01":"2024-08-31"]
prices2025 = stock_data["2020-09-01":"2025-08-31"]
prices2024 = stock_data["2021-09-01":"2026-08-31"]

##### BIODIV-SR #####
# res = markowitz.optimize_portfolio(stock_data)
# print(res)

mu, sigma, s, names = esgsr.prepare_inputs(
    prices2026,
    stock_info,
    esg_col="Biodiversity Theme Score 2026",
    rf_annual=0.02,
    zscore_esg=True,
)
frontier2026, weights2026 = esgsr.esg_sr_frontier(mu, sigma, s, tickers=names)
mu, sigma, s, names = esgsr.prepare_inputs(
    prices2025,
    stock_info,
    esg_col="Biodiversity Theme Score 2025",
    rf_annual=0.02,
    zscore_esg=True,
)
frontier2025, weights2025 = esgsr.esg_sr_frontier(mu, sigma, s, tickers=names)
mu, sigma, s, names = esgsr.prepare_inputs(
    prices2024,
    stock_info,
    esg_col="Biodiversity Theme Score 2024",
    rf_annual=0.02,
    zscore_esg=True,
)
frontier2024, weights2024 = esgsr.esg_sr_frontier(mu, sigma, s, tickers=names)

frontier2024.plot(y="sharpe", label="2024")
plt.savefig("../tex/szakdolgozat/img/biodiv-sr2024.pdf")
frontier2025.plot(y="sharpe", label="2025")
plt.savefig("../tex/szakdolgozat/img/biodiv-sr2025.pdf")
frontier2026.plot(y="sharpe", label="2026")
plt.savefig("../tex/szakdolgozat/img/biodiv-sr2026.pdf")

# plt.savefig("../src/biodiv-sr.pdf")

##### PLOTTING #####

# labels = np.arange(6)
# b2026 = stock_info.value_counts("Biodiversity Theme Score 2026", sort=True)
# b2025 = stock_info.value_counts("Biodiversity Theme Score 2025", sort=True)
# b2024 = stock_info.value_counts("Biodiversity Theme Score 2024", sort=True)
#
# plt.bar(labels - 0.2, b2024, 0.2)
# plt.bar(labels, b2025, 0.2)
# plt.bar(labels + 0.2, b2026, 0.2)
# plt.xlabel("Biodiversity Theme Score")
# plt.ylabel("Number of data points")
# plt.legend(["2024", "2025", "2026"])
#
# plt.show()
# plt.savefig("../src/plots/biodiv_theme.pdf")


stock_data.to_csv("../data/stock_data_out.csv")
stock_info.to_csv("../data/stock_info_out.csv")
