---
author: Milan Petrović
title: "9. Generiranje testnih podataka i upravljanje bazom"
layout: default
parent: PZW
nav_order: 9
has_children: false
has_toc: false
nav_exclude: false
---

# Generiranje testnih podataka i upravljanje bazom
{: .no_toc }

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Zašto testni podaci

Ručni unos kroz administratorsko sučelje je spor, a s tri knjige ne vidimo kako se ponaša straničenje, pretraga ili brzina upita. Zato bazu za razvoj punimo **testnim podacima** (engl. *dummy data*), nasumično generiranim podacima koji izgledaju stvarno. Postupak punjenja baze početnim ili testnim podacima zove se **sijanje** (engl. *seeding*).

U ovom poglavlju koristimo:

- paket [factory_boy](https://pypi.org/project/factory-boy/) za generiranje objekata (u pozadini koristi [Faker](https://faker.readthedocs.io/)),
- vlastitu naredbu u `manage.py` koja jednom naredbom napuni bazu,
- naredbe `dumpdata` i `loaddata` za izvoz i uvoz podataka (fixtures),
- podatkovne migracije za podatke koji moraju postojati u svakoj instalaciji.

Nastavljamo s projektom `knjiznica` i modelima `Publisher`, `Author` i `Book` iz [poglavlja 7](07-genericki-pogledi.md).

## Generiranje podataka paketom factory_boy

Instalacija potrebnog Python paketa:

``` shell
$ python -m pip install factory_boy
```

Kada je paket instaliran, potrebno je stvoriti klase koje automatski stvaraju objekte s nasumičnim podacima. Detaljnije o funkcionalnosti možete pronaći u [službenoj dokumentaciji](https://factoryboy.readthedocs.io/).

{: .zadatak }
> Unutar aplikacije `main` stvorite datoteku `factories.py`.

Datoteka `main/factories.py` služi kao predložak za popunjavanje modela iz `main/models.py`. Primijetit ćete sličnost u stilu pisanja klasa: za svaki model definiramo odgovarajuću tvornicu (engl. *factory*).

``` python
import factory
from factory.django import DjangoModelFactory

from main.models import Author, Book, Publisher


class PublisherFactory(DjangoModelFactory):
    class Meta:
        model = Publisher
        django_get_or_create = ("name",)

    name = factory.Faker("company", locale="hr_HR")
    address = factory.Faker("street_address", locale="hr_HR")
    city = factory.Faker("city", locale="hr_HR")
    country = "Hrvatska"
    website = factory.Faker("url")


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker("name", locale="hr_HR")
    address = factory.Faker("street_address", locale="hr_HR")
    city = factory.Faker("city", locale="hr_HR")
    country = factory.Faker("country", locale="hr_HR")
    date_of_birth = factory.Faker("date_between", start_date="-90y", end_date="-20y")


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=4)
    abstract = factory.Faker("paragraph", nb_sentences=5)
    author = factory.SubFactory(AuthorFactory)
    publisher = factory.SubFactory(PublisherFactory)
    publication_date = factory.Faker("date_between", start_date="-30y", end_date="today")
```

| Izraz | Značenje |
| ----- | -------- |
| `factory.Faker("name", locale="hr_HR")` | nasumično hrvatsko ime i prezime |
| `"Hrvatska"` | ista vrijednost za sve objekte |
| `factory.SubFactory(AuthorFactory)` | za svaku knjigu stvara se i novi autor |
| `factory.Iterator(Author.objects.all())` | knjige se redom dodjeljuju **postojećim** autorima |
| `factory.Sequence(lambda n: f"Knjiga {n}")` | jedinstvena vrijednost s rednim brojem |
| `django_get_or_create = ("name",)` | ako izdavač tog imena postoji, koristi se postojeći (polje `name` je jedinstveno) |

{: .napomena }
> Za `DateField` koristimo `date_between` koji vraća datum. Faker `date_time` vraća datum i vrijeme, što za `DateField` nije prikladno.

{: .zadatak }
> Isprobajte tvornice u ljusci. Prije pokretanja ljuske provjerite jesu li primijenjene sve migracije.

``` shell
$ python manage.py shell
```

``` python
>>> from main.factories import AuthorFactory, BookFactory
>>> a = AuthorFactory()
>>> a.name
>>> b = BookFactory()
>>> b.title
>>> b.author
>>> BookFactory(author=a)                # vrijednosti možemo i zadati
>>> BookFactory.create_batch(5, author=a)  # pet knjiga istog autora
>>> AuthorFactory.build()                # objekt koji NIJE spremljen u bazu
```

{: .zadatak }
> Provjerite u administratorskom sučelju jesu li podaci generirani tvornicama spremljeni u bazu.

## Vlastita naredba u `manage.py`

Kada su tvornice napisane i isprobane, napravit ćemo vlastitu naredbu koja jednim pozivom obriše stare i stvori nove testne podatke. Za početak pokrenite:

``` shell
$ python manage.py
```

Ispisao se popis trenutno dostupnih naredbi. Django vlastite naredbe traži u direktoriju `management/commands/` svake aplikacije. Oba direktorija moraju biti Python paketi, tj. sadržavati datoteku `__init__.py`.

Linux i macOS:

``` shell
$ mkdir -p main/management/commands
$ touch main/management/__init__.py main/management/commands/__init__.py
$ touch main/management/commands/setup_test_data.py
```

Windows (PowerShell):

``` shell
> mkdir main\management\commands
> New-Item main\management\__init__.py, main\management\commands\__init__.py, main\management\commands\setup_test_data.py
```

Ime datoteke postaje ime naredbe. Sadržaj datoteke `main/management/commands/setup_test_data.py` ([detaljnije o vlastitim upravljačkim naredbama](https://docs.djangoproject.com/en/6.1/howto/custom-management-commands/)):

``` python
import random

from django.core.management.base import BaseCommand
from django.db import transaction

from main.factories import AuthorFactory, BookFactory, PublisherFactory
from main.models import Author, Book, Publisher


class Command(BaseCommand):
    help = "Briše postojeće i generira nove testne podatke"

    def add_arguments(self, parser):
        parser.add_argument("--authors", type=int, default=10, help="broj autora")
        parser.add_argument("--books", type=int, default=100, help="broj knjiga")

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Brisanje starih podataka...")
        for model in [Book, Author, Publisher]:
            model.objects.all().delete()

        self.stdout.write("Stvaranje novih podataka...")
        publishers = PublisherFactory.create_batch(5)
        authors = AuthorFactory.create_batch(options["authors"])

        for _ in range(options["books"]):
            BookFactory(author=random.choice(authors), publisher=random.choice(publishers))

        self.stdout.write(self.style.SUCCESS(
            f"Stvoreno {options['authors']} autora i {options['books']} knjiga."
        ))
```

Dekorator `@transaction.atomic` označava da se cijela metoda `handle()` izvršava kao jedna transakcija ([detaljnije o modulu transaction](https://docs.djangoproject.com/en/6.1/topics/db/transactions/)). Ako se u bilo kojem trenutku dogodi greška, sve promjene se poništavaju i baza ostaje kakva je bila. Nikad ne ostanemo sa "pola obrisanom" bazom.

{: .zadatak }
> Isprobajte stvorenu naredbu, a zatim provjerite unesene podatke u administratorskom sučelju i na popisu knjiga.

``` shell
$ python manage.py setup_test_data
$ python manage.py setup_test_data --authors 3 --books 20
$ python manage.py help setup_test_data
```

{: .upozorenje }
> Naredba briše **sve** knjige, autore i izdavače. Namijenjena je isključivo razvojnoj bazi.

## Fixture: izvoz i uvoz podataka

**Fixture** je datoteka s podacima (JSON, XML ili YAML) koje Django može uvesti u bazu. Najjednostavniji način rada s njima su naredbe `dumpdata` i `loaddata`.

Naredbom `dumpdata` izvozimo zapise iz baze ([dokumentacija naredbe dumpdata](https://docs.djangoproject.com/en/6.1/ref/django-admin/#dumpdata)):

``` shell
$ python manage.py dumpdata main.Author --pks 1 --indent 4 --output 0001_author.json
```

{: .upozorenje }
> Umjesto preusmjeravanja izlaza znakom `>` koristimo opciju `--output`. U Windows PowerShellu preusmjeravanje može datoteku spremiti u kodiranju UTF-16, koje `loaddata` ne može pročitati.

Sadržaj datoteke izgleda ovako:

``` json
[
{
    "model": "main.author",
    "pk": 1,
    "fields": {
        "name": "Ivana Horvat",
        "address": "Ilica 1",
        "city": "Zagreb",
        "country": "Hrvatska",
        "date_of_birth": "1975-03-14",
        "date_of_death": null
    }
}
]
```

Ostali korisni primjeri:

``` shell
$ python manage.py dumpdata main --indent 2 --output main_podaci.json   # cijela aplikacija
$ python manage.py dumpdata main.Publisher main.Author --indent 2 --output autori.json
$ python manage.py dumpdata --exclude contenttypes --exclude auth.permission --indent 2 --output sve.json
```

{: .zadatak }
> Izvezite autora s primarnim ključem 1, zatim ga obrišite iz baze.

**Rješenje zadatka.**

``` python
>>> from main.models import Author
>>> Author.objects.filter(pk=1).delete()
```

Za uvoz podataka u bazu koristimo naredbu `loaddata` ([dokumentacija naredbe loaddata](https://docs.djangoproject.com/en/6.1/ref/django-admin/#loaddata)).

{: .zadatak }
> Uvezite prethodno stvoreni `0001_author.json` u bazu i provjerite je li autor ponovno tu. Što se dogodilo s njegovim knjigama?

``` shell
$ python manage.py loaddata 0001_author.json
```

**Rješenje zadatka.** Autor je vraćen s istim primarnim ključem, ali knjige nisu: obrisane su kaskadno (`on_delete=models.CASCADE`), a nisu bile u izvezenoj datoteci.

{: .napomena }
> `loaddata` traži datoteke i u direktoriju `fixtures/` svake aplikacije. Ako datoteku spremite kao `main/fixtures/0001_author.json`, dovoljno je pokrenuti `python manage.py loaddata 0001_author`. Tu ćemo konvenciju koristiti i u testovima (vidi [poglavlje 14](14-testiranje-i-uzorci-dizajna.md)).

### Prirodni ključevi

Primarni ključevi se razlikuju od baze do baze, pa fixture koji se oslanja na njih nije prenosiv. Primjer s korisnicima i grupama:

``` python
>>> from django.contrib.auth.models import Group, User
>>> usergroup = Group.objects.create(name="usergroup")
>>> ivo = User.objects.create_user("ivo")
>>> ivo.pk
>>> ivo.groups.add(usergroup)
```

``` shell
$ python manage.py dumpdata auth.User --pks 2 --indent 4
$ python manage.py dumpdata auth.User --pks 2 --indent 4 --natural-foreign
```

U prvom ispisu grupa je navedena primarnim ključem (npr. `"groups": [1]`), a u drugom prirodnim ključem, tj. imenom (`"groups": [["usergroup"]]`). Takav fixture radi i u bazi u kojoj grupa ima drugi primarni ključ.

### Poništavanje sijanja

Ponekad želimo iz baze ukloniti točno one zapise koje smo uvezli fixtureom. Za to možemo napisati naredbu `revert_seed` koja čita fixture i briše zapise s navedenim primarnim ključevima. Datoteka `main/management/commands/revert_seed.py`:

``` python
import json
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Briše iz baze zapise navedene u zadanim fixture datotekama"

    def add_arguments(self, parser):
        parser.add_argument("fixtures", nargs="+", help="putanje do JSON datoteka")

    def handle(self, *args, **options):
        # datoteke obrađujemo obrnutim redom kako bi se ovisni zapisi brisali prvi
        for path in sorted(options["fixtures"], reverse=True):
            try:
                records = json.loads(Path(path).read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as e:
                raise CommandError(f"Ne mogu pročitati {path}: {e}")

            self.stdout.write(f"Poništavanje {path}")
            for record in reversed(records):
                model = apps.get_model(record["model"])  # npr. "main.author"
                deleted, _ = model.objects.filter(pk=record["pk"]).delete()
                status = "obrisan" if deleted else "nije pronađen"
                self.stdout.write(f"  {model.__name__}(pk={record['pk']}): {status}")
```

``` shell
$ python manage.py revert_seed 0001_author.json
```

Funkcija `apps.get_model()` iz oznake modela u fixtureu (`"main.author"`) dohvaća klasu modela, pa naredba radi za sve modele.

## Podatkovne migracije

Testni podaci služe samo za razvoj. Postoje i podaci koji moraju postojati u **svakoj** instalaciji aplikacije, npr. početni popis žanrova ili zadane grupe korisnika. Njih dodajemo **podatkovnom migracijom**, pa se automatski unesu pri `migrate`.

Prazna migracija stvara se naredbom:

``` shell
$ python manage.py makemigrations main --empty --name pocetni_izdavaci
```

U stvorenu datoteku `main/migrations/000X_pocetni_izdavaci.py` dodajemo funkcije za unos i uklanjanje podataka:

``` python
from django.db import migrations

IZDAVACI = [
    {"name": "Školska knjiga", "address": "Masarykova 28", "city": "Zagreb", "country": "Hrvatska"},
    {"name": "Profil", "address": "Kaptol 25", "city": "Zagreb", "country": "Hrvatska"},
]


def dodaj_izdavace(apps, schema_editor):
    Publisher = apps.get_model("main", "Publisher")
    for podaci in IZDAVACI:
        Publisher.objects.get_or_create(name=podaci["name"], defaults=podaci)


def ukloni_izdavace(apps, schema_editor):
    Publisher = apps.get_model("main", "Publisher")
    Publisher.objects.filter(name__in=[p["name"] for p in IZDAVACI]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),  # ostavite ono što je Django sam upisao
    ]

    operations = [
        migrations.RunPython(dodaj_izdavace, ukloni_izdavace),
    ]
```

{: .upozorenje }
> U migracijama model dohvaćamo s `apps.get_model()`, a ne uvozom `from main.models import Publisher`. Migracija mora raditi s modelom kakav je bio u trenutku te migracije, a ne s današnjom verzijom.

## Upravljanje migracijama i bazom

| Naredba | Namjena |
| ------- | ------- |
| `python manage.py showmigrations` | popis migracija i jesu li primijenjene |
| `python manage.py sqlmigrate main 0002` | SQL koji izvršava migracija |
| `python manage.py migrate main 0002` | vraćanje baze na stanje nakon migracije 0002 (poništavanje kasnijih) |
| `python manage.py migrate main zero` | poništavanje svih migracija aplikacije |
| `python manage.py makemigrations --check` | provjera postoje li promjene modela bez migracije (korisno u CI-ju) |
| `python manage.py squashmigrations main 0001 0010` | spajanje više migracija u jednu |
| `python manage.py flush` | brisanje svih podataka (tablice ostaju) |
| `python manage.py dbshell` | klijent baze za SQL upite |

{: .napomena }
> Poništavanje migracije s `RunPython` radi samo ako je zadana i funkcija za poništavanje (drugi argument). Ako je nema, a poništavanje nema smisla, koristite `migrations.RunPython.noop`.

Kopija razvojne baze najjednostavnije se radi naredbom `dumpdata` (kao gore) ili, za SQLite, kopiranjem datoteke `db.sqlite3` dok poslužitelj ne radi.

{: .napomena }
> Stariji paket `django-seed` nije aktivno održavan već nekoliko godina, pa za generiranje podataka koristimo factory_boy.

## Zadaci za vježbu

{: .zadatak }
> - Dodajte naredbi `setup_test_data` argument `--keep` koji preskače brisanje postojećih podataka.
> - Napišite podatkovnu migraciju koja stvara grupu korisnika `Knjižničari` (model `auth.Group`). Pazite da migracija u `dependencies` ima i migraciju aplikacije `auth`.
> - Izvezite sve podatke aplikacije `main` u `main/fixtures/knjiznica.json`, pokrenite `flush`, pa ih ponovno uvezite. Što se dogodilo s administratorskim računom i zašto?
> - Poništite migraciju s početnim izdavačima (`migrate main` na prethodnu migraciju) i provjerite jesu li izdavači uklonjeni.