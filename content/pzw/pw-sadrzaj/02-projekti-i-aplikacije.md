---
author: Milan Petrović
title: "2. Stvaranje Django projekta i aplikacija"
layout: default
parent: PZW
nav_order: 2
has_children: false
has_toc: false
nav_exclude: false
---

# Stvaranje Django projekta i aplikacija
{: .no_toc }

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Projekt i aplikacija

Django razlikuje dva pojma:

- **Projekt** je cijela web stranica: skup postavki (baza podataka, instalirane aplikacije, jezik, vremenska zona) i glavno usmjeravanje URL-ova.
- **Aplikacija** je zaokružena cjelina koja radi jednu stvar, npr. blog, katalog knjiga ili evidencija studenata. Projekt se sastoji od jedne ili više aplikacija, a ista aplikacija se može koristiti u više projekata.

Kroz poglavlja 2 do 6 gradit ćemo projekt `mysite` s aplikacijom `main` za evidenciju predmeta, studenata i profesora.

## Stvaranje prvog projekta

{: .napomena }
> Prije rada aktivirajte virtualno okruženje u kojem je instaliran Django (vidi [1. Postavljanje razvojnog okruženja](01-postavljanje-okruzenja.md)).

Stvaranje direktorija gdje ćemo stvoriti naš projekt:

``` shell
$ mkdir moja_prva_stranica
```

Zatim idemo u taj direktorij naredbom:

``` shell
$ cd moja_prva_stranica
```

U njemu stvaramo Django projekt naredbom:

``` shell
$ django-admin startproject mysite
```

Ostale raspoložive naredbe možemo vidjeti s naredbom `django-admin`, a za detaljnije o pojedinim naredbama koristite `django-admin help`, npr. za naredbu `startproject` na način:

``` shell
$ django-admin help startproject
```

Naredba `startproject` stvara novi direktorij naziva koji smo proslijedili, u našem slučaju to je `mysite`.

{: .napomena }
> Ako na kraj naredbe dodate točku, `django-admin startproject mysite .`, projekt se stvara u trenutnom direktoriju bez dodatnog vanjskog direktorija. Obje varijante su ispravne, samo se razlikuju u jednoj razini direktorija.

Prebacimo se u direktorij `mysite` pomoću naredbe `cd mysite` i ispišimo sadržaj direktorija u obliku stabla naredbom `tree` (na Windowsima `tree /F`), a možete koristiti i naredbu `ls`.

``` shell
$ tree
.
├── manage.py
└── mysite
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

Unutarnji direktorij `mysite` središnji je dio naše stranice. Ovo je "glavna" konfiguracija projekta: postavke i usmjeravanje zahtjeva prema aplikacijama koje ćemo stvoriti. Samu funkcionalnost (prikaz podataka, obrasce, modele) ne pišemo ovdje, nego u aplikacijama.

### Projektni direktorij i njegov sadržaj

Vanjski direktorij `mysite/` je korijenski direktorij projekta, mjesto gdje se nalaze sve datoteke i direktoriji projekta. Njegovo ime Djangu nije bitno i možete ga slobodno preimenovati.

Unutarnji direktorij `mysite/` je Python paket projekta. Njegovo ime koristimo pri uvozu, npr. `mysite.urls`.

Datoteka `mysite/__init__.py` govori interpreteru da se direktorij tretira kao Python paket.

Datoteka `mysite/settings.py` sadrži postavke Django projekta. Najvažniji dio za početak je popis `INSTALLED_APPS`: svaku novu aplikaciju koju stvorimo moramo ovdje ručno dodati.

Datoteka `mysite/urls.py` sadrži deklarirane URL-ove projekta i služi kao "kazalo sadržaja" stranice. Pomoću nje usmjeravamo zahtjeve prema aplikacijama.

Datoteke `mysite/wsgi.py` i `mysite/asgi.py` su ulazne točke za produkcijske web poslužitelje. WSGI je dugogodišnji Python standard za komunikaciju web poslužitelja i aplikacija, a ASGI njegov nasljednik koji podržava i asinkroni Python. Za vrijeme razvoja ove datoteke ne mijenjamo.

Datoteka `manage.py` je pomoćni program za upravljanje projektom iz terminala. Preko nje pokrećemo poslužitelj, stvaramo aplikacije, radimo migracije baze itd.

{: .opasnost }
> Pazite da `SECRET_KEY` iz `settings.py` ne bude javno vidljiv, npr. na GitHubu. Zlonamjerni pojedinac ga može iskoristiti za krivotvorenje kolačića sesije i preuzimanje tuđih računa, uključujući administratorski. Kako ključ čuvati izvan koda opisano je u poglavlju [13. Sigurnost](13-sigurnost.md).

## Osnovne postavke projekta

Otvorite `mysite/settings.py` i pogledajte najvažnije postavke:

| Postavka | Značenje |
| -------- | -------- |
| `BASE_DIR` | putanja do korijenskog direktorija projekta, koristi se za gradnju ostalih putanja |
| `SECRET_KEY` | tajni ključ za kriptografske potpise (kolačići, tokeni) |
| `DEBUG` | ako je `True`, Django prikazuje detaljne stranice s greškama. U produkciji **mora** biti `False` |
| `ALLOWED_HOSTS` | popis domena na kojima stranica smije raditi kad je `DEBUG = False` |
| `INSTALLED_APPS` | popis aplikacija koje čine projekt |
| `MIDDLEWARE` | slojevi kroz koje prolazi svaki zahtjev i odgovor |
| `ROOT_URLCONF` | modul s glavnim URL-ovima (`mysite.urls`) |
| `TEMPLATES` | postavke sustava predložaka |
| `DATABASES` | postavke baze podataka (zadano SQLite) |
| `LANGUAGE_CODE`, `TIME_ZONE` | jezik sučelja i vremenska zona |
| `STATIC_URL` | URL prefiks za statičke datoteke (CSS, JS, slike) |

Prilagodimo jezik i vremensku zonu:

``` python
LANGUAGE_CODE = "hr"

TIME_ZONE = "Europe/Zagreb"

USE_I18N = True

USE_TZ = True
```

S `USE_TZ = True` Django vremena u bazi sprema u UTC-u, a za prikaz ih pretvara u zonu iz `TIME_ZONE`.

## Lokalni poslužitelj za razvoj

Pokrenimo sada lokalni poslužitelj (engl. *development server*) na kojem ćemo razvijati aplikaciju.

{: .upozorenje }
> Za pokretanje poslužitelja koristite zasebni terminal (s aktiviranim virtualnim okruženjem). Poslužitelj radi cijelo vrijeme razvoja i nakon promjene koda sam se ponovno učita, pa ga ne treba ručno ponovno pokretati. Iznimka su nove datoteke koje se ne učitaju dok ih nešto ne uvozi te neke promjene postavki.

U direktoriju u kojem se nalazi `manage.py` pokrenite:

``` shell
$ python manage.py runserver
```

Poslužitelj zaustavljate kombinacijom <kbd>Ctrl</kbd>+<kbd>C</kbd>.

{: .zadatak }
> Provjerite rad poslužitelja posjetom adrese `http://127.0.0.1:8000/` u web pregledniku. Zatim promijenite `LANGUAGE_CODE` u `"hr"` (ako već niste) i osvježite stranicu.

Ovo je poslužitelj na kojem ćemo razvijati Django aplikacije. U terminalu možete vidjeti HTTP zahtjeve koje poslužitelj prima i statusni kod odgovora na njih.

{: .zadatak }
> Provjerite ispis u terminalu prilikom osvježavanja stranice pritiskom na tipke <kbd>Ctrl</kbd>+<kbd>R</kbd> ili <kbd>F5</kbd>. Zatim posjetite `http://127.0.0.1:8000/nepostojece/` i pogledajte statusni kod u terminalu.

Poslužitelj možete pokrenuti i na drugom portu ili ga učiniti dostupnim ostalim računalima u lokalnoj mreži:

``` shell
$ python manage.py runserver 8080
$ python manage.py runserver 0.0.0.0:8000
```

{: .upozorenje }
> Razvojni poslužitelj nije namijenjen za produkciju: nije optimiziran za brzinu ni za sigurnost. Za objavu aplikacije koriste se poslužitelji poput Gunicorna ili Uvicorna.

Prilikom pokretanja primijetit ćete poruku da postoje neprimijenjene migracije (engl. *unapplied migrations*). Što su migracije objašnjeno je u poglavlju [4. Baze podataka, modeli i ORM](04-baze-modeli-orm.md). Zasad ih možete primijeniti naredbom `python manage.py migrate`.

## Stvaranje prve aplikacije

Započnimo sa stvaranjem prve aplikacije. U direktoriju u kojem se nalazi `manage.py` pokrenite:

``` shell
$ python manage.py startapp main
```

Primijetit ćete da je stvoren novi poddirektorij naziva `main`.

``` shell
$ tree main
main
├── __init__.py
├── admin.py
├── apps.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```

| Datoteka | Namjena |
| -------- | ------- |
| `admin.py` | registracija modela u administratorskom sučelju |
| `apps.py` | konfiguracija aplikacije (klasa `MainConfig`) |
| `migrations/` | migracije baze podataka za modele ove aplikacije |
| `models.py` | modeli, tj. opis podataka |
| `tests.py` | testovi |
| `views.py` | pogledi, tj. funkcije i klase koje obrađuju zahtjeve |

Datoteke `urls.py`, `forms.py` i direktorije `templates/` i `static/` stvarat ćemo ručno kada nam zatrebaju.

{: .zadatak }
> Provjerite sadržaj direktorija `mysite/mysite` i direktorija `mysite/main` naredbama `tree` i `ls`.

### Registracija aplikacije u projektu

Django ne zna za aplikaciju dok je ne dodamo u `INSTALLED_APPS`. U datoteci `main/apps.py` definirana je klasa `MainConfig`, a u `mysite/settings.py` dodajemo:

``` python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main.apps.MainConfig",  # ovu liniju dodajemo
]
```

Umjesto `"main.apps.MainConfig"` dovoljno je napisati i samo `"main"`. Django će sam pronaći konfiguracijsku klasu.

{: .upozorenje }
> Zaboravljena registracija aplikacije najčešći je uzrok poruka poput `No changes detected` pri migracijama ili `TemplateDoesNotExist` pri prikazu predložaka.

## Organizacija koda

Nakon dodavanja nekoliko aplikacija i zajedničkih predložaka, tipičan projekt izgleda ovako:

``` text
moja_prva_stranica/
├── .venv/                 # virtualno okruženje (ne ide u Git)
├── requirements.txt
└── mysite/
    ├── manage.py
    ├── db.sqlite3         # baza podataka (ne ide u Git)
    ├── mysite/            # postavke i glavni URL-ovi
    ├── main/              # aplikacija
    │   ├── migrations/
    │   ├── templates/main/
    │   ├── static/main/
    │   ├── admin.py
    │   ├── models.py
    │   ├── urls.py
    │   └── views.py
    ├── templates/         # zajednički predlošci projekta
    └── static/            # zajedničke statičke datoteke projekta
```

Nekoliko preporuka:

- Aplikaciju nazovite po onome što radi (`katalog`, `korisnici`, `blog`), a ne općenito.
- Ako se opis aplikacije ne može izreći jednom rečenicom bez veznika "i", vjerojatno ju treba podijeliti.
- Postavke i usmjeravanje drže se u projektnom paketu, a sva logika u aplikacijama.

## Pregled naredbi `manage.py`

Popis svih naredbi dobijete s `python manage.py help`, a opis pojedine naredbe s `python manage.py help <naredba>`.

| Naredba | Namjena |
| ------- | ------- |
| `runserver` | pokretanje razvojnog poslužitelja |
| `startapp` | stvaranje nove aplikacije |
| `makemigrations` | priprema migracija nakon promjene modela |
| `migrate` | primjena migracija na bazu |
| `createsuperuser` | stvaranje administratora |
| `shell` | interaktivna Python ljuska s učitanim projektom |
| `check` | provjera ispravnosti projekta |
| `test` | pokretanje testova |

{: .zadatak }
> - Stvorite novi projekt `vjezba2` i u njemu dvije aplikacije, `katalog` i `korisnici`. Registrirajte obje u `INSTALLED_APPS`.
> - Pokrenite `python manage.py check` i provjerite da nema grešaka.
> - Namjerno napravite tipfeler u nazivu aplikacije u `INSTALLED_APPS` i ponovno pokrenite `check`. Pročitajte poruku o grešci.