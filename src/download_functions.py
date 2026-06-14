import lseg.data as ld
import pandas


def symbol_conversion(ric):
    # Tickerer rendezése
    const_data = ld.content.symbol_conversion.Definition(
        ric).get_data()
    const_data.data.df.to_csv("../data/raw/symbology.csv")

    return


def fundamentals_download(ric):
    # Legutolsó ESG adatok (éves bontás majd később)
    fields = [
        "TR.TickerSymbol",
        "TR.ISIN",
        "TR.ExchangeCode",
        "TR.ExchangeCountry",
        "TR.HeadquartersCountry",
        "TR.GICSSector",
        "TR.GICSSectorCode",
        "TR.GICSIndustry",
        "TR.GICSIndustryCode",
        "TR.GICSSubindustry",
    ]

    fundamentals = ld.get_data(
        universe=ric,
        fields=fields
    )
    fundamentals.to_csv("../data/raw/fundamentals.csv")

    return


def esg_download(ric):
    # Legutolsó ESG adatok (éves bontás majd később)
    fields = [
        "TR.TickerSymbol",
        "TR.ESGScore.date",
        "TR.ESGScore",              # ESG Combined Score
        "TR.EnvironmentPillarESGScore.date",  # Environmental
        "TR.EnvironmentPillarESGScore",  # Environmental
        "TR.SocialPillarESGScore.date",       # Social
        "TR.SocialPillarESGScore",
        "TR.GovernancePillarESGScore.date",
        "TR.GovernancePillarESGScore",
        # Green revenue
        "TR.CompanyGreenRevenuePercentage",
        "TR.EstimatedEUTaxonomyAlignedCompanyGreenRevenuePercentage",
        # Biodiversity
        "TR.BiodiversityTargets",
        "TR.BiodiversityCommitment",
        "TR.BiodiversityImpactReductionScore",
        "TR.RecentBiodiversityAndEcosistemControversies",
        # LSEG ESG new scores
        "TR.BiodiversityThemeScore",
        "TR.BiodiversityThemeMaterialityLevel",
        "TR.ClimateTransitionThemeScore",
        "TR.ClimateTransitionThemeMaterialityLevel"

    ]

    esg_data = ld.get_data(
        universe=ric,
        fields=fields
    )
    esg_data.to_csv("../data/raw/esg_latest.csv")

    return


def historic_price_download(ric):
    for asset in ric:
        # Historic price letöltés
        break

    return
