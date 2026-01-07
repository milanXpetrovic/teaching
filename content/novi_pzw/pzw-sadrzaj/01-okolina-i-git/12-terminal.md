---
parent: Razvojna Okolina i Git
nav_order: 2
title: 1.2 Rad s Terminalom/Command Lineom
---

# 1.2 Rad s Terminalom/Command Lineom
Nakon što smo instalirali Python, vrijeme je da se upoznamo s alatom koji će postati vaš najbolji prijatelj (ili barem vrlo čest suradnik) na putu razvoja softvera – **terminalom**.

## Što je terminal?

Terminal, poznat i kao komandna linija (eng. *Command Line Interface* - CLI), je tekstualno sučelje za interakciju s vašim računalom. Umjesto da klikate po ikonama i prozorima, terminalu dajete direktne tekstualne naredbe.

Možda zvuči zastarjelo, ali za developere je to jedan od najmoćnijih i najbržih alata. Pomoću terminala ćemo:

* Pokretati Django razvojni server.
* Koristiti Git za kontrolu verzija.
* Upravljati virtualnim okruženjima.
* Izvršavati skripte i Django komande (`manage.py`).
* Brzo se kretati po direktorijima i manipulirati datotekama.

> **Različiti nazivi, ista svrha:**
>
> * Na **macOS** i **Linux** sustavima, aplikacija se obično zove **Terminal**.
> * Na **Windowsima**, imate **Command Prompt (CMD)** i **PowerShell**. Preporučujemo korištenje **PowerShell-a** jer je moderniji i moćniji.
>
> Iako se nazivi razlikuju, osnovne komande i principi rada su vrlo slični.

## Otvaranje terminala

* **Windows:** Pritisnite tipku `Win`, upišite `PowerShell` i pritisnite Enter.
* **macOS:** Pritisnite `Cmd + Space` da otvorite Spotlight, upišite `Terminal` i pritisnite Enter.
* **Linux (Ubuntu/Debian):** Pritisnite `Ctrl + Alt + T` ili pronađite aplikaciju **Terminal** u izborniku.

## Osnovni koncepti

Kada otvorite terminal, vidjet ćete nešto poput ovoga:

```bash
    korisnik@racunalo:~$
```

Ovo se zove prompt. On vam govori:

1. Tko ste (korisnik).
2. Na kojem ste računalu (racunalo).
3. U kojem ste trenutno direktoriju (~, što je oznaka za vaš home direktorij).
4. Znak $ označava da je terminal spreman prihvatiti vašu naredbu.

Vaš zadatak je upisati naredbu i pritisnuti `Enter`.

**Osnovne naredbe koje morate znati**
Ne morate znati stotine naredbi. Za početak, dovoljno je savladati ovih nekoliko ključnih.
**1. Navigacija po direktorijima**
Ovo su komande za kretanje kroz datotečni sustav.
    `pwd` (Print Working Directory) - **Gdje sam?** - Ispisuje punu putanju do direktorija u kojem se trenutno nalazite.
    code Bash

```bash
pwd
# Izlaz: /home/korisnik/projekti
```

* `ls` (List) - **Što je ovdje?**
  * Prikazuje sadržaj trenutnog direktorija (datoteke i poddirektorije).
  * `Windows ekvivalent: dir

```bash
ls
# Izlaz: projekt1  projekt2  README.md
```
  
**Korisni dodaci:**

* ls -l: Prikazuje detaljan popis s dozvolama, vlasnikom, veličinom i datumom.
* ls -a: Prikazuje i skrivene datoteke (one koje počinju s točkom, npr. .git).

* `cd` (Change Directory) - **Promijeni direktorij**
  * Najvažnija naredba za navigaciju. Mijenja trenutni direktorij.

```bash
    # Ulazak u poddirektorij 'projekt1'
    cd projekt1

    # Povratak u roditeljski direktorij (jedan nivo "gore")
    cd ..

    # Povratak u 'home' direktorij s bilo koje lokacije
    cd ~
    # ili samo
    cd
```

## 2. Rad s datotekama i direktorijima

Ovo su komande za stvaranje, brisanje i premještanje.

* `mkdir` (Make Directory) - Stvori novi direktorij
  * Koristit ćemo je za kreiranje direktorija za naše Django projekte.

    ``` bash
    mkdir moj-novi-django-projekt
    ```

`touch` - Stvori praznu datoteku

* Korisno za brzo stvaranje datoteka poput `.gitignore` ili `requirements.txt`.
* Windows (CMD) ekvivalent: echo. > ime_datoteke.txt

```bash
touch README.md
```
  
`mv` (Move) - Premjesti ili preimenuj

```bash

# Preimenovanje datoteke
mv stara_datoteka.txt nova_datoteka.txt

# Premještanje datoteke u drugi direktorij
mv nova_datoteka.txt ./dokumenti/
```
  
`cp` (Copy) - Kopiraj

```bash
# Kopiranje datoteke
cp original.txt kopija.txt
```
  
`rm` (Remove) - Obriši datoteku

```bash
rm kopija.txt
```

`rm -r` - Obriši direktorij (i sav njegov sadržaj)

* ⚠️ UPOZORENJE: Budite VRLO OPREZNI s rm naredbom, pogotovo s -r (recursive) dodatkom. Ona briše datoteke i direktorije trajno, bez slanja u smeće. Naredba rm -rf / može obrisati cijeli vaš sustav. Uvijek dvaput provjerite što brišete!

```bash
    # Brisanje direktorija 'stari-projekt' i svega unutar njega
    rm -r stari-projekt
```

**Korisni savjeti za brži rad:**

* Dovršavanje pomoću tipke Tab (Tab Completion): Ovo je vaša supermoć! Kada počnete tipkati ime datoteke ili direktorija, pritisnite Tab i terminal će pokušati automatski dovršiti ime. Ako postoji više opcija, pritisnite Tab dvaput da ih vidite. Ovo štedi vrijeme i smanjuje greške pri tipkanju.
* Povijest naredbi: Koristite tipke sa strelicama Gore (↑) i Dolje (↓) za kretanje kroz naredbe koje ste prethodno unijeli.

**Čišćenje ekrana:**

* Na macOS/Linux: `clear`
* Na Windows: `cls`

Ne morate odmah zapamtiti sve. Najvažnije je da se naviknete na kretanje (`cd`, `ls`, `pwd`) i stvaranje direktorija (`mkdir`). Ostalo će doći s vježbom.

Sada kada se osjećate ugodnije u terminalu, spremni smo napraviti sljedeći korak: naučiti kako izolirati okruženja naših projekata.
