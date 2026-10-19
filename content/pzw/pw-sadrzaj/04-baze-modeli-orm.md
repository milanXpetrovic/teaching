---
author: Milan Petrović
title: "4. Baze podataka, modeli i objektno-relacijsko preslikavanje"
layout: default
parent: PZW
nav_order: 4
has_children: false
has_toc: false
nav_exclude: false
---

# Baze podataka, modeli i objektno-relacijsko preslikavanje
{: .no_toc }

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Objektno-relacijsko preslikavanje

Relacijske baze podataka rade s tablicama, recima i stupcima, a mi u Pythonu radimo s klasama i objektima. **Objektno-relacijsko preslikavanje** (engl. *Object-Relational Mapping*, ORM) povezuje ta dva svijeta, pa s bazom radimo pišući Python, a ORM umjesto nas generira SQL.

| Python (Django) | Relacijska baza |
| --------------- | --------------- |
| klasa modela | tablica |
| atribut (polje) modela | stupac |
| objekt (instanca) modela | redak |
| `Predmet.objects.filter(...)` | `SELECT ... WHERE ...` |
| `predmet.save()` | `INSERT` ili `UPDATE` |
| `predmet.delete()` | `DELETE` |

Prednosti ORM-a su neovisnost o vrsti baze (isti kod radi na SQLiteu, PostgreSQL-u i MySQL-u), zaštita od SQL injekcije te manje ponavljajućeg koda.

## Postavke baze podataka

Zadana baza je SQLite 3 i nalazi se u datoteci `db.sqlite3` u korijenskom direktoriju projekta (pokraj `manage.py`). SQLite ne zahtijeva poseban poslužitelj i idealan je za razvoj. Postavke su u `settings.py` pod `DATABASES`:

``` python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

Za produkciju se najčešće koristi PostgreSQL. Uz instalirani paket `psycopg` (`python -m pip install "psycopg[binary]"`) postavke izgledaju ovako:

``` python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mysite",
        "USER": "mysite_user",
        "PASSWORD": "...",  # u stvarnom projektu iz varijable okruženja, vidi poglavlje 13
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

## Stvaranje modela

Stvoreni model se preslikava na tablicu u bazi podataka, a polja modela postaju stupci te tablice. Django automatski dodaje i primarni ključ `id`, osim ako sami ne odredimo drugo polje kao primarni ključ.

{: .zadatak }
> Otvorite `main/models.py` i definirajte klasu imena `Predmet`. U klasi definirajte polja `predmet_naslov`, `predmet_sadrzaj` i `predmet_vrijeme_objave`. Njihovi tipovi neka budu `CharField()` s parametrom `max_length` postavljenim na `100`, `TextField()` i `DateTimeField()` s opisnim nazivom `"datum objave"`.

**Rješenje zadatka.** Datoteka `main/models.py`:

``` python
from django.db import models


class Predmet(models.Model):
    predmet_naslov = models.CharField(max_length=100)
    predmet_sadrzaj = models.TextField()
    predmet_vrijeme_objave = models.DateTimeField("datum objave")
```

Prvi pozicijski argument polja je opisni naziv (engl. *verbose name*) koji se prikazuje u administratorskom sučelju i obrascima.

{: .zadatak }
> Definirajte metodu `__str__()` unutar klase `Predmet` koja vraća naslov predmeta `predmet_naslov`.

**Rješenje zadatka.** U datoteci `main/models.py` unutar klase `Predmet` dodajemo:

``` python
    def __str__(self):
        return self.predmet_naslov
```

Metoda `__str__()` određuje kako se objekt prikazuje kao tekst: u ljusci, administratorskom sučelju i predlošcima. Bez nje bismo vidjeli neinformativno `Predmet object (1)`.

## Tipovi polja

Službena [Django dokumentacija](https://docs.djangoproject.com/en/6.1/ref/models/fields/) opisuje sva polja. Najčešće korištena su:

| Polje | Namjena | Primjer |
| ----- | ------- | ------- |
| `CharField(max_length=...)` | kraći tekst, obavezna maksimalna duljina | ime, naslov |
| `TextField()` | dugi tekst | opis, sadržaj |
| `IntegerField()`, `PositiveSmallIntegerField()` | cijeli brojevi | broj ECTS bodova |
| `DecimalField(max_digits=..., decimal_places=...)` | decimalni brojevi točne preciznosti | cijena |
| `FloatField()` | decimalni brojevi s pomičnim zarezom | mjerenje |
| `BooleanField()` | istina ili laž | aktivan |
| `DateField()`, `DateTimeField()`, `TimeField()` | datum, datum i vrijeme, vrijeme | datum rođenja |
| `EmailField()`, `URLField()` | tekst s provjerom formata | e-mail, web stranica |
| `SlugField()` | kratki tekst za URL-ove | `uvod-u-django` |
| `FileField()`, `ImageField()` | datoteke i slike (vidi [poglavlje 10](10-static-i-multimedija.md)) | fotografija |
| `ForeignKey`, `ManyToManyField`, `OneToOneField` | veze među modelima (vidi [poglavlje 5](05-relacije-i-upiti.md)) | nositelj predmeta |

### Opcije polja

| Opcija | Značenje |
| ------ | -------- |
| `null=True` | baza smije spremiti `NULL` |
| `blank=True` | polje smije ostati prazno u obrascima |
| `default=...` | zadana vrijednost (vrijednost ili funkcija) |
| `unique=True` | vrijednost mora biti jedinstvena u tablici |
| `choices=...` | dopuštene vrijednosti, prikazuju se kao padajući izbornik |
| `verbose_name=...` | opisni naziv polja |
| `help_text=...` | pomoćni tekst u obrascima |
| `validators=[...]` | dodatne provjere vrijednosti |

{: .napomena }
> `null` se odnosi na bazu, a `blank` na provjeru obrazaca. Za tekstualna polja (`CharField`, `TextField`) Django preporučuje samo `blank=True` jer se "prazno" sprema kao prazan niz `""`, a ne kao `NULL`.

### Klasa `Meta`

Unutarnja klasa `Meta` sadrži postavke modela koje nisu polja:

``` python
class Predmet(models.Model):
    # ... polja ...

    class Meta:
        ordering = ["predmet_naslov"]
        verbose_name = "predmet"
        verbose_name_plural = "predmeti"
```

`ordering` određuje zadani redoslijed rezultata upita, a `verbose_name_plural` ispravlja množinu koju bi Django inače složio dodavanjem slova "s" ("Predmets").

## Migracije

Svaki novi model je nova tablica u bazi podataka, a svaka promjena modela zahtijeva promjenu tablice. Django to radi pomoću **migracija**, Python datoteka koje opisuju promjene sheme baze. Postupak uvijek ima dva koraka:

1. `makemigrations` usporedi modele s postojećim migracijama i zapiše nove promjene u datoteku migracije.
2. `migrate` primijeni sve još neprimijenjene migracije na bazu.

Pokrenimo pripremu migracije:

``` shell
$ python manage.py makemigrations
Migrations for 'main':
  main/migrations/0001_initial.py
    + Create model Predmet
```

{: .upozorenje }
> Ako dobijete poruku `No changes detected`, najvjerojatnije aplikacija `main` nije dodana u `INSTALLED_APPS` u `settings.py` (vidi [poglavlje 2](02-projekti-i-aplikacije.md#registracija-aplikacije-u-projektu)).

{: .zadatak }
> Pročitajte sadržaj datoteke `main/migrations/0001_initial.py`.

Zatim pokrenimo naredbu `migrate` kako bi se migracija izvršila:

``` shell
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, main, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  ...
  Applying main.0001_initial... OK
  Applying sessions.0001_initial... OK
```

Osim naše migracije primijenjene su i migracije ugrađenih aplikacija (`admin`, `auth`, `contenttypes`, `sessions`) koje su navedene u `INSTALLED_APPS`. Zato je poslužitelj pri prvom pokretanju javljao da postoje neprimijenjene migracije.

Nakon svake promjene modela, bilo da se radi o izmjeni ili stvaranju novih modela, potrebno je ponoviti `makemigrations` pa `migrate`.

Korisne naredbe za pregled migracija:

``` shell
$ python manage.py showmigrations      # popis migracija i jesu li primijenjene
$ python manage.py sqlmigrate main 0001  # SQL koji će migracija izvršiti
```

{: .zadatak }
> Pokrenite `python manage.py sqlmigrate main 0001` i pronađite naredbu `CREATE TABLE`. Kako se zove tablica i koje stupce ima?

**Rješenje zadatka.** Tablica se zove `main_predmet` (ime aplikacije i ime modela malim slovima) i ima stupce `id`, `predmet_naslov`, `predmet_sadrzaj` i `predmet_vrijeme_objave`.

## Interakcija s modelom

Za interakciju s modelom koristimo naredbu `python manage.py shell` koja pokreće Python ljusku s učitanim postavkama projekta. Od Djanga 5.2 ljuska automatski uvozi sve modele, a izričit uvoz ne smeta:

``` python
>>> from main.models import Predmet
>>> from django.utils import timezone
```

Za dohvaćanje svih objekata koristimo `Predmet.objects.all()` koji zasad vraća prazan `QuerySet`:

``` python
>>> Predmet.objects.all()
<QuerySet []>
```

Stvorimo novi objekt, postavimo vrijednosti polja i spremimo ga:

``` python
>>> novi_predmet = Predmet()
>>> novi_predmet.predmet_naslov = "Programiranje za web"
>>> novi_predmet.predmet_sadrzaj = "Ovo je opis predmeta."
>>> novi_predmet.predmet_vrijeme_objave = timezone.now()
>>> novi_predmet.save()
>>> novi_predmet.id
1
```

Do poziva `save()` objekt postoji samo u memoriji, a tek nakon njega i u bazi. Isto se može napraviti jednim pozivom:

``` python
>>> Predmet.objects.create(
...     predmet_naslov="Baze podataka",
...     predmet_sadrzaj="Relacijski model i SQL.",
...     predmet_vrijeme_objave=timezone.now(),
... )
<Predmet: Baze podataka>
```

Isprobajmo ponovno `Predmet.objects.all()` i uočimo nove predmete u popisu. Kroz rezultate se može i iterirati, primjerice petljom `for`:

``` python
>>> for p in Predmet.objects.all():
...     print(p.id, p.predmet_naslov)
```

Osnovne operacije:

``` python
>>> p = Predmet.objects.get(id=1)          # dohvat jednog objekta
>>> p.predmet_naslov = "Programiranje za web (PZW)"
>>> p.save()                               # ažuriranje (UPDATE)
>>> Predmet.objects.filter(predmet_naslov__icontains="baze")  # filtriranje
>>> Predmet.objects.count()                # broj zapisa
>>> p.delete()                             # brisanje (DELETE)
```

Upiti su detaljno obrađeni u [poglavlju 5](05-relacije-i-upiti.md#upiti).

## Administratorsko sučelje

Django dolazi s gotovim administratorskim sučeljem za unos i uređivanje podataka. Administratora stvaramo naredbom:

``` shell
$ python manage.py createsuperuser
Username (leave blank to use 'korisnik'):
Email address:
Password:
Password (again):
```

Dodijelite proizvoljno ime i lozinku, a adresu e-pošte zasad možete ostaviti praznu.

{: .zadatak }
> Posjetite na lokalnom poslužitelju adresu `http://127.0.0.1:8000/admin/` i prijavite se.

Model `Predmet` se zasad ne vidi u sučelju jer ga nismo registrirali. Datoteka `mysite/main/admin.py`:

``` python
from django.contrib import admin

from .models import Predmet

admin.site.register(Predmet)
```

{: .zadatak }
> Osvježite stranicu na adresi `http://127.0.0.1:8000/admin/` i dodajte nekoliko predmeta.

### Prilagodba prikaza u administratorskom sučelju

Umjesto osnovne registracije možemo napisati klasu `ModelAdmin` koja određuje stupce u popisu, pretraživanje i filtre:

``` python
from django.contrib import admin

from .models import Predmet


@admin.register(Predmet)
class PredmetAdmin(admin.ModelAdmin):
    list_display = ["predmet_naslov", "predmet_vrijeme_objave"]
    search_fields = ["predmet_naslov", "predmet_sadrzaj"]
    list_filter = ["predmet_vrijeme_objave"]
```

Ovdje se koristi dekorator `@admin.register(Predmet)` umjesto poziva `admin.site.register(Predmet)`. Ne koristite oba za isti model.

{: .zadatak }
> - Dodajte modelu `Predmet` polje `predmet_ects` tipa `PositiveSmallIntegerField` sa zadanom vrijednošću `5`. Napravite i primijenite migraciju. Zašto Django pri `makemigrations` nije tražio vrijednost za postojeće retke?
> - Dodajte polje `predmet_semestar` s izborima `"zimski"` i `"ljetni"` (opcija `choices`) i zadanom vrijednošću `"zimski"`.
> - Prikažite oba nova polja u popisu predmeta u administratorskom sučelju i dodajte filtar po semestru.