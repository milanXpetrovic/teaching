---
author: Milan Petrović
title: "6. Django predlošci i dinamički prikaz sadržaja"
layout: default
parent: PZW
nav_order: 6
has_children: false
has_toc: false
nav_exclude: false
---

# Django predlošci i dinamički prikaz sadržaja
{: .no_toc }

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Zašto predlošci

U [poglavlju 3](03-arhitektura-url-pogledi.md) pogledi su vraćali HTML zapisan izravno u Python kodu. To brzo postaje nepregledno, a dizajneri i programeri si smetaju u istim datotekama. **Predlošci** (engl. *templates*) odvajaju prikaz od logike: pogled pripremi podatke (kontekst), a predložak odredi kako se prikazuju.

Django koristi vlastiti jezik predložaka (Django Template Language, DTL). Namjerno je ograničen: u predlošku se ne pišu proizvoljne Python naredbe, nego samo varijable, oznake i filteri. Logika pripada pogledima i modelima.

Nastavljamo s projektom `mysite` i modelima iz [poglavlja 5](05-relacije-i-upiti.md).

## Gdje Django traži predloške

Postavke su u `settings.py` pod `TEMPLATES`:

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

Django traži predložak redom: najprije u direktorijima iz `DIRS`, zatim u direktoriju `templates/` svake aplikacije iz `INSTALLED_APPS`. Prvi pronađeni se koristi.

{: .napomena }
> Predloške aplikacije spremamo u `main/templates/main/`, a ne izravno u `main/templates/`. Dodatni direktorij s imenom aplikacije je **imenski prostor**: kada bi dvije aplikacije imale predložak `index.html`, Django ne bi znao koji želimo. Ovako ih razlikujemo kao `main/index.html` i `blog/index.html`.

Stvorite direktorije:

``` shell
$ mkdir templates
$ mkdir -p main/templates/main
```

Na Windowsima umjesto `mkdir -p main/templates/main` koristite `mkdir main\templates\main`.

## Funkcija `render()`

Funkcija `render(request, predlozak, kontekst)` učita predložak, popuni ga podacima iz konteksta (rječnika) i vrati `HttpResponse`.

{: .zadatak }
> Definirajte pogled koji u bazi pronalazi sve studente zadanog imena. Ime neka se prenosi kroz URL (`studenti/ime/<str:ime>/`). Popis pronađenih studenata proslijedite funkciji `render` i prikažite u predlošku `main/studenti.html`.

**Rješenje zadatka.** U datoteci `main/views.py`:

``` python
from django.shortcuts import render

from .models import Student


def studenti_po_imenu(request, ime):
    studenti = Student.objects.filter(student_ime__iexact=ime)
    context = {"ime": ime, "studenti": studenti}
    return render(request, "main/studenti.html", context)
```

Koristimo `iexact` kako bi `/studenti/ime/marko/` pronašao i "Marko".

U datoteci `main/urls.py`:

``` python
path("studenti/ime/<str:ime>/", views.studenti_po_imenu, name="studenti_po_imenu"),
```

Datoteka `main/templates/main/studenti.html`:

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

{: .zadatak }
> Posjetite `http://127.0.0.1:8000/studenti/ime/Marko/` i `http://127.0.0.1:8000/studenti/ime/Zvonimir/`.

### Početna stranica s brojem zapisa

{: .zadatak }
> Izmijenite pogled `homepage` tako da u bazi prebroji studente, predmete i profesore te brojeve proslijedi predlošku `main/index.html`.

**Rješenje zadatka.** U datoteci `main/views.py`:

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

Datoteka `main/templates/main/index.html`:

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

{: .napomena }
> Metoda `count()` nikad ne podiže iznimku `DoesNotExist`: ako zapisa nema, jednostavno vraća 0. Iznimka se javlja samo kod dohvata jednog objekta metodom `get()`, a za taj slučaj postoji prečac `get_object_or_404()` (vidi u nastavku).

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

Ako varijabla ne postoji, Django ispisuje prazan niz umjesto da javi grešku.
{% endraw %}

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
{% endraw %}

{% raw %}
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

{: .zadatak }
> Stvorite osnovni predložak `templates/base.html` s naslovom stranice, izbornikom i blokom za sadržaj. Provjerite da je u `settings.py` pod `DIRS` navedena putanja `BASE_DIR / "templates"`.

**Rješenje zadatka.** Datoteka `templates/base.html`:

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

{: .upozorenje }
> Oznaka `url` javlja grešku `NoReverseMatch` ako URL zadanog imena ne postoji. Stavku izbornika "Predmeti" dodajte tek kada u nastavku poglavlja napravite pogled `predmeti`.

Podređeni predložak počinje oznakom `extends` i definira samo blokove koje mijenja. Izmijenimo `main/templates/main/index.html`:

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

{% raw %}
Oznaka `extends` mora biti prva oznaka u predlošku. Izraz `{{ block.super }}` umeće sadržaj istog bloka iz roditeljskog predloška, ovdje naslov "Fakultet".
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

## Popis i detalji predmeta

{: .zadatak }
> Napravite pogled `predmeti` koji prikazuje sve predmete s nositeljem i brojem upisanih studenata. Svaki predmet neka bude poveznica na stranicu s detaljima predmeta na kojoj se prikazuju opis, nositelj i popis studenata.

**Rješenje zadatka.** U datoteci `main/views.py`:

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

U datoteci `main/urls.py`:

``` python
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("studenti/ime/<str:ime>/", views.studenti_po_imenu, name="studenti_po_imenu"),
    path("predmeti/", views.predmeti, name="predmeti"),
    path("predmeti/<int:pk>/", views.predmet_detalj, name="predmet_detalj"),
]
```

Datoteka `main/templates/main/predmeti.html`:

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

Datoteka `main/templates/main/predmet_detalj.html`:

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
{% endraw %}

{% raw %}
Primijetite da se u predlošku metode pozivaju bez zagrada: `predmet.studenti.all`, a ne `predmet.studenti.all()`.
{% endraw %}

## Automatsko zaštićivanje (autoescape)

{% raw %}
Django sve varijable prije ispisa automatski zaštićuje (engl. *escape*): znakovi `<`, `>`, `&`, `'` i `"` pretvaraju se u HTML entitete. Ako student upiše ime `<script>alert(1)</script>`, predložak će ga prikazati kao tekst, a ne izvršiti kao skriptu. To je zaštita od XSS napada.

Filter `safe` isključuje zaštitu za pojedinu varijablu, npr. `{{ html_sadrzaj|safe }}`. Koristite ga **samo** za sadržaj koji ste sami generirali i kojem vjerujete, nikad za unos korisnika. Više u [poglavlju 13](13-sigurnost.md).
{% endraw %}

## Kontekstni procesori

{% raw %}
Neke varijable dostupne su u svim predlošcima bez da ih pogled izričito šalje. Dodaju ih kontekstni procesori iz postavke `context_processors`: `request` (trenutni zahtjev), `user` i `perms` (prijavljeni korisnik i njegove ovlasti) te `messages` (poruke korisniku). Primjerice, `{{ request.path }}` možemo iskoristiti za isticanje aktivne stavke izbornika.
{% endraw %}

## Vlastiti filteri (za one koji žele znati više)

Vlastite filtere pišemo u paketu `templatetags` unutar aplikacije. Stvorite `main/templatetags/__init__.py` (prazna datoteka) i `main/templatetags/main_extras.py`:

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

## Zadaci za vježbu

{: .zadatak }
> - Napravite stranicu `profesori/` koja prikazuje sve profesore i za svakog popis predmeta kojima je nositelj. Koristite `related_name` iz modela i `prefetch_related` u pogledu.
> - Napravite stranicu s detaljima studenta (`studenti/<int:pk>/`) s popisom upisanih predmeta i naslovom završnog rada, ako ga student ima.
> - Na stranici s detaljima predmeta svakog studenta pretvorite u poveznicu na njegovu stranicu s detaljima.
> - Dodajte u izbornik osnovnog predloška poveznicu na popis profesora.
> - Posjetite `/predmeti/9999/` i provjerite da dobivate odgovor 404.