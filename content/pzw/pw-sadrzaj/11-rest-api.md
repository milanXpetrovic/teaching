---
author: Milan Petrović
title: "11. Razvoj REST API-ja pomoću Django REST frameworka"
layout: default
parent: PZW
nav_order: 11
has_children: false
has_toc: false
nav_exclude: false
---

# Razvoj REST API-ja pomoću Django REST frameworka
{: .no_toc }

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Što je REST API

Do sada je naša aplikacija vraćala HTML namijenjen ljudima u pregledniku. Mobilne aplikacije, JavaScript sučelja (React, Vue...) i drugi sustavi trebaju podatke u strojno čitljivom obliku, najčešće JSON-u. Sučelje preko kojeg ih dobivaju zove se **API** (engl. *Application Programming Interface*).

**REST** (engl. *Representational State Transfer*) je stil oblikovanja API-ja nad HTTP-om s nekoliko načela:

- Podaci su organizirani kao **resursi** s vlastitim adresama: `/api/books/` je kolekcija knjiga, `/api/books/7/` jedna knjiga.
- **HTTP metoda** određuje radnju nad resursom.
- **Statusni kod** govori kako je zahtjev završio.
- Poslužitelj ne pamti stanje klijenta između zahtjeva (engl. *stateless*): svaki zahtjev nosi sve potrebno, uključujući podatke za autentifikaciju.

| Metoda | Adresa | Radnja | Uspješan odgovor |
| ------ | ------ | ------ | ---------------- |
| `GET` | `/api/books/` | popis knjiga | `200 OK` |
| `POST` | `/api/books/` | stvaranje knjige | `201 Created` |
| `GET` | `/api/books/7/` | detalji knjige | `200 OK` |
| `PUT` | `/api/books/7/` | zamjena svih podataka knjige | `200 OK` |
| `PATCH` | `/api/books/7/` | izmjena dijela podataka | `200 OK` |
| `DELETE` | `/api/books/7/` | brisanje knjige | `204 No Content` |

Česti kodovi greške su `400 Bad Request` (neispravni podaci), `401 Unauthorized` (niste prijavljeni), `403 Forbidden` (nemate ovlast) i `404 Not Found`.

## API bez dodatnih paketa

Jednostavan API možemo napraviti i samim Djangom pomoću `JsonResponse`:

``` python
from django.http import JsonResponse

from main.models import Book


def api_books(request):
    books = Book.objects.select_related("author").values("id", "title", "author__name")
    return JsonResponse({"results": list(books)})
```

Za čitanje je to dovoljno, ali za pravi API trebali bismo ručno pisati provjeru ulaznih podataka, pretvorbu u model i natrag, autentifikaciju, ovlasti, straničenje i dokumentaciju. Sve to nudi **Django REST framework** (DRF).

## Instalacija i postavljanje

Nastavljamo s projektom `knjiznica`. API ćemo smjestiti u zasebnu aplikaciju `api`, a ona će koristiti modele iz aplikacije `main`.

``` shell
$ python -m pip install djangorestframework
$ python manage.py startapp api
```

DRF 3.18 podržava Django 5.2, 6.0 i 6.1. U `settings.py`:

``` python
INSTALLED_APPS = [
    # ...
    "rest_framework",
    "main",
    "api",
]
```

## Serializatori

**Serializator** pretvara objekte modela u Python rječnike (a zatim u JSON) i obrnuto: iz primljenog JSON-a provjerava podatke i stvara ili mijenja objekte. Ulogom je sličan `ModelForm` obrascu iz [poglavlja 8](08-obrasci-get-post-modelforms.md).

Datoteka `api/serializers.py`:

``` python
from django.utils import timezone
from rest_framework import serializers

from main.models import Author, Book, Publisher


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["id", "name", "city", "country", "website"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "city", "country", "date_of_birth", "date_of_death"]


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "abstract", "author", "author_name", "publisher", "publication_date"]

    def validate_publication_date(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError("Datum izdanja ne može biti u budućnosti.")
        return value
```

Polje `author` serijalizira se kao primarni ključ autora, a dodatno polje `author_name` samo za čitanje prikazuje i ime. Metoda `validate_<polje>()` odgovara metodi `clean_<polje>()` u obrascima.

Isprobajmo serializator u ljusci:

``` python
>>> from api.serializers import BookSerializer
>>> from main.models import Book
>>> s = BookSerializer(Book.objects.first())
>>> s.data
{'id': 1, 'title': '...', 'abstract': '...', 'author': 3, 'author_name': '...', 'publisher': 2, 'publication_date': '2011-05-03'}
>>> BookSerializer(Book.objects.all()[:3], many=True).data   # više objekata
```

I u drugom smjeru, iz podataka u objekt:

``` python
>>> s = BookSerializer(data={"title": "Nova knjiga", "author": 1, "publication_date": "2100-01-01"})
>>> s.is_valid()
False
>>> s.errors
{'publication_date': [ErrorDetail(string='Datum izdanja ne može biti u budućnosti.', code='invalid')]}
>>> s = BookSerializer(data={"title": "Nova knjiga", "author": 1, "publication_date": "2020-01-01"})
>>> s.is_valid()
True
>>> s.save()
<Book: Nova knjiga>
```

## Pogledi za API

DRF nudi više razina apstrakcije, od funkcija do potpuno automatskih skupova pogleda. Pogledat ćemo sve tri, a u projektu koristiti posljednju.

### Funkcijski pogled s dekoratorom `@api_view`

``` python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from main.models import Book

from .serializers import BookSerializer


@api_view(["GET", "POST"])
def book_list(request):
    if request.method == "GET":
        books = Book.objects.select_related("author")
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    serializer = BookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)   # neispravni podaci: odgovor 400
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
```

`request.data` sadrži tijelo zahtjeva bez obzira je li poslano kao JSON ili obrazac, a `Response` sam odabire format odgovora.

### Generički pogledi

Isto kao generički pogledi u [poglavlju 7](07-genericki-pogledi.md), samo za API:

``` python
from rest_framework import generics


class BookListCreate(generics.ListCreateAPIView):
    queryset = Book.objects.select_related("author")
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.select_related("author")
    serializer_class = BookSerializer
```

``` python
path("books/", views.BookListCreate.as_view()),
path("books/<int:pk>/", views.BookDetail.as_view()),
```

### Skupovi pogleda (ViewSets) i usmjerivači

`ModelViewSet` u jednoj klasi objedinjuje sve radnje (popis, stvaranje, detalji, izmjena, brisanje), a **usmjerivač** (engl. *router*) sam stvara URL-ove. Datoteka `api/views.py`:

``` python
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import Author, Book, Publisher

from .serializers import AuthorSerializer, BookSerializer, PublisherSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @action(detail=True)
    def books(self, request, pk=None):
        """Sve knjige zadanog autora: /api/authors/<pk>/books/"""
        author = self.get_object()
        serializer = BookSerializer(author.books.all(), many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("author", "publisher")
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "author__name"]
    ordering_fields = ["title", "publication_date"]
```

Datoteka `api/urls.py`:

``` python
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("publishers", views.PublisherViewSet)
router.register("authors", views.AuthorViewSet)
router.register("books", views.BookViewSet)

urlpatterns = router.urls
```

U `knjiznica/urls.py` dodajemo:

``` python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),  # prijava za preglednik API-ja
    path("", include("main.urls")),
]
```

Usmjerivač je stvorio sljedeće adrese:

| Adresa | Metode |
| ------ | ------ |
| `/api/` | `GET`: popis svih resursa |
| `/api/books/` | `GET`, `POST` |
| `/api/books/<pk>/` | `GET`, `PUT`, `PATCH`, `DELETE` |
| `/api/authors/<pk>/books/` | `GET` (dodatna radnja `@action`) |

Isto vrijedi za `authors` i `publishers`.

## Preglednik API-ja

{: .zadatak }
> Posjetite `http://127.0.0.1:8000/api/` u pregledniku. Kliknite na `books`, isprobajte pretragu `?search=` i poredak `?ordering=-publication_date`, otvorite detalje jedne knjige.

DRF pri pristupu iz preglednika prikazuje HTML sučelje (engl. *browsable API*) s obrascima za slanje zahtjeva. Programi koji šalju zaglavlje `Accept: application/json` dobivaju čisti JSON. Isto možete vidjeti dodavanjem `?format=json` na adresu.

## Ovlasti i autentifikacija

Trenutno svatko može brisati knjige. U `settings.py` postavljamo zadana pravila za cijeli API:

``` python
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}
```

`IsAuthenticatedOrReadOnly` svima dopušta čitanje (`GET`, `HEAD`, `OPTIONS`), a izmjene samo prijavljenim korisnicima. Ostale ugrađene klase su `AllowAny`, `IsAuthenticated`, `IsAdminUser` i `DjangoModelPermissions` (koristi ovlasti iz [poglavlja 12](12-autentifikacija-autorizacija.md)).

Ovlasti se mogu zadati i za pojedini pogled, a možemo napisati i vlastite:

``` python
from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsStaffOrReadOnly]
```

### Autentifikacija tokenom

`SessionAuthentication` koristi kolačić sesije, što radi u pregledniku nakon prijave na `/api-auth/login/`. Ostali klijenti (mobilne aplikacije, skripte) uz svaki zahtjev šalju **token**. Dodajemo aplikaciju i adresu za dobivanje tokena:

``` python
INSTALLED_APPS = [
    # ...
    "rest_framework",
    "rest_framework.authtoken",
]
```

``` shell
$ python manage.py migrate
```

``` python
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # ...
    path("api/token/", obtain_auth_token),
]
```

## Isprobavanje API-ja iz terminala

``` shell
$ curl http://127.0.0.1:8000/api/books/
$ curl "http://127.0.0.1:8000/api/books/?search=rat&ordering=title"

$ curl -X POST http://127.0.0.1:8000/api/token/ -d "username=admin&password=lozinka"
{"token":"9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"}

$ curl -X POST http://127.0.0.1:8000/api/books/ \
    -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
    -H "Content-Type: application/json" \
    -d '{"title": "Nova knjiga", "author": 1, "publication_date": "2024-05-01"}'

$ curl -X DELETE http://127.0.0.1:8000/api/books/5/ \
    -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

{: .napomena }
> U Windows PowerShellu `curl` može biti zamjenski naziv za `Invoke-WebRequest`. Koristite `curl.exe` ili alate s grafičkim sučeljem poput Postmana ili Bruna, a za jednostavne provjere dovoljan je i preglednik API-ja.

{: .zadatak }
> - Bez tokena pokušajte stvoriti knjigu metodom `POST`. Koji statusni kod dobivate?
> - Dobijte token za svog administratora i stvorite novu knjigu.
> - Pošaljite knjigu s datumom izdanja u budućnosti i pročitajte odgovor.
> - Izmijenite samo naslov knjige metodom `PATCH`.

## Dokumentacija i ostale teme

- **Dokumentacija API-ja**: paket [drf-spectacular](https://drf-spectacular.readthedocs.io/) iz pogleda i serializatora generira OpenAPI shemu i interaktivno sučelje Swagger UI.
- **CORS**: ako se API poziva iz JavaScripta s druge domene (npr. React aplikacija na `localhost:5173`), preglednik to blokira dok poslužitelj izričito ne dopusti. Za to se koristi paket `django-cors-headers`.
- **Filtriranje po poljima**: paket `django-filter` omogućuje upite poput `/api/books/?author=3&publisher=2`.
- **Verzioniranje**: kada se API mijenja na nekompatibilan način, uvodi se nova verzija, npr. `/api/v2/`.

## Zadaci za vježbu

{: .zadatak }
> - Dodajte `@action` na `PublisherViewSet` koja vraća sve knjige izdavača (`/api/publishers/<pk>/books/`).
> - Dodajte na `BookViewSet` radnju `recent` (`detail=False`) koja vraća 5 najnovijih knjiga.
> - Napišite `AuthorDetailSerializer` koji uz podatke o autoru sadrži i ugniježđeni popis njegovih knjiga (`books = BookSerializer(many=True, read_only=True)`) i koristite ga samo za detalje autora (nadjačajte `get_serializer_class()`).
> - Dopustite izmjene autora samo korisnicima s `is_staff`, a izmjene knjiga svim prijavljenim korisnicima.