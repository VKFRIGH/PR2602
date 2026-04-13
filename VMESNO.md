# Kakovost življenja: primerjava, dejavniki in prihodnji trendi

## Uvod
Za projekt smo se odločili raziskati kakovost življenja po svetu. Da bi delo lažje strukturirali, smo si zastavili šest raziskovalnih vprašanj, na katera smo tekom raziskave odgovarjali. Trenutno smo uspešno odgovorili na pet vprašanj, šesto pa je še v obdelavi, saj je nekoliko zahtevnejše v primerjavi z ostalimi.

## Podatki in njihova priprava
Podatke za projekt smo pridobili iz štirih virov: World Happiness Report, UNDP Human Development Index, World Bank DataBank (World Development Indicators) in Numbeo Quality of Life Index. Te vire smo izbrali, ker so poleg ustreznosti za našo temo tudi dovolj obsežni in relevantni. Podatke smo za prvo in drugo vprašanje ter za naslednja tri vprašanja združili v enotne tabele. Pri prvih dveh vprašanjih smo baze združili tako, da ima vsaka država eno vrstico, stolpci pa predstavljajo posamezne atribute za to državo za leto 2023. Pri preostalih vprašanjih pa je tabela strukturirana tako, da ima vsaka država in vsako leto svojo vrstico, stolpci pa predstavljajo posamezne značilnosti države. Za lažje združevanje tabel smo uporabili orodje Country Converter, ki nam je poenostavilo standardizacijo držav po ISO kodah, saj so nekatere baze že uporabljale ISO oznake, druge pa ne. Zato smo morali zagotoviti enoten format vseh tabel pred združevanjem. Po združitvi podatkov smo dodatno odstranili oziroma popravili redundantne, podvojene in manjkajoče vrednosti, saj bi lahko vplivale na kasnejšo analizo. Posebno pozornost smo namenili atributom z enakim pomenom ter spremenljivkam, ki niso prispevale k raziskavi, kot so nepotrebne interpretacije 

### Zaključna tabela 1
*(dodajte vsebino)*

### Zaključna tabela 2
*(dodajte vsebino)*

## Ovrednotenje podatkov
Ko smo podatke pretvorili v uporabno obliko, jih je bilo treba še ovrednotiti. Pri prvih dveh vprašanjih smo uporabili metodo Borda count, saj ta pristop bistveno poenostavi analizo, ker normalizacija tabele ni potrebna. Pri tem pa smo morali biti pozorni, da smo izključili atribute, kot sta ISO koda in ime države, saj bi lahko vplivali na napačno interpretacijo rezultatov. Prav tako smo morali nekatere spremenljivke obrniti, ker nižja vrednost v določenih primerih pomeni boljše stanje (npr. zaznanvanje korupcije).

<img width="600" height="360" alt="image" src="https://github.com/user-attachments/assets/23b528da-2992-423c-9dee-963a91a072fa" />


Pri odgovarjanju na preostala tri vprašanja smo uporabili več metod ovrednotenja. Prva med njimi je razlika med zadnjim in prvim letom zbiranja podatkov, ki predstavlja dober pokazatelj, katere države so danes v boljšem položaju kot na začetku opazovanega obdobja. Vendar ta metoda ne omogoča vpogleda v trende rasti ali padanja skozi čas, niti ne pokaže trenutnega stanja v kontekstu celotnega razvoja države.Za bolj celovito analizo smo zato uporabili fasetne grafe, ki omogočajo neposredno primerjavo razvojnih poti posameznih evropskih držav skozi čas. Na ta način je mogoče lažje prepoznati dolgoročne trende rasti ali upadanja ter oceniti trenutno stanje v primerjavi s preteklostjo.

<img width="700" height="900" alt="image" src="https://github.com/user-attachments/assets/6b9aef99-e24f-4674-928d-00e2520c3964" />

Poleg tega smo uporabili tudi korelacijsko matriko, ki nam omogoča ugotavljanje povezav in vplivov posameznih spremenljivk na kakovost življenja.



## Ugotovitve

Vprašanje, katera država ima trenutno najvišjo kakovost življenja, je težko odgovoriti povsem natančno, saj prihodnjih trendov še nismo analizirali. Na podlagi rezultatov za leto 2023 pa lahko sklepamo, da je na prvem mestu Norveška, saj je v tem letu dosegla najvišjo skupno vrednost kazalnika kakovosti življenja.
Razlog za njen vodilni položaj je najlažje pojasniti z interpretacijo spodnjega grafa. Iz njega je razvidno, da ima Norveška sicer nekoliko nižji Ladder score v primerjavi s povprečjem najboljših 10 držav, vendar izrazito izstopa pri drugih kazalnikih. Dosega zelo visoko stopnjo svobode (z-score približno 2,2, kar jo uvršča med približno 1 % najboljših držav), prav tako pa izkazuje višjo raven radodarnosti in boljšo (nižjo) zaznano korupcijo. Kombinacija teh dejavnikov, skupaj z nekoliko nadpovprečnim BDP glede na top 10 povprečje, na koncu vodi do tega, da Norveška zasede prvo mesto.
Na vprašanje o rasti in padanju kakovosti življenja lahko odgovorimo na podlagi spodnjega grafa, ki prikazuje neto spremembo kakovosti življenja evropskih držav. Iz njega je razvidno, da sta največjo rast dosegli Ukrajina in Rusija, medtem ko so najmanjšo rast zabeležile Švica, Nemčija, Finska in Danska, ki jih sicer običajno dojemamo kot bolj razvite države. Vendar pa je ta graf lahko zavajajoč, saj sama rast ne odraža nujno dejanske kakovosti življenja. Povečanje iz 90 na 100 je bistveno težje doseči kot rast iz 0 na 50, zato je za bolj realno sliko smiselno upoštevati tudi fasetne grafe (slika v poglavju ovrednotenje podatkov), ki omogočajo celovitejšo primerjavo.

