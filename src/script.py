import lseg.data as ld
from lseg.data.discovery import Chain
import pandas
import download_functions as dwnld

# "Controlled flight into terrain"

ld.open_session()

# Nézd meg a workspace code creator funkciót!

# Fetch data from LSEG
# Fusson a háttérbe a workspace!!

# ric = ".STOXX50"
ric = [
    "ALVG.DE",
    "ZURN.S",
    "BBVA.MC",
    "REL.L",
    "HSBA.L",
    "RR.L",
    "AXAF.PA",
    "ENEI.MI",
    "SASY.PA",
    "ASML.AS",
    "ULVR.L",
    "UBSG.S",
    "CRDI.MI",
    "RIO.L",
    "TTEF.PA",
    "AZN.L",
    "BATS.L",
    "ESLX.PA",
    "INGA.AS",
    "ROPC.S",
    "NOVN.S",
    "ISP.MI",
    "PRX.AS",
    "SHEL.AS",
    "NG.L",
    "AIR.PA",
    "OREP.PA",
    "LSEG.L",
    "ENR1n.DE",
    "SAPG.DE",
    "ABBN.S",
    "CFR.S",
    "AIRP.PA",
    "DTEGn.DE",
    "ABI.BR",
    "SCHN.PA",
    "BNPP.PA",
    "NOVOb.CO",
    "IBE.MC",
    "RHMG.DE",
    "LVMH.PA",
    "MUVGn.DE",
    "BP.L",
    "SAN.MC",
    "GSK.L",
    "SIEGn.DE",
    "HRMS.PA",
    "NESN.S",
    "SAF.PA",
    "SGEF.PA"
]
start = "2013-01-01"
end = "2025-12-31"

print(f"Downloading data for RIC:\n{ric}")

# Az indexből csinál Chain objektumot az adatlekéréshez
# index_chain = Chain(f"0#{ric}")     # Mi legyen a kezdeti időpont?
# print(index_chain.constituents)


# dwnld.symbol_conversion(ric)

dwnld.fundamentals_download(ric)

# dwnld.esg_download(ric)


ld.close_session()

print("Finished!")
