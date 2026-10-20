---
author: Milan Petrović
title: "6. Django predlošci i dinamički prikaz sadržaja"
layout: default
parent: PZW
nav_order: 6
has_children: false
has_toc: true
nav_exclude: true
---

# Django predlošci i dinamički prikaz sadržaja
{: .no_toc }

Pogledi pripremaju podatke, a predlošci određuju kako će ih korisnik vidjeti. U ovom poglavlju aplikaciji za evidenciju predmeta i studenata dajemo pravo HTML sučelje.
{: .fs-6 .fw-300 }

{: .savjet-title }
> Ciljevi poglavlja
>
> Nakon ovog poglavlja moći ćete:
> - podatke iz pogleda proslijediti predlošku funkcijom `render()`,
> - koristiti varijable, oznake i filtere jezika predložaka,
> - izgraditi zajednički izgled svih stranica nasljeđivanjem predložaka,
> - povezivati stranice oznakom `url` i prikazivati povezane objekte,
> - objasniti zašto Django automatski zaštićuje ispis varijabli.

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

---

## Zašto predlošci

U [poglavlju 3](03-arhitektura-url-pogledi.md) pogledi su vraćali HTML zapisan izravno u Python kodu. To brzo postaje nepregledno, a dizajneri i programeri si smetaju u istim datotekama. **Predlošci** (engl. *templates*) odvajaju prikaz od logike: pogled pripremi podatke (kontekst), a predložak odredi kako se prikazuju.

Django koristi vlastiti jezik predložaka (Django Template Language, DTL). Namjerno je ograničen: u predlošku se ne pišu proizvoljne Python naredbe, nego samo varijable, oznake i filteri. Logika pripada pogledima i modelima.

## Priprema projekta

Ovo poglavlje nastavlja se na projekt `mysite` iz poglavlja 2 do 5. Ako ste ih radili i u bazi imate nekoliko profesora, predmeta i studenata, ovaj odjeljak možete preskočiti.

Ako krećete od ovog poglavlja, otvorite upute u nastavku. Za desetak minuta imat ćete projekt s modelima i podacima na kojima rade svi primjeri i zadaci.

<details class="priprema" markdown="block">
<summary>Postavljanje projekta od početka</summary>

### 1. Projekt i aplikacija
{: .no_toc }

Detaljno objašnjenje ovih koraka nalazi se u [poglavlju 1](01-postavljanje-okruzenja.md) i [poglavlju 2](02-projekti-i-aplikacije.md).

``` shell
$ mkdir moja_prva_stranica
$ cd moja_prva_stranica
$ python3 -m venv .venv
$ source .venv/bin/activate          # Windows: .venv\Scripts\activate
$ python -m pip install "Django>=6.1,<6.2"
$ django-admin startproject mysite
$ cd mysite
$ python manage.py startapp main
```

### 2. Postavke
{: .no_toc }

U `mysite/settings.py` dodajte aplikaciju u `INSTALLED_APPS` te postavite jezik i vremensku zonu:

`mysite/settings.py`
{: .datoteka }

``` python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main",
]

LANGUAGE_CODE = "hr"
TIME_ZONE = "Europe/Zagreb"
```

### 3. Modeli
{: .no_toc }

Modeli i veze među njima objašnjeni su u [poglavlju 4](04-baze-modeli-orm.md) i [poglavlju 5](05-relacije-i-upiti.md). Profesor je nositelj predmeta (veza many-to-one), student upisuje predmete (many-to-many) i piše jedan završni rad (one-to-one).

`main/models.py`
{: .datoteka }

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

`main/admin.py`
{: .datoteka }

``` python
from django.contrib import admin

from .models import Predmet, Profesor, Student, ZavrsniRad

admin.site.register([Predmet, Profesor, Student, ZavrsniRad])
```

### 4. URL-ovi i početni pogled
{: .no_toc }

`mysite/urls.py`
{: .datoteka }

``` python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("main.urls")),
    path("admin/", admin.site.urls),
]
```

`main/urls.py`
{: .datoteka }

``` python
from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="homepage"),
]
```

`main/views.py`
{: .datoteka }

``` python
from django.http import HttpResponse


def homepage(request):
    return HttpResponse("Dobro došli!")
```

### 5. Baza i početni podaci
{: .no_toc }

Stvorite tablice u bazi:

``` shell
$ python manage.py makemigrations main
$ python manage.py migrate
```

Početne podatke učitat ćemo iz takozvanog *fixturea*, JSON datoteke sa zapisima (detaljnije u [poglavlju 9](09-testni-podaci-i-sijanje.md)). Stvorite direktorij `main/fixtures` i u njemu datoteku:

`main/fixtures/pocetni_podaci.json`
{: .datoteka }

``` json
[
  {"model": "main.profesor", "pk": 1, "fields": {"prof_ime": "Ivana", "prof_prezime": "Horvat", "prof_email": "ivana.horvat@uniri.hr"}},
  {"model": "main.profesor", "pk": 2, "fields": {"prof_ime": "Petar", "prof_prezime": "Babić", "prof_email": "petar.babic@uniri.hr"}},
  {"model": "main.profesor", "pk": 3, "fields": {"prof_ime": "Ana", "prof_prezime": "Marić", "prof_email": "ana.maric@uniri.hr"}},

  {"model": "main.predmet", "pk": 1, "fields": {"predmet_naslov": "Programiranje za web", "predmet_sadrzaj": "Izrada web aplikacija u Djangu.", "predmet_vrijeme_objave": "2026-09-01T08:00:00Z", "predmet_nositelj": 1}},
  {"model": "main.predmet", "pk": 2, "fields": {"predmet_naslov": "Baze podataka", "predmet_sadrzaj": "Relacijski model, SQL i normalizacija.", "predmet_vrijeme_objave": "2026-09-01T08:00:00Z", "predmet_nositelj": 2}},
  {"model": "main.predmet", "pk": 3, "fields": {"predmet_naslov": "Operacijski sustavi", "predmet_sadrzaj": "Procesi, memorija i datotečni sustavi.", "predmet_vrijeme_objave": "2026-09-01T08:00:00Z", "predmet_nositelj": 2}},
  {"model": "main.predmet", "pk": 4, "fields": {"predmet_naslov": "Računalne mreže", "predmet_sadrzaj": "Mrežni slojevi i protokoli.", "predmet_vrijeme_objave": "2026-09-01T08:00:00Z", "predmet_nositelj": null}},

  {"model": "main.student", "pk": 1, "fields": {"student_ime": "Marko", "student_prezime": "Jurić", "student_broj_xice": "0036000001", "student_predmeti": [1, 2]}},
  {"model": "main.student", "pk": 2, "fields": {"student_ime": "Marko", "student_prezime": "Novak", "student_broj_xice": "0036000002", "student_predmeti": [1, 3]}},
  {"model": "main.student", "pk": 3, "fields": {"student_ime": "Marko", "student_prezime": "Knežević", "student_broj_xice": "0036000003", "student_predmeti": [2]}},
  {"model": "main.student", "pk": 4, "fields": {"student_ime": "Ivan", "student_prezime": "Pavić", "student_broj_xice": "0036000004", "student_predmeti": [1, 2, 3]}},
  {"model": "main.student", "pk": 5, "fields": {"student_ime": "Ana", "student_prezime": "Vuković", "student_broj_xice": "0036000005", "student_predmeti": [1]}},
  {"model": "main.student", "pk": 6, "fields": {"student_ime": "Petra", "student_prezime": "Tomić", "student_broj_xice": "0036000006", "student_predmeti": []}},

  {"model": "main.zavrsnirad", "pk": 4, "fields": {"mentor": 1, "rad_naslov": "Web aplikacija za evidenciju studenata u Djangu", "rad_zadatak": "Izraditi web aplikaciju za evidenciju predmeta i studenata.", "rad_prvi_upis": true}},
  {"model": "main.zavrsnirad", "pk": 5, "fields": {"mentor": 2, "rad_naslov": "Optimizacija upita u relacijskim bazama podataka", "rad_zadatak": "Usporediti strategije indeksiranja na stvarnom skupu podataka.", "rad_prvi_upis": true}}
]
```

Učitajte podatke:

``` shell
$ python manage.py loaddata pocetni_podaci
Installed 15 object(s) from 1 fixture(s)
```

U bazi su sada 3 profesora, 4 predmeta (jedan bez nositelja), 6 studenata (od kojih se trojica zovu Marko, a jedna studentica nema upisanih predmeta) i 2 završna rada.

{: .upozorenje }
> Naredba `loaddata` prepisuje postojeće zapise s istim primarnim ključem. Na projektu u kojem već imate vlastite podatke nemojte je pokretati.

### 6. Provjera
{: .no_toc }

Stvorite administratora i pokrenite poslužitelj:

``` shell
$ python manage.py createsuperuser
$ python manage.py runserver
```

Na adresi `http://127.0.0.1:8000/` treba pisati "Dobro došli!", a na `http://127.0.0.1:8000/admin/` treba vidjeti učitane profesore, predmete, studente i završne radove.

</details>

## Gdje Django traži predloške

Postavke su u `settings.py` pod `TEMPLATES`:

`mysite/settings.py`
{: .datoteka }

``` python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # zajednički predlošci projekta
        "APP_DIRS": True,                   # traži i u <aplikacija>/templates/
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

Django traži predložak redom: najprije u direktorijima iz `DIRS`, zatim u direktoriju `templates/` svake aplikacije iz `INSTALLED_APPS`. Koristi se prvi pronađeni.

{: .napomena }
> Predloške aplikacije spremamo u `main/templates/main/`, a ne izravno u `main/templates/`. Dodatni direktorij s imenom aplikacije je **imenski prostor**: kada bi dvije aplikacije imale predložak `index.html`, Django ne bi znao koji želimo. Ovako ih razlikujemo kao `main/index.html` i `blog/index.html`.

Stvorite direktorije (na Windowsima umjesto `mkdir -p main/templates/main` koristite `mkdir main\templates\main`):

``` shell
$ mkdir templates
$ mkdir -p main/templates/main
```

Na kraju poglavlja projekt će imati sljedeće predloške:

``` text
mysite/
├── templates/
│   └── base.html                 # osnovni predložak (zadatak 6.3)
└── main/
    ├── templates/
    │   └── main/
    │       ├── index.html        # početna stranica (zadatak 6.2)
    │       ├── studenti.html     # studenti zadanog imena (zadatak 6.1)
    │       ├── predmeti.html     # popis predmeta (zadatak 6.4)
    │       └── predmet_detalj.html
    ├── urls.py
    └── views.py
```

## Funkcija `render()`

Funkcija `render(request, predlozak, kontekst)` učita predložak, popuni ga podacima iz konteksta (rječnika) i vrati `HttpResponse`.

{: .zadatak-title }
> Zadatak 6.1 · Studenti zadanog imena
>
> 1. Definirajte pogled koji u bazi pronalazi sve studente zadanog imena. Ime neka se prenosi kroz URL (`studenti/ime/<str:ime>/`).
> 2. Popis pronađenih studenata proslijedite funkciji `render` i prikažite u predlošku `main/studenti.html`. Ako nema nijednog studenta, ispišite poruku.
> 3. Posjetite `/studenti/ime/Marko/` i `/studenti/ime/Zvonimir/`.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 6.1</summary>

`main/views.py`
{: .datoteka }

``` python
from django.shortcuts import render

from .models import Student


def studenti_po_imenu(request, ime):
    studenti = Student.objects.filter(student_ime__iexact=ime)
    context = {"ime": ime, "studenti": studenti}
    return render(request, "main/studenti.html", context)
```

Koristimo `iexact` kako bi `/studenti/ime/marko/` pronašao i "Marko".

`main/urls.py`
{: .datoteka }

``` python
path("studenti/ime/<str:ime>/", views.studenti_po_imenu, name="studenti_po_imenu"),
```

`main/templates/main/studenti.html`
{: .datoteka }

{% raw %}
``` django
<h2>Studenti imena {{ ime }}</h2>
<ul>
    {% for s in studenti %}
        <li>
            Ime: {{ s.student_ime }}<br>
            Prezime: {{ s.student_prezime }}<br>
            Broj X-ice: {{ s.student_broj_xice }}
        </li>
    {% empty %}
        <li>Nema studenata tog imena.</li>
    {% endfor %}
</ul>
```
{% endraw %}

</details>

{: .zadatak-title }
> Zadatak 6.2 · Početna stranica s brojem zapisa
>
> Izmijenite pogled `homepage` tako da u bazi prebroji studente, predmete i profesore te brojeve proslijedi predlošku `main/index.html`.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 6.2</summary>

`main/views.py`
{: .datoteka }

``` python
from .models import Predmet, Profesor, Student


def homepage(request):
    context = {
        "broj_studenata": Student.objects.count(),
        "broj_predmeta": Predmet.objects.count(),
        "broj_profesora": Profesor.objects.count(),
    }
    return render(request, "main/index.html", context)
```

`main/templates/main/index.html`
{: .datoteka }

{% raw %}
``` django
<h1>Dobro došli na UNIRI</h1>

<p>Na fakultetu je upisano:</p>
<ul>
    <li><strong>Studenata:</strong> {{ broj_studenata }}</li>
    <li><strong>Predmeta:</strong> {{ broj_predmeta }}</li>
    <li><strong>Profesora:</strong> {{ broj_profesora }}</li>
</ul>
```
{% endraw %}

</details>

{: .napomena }
> Metoda `count()` nikad ne podiže iznimku `DoesNotExist`: ako zapisa nema, jednostavno vraća 0. Iznimka se javlja samo kod dohvata jednog objekta metodom `get()`, a za taj slučaj postoji prečac `get_object_or_404()` (vidi [zadatak 6.4](#popis-i-detalji-predmeta)).

## Sintaksa predložaka

### Varijable

Pomoću varijabli ispisujemo sadržaj proslijeđen kroz kontekst. Kontekst je Python rječnik u kojem su podaci mapirani kao parovi ključ-vrijednost.

{% raw %}
Varijable pišemo unutar dvostrukih vitičastih zagrada, `{{ varijabla }}`:

``` django
<p>Ime: {{ first_name }}, Prezime: {{ last_name }}.</p>
```

Što će iz konteksta `{'first_name': 'Ivo', 'last_name': 'Ivić'}` biti prikazano kao:

``` html
<p>Ime: Ivo, Prezime: Ivić.</p>
```

Točkom pristupamo dijelovima varijable. Django redom pokušava pristup ključu rječnika, atributu, metodi bez argumenata i indeksu popisa. Tako `{{ student.student_ime }}` čita atribut, `{{ predmet.studenti.count }}` poziva metodu, a `{{ popis.0 }}` uzima prvi element.
{% endraw %}

{: .upozorenje }
> Ako varijabla ne postoji ili joj je ime pogrešno napisano, Django ispisuje prazan niz umjesto da javi grešku. Kada se nešto "ne prikazuje", prvo provjerite ime varijable u pogledu i u predlošku.

### Oznake

{% raw %}
Oznake se pišu unutar `{% %}` i predstavljaju logiku unutar predloška: petlje, uvjete, nasljeđivanje, poveznice i slično. Neke oznake imaju i završnu oznaku:

``` django
{% tag %} ... sadržaj ... {% endtag %}
```
{% endraw %}

### Filteri

Filtere koristimo za transformaciju vrijednosti varijabli. Pišu se iza okomite crte, a neki primaju i argument iza dvotočke:

{% raw %}
- `{{ ime|upper }}`: pretvaranje u velika slova (`lower` u mala, `title` prvo slovo svake riječi veliko)
- `{{ studenti|length }}`: duljina popisa ili niza znakova
- `{{ opis|default:"Nema opisa." }}`: zamjena ako je vrijednost prazna
- `{{ predmet.predmet_sadrzaj|truncatewords:30 }}`: prvih 30 riječi
- `{{ predmet.predmet_vrijeme_objave|date:"d.m.Y. H:i" }}`: formatiranje datuma, npr. `19.10.2026. 14:05`
- `{{ tekst|linebreaks }}`: prijelomi redaka postaju `<p>` i `<br>`
- `{{ popis|join:", " }}`: spajanje elemenata popisa
- `{{ n }} book{{ n|pluralize }}`: množina dodavanjem nastavka, prikladna za engleski ("1 book", "2 books"), ali ne i za hrvatsku množinu
{% endraw %}

Popis svih ugrađenih oznaka i filtera nalazi se u [dokumentaciji](https://docs.djangoproject.com/en/6.1/ref/templates/builtins/).

### Komentari

{% raw %}
Jednoredni komentar pišemo kao `{# Ovo neće biti prikazano #}`, a višeredni unutar `{% comment %} ... {% endcomment %}`. Za razliku od HTML komentara, ovi se ne šalju pregledniku.
{% endraw %}

### Petlje

Primjer korištenja petlje `for` s oznakom `empty` za slučaj praznog popisa:

{% raw %}
``` django
<ul>
{% for predmet in predmeti %}
    <li>{{ forloop.counter }}. {{ predmet.predmet_naslov }}</li>
{% empty %}
    <li>Nema predmeta.</li>
{% endfor %}
</ul>
```

Unutar petlje dostupna je varijabla `forloop` s atributima `counter` (od 1), `counter0` (od 0), `first`, `last` i `revcounter`.
{% endraw %}

### Uvjeti

Primjer provjere je li korisnik prijavljen (detaljnije u [poglavlju 12](12-autentifikacija-autorizacija.md)):

{% raw %}
``` django
{% if user.is_authenticated %}
    <p>Hello, {{ user.username }}.</p>
{% endif %}
```
{% endraw %}

Primjer naredbi `if`, `elif` i `else`:

{% raw %}
``` django
{% if studenti|length > 10 %}
    Velika grupa: {{ studenti|length }} studenata.
{% elif studenti %}
    Broj studenata: {{ studenti|length }}
{% else %}
    Nema studenata.
{% endif %}
```
{% endraw %}

U uvjetima se mogu koristiti operatori `==`, `!=`, `<`, `>`, `<=`, `>=`, `in`, `not`, `and` i `or`.

## Nasljeđivanje predložaka

Sve stranice obično dijele isto zaglavlje, izbornik i podnožje. Da ih ne bismo kopirali u svaki predložak, stvaramo **osnovni predložak** s blokovima koje podređeni predlošci mogu nadjačati.

{: .zadatak-title }
> Zadatak 6.3 · Osnovni predložak
>
> 1. Stvorite osnovni predložak `templates/base.html` s naslovom stranice, izbornikom i blokom za sadržaj.
> 2. Provjerite da je u `settings.py` pod `DIRS` navedena putanja `BASE_DIR / "templates"`.
> 3. Izmijenite `main/index.html` tako da nasljeđuje osnovni predložak.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 6.3</summary>

`templates/base.html`
{: .datoteka }

{% raw %}
``` django
<!DOCTYPE html>
<html lang="hr">
<head>
    <meta charset="utf-8">
    <title>{% block title %}Fakultet{% endblock %}</title>
</head>
<body>
    <h1>Fakultet</h1>
    <nav id="sidebar">
        {% block sidebar %}
        <ul>
            <li><a href="{% url 'main:homepage' %}">Početna</a></li>
            <li><a href="{% url 'main:predmeti' %}">Predmeti</a></li>
        </ul>
        {% endblock %}
    </nav>

    <main class="content">
        {% block content %}
        {% endblock %}
    </main>
</body>
</html>
```
{% endraw %}

`main/templates/main/index.html`
{: .datoteka }

{% raw %}
``` django
{% extends "base.html" %}

{% block title %}Početna | {{ block.super }}{% endblock %}

{% block content %}
<h2>Dobro došli na UNIRI</h2>
<ul>
    <li><strong>Studenata:</strong> {{ broj_studenata }}</li>
    <li><strong>Predmeta:</strong> {{ broj_predmeta }}</li>
    <li><strong>Profesora:</strong> {{ broj_profesora }}</li>
</ul>
{% endblock %}
```
{% endraw %}

</details>

{: .upozorenje }
> Oznaka `url` javlja grešku `NoReverseMatch` ako URL zadanog imena ne postoji. Stavku izbornika "Predmeti" dodajte tek kada u [zadatku 6.4](#popis-i-detalji-predmeta) napravite pogled `predmeti`.

{% raw %}
Podređeni predložak počinje oznakom `extends` i definira samo blokove koje mijenja. Oznaka `extends` mora biti prva oznaka u predlošku. Izraz `{{ block.super }}` umeće sadržaj istog bloka iz roditeljskog predloška, u primjeru gore naslov "Fakultet".
{% endraw %}

### Uključivanje dijelova predložaka

Ponavljajuće dijelove (npr. karticu predmeta) izdvajamo u zasebnu datoteku i uključujemo oznakom `include`:

{% raw %}
``` django
{% for p in predmeti %}
    {% include "main/_predmet_kartica.html" with predmet=p %}
{% endfor %}
```
{% endraw %}

Podvlaka na početku imena datoteke je konvencija koja označava da predložak nije cijela stranica. Od Djanga 6.0 postoje i *template partials*, imenovani dijelovi unutar istog predloška ([dokumentacija](https://docs.djangoproject.com/en/6.1/ref/templates/language/)).

## Poveznice s oznakom `url`

{% raw %}
Adrese u predlošcima ne pišemo ručno, nego ih slažemo iz imena URL-a, isto kao funkcijom `reverse()` u [poglavlju 3](03-arhitektura-url-pogledi.md#imenovani-url-ovi-i-funkcija-reverse). Argumenti se navode iza imena:

``` django
<a href="{% url 'main:predmet_detalj' predmet.pk %}">{{ predmet.predmet_naslov }}</a>
```
{% endraw %}

Ako se adresa u `urls.py` promijeni, sve poveznice u predlošcima nastavljaju raditi.

## Popis i detalji predmeta

{: .zadatak-title }
> Zadatak 6.4 · Popis i detalji predmeta
>
> 1. Napravite pogled `predmeti` koji prikazuje sve predmete s nositeljem i brojem upisanih studenata.
> 2. Svaki predmet neka bude poveznica na stranicu s detaljima predmeta (`predmeti/<int:pk>/`).
> 3. Na stranici s detaljima prikažite opis, nositelja i popis upisanih studenata.
> 4. Dodajte stavku "Predmeti" u izbornik osnovnog predloška.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 6.4</summary>

`main/views.py`
{: .datoteka }

``` python
from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from .models import Predmet


def predmeti(request):
    predmeti = (
        Predmet.objects.select_related("predmet_nositelj")
        .annotate(broj_studenata=Count("studenti"))
        .order_by("predmet_naslov")
    )
    return render(request, "main/predmeti.html", {"predmeti": predmeti})


def predmet_detalj(request, pk):
    predmet = get_object_or_404(Predmet, pk=pk)
    return render(request, "main/predmet_detalj.html", {"predmet": predmet})
```

Funkcija `get_object_or_404()` pokušava dohvatiti objekt i, ako on ne postoji, podiže `Http404`. Bez nje bismo za nepostojeći predmet dobili grešku 500 umjesto 404.

`main/urls.py`
{: .datoteka }

``` python
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("studenti/ime/<str:ime>/", views.studenti_po_imenu, name="studenti_po_imenu"),
    path("predmeti/", views.predmeti, name="predmeti"),
    path("predmeti/<int:pk>/", views.predmet_detalj, name="predmet_detalj"),
]
```

`main/templates/main/predmeti.html`
{: .datoteka }

{% raw %}
``` django
{% extends "base.html" %}

{% block title %}Predmeti | {{ block.super }}{% endblock %}

{% block content %}
<h2>Predmeti</h2>
<ul>
    {% for predmet in predmeti %}
        <li>
            <a href="{% url 'main:predmet_detalj' predmet.pk %}">{{ predmet.predmet_naslov }}</a>
            ({{ predmet.predmet_nositelj|default:"nositelj nije određen" }},
            broj studenata: {{ predmet.broj_studenata }})
        </li>
    {% empty %}
        <li>Nema predmeta.</li>
    {% endfor %}
</ul>
{% endblock %}
```
{% endraw %}

`main/templates/main/predmet_detalj.html`
{: .datoteka }

{% raw %}
``` django
{% extends "base.html" %}

{% block title %}{{ predmet.predmet_naslov }} | {{ block.super }}{% endblock %}

{% block content %}
<h2>{{ predmet.predmet_naslov }}</h2>
<p>Objavljeno: {{ predmet.predmet_vrijeme_objave|date:"d.m.Y." }}</p>
<p>Nositelj:
    {% if predmet.predmet_nositelj %}
        {{ predmet.predmet_nositelj.prof_ime }} {{ predmet.predmet_nositelj.prof_prezime }}
    {% else %}
        nije određen
    {% endif %}
</p>

{{ predmet.predmet_sadrzaj|linebreaks }}

<h3>Upisani studenti ({{ predmet.studenti.count }})</h3>
<ul>
    {% for s in predmet.studenti.all %}
        <li>{{ s.student_ime }} {{ s.student_prezime }} ({{ s.student_broj_xice }})</li>
    {% empty %}
        <li>Nitko nije upisao ovaj predmet.</li>
    {% endfor %}
</ul>

<p><a href="{% url 'main:predmeti' %}">Natrag na popis predmeta</a></p>
{% endblock %}
```

U predlošku se metode pozivaju bez zagrada: `predmet.studenti.all`, a ne `predmet.studenti.all()`.
{% endraw %}

</details>

## Automatsko zaštićivanje (autoescape)

{% raw %}
Django sve varijable prije ispisa automatski zaštićuje (engl. *escape*): znakovi `<`, `>`, `&`, `'` i `"` pretvaraju se u HTML entitete. Ako student upiše ime `<script>alert(1)</script>`, predložak će ga prikazati kao tekst, a ne izvršiti kao skriptu. To je zaštita od XSS napada.
{% endraw %}

{% raw %}
{: .opasnost }
> Filter `safe` isključuje zaštitu za pojedinu varijablu, npr. `{{ html_sadrzaj|safe }}`. Koristite ga **samo** za sadržaj koji ste sami generirali i kojem vjerujete, nikad za unos korisnika. Više u [poglavlju 13](13-sigurnost.md).
{% endraw %}

## Kontekstni procesori

{% raw %}
Neke varijable dostupne su u svim predlošcima bez da ih pogled izričito šalje. Dodaju ih kontekstni procesori iz postavke `context_processors`: `request` (trenutni zahtjev), `user` i `perms` (prijavljeni korisnik i njegove ovlasti) te `messages` (poruke korisniku). Primjerice, `{{ request.path }}` možemo iskoristiti za isticanje aktivne stavke izbornika (vidi [zadatak 6.9](#zadaci)).
{% endraw %}

## Vlastiti filteri

<span class="label label-yellow">Dodatno</span> Ovaj odjeljak nije nužan za nastavak kolegija.

Vlastite filtere pišemo u paketu `templatetags` unutar aplikacije. Stvorite praznu datoteku `main/templatetags/__init__.py` i datoteku s filterima:

`main/templatetags/main_extras.py`
{: .datoteka }

``` python
from django import template

register = template.Library()


@register.filter
def inicijali(student):
    return f"{student.student_ime[:1]}. {student.student_prezime[:1]}."
```

{% raw %}
U predlošku ih učitavamo oznakom `load`: `{% load main_extras %}`, a zatim koristimo kao `{{ s|inicijali }}`. Nakon stvaranja direktorija `templatetags` ponovno pokrenite razvojni poslužitelj.
{% endraw %}

## Šalabahter

{% raw %}
| Sintaksa | Namjena |
| -------- | ------- |
| `{{ varijabla }}`, `{{ objekt.atribut }}` | ispis vrijednosti |
| `{% for x in popis %}` … `{% empty %}` … `{% endfor %}` | petlja s granom za prazan popis |
| `{% if uvjet %}` … `{% elif %}` … `{% else %}` … `{% endif %}` | uvjet |
| `{% extends "base.html" %}` | nasljeđivanje osnovnog predloška (prva oznaka u datoteci) |
| `{% block ime %}` … `{% endblock %}` | blok koji podređeni predložak može nadjačati |
| `{{ block.super }}` | sadržaj istog bloka iz roditelja |
| `{% include "dio.html" with x=y %}` | umetanje drugog predloška |
| `{% url 'aplikacija:ime' argument %}` | adresa iz imena URL-a |
| `{% load ime_biblioteke %}` | učitavanje dodatnih oznaka i filtera |
| `{# komentar #}`, `{% comment %}` … `{% endcomment %}` | komentari koji se ne šalju pregledniku |
{% endraw %}

## Sažetak

{: .savjet-title }
> Što smo naučili
>
> - Pogled podatke šalje predlošku kao rječnik (kontekst) funkcijom `render()`.
> - Predloške aplikacije spremamo u `<aplikacija>/templates/<aplikacija>/`, a zajedničke u `templates/` projekta.
> - Osnovni predložak definira zajednički izgled, a podređeni predlošci nadjačavaju samo svoje blokove.
> - Adrese ne pišemo ručno, nego oznakom `url` iz imena URL-a.
> - Za dohvat jednog objekta u pogledu koristimo `get_object_or_404()`.
> - Ispis je automatski zaštićen od XSS-a, a filter `safe` tu zaštitu isključuje.

## Zadaci za vježbu
{: #zadaci }

{: .zadatak-title }
> Zadatak 6.5 · Nepostojeći predmet
>
> Posjetite `/predmeti/9999/` i provjerite da dobivate odgovor 404. Što prikazuje stranica s greškom i zašto?

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 6.5</summary>

Pogled `predmet_detalj` koristi `get_object_or_404()`, koja za nepostojeći predmet podiže `Http404`. Dok je `DEBUG = True`, Django prikazuje žutu stranicu *Page not found (404)* s popisom svih URL uzoraka koje je pokušao, što pomaže pri razvoju. S `DEBUG = False` prikazuje se jednostavna stranica, koju možemo zamijeniti vlastitim predloškom `templates/404.html`.

</details>

{: .zadatak-title }
> Zadatak 6.6 · Popis profesora
>
> 1. Napravite stranicu `profesori/` koja prikazuje sve profesore i za svakog popis predmeta kojima je nositelj.
> 2. Koristite `related_name` iz modela i `prefetch_related` u pogledu.
> 3. Dodajte poveznicu na popis profesora u izbornik osnovnog predloška.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 6.6</summary>

`main/views.py`
{: .datoteka }

``` python
from .models import Profesor


def profesori(request):
    profesori = Profesor.objects.prefetch_related("predmeti").order_by("prof_prezime", "prof_ime")
    return render(request, "main/profesori.html", {"profesori": profesori})
```

`main/urls.py`
{: .datoteka }

``` python
path("profesori/", views.profesori, name="profesori"),
```

`main/templates/main/profesori.html`
{: .datoteka }

{% raw %}
``` django
{% extends "base.html" %}

{% block title %}Profesori | {{ block.super }}{% endblock %}

{% block content %}
<h2>Profesori</h2>
{% for prof in profesori %}
    <h3>{{ prof.prof_ime }} {{ prof.prof_prezime }}</h3>
    <ul>
        {% for predmet in prof.predmeti.all %}
            <li><a href="{% url 'main:predmet_detalj' predmet.pk %}">{{ predmet.predmet_naslov }}</a></li>
        {% empty %}
            <li>Nije nositelj nijednog predmeta.</li>
        {% endfor %}
    </ul>
{% empty %}
    <p>Nema profesora.</p>
{% endfor %}
{% endblock %}
```
{% endraw %}

U izbornik u `templates/base.html` dodajemo:

{% raw %}
``` django
<li><a href="{% url 'main:profesori' %}">Profesori</a></li>
```
{% endraw %}

Zahvaljujući `prefetch_related` stranica izvršava samo dva upita, bez obzira na broj profesora: jedan za profesore i jedan za sve njihove predmete.

</details>

{: .zadatak-title }
> Zadatak 6.7 · Detalji studenta
>
> Napravite stranicu s detaljima studenta (`studenti/<int:pk>/`) s popisom upisanih predmeta i naslovom završnog rada, ako ga student ima.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 6.7</summary>

`main/views.py`
{: .datoteka }

``` python
from .models import Student


def student_detalj(request, pk):
    student = get_object_or_404(Student.objects.prefetch_related("student_predmeti"), pk=pk)
    return render(request, "main/student_detalj.html", {"student": student})
```

`main/urls.py`
{: .datoteka }

``` python
path("studenti/<int:pk>/", views.student_detalj, name="student_detalj"),
```

`main/templates/main/student_detalj.html`
{: .datoteka }

{% raw %}
``` django
{% extends "base.html" %}

{% block title %}{{ student.student_ime }} {{ student.student_prezime }} | {{ block.super }}{% endblock %}

{% block content %}
<h2>{{ student.student_ime }} {{ student.student_prezime }}</h2>
<p>Broj X-ice: {{ student.student_broj_xice }}</p>

<h3>Upisani predmeti</h3>
<ul>
    {% for p in student.student_predmeti.all %}
        <li><a href="{% url 'main:predmet_detalj' p.pk %}">{{ p.predmet_naslov }}</a></li>
    {% empty %}
        <li>Student nema upisanih predmeta.</li>
    {% endfor %}
</ul>

<h3>Završni rad</h3>
{% if student.zavrsni_rad %}
    <p>{{ student.zavrsni_rad.rad_naslov }}
    (mentor: {{ student.zavrsni_rad.mentor.prof_ime }} {{ student.zavrsni_rad.mentor.prof_prezime }})</p>
{% else %}
    <p>Student još nema prijavljen završni rad.</p>
{% endif %}
{% endblock %}
```
{% endraw %}

{: .napomena }
> U Pythonu bi `student.zavrsni_rad` za studenta bez rada podigao iznimku `RelatedObjectDoesNotExist`, pa se tamo koristi `hasattr(student, "zavrsni_rad")`. Predlošci takve iznimke prešućuju i tretiraju vrijednost kao praznu, pa uvjet u predlošku radi bez dodatnih provjera.

</details>

{: .zadatak-title }
> Zadatak 6.8 · Poveznice na studente
>
> Na stranici s detaljima predmeta svakog studenta pretvorite u poveznicu na njegovu stranicu s detaljima iz zadatka 6.7.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 6.8</summary>

U `main/templates/main/predmet_detalj.html` stavku popisa studenata zamijenite s:

{% raw %}
``` django
<li>
    <a href="{% url 'main:student_detalj' s.pk %}">{{ s.student_ime }} {{ s.student_prezime }}</a>
    ({{ s.student_broj_xice }})
</li>
```
{% endraw %}

</details>

{: .zadatak-title }
> Zadatak 6.9 · Aktivna stavka izbornika
>
> Istaknite (npr. podebljajte) stavku izbornika koja odgovara trenutnoj stranici. Stavka "Predmeti" neka bude istaknuta i na popisu predmeta i na stranici s detaljima predmeta.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 6.9</summary>

{% raw %}
Kontekstni procesor `request` u predložak donosi trenutni zahtjev, a `request.resolver_match.url_name` sadrži ime URL-a koji je odgovorio na zahtjev. Atribut `aria-current="page"` je standardni način označavanja trenutne stranice, koji koriste i čitači zaslona.
{% endraw %}

`templates/base.html`
{: .datoteka }

{% raw %}
``` django
<head>
    <meta charset="utf-8">
    <title>{% block title %}Fakultet{% endblock %}</title>
    <style>
        nav a[aria-current="page"] { font-weight: bold; }
    </style>
</head>

...

{% with ime=request.resolver_match.url_name %}
<ul>
    <li><a href="{% url 'main:homepage' %}"
           {% if ime == "homepage" %}aria-current="page"{% endif %}>Početna</a></li>
    <li><a href="{% url 'main:predmeti' %}"
           {% if ime == "predmeti" or ime == "predmet_detalj" %}aria-current="page"{% endif %}>Predmeti</a></li>
    <li><a href="{% url 'main:profesori' %}"
           {% if ime == "profesori" %}aria-current="page"{% endif %}>Profesori</a></li>
</ul>
{% endwith %}
```
{% endraw %}

Stilove ćemo u [poglavlju 10](10-static-i-multimedija.md) premjestiti iz elementa `<style>` u zasebnu CSS datoteku.

</details>

---

[← 5. Relacije i upiti](05-relacije-i-upiti.md){: .btn .mr-2 }
[7. Generički pogledi →](07-genericki-pogledi.md){: .btn .btn-primary }