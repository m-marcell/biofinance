**** Generate Pseudo Dataset ****;

*Set relevant path;

cd "C:\Stata\Replication Package Biodiversity Finance\" 

log using log\simulation.log, replace

*Bidodiversity deals;

clear

set obs 65
gen dealid = _n

gen inportfolio = (_n <= 33) /* 33 deals in portfolio; 32 discarded deals (65 in total) */

gen blended = (_n <= 14) /* out of the 33 deals in portfolio, 14 are blended finance deals */
replace blended = . if inportfolio == 0

*Distribute the 8 different asset classes;

set seed 1234

gen var1 = 1 + int(runiform(0,8)) /* random variables that takes on values 1, 2, ..., 8 */

gen assetclass = "Agriculture: soil and pollinators" if var1 == 1
replace assetclass = "Forests" if var1 == 2
replace assetclass = "Natural parks & wildlife protection" if var1 == 3
replace assetclass = "Genetic resources" if var1 == 4
replace assetclass = "Watersheds" if var1 == 5
replace assetclass = "Coastal ecosystems" if var1 == 6
replace assetclass = "Fisheries" if var1 == 7
replace assetclass = "Oceans (incl. coral reef)" if var1 == 8

*Distribute the 24 countries;

gen var2 = 1 + int(runiform(0,24)) /* random variables that takes on values 1, 2, ..., 24 */

gen country = "Ghana" if var2 == 1
replace country = "Ivory Coast" if var2 == 2
replace country = "Kenya" if var2 == 3
replace country = "Madagascar" if var2 == 4
replace country = "Morocco" if var2 == 5
replace country = "Bhutan" if var2 == 6
replace country = "India" if var2 == 7
replace country = "Indonesia" if var2 == 8
replace country = "Laos" if var2 == 9
replace country = "Philippines" if var2 == 10
replace country = "Vietnam" if var2 == 11
replace country = "Asia (multiple countries)" if var2 == 12
replace country = "France" if var2 == 13
replace country = "Norway" if var2 == 14
replace country = "United Kingdom" if var2 == 15
replace country = "Bahamas" if var2 == 16
replace country = "Brazil" if var2 == 17
replace country = "Colombia" if var2 == 18
replace country = "Costa Rica" if var2 == 19
replace country = "Mexico" if var2 == 20
replace country = "Nicaragua" if var2 == 21
replace country = "Peru" if var2 == 22
replace country = "Australia" if var2 == 23
replace country = "Multiple continents" if var2 == 24

*Distribute the 7 investment types;

gen var3 = 1 + int(runiform(0,7)) /* random variables that takes on values 1, 2, ..., 7 */

gen investmenttype = "Equity" if var3 == 1
replace investmenttype = "Equity + Debt" if var3 == 2
replace investmenttype = "Equity + Debt with profit sharing" if var3 == 3
replace investmenttype = "Equity + VERPA" if var3 == 4
replace investmenttype = "Debt" if var3 == 5
replace investmenttype = "Debt with profit sharing" if var3 == 6
replace investmenttype = "VERPA" if var3 == 7

replace investmenttype = "" if inportfolio == 0

drop var1 var2 var3

*Generate deal characteristics;
	
	/*	All continuous variables are generated using uniform distributions centered at
		the mean in the actual data and in the range of positive numbers.
		Specifically, for a given mean, the distribution is U[0, 2*mean]. */
	
gen maturity = runiform(0, 2*7.94)
gen dealsize = runiform(0, 2*22.84)

gen equity = runiform(0, 2*3.21)
gen debt = runiform(0, 2*2.79)
gen verpa = runiform(0, 2*0.62)
gen ticketsize = equity + debt + verpa

gen irr = runiform(0, 2*13.52)
gen irrstd = runiform(0, 2*6.55)

gen impactarea = runiform(0, 2*73408)
gen emissions = runiform(0, 2*5665)
gen beneficiaries = runiform(0, 2*11623)
gen jobs = runiform(0, 2*1846)
gen certification = round(runiform(0, 1)) /* dummy variable */

gen factfinding = round(runiform(0, 1)) if blended == 1 /* dummy variable (among blended deals) */
replace factfinding = 0 if factfinding == .

replace maturity = . if inportfolio == 0
replace dealsize = . if inportfolio == 0
replace equity = . if inportfolio == 0
replace debt = . if inportfolio == 0
replace verpa = . if inportfolio == 0
replace ticketsize = . if inportfolio == 0
replace irrstd = . if inportfolio == 0
replace certification = . if inportfolio == 0
replace factfinding = . if inportfolio == 0

*Impact over time;

gen impactarea0 = impactarea*runiform(0, 2*0.053) if inportfolio == 1
gen impactarea1 = impactarea*runiform(0, 2*0.095) if inportfolio == 1
gen impactarea2 = impactarea*runiform(0, 2*0.132) if inportfolio == 1
gen impactarea3 = impactarea*runiform(0, 2*0.167) if inportfolio == 1

gen emissions0 = emissions*runiform(0, 2*0.022) if inportfolio == 1
gen emissions1 = emissions*runiform(0, 2*0.083) if inportfolio == 1
gen emissions2 = emissions*runiform(0, 2*0.113) if inportfolio == 1
gen emissions3 = emissions*runiform(0, 2*0.128) if inportfolio == 1

gen beneficiaries0 = beneficiaries*runiform(0, 2*0.332) if inportfolio == 1
gen beneficiaries1 = beneficiaries*runiform(0, 2*0.666) if inportfolio == 1
gen beneficiaries2 = beneficiaries*runiform(0, 2*0.670) if inportfolio == 1
gen beneficiaries3 = beneficiaries*runiform(0, 2*0.764) if inportfolio == 1

gen jobs0 = jobs*runiform(0, 2*0.266) if inportfolio == 1
gen jobs1 = jobs*runiform(0, 2*0.399) if inportfolio == 1
gen jobs2 = jobs*runiform(0, 2*0.451) if inportfolio == 1
gen jobs3 = jobs*runiform(0, 2*0.541) if inportfolio == 1

*ESG assessments;

gen esg1 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg2 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg3 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg4 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg5 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg6 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg7 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg8 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg9 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg10 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg11 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg12 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg13 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg14 = 1 + int(runiform(0,3)) if inportfolio == 1

label variable esg1 "Sustainability"
label variable esg2 "Environmental"
label variable esg3 "Social"
label variable esg4 "Governance"
label variable esg5 "Natural ecosystems"
label variable esg6 "Sustainable product lands & seascapes"
label variable esg7 "Climate change mitigation"
label variable esg8 "Circular economy"
label variable esg9 "Socio-economic development"
label variable esg10 "Livelihoods and decent work"
label variable esg11 "Climate adaptation"
label variable esg12 "Inclusion"
label variable esg13 "Quality of I&ESG management"
label variable esg14 "Business ethics"

gen esg_ra1 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra2 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra3 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra4 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra5 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra6 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra7 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra8 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra9 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra10 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra11 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra12 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra13 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra14 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra15 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra16 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra17 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra18 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_ra19 = 1 + int(runiform(0,3)) if inportfolio == 1

label variable esg_ra1 "ESG risk"
label variable esg_ra2 "Environmental risk"
label variable esg_ra3 "Social risk"
label variable esg_ra4 "Governance risk"
label variable esg_ra5 "Country risk and governance risk"
label variable esg_ra6 "Business ethics risk"
label variable esg_ra7 "Legal and regulatory E&S compliance risk"
label variable esg_ra8 "Certifications and standards risk"
label variable esg_ra9 "Environmental and social assessment and management risk"
label variable esg_ra10 "Pollution control, energy and water use risk"
label variable esg_ra11 "Biodiversity conservation risk"
label variable esg_ra12 "Human resources policies & procedures risk"
label variable esg_ra13 "Health & safety at work risk"
label variable esg_ra14 "Community health, safety and security risk"
label variable esg_ra15 "Land tenure and land use change risk"
label variable esg_ra16 "Indigenous peoples' rights and interests risk"
label variable esg_ra17 "Stakeholder engagement and grievance management risk"
label variable esg_ra18 "Gender risk"
label variable esg_ra19 "Cultural heritage risk"

gen esg_rm1 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm2 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm3 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm4 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm5 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm6 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm7 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm8 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm9 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm10 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm11 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm12 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm13 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm14 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm15 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm16 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm17 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm18 = 1 + int(runiform(0,3)) if inportfolio == 1
gen esg_rm19 = 1 + int(runiform(0,3)) if inportfolio == 1

label variable esg_rm1 "ESG risk management"
label variable esg_rm2 "Environmental risk management"
label variable esg_rm3 "Social risk management"
label variable esg_rm4 "Governance risk management"
label variable esg_rm5 "Country risk and governance management"
label variable esg_rm6 "Business ethics management"
label variable esg_rm7 "Legal and regulatory E&S compliance management"
label variable esg_rm8 "Certifications and standards management"
label variable esg_rm9 "Environmental and social assessment and management"
label variable esg_rm10 "Pollution control, energy and water use management"
label variable esg_rm11 "Biodiversity conservation management"
label variable esg_rm12 "Human resources policies & procedures management"
label variable esg_rm13 "Health & safety at work management"
label variable esg_rm14 "Community health, safety and security management"
label variable esg_rm15 "Land tenure and land use change management"
label variable esg_rm16 "Indigenous peoples' rights and interests management"
label variable esg_rm17 "Stakeholder engagement and grievance management"
label variable esg_rm18 "Gender management"
label variable esg_rm19 "Cultural heritage management"

*Archive dataset;

save data\pseudo_dataset.dta, replace

log close

************************;
