---
parent: 'Django Temelji: Od Projekta do Prve Aplikacije'
nav_order: 2
title: '2.2 Kreiranje Django Projekta'
---

# 2.2 Kreiranje Django Projekta

Sada kada razumijemo teorijsku podlogu Djanga, vrijeme je da zasučemo rukave i stvorimo kostur našeg prvog projekta.

## Preduvjeti

Prije nego što nastavimo, provjerimo jesmo li spremni. U ovom trenutku, trebali biste imati:

1. **Kreiran direktorij projekta** (npr. `moj-django-projekt`).
2. **Kreirano i aktivirano virtualno okruženje** unutar tog direktorija. Vaš terminalski prompt mora imati `(venv)` prefiks!
3. **Instaliran Django** unutar aktivnog okruženja pomoću naredbe `pip install django`.

Ako niste, vratite se na prethodnu cjelinu i dovršite vježbu.

## `django-admin startproject`: Stvaranje kostura

Glavni alat za administrativne zadatke u Djangu je `django-admin`. Koristit ćemo ga za kreiranje početne strukture našeg projekta.

Navigirajte u terminalu do vašeg praznog projektnog direktorija (onog koji sadrži samo `venv` poddirektorij) i pokrenite sljedeću naredbu:

    django-admin startproject myproject .

Obratite pažnju na točku (`.`) na kraju naredbe!

> **Two Scoops Savjet: Zašto točka na kraju?**
>
> Kada pokrenete `django-admin startproject myproject` (bez točke), Django će stvoriti sljedeću strukturu:
>
>     moj-django-projekt/
>     └── myproject/
>         ├── manage.py
>         └── myproject/
>             ├── settings.py
>             └── ...
>
> Ovo stvara nepotrebnu, dodatnu razinu ugniježđivanja (`myproject/myproject`) koja može biti zbunjujuća.
>
> Dodavanjem točke (`.`) na kraju, govorimo Djangu: "Kreiraj projekt u **ovom trenutnom direktoriju**". To rezultira čišćom i preglednijom strukturom gdje se `manage.py` nalazi u korijenu vašeg repozitorija:
>
>     moj-django-projekt/
>     ├── manage.py
>     ├── venv/
>     └── myproject/
>         ├── settings.py
>         └── ...
>
> Ovo je preporučena praksa za organizaciju projekta.

## Anatomija Django Projekta

Naredba `startproject` je za nas generirala nekoliko datoteka i direktorija. Pogledajmo što je što:

* **Vanjski `myproject/` direktorij (korijen projekta):** Ovo je kontejner za vaš projekt. Njegovo ime nije bitno za Django; možete ga preimenovati u što god želite.
* `manage.py`: Ovo je skripta koja služi kao komandno-linijsko sučelje za vaš projekt. Pomoću nje ćemo pokretati server, raditi migracije baze, i izvršavati razne druge Django naredbe. **Ovu datoteku gotovo nikada nećete morati uređivati.**
* **Unutarnji `myproject/` direktorij:** Ovo je stvarni Python paket za vaš projekt. Njegovo ime se koristi za importiranje bilo čega unutar njega (npr. `myproject.settings`).
    * `__init__.py`: Prazna datoteka koja govori Pythonu da ovaj direktorij treba tretirati kao Python paket (omogućuje importiranje).
    * `settings.py`: Konfiguracijska datoteka za cijeli Django projekt. Ovdje se nalaze postavke za bazu podataka, `SECRET_KEY`, lista instaliranih aplikacija (`INSTALLED_APPS`), `DEBUG` mod i još mnogo toga. Ovu datoteku ćemo često mijenjati.
    * `urls.py`: Glavna URL konfiguracija za projekt. Možemo je zamisliti kao "kazalo sadržaja" naše web stranice. Ovdje Django odlučuje koji *view* treba pozvati za određeni URL.
    * `wsgi.py` i `asgi.py`: Ulazne točke za WSGI i ASGI kompatibilne web servere. One se koriste prilikom *deploymenta* (postavljanja aplikacije na produkcijski server) i nećemo ih dirati tijekom razvoja.

## Pokretanje Razvojnog Servera

Najuzbudljiviji trenutak je vidjeti našu stranicu po prvi put! Django dolazi s ugrađenim, laganim web serverom namijenjenim isključivo za razvoj.

1. Provjerite da ste u terminalu i dalje u korijenskom direktoriju projekta (onom gdje se nalazi `manage.py`).
2. Pokrenite server sljedećom naredbom:

        python manage.py runserver

3. U terminalu ćete vidjeti otprilike ovakav ispis:

        Watching for file changes with StatReloader
        Performing system checks...

        System check identified no issues (0 silenced).
        October 23, 2025 - 15:32:00
        Django version 4.1, using settings 'myproject.settings'
        Starting development server at http://127.0.0.1:8000/
        Quit the server with CTRL-C.

4. Otvorite web preglednik i posjetite adresu: **http://127.0.0.1:8000/**

Trebali biste vidjeti Djangovu zadanu pozdravnu stranicu s raketom koja polijeće. To je potvrda da je sve ispravno postavljeno!

Terminal u kojem ste pokrenuli server sada ispisuje logove HTTP zahtjeva. Svaki put kad osvježite stranicu, vidjet ćete novi redak.

Za zaustavljanje servera, vratite se u terminal i pritisnite `Ctrl + C`.
