# Kakovost življenja: primerjava, dejavniki in prihodnji trendi

## Uvod
Za projekt smo se odločili raziskati kakovost življenja po svetu. Da bi delo lažje strukturirali, smo si zastavili šest raziskovalnih vprašanj, na katera smo tekom raziskave odgovarjali. Trenutno smo uspešno odgovorili na pet vprašanj, šesto pa je še v obdelavi, saj je nekoliko zahtevnejše v primerjavi z ostalimi.

## Podatki in njihova priprava
Podatke za projekt smo pridobili iz štirih virov:
- World Happiness Report  
- UNDP Human Development Index  
- World Bank DataBank (World Development Indicators)  
- Numbeo Quality of Life Index  

Te vire smo izbrali, ker so poleg ustreznosti za našo temo tudi dovolj obsežni in relevantni.

Podatke smo za prvo in drugo vprašanje ter za naslednja tri vprašanja združili v enotne tabele. Pri prvih dveh vprašanjih smo baze združili tako, da ima vsaka država eno vrstico, stolpci pa predstavljajo posamezne atribute za to državo za leto 2023.

Pri preostalih vprašanjih pa je tabela strukturirana tako, da ima vsaka država in vsako leto svojo vrstico, stolpci pa predstavljajo posamezne značilnosti države.

Za lažje združevanje tabel smo uporabili orodje **Country Converter**, ki nam je poenostavilo standardizacijo držav po ISO kodah, saj so nekatere baze že uporabljale ISO oznake, druge pa ne. Zato smo morali zagotoviti enoten format vseh tabel pred združevanjem.

Po združitvi podatkov smo dodatno odstranili oziroma popravili:
- redundantne podatke  
- podvojene vrednosti  
- manjkajoče vrednosti  

Posebno pozornost smo namenili atributom z enakim pomenom ter spremenljivkam, ki niso prispevale k raziskavi.

### Zaključna tabela 1
*(dodajte vsebino)*

### Zaključna tabela 2
*(dodajte vsebino)*

## Ovrednotenje podatkov
Ko smo podatke pretvorili v uporabno obliko, jih je bilo treba še ovrednotiti.

Pri prvih dveh vprašanjih smo uporabili metodo **Borda count**, saj ta pristop bistveno poenostavi analizo, ker normalizacija tabele ni potrebna. Pri tem pa smo morali biti pozorni, da smo izključili atribute, kot sta ISO koda in ime države, saj bi lahko vplivali na napačno interpretacijo rezultatov.

Prav tako smo morali nekatere spremenljivke obrniti, ker nižja vrednost v določenih primerih pomeni boljše stanje (npr. zaznavanje korupcije).

Pri odgovarjanju na preostala tri vprašanja smo uporabili več metod:
- razlika med zadnjim in prvim letom zbiranja podatkov  
- fasetni grafi  
- korelacijska matrika  

Razlika med zadnjim in prvim letom predstavlja dober pokazatelj napredka, vendar ne omogoča vpogleda v trende skozi čas.

Za bolj celovito analizo smo uporabili **fasetne grafe**, ki omogočajo primerjavo razvojnih poti držav skozi čas.

Poleg tega smo uporabili tudi **korelacijsko matriko**, ki omogoča ugotavljanje povezav med spremenljivkami.

## Ugotovitve

Vprašanje, katera država ima trenutno najvišjo kakovost življenja, je težko odgovoriti povsem natančno, saj prihodnjih trendov še nismo analizirali.

Na podlagi rezultatov za leto 2023 lahko sklepamo, da je na prvem mestu **Norveška**, saj je dosegla najvišjo skupno vrednost kazalnika kakovosti življenja.

Razlog za njen vodilni položaj:
- nekoliko nižji *Ladder score* v primerjavi s top 10  
- zelo visoka stopnja svobode (z-score ~ 2,2)  
- višja raven radodarnosti  
- nižja zaznana korupcija  
- nadpovprečen BDP  

Kombinacija teh dejavnikov jo postavlja na prvo mesto.

Pri analizi rasti kakovosti življenja (na podlagi grafa neto spremembe):
- največjo rast: **Ukrajina**, **Rusija**  
- najmanjšo rast: **Švica**, **Nemčija**, **Finska**, **Danska**

Pomembno pa je poudariti, da:
- rast ne pomeni nujno visoke kakovosti življenja  
- rast iz 90 → 100 je težja kot iz 0 → 50  

Zato je za realnejšo sliko treba upoštevati tudi fasetne grafe, ki omogočajo celovitejšo primerjavo skozi čas.
