**** Run analysis ****;

*Set relevant path;

cd "C:\Stata\Replication Package Biodiversity Finance\" 

log using log\results.log, replace

*Tables and figures in the main text;

use data\pseudo_dataset.dta, clear
keep if inportfolio == 1 /* Restrict to 33 in-portfolio deals */

*Table 1 does not use data;

*Table 2 does not use data;

*Table 3;

gen naturalasset = "land" if assetclass == "Agriculture: soil and pollinators" | assetclass == "Forests" | assetclass == "Natural parks & wildlife protection" | assetclass == "Genetic resources"
replace naturalasset = "sea" if assetclass == "Watersheds" | assetclass == "Coastal ecosystems" | assetclass == "Fisheries" | assetclass == "Oceans (incl. coral reef)"

tab naturalasset
tab assetclass if naturalasset == "land"
tab assetclass if naturalasset == "sea"

tab naturalasset if blended == 1
tab assetclass if naturalasset == "land" & blended == 1
tab assetclass if naturalasset == "sea" & blended == 1

tab naturalasset if blended == 0
tab assetclass if naturalasset == "land" & blended == 0
tab assetclass if naturalasset == "sea" & blended == 0

*Table 4;

gen continent = "Africa" if country == "Ghana" | country == "Ivory Coast" | country == "Kenya" | country == "Madagascar" | country == "Morocco"
replace continent = "Asia" if country == "Bhutan" | country == "India" | country == "Indonesia" | country == "Laos" | country == "Philippines" | country == "Vietnam" | country == "Asia (multiple countries)" 
replace continent = "Europe" if country == "France" | country == "Norway" | country == "United Kingdom" 
replace continent = "Latin America and Caribbean" if country == "Bahamas" | country == "Brazil" | country == "Colombia" | country == "Costa Rica" | country == "Mexico" | country == "Nicaragua" | country == "Peru" 
replace continent = "Oceania" if country == "Australia" 
replace continent = "Multiple continents" if  country == "Multiple continents" 

tab continent
tab country if continent == "Africa"
tab country if continent == "Asia"
tab country if continent == "Europe"
tab country if continent == "Latin America and Caribbean"
tab country if continent == "Oceania"
tab country if continent == "Multiple continents"

tab continent if blended == 1
tab country if continent == "Africa" & blended == 1
tab country if continent == "Asia" & blended == 1
tab country if continent == "Europe" & blended == 1
tab country if continent == "Latin America and Caribbean" & blended == 1
tab country if continent == "Oceania" & blended == 1
tab country if continent == "Multiple continents" & blended == 1

tab continent if blended == 0
tab country if continent == "Africa" & blended == 0
tab country if continent == "Asia" & blended == 0
tab country if continent == "Europe" & blended == 0
tab country if continent == "Latin America and Caribbean" & blended == 0
tab country if continent == "Oceania" & blended == 0
tab country if continent == "Multiple continents" & blended == 0

*Table 5;

tab investmenttype
tab investmenttype if blended == 1 
tab investmenttype if blended == 0

*Table 6;

**Panel A;

gen equity_pct = equity/ticketsize
gen debt_pct = debt/ticketsize
gen verpa_pct = verpa/ticketsize

sum maturity dealsize ticketsize equity debt verpa equity_pct debt_pct verpa_pct

sum maturity dealsize ticketsize equity debt verpa equity_pct debt_pct verpa_pct if blended == 1
sum maturity dealsize ticketsize equity debt verpa equity_pct debt_pct verpa_pct if blended == 0

ttest maturity, by(blended)
ttest dealsize, by(blended)
ttest ticketsize, by(blended)
ttest equity, by(blended)
ttest debt, by(blended)
ttest verpa, by(blended)
ttest equity_pct, by(blended)
ttest debt_pct, by(blended)
ttest verpa_pct, by(blended)

**Panel B;

gen sharperatio = irr/irrstd

sum irr irrstd sharperatio

sum irr irrstd sharperatio if blended == 1
sum irr irrstd sharperatio if blended == 0

ttest irr, by(blended)
ttest irrstd, by(blended)
ttest sharperatio, by(blended)

**Panel C;

sum impactarea emissions beneficiaries jobs certification

sum impactarea emissions beneficiaries jobs certification if blended == 1
sum impactarea emissions beneficiaries jobs certification if blended == 0

ttest impactarea, by(blended)
ttest emissions, by(blended)
ttest beneficiaries, by(blended)
ttest jobs, by(blended)
ttest certification, by(blended)

gen limpactarea = log(impactarea)
ttest limpactarea, by(blended)

**Panel D;

gen impactarea_rel = impactarea/dealsize
gen emissions_rel = emissions/dealsize
gen beneficiaries_rel = beneficiaries/dealsize
gen jobs_rel = jobs/dealsize

sum impactarea_rel emissions_rel beneficiaries_rel jobs_rel

sum impactarea_rel emissions_rel beneficiaries_rel jobs_rel if blended == 1
sum impactarea_rel emissions_rel beneficiaries_rel jobs_rel if blended == 0

ttest impactarea_rel, by(blended)
ttest emissions_rel, by(blended)
ttest beneficiaries_rel, by(blended)
ttest jobs_rel, by(blended)

**Panel E;

sum factfinding

sum factfinding if blended == 1
sum factfinding if blended == 0

ttest factfinding, by(blended)

*Table 7 does not use data;

*Table 8;

use data\pseudo_dataset.dta, clear

sum irr impactarea emissions beneficiaries jobs if inportfolio == 1
sum irr impactarea emissions beneficiaries jobs if inportfolio == 0

ttest irr, by(inportfolio)
ttest impactarea, by(inportfolio)
ttest emissions, by(inportfolio)
ttest beneficiaries, by(inportfolio)
ttest jobs, by(inportfolio)

gen limpactarea = log(impactarea)
ttest limpactarea, by(inportfolio)

*Figure 1 does not use data;

*Figure 2 does not use data;

*Figure 3 does not use data;

*Figure 4 plots the statistics from Table 4 (using map charts in Microsoft Excel);

*Figure 5 plots the statistics from Table 4 (using map charts in Microsoft Excel);

*Figure 6;

use data\pseudo_dataset.dta, clear
keep if inportfolio == 1 /* Restrict to 33 in-portfolio deals */

gen impactarea0rel = impactarea0/impactarea
gen impactarea1rel = impactarea1/impactarea
gen impactarea2rel = impactarea2/impactarea
gen impactarea3rel = impactarea3/impactarea

sum impactarea0rel impactarea1rel impactarea2rel impactarea3rel

gen emissions0rel = emissions0/emissions
gen emissions1rel = emissions1/emissions
gen emissions2rel = emissions2/emissions
gen emissions3rel = emissions3/emissions

sum emissions0rel emissions1rel emissions2rel emissions3rel

gen beneficiaries0rel = beneficiaries0/beneficiaries
gen beneficiaries1rel = beneficiaries1/beneficiaries
gen beneficiaries2rel = beneficiaries2/beneficiaries
gen beneficiaries3rel = beneficiaries3/beneficiaries

sum beneficiaries0rel beneficiaries1rel beneficiaries2rel beneficiaries3rel

gen jobs0rel = jobs0/jobs
gen jobs1rel = jobs1/jobs
gen jobs2rel = jobs2/jobs
gen jobs3rel = jobs3/jobs

sum jobs0rel jobs1rel jobs2rel jobs3rel

*Tables in Online Appendix;

*Table A1 does not use data;

*Table A2;

gen naturalasset = "land" if assetclass == "Agriculture: soil and pollinators" | assetclass == "Forests" | assetclass == "Natural parks & wildlife protection" | assetclass == "Genetic resources"
replace naturalasset = "sea" if assetclass == "Watersheds" | assetclass == "Coastal ecosystems" | assetclass == "Fisheries" | assetclass == "Oceans (incl. coral reef)"

gen continent = "Africa" if country == "Ghana" | country == "Ivory Coast" | country == "Kenya" | country == "Madagascar" | country == "Morocco"
replace continent = "Asia" if country == "Bhutan" | country == "India" | country == "Indonesia" | country == "Laos" | country == "Philippines" | country == "Vietnam" | country == "Asia (multiple countries)" 
replace continent = "Europe" if country == "France" | country == "Norway" | country == "United Kingdom" 
replace continent = "Latin America and Caribbean" if country == "Bahamas" | country == "Brazil" | country == "Colombia" | country == "Costa Rica" | country == "Mexico" | country == "Nicaragua" | country == "Peru" 
replace continent = "Oceania" if country == "Australia" 
replace continent = "Multiple continents" if  country == "Multiple continents" 

by naturalasset, sort: sum irr 
by continent, sort: sum irr 
by investmenttype, sort: sum irr 

*Table A3;

ssc install labsumm

*Panel A (ESG assessment);

labsumm esg1-esg14
labsumm esg1-esg14 if blended == 1
labsumm esg1-esg14 if blended == 0

*Panel B (ESG risk assessment);

labsumm esg_ra1-esg_ra19
labsumm esg_ra1-esg_ra19 if blended == 1
labsumm esg_ra1-esg_ra19 if blended == 0

*Panel C (ESG risk management);

labsumm esg_rm1-esg_rm19
labsumm esg_rm1-esg_rm19 if blended == 1
labsumm esg_rm1-esg_rm19 if blended == 0

*Table A4;

gen impactarea_rel = impactarea3rel
replace impactarea_rel = impactarea2rel if impactarea_rel == .
replace impactarea_rel = impactarea1rel if impactarea_rel == .
replace impactarea_rel = impactarea0rel if impactarea_rel == .

sum impactarea_rel
sum impactarea_rel if blended == 1
sum impactarea_rel if blended == 0

ttest impactarea_rel, by(blended)

gen emissions_rel = emissions3rel
replace emissions_rel = emissions2rel if emissions_rel == .
replace emissions_rel = emissions1rel if emissions_rel == .
replace emissions_rel = emissions0rel if emissions_rel == .

sum emissions_rel
sum emissions_rel if blended == 1
sum emissions_rel if blended == 0

ttest emissions_rel, by(blended)

gen beneficiaries_rel = beneficiaries3rel
replace beneficiaries_rel = beneficiaries2rel if beneficiaries_rel == .
replace beneficiaries_rel = beneficiaries1rel if beneficiaries_rel == .
replace beneficiaries_rel = beneficiaries0rel if beneficiaries_rel == .

sum beneficiaries_rel
sum beneficiaries_rel if blended == 1
sum beneficiaries_rel if blended == 0

ttest beneficiaries_rel, by(blended)

gen jobs_rel = jobs3rel
replace jobs_rel = jobs2rel if jobs_rel == .
replace jobs_rel = jobs1rel if jobs_rel == .
replace jobs_rel = jobs0rel if jobs_rel == .

sum jobs_rel
sum jobs_rel if blended == 1
sum jobs_rel if blended == 0

ttest jobs_rel, by(blended)

*Table A5 does not use data;

log close

************************;
