---
author: Milan Petrović
title: "5. Relacije među modelima i dohvaćanje podataka"
layout: default
parent: PZW
nav_order: 5
has_children: false
has_toc: false
nav_exclude: false
---

# Relacije među modelima i dohvaćanje podataka
{: .no_toc }

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Relacije među modelima

Podaci u stvarnosti su povezani: predmet ima nositelja, student upisuje više predmeta, svaki student piše jedan završni rad. Django podržava tri vrste veza, detaljno opisane u [Djangovoj dokumentaciji](https://docs.djangoproject.com/en/6.1/topics/db/examples/):

| Veza | Polje u Djangu | Primjer |
| ---- | -------------- | ------- |
| [Many-to-one](https://docs.djangoproject.com/en/6.1/topics/db/examples/many_to_one/) (više-prema-jedan) | `ForeignKey` | više predmeta ima istog nositelja |
| [Many-to-many](https://docs.djangoproject.com/en/6.1/topics/db/examples/many_to_many/) (više-prema-više) | `ManyToManyField` | student upisuje više predmeta, predmet ima više studenata |
| [One-to-one](https://docs.djangoproject.com/en/6.1/topics/db/examples/one_to_one/) (jedan-prema-jedan) | `OneToOneField` | student ima jedan završni rad |

Nastavljamo s projektom `mysite` i modelom `Predmet` iz [prethodnog poglavlja](04-baze-modeli-orm.md).

## Many-to-one

{: .zadatak }
> Definirajte klasu `Profesor` koja sadrži polja `prof_ime` i `prof_prezime` tipa `CharField` duljine 30 te `prof_email` tipa `EmailField`. Unutar klase definirajte metodu `__str__()` koja vraća e-mail adresu profesora. Registrirajte model u administratorskom sučelju te pokrenite `makemigrations` i `migrate`.

**Rješenje zadatka.** U datoteci `main/models.py` (klasu `Profesor` pišemo **iznad** klase `Predmet` jer će je `Predmet` referencirati):

``` python
class Profesor(models.Model):
    prof_ime = models.CharField(max_length=30)
    prof_prezime = models.CharField(max_length=30)
    prof_email = models.EmailField(unique=True)

    def __str__(self):
        return self.prof_email
```

{: .zadatak }
> Izmijenite klasu `Predmet` tako da joj dodate nositelja: polje `predmet_nositelj` neka bude veza many-to-one s modelom `Profesor`. Za definiranje veze koristite `ForeignKey`. Pokrenite `makemigrations` i `migrate`.

**Rješenje zadatka.** U datoteci `main/models.py`:

``` python
class Predmet(models.Model):
    predmet_naslov = models.CharField(max_length=100)
    predmet_sadrzaj = models.TextField()
    predmet_vrijeme_objave = models.DateTimeField("datum objave")
    predmet_nositelj = models.ForeignKey(
        Profesor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="predmeti",
    )

    def __str__(self):
        return self.predmet_naslov
```

U bazi se stvara stupac `predmet_nositelj_id` koji sadrži primarni ključ profesora.

{: .napomena }
> U tablici `main_predmet` već postoje retci. Kada bi novo polje bilo obavezno (bez `null=True`), `makemigrations` bi nas pitao koju vrijednost upisati u postojeće retke. Zato vezu dodanu naknadno činimo neobaveznom ili joj zadajemo `default`.

Argument `on_delete` je obavezan i određuje što se događa s predmetima kada se obriše profesor:

| Vrijednost | Ponašanje |
| ---------- | --------- |
| `models.CASCADE` | brišu se i svi povezani predmeti |
| `models.PROTECT` | brisanje profesora nije dopušteno dok ima predmete (`ProtectedError`) |
| `models.RESTRICT` | slično kao `PROTECT`, ali dopušta brisanje ako se predmeti brišu u istoj kaskadi |
| `models.SET_NULL` | nositelj se postavlja na `NULL` (zahtijeva `null=True`) |
| `models.SET_DEFAULT` | nositelj se postavlja na zadanu vrijednost |
| `models.DO_NOTHING` | Django ne radi ništa, brigu preuzima baza |

Izbor ovisi o značenju podataka: predmet ne treba nestati jer je profesor otišao, pa koristimo `SET_NULL`. Od Djanga 6.1 postoje i varijante koje brisanje prepuštaju samoj bazi podataka (vidi [bilješke izdanja](https://docs.djangoproject.com/en/6.1/releases/6.1/)).

## Many-to-many

{: .zadatak }
> - Dopunite `main/models.py` novom klasom `Student`. Klasa sadrži polja `student_ime` (`CharField` duljine 25), `student_prezime` (`CharField` duljine 50) i `student_broj_xice` (`CharField` duljine 10, jedinstven).
> - Dodajte polje `student_predmeti` koje je s klasom `Predmet` povezano vezom many-to-many.
> - U klasi `Predmet` izmijenite polje `predmet_vrijeme_objave` tako da mu zadana vrijednost bude trenutno vrijeme (`timezone.now`).
> - Definirajte metodu `__str__()` koja vraća `student_broj_xice` i registrirajte model u administratorskom sučelju.
> - Pokrenite `makemigrations` i `migrate`.

**Rješenje zadatka.** Datoteka `main/models.py`:

``` python
from django.db import models
from django.utils import timezone


class Predmet(models.Model):
    predmet_naslov = models.CharField(max_length=100)
    predmet_sadrzaj = models.TextField()
    predmet_vrijeme_objave = models.DateTimeField("datum objave", default=timezone.now)
    # ... predmet_nositelj kao gore ...


class Student(models.Model):
    student_ime = models.CharField(max_length=25)
    student_prezime = models.CharField(max_length=50)
    student_broj_xice = models.CharField(max_length=10, unique=True)
    student_predmeti = models.ManyToManyField(Predmet, related_name="studenti", blank=True)

    def __str__(self):
        return self.student_broj_xice
```

{: .upozorenje }
> Primijetite da pišemo `default=timezone.now`, **bez zagrada**. Tako predajemo funkciju koja se poziva pri svakom stvaranju objekta. S `timezone.now()` bi se vrijeme izračunalo jednom, pri učitavanju modula, i svi bi predmeti dobili isto vrijeme.

Za vezu many-to-many Django stvara pomoćnu tablicu `main_student_student_predmeti` s parovima (student, predmet). Takvu vezu nije bitno na kojoj strani definiramo.

U datoteci `main/admin.py` možemo registrirati više modela odjednom:

``` python
from django.contrib import admin

from .models import Predmet, Profesor, Student

admin.site.register([Predmet, Profesor, Student])
```

Provjerite radi li sve posjetom `http://127.0.0.1:8000/admin/`.

## One-to-one

Studenta i profesora povezat ćemo modelom `ZavrsniRad`: svaki završni rad piše jedan student, a mentor mu je profesor.

{: .zadatak }
> - Definirajte klasu `ZavrsniRad`. Klasa je s modelom `Student` povezana vezom one-to-one koja je ujedno i primarni ključ (`primary_key=True`), uz `on_delete=models.CASCADE`.
> - Dodajte polje `mentor` povezano s modelom `Profesor`. Razmislite koja je vrsta veze ispravna.
> - Dodajte polja `rad_naslov` (`CharField` duljine 200), `rad_zadatak` (`TextField`) i `rad_prvi_upis` (`BooleanField` sa zadanom vrijednošću `True`).
> - Definirajte metodu `__str__()` koja vraća tekst s brojem X-ice studenta i registrirajte model.
> - Pokrenite `makemigrations` i `migrate`.

**Rješenje zadatka.** U datoteci `main/models.py`:

``` python
class ZavrsniRad(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="zavrsni_rad",
    )
    mentor = models.ForeignKey(
        Profesor,
        on_delete=models.PROTECT,
        related_name="mentorstva",
    )
    rad_naslov = models.CharField(max_length=200)
    rad_zadatak = models.TextField()
    rad_prvi_upis = models.BooleanField(default=True)

    def __str__(self):
        return f"Završni rad studenta s brojem X-ice {self.student.student_broj_xice}"
```

{: .napomena }
> Za mentora je ispravna veza `ForeignKey`, a ne `OneToOneField`. Veza one-to-one značila bi da jedan profesor može biti mentor samo jednom radu. Kod modeliranja uvijek postavite pitanje u oba smjera: "koliko radova ima jedan student?" (jedan) i "koliko radova može mentorirati jedan profesor?" (više).

U `main/admin.py` dopunjavamo popis modela:

``` python
admin.site.register([Predmet, Profesor, Student, ZavrsniRad])
```

## Pristup povezanim objektima

Veze se mogu koristiti u oba smjera. Smjer "unatrag" dobiva ime iz argumenta `related_name` (bez njega bi Django koristio `<model>_set`, npr. `profesor.predmet_set`).

| Iz objekta | Izraz | Rezultat |
| ---------- | ----- | -------- |
| predmet | `predmet.predmet_nositelj` | jedan `Profesor` ili `None` |
| profesor | `profesor.predmeti.all()` | svi predmeti kojima je nositelj |
| student | `student.student_predmeti.all()` | svi upisani predmeti |
| predmet | `predmet.studenti.all()` | svi studenti koji su ga upisali |
| student | `student.zavrsni_rad` | jedan `ZavrsniRad` (ili iznimka `RelatedObjectDoesNotExist`) |
| profesor | `profesor.mentorstva.all()` | svi radovi koje mentorira |

Za rad s vezom many-to-many koristimo metode `add()`, `remove()`, `set()` i `clear()`.

## Upiti

Naredba za pokretanje Python ljuske s učitanim projektom:

``` shell
$ python manage.py shell
```

### Stvaranje povezanih objekata

``` python
>>> from main.models import Predmet, Profesor, Student, ZavrsniRad
>>> profesor = Profesor.objects.create(
...     prof_ime="Pero", prof_prezime="Perić", prof_email="pero@uniri.hr"
... )
>>> predmet1 = Predmet.objects.create(
...     predmet_naslov="Programiranje za web", predmet_sadrzaj="Django", predmet_nositelj=profesor
... )
>>> predmet2 = Predmet.objects.create(predmet_naslov="Baze podataka", predmet_sadrzaj="SQL")
>>> predmet2.predmet_nositelj = profesor   # povezivanje preko vanjskog ključa
>>> predmet2.save()
```

Studentu možemo dodati *n* predmeta, ali tek **nakon** što je student spremljen, jer veza many-to-many zahtijeva da oba objekta imaju primarni ključ:

``` python
>>> student = Student.objects.create(
...     student_ime="Ana", student_prezime="Anić", student_broj_xice="0036000001"
... )
>>> student.student_predmeti.add(predmet1, predmet2)
>>> student.student_predmeti.all()
<QuerySet [<Predmet: Programiranje za web>, <Predmet: Baze podataka>]>
```

Stvaranje završnog rada s vezama one-to-one i many-to-one:

``` python
>>> zr = ZavrsniRad(student=student, mentor=profesor, rad_naslov="Web aplikacija u Djangu",
...                 rad_zadatak="Izraditi aplikaciju za evidenciju predmeta.")
>>> zr.save()
>>> student.zavrsni_rad
<ZavrsniRad: Završni rad studenta s brojem X-ice 0036000001>
```

### Osnovni upiti

Upit koji vraća sve objekte tražene klase:

``` python
>>> profesori = Profesor.objects.all()
```

Dohvat **jednog** objekta po zadanoj vrijednosti:

``` python
>>> profesor = Profesor.objects.get(prof_email="pero@uniri.hr")
```

{: .upozorenje }
> `get()` podiže iznimku `Profesor.DoesNotExist` ako objekt ne postoji, odnosno `Profesor.MultipleObjectsReturned` ako ih je pronađeno više. Koristite ga samo za jedinstvene vrijednosti, npr. primarni ključ ili jedinstvenu e-mail adresu.

Pretraga svih objekata čije ime sadrži zadani tekst:

``` python
>>> Profesor.objects.filter(prof_ime__contains="Pero")
```

Isključivanje objekata:

``` python
>>> Predmet.objects.exclude(predmet_nositelj=None)
```

Uzimanje prvih 5 zapisa (u SQL-u postaje `LIMIT 5`):

``` python
>>> Profesor.objects.all()[:5]
```

Sortiranje i dohvaćanje prvog u nizu (znak minus znači silazni poredak):

``` python
>>> Profesor.objects.order_by("prof_prezime", "prof_ime").first()
>>> Predmet.objects.order_by("-predmet_vrijeme_objave")[:3]
```

Ostale korisne metode:

``` python
>>> Student.objects.count()
>>> Student.objects.filter(student_ime="Ana").exists()
>>> Predmet.objects.values_list("predmet_naslov", flat=True)
>>> Profesor.objects.values("prof_ime", "prof_prezime")
```

Metode se mogu ulančavati jer svaka vraća novi `QuerySet`:

``` python
>>> Predmet.objects.filter(predmet_naslov__icontains="web").exclude(predmet_nositelj=None).order_by("predmet_naslov")
```

### Pretraživanje po poljima (lookups)

Uvjet se piše kao `polje__operator=vrijednost` (dvije podvlake):

| Operator | Značenje | Primjer |
| -------- | -------- | ------- |
| `exact` (zadano) | točno jednako | `prof_ime="Pero"` |
| `iexact` | jednako, bez obzira na velika i mala slova | `prof_ime__iexact="pero"` |
| `contains`, `icontains` | sadrži | `predmet_naslov__icontains="web"` |
| `startswith`, `endswith` | počinje, završava s | `student_broj_xice__startswith="0036"` |
| `gt`, `gte`, `lt`, `lte` | veće, veće ili jednako, manje, manje ili jednako | `predmet_ects__gte=6` |
| `in` | nalazi se u popisu | `id__in=[1, 3, 5]` |
| `range` | u rasponu | `predmet_ects__range=(4, 6)` |
| `isnull` | je li `NULL` | `predmet_nositelj__isnull=True` |
| `year`, `month`, `day` | dio datuma | `predmet_vrijeme_objave__year=2026` |

### Upiti preko veza

Dvostruke podvlake služe i za "skakanje" preko veza. Django sam složi potrebni `JOIN`:

``` python
>>> Predmet.objects.filter(predmet_nositelj__prof_prezime="Perić")
>>> Student.objects.filter(student_predmeti__predmet_naslov__icontains="web")
>>> Profesor.objects.filter(predmeti__studenti__student_ime="Ana").distinct()
```

### Složeni uvjeti: objekti `Q` i `F`

Više argumenata u `filter()` spaja se operatorom AND. Za OR i NOT koristimo objekte `Q`:

``` python
>>> from django.db.models import Q
>>> Student.objects.filter(Q(student_ime="Ana") | Q(student_ime="Ivan"))
>>> Student.objects.filter(~Q(student_prezime__startswith="A"))
```

Objekt `F` predstavlja vrijednost polja u bazi, pa njime uspoređujemo polja ili mijenjamo vrijednosti bez dohvaćanja u Python:

``` python
>>> from django.db.models import F
>>> Predmet.objects.update(predmet_ects=F("predmet_ects") + 1)
```

### Agregacija i anotacija

``` python
>>> from django.db.models import Avg, Count
>>> Predmet.objects.aggregate(prosjek_ects=Avg("predmet_ects"))
{'prosjek_ects': 5.5}
>>> for p in Predmet.objects.annotate(broj_studenata=Count("studenti")):
...     print(p.predmet_naslov, p.broj_studenata)
```

`aggregate()` vraća rječnik s jednom vrijednošću za cijeli skup, a `annotate()` svakom objektu dodaje izračunato polje.

### Lijeno izvršavanje i problem N+1

`QuerySet` je **lijen**: stvaranje i ulančavanje ne šalje upit bazi. Upit se izvršava tek kada podatke stvarno trebamo (iteracija, `list()`, `len()`, ispis). SQL upit možete vidjeti s `print(qs.query)`.

Česta zamka je problem N+1 upita:

``` python
>>> for p in Predmet.objects.all():             # 1 upit
...     print(p.predmet_nositelj)               # + 1 upit za svaki predmet
```

Rješenje je unaprijed dohvatiti povezane objekte:

``` python
>>> Predmet.objects.select_related("predmet_nositelj")   # ForeignKey, OneToOne: JOIN
>>> Student.objects.prefetch_related("student_predmeti")  # ManyToMany, unatrag: dodatni upit
```

### Grupne izmjene i brisanje

``` python
>>> Predmet.objects.filter(predmet_nositelj=None).update(predmet_sadrzaj="Nositelj nije određen.")
>>> Student.objects.filter(student_ime="Test").delete()
```

## Korištenje naredbe `manage.py` za upravljanje bazom

- Nakon svake promjene modela pokrenite `python manage.py makemigrations` i `python manage.py migrate`.
- Naredbom `python manage.py flush` brišu se svi podaci iz baze (tablice ostaju).
- Naredba `python manage.py dbshell` otvara klijent baze u kojem možete pisati SQL, npr. `SELECT * FROM main_predmet;`.

{: .upozorenje }
> Ne mijenjajte strukturu tablica ručno kroz `dbshell` (npr. `ALTER TABLE`). Django tada više ne zna kakva je baza i sljedeća migracija može završiti greškom. Sve promjene sheme radite kroz modele i migracije.

## Zadaci za vježbu

{: .zadatak }
> - Kroz administratorsko sučelje dodajte 5 studenata. Od 5 studenata, 3 neka imaju isto ime, primjerice: Marko, Marko, Marko, Ivan i Ana. Prezime i broj X-ice zadajte proizvoljno.
> - Dodajte 3 profesora i 4 predmeta te studentima upišite po nekoliko predmeta.
> - U ljusci napišite upite koji dohvaćaju:
>   1. sve studente koji se zovu Marko,
>   2. broj studenata koji se ne zovu Marko,
>   3. sve predmete nekog profesora (na dva načina: preko `filter()` i preko `related_name`),
>   4. sve studente koji su upisali predmet čiji naslov sadrži riječ "web",
>   5. predmete poredane po broju upisanih studenata, od najvećeg.

**Rješenje zadatka.**

``` python
>>> Student.objects.filter(student_ime="Marko")
>>> Student.objects.exclude(student_ime="Marko").count()
>>> p = Profesor.objects.first()
>>> Predmet.objects.filter(predmet_nositelj=p)
>>> p.predmeti.all()
>>> Student.objects.filter(student_predmeti__predmet_naslov__icontains="web").distinct()
>>> Predmet.objects.annotate(n=Count("studenti")).order_by("-n")
```

## Cjelovit kod modela

``` python
from django.db import models
from django.utils import timezone


class Profesor(models.Model):
    prof_ime = models.CharField(max_length=30)
    prof_prezime = models.CharField(max_length=30)
    prof_email = models.EmailField(unique=True)

    def __str__(self):
        return self.prof_email


class Predmet(models.Model):
    predmet_naslov = models.CharField(max_length=100)
    predmet_sadrzaj = models.TextField()
    predmet_vrijeme_objave = models.DateTimeField("datum objave", default=timezone.now)
    predmet_nositelj = models.ForeignKey(
        Profesor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="predmeti",
    )

    def __str__(self):
        return self.predmet_naslov


class Student(models.Model):
    student_ime = models.CharField(max_length=25)
    student_prezime = models.CharField(max_length=50)
    student_broj_xice = models.CharField(max_length=10, unique=True)
    student_predmeti = models.ManyToManyField(Predmet, related_name="studenti", blank=True)

    def __str__(self):
        return self.student_broj_xice


class ZavrsniRad(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="zavrsni_rad",
    )
    mentor = models.ForeignKey(
        Profesor,
        on_delete=models.PROTECT,
        related_name="mentorstva",
    )
    rad_naslov = models.CharField(max_length=200)
    rad_zadatak = models.TextField()
    rad_prvi_upis = models.BooleanField(default=True)

    def __str__(self):
        return f"Završni rad studenta s brojem X-ice {self.student.student_broj_xice}"
```

Polja `predmet_ects` i `predmet_semestar` iz zadataka [poglavlja 4](04-baze-modeli-orm.md) ovdje nisu prikazana, ali ih ostavite u modelu ako ste ih dodali.