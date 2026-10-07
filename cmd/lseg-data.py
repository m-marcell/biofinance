import lseg.data as ld

ld.open_session()

df = ld.get_data(
    universe=["AAPL.O", "MSFT.O"],
    fields=["TR.PriceClose", "TR.Volume"]
)

print(df)

ld.close_session()
