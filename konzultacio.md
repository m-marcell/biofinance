# Konzultáció segéd 2026.04.09.

## Q&A

- _Milyen indexet használjuk? Van valami átfogó EU-s index, vagy magunknak rakjuk össze a tagokat? Esetleg maradjunk az MSCI All Country World Indexnél?_: Maradjunk
- _ESG provider MSCI vs Refinitiv; válasszunk egyet, vagy gyűjtsük ki mindkettőt és súlyozzuk őket?_:
- _Honnan legyenek árfolyamadataink? API-nak elvileg van limitje, szóval nem bizots, hogy ennyzi eszközre le tudjuk tölteni a napi zárókat! Más forrásokból szedjünk árfolyamadatokat?_:
- _Mi legyen a time-range? 10 év? Így lesz benne bőven normál időszak és krízisidőszak is._: Minél hosszabb időtáv, majd később alakítunk rajta.
- _Mi legyen az ENCORE-ral? Hogy építsük bele a kutatásba?_:

## Felhasznált fő irodalom

#### Biodiversity risk premium (Helena, Gergő)
Faktormodell helyett markovitz-féle portfólióelmélet szerint összeállítótt (short pozíciók kizárva, mivel az nem felel meg a SRI befektetőnek!) biodiversity risk premium (Sharpe rátákkal), majd ezutám Fama-French faktorok vizsgálata is! Az SRI befektetők 3 különböző szinten állítják be a biodiverzitásra vonatkozó kockázatkerüléseket (biodiversity screening).

MSCI All Country World Index adataira 2013-2023-ig (normál és krízisidőszakok is vannak!).

#### Responsible investing: The ESG-efficient frontier

A cél az, hogy a sztenderd mean-variance hasznosságfüggvényű (ESG-unaware) befektetőt kiegészítsük egy ESG értéken alapúló feltétellel (ESG-aware investors). Egy harmadik típúsú befektetőt is figyelembe vesz (ESG-motivated), ők a figyelembe vétel mellett preferálják a magasabb ESG értékkel rendelkező papírokat, tehát ők egy optimális trade-off-ot keresnek a magas hozam, alacsony variancia és magas ESG érték között.

Ez az optimapilálás nehéznek tűnik, de a probléma átalakítható a Share-ráták és ESG score-ok közötti optimalizálásra (A risk-return optimalizálást a Sharpe-ráta össze tudja vonni!).

Ami még érdekes, hogy nem minden esetben az összesített ESG értékeket használják, hanem külön-külön veszik az E-S-G pillért is (természetesen az összértékkel is megcsinálják végül).

#### Modeling demand for ESG

Az előző kutatást viszi tovább, több empirikus eredménnyel.

A sztenderd hassznosságon alapuló befektetési modellbe az ESG értéket nem mint külsö faktorként, hanem közvetlenül veszi bele, így jobban meg tudja határozni, hogy az ESG szempontból veszélyes befektetések miként befolyásolják közvetlenül a hasznosságot.

Eredményül azt kapták, hogy az ESG közvetlen beépítése által magasabb hasznosságot érnek el a befektetők, azokhoz képest, akik ezt nem teszik (sima mean-variance alapú). Empirikus kutatással (USA piac) megerősítették ezt. Ez a kutatás is hangsúlyozza, hogy ennek a modellnek a használhatósága nagyban függ az elérhető adatok (ESG providerek) minőségétől.

#### Aggregate Confusion: The Divergence of ESG Ratings

_Végére valami takeway_

6 különböző ESG értékelő ratingjeit hasonlítja össze, hogy mennyiben és hogyan térnek el ezek egymástól. 3 fő elem szerint vizsgálja az értékeket, scope, weight és measurement. A scope és weight az mutatja, hogy mit szeretne mérni az ESG score (milyen változók alapján), és a measurement pedig azt, hogy ezt hogyan méri.

Egy fő felfedezése a cikkenek, hogy lehetséges ezeket az ESG értékeket újrabecsülni, és ezáltal megmondani, hogy az értékelés során mely változók kaptak fontosabb vagy kevésbé fontosabb szerepet a vésgő score-ban.

A takeaway az, hogy más ESG provider adatai alapján teljesen más következtetésekre lehet jutni, ezért fontos az, hogy hogyan választunk adatforrást!
- Egy megoldás lehet erre a problémára az, hogy több provider adatait "súlyozzuk", így egy közös ESG konszenzusra jutunk
- Egy másik lehetőség, hogy alacsonyabb szintű mutatókra építjük az elemzéseket (GHG Emissions, Labor Practices, stb...), így már nem kell a providerek különbségeivel számolni.

#### Climate Impact Investing

_Naggggyon matekintenzív papír!!_

A vállalatok kibocsátását befolyásolják a piaci zöld befektetők, megfigyelések szerint, amennyiben a zöld befektetők száma vagy érzékenysége megnő, akkor a vállalatok kibocsátása csökkentő trendet mutat (ugyanez igaz fordítva is!). Továbbá az is fontos, hogy amennyiben már csak ötletként felmerülnek az új/szigorúbb klímarendeletek, a vállalatok sokasága már akkor elkezi az átállást, és kevesebb GHG-t bocsát ki.
