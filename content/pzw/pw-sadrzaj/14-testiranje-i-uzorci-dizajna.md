---
author: Milan Petrović
title: "14. Testiranje Django aplikacija i primjena uzoraka dizajna"
layout: default
parent: PZW
nav_order: 14
has_children: false
has_toc: true
nav_exclude: true
---

# Testiranje Django aplikacija i primjena uzoraka dizajna
{: .no_toc }

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Vrste testova

Ovaj dio je djelomično sastavljen prema [Django tutorialu s MDN-a](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Testing).

**Test jedinke** (engl. *unit test*) najbrži je za izvođenje i testira dio koda neovisno o drugim dijelovima.

``` python
def zbroji(prvi, drugi):
    return prvi + drugi


def test_zbroji():
    assert zbroji(3, 6) == 9
```

**Test integracije** testira više dijelova zajedno kako bi se osiguralo da međusobno ispravno surađuju, npr. pogled, model i predložak.

**Funkcijski test** provjerava funkcionalnost iz perspektive krajnjeg korisnika, npr. upravljanjem preglednikom pomoću alata Selenium ili Playwright. Najsporiji je za izvođenje.

**Regresijski test** reproducira grešku koja se prethodno dogodila u kodu. Najprije se pokreće kako bi se provjerilo da je greška ispravljena, a zatim stalno, kako bi se osiguralo da se nakon kasnijih promjena koda greška ne vrati.

Zašto pisati testove? Testovi nam daju sigurnost da promjena na jednom mjestu nije pokvarila nešto na drugom. Kod koji ima testove možemo mijenjati i poboljšavati bez straha, a testovi ujedno dokumentiraju kako se kod treba ponašati.

## Testiranje u Djangu

Django testove piše pomoću Pythonovog modula `unittest`, uz vlastite klase za testiranje:

| Klasa | Kada je koristiti |
| ----- | ----------------- |
| `SimpleTestCase` | testovi koji ne koriste bazu podataka (URL-ovi, pomoćne funkcije) |
| [`TestCase`](https://docs.djangoproject.com/en/6.1/topics/testing/tools/#testcase) | najčešće korištena klasa: svaki test se izvodi u transakciji koja se na kraju poništava |
| `TransactionTestCase` | testovi koji ispituju samo ponašanje transakcija |
| `LiveServerTestCase` | funkcijski testovi s pravim poslužiteljem (npr. uz Selenium) |

Pri pokretanju testova Django stvara **zasebnu, praznu testnu bazu**, primjenjuje sve migracije, izvodi testove i na kraju bazu briše. Vaši razvojni podaci nikad nisu dirnuti, ali to znači i da testovi ne vide podatke iz razvojne baze. Sve što test treba, mora sam stvoriti.

### Organizacija testova

Nastavljamo s projektom `knjiznica`. Umjesto jedne datoteke `main/tests.py` testove organiziramo u paket:

``` text
main/
└── tests/
    ├── __init__.py
    ├── test_forms.py
    ├── test_models.py
    ├── test_urls.py
    └── test_views.py
```

{: .upozorenje }
> Obrišite datoteku `main/tests.py`. Ako postoje i datoteka `tests.py` i direktorij `tests/`, Python ne zna koji je modul `main.tests` i testovi se ne pokreću. Svaka datoteka s testovima mora počinjati s `test`.

{: .zadatak }
> Unutar aplikacije `main` stvorite direktorij `tests` s praznom datotekom `__init__.py` i datotekama za testiranje URL-ova, pogleda, modela i obrazaca.

### Pokretanje testova

``` shell
$ python manage.py test                                  # svi testovi projekta
$ python manage.py test main.tests                       # testovi aplikacije main
$ python manage.py test main.tests.test_views            # jedna datoteka
$ python manage.py test main.tests.test_views.TestViews.test_homepage_GET   # jedan test
$ python manage.py test -v 2                             # opširniji ispis
$ python manage.py test --keepdb                         # testna baza se ne briše (brže ponovno pokretanje)
```

## Testiranje `urls.py`

Testovi URL-ova provjeravaju da ime URL-a daje očekivanu adresu i da ta adresa poziva očekivani pogled. Ne koriste bazu, pa nasljeđuju `SimpleTestCase`. Datoteka `main/tests/test_urls.py`:

``` python
from django.test import SimpleTestCase
from django.urls import resolve, reverse

from main.views import AuthorBookList, AuthorList, BookList, homepage


class TestUrls(SimpleTestCase):

    def test_homepage_url_is_resolved(self):
        url = reverse("main:homepage")
        self.assertEqual(resolve(url).func, homepage)

    def test_books_url_is_resolved(self):
        url = reverse("main:book_list")
        self.assertEqual(resolve(url).func.view_class, BookList)

    def test_authors_url_is_resolved(self):
        url = reverse("main:author_list")
        self.assertEqual(resolve(url).func.view_class, AuthorList)

    def test_author_books_url_is_resolved(self):
        url = reverse("main:author_books", args=[1])
        self.assertEqual(resolve(url).func.view_class, AuthorBookList)
```

Funkcijski pogled uspoređujemo preko `resolve(url).func`, a generički preko `resolve(url).func.view_class`, jer `as_view()` vraća funkciju koja omata klasu.

{: .napomena }
> Svaka metoda testa mora imati **jedinstveno ime**. Ako dvije metode u istoj klasi imaju isto ime, druga tiho zamjenjuje prvu i prvi test se nikad ne izvodi. Koristite `assertEqual` (bez "s" na kraju). Stari naziv `assertEquals` uklonjen je u Pythonu 3.12.

## Testiranje `views.py`

Testovi pogleda koriste **testnog klijenta** (`self.client`), koji šalje zahtjeve aplikaciji bez pravog poslužitelja i preglednika. Klasa `TestCase` ga sama stvara za svaki test. Datoteka `main/tests/test_views.py`:

``` python
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from main.models import Author, Book


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(
            name="some-author",
            address="TestAddress",
            city="TestCity",
            country="TestCountry",
        )
        cls.book = Book.objects.create(
            title="Test Book", author=cls.author, publication_date="2020-01-01"
        )

    def test_homepage_GET(self):
        response = self.client.get(reverse("main:homepage"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/homepage.html")
        self.assertTemplateUsed(response, "base_generic.html")

    def test_author_books_GET(self):
        response = self.client.get(reverse("main:author_books", args=[self.author.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/book_list.html")
        self.assertContains(response, "Test Book")

    def test_author_books_unknown_author_returns_404(self):
        response = self.client.get(reverse("main:author_books", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_book_create_requires_login(self):
        url = reverse("main:book_create")
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_book_create_POST(self):
        user = User.objects.create_user("ana", password="tajna-lozinka-123")
        self.client.force_login(user)

        response = self.client.post(reverse("main:book_create"), {
            "title": "Nova knjiga",
            "abstract": "Kratki sažetak.",
            "author": self.author.pk,
            "publication_date": "2021-05-05",
        })

        book = Book.objects.get(title="Nova knjiga")
        self.assertRedirects(response, book.get_absolute_url())
        self.assertEqual(book.added_by, user)
```

- `setUpTestData()` se izvodi **jednom** za cijelu klasu, a `setUp()` prije **svakog** testa. Podatke koje testovi samo čitaju stvarajte u `setUpTestData()` jer je brže.
- `force_login()` prijavljuje korisnika bez provjere lozinke.
- Zadnja dva testa pretpostavljaju zaštitu i polje `added_by` iz [poglavlja 12](12-autentifikacija-autorizacija.md).

Najčešće korištene provjere:

| Metoda | Provjerava |
| ------ | ---------- |
| `assertEqual(a, b)`, `assertTrue(x)`, `assertIn(a, b)` | osnovne usporedbe |
| `assertContains(response, tekst)` | odgovor ima status 200 i sadrži tekst |
| `assertNotContains(response, tekst)` | odgovor ne sadrži tekst |
| `assertTemplateUsed(response, ime)` | korišten je predložak |
| `assertRedirects(response, url)` | odgovor preusmjerava na adresu |
| `assertRaises(Iznimka)` | kod podiže iznimku |
| `assertNumQueries(n)` | blok koda izvodi točno *n* SQL upita |

Odgovor testnog klijenta ima i atribut `response.context` s kontekstom predloška, npr. `response.context["book_list"]`.

## Testiranje `models.py`

Datoteka `main/tests/test_models.py`:

``` python
from django.test import TestCase

from main.models import Author, Book


class TestModels(TestCase):

    def setUp(self):
        self.author1 = Author.objects.create(
            name="some-author",
            address="TestAddress",
            city="TestCity",
            country="TestCountry",
        )

    def test_author_str(self):
        self.assertEqual(str(self.author1), "some-author")

    def test_author_get_absolute_url(self):
        self.assertEqual(self.author1.get_absolute_url(), f"/autori/{self.author1.pk}/")

    def test_books_ordered_newest_first(self):
        old = Book.objects.create(title="Stara", author=self.author1, publication_date="1990-01-01")
        new = Book.objects.create(title="Nova", author=self.author1, publication_date="2020-01-01")
        self.assertEqual(list(Book.objects.all()), [new, old])
```

## Testiranje obrazaca

Datoteka `main/tests/test_forms.py`:

``` python
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from main.forms import BookForm
from main.models import Author


class TestBookForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(name="Autor")

    def test_valid_data(self):
        form = BookForm(data={
            "title": "Naslov",
            "author": self.author.pk,
            "publication_date": "2020-01-01",
        })
        self.assertTrue(form.is_valid())

    def test_future_publication_date_is_invalid(self):
        future = timezone.localdate() + timedelta(days=1)
        form = BookForm(data={
            "title": "Naslov",
            "author": self.author.pk,
            "publication_date": future.isoformat(),
        })
        self.assertFalse(form.is_valid())
        self.assertIn("publication_date", form.errors)
```

## Podaci za testove

### Fixture

Testovi mogu učitati podatke iz fixtureova iz [poglavlja 9](09-testni-podaci-i-sijanje.md#fixture-izvoz-i-uvoz-podataka). Datoteku spremite kao `main/fixtures/0001_author.json` i navedite je u atributu `fixtures`:

``` python
from django.test import TestCase

from main.models import Author


class FixtureTest(TestCase):
    fixtures = ["0001_author.json"]

    def test_author_from_fixture(self):
        author = Author.objects.get(pk=1)
        self.assertEqual(author.name, "Ivana Horvat")
```

Bez atributa `fixtures` ovaj test bi pao s greškom `Author.DoesNotExist`, jer je testna baza prazna i ne sadrži podatke iz razvojne baze.

### factory_boy

Tvornice iz [poglavlja 9](09-testni-podaci-i-sijanje.md) su često praktičnije od fixtureova. Stvaraju samo podatke koje test treba i ne lome se kada se model promijeni:

``` python
from django.test import TestCase
from django.urls import reverse

from main.factories import BookFactory


class TestPagination(TestCase):

    def test_book_list_is_paginated(self):
        BookFactory.create_batch(12)

        response = self.client.get(reverse("main:book_list"))

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["book_list"]), 5)
```

## Testiranje REST API-ja

DRF nudi klasu `APITestCase` s klijentom koji šalje i prima JSON. Datoteka `api/tests.py`:

``` python
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from main.factories import AuthorFactory, BookFactory


class TestBookApi(APITestCase):

    def test_list_is_public(self):
        BookFactory.create_batch(3)
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)

    def test_create_requires_authentication(self):
        author = AuthorFactory()
        data = {"title": "API knjiga", "author": author.pk, "publication_date": "2020-01-01"}
        response = self.client.post("/api/books/", data, format="json")
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        self.client.force_authenticate(User.objects.create_user("api-korisnik"))
        response = self.client.post("/api/books/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

## Pokrivenost koda

Alat `coverage` mjeri koji su redci koda izvršeni tijekom testova:

``` shell
$ python -m pip install coverage
$ coverage run manage.py test
$ coverage report
$ coverage html          # izvještaj u direktoriju htmlcov/, otvorite htmlcov/index.html
```

Visoka pokrivenost ne znači da je kod bez grešaka, ali neizvršeni redci su sigurno netestirani. Izvještaj je koristan za pronalazak dijelova koje ste zaboravili testirati.

{: .napomena }
> Popularna alternativa ugrađenom pokretaču testova je `pytest` s dodatkom `pytest-django`, koji omogućuje kraće testove s običnim `assert` naredbama.

## Uzorci dizajna u Djangu

**Uzorak dizajna** (engl. *design pattern*) je provjereno, imenovano rješenje problema koji se često ponavlja u oblikovanju programa. Django je izgrađen na nizu poznatih uzoraka. Prepoznati ih pomaže razumjeti zašto je okvir organiziran baš ovako i kako ga ispravno proširiti.

| Uzorak | Gdje se pojavljuje u Djangu |
| ------ | --------------------------- |
| Model-View-Controller | arhitektura model-template-view ([poglavlje 3](03-arhitektura-url-pogledi.md)) |
| Front Controller | jedna ulazna točka (WSGI/ASGI) i usmjerivač URL-ova koji zahtjev predaje pogledu |
| Active Record | objekt modela zna se sam spremiti i obrisati: `book.save()`, `book.delete()` |
| Template Method | generički pogledi: okvir određuje redoslijed koraka, a mi nadjačavamo `get_queryset()` i sl. |
| Mixin | `LoginRequiredMixin`, `SuccessMessageMixin`: funkcionalnost se dodaje višestrukim nasljeđivanjem |
| Decorator | `@login_required`, `@require_GET`: omataju funkciju dodatnim ponašanjem |
| Chain of Responsibility | middleware: svaki sloj obradi zahtjev i preda ga sljedećem |
| Observer | signali: `post_save`, `post_delete`... |
| Strategy | zamjenjivi pozadinski sustavi: e-pošta, pohrana datoteka, autentifikacija, predmemorija |
| Factory | `as_view()` stvara funkcije-poglede, factory_boy stvara testne objekte |

U nastavku je nekoliko uzoraka koje ćete i sami primjenjivati.

### Vlastiti QuerySet i Manager

Upite koji se ponavljaju ne pišemo u svakom pogledu, nego ih stavljamo u vlastitu klasu `QuerySet`. Takav sloj za dohvat podataka sličan je uzorku Repository. U `main/models.py`:

``` python
class BookQuerySet(models.QuerySet):
    def with_related(self):
        return self.select_related("author", "publisher")

    def published_after(self, year):
        return self.filter(publication_date__year__gt=year)

    def search(self, q):
        return self.filter(models.Q(title__icontains=q) | models.Q(author__name__icontains=q))


class Book(models.Model):
    # ... polja ...

    objects = BookQuerySet.as_manager()
```

Metode se mogu ulančavati, a pogledi postaju kraći i čitljiviji:

``` python
Book.objects.with_related().published_after(2000).search("rat")
```

### Debeli modeli, tanki pogledi

Poslovna pravila (npr. "knjiga je novo izdanje ako je izdana u zadnjih godinu dana") pripadaju modelu, a ne pogledu ni predlošku. Tako ih koriste svi pogledi, API i administratorsko sučelje, a lako ih je testirati:

``` python
class Book(models.Model):
    # ...

    @property
    def is_new(self):
        return self.publication_date >= timezone.localdate() - timedelta(days=365)
```

{% raw %}
U predlošku: `{% if book.is_new %}<span>Novo!</span>{% endif %}`. Za radnje koje uključuju više modela (npr. posudba knjige koja mijenja stanje knjige i stvara zapis o posudbi) često se koristi zasebna datoteka `services.py` s funkcijama poslovne logike.
{% endraw %}

### Middleware (Chain of Responsibility)

Vlastiti middleware je klasa koja prima sljedeći sloj u lancu (`get_response`) i poziva ga. Primjer koji mjeri trajanje obrade zahtjeva, u datoteci `main/middleware.py`:

``` python
import time


class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)       # predaja sljedećem sloju
        trajanje_ms = (time.perf_counter() - start) * 1000
        response["X-Response-Time-ms"] = f"{trajanje_ms:.1f}"
        return response
```

``` python
MIDDLEWARE = [
    # ...
    "main.middleware.TimingMiddleware",
]
```

### Signali (Observer)

Signali omogućuju da se kod izvrši kada se nešto dogodi, a da pošiljatelj ne zna tko sluša. Datoteka `main/signals.py`:

``` python
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Book

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Book)
def log_new_book(sender, instance, created, **kwargs):
    if created:
        logger.info("Dodana knjiga: %s", instance.title)
```

Signale treba učitati pri pokretanju aplikacije, u `main/apps.py`:

``` python
from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"

    def ready(self):
        from . import signals  # noqa: F401
```

{: .upozorenje }
> Signali skrivaju tijek programa: iz koda koji sprema knjigu ne vidi se da se izvršava još nešto. Koristite ih za povezivanje s tuđim aplikacijama ili za sporedne radnje (zapisivanje, čišćenje datoteka). Vlastitu logiku je bolje pozvati izravno.

## Zadaci za vježbu

{: .zadatak }
> - Napišite testove za `PublisherBookList`: postojeći izdavač vraća samo njegove knjige, a nepostojeći izdavač vraća 404.
> - Napišite test koji provjerava da korisnik bez ovlasti ne može urediti tuđu knjigu (odgovor 404) i da je knjižničar može urediti.
> - Napišite test za pretragu knjiga (`?q=`) koji koristi factory_boy.
> - Uvedite `BookQuerySet` iz ovog poglavlja, prepravite `BookList` da ga koristi i napišite testove za njegove metode. Provjerite da prethodni testovi i dalje prolaze.
> - Pomoću `assertNumQueries` provjerite da popis knjiga izvodi isti broj upita bez obzira na broj knjiga.
> - Pokrenite `coverage` i dopišite testove za barem dva dijela koda koja nisu pokrivena.