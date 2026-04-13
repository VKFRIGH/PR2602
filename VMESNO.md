# Kakovost življenja: primerjava, dejavniki in prihodnji trendi
VID KOVAČIČ,  JAKOB IHAN, BOR KAJIN, KRISTJAN HANDANOVIĆ
     
## Uvod
Za projekt smo se odločili raziskati kakovost življenja po svetu, pri čemer smo si za lažjo strukturiranost dela zastavili več raziskovalnih vprašanj, kot so katera država ima najbolj kakovostno življenje, zakaj ima najboljšo kakovost, katere države beležijo rast kakovosti in zakaj, kateri faktorji vplivajo na kakovost življenja ter pri katerih državah kakovost pada in zakaj. Poleg tega nas zanima tudi, kaj bi lahko napovedovali za prihodnja leta. Na večino teh vprašanj smo tekom raziskave že uspešno odgovorili, medtem ko zadnje vprašanje še vedno obdelujemo, saj je nekoliko zahtevnejše v primerjavi z ostalimi.

## Podatki in njihova priprava
Podatke za projekt smo pridobili iz štirih virov: World Happiness Report, UNDP Human Development Index, World Bank DataBank (World Development Indicators) in Numbeo Quality of Life Index. Te vire smo izbrali, ker so poleg ustreznosti za našo temo tudi dovolj obsežni in relevantni. Podatke smo za prvo in drugo vprašanje ter za naslednja tri vprašanja združili v enotne tabele. Pri prvih dveh vprašanjih smo baze združili tako, da ima vsaka država eno vrstico, stolpci pa predstavljajo posamezne atribute za to državo za leto 2023. Pri preostalih vprašanjih pa je tabela strukturirana tako, da ima vsaka država in vsako leto svojo vrstico, stolpci pa predstavljajo posamezne značilnosti države. Za lažje združevanje tabel smo uporabili orodje Country Converter, ki nam je poenostavilo standardizacijo držav po ISO kodah, saj so nekatere baze že uporabljale ISO oznake, druge pa ne. Zato smo morali zagotoviti enoten format vseh tabel pred združevanjem. Po združitvi podatkov smo dodatno odstranili oziroma popravili redundantne, podvojene in manjkajoče vrednosti, saj bi lahko vplivale na kasnejšo analizo. Posebno pozornost smo namenili atributom z enakim pomenom ter spremenljivkam, ki niso prispevale k raziskavi, kot so nepotrebne interpretacije 

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
Ko smo podatke pretvorili v uporabno obliko, jih je bilo treba še ovrednotiti. Pri prvih dveh vprašanjih smo uporabili metodo Borda count, saj ta pristop bistveno poenostavi analizo, ker normalizacija tabele ni potrebna. Pri tem pa smo morali biti pozorni, da smo izključili atribute, kot sta ISO koda in ime države, saj bi lahko vplivali na napačno interpretacijo rezultatov. Prav tako smo morali nekatere spremenljivke obrniti, ker nižja vrednost v določenih primerih pomeni boljše stanje (npr. zaznanvanje korupcije).

<img width="600" height="360" alt="image" src="https://github.com/user-attachments/assets/23b528da-2992-423c-9dee-963a91a072fa" />
<img src="https://github.com/user-attachments/assets/23b528da-2992-423c-9dee-963a91a072fa" style="max-width: 100%;" />


Pri odgovarjanju na preostala tri vprašanja smo uporabili več metod ovrednotenja. Prva med njimi je razlika med zadnjim in prvim letom zbiranja podatkov, ki predstavlja dober pokazatelj, katere države so danes v boljšem položaju kot na začetku opazovanega obdobja. Vendar ta metoda ne omogoča vpogleda v trende rasti ali padanja skozi čas, niti ne pokaže trenutnega stanja v kontekstu celotnega razvoja države.Za bolj celovito analizo smo zato uporabili fasetne grafe, ki omogočajo neposredno primerjavo razvojnih poti posameznih evropskih držav skozi čas. Na ta način je mogoče lažje prepoznati dolgoročne trende rasti ali upadanja ter oceniti trenutno stanje v primerjavi s preteklostjo.

<img width="600" height="700" alt="image" src="https://github.com/user-attachments/assets/6b9aef99-e24f-4674-928d-00e2520c3964" />

Poleg tega smo uporabili tudi korelacijsko matriko, ki nam omogoča ugotavljanje povezav in vplivov posameznih spremenljivk na kakovost življenja.



## Ugotovitve

Vprašanje, katera država ima trenutno najvišjo kakovost življenja, je težko odgovoriti povsem natančno, saj prihodnjih trendov še nismo analizirali. Na podlagi rezultatov za leto 2023 pa lahko sklepamo, da je na prvem mestu Norveška, saj je v tem letu dosegla najvišjo skupno vrednost kazalnika kakovosti življenja.
Razlog za njen vodilni položaj je najlažje pojasniti z interpretacijo spodnjega grafa. Iz njega je razvidno, da ima Norveška sicer nekoliko nižji Ladder score v primerjavi s povprečjem najboljših 10 držav, vendar izrazito izstopa pri drugih kazalnikih. Dosega zelo visoko stopnjo svobode (z-score približno 2,2, kar jo uvršča med približno 1 % najboljših držav), prav tako pa izkazuje višjo raven radodarnosti in boljšo (nižjo) zaznano korupcijo. Kombinacija teh dejavnikov, skupaj z nekoliko nadpovprečnim BDP glede na top 10 povprečje, na koncu vodi do tega, da Norveška zasede prvo mesto.

<img width="800" height="558" alt="image" src="https://github.com/user-attachments/assets/ab3298fb-f17d-4232-bd69-dd93e4cc29da" />

Na vprašanje o rasti in padanju kakovosti življenja lahko odgovorimo na podlagi spodnjega grafa, ki prikazuje neto spremembo kakovosti življenja evropskih držav(2014-2025). Iz njega je razvidno, da sta največjo rast dosegli Ukrajina in Rusija, medtem ko so najmanjšo rast zabeležile Švica, Nemčija, Finska in Danska, ki jih sicer običajno dojemamo kot bolj razvite države. Vendar pa je ta graf lahko zavajajoč, saj sama rast ne odraža nujno dejanske kakovosti življenja. Povečanje iz 90 na 100 je bistveno težje doseči kot rast iz 0 na 50, zato je za bolj realno sliko smiselno upoštevati tudi fasetne grafe (slika v poglavju ovrednotenje podatkov), ki omogočajo celovitejšo primerjavo.


<img width="700" height="700" alt="image" src="https://github.com/user-attachments/assets/9c8bd7d9-d93f-4cd0-9675-e4f88be4d1cb" />


Na zadnje vprašanje lahko najlažje odgovorimo s pomočjo korelacijske matrike, iz katere je razvidno, kateri dejavniki so najmočneje povezani s kakovostjo življenja. Opazimo, da ima kakovost življenja najvišjo pozitivno korelacijo z oceno zadovoljstva z življenjem ter kupno močjo, kar nakazuje, da sta za posameznike ključnega pomena predvsem finančna varnost in splošno zadovoljstvo z življenjem v državi bivanja.

Prav tako je razvidno, da ima indeks onesnaževanja izrazit negativen vpliv, kar pomeni, da ljudje visoko vrednotijo čisto in zdravo okolje. Poleg teh glavnih korelacij pomembno vlogo igra tudi kakovost zdravstvenega sistema, saj ta neposredno vpliva na daljšo pričakovano življenjsko dobo in višjo kakovost vsakdanjega življenja.

<img width="700" height="650" alt="image" src="https://github.com/user-attachments/assets/12f92fba-c693-4d37-b497-fabb8701c319" />

## Zaključek in povezave do kode ter podrobnejšega opisa postopkov

Ker poročilo zaradi omejitve (900 besed) ne sme biti preobsežno, vanj nismo vključili izvorne kode in podrobnejših razlag postopkov. Te so dostopne v preostalih dveh vejah repozitorija: podrobnosti za prvi dve raziskovalni vprašanji se nahajajo v veji J_PR_Projekt, medtem ko so analize za preostala tri vprašanja zbrane v veji B+K_PR_Projekt.

V prihodnje nameravamo raziskavo še nadgraditi, in sicer z odgovorom na vprašanje o prihodnjih trendih kakovosti življenja ter z implementacijo interaktivnega vpogleda v podatke in ključne ugotovitve.
