---
author: Milan Petrović
title: "3. Arhitektura Django aplikacija, URL usmjeravanje i pogledi"
layout: default
parent: PZW
nav_order: 3
has_children: false
has_toc: true
nav_exclude: true
---

# Arhitektura Django aplikacija, URL usmjeravanje i pogledi
{: .no_toc }

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Paradigma model-view-controller (MVC)

Django koristi paradigmu [model-view-controller](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) (MVC) koju naziva model-template-view (MTV). Gotovo svaka stranica izrađena u Djangu koristi ova tri dijela kako bi prikazala podatke.

Korisnik posjeti URL, Django prema popisu URL-ova (`urls.py`) odabere odgovarajući pogled (`views.py`). Pogled po potrebi dohvati podatke iz modela (`models.py`) i preda ih predlošku (`templates/`) koji složi HTML. Ulogu kontrolera u Djangu dijele sam okvir (usmjeravanje URL-ova) i pogledi.

Unutar Djanga koristi se djelomično izmijenjena terminologija, a od sada nadalje koristit ćemo Django terminologiju (model, template i view).

| MVC naziv | Django naziv | Značenje |
| --------- | ------------ | -------- |
| Model | Model | Sloj podataka: Python klase (modeli) koje se preslikavaju na tablice u bazi podataka, zajedno s kodom koji radi s tim podacima. Modeli se mogu mijenjati i dopunjavati, a promjene se u bazi primjenjuju migracijama (vidi [poglavlje 4](04-baze-modeli-orm.md)). |
| View | Template | Sloj prikaza: predlošci, tj. HTML datoteke s posebnim oznakama u koje se umeću podaci. Određuju **kako** se podaci prikazuju (vidi [poglavlje 6](06-predlosci-dinamicki-sadrzaj.md)). |
| Controller | View | Sloj logike: funkcija ili klasa koja prima HTTP zahtjev i vraća HTTP odgovor. Određuje **koji** se podaci prikazuju: dohvaća ih iz modela, obrađuje obrasce i odabire predložak. Odgovor može biti HTML, preusmjeravanje, [statusni kod](https://http.cat/), JSON, slika i drugo. |

## Tijek obrade zahtjeva

Kada preglednik pošalje zahtjev, u Djangu se događa sljedeće:

1. Web poslužitelj preda zahtjev Djangu preko WSGI ili ASGI sučelja (`wsgi.py` ili `asgi.py`).
2. Django od zahtjeva napravi objekt `HttpRequest` i provuče ga kroz slojeve **middlewarea** (sesije, autentifikacija, CSRF zaštita...).
3. Usmjerivač URL-ova čita modul naveden u `ROOT_URLCONF` (`mysite/urls.py`) i redom uspoređuje putanju zahtjeva s uzorcima u `urlpatterns`.
4. Prvi uzorak koji odgovara određuje **pogled** koji se poziva. Ako nijedan ne odgovara, vraća se odgovor 404.
5. Pogled po potrebi radi s modelima i predlošcima te vraća objekt `HttpResponse`.
6. Odgovor ponovno prolazi kroz middleware (obrnutim redoslijedom) i šalje se pregledniku.

## Uvod u Django: Hello world

U nastavku je prikazano kako stvoriti stranicu koja prikazuje tekst na početnoj stranici. Za ovo nije potreban model, nego samo pogled u kojem je definiran tekst koji želimo prikazati.

{: .zadatak }
> Otvorite datoteku `mysite/mysite/urls.py` i provjerite što je u njoj zapisano.

Za definiranje putanje na koju će Django primati HTTP zahtjeve koristi se funkcija `django.urls.path()` ([dokumentacija](https://docs.djangoproject.com/en/6.1/ref/urls/#path)). Zadani sadržaj usmjerava samo na administratorsko sučelje ([dokumentacija](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/)).

Datoteka `mysite/mysite/urls.py` ima sadržaj:

``` python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]
```

Vidimo da imamo samo jedan URL, onaj za stranicu za administraciju, koji nam trenutno ne treba. Django web stranicu vidi kao kolekciju aplikacija, a datoteka `urls.py` projekta obično samo usmjerava zahtjeve prema URL-ovima pojedinih aplikacija.

Aplikaciju `main` stvorili smo i registrirali u [prethodnom poglavlju](02-projekti-i-aplikacije.md#stvaranje-prve-aplikacije). Usmjerimo sada glavni dio projekta prema njoj. To radimo u `mysite/mysite/urls.py`:

``` python
from django.contrib import admin
from django.urls import include, path  # uvozimo include

urlpatterns = [
    path("", include("main.urls")),  # dodajemo URL-ove aplikacije main
    path("admin/", admin.site.urls),
]
```

Ako pogledamo u direktorij aplikacije `main`, vidjet ćemo da datoteka `urls.py` ne postoji. Stvorimo datoteku `mysite/main/urls.py` sa sljedećim sadržajem:

``` python
from django.urls import path

from . import views

app_name = "main"  # imenski prostor (namespace) URL-ova aplikacije

urlpatterns = [
    path("", views.homepage, name="homepage"),
]
```

Prođimo ukratko kroz logiku rada programa. Za adresu `http://127.0.0.1:8000/` putanja je prazna, stoga odgovara uzorku `""` iz `path("", include("main.urls"))`. Django zato učitava `main.urls`, odnosno datoteku `mysite/main/urls.py`.

U njoj prazna putanja odgovara uzorku `path("", views.homepage, name="homepage")`. Time smo usmjerili Django da pozove funkciju `homepage()` iz `main/views.py`, koju moramo još napisati.

Datoteka `mysite/main/views.py`:

``` python
from django.http import HttpResponse


def homepage(request):
    # primijetite da odgovor može sadržavati HTML
    return HttpResponse("Welcome to homepage! <strong>#samoOIRI</strong>")
```

Svaki pogled kao prvi argument prima objekt `request` (zahtjev) i mora vratiti objekt odgovora.

{: .zadatak }
> Osvježite stranicu `http://127.0.0.1:8000/` u pregledniku.

## Više pogleda

{: .zadatak }
> Izmijenite funkciju `homepage()` u `main/views.py` tako da vraća cijeli HTML dokument s naslovom i odlomkom teksta.

**Rješenje zadatka.**

``` python
from django.http import HttpResponse


def homepage(request):
    return HttpResponse(
        "<html><body><h1>Homepage</h1>"
        "<p><strong>Homepage</strong> i još neki tekst na homepage.</p>"
        "</body></html>"
    )
```

{: .zadatak }
> Definirajte funkciju `current_datetime()` u datoteci `main/views.py` koja vraća HTTP odgovor s trenutnim datumom i vremenom. Dodajte joj putanju `vrijeme/`.

**Rješenje zadatka.** U datoteci `main/views.py`:

``` python
from django.utils import timezone


def current_datetime(request):
    now = timezone.localtime()
    html = f"<html><body>Trenutno vrijeme: {now:%d.%m.%Y. %H:%M:%S}</body></html>"
    return HttpResponse(html)
```

U datoteci `main/urls.py`:

``` python
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("vrijeme/", views.current_datetime, name="current_datetime"),
]
```

Koristimo `django.utils.timezone` umjesto modula `datetime` jer uvažava postavke `TIME_ZONE` i `USE_TZ`.

### Vraćanje grešaka u odgovorima na zahtjeve

{: .zadatak }
> Definirajte funkciju `not_found()` u `main/views.py`. Funkcija neka vraća `HttpResponseNotFound` s proizvoljnim sadržajem. Dodajte joj putanju `nema/`.

**Rješenje zadatka.** U datoteci `main/views.py`:

``` python
from django.http import HttpResponseNotFound


def not_found(request):
    return HttpResponseNotFound("<h1>Page not found</h1>")
```

Češći način vraćanja greške 404 je podizanje iznimke `Http404`. Django je tada sam pretvori u odgovor sa statusom 404:

``` python
from django.http import Http404


def tajna(request):
    raise Http404("Ova stranica ne postoji.")
```

## Dinamički dijelovi URL-a

Do sada su putanje bile statične. Često želimo da dio URL-a bude parametar, npr. `/predmeti/7/` ili `/pozdrav/Ana/`. Takve dijelove pišemo u šiljastim zagradama, a Django ih predaje pogledu kao imenovane argumente.

``` python
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("pozdrav/<str:ime>/", views.pozdrav, name="pozdrav"),
    path("zbroj/<int:a>/<int:b>/", views.zbroj, name="zbroj"),
]
```

``` python
def pozdrav(request, ime):
    return HttpResponse(f"Pozdrav, {ime}!")


def zbroj(request, a, b):
    return HttpResponse(f"{a} + {b} = {a + b}")
```

Dio prije dvotočke je **pretvarač** (engl. *path converter*) koji određuje što se smije pojaviti na tom mjestu i u koji tip se vrijednost pretvara:

| Pretvarač | Prihvaća | Tip u pogledu |
| --------- | -------- | ------------- |
| `str` | bilo koji niz znakova osim `/` (zadano) | `str` |
| `int` | nula ili pozitivan cijeli broj | `int` |
| `slug` | slova, brojke, `-` i `_`, npr. `uvod-u-django` | `str` |
| `uuid` | UUID, npr. `075194d3-6885-417e-a8a8-6c931e272f00` | `uuid.UUID` |
| `path` | bilo koji niz znakova uključujući `/` | `str` |

Ako vrijednost ne odgovara pretvaraču (npr. `/zbroj/dva/tri/`), uzorak se ne podudara i Django vraća 404, a pogled se uopće ne poziva.

{: .zadatak }
> Dodajte putanju `kvadrat/<int:broj>/` koja ispisuje kvadrat zadanog broja. Isprobajte `/kvadrat/12/` i `/kvadrat/-3/` te objasnite rezultat.

### Regularni izrazi u URL-ovima

Za složenija pravila postoji funkcija `re_path()` koja prima regularni izraz:

``` python
from django.urls import re_path

urlpatterns = [
    re_path(r"^arhiva/(?P<godina>[0-9]{4})/$", views.arhiva, name="arhiva"),
]
```

U većini slučajeva pretvarači iz `path()` su dovoljni i čitljiviji.

{: .upozorenje }
> Ako trebate osvježiti znanje regularnih izraza, pogledajte gradivo kolegija Operacijski sustavi te dokumentaciju [Regularni izrazi i Python](https://docs.python.org/3/library/re.html#module-re).

## Imenovani URL-ovi i funkcija `reverse()`

Svaki uzorak smo imenovali argumentom `name`, a aplikaciji smo zadali imenski prostor s `app_name = "main"`. Zahvaljujući tome adrese u kodu nikad ne pišemo ručno, nego ih Django složi iz imena:

``` python
from django.urls import reverse

reverse("main:homepage")                 # '/'
reverse("main:pozdrav", args=["Ana"])     # '/pozdrav/Ana/'
reverse("main:zbroj", kwargs={"a": 2, "b": 3})  # '/zbroj/2/3/'
```

Ako kasnije promijenimo `pozdrav/` u `hello/`, sve poveznice nastavljaju raditi jer se izračunavaju iz imena. U predlošcima isto radi oznaka `url` (vidi [poglavlje 6](06-predlosci-dinamicki-sadrzaj.md)):

{% raw %}
``` django
<a href="{% url 'main:pozdrav' 'Ana' %}">Pozdravi Anu</a>
```
{% endraw %}

### Preusmjeravanje

Funkcija `redirect()` vraća odgovor koji preglednik upućuje na drugu adresu. Prima ime URL-a, objekt ili adresu:

``` python
from django.shortcuts import redirect


def stara_adresa(request):
    return redirect("main:homepage")
```

## Objekt `HttpRequest`

Pogled preko argumenta `request` ima pristup svim podacima o zahtjevu:

| Atribut | Sadržaj |
| ------- | ------- |
| `request.method` | HTTP metoda: `"GET"`, `"POST"`... |
| `request.path` | putanja, npr. `/pozdrav/Ana/` |
| `request.GET` | parametri iz URL-a nakon `?`, npr. za `?ime=Ana&dob=20` |
| `request.POST` | podaci poslani obrascem metodom POST |
| `request.headers` | zaglavlja zahtjeva, npr. `request.headers["User-Agent"]` |
| `request.COOKIES` | kolačići |
| `request.user` | prijavljeni korisnik (vidi [poglavlje 12](12-autentifikacija-autorizacija.md)) |

``` python
def info(request):
    ime = request.GET.get("ime", "neznanče")
    preglednik = request.headers.get("User-Agent", "nepoznat")
    return HttpResponse(
        f"<p>Bok, {ime}!</p>"
        f"<p>Metoda: {request.method}, putanja: {request.path}</p>"
        f"<p>Preglednik: {preglednik}</p>"
    )
```

{: .zadatak }
> Dodajte pogled `info` na putanju `info/` i posjetite `http://127.0.0.1:8000/info/?ime=Ana`. Što se dogodi ako izostavite parametar `ime`?

{: .upozorenje }
> Ovdje podatke od korisnika izravno umećemo u HTML samo radi jednostavnosti primjera. U stvarnim aplikacijama to otvara mogućnost XSS napada. Predlošci (poglavlje 6) takve vrijednosti automatski zaštićuju, a detalji su u [poglavlju 13](13-sigurnost.md).

## Vrste odgovora i statusni kodovi

| Klasa ili funkcija | Statusni kod | Namjena |
| ------------------ | ------------ | ------- |
| `HttpResponse` | 200 (ili zadani `status=`) | općeniti odgovor |
| `JsonResponse` | 200 | odgovor u formatu JSON |
| `redirect()`, `HttpResponseRedirect` | 302 | privremeno preusmjeravanje |
| `HttpResponsePermanentRedirect` | 301 | trajno preusmjeravanje |
| `HttpResponseBadRequest` | 400 | neispravan zahtjev |
| `HttpResponseForbidden` | 403 | zabranjen pristup |
| `HttpResponseNotFound`, `raise Http404` | 404 | resurs ne postoji |
| `HttpResponseNotAllowed` | 405 | metoda nije dopuštena |

Primjer odgovora u formatu JSON, koji je temelj za REST API (vidi [poglavlje 11](11-rest-api.md)):

``` python
from django.http import JsonResponse


def api_vrijeme(request):
    return JsonResponse({"vrijeme": timezone.localtime().isoformat()})
```

Dopuštene HTTP metode možemo ograničiti dekoratorima:

``` python
from django.views.decorators.http import require_GET


@require_GET
def samo_citanje(request):
    return HttpResponse("Ovaj pogled prihvaća samo GET.")
```

## Pogledi kao funkcije i kao klase

Pogledi mogu biti funkcije (engl. *function-based views*) ili klase (engl. *class-based views*). Isti pogled napisan kao klasa:

``` python
from django.views import View


class PozdravView(View):
    def get(self, request, ime):
        return HttpResponse(f"Pozdrav, {ime}!")
```

``` python
path("pozdrav-klasa/<str:ime>/", views.PozdravView.as_view(), name="pozdrav_klasa"),
```

Klasa za svaku HTTP metodu ima zasebnu metodu (`get`, `post`...), a nedopuštene metode automatski odbija statusom 405. Prava snaga klasa su **generički pogledi** za česte zadatke poput popisa i detalja objekata, opisani u [poglavlju 7](07-genericki-pogledi.md).

{: .zadatak }
> - Napišite pogled `kalkulator` na putanji `kalkulator/<int:a>/<str:operacija>/<int:b>/` koji podržava operacije `plus`, `minus`, `puta` i `kroz`. Za nepoznatu operaciju vratite `HttpResponseBadRequest`, a za dijeljenje nulom podignite `Http404` s odgovarajućom porukom.
> - Napišite pogled koji vraća `JsonResponse` s rezultatom kalkulatora.
> - Napišite pogled `/stara-pocetna/` koji preusmjerava na početnu stranicu koristeći ime URL-a.