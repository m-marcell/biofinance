import lseg.data as ld
from lseg.data.discovery import Chain
import pandas

ld.open_session()

# Nézd meg a workspace code creator funkciót!

# Fetch data from LSEG
# Fusson a háttérbe a workspace!!
print("Working ...")


ric = ".FTSE"
start = "2013-01-01"
end = "2025-12-31"

# Az indexből csinál Chain objektumot az adatlekéréshez
index_chain = Chain(f"0#{ric}")
print(index_chain.constituents)

'''
# Tickerer rendezése
const_data = ld.content.symbol_conversion.Definition(
    index_chain.constituents).get_data()
const_data.data.df.to_csv("data/symbology.csv")
'''

# Legutolsó ESG adatok (éves bontás majd később)
fields = [
    "TR.ExchangeCountry",
    "TR.HeadquartersCountry",
    "TR.GICSSector",
    "TR.TRESGScore.date",
    "TR.TRESGScore",              # ESG Combined Score
    "TR.EnvironmentPillarScore.date",  # Environmental
    "TR.EnvironmentPillarScore",  # Environmental
    "TR.SocialPillarScore.date",       # Social
    "TR.SocialPillarScore",
    "TR.GovernancePillarScore.date",
    "TR.GovernancePillarScore"
]

esg_data = ld.get_data(
    universe=index_chain,
    fields=fields
)
esg_data.to_csv("data/raw/esg_latest.csv")

ld.close_session()

print("Finished!")
