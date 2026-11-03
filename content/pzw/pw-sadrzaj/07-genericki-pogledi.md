---
author: Milan Petrović
title: "7. Generički pogledi i dinamičko filtriranje"
layout: default
parent: PZW
nav_order: 7
has_children: false
has_toc: false
nav_exclude: false
---

# Generički pogledi i dinamičko filtriranje
{: .no_toc }

Do sada smo svaki pogled pisali kao funkciju. Popisi objekata i stranice s detaljima ponavljaju se u gotovo svakoj aplikaciji, pa Django za njih nudi gotove klase: generičke poglede. U ovom poglavlju započinjemo novi projekt, knjižnicu, i na njemu gradimo popise, detalje i filtriranje prema adresi.

{: .savjet-title }
> Ciljevi poglavlja
>
> Nakon ovog poglavlja moći ćete:
> - objasniti kada i zašto generički pogled zamjenjuje pogled napisan kao funkcija,
> - prikazati popis i detalje objekata pogledima `ListView` i `DetailView`,
> - podijeliti dugačak popis na stranice (straničenje),
> - filtrirati objekte prema argumentima iz URL-a nadjačavanjem metoda `get_queryset()` i `get_context_data()`,
> - prikazati statičnu stranicu pogledom `TemplateView`,
> - opisati redoslijed metoda koje generički pogled poziva pri obradi zahtjeva.

---

## Priprema projekta

Od ovog poglavlja do kraja kolegija gradimo novi projekt: **knjižnicu** s izdavačima, autorima i knjigama.

{: .zadatak-title }
> Zadatak 7.1 · Projekt knjižnica
>
> 1. Stvorite novi Django projekt `knjiznica` i unutar njega aplikaciju `main`.
> 2. Dodajte aplikaciju `main` u `INSTALLED_APPS` te postavite hrvatski jezik i vremensku zonu.
> 3. U `knjiznica/urls.py` dodajte usmjeravanje na `main/urls.py`, a zatim stvorite `main/urls.py`.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 7.1</summary>

Prije stvaranja projekta aktivirajte virtualno okruženje (vidi [poglavlje 1](01-postavljanje-okruzenja.md)).

``` shell
$ django-admin startproject knjiznica
$ cd knjiznica
$ python manage.py startapp main
```

`knjiznica/settings.py`
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

`knjiznica/urls.py`
{: .datoteka }

``` python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
]
```

`main/urls.py`
{: .datoteka }

``` python
from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
]
```

</details>

### Modeli

`main/models.py`
{: .datoteka }

``` python
from django.db import models
from django.urls import reverse


class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=60)
    country = models.CharField(max_length=50)
    website = models.URLField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=60, blank=True)
    country = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("main:author_detail", args=[self.pk])


class Book(models.Model):
    title = models.CharField(max_length=200)
    abstract = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    publisher = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name="books"
    )
    publication_date = models.DateField()

    class Meta:
        ordering = ["-publication_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:book_detail", args=[self.pk])
```

{: .napomena }
> U stvarnosti knjiga može imati više autora, što bi se modeliralo vezom `ManyToManyField` (vidi [poglavlje 5](05-relacije-i-upiti.md#many-to-many)). Radi jednostavnosti ovdje svaka knjiga ima jednog autora.

Metoda `get_absolute_url()` vraća kanonsku adresu objekta. Koriste je generički pogledi, administratorsko sučelje (gumb *View on site*) i predlošci. Imena `main:author_detail` i `main:book_detail` definirat ćemo u nastavku poglavlja.

Provedite migraciju:

``` shell
$ python manage.py makemigrations
$ python manage.py migrate
```

Registrirajte modele:

`main/admin.py`
{: .datoteka }

``` python
from django.contrib import admin

from .models import Author, Book, Publisher

admin.site.register([Author, Book, Publisher])
```

### Predlošci na razini projekta

U [poglavlju 6](06-predlosci-dinamicki-sadrzaj.md) predlošci aplikacije bili su u `main/templates/main/`, a zajednički osnovni predložak u `templates/`. U ovom projektu sve predloške držimo u zajedničkom direktoriju `templates` u korijenskom direktoriju projekta, a predloške aplikacije u njegovom poddirektoriju `templates/main/`. Oba pristupa su ispravna, a zajednički direktorij je praktičan kada su sve aplikacije dio istog projekta.

``` shell
$ mkdir -p templates/main
```

`knjiznica/settings.py`
{: .datoteka }

``` python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        # ...
    },
]
```

Na kraju poglavlja projekt će imati sljedeće predloške:

``` text
knjiznica/
├── knjiznica/
├── main/
└── templates/
    ├── base_generic.html          # osnovni predložak
    └── main/
        ├── homepage.html          # početna stranica
        ├── publisher_list.html    # popis izdavača
        ├── book_list.html         # popis knjiga (zadatak 7.3)
        ├── book_detail.html       # detalji knjige (zadatak 7.4)
        ├── books_by_publisher.html  # knjige izdavača (zadatak 7.5)
        ├── author_list.html       # popis autora (zadatak 7.6)
        ├── author_detail.html     # detalji autora (zadatak 7.7)
        └── about.html             # statična stranica (zadatak 7.8)
```

Osnovni predložak:

`templates/base_generic.html`
{: .datoteka }

{% raw %}
``` django
<!DOCTYPE html>
<html lang="hr">
<head>
    <meta charset="utf-8">
    <title>{% block title %}Knjižnica{% endblock %}</title>
</head>
<body>
    <h1>Moja knjižnica</h1>
    <nav id="sidebar">
        {% block sidebar %}
        <ul>
            <li><a href="{% url 'main:homepage' %}">Početna</a></li>
            <li><a href="{% url 'main:book_list' %}">Knjige</a></li>
            <li><a href="{% url 'main:author_list' %}">Autori</a></li>
            <li><a href="{% url 'main:publisher_list' %}">Izdavači</a></li>
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

{: .upozorenje }
> Oznaka `url` javlja grešku `NoReverseMatch` ako URL zadanog imena ne postoji. Stavke izbornika za knjige, autore i izdavače zato dodajte tek kada u nastavku poglavlja napravite odgovarajuće poglede. HTML komentar `<!-- -->` tu ne pomaže jer Django oznake unutar njega i dalje izvršava.

Početna stranica kao obična funkcija:

`main/views.py`
{: .datoteka }

``` python
from django.shortcuts import render

from .models import Author, Book, Publisher


def homepage(request):
    context = {
        "num_books": Book.objects.count(),
        "num_authors": Author.objects.count(),
        "num_publishers": Publisher.objects.count(),
    }
    return render(request, "main/homepage.html", context)
```

`main/urls.py`
{: .datoteka }

``` python
urlpatterns = [
    path("", views.homepage, name="homepage"),
]
```

`templates/main/homepage.html`
{: .datoteka }

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block content %}
<h2>Dobro došli</h2>
<p>U knjižnici je {{ num_books }} knjiga od {{ num_authors }} autora i {{ num_publishers }} izdavača.</p>
{% endblock %}
```
{% endraw %}

{: .zadatak-title }
> Zadatak 7.2 · Početni podaci
>
> 1. Stvorite administratora.
> 2. Kroz administratorsko sučelje dodajte barem 3 izdavača, 4 autora i 9 knjiga. Barem dva izdavača neka budu iz Hrvatske, a barem jedna knjiga neka nema izdavača. Ostale vrijednosti zadajte proizvoljno.
>
> Ako želite preskočiti ručni unos, podatke možete učitati iz *fixturea* u rješenju. Zadaci u nastavku poglavlja pretpostavljaju te podatke.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 7.2</summary>

``` shell
$ python manage.py createsuperuser
```

Umjesto ručnog unosa stvorite direktorij `main/fixtures` i u njemu datoteku (detaljnije o fixtureima u [poglavlju 9](09-testni-podaci-i-sijanje.md)):

`main/fixtures/knjiznica.json`
{: .datoteka }

``` json
[
  {"model": "main.publisher", "pk": 1, "fields": {"name": "Naklada Kvarner", "address": "Korzo 1", "city": "Rijeka", "country": "Hrvatska"}},
  {"model": "main.publisher", "pk": 2, "fields": {"name": "Zagrebačka knjiga", "address": "Ilica 10", "city": "Zagreb", "country": "Hrvatska"}},
  {"model": "main.publisher", "pk": 3, "fields": {"name": "Thames Press", "address": "1 Fleet Street", "city": "London", "country": "Ujedinjeno Kraljevstvo"}},

  {"model": "main.author", "pk": 1, "fields": {"name": "Ivana Brlić-Mažuranić", "city": "Slavonski Brod", "country": "Hrvatska", "date_of_birth": "1874-04-18", "date_of_death": "1938-09-21"}},
  {"model": "main.author", "pk": 2, "fields": {"name": "Miroslav Krleža", "city": "Zagreb", "country": "Hrvatska", "date_of_birth": "1893-07-07", "date_of_death": "1981-12-29"}},
  {"model": "main.author", "pk": 3, "fields": {"name": "Marija Jurić Zagorka", "city": "Zagreb", "country": "Hrvatska", "date_of_birth": "1873-01-02", "date_of_death": "1957-11-30"}},
  {"model": "main.author", "pk": 4, "fields": {"name": "George Orwell", "city": "London", "country": "Ujedinjeno Kraljevstvo", "date_of_birth": "1903-06-25", "date_of_death": "1950-01-21"}},

  {"model": "main.book", "pk": 1, "fields": {"title": "Čudnovate zgode šegrta Hlapića", "abstract": "Dobrodušni šegrt Hlapić bježi od strogog majstora i na putu doživljava niz pustolovina.", "author": 1, "publisher": 1, "publication_date": "2019-09-02"}},
  {"model": "main.book", "pk": 2, "fields": {"title": "Priče iz davnine", "abstract": "Zbirka bajki nadahnutih slavenskom mitologijom.", "author": 1, "publisher": 1, "publication_date": "2021-03-15"}},
  {"model": "main.book", "pk": 3, "fields": {"title": "Povratak Filipa Latinovicza", "abstract": "Slikar se nakon mnogo godina vraća u rodni kraj i suočava s prošlošću.", "author": 2, "publisher": 2, "publication_date": "2018-05-10"}},
  {"model": "main.book", "pk": 4, "fields": {"title": "Gospoda Glembajevi", "abstract": "Drama o propadanju bogate zagrebačke obitelji.", "author": 2, "publisher": null, "publication_date": "2016-11-20"}},
  {"model": "main.book", "pk": 5, "fields": {"title": "Na rubu pameti", "abstract": "Ispovijest čovjeka koji odbija prihvatiti licemjerje svoje okoline.", "author": 2, "publisher": 2, "publication_date": "2022-01-25"}},
  {"model": "main.book", "pk": 6, "fields": {"title": "Grička vještica", "abstract": "Povijesni roman o progonima vještica u starom Zagrebu.", "author": 3, "publisher": 2, "publication_date": "2020-10-05"}},
  {"model": "main.book", "pk": 7, "fields": {"title": "Kći Lotršćaka", "abstract": "Povijesni roman smješten u stari Zagreb.", "author": 3, "publisher": 1, "publication_date": "2023-04-18"}},
  {"model": "main.book", "pk": 8, "fields": {"title": "Nineteen Eighty-Four", "abstract": "Distopijski roman o totalitarnoj državi i stalnom nadzoru.", "author": 4, "publisher": 3, "publication_date": "2024-02-01"}},
  {"model": "main.book", "pk": 9, "fields": {"title": "Animal Farm", "abstract": "Alegorija o životinjama koje preuzmu farmu i o vlasti koja kvari.", "author": 4, "publisher": 3, "publication_date": "2025-06-12"}}
]
```

Datumi izdanja izmišljeni su za potrebe vježbi.

``` shell
$ python manage.py loaddata knjiznica
Installed 16 object(s) from 1 fixture(s)
```

U bazi su sada 3 izdavača (dva iz Hrvatske), 4 autora i 9 knjiga, od kojih jedna nema izdavača.

</details>

## Zašto generički pogledi

Velik dio web aplikacija svodi se na iste obrasce: prikaži popis objekata, prikaži detalje jednog objekta, stvori, uredi ili obriši objekt. Pogled za popis knjiga napisan kao funkcija izgleda ovako:

``` python
def book_list(request):
    books = Book.objects.all()
    return render(request, "main/book_list.html", {"book_list": books})
```

Za autore, izdavače i sve ostale modele pisali bismo gotovo isti kod. **Generički pogledi** su gotove klase za takve česte zadatke. Isti pogled kao klasa:

``` python
from django.views.generic import ListView


class BookList(ListView):
    model = Book
```

Najčešće korišteni generički pogledi:

| Pogled | Namjena |
| ------ | ------- |
| `TemplateView` | prikaz predloška bez podataka iz baze |
| `ListView` | popis objekata |
| `DetailView` | detalji jednog objekta |
| `CreateView`, `UpdateView`, `DeleteView` | stvaranje, uređivanje i brisanje (vidi [poglavlje 8](08-obrasci-get-post-modelforms.md)) |
| `RedirectView` | preusmjeravanje |

## Pogled `ListView`

Stvorimo prvi generički pogled nad modelom:

`main/views.py`
{: .datoteka }

``` python
from django.views.generic import ListView

from .models import Publisher


class PublisherList(ListView):
    model = Publisher
```

Klasu u pogled pretvaramo metodom `as_view()`:

`main/urls.py`
{: .datoteka }

``` python
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("izdavaci/", views.PublisherList.as_view(), name="publisher_list"),
]
```

`ListView` sam određuje ime predloška prema konvenciji `<aplikacija>/<model>_list.html`, dakle `main/publisher_list.html`.

`templates/main/publisher_list.html`
{: .datoteka }

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block content %}
    <h2>Izdavači</h2>
    <ul>
        {% for publisher in object_list %}
            <li>
                {{ publisher.name }}<br>
                Grad: {{ publisher.city }}
            </li>
        {% empty %}
            <li>Nema izdavača.</li>
        {% endfor %}
    </ul>
{% endblock %}
```
{% endraw %}

`ListView` predlošku šalje popis objekata pod dva imena: `object_list` i `<model>_list` (ovdje `publisher_list`). Drugo ime je čitljivije pa ćemo ga koristiti u nastavku.

Pokrenite poslužitelj i provjerite ispis izdavača na adresi `http://127.0.0.1:8000/izdavaci/`.

### Najčešći atributi

| Atribut | Značenje | Primjer |
| ------- | -------- | ------- |
| `model` | model čiji se objekti prikazuju | `model = Book` |
| `queryset` | upit umjesto `model.objects.all()` | `queryset = Book.objects.select_related("author")` |
| `template_name` | predložak umjesto zadanog | `template_name = "main/knjige.html"` |
| `context_object_name` | ime popisa u predlošku | `context_object_name = "knjige"` |
| `ordering` | poredak | `ordering = ["title"]` |
| `paginate_by` | broj objekata po stranici | `paginate_by = 10` |
| `allow_empty` | ako je `False`, prazan popis vraća 404 | `allow_empty = False` |

### Straničenje

Kada je postavljen atribut `paginate_by`, `ListView` prikazuje samo jednu stranicu popisa, a broj stranice čita iz parametra `page` u adresi (`/knjige/?page=2`). Predložak tada dobiva i varijable `page_obj` (trenutna stranica) i `is_paginated` (ima li popis više od jedne stranice).

{: .zadatak-title }
> Zadatak 7.3 · Popis knjiga sa straničenjem
>
> 1. Napravite pogled `BookList` na adresi `knjige/` koji prikazuje 5 knjiga po stranici. Autora i izdavača dohvatite istim upitom (`select_related`).
> 2. U predlošku `book_list.html` za svaku knjigu ispišite naslov, autora i prvih 40 riječi sažetka.
> 3. Ispod popisa dodajte navigaciju na prethodnu i sljedeću stranicu te broj trenutne stranice.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 7.3</summary>

`main/views.py`
{: .datoteka }

``` python
from .models import Book


class BookList(ListView):
    model = Book
    paginate_by = 5
    queryset = Book.objects.select_related("author", "publisher")
```

`main/urls.py`
{: .datoteka }

``` python
path("knjige/", views.BookList.as_view(), name="book_list"),
```

`templates/main/book_list.html`
{: .datoteka }

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block content %}
<h2>Knjige</h2>

{% for book in book_list %}
    <div class="book">
        <h4>{{ book.title }}</h4>
        <p>Autor: {{ book.author }}</p>
        <p>{{ book.abstract|truncatewords:40 }}</p>
    </div>
{% empty %}
    <p>Nema knjiga.</p>
{% endfor %}

{% if is_paginated %}
<nav class="pagination">
    {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">&laquo; prethodna</a>
    {% endif %}
    Stranica {{ page_obj.number }} od {{ page_obj.paginator.num_pages }}
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">sljedeća &raquo;</a>
    {% endif %}
</nav>
{% endif %}
{% endblock %}
```
{% endraw %}

S podacima iz zadatka 7.2 popis ima dvije stranice. Knjige su poredane od najnovije prema najstarijoj zbog `ordering` u klasi `Meta` modela `Book`.

</details>

## Pogled `DetailView`

`DetailView` prikazuje jedan objekt. Objekt pronalazi prema argumentu `pk` (ili `slug`) iz URL-a, a ako objekt ne postoji, sam vraća 404.

`main/views.py`
{: .datoteka }

``` python
from django.views.generic import DetailView


class BookDetail(DetailView):
    model = Book
```

`main/urls.py`
{: .datoteka }

``` python
path("knjige/<int:pk>/", views.BookDetail.as_view(), name="book_detail"),
```

Predložak se po konvenciji zove `main/book_detail.html`, a objekt je u njemu dostupan kao `object` i kao `book`.

{: .zadatak-title }
> Zadatak 7.4 · Detalji knjige
>
> 1. Napravite predložak `book_detail.html` koji prikazuje naslov, autora, izdavača, datum izdanja i cijeli sažetak knjige. Ako knjiga nema izdavača, ispišite "nepoznat".
> 2. Naslov stranice u pregledniku neka bude naslov knjige.
> 3. Naslove na popisu knjiga pretvorite u poveznice na stranicu s detaljima. Iskoristite metodu `get_absolute_url()`.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 7.4</summary>

`templates/main/book_detail.html`
{: .datoteka }

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block title %}{{ book.title }} | {{ block.super }}{% endblock %}

{% block content %}
<h2>{{ book.title }}</h2>
<p>Autor: {{ book.author }}</p>
<p>Izdavač: {{ book.publisher|default:"nepoznat" }}</p>
<p>Datum izdanja: {{ book.publication_date|date:"d.m.Y." }}</p>
{{ book.abstract|linebreaks }}
{% endblock %}
```
{% endraw %}

U `templates/main/book_list.html` naslov knjige zamijenite poveznicom:

{% raw %}
``` django
<h4><a href="{{ book.get_absolute_url }}">{{ book.title }}</a></h4>
```
{% endraw %}

</details>

## Dinamičko filtriranje

U nastavku je prikazan način na koji se omogućava dinamička pretraga pomoću URL-a. Za zadani naziv izdavača vraćat će se sve knjige koje je taj izdavač objavio. Naziv izdavača neće biti statično zapisan u URL uzorku, nego će se uzimati iz adrese.

Umjesto atributa `model` nadjačavamo metodu `get_queryset()`:

`main/views.py`
{: .datoteka }

``` python
from django.shortcuts import get_object_or_404, render


class PublisherBookList(ListView):
    template_name = "main/books_by_publisher.html"

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.kwargs["publisher"])
        return Book.objects.filter(publisher=self.publisher)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["publisher"] = self.publisher
        return context
```

Argumenti iz URL-a dostupni su u rječniku `self.kwargs`. Metodom `get_context_data()` predlošku šaljemo i samog izdavača, kako bismo mogli ispisati njegovo ime. Popis knjiga i dalje je dostupan kao `book_list`, jer `ListView` ime određuje prema modelu objekata koje vraća `get_queryset()`.

Umjesto da svakog izdavača zadajemo pojedinačno, u URL uzorku koristimo `<str:publisher>`:

`main/urls.py`
{: .datoteka }

``` python
path("izdavaci/<str:publisher>/", views.PublisherBookList.as_view(), name="publisher_books"),
```

{: .zadatak-title }
> Zadatak 7.5 · Knjige izdavača
>
> 1. Stvorite predložak `books_by_publisher.html` koji ispisuje ime izdavača i naslove svih knjiga tog izdavača kao poveznice na detalje knjige.
> 2. Na popisu izdavača ime svakog izdavača pretvorite u poveznicu na njegove knjige.
> 3. Posjetite adresu nepostojećeg izdavača, npr. `/izdavaci/Nepostojeći/`. Što se dogodi i zašto?

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 7.5</summary>

`templates/main/books_by_publisher.html`
{: .datoteka }

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block title %}{{ publisher.name }} | {{ block.super }}{% endblock %}

{% block content %}
    <h2>Knjige izdavača {{ publisher.name }}</h2>
    <ul>
        {% for book in book_list %}
            <li><a href="{{ book.get_absolute_url }}">{{ book.title }}</a></li>
        {% empty %}
            <li>Ovaj izdavač nema knjiga.</li>
        {% endfor %}
    </ul>
{% endblock %}
```
{% endraw %}

U `templates/main/publisher_list.html` ime izdavača zamijenite poveznicom:

{% raw %}
``` django
<a href="{% url 'main:publisher_books' publisher.name %}">{{ publisher.name }}</a><br>
```
{% endraw %}

Za nepostojećeg izdavača `get_object_or_404()` podiže `Http404`, pa dobivamo odgovor 404 umjesto greške 500.

</details>

{: .napomena }
> Imena u URL-u su nespretna: razmaci i dijakritički znakovi kodiraju se u adresi (`/izdavaci/Zagreba%C4%8Dka%20knjiga/`), a promjena imena mijenja adresu. Zato se u praksi koriste primarni ključ (`<int:pk>`) ili `SlugField` s kratkim imenom za URL (`<slug:slug>`), npr. `/izdavaci/zagrebacka-knjiga/`.

### Knjige zadanog autora

Isti predložak možemo koristiti za više pogleda. Pogled za knjige jednog autora koristit će predložak `book_list.html`, a naslov stranice mijenjat ćemo prema tome je li predlošku poslan autor.

{: .zadatak-title }
> Zadatak 7.6 · Autori i njihove knjige
>
> 1. Napravite pogled `AuthorList` (`autori/`) za popis svih autora i predložak `author_list.html` koji za svakog autora ispisuje ime, grad i državu.
> 2. Napravite pogled `AuthorBookList` koji prikazuje sve knjige autora čiji je primarni ključ zadan u URL-u (`autori/<int:pk>/knjige/`). Iskoristite postojeći predložak `book_list.html`.
> 3. U `book_list.html` naslov neka glasi "Knjige autora …" kada je zadan autor, a inače "Knjige".
> 4. Na popisu autora i na popisu knjiga dodajte poveznice na knjige pojedinog autora.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 7.6</summary>

`main/views.py`
{: .datoteka }

``` python
from .models import Author


class AuthorList(ListView):
    model = Author


class AuthorBookList(ListView):
    template_name = "main/book_list.html"

    def get_queryset(self):
        self.author = get_object_or_404(Author, pk=self.kwargs["pk"])
        return Book.objects.filter(author=self.author).select_related("author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = self.author
        return context
```

`main/urls.py`
{: .datoteka }

``` python
path("autori/", views.AuthorList.as_view(), name="author_list"),
path("autori/<int:pk>/knjige/", views.AuthorBookList.as_view(), name="author_books"),
```

`templates/main/author_list.html`
{: .datoteka }

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block content %}
<h2>Autori</h2>
{% for author in author_list %}
    <div class="author">
        <h4>{{ author.name }}</h4>
        <p>Grad: {{ author.city|default:"-" }}</p>
        <p>Država: {{ author.country|default:"-" }}</p>
        <p><a href="{% url 'main:author_books' author.pk %}">Sve knjige autora {{ author.name }}</a></p>
    </div>
{% empty %}
    <p>Nema autora.</p>
{% endfor %}
{% endblock %}
```
{% endraw %}

U `templates/main/book_list.html` mijenjamo naslov i redak s autorom:

{% raw %}
``` django
<h2>{% if author %}Knjige autora {{ author.name }}{% else %}Knjige{% endif %}</h2>
```

``` django
<p>Autor: <a href="{% url 'main:author_books' book.author.pk %}">{{ book.author }}</a></p>
```
{% endraw %}

Pogled `BookList` ne šalje varijablu `author`, pa uvjet nije ispunjen i naslov je "Knjige".

</details>

{: .zadatak-title }
> Zadatak 7.7 · Detalji autora
>
> 1. Napravite pogled `AuthorDetail` na adresi `autori/<int:pk>/` (ime URL-a `author_detail`, kako ga koristi `get_absolute_url()`).
> 2. Napravite predložak `author_detail.html` koji prikazuje podatke o autoru i popis njegovih knjiga koristeći `author.books.all`. Datum smrti prikažite samo ako je poznat.
> 3. Ime autora na popisu autora i na stranici s detaljima knjige pretvorite u poveznicu na detalje autora.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 7.7</summary>

`main/views.py`
{: .datoteka }

``` python
class AuthorDetail(DetailView):
    model = Author
```

`main/urls.py`
{: .datoteka }

``` python
path("autori/<int:pk>/", views.AuthorDetail.as_view(), name="author_detail"),
```

`templates/main/author_detail.html`
{: .datoteka }

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block title %}{{ author.name }} | {{ block.super }}{% endblock %}

{% block content %}
<h2>{{ author.name }}</h2>
<p>Grad: {{ author.city|default:"-" }}, država: {{ author.country|default:"-" }}</p>
<p>Datum rođenja: {{ author.date_of_birth|date:"d.m.Y."|default:"nepoznat" }}</p>
{% if author.date_of_death %}
    <p>Datum smrti: {{ author.date_of_death|date:"d.m.Y." }}</p>
{% endif %}

<h3>Knjige</h3>
<ul>
    {% for book in author.books.all %}
        <li>
            <a href="{{ book.get_absolute_url }}">{{ book.title }}</a>
            ({{ book.publication_date|date:"Y." }})
        </li>
    {% empty %}
        <li>Autor nema knjiga u knjižnici.</li>
    {% endfor %}
</ul>
{% endblock %}
```
{% endraw %}

U `templates/main/author_list.html` ime autora zamijenite poveznicom:

{% raw %}
``` django
<h4><a href="{{ author.get_absolute_url }}">{{ author.name }}</a></h4>
```
{% endraw %}

U `templates/main/book_detail.html` redak s autorom zamijenite s:

{% raw %}
``` django
<p>Autor: <a href="{{ book.author.get_absolute_url }}">{{ book.author }}</a></p>
```
{% endraw %}

</details>

## Pogled `TemplateView`

Za statične stranice ne trebamo pisati klasu. Dovoljno je u `urls.py` zadati predložak:

`main/urls.py`
{: .datoteka }

``` python
from django.views.generic import TemplateView

urlpatterns = [
    # ...
    path("o-nama/", TemplateView.as_view(template_name="main/about.html"), name="about"),
]
```

{: .zadatak-title }
> Zadatak 7.8 · Stranica "O nama"
>
> 1. Stvorite predložak `about.html` s kratkim opisom knjižnice. Predložak neka nasljeđuje osnovni predložak.
> 2. Dodajte stavku "O nama" u izbornik osnovnog predloška.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 7.8</summary>

`templates/main/about.html`
{: .datoteka }

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block title %}O nama | {{ block.super }}{% endblock %}

{% block content %}
<h2>O nama</h2>
<p>Knjižnica je aplikacija za evidenciju knjiga, autora i izdavača izrađena na kolegiju Programiranje za web.</p>
{% endblock %}
```
{% endraw %}

U izbornik u `templates/base_generic.html` dodajemo:

{% raw %}
``` django
<li><a href="{% url 'main:about' %}">O nama</a></li>
```
{% endraw %}

</details>

## Kako radi generički pogled

Generički pogled je klasa čije metode Django poziva određenim redoslijedom. Za `ListView` to je pojednostavljeno:

1. `as_view()` stvara funkciju-pogled koju Django poziva za svaki zahtjev.
2. `dispatch()` prema HTTP metodi poziva `get()`, `post()` itd.
3. `get()` poziva `get_queryset()` i rezultat sprema u `self.object_list`.
4. `get_context_data()` slaže kontekst (popis, straničenje, dodatne varijable).
5. `render_to_response()` metodom `get_template_names()` određuje predložak i vraća odgovor.

Mi nadjačavamo samo korake koji nam trebaju, kao što smo učinili s `get_queryset()` i `get_context_data()`. Ovo je primjer uzorka dizajna *Template Method* (vidi [poglavlje 14](14-testiranje-i-uzorci-dizajna.md)). Izvorni kod i sve metode svakog generičkog pogleda pregledno su prikazani na stranici [Classy Class-Based Views](https://ccbv.co.uk/).

{: .upozorenje }
> Pri nadjačavanju `get_context_data()` uvijek najprije pozovite `super().get_context_data(**kwargs)`. Bez toga predložak ostaje bez popisa objekata i varijabli za straničenje.

## Šalabahter

{% raw %}
| Sintaksa | Namjena |
| -------- | ------- |
| `class X(ListView): model = M` | popis objekata, predložak `<aplikacija>/<model>_list.html` |
| `class X(DetailView): model = M` | jedan objekt prema `pk` ili `slug`, predložak `<aplikacija>/<model>_detail.html` |
| `path("...", views.X.as_view(), name="...")` | povezivanje klase s URL-om |
| `paginate_by = n` | straničenje, u predlošku `page_obj` i `is_paginated` |
| `get_queryset()` | vlastiti upit, npr. filtriranje prema `self.kwargs` |
| `get_context_data(**kwargs)` | dodatne varijable u predlošku |
| `self.kwargs["ime"]` | argument iz URL uzorka |
| `self.request.GET.get("q", "")` | parametar iz upitnog niza adrese |
| `TemplateView.as_view(template_name="...")` | statična stranica bez klase |
| `get_absolute_url()` | kanonska adresa objekta |
| `{% querystring page=2 %}` | upitni niz s promijenjenim parametrom, ostali se zadržavaju |
{% endraw %}

## Sažetak

{: .savjet-title }
> Što smo naučili
>
> - Generički pogledi su gotove klase za česte obrasce: popis, detalji, stvaranje, uređivanje i brisanje.
> - Klasu povezujemo s URL-om metodom `as_view()`, a ime predloška određuje se prema konvenciji `<aplikacija>/<model>_list.html` ili `_detail.html`.
> - Atributom `paginate_by` popis dijelimo na stranice.
> - Za filtriranje nadjačavamo `get_queryset()`, a argumente iz URL-a čitamo iz `self.kwargs`.
> - Dodatne varijable predlošku šaljemo nadjačavanjem `get_context_data()`.
> - Isti predložak može služiti za više pogleda.
> - Statične stranice prikazujemo pogledom `TemplateView` bez pisanja klase.

## Zadaci za vježbu
{: #zadaci }

{: .zadatak-title }
> Zadatak 7.9 · Straničenje autora
>
> 1. Na popisu autora prikažite 3 autora po stranici.
> 2. Navigaciju po stranicama izdvojite u zaseban predložak `_paginacija.html` i uključite ga i u popis autora i u popis knjiga.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 7.9</summary>

`main/views.py`
{: .datoteka }

``` python
class AuthorList(ListView):
    model = Author
    paginate_by = 3
```

`templates/main/_paginacija.html`
{: .datoteka }

{% raw %}
``` django
{% if is_paginated %}
<nav class="pagination">
    {% if page_obj.has_previous %}
        <a href="{% querystring page=page_obj.previous_page_number %}">&laquo; prethodna</a>
    {% endif %}
    Stranica {{ page_obj.number }} od {{ page_obj.paginator.num_pages }}
    {% if page_obj.has_next %}
        <a href="{% querystring page=page_obj.next_page_number %}">sljedeća &raquo;</a>
    {% endif %}
</nav>
{% endif %}
```
{% endraw %}

{% raw %}
Oznaka `{% querystring %}` (od Djanga 5.1) slaže upitni niz iz trenutne adrese i mijenja samo navedeni parametar. Za razliku od `?page=...`, zadržava ostale parametre, što će nam trebati u [zadatku 7.13](#zadaci).
{% endraw %}

U `templates/main/author_list.html` iza petlje, a u `templates/main/book_list.html` umjesto cijelog bloka `{% raw %}{% if is_paginated %}{% endraw %}` dodajemo:

{% raw %}
``` django
{% include "main/_paginacija.html" %}
```
{% endraw %}

Uključeni predložak vidi sve varijable konteksta, pa mu `page_obj` i `is_paginated` ne treba izričito slati.

</details>

{: .zadatak-title }
> Zadatak 7.10 · Knjige istog izdavača
>
> Na stranici s detaljima knjige dodajte poveznicu na sve knjige istog izdavača. Za knjigu bez izdavača poveznicu nemojte prikazati.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 7.10</summary>

U `templates/main/book_detail.html` iza retka s izdavačem dodajemo:

{% raw %}
``` django
{% if book.publisher %}
    <p><a href="{% url 'main:publisher_books' book.publisher.name %}">Sve knjige izdavača {{ book.publisher.name }}</a></p>
{% endif %}
```
{% endraw %}

Bez uvjeta bi za knjigu "Gospoda Glembajevi" oznaka `url` dobila praznu vrijednost i javila grešku `NoReverseMatch`, jer `<str:publisher>` ne prihvaća prazan niz.

</details>

{: .zadatak-title }
> Zadatak 7.11 · Najnovije knjige i hrvatski izdavači
>
> 1. Napravite pogled `RecentBookList` na adresi `knjige/nove/` koji prikazuje 5 najnovijih knjiga.
> 2. Napravite pogled `CroatianPublisherList` na adresi `izdavaci/hrvatski/` koji prikazuje samo izdavače iz Hrvatske.
> 3. Objasnite zašto `izdavaci/hrvatski/` mora biti u `urls.py` ispred `izdavaci/<str:publisher>/`, a za `knjige/nove/` i `knjige/<int:pk>/` redoslijed nije bitan.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 7.11</summary>

`main/views.py`
{: .datoteka }

``` python
class RecentBookList(ListView):
    template_name = "main/book_list.html"

    def get_queryset(self):
        return Book.objects.select_related("author").order_by("-publication_date")[:5]


class CroatianPublisherList(ListView):
    queryset = Publisher.objects.filter(country="Hrvatska")
```

`CroatianPublisherList` radi nad modelom `Publisher`, pa koristi zadani predložak `publisher_list.html`.

`main/urls.py`
{: .datoteka }

``` python
path("izdavaci/", views.PublisherList.as_view(), name="publisher_list"),
path("izdavaci/hrvatski/", views.CroatianPublisherList.as_view(), name="croatian_publishers"),
path("izdavaci/<str:publisher>/", views.PublisherBookList.as_view(), name="publisher_books"),
path("knjige/", views.BookList.as_view(), name="book_list"),
path("knjige/<int:pk>/", views.BookDetail.as_view(), name="book_detail"),
path("knjige/nove/", views.RecentBookList.as_view(), name="recent_books"),
```

Django isprobava uzorke redom i koristi prvi koji odgovara adresi. Pretvornik `str` prihvaća bilo koji niz bez znaka `/`, pa i `hrvatski`. Da je `izdavaci/<str:publisher>/` naveden prvi, adresa `/izdavaci/hrvatski/` završila bi u pogledu `PublisherBookList`, koji bi tražio izdavača imena "hrvatski" i vratio 404. Pretvornik `int` prihvaća samo znamenke, pa `knjige/<int:pk>/` nikad ne odgovara adresi `/knjige/nove/` i redoslijed tih dvaju uzoraka nije bitan.

Usput, izdavač koji se zaista zove "hrvatski" više ne bi imao dostupnu stranicu s knjigama. To je još jedan razlog za `pk` ili `slug` u adresi.

</details>

{: .zadatak-title }
> Zadatak 7.12 · Izdavači s najviše knjiga
>
> Na početnu stranicu dodajte popis 3 izdavača s najviše knjiga i uz svakog ispišite broj knjiga. Koristite `annotate` i `Count`.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 7.12</summary>

`main/views.py`
{: .datoteka }

``` python
from django.db.models import Count


def homepage(request):
    context = {
        "num_books": Book.objects.count(),
        "num_authors": Author.objects.count(),
        "num_publishers": Publisher.objects.count(),
        "top_publishers": Publisher.objects.annotate(num_books=Count("books"))
        .order_by("-num_books", "name")[:3],
    }
    return render(request, "main/homepage.html", context)
```

Ime `books` je `related_name` veze `Book.publisher`. Drugi kriterij poretka (`name`) određuje redoslijed izdavača s jednakim brojem knjiga.

`templates/main/homepage.html`
{: .datoteka }

{% raw %}
``` django
<h3>Izdavači s najviše knjiga</h3>
<ol>
    {% for publisher in top_publishers %}
        <li>
            <a href="{% url 'main:publisher_books' publisher.name %}">{{ publisher.name }}</a>
            ({{ publisher.num_books }})
        </li>
    {% endfor %}
</ol>
```
{% endraw %}

</details>

{: .zadatak-title }
> Zadatak 7.13 · Pretraga knjiga po naslovu
>
> 1. Iznad popisa knjiga dodajte polje za pretragu. Upisani pojam neka se šalje u adresi kao parametar `q` (`/knjige/?q=zagreb`).
> 2. Pogled `BookList` neka prikazuje samo knjige čiji naslov sadrži zadani pojam, bez obzira na velika i mala slova. Bez pojma neka prikazuje sve knjige.
> 3. Upisani pojam neka ostane u polju nakon pretrage, a straničenje neka radi i za rezultate pretrage.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 7.13</summary>

Argumenti iz URL uzorka nalaze se u `self.kwargs`, a parametri iz upitnog niza (dio adrese iza `?`) u `self.request.GET`.

`main/views.py`
{: .datoteka }

``` python
class BookList(ListView):
    model = Book
    paginate_by = 5

    def get_queryset(self):
        queryset = Book.objects.select_related("author", "publisher")
        self.q = self.request.GET.get("q", "").strip()
        if self.q:
            queryset = queryset.filter(title__icontains=self.q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.q
        return context
```

U `templates/main/book_list.html` ispod naslova dodajemo:

{% raw %}
``` django
<form method="get" action="{% url 'main:book_list' %}">
    <input type="search" name="q" value="{{ q }}" placeholder="Naslov knjige">
    <button type="submit">Traži</button>
</form>
```
{% endraw %}

{% raw %}
Atribut `action` šalje pretragu uvijek na popis svih knjiga, i kada se predložak koristi za knjige jednog autora. Ako ste u zadatku 7.9 navigaciju izdvojili u `_paginacija.html` s oznakom `{% querystring %}`, parametar `q` zadržava se pri prelasku na sljedeću stranicu bez dodatnih izmjena. S poveznicama oblika `?page=...` pretraga bi se na drugoj stranici izgubila.
{% endraw %}

{: .napomena }
> SQLite ne razlikuje velika i mala slova samo za slova engleske abecede. Pretraga `čud` zato neće pronaći naslov koji počinje s "Čud". PostgreSQL nema to ograničenje. Obrasce detaljnije obrađujemo u [poglavlju 8](08-obrasci-get-post-modelforms.md).

</details>

{: .zadatak-title }
> Zadatak 7.14 · Knjige po godini izdanja
>
> 1. Napravite pogled koji na adresi `knjige/godina/<int:godina>/` prikazuje knjige izdane zadane godine. Iskoristite predložak `book_list.html` i u naslovu ispišite godinu.
> 2. Ako te godine nije izdana nijedna knjiga, pogled neka vrati odgovor 404.

<details class="rjesenje" markdown="block">
<summary>Rješenje zadatka 7.14</summary>

`main/views.py`
{: .datoteka }

``` python
class YearBookList(ListView):
    template_name = "main/book_list.html"
    allow_empty = False

    def get_queryset(self):
        return Book.objects.filter(
            publication_date__year=self.kwargs["godina"]
        ).select_related("author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["godina"] = self.kwargs["godina"]
        return context
```

S `allow_empty = False` pogled `ListView` za prazan popis sam podiže `Http404`.

`main/urls.py`
{: .datoteka }

``` python
path("knjige/godina/<int:godina>/", views.YearBookList.as_view(), name="books_by_year"),
```

Uzorak ne smije biti `knjige/<int:godina>/`, jer bi se preklapao s `knjige/<int:pk>/`: oba prihvaćaju broj i uvijek bi odgovarao onaj prvi naveden.

U `templates/main/book_list.html` proširujemo naslov:

{% raw %}
``` django
<h2>
    {% if author %}Knjige autora {{ author.name }}
    {% elif godina %}Knjige izdane {{ godina }}. godine
    {% else %}Knjige{% endif %}
</h2>
```
{% endraw %}

Provjerite adrese `/knjige/godina/2024/` i `/knjige/godina/1990/`.

</details>

---

[← 6. Predlošci](06-predlosci-dinamicki-sadrzaj.md){: .btn .mr-2 }
[8. Obrasci →](08-obrasci-get-post-modelforms.md){: .btn .btn-primary }