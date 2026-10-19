---
author: Milan Petrović
title: "1. Postavljanje razvojnog okruženja i uvod u Django"
layout: default
parent: PZW
nav_order: 1
has_children: false
has_toc: false
nav_exclude: false
---

# Postavljanje razvojnog okruženja i uvod u Django
{: .no_toc }

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Što je Django

Django je besplatan web okvir (engl. *web framework*) otvorenog koda pisan u Pythonu. Nastao je 2005. godine u redakciji novina *Lawrence Journal-World* u Kansasu, gdje su ga razvili Adrian Holovaty i Simon Willison kako bi brzo izrađivali web aplikacije za redakciju. Ime je dobio po jazz gitaristu Djangu Reinhardtu. Danas ga razvija i održava zajednica okupljena oko neprofitne organizacije Django Software Foundation.

Djangova filozofija sažeta je u nekoliko načela:

- **"Baterije uključene"** (engl. *batteries included*): u samom okviru dolaze ORM za rad s bazom podataka, administratorsko sučelje, autentifikacija korisnika, obrasci, sustav predložaka, zaštita od čestih napada i mnogo toga drugoga, pa za većinu stvari nije potrebno tražiti dodatne pakete.
- **DRY** (engl. *Don't Repeat Yourself*): svaka informacija treba postojati na jednom mjestu. Primjerice, model opisan u Pythonu služi i za stvaranje tablice u bazi i za generiranje obrazaca i administratorskog sučelja.
- **Brz razvoj**: od ideje do aplikacije koja radi treba proći što manje vremena.
- **Sigurnost prema zadanim postavkama**: zaštita od CSRF-a, XSS-a, SQL injekcije i *clickjackinga* uključena je bez dodatnog rada (detaljnije u poglavlju [13. Sigurnost Django web aplikacija](13-sigurnost.md)).

Primjeri web sjedišta u Djangu:

- [Instagram](https://www.instagram.com/) (velikim dijelom)
- [RiTeh](http://www.riteh.uniri.hr/) (shoutout: [Zavod za računarstvo](http://www.riteh.uniri.hr/ustroj/zavodi/zr/))

## Kako radi web aplikacija

Web radi po modelu klijent-poslužitelj. Klijent (najčešće web preglednik) šalje **HTTP zahtjev** (engl. *request*) poslužitelju, a poslužitelj vraća **HTTP odgovor** (engl. *response*).

1. Korisnik u pregledniku upiše adresu, npr. `http://127.0.0.1:8000/predmeti/`.
2. Preglednik pošalje zahtjev `GET /predmeti/` poslužitelju.
3. Django pronađe koji dio koda je zadužen za tu adresu, izvrši ga (po potrebi dohvati podatke iz baze) i složi HTML.
4. Poslužitelj vrati odgovor sa statusnim kodom (npr. `200 OK`) i sadržajem.
5. Preglednik prikaže primljeni HTML.

Django je zadužen za korake 3 i 4. Kako točno Django obrađuje zahtjev opisano je u poglavlju [3. Arhitektura Django aplikacija, URL usmjeravanje i pogledi](03-arhitektura-url-pogledi.md).

## Potrebni alati

Za rad na vježbama trebat će nam:

| Alat | Namjena |
| ---- | ------- |
| Python 3.12 ili noviji | programski jezik u kojem je pisan Django |
| `pip` | upravitelj Python paketa |
| `venv` | izolirana virtualna okruženja za svaki projekt |
| Django 6.1 | web okvir |
| uređivač koda (npr. VS Code) | pisanje koda |
| terminal | pokretanje naredbi |
| Git | upravljanje verzijama (detaljnije u poglavlju [15](15-timski-razvoj-git-dokumentacija.md)) |

Django 6.1 podržava Python 3.12, 3.13 i 3.14.

## Instalacija Pythona

### Windows

1. Preuzmite instalacijski program s [python.org/downloads](https://www.python.org/downloads/).
2. Prilikom instalacije **obavezno označite opciju *Add python.exe to PATH***.
3. Otvorite novi terminal (PowerShell ili Command Prompt) i provjerite instalaciju:

``` shell
> python --version
Python 3.13.x
> py --version
Python 3.13.x
```

Na Windowsima je uz `python` dostupan i pokretač `py` koji je koristan kada imate instalirano više verzija Pythona.

### Linux (Debian, Ubuntu i srodni)

``` shell
$ sudo apt update
$ sudo apt install python3 python3-venv python3-pip
$ python3 --version
```

Na Fedori se koristi `sudo dnf install python3`.

### macOS

Python možete instalirati s [python.org](https://www.python.org/downloads/) ili pomoću [Homebrewa](https://brew.sh/):

``` shell
$ brew install python
$ python3 --version
```

{: .napomena }
> Na Linuxu i macOS-u naredba se obično zove `python3`, a na Windowsima `python` ili `py`. Unutar aktiviranog virtualnog okruženja (vidi u nastavku) na svim sustavima radi naredba `python`, pa ćemo u ostatku materijala koristiti nju.

## Virtualno okruženje

Svaki Python projekt ima svoje ovisnosti (pakete određenih verzija). Kada bismo sve pakete instalirali globalno, projekti bi si međusobno smetali: jedan projekt treba Django 5.2, drugi Django 6.1. Zato za svaki projekt stvaramo zasebno **virtualno okruženje**, direktorij s vlastitom kopijom interpretera i vlastitim paketima.

Stvorimo direktorij za vježbe i u njemu virtualno okruženje naziva `.venv`:

``` shell
$ mkdir pzw
$ cd pzw
$ python3 -m venv .venv
```

Na Windowsima:

``` shell
> mkdir pzw
> cd pzw
> py -m venv .venv
```

### Aktivacija okruženja

Linux i macOS (bash, zsh):

``` shell
$ source .venv/bin/activate
(.venv) $
```

Windows, Command Prompt:

``` shell
> .venv\Scripts\activate.bat
(.venv) >
```

Windows, PowerShell:

``` shell
> .venv\Scripts\Activate.ps1
(.venv) >
```

{: .upozorenje }
> Ako PowerShell javi da je izvršavanje skripti onemogućeno, jednom pokrenite `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` i potvrdite promjenu.

Naziv okruženja u zagradama na početku retka, `(.venv)`, znači da je okruženje aktivno. Sve naredbe `python` i `pip` od tog trenutka koriste pakete iz okruženja. Okruženje deaktivirate naredbom `deactivate`.

{: .napomena }
> Virtualno okruženje aktivirate u **svakom novom terminalu** u kojem radite na projektu. Ako vam Django odjednom "nestane", prvo provjerite je li okruženje aktivno.

## Instalacija Djanga

Unutar aktiviranog okruženja ažurirajmo `pip` i instalirajmo Django:

``` shell
(.venv) $ python -m pip install --upgrade pip
(.venv) $ python -m pip install "Django>=6.1,<6.2"
```

Ograničenjem verzije osiguravamo da svi na vježbama rade s istom glavnom verzijom Djanga.

Provjerimo instaliranu verziju:

``` shell
(.venv) $ python -m django --version
6.1
```

### Popis ovisnosti `requirements.txt`

Popis instaliranih paketa s točnim verzijama spremamo u datoteku `requirements.txt`:

``` shell
(.venv) $ python -m pip freeze > requirements.txt
```

Netko drugi (ili vi na drugom računalu) tada jednom naredbom instalira iste pakete:

``` shell
(.venv) $ python -m pip install -r requirements.txt
```

{: .zadatak }
> Stvorite virtualno okruženje, aktivirajte ga, instalirajte Django i stvorite `requirements.txt`. Otvorite datoteku i provjerite koje pakete sadrži osim Djanga.

**Rješenje zadatka.** Osim Djanga, u datoteci su i njegove ovisnosti `asgiref` i `sqlparse` (na Windowsima još i `tzdata`).

## Uređivač koda

Preporučujemo [Visual Studio Code](https://code.visualstudio.com/) s ekstenzijom **Python** (izdavač Microsoft). Nakon otvaranja direktorija projekta (*File → Open Folder*) odaberite interpreter iz virtualnog okruženja: <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> → *Python: Select Interpreter* → odaberite onaj iz `.venv`. Time VS Code ispravno prepoznaje instalirane pakete i nudi dovršavanje koda.

Za isticanje sintakse Django predložaka korisna je i ekstenzija **Django**. Dobra alternativa je PyCharm, koji studenti mogu koristiti uz besplatnu studentsku licencu.

## Korisne naredbe u terminalu

| Radnja | Linux / macOS | Windows |
| ------ | ------------- | ------- |
| ispis sadržaja direktorija | `ls` | `dir` |
| ispis stabla direktorija | `tree` | `tree /F` |
| promjena direktorija | `cd ime` | `cd ime` |
| stvaranje direktorija | `mkdir ime` | `mkdir ime` |
| stvaranje prazne datoteke | `touch ime.py` | `type nul > ime.py` |
| pokretanje Django naredbi | `python manage.py ...` ili `./manage.py ...` | `python manage.py ...` |

Na Linuxu naredbu `tree` po potrebi instalirate s `sudo apt install tree`.

## Čitanje dokumentacije i Stack Overflow

> Tko radi taj i griješi, a iz grešaka se najbolje uči.

Djangovu službenu dokumentaciju možete pronaći [ovdje](https://docs.djangoproject.com/en/6.1/). Pazite da u gornjem desnom kutu dokumentacije bude odabrana verzija koju koristite. Službeni [tutorial](https://docs.djangoproject.com/en/6.1/intro/tutorial01/) izvrstan je dodatni materijal uz ove vježbe.

[Stack Overflow](https://stackoverflow.com/) je mjesto za pitanja i odgovore za profesionalne programere i entuzijaste. Sadrži pitanja i odgovore na širok raspon tema u računalnom programiranju. Više na [Wikipediji](https://en.wikipedia.org/wiki/Stack_Overflow).

Primjeri pitanja postavljenih na Stack Overflowu vezanih za probleme u Pythonu i Djangu:

- [Primjer 1](https://stackoverflow.com/q/3500371)
- [Primjer 2](https://stackoverflow.com/q/28842901)
- [Primjer 3](https://stackoverflow.com/q/755857)

Pri čitanju odgovora obratite pažnju na datum: odgovor napisan za Django 1.x često više ne vrijedi. Zajednica je aktivna i na službenom [Django forumu](https://forum.djangoproject.com/).

{: .napomena }
> Kada dobijete grešku, pročitajte cijelu poruku od dna prema vrhu. Posljednji redak (npr. `ModuleNotFoundError: No module named 'django'`) govori što je pošlo po zlu, a redci iznad njega gdje se to dogodilo.

{: .zadatak }
> - U dokumentaciji pronađite stranicu koja opisuje naredbu `startproject`.
> - Pokrenite `python -c "import django; print(django.get_version())"` i usporedite ispis s ispisom naredbe `python -m django --version`.
> - Deaktivirajte okruženje i ponovno pokrenite `python -m django --version`. Objasnite rezultat.