---
author: Milan Petrović
title: "15. Timski razvoj, upravljanje verzijama i dokumentiranje koda"
layout: default
parent: PZW
nav_order: 15
has_children: false
has_toc: false
nav_exclude: false
---

# Timski razvoj, upravljanje verzijama i dokumentiranje koda
{: .no_toc }

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Zašto upravljanje verzijama

Kada na istom kodu radi više ljudi, ili jedna osoba kroz dulje vrijeme, potrebno je znati tko je što promijenio, kada i zašto, moći se vratiti na ispravnu verziju i spojiti istovremene izmjene. To rješava **sustav za upravljanje verzijama** (engl. *version control system*). Danas je daleko najrašireniji **Git**, a repozitoriji se najčešće dijele preko servisa GitHub, GitLab ili Codeberg.

## Osnove Gita

### Instalacija i postavljanje

Git preuzmite s [git-scm.com](https://git-scm.com/) (na Linuxu `sudo apt install git`). Prije prvog korištenja postavite ime i e-mail adresu, koji se zapisuju uz svaku promjenu:

``` shell
$ git config --global user.name "Ime Prezime"
$ git config --global user.email "ime.prezime@student.uniri.hr"
$ git config --global init.defaultBranch main
```

### Osnovni tijek rada

``` shell
$ cd knjiznica
$ git init                       # stvaranje repozitorija
$ git status                     # stanje radnog direktorija
$ git add .                      # priprema promjena za spremanje
$ git commit -m "Početna verzija projekta knjižnice"
$ git log --oneline              # povijest promjena
$ git diff                       # promjene koje još nisu pripremljene
```

Git datoteke vidi u tri stanja: **promijenjene** u radnom direktoriju, **pripremljene** (engl. *staged*) naredbom `git add` i **spremljene** u povijest naredbom `git commit`. Svaki commit je snimka stanja projekta s porukom koja opisuje promjenu.

### Što ide u repozitorij, a što ne

U repozitorij ide sve što je potrebno da netko drugi pokrene projekt: kod, predlošci, statičke datoteke, **migracije**, `requirements.txt`, dokumentacija. Ne idu stvari koje se mogu ponovno stvoriti, osobne postavke i tajni podaci.

Datoteka `.gitignore` u korijenu repozitorija za Django projekt:

``` text
# Python
__pycache__/
*.py[cod]

# virtualno okruženje
.venv/
venv/

# Django
db.sqlite3
media/
staticfiles/

# tajni podaci i lokalne postavke
.env

# alati
.coverage
htmlcov/
.vscode/
.idea/
```

{: .opasnost }
> Datoteka `.env` s `SECRET_KEY`-em i lozinkama nikad ne smije završiti u repozitoriju (vidi [poglavlje 13](13-sigurnost.md#tajni-podaci-izvan-koda)). Umjesto nje u repozitorij stavite `.env.example` s nazivima varijabli i izmišljenim vrijednostima.

### Udaljeni repozitorij

Nakon stvaranja praznog repozitorija na GitHubu ili GitLabu povežite ga s lokalnim i pošaljite promjene:

``` shell
$ git remote add origin git@github.com:korisnik/knjiznica.git
$ git push -u origin main
```

Članovi tima projekt preuzimaju naredbom `git clone`, a tuđe promjene dohvaćaju s `git pull`.

## Grananje

**Grana** (engl. *branch*) je zasebna linija razvoja. Glavna grana (`main`) uvijek treba sadržavati ispravan kod, a svaka nova funkcionalnost ili ispravak razvija se u vlastitoj grani:

``` shell
$ git switch -c feature/pretraga-knjiga    # nova grana i prelazak na nju
$ git add .
$ git commit -m "Dodaj pretragu knjiga po naslovu i autoru"
$ git push -u origin feature/pretraga-knjiga
```

Kada je funkcionalnost gotova, grana se spaja u `main`, najčešće kroz zahtjev za spajanje (vidi u nastavku). Lokalno se spajanje radi ovako:

``` shell
$ git switch main
$ git pull
$ git merge feature/pretraga-knjiga
```

### Sukobi

Ako su dvije osobe promijenile isti dio iste datoteke, Git ne može sam odlučiti koja je promjena ispravna i javlja **sukob** (engl. *merge conflict*). U datoteci označi oba dijela:

``` text
<<<<<<< HEAD
    paginate_by = 10
=======
    paginate_by = 20
>>>>>>> feature/pretraga-knjiga
```

Sukob rješavate tako da ručno uredite datoteku u željeno stanje, uklonite oznake, pokrenete testove pa napravite `git add` i `git commit`. VS Code ima pregledno sučelje za rješavanje sukoba.

## Timski tijek rada

Uobičajen tijek rada u malom timu (tzv. *GitHub flow*):

1. Zadatak se zapiše kao **issue** s opisom i kriterijima prihvaćanja.
2. Programer stvara granu za taj zadatak.
3. Radi male, smislene commitove.
4. Šalje granu i otvara **zahtjev za spajanje** (engl. *pull request*, na GitLabu *merge request*) s opisom promjena i poveznicom na issue.
5. Automatski se pokreću testovi (CI, vidi u nastavku).
6. Barem jedan član tima pregledava kod (engl. *code review*) i komentira.
7. Nakon odobrenja grana se spaja u `main` i briše.

### Poruke commitova

Dobra poruka u prvom retku ukratko (do 50-ak znakova) i u imperativu kaže što commit radi, a po potrebi nakon praznog retka objašnjava zašto:

``` text
Dodaj straničenje na popis autora

Popis autora postao je prespor s više od 500 zapisa.
Prikazujemo 20 autora po stranici, isto kao kod knjiga.
```

Mnogi timovi koriste konvenciju [Conventional Commits](https://www.conventionalcommits.org/) s prefiksima poput `feat:`, `fix:`, `docs:`, `test:` i `refactor:`.

### Pregled koda

Pri pregledu koda tuđeg zahtjeva za spajanje provjerite:

- radi li kod ono što zadatak traži i postoje li testovi za to,
- jesu li zaštićeni pogledi koje trebaju biti (prijava, ovlasti, objekti drugih korisnika),
- jesu li uz promjene modela priložene migracije,
- postoje li očiti problemi s performansama (npr. upiti u petlji),
- je li kod čitljiv i u skladu s dogovorenim stilom.

Komentirajte kod, a ne osobu, i predlažite konkretna rješenja.

## Migracije u timu

Migracije su dio koda i idu u repozitorij. Nekoliko pravila sprječava većinu problema:

- Nakon `git pull` uvijek pokrenite `python manage.py migrate`.
- Ne mijenjajte migracije koje su već spojene u `main` i koje su drugi možda primijenili. Za ispravak napravite novu migraciju.
- Ako dvije osobe u različitim granama naprave migraciju za istu aplikaciju, nakon spajanja postoje dvije migracije s istim prethodnikom (npr. `0004_book_cover` i `0004_author_photo`). Django to prepoznaje, a rješava se naredbom:

``` shell
$ python manage.py makemigrations --merge
```

- U CI-ju pokrenite `python manage.py makemigrations --check --dry-run`, koja javlja grešku ako netko promijeni model, a zaboravi napraviti migraciju.

## Jednako okruženje za sve

Projekt mora raditi jednako na računalu svakog člana tima:

- Ovisnosti s točnim verzijama drže se u `requirements.txt` (vidi [poglavlje 1](01-postavljanje-okruzenja.md#popis-ovisnosti-requirementstxt)). Nakon instalacije novog paketa ažurirajte datoteku i spremite je u commit.
- Postavke koje se razlikuju po računalu (tajni ključ, baza, `DEBUG`) čitaju se iz varijabli okruženja (vidi [poglavlje 13](13-sigurnost.md#tajni-podaci-izvan-koda)).
- Datoteka `README.md` opisuje kako pokrenuti projekt od nule.

## Stil i kvaliteta koda

Kod koji svi pišu na isti način lakše je čitati i pregledavati. Za Python vrijedi stilski vodič [PEP 8](https://peps.python.org/pep-0008/). Ručna provjera stila je gubitak vremena, pa se prepušta alatima. [Ruff](https://docs.astral.sh/ruff/) je brz alat koji provjerava česte greške (engl. *linter*) i formatira kod:

``` shell
$ python -m pip install ruff
$ ruff check .            # pronalazi greške i loše prakse
$ ruff check . --fix      # ispravlja ono što može sam
$ ruff format .           # formatira kod
```

Alat [pre-commit](https://pre-commit.com/) pokreće provjere automatski prije svakog commita. Datoteka `.pre-commit-config.yaml`:

``` yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

``` shell
$ python -m pip install pre-commit
$ pre-commit install          # jednom, nakon kloniranja repozitorija
$ pre-commit autoupdate       # ažurira verzije alata u konfiguraciji
```

## Kontinuirana integracija

**Kontinuirana integracija** (engl. *continuous integration*, CI) znači da se za svaki push i zahtjev za spajanje automatski pokreću provjere i testovi. Tako se greška otkrije prije spajanja u `main`, a ne kada je netko drugi preuzme. Na GitHubu se to radi pomoću GitHub Actions. Datoteka `.github/workflows/tests.yml`:

``` yaml
name: Testovi

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python -m pip install -r requirements.txt
      - run: ruff check .
      - run: python manage.py makemigrations --check --dry-run
      - run: python manage.py test
        env:
          DJANGO_SECRET_KEY: samo-za-testove
          DJANGO_DEBUG: "True"
```

Ovaj primjer pretpostavlja da su `ruff` i ostali alati navedeni u `requirements.txt`. Na GitLabu se isto postiže datotekom `.gitlab-ci.yml`.

## Dokumentiranje koda

### Komentari i docstringovi

Komentari objašnjavaju **zašto** je kod napisan baš tako, a ne **što** radi. Ono što kod radi treba biti vidljivo iz dobrih imena.

``` python
# Loše: ponavlja kod
i += 1  # povećaj i za 1

# Dobro: objašnjava razlog
# Knjižnica broji dane posudbe od sljedećeg radnog dana
dan_pocetka = sljedeci_radni_dan(datum_posudbe)
```

**Docstring** je opis modula, klase ili funkcije, zapisan kao prvi niz znakova u njima ([PEP 257](https://peps.python.org/pep-0257/)). Prikazuju ga uređivači koda i funkcija `help()`, a iz njega se može generirati dokumentacija:

``` python
class BookQuerySet(models.QuerySet):
    """Upiti nad knjigama koji se koriste u više pogleda."""

    def published_after(self, year: int) -> "BookQuerySet":
        """Vraća knjige izdane nakon zadane godine.

        Args:
            year: Godina izdanja; knjige izdane te godine nisu uključene.

        Returns:
            Filtrirani QuerySet knjiga.
        """
        return self.filter(publication_date__year__gt=year)
```

Oznake tipova (engl. *type hints*) poput `year: int` dodatno dokumentiraju kod i omogućuju alatima da uoče greške.

### README

Datoteka `README.md` je prvo što netko vidi u repozitoriju. Trebala bi sadržavati:

- kratak opis projekta i njegove namjene,
- potrebne alate i verzije (Python, Django),
- korake za pokretanje od nule,
- način pokretanja testova,
- opis strukture projekta i poveznice na ostalu dokumentaciju,
- popis autora i licencu.

Primjer dijela s uputama:

~~~ markdown
## Pokretanje

```bash
git clone git@github.com:korisnik/knjiznica.git
cd knjiznica
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env          # i upišite vrijednosti
python manage.py migrate
python manage.py setup_test_data
python manage.py runserver
```
~~~

### Ostala dokumentacija

- **API**: dokumentacija generirana iz koda pomoću `drf-spectacular` (vidi [poglavlje 11](11-rest-api.md#dokumentacija-i-ostale-teme)).
- **Administratorska dokumentacija**: aplikacija `django.contrib.admindocs` u administratorskom sučelju prikazuje docstringove modela i pogleda.
- **Projektna dokumentacija**: veći projekti imaju zasebnu dokumentaciju pisanu u Markdownu, objavljenu alatima poput MkDocsa ili Sphinxa.
- **CHANGELOG**: popis promjena po verzijama.

## Zadaci za vježbu

{: .zadatak }
> Radite u timovima od 2 do 3 osobe.
> - Jedan član tima stavlja projekt `knjiznica` u novi repozitorij na GitHubu ili GitLabu s ispravnim `.gitignore`, `.env.example` i `README.md`, i dodaje ostale članove.
> - Svaki član klonira repozitorij i pokreće projekt isključivo prema uputama iz `README.md`. Što nedostaje u uputama, nadopunite.
> - Svaki član u vlastitoj grani razvije jednu funkcionalnost iz zadataka prethodnih poglavlja (s testovima) i otvori zahtjev za spajanje. Drugi član pregleda kod i ostavi barem jedan komentar.
> - Dvoje članova u svojim granama doda novo polje istom modelu i napravi migraciju. Spojite obje grane i riješite sukob migracija.
> - Postavite pre-commit s Ruffom i GitHub Actions s testovima. Namjerno pošaljite commit s testom koji pada i provjerite da CI to javlja.