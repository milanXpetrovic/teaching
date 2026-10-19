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

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Priprema i postavljanje projekta

Od ovog poglavlja do kraja kolegija gradimo novi projekt: **knjižnicu** s izdavačima, autorima i knjigama.

{: .zadatak }
> Stvorite novi Django projekt `knjiznica` i unutar njega aplikaciju `main`. Povežite projekt i aplikaciju:
> - dodajte aplikaciju `main` u `INSTALLED_APPS` u `knjiznica/settings.py`,
> - u `knjiznica/urls.py` dodajte usmjeravanje na `main/urls.py`, a zatim stvorite `main/urls.py`.

**Rješenje zadatka.**

``` shell
$ django-admin startproject knjiznica
$ cd knjiznica
$ python manage.py startapp main
```

Datoteka `knjiznica/urls.py`:

``` python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
]
```

Datoteka `main/urls.py` zasad je prazna:

``` python
from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
]
```

### Model

Datoteka `main/models.py`:

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

Metoda `get_absolute_url()` vraća kanonsku adresu objekta. Koriste je generički pogledi, administratorsko sučelje (gumb *View on site*) i predlošci.

Nakon što je model stvoren, potrebno je provesti migraciju:

``` shell
$ python manage.py makemigrations
$ python manage.py migrate
```

Registrirajte modele u `main/admin.py`:

``` python
from django.contrib import admin

from .models import Author, Book, Publisher

admin.site.register([Author, Book, Publisher])
```

### Predlošci na razini projekta

U ovom projektu sve predloške držimo u zajedničkom direktoriju `templates` u korijenskom direktoriju projekta. Unutar njega stvorite `templates/main/` za predloške aplikacije. U `settings.py` pod `TEMPLATES` postavite:

``` python
"DIRS": [BASE_DIR / "templates"],
```

Oba pristupa (predlošci u aplikaciji kao u [poglavlju 6](06-predlosci-dinamicki-sadrzaj.md) ili u zajedničkom direktoriju) su ispravna. Zajednički direktorij je praktičan kada su sve aplikacije dio istog projekta.

Osnovni predložak `templates/base_generic.html`:

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
    <div id="sidebar">
        {% block sidebar %}
        <ul>
            <li><a href="{% url 'main:homepage' %}">Početna</a></li>
            <li><a href="{% url 'main:book_list' %}">Knjige</a></li>
            <li><a href="{% url 'main:author_list' %}">Autori</a></li>
            <li><a href="{% url 'main:publisher_list' %}">Izdavači</a></li>
        </ul>
        {% endblock %}
    </div>

    <div class="content">
        {% block content %}
        {% endblock %}
    </div>
</body>
</html>
```
{% endraw %}

{: .upozorenje }
> Oznaka `url` javlja grešku `NoReverseMatch` ako URL zadanog imena ne postoji. Stavke izbornika za knjige, autore i izdavače zato dodajte tek kada u nastavku poglavlja napravite odgovarajuće poglede. HTML komentar `<!-- -->` tu ne pomaže jer Django oznake unutar njega i dalje izvršava.

Početna stranica kao obična funkcija u `main/views.py`:

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

Datoteka `templates/main/homepage.html`:

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block content %}
<h2>Dobro došli</h2>
<p>U knjižnici je {{ num_books }} knjiga od {{ num_authors }} autora i {{ num_publishers }} izdavača.</p>
{% endblock %}
```
{% endraw %}

{: .zadatak }
> Stvorite administratora i kroz administratorsko sučelje dodajte 3 izdavača, 3 autora i barem 6 knjiga. Sve vrijednosti zadajte proizvoljno. (U [poglavlju 9](09-testni-podaci-i-sijanje.md) naučit ćemo podatke generirati automatski.)

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

Stvorimo prvi generički pogled nad modelom. U datoteku `main/views.py` dodajemo:

``` python
from django.views.generic import ListView

from .models import Publisher


class PublisherList(ListView):
    model = Publisher
```

A zatim ga povežite u `main/urls.py`. Klasu pretvaramo u pogled metodom `as_view()`:

``` python
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("izdavaci/", views.PublisherList.as_view(), name="publisher_list"),
]
```

Kada smo stvorili pogled i povezali ga u `urls.py`, potreban nam je predložak u kojem će se prikazati odgovor. `ListView` sam određuje ime predloška prema konvenciji `<aplikacija>/<model>_list.html`, dakle `main/publisher_list.html`.

Datoteka `templates/main/publisher_list.html`:

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block content %}
    <h2>Izdavači</h2>
    <ul>
        {% for publisher in object_list %}
            <li>
                <a href="{% url 'main:publisher_books' publisher.name %}">{{ publisher.name }}</a><br>
                Grad: {{ publisher.city }}
            </li>
        {% empty %}
            <li>Nema izdavača.</li>
        {% endfor %}
    </ul>
{% endblock %}
```
{% endraw %}

Poveznica na knjige izdavača (`main:publisher_books`) proradit će kada u nastavku dodamo taj pogled. Do tada privremeno uklonite oznaku `<a>` ili će stranica javiti grešku `NoReverseMatch`.

`ListView` predlošku šalje popis objekata pod dva imena: `object_list` i `<model>_list` (ovdje `publisher_list`). Drugo ime je čitljivije pa ćemo ga koristiti u nastavku.

{: .zadatak }
> Provjerite ispis izdavača na adresi `http://127.0.0.1:8000/izdavaci/`.

### Najčešći atributi

| Atribut | Značenje | Primjer |
| ------- | -------- | ------- |
| `model` | model čiji se objekti prikazuju | `model = Book` |
| `queryset` | upit umjesto `model.objects.all()` | `queryset = Book.objects.select_related("author")` |
| `template_name` | predložak umjesto zadanog | `template_name = "main/knjige.html"` |
| `context_object_name` | ime popisa u predlošku | `context_object_name = "knjige"` |
| `ordering` | poredak | `ordering = ["title"]` |
| `paginate_by` | broj objekata po stranici | `paginate_by = 10` |

### Popis knjiga sa straničenjem

``` python
class BookList(ListView):
    model = Book
    paginate_by = 5
    queryset = Book.objects.select_related("author", "publisher")
```

``` python
path("knjige/", views.BookList.as_view(), name="book_list"),
```

Kada je postavljen `paginate_by`, predložak dobiva i varijable `page_obj` i `is_paginated`. Datoteka `templates/main/book_list.html`:

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block content %}
<h2>{% if author %}Knjige autora {{ author.name }}{% else %}Knjige{% endif %}</h2>

{% for book in book_list %}
    <div class="book">
        <h4><a href="{{ book.get_absolute_url }}">{{ book.title }}</a></h4>
        <p>Autor: <a href="{% url 'main:author_books' book.author.pk %}">{{ book.author }}</a></p>
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

Poveznica `main:author_books` definirana je u nastavku poglavlja.

## Pogled `DetailView`

`DetailView` prikazuje jedan objekt. Objekt pronalazi prema argumentu `pk` (ili `slug`) iz URL-a, a ako objekt ne postoji, sam vraća 404.

``` python
from django.views.generic import DetailView


class BookDetail(DetailView):
    model = Book
```

``` python
path("knjige/<int:pk>/", views.BookDetail.as_view(), name="book_detail"),
```

Predložak se po konvenciji zove `main/book_detail.html`, a objekt je dostupan kao `object` i `book`. Datoteka `templates/main/book_detail.html`:

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block title %}{{ book.title }} | {{ block.super }}{% endblock %}

{% block content %}
<h2>{{ book.title }}</h2>
<p>Autor: <a href="{{ book.author.get_absolute_url }}">{{ book.author }}</a></p>
<p>Izdavač: {{ book.publisher|default:"nepoznat" }}</p>
<p>Datum izdanja: {{ book.publication_date|date:"d.m.Y." }}</p>
{{ book.abstract|linebreaks }}
{% endblock %}
```
{% endraw %}

## Dinamičko filtriranje

U nastavku je prikazan način na koji se omogućava dinamička pretraga pomoću URL-a. Za zadani naziv izdavača vraćat će se sve knjige koje je taj izdavač objavio. Naziv izdavača neće biti statično zapisan u URL uzorku, nego će se uzimati iz adrese.

Za početak potrebno je definirati pogled u `main/views.py` koji vraća sve knjige zadanog izdavača. Umjesto atributa `model` nadjačavamo metodu `get_queryset()`:

``` python
from django.shortcuts import get_object_or_404


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

Argumenti iz URL-a dostupni su u rječniku `self.kwargs`. Metodom `get_context_data()` predlošku šaljemo i samog izdavača, kako bismo mogli ispisati njegovo ime.

Zatim u `main/urls.py` povezujemo pogled. Umjesto da svakog izdavača zadajemo pojedinačno, koristimo `<str:publisher>`:

``` python
path("izdavaci/<str:publisher>/", views.PublisherBookList.as_view(), name="publisher_books"),
```

{: .zadatak }
> Stvorite `books_by_publisher.html` unutar `templates/main` koji ispisuje ime izdavača i naslove svih knjiga tog izdavača.

**Rješenje zadatka.**

{% raw %}
``` django
{% extends "base_generic.html" %}

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

Pokrenite poslužitelj i provjerite pretraživanje po izdavaču. Što se dogodi za nepostojećeg izdavača?

{: .napomena }
> Imena u URL-u su nespretna: razmaci, dijakritički znakovi i promjena imena mijenjaju adresu. Zato se u praksi koriste primarni ključ (`<int:pk>`) ili `SlugField` s kratkim imenom za URL (`<slug:slug>`), npr. `/izdavaci/skolska-knjiga/`.

### Knjige zadanog autora

{: .zadatak }
> - Napravite pogled `AuthorList` za popis svih autora i predložak `author_list.html`.
> - Napravite pogled `AuthorBookList` koji prikazuje sve knjige autora čiji je primarni ključ zadan u URL-u (`autori/<int:pk>/knjige/`). Iskoristite postojeći predložak `book_list.html`.
> - Ime svakog autora na popisu pretvorite u poveznicu na njegove knjige.

**Rješenje zadatka.** U datoteci `main/views.py`:

``` python
class AuthorList(ListView):
    model = Author


class AuthorDetail(DetailView):
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

U datoteci `main/urls.py`:

``` python
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("izdavaci/", views.PublisherList.as_view(), name="publisher_list"),
    path("izdavaci/<str:publisher>/", views.PublisherBookList.as_view(), name="publisher_books"),
    path("knjige/", views.BookList.as_view(), name="book_list"),
    path("knjige/<int:pk>/", views.BookDetail.as_view(), name="book_detail"),
    path("autori/", views.AuthorList.as_view(), name="author_list"),
    path("autori/<int:pk>/", views.AuthorDetail.as_view(), name="author_detail"),
    path("autori/<int:pk>/knjige/", views.AuthorBookList.as_view(), name="author_books"),
]
```

Datoteka `templates/main/author_list.html`:

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block content %}
<h2>Autori</h2>
{% for author in author_list %}
    <div class="author">
        <h4><a href="{{ author.get_absolute_url }}">{{ author.name }}</a></h4>
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

Predložak `book_list.html` od ranije već provjerava postoji li varijabla `author` i prema tome mijenja naslov.

{: .zadatak }
> Napravite predložak `author_detail.html` koji prikazuje podatke o autoru i popis njegovih knjiga koristeći `author.books.all`.

## Pogled `TemplateView`

Za statične stranice ne trebamo pisati klasu. Dovoljno je u `urls.py` zadati predložak:

``` python
from django.views.generic import TemplateView

urlpatterns = [
    # ...
    path("o-nama/", TemplateView.as_view(template_name="main/about.html"), name="about"),
]
```

## Kako radi generički pogled

Generički pogled je klasa čije metode Django poziva određenim redoslijedom. Za `ListView` to je pojednostavljeno:

1. `as_view()` stvara funkciju-pogled koju Django poziva za svaki zahtjev.
2. `dispatch()` prema HTTP metodi poziva `get()`, `post()` itd.
3. `get()` poziva `get_queryset()` kako bi dohvatio objekte.
4. `get_context_data()` slaže kontekst (popis, straničenje, dodatne varijable).
5. `get_template_names()` određuje predložak.
6. `render_to_response()` vraća odgovor.

Mi nadjačavamo samo korake koji nam trebaju, kao što smo učinili s `get_queryset()` i `get_context_data()`. Ovo je primjer uzorka dizajna *Template Method* (vidi [poglavlje 14](14-testiranje-i-uzorci-dizajna.md)). Izvorni kod i sve metode svakog generičkog pogleda pregledno su prikazani na stranici [Classy Class-Based Views](https://ccbv.co.uk/).

## Zadaci za vježbu

{: .zadatak }
> - Dodajte straničenje i na popis autora (3 autora po stranici).
> - Na stranici s detaljima knjige dodajte poveznicu na ostale knjige istog izdavača.
> - Napravite pogled `RecentBookList` na putanji `knjige/nove/` koji prikazuje 5 najnovijih knjiga, i pogled na putanji `izdavaci/hrvatski/` koji prikazuje samo izdavače iz Hrvatske. Objasnite zašto `izdavaci/hrvatski/` mora biti u `urls.py` ispred `izdavaci/<str:publisher>/`, a za `knjige/nove/` i `knjige/<int:pk>/` redoslijed nije bitan.
> - Na početnu stranicu dodajte popis 3 izdavača s najviše knjiga (koristite `annotate` i `Count`).