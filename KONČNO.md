# Kakovost življenja: primerjava, dejavniki in prihodnji trendi
VID KOVAČIČ,  JAKOB IHAN, BOR KAJIN, KRISTJAN HANDANOVIĆ<br>

## Uvod

Pri našem projektu smo se odločili raziskati kakovost življenja po svetu. V strukturno oporo poteku dela, smo si zastavili več raziskovalnih vprašanj: 

1. Katera država ima najbolj kakovostno življenje?
2. Zakaj ima najboljšo kakovost življenja?
3. Katere države beležijo rast kakovosti in zakaj? 
4. Kateri faktorji vplivajo na kakovost življenja? 
5. Pri katerih državah kakovost pada in zakaj?
6. Kaj bi lahko napovedovali za prihodnja leta?

Poleg vprašanj pa smo ustvarili tudi streamlit, ki omogoča interaktiven vpogled v najpomembnejše podatke;

## Podatki in njihova priprava

Podatke smo pridobili iz štirih virov:  


- [World Happiness Report](https://www.worldhappiness.report/data-sharing/ )
- [UNDP Human Development Index](https://hdr.undp.org/data-center/human-development-index#/indicies/HDI)
- [World Bank DataBank (World Development Indicators)](https://datacatalog.worldbank.org/search/dataset/0037712/world-development-indicators)
- [Numbeo Quality of Life Index](https://www.numbeo.com/quality-of-life/rankings_by_country.jsp)

Te smo izbrali, ker so poleg ustreznosti za našo temo tudi dovolj obsežni in relevantni. Pri prvih dveh vprašanjih, enako kot pri preostalih treh, smo podatke združili v dve ločeni tabeli. V prvi tabeli ima vsaka država eno vrstico, stolpci pa predstavljajo posamezne atribute za leto 2023. Pri preostalih vprašanjih pa je tabela strukturirana tako, da ima vsaka država za vsako leto svojo vrstico, stolpci pa predstavljajo posamezne značilnosti države. 

Za lažje združevanje smo uporabili orodje Country Converter, ki nam je omogočilo standardizacijo držav po ISO kodah, saj so nekatere baze te oznake že vsebovale, druge pa ne. Zato smo morali pred združevanjem zagotoviti enoten format vseh tabel. 

Po združitvi smo podatke dodatno očistili — odstranili oziroma popravili smo redundantne, podvojene in manjkajoče vrednosti, saj bi te lahko vplivale na nadaljnjo analizo. Posebno pozornost smo namenili atributom z enakim pomenom ter spremenljivkam, ki niso prispevale k raziskavi.

### Zaključna tabela 1
| iso_code | Country name | Ladder score | Logged GDP per capita | Social support | Healthy life expectancy | Freedom to make life choices | Generosity | Perceptions of corruption | HDI rank | Human Development Index (HDI) | Expected years of schooling | Mean years of schooling | Individuals using the Internet (% of population) | School enrollment, primary (% net) |
|----------|--------------|--------------|------------------------|----------------|--------------------------|------------------------------|------------|-----------------------------|----------|-------------------------------|------------------------------|---------------------------|-----------------------------------------------|------------------------------------|
| FIN      | Finland      | 7.8042       | 10.792010             | 0.968770       | 71.149994               | 0.961408                     | -0.018824  | 0.181745                    | 12       | 0.948                         | 19.494089                   | 12.979625                | 93.5139                                      | 98.62944                           |
| DNK      | Denmark      | 7.5864       | 10.962164             | 0.954112       | 71.250145               | 0.933533                     | 0.134242   | 0.195814                    | 4        | 0.962                         | 18.70401                    | 13.027321                | 98.7756                                      | 98.53748                           |
| ISL      | Iceland      | 7.5296       | 10.895531             | 0.982533       | 72.050018               | 0.936349                     | 0.210987   | 0.667848                    | 1        | 0.972                         | 18.85059                    | 13.908926                | 99.8301                                      | 99.83367                           |
| ISR      | Israel       | 7.4729       | 10.638705             | 0.943344       | 72.697205               | 0.808866                     | -0.023080  | 0.708094                    | 27       | 0.919                         | 14.93416                    | 13.534595                | 87.0384                                      | 97.01884                           |
| NLD      | Netherlands  | 7.4030       | 10.942279             | 0.930499       | 71.550018               | 0.886875                     | 0.212686   | 0.378929                    | 8        | 0.955                         | 18.58485                    | 12.669947                | 97.0068                                      | 98.64765                           |

### Zaključna tabela 2

| Country Name | Country Code | Year | School enrollment, primary (% net) | Individuals using the Internet (% of population) | Life evaluation (3-year average) | Log GDP per capita | Social support | Healthy life expectancy | Freedom to make life choices | QoL Rank | Quality of Life Index | Purchasing Power Index | Safety Index | Health Care Index | Cost of Living Index | Property Price to Income Ratio | Traffic Commute Time Index | Pollution Index | Climate Index |
|--------------|--------------|------|------------------------------------|--------------------------------------------------|----------------------------------|--------------------|----------------|--------------------------|--------------------------------|----------|------------------------|------------------------|--------------|--------------------|------------------------|-------------------------------|-----------------------------|------------------|----------------|
| Austria      | AUT          | 2019 | 88.61718                           | 87.7522                                          | 7.2942                           | 1.317286           | 1.437445       | 1.000934                 | 0.603369                       | 4.5      | 189.45                 | 93.30                  | 77.70        | 79.35              | 71.95                  | 10.35                        | 25.30                      | 21.90           | 79.05          |
| Austria      | AUT          | 2020 | 88.61718                           | 87.5294                                          | 7.2680                           | 1.492000           | 1.062000       | 0.782000                 | 0.640000                       | 5.0      | 182.10                 | 80.90                  | 75.95        | 78.65              | 71.10                  | 10.85                        | 26.05                      | 21.90           | 77.75          |
| Austria      | AUT          | 2021 | 88.61718                           | 92.5292                                          | 7.1630                           | 1.931000           | 1.165000       | 0.774000                 | 0.623000                       | 5.5      | 179.40                 | 73.45                  | 74.65        | 77.70              | 75.20                  | 10.65                        | 25.70                      | 19.80           | 77.45          |
| Austria      | AUT          | 2022 | 88.61718                           | 93.6141                                          | 7.0970                           | 1.927000           | 1.382000       | 0.535000                 | 0.630000                       | 7.5      | 178.65                 | 76.20                  | 73.55        | 76.45              | 67.55                  | 10.80                        | 25.45                      | 21.95           | 77.10          |
| Austria      | AUT          | 2023 | 88.61718                           | 95.3347                                          | 6.9050                           | 1.885000           | 1.336000       | 0.696000                 | 0.703000                       | 7.0      | 184.55                 | 88.40                  | 72.55        | 76.85              | 67.35                  | 10.45                        | 24.30                      | 21.30           | 77.00          |

## Ovrednotenje podatkov
Ko smo podatke pretvorili v uporabno obliko, jih je bilo treba tudi ovrednotiti. Pri prvih dveh vprašanjih smo uporabili metodo Borda count, saj ta pristop bistveno poenostavi analizo, ker normalizacija podatkov ni potrebna. Pri tem smo morali izločiti atribute, kot sta ISO koda in ime države, saj bi lahko vplivali na napačno interpretacijo rezultatov. Prav tako smo nekatere spremenljivke obrnili, ker v določenih primerih nižja vrednost pomeni boljše stanje (npr. zaznavanje korupcije).
<br><br>
<img src="https://github.com/user-attachments/assets/23b528da-2992-423c-9dee-963a91a072fa" width="90%"  />
<br><br>
Pri preostalih treh vprašanjih smo uporabili več metod ovrednotenja. Ena izmed njih je razlika med zadnjim in prvim letom zbiranja podatkov, ki predstavlja dober pokazatelj napredka posameznih držav. Vendar pa ta metoda ne omogoča vpogleda v trende skozi čas niti ne odraža trenutnega stanja v širšem kontekstu razvoja države.

Za bolj celovito analizo smo zato uporabili fasetne grafe, ki omogočajo neposredno primerjavo razvojnih poti evropskih držav skozi čas. Na ta način lahko lažje prepoznamo dolgoročne trende ter ocenimo trenutno stanje v primerjavi s preteklostjo.
<br><br>
<img src="https://github.com/user-attachments/assets/6b9aef99-e24f-4674-928d-00e2520c3964" width="90%" />
<br><br>

Uporabili smo tudi korelacijsko matriko, ki omogoča analizo povezav med posameznimi spremenljivkami ter njihovega vpliva na kakovost življenja.

Za napovedovanje prihodnjih vrednosti kakovosti življenja smo uporabili linearno regresijo po posameznih državah. Podatke smo omejili na obdobje po letu 2017, saj se je pred tem spremenila metodologija izračuna indeksa kakovosti življenja. Za vsako državo smo ustvarili ločen regresijski model, kjer je leto predstavljalo neodvisno spremenljivko, indeks kakovosti življenja pa odvisno spremenljivko.Uspešnost modela smo ocenjevali s koeficientom determinacije R^2
, ki meri, kako dobro model opisuje gibanje podatkov skozi čas. Višje vrednosti pomenijo bolj zanesljivo napoved.

Poleg same napovedne premice smo izračunali tudi interval negotovosti. Ta temelji na standardnem odklonu residualov oziroma napak modela. Ker negotovost napovedi s časom narašča, smo interval zaupanja za prihodnja leta postopoma širili. Na grafih:

## Ugotovitve

Na vprašanje, katera država ima najvišjo kakovost življenja, lahko na podlagi naših izračunov odgovorimo, da je to Norveška, saj dosega najvišjo skupno vrednost kazalnika, kar jo uvršča na prvo mesto.

Razloge za njen vodilni položaj najlažje pojasnimo z interpretacijo spodnjega grafa. Iz njega je razvidno, da ima Norveška sicer nekoliko nižji Ladder score v primerjavi s povprečjem desetih najbolje uvrščenih držav, vendar izrazito izstopa pri drugih kazalnikih. Dosega zelo visoko stopnjo svobode (z-vrednost približno 2,2, kar jo uvršča med približno 1 % najboljših držav), hkrati pa izkazuje tudi višjo raven radodarnosti ter nižjo zaznano stopnjo korupcije. Kombinacija teh dejavnikov, skupaj z nadpovprečnim BDP na prebivalca glede na povprečje najboljših držav, vodi do tega, da Norveška zasede prvo mesto.
<br><br>
<img src="https://github.com/user-attachments/assets/ab3298fb-f17d-4232-bd69-dd93e4cc29da" width="90%" />
<br><br>
Na vprašanje o rasti in upadanju kakovosti življenja lahko odgovorimo na podlagi spodnjega grafa, ki prikazuje neto spremembo kakovosti življenja evropskih držav v obdobju 2014–2025. Iz grafa je razvidno, da sta največjo relativno rast dosegli Ukrajina in Rusija, medtem ko so najmanjše spremembe zabeležile Švica, Nemčija, Finska in Danska.

Pri interpretaciji teh rezultatov je treba upoštevati, da relativna rast ne odraža nujno dejanske ravni kakovosti življenja. Države z že visoko začetno vrednostjo težje dosegajo velike spremembe kot države z nižjim izhodiščem. Zato je za celovitejšo razumevanje smiselno upoštevati tudi absolutne vrednosti in dodatne vizualizacije, kot so fasetni grafi (prikazani v poglavju Ovrednotenje podatkov), ki omogočajo bolj uravnoteženo primerjavo.

Poleg same napovedne premice smo izračunali tudi interval negotovosti. Ta temelji na standardnem odklonu residualov oziroma napak modela. Ker negotovost napovedi s časom narašča, smo interval zaupanja za prihodnja leta postopoma širili. Na grafih:

<br><br>
<img src="https://github.com/user-attachments/assets/9c8bd7d9-d93f-4cd0-9675-e4f88be4d1cb" width="90%" />
<br><br>

Na zadnje vprašanje lahko najlažje odgovorimo s pomočjo korelacijske matrike. Ta razkriva, kateri dejavniki so najmočneje povezani s kakovostjo življenja. Opazimo, da ima kakovost življenja najvišjo pozitivno korelacijo z zadovoljstvom z življenjem ter kupno močjo, kar nakazuje, da sta za posameznike ključnega pomena predvsem finančna varnost in splošno zadovoljstvo z življenjem.

Prav tako je razvidno, da ima indeks onesnaževanja izrazit negativen vpliv, kar pomeni, da ljudje visoko vrednotijo čisto in zdravo okolje. Pomembno vlogo ima tudi kakovost zdravstvenega sistema, saj ta neposredno vpliva na daljšo pričakovano življenjsko dobo in višjo kakovost vsakdanjega življenja.

<br><br>
<img src="https://github.com/user-attachments/assets/12f92fba-c693-4d37-b497-fabb8701c319" width="75%" />
<br><br>

Z linearno regresijo  pa lahko napovemo da bo po naših napovedih večino držav imelo rast kakovosti življenja z izjemo Grčije in Belorusije kjer kakovost življenja počasi pada. Iz grafa je vidno, da ima najmanjši interval negotovosti Albanija takoj pa ji sledijo Malta, Luksenburg, Latvija in litva  to pomeni da so v preteklosti te države imel zelo linearno rast in se to pričakuje tudi v prihodnosti. Velik interval negotovosti pa imajo države pri katerih kakovost zelo niha na grafu še posebaj iztopajo države kot so Srbija ter Bosna in Hercegovina.
<br><br>
<img width="1989" height="2395" alt="image" src="https://github.com/user-attachments/assets/8c37efc4-e0f7-473b-8ef6-f0d95e4ae7ad" width="75%"/>
<br><br>
## Aplikacija streamlit
Naredili smo tudi aplikacijo ki omogoča interaktiven vpogled v podatke. Vsebuje opcijo za zemljevid kjer lahko paogledamo borda_count celega sveta ali pa pogledamo vrednosti posameznih atributov druga opcija pa nam omogoča primerjavo posameznih držav po izbranih atributih. Aplikacija se nahaja pod Releases kjer so tudi navodila za zagon aplikacija pa je tudi objavljena na [link](https://pr2602-dyglvptx874uybcsu7rwgx.streamlit.app/).

## Zaključek in povezave do kode ter podrobnejšega opisa postopkov

Zaradi omejitve obsega (1300 besed) v poročilo nismo vključili izvorne kode in podrobnejših opisov postopkov. Ti so na voljo v preostalih dveh vejah repozitorija: podrobnosti za prvi dve raziskovalni vprašanji se nahajajo v veji [J_PR_Projekt](https://github.com/VKFRIGH/PR2602/blob/J_PR_Projekt/projektJ.ipynb), analize za preostala tri vprašanja pa v veji [B+K_PR_Projekt](https://github.com/VKFRIGH/PR2602/blob/B%2BK_PR_Projekt/projektB%2BK.ipynb).



