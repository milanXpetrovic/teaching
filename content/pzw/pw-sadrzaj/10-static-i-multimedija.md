---
author: Milan Petrović
title: "10. Upravljanje statičkim datotekama i multimedijom"
layout: default
parent: PZW
nav_order: 10
has_children: false
has_toc: false
nav_exclude: false
---

# Upravljanje statičkim datotekama i multimedijom
{: .no_toc }

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Statičke i medijske datoteke

Django razlikuje dvije vrste datoteka koje nisu Python kod ni predlošci:

| | Statičke datoteke (*static*) | Medijske datoteke (*media*) |
| --- | --- | --- |
| što su | CSS, JavaScript, slike sučelja, fontovi | datoteke koje učitavaju korisnici: fotografije, PDF-ovi |
| tko ih stvara | programer, dio su koda | korisnici, za vrijeme rada aplikacije |
| idu u Git | da | ne |
| postavke | `STATIC_URL`, `STATICFILES_DIRS`, `STATIC_ROOT` | `MEDIA_URL`, `MEDIA_ROOT` |
| u predlošku | `static` oznaka | atribut `.url` polja |

Nastavljamo s projektom `knjiznica`.

## Vanjski CSS

Najjednostavniji način dodavanja stila je uvoz gotovog CSS-a s vanjskog poslužitelja (CDN-a), npr. Bootstrapa, u zaglavlje osnovnog predloška:

{% raw %}
``` django
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
    <title>{% block title %}Knjižnica{% endblock %}</title>
</head>
```
{% endraw %}

Prednost je jednostavnost, a nedostatak ovisnost o tuđem poslužitelju. Za vlastiti CSS koristimo statičke datoteke.

## Statičke datoteke

### Postavke

Aplikacija `django.contrib.staticfiles` je već u `INSTALLED_APPS`, a u `settings.py` postoji:

``` python
STATIC_URL = "static/"
```

`STATIC_URL` je URL prefiks pod kojim su statičke datoteke dostupne, npr. `/static/main/style.css`.

### Direktorij za statičke datoteke

Kao i kod predložaka, statičke datoteke aplikacije spremamo u direktorij `static/` unutar aplikacije, s dodatnim poddirektorijem imena aplikacije kao imenskim prostorom:

``` text
main/
└── static/
    └── main/
        ├── style.css
        └── img/
            └── logo.png
```

{: .zadatak }
> Unutar aplikacije `main` stvorite direktorij `static/main` i u njemu datoteku `style.css`.

Sadržaj datoteke `style.css` možete proizvoljno zadati i prilagođavati vlastitim željama. Primjerice, datoteka `main/static/main/style.css` može biti oblika:

``` css
h1 {
    color: blue;
    text-align: center;
}

h2 {
    text-align: center;
}

#sidebar li {
    list-style-type: none;
    display: inline-block;
}

#sidebar li a {
    padding: 16px;
}
```

### Korištenje u predlošku

{% raw %}
Statičku datoteku u predlošku referenciramo oznakom `static`, koju prvo moramo učitati s `{% load static %}`:

``` django
{% load static %}
<!DOCTYPE html>
<html lang="hr">
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="{% static 'main/style.css' %}">
    <title>{% block title %}Knjižnica{% endblock %}</title>
</head>
```

Oznaka `{% static 'main/style.css' %}` postaje `/static/main/style.css`. Adresu ne pišemo ručno jer se `STATIC_URL` u produkciji često mijenja (npr. u adresu CDN-a).
{% endraw %}

{: .upozorenje }
> Oznaku `load static` treba navesti u **svakom** predlošku koji koristi `static`, i u podređenim predlošcima, jer se učitane oznake ne nasljeđuju.

Na isti način dodajemo slike i JavaScript:

{% raw %}
``` django
<img src="{% static 'main/img/logo.png' %}" alt="Logo knjižnice">
<script src="{% static 'main/app.js' %}" defer></script>
```
{% endraw %}

{: .napomena }
> Ako se promjena CSS-a ne vidi, preglednik vjerojatno koristi spremljenu (*cache*) verziju. Osvježite stranicu s <kbd>Ctrl</kbd>+<kbd>F5</kbd> (na macOS-u <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd>). Ako ste direktorij `static` stvorili dok je poslužitelj radio, ponovno ga pokrenite.

{: .zadatak }
> Dopunite `style.css` tako da elementima s klasama `book` i `author` (iz predložaka `book_list.html` i `author_list.html`) dodate obrub.

**Rješenje zadatka.** U datoteku `style.css` dodajemo:

``` css
.book {
    border-color: cyan;
    border-style: double;
    padding: 0 20px 20px;
    margin-bottom: 10px;
}

.author {
    border-color: olive;
    border-style: double;
    padding: 0 20px 20px;
    margin-bottom: 10px;
}
```

### Zajedničke statičke datoteke projekta

Datoteke koje ne pripadaju nijednoj aplikaciji (npr. zajednički logo) držimo u direktoriju `static/` u korijenu projekta i navodimo ga u postavkama:

``` python
STATICFILES_DIRS = [BASE_DIR / "static"]
```

Django za vrijeme razvoja traži datoteke u direktorijima iz `STATICFILES_DIRS` i u `static/` direktorijima aplikacija. Naredbom `python manage.py findstatic main/style.css` možete provjeriti gdje je datoteka pronađena.

### Statičke datoteke u produkciji

Razvojni poslužitelj poslužuje statičke datoteke samo dok je `DEBUG = True`. U produkciji se sve statičke datoteke skupljaju u jedan direktorij koji poslužuje web poslužitelj (npr. Nginx) ili paket WhiteNoise:

``` python
STATIC_ROOT = BASE_DIR / "staticfiles"
```

``` shell
$ python manage.py collectstatic
```

Naredba `collectstatic` kopira datoteke iz svih aplikacija i iz `STATICFILES_DIRS` u `STATIC_ROOT`. Direktorij `staticfiles/` ne ide u Git jer se uvijek može ponovno stvoriti.

Kako preglednici ne bi koristili staru verziju datoteke nakon promjene, koristi se pohrana koja imenu datoteke dodaje sažetak sadržaja (npr. `style.3f2a1c.css`):

``` python
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"},
}
```

{: .napomena }
> Jednostavan način posluživanja statičkih datoteka iz same Django aplikacije je paket [WhiteNoise](https://whitenoise.readthedocs.io/): nakon instalacije dodaje se `"whitenoise.middleware.WhiteNoiseMiddleware"` u `MIDDLEWARE`, odmah iza `SecurityMiddleware`.

## Medijske datoteke

### Postavke

U `settings.py` dodajemo:

``` python
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
```

`MEDIA_ROOT` je direktorij na disku gdje se spremaju učitane datoteke, a `MEDIA_URL` URL prefiks pod kojim su dostupne.

Za vrijeme razvoja medijske datoteke poslužuje Django. U `knjiznica/urls.py` dodajemo:

``` python
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Funkcija `static()` dodaje uzorke samo kada je `DEBUG = True`. U produkciji medijske datoteke poslužuje web poslužitelj ili vanjska pohrana (npr. S3, preko paketa `django-storages`).

### Polja `ImageField` i `FileField`

Za rad sa slikama potreban je paket Pillow:

``` shell
$ python -m pip install Pillow
```

Dodajmo autoru fotografiju. U `main/models.py`:

``` python
import uuid
from pathlib import Path

from django.db import models


def author_photo_path(instance, filename):
    """Sprema fotografiju pod nasumičnim imenom, zadržavajući nastavak."""
    ext = Path(filename).suffix.lower()
    return f"autori/{uuid.uuid4().hex}{ext}"


class Author(models.Model):
    # ... postojeća polja ...
    photo = models.ImageField("fotografija", upload_to=author_photo_path, blank=True)
```

Argument `upload_to` određuje poddirektorij unutar `MEDIA_ROOT`. Može biti niz znakova (npr. `"autori/"`) ili funkcija koja vraća putanju. Funkcija nam omogućuje da datoteke ne spremamo pod imenom koje je zadao korisnik, čime izbjegavamo sukobe imena i čudne znakove.

{: .napomena }
> Funkcija za `upload_to` mora biti definirana na razini modula (ne kao `lambda` ni kao metoda), jer se njezino ime zapisuje u migraciju.

U bazi se ne sprema sama datoteka, nego samo putanja do nje, npr. `autori/9f1c...e2.jpg`. Napravite i primijenite migraciju.

### Učitavanje datoteka kroz obrazac

{% raw %}
Da bi obrazac mogao slati datoteke, element `<form>` mora imati atribut `enctype="multipart/form-data"`, a metoda mora biti POST. Bez tog atributa preglednik šalje samo ime datoteke.

``` django
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form }}
    <button type="submit">Spremi</button>
</form>
```
{% endraw %}

Učitane datoteke Django sprema u `request.FILES`, a ne u `request.POST`. Generički pogledi `CreateView` i `UpdateView` to obrađuju sami. U funkcijskom pogledu obrascu predajemo oba rječnika:

``` python
form = AuthorForm(request.POST, request.FILES, instance=author)
```

`ModelForm` za autora s fotografijom u `main/forms.py`:

``` python
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "city", "country", "date_of_birth", "date_of_death", "photo"]

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        if photo and photo.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Fotografija smije imati najviše 2 MB.")
        return photo
```

`ImageField` uz pomoć Pillowa sam provjerava je li učitana datoteka stvarno slika. Za ostale datoteke dopuštene nastavke ograničavamo validatorom:

``` python
from django.core.validators import FileExtensionValidator

pdf = models.FileField(
    upload_to="knjige/pdf/",
    blank=True,
    validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
)
```

### Prikaz u predlošku

{% raw %}
Adresu datoteke daje atribut `.url` polja. Kako polje može biti prazno, prvo provjeravamo postoji li datoteka:

``` django
{% if author.photo %}
    <img src="{{ author.photo.url }}" alt="Fotografija: {{ author.name }}" width="200">
{% else %}
    <p>Fotografija nije dostupna.</p>
{% endif %}
```
{% endraw %}

Ostali korisni atributi su `author.photo.name` (putanja unutar `MEDIA_ROOT`), `author.photo.size` (veličina u bajtovima), te za slike `author.photo.width` i `author.photo.height`.

{: .upozorenje }
> Django pri brisanju objekta ili zamjeni datoteke **ne briše** staru datoteku s diska. Za čišćenje se koristi signal `post_delete` ili paket `django-cleanup`.

### Sigurnost učitanih datoteka
{: #sigurnost-ucitanih-datoteka }

Datoteke koje šalju korisnici treba smatrati nepouzdanima:

- ograničite dopuštene vrste i veličinu datoteka,
- ne koristite ime datoteke koje je poslao korisnik (zato `upload_to` funkcija),
- ne dopuštajte učitavanje HTML-a ni SVG-a koji bi se prikazivali na vašoj domeni (mogu sadržavati JavaScript),
- direktorij `media/` ne stavljajte u Git i u produkciji ga poslužujte tako da se datoteke nikad ne izvršavaju kao kod.

Više o tome u [poglavlju 13](13-sigurnost.md).

## Zadaci za vježbu

{: .zadatak }
> - Dodajte autoru fotografiju, prikažite je na stranici s detaljima autora i u popisu autora (kao manju sličicu).
> - Napravite stranice za dodavanje i uređivanje autora s mogućnošću učitavanja fotografije. Provjerite što se dogodi ako iz obrasca uklonite `enctype`.
> - Dodajte knjizi polje `cover` (`ImageField`) za naslovnicu i prikažite naslovnice na popisu knjiga.
> - U direktoriju `static/` u korijenu projekta napravite zajednički `logo.png` i prikažite ga u zaglavlju osnovnog predloška.
> - Postavite `STATIC_ROOT`, pokrenite `collectstatic` i pregledajte sadržaj direktorija `staticfiles/`. Odakle su došle datoteke administratorskog sučelja?