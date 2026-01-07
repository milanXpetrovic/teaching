---
parent: 'Django Temelji: Od Projekta do Prve Aplikacije'
nav_order: 3
title: '2.3 Kreiranje Django Aplikacije'
---

# 2.3 Kreiranje Django Aplikacije

U prošlom koraku stvorili smo Django **projekt**. Sada je vrijeme da unutar njega stvorimo našu prvu **aplikaciju**.

## Projekt vs. Aplikacija: Koja je razlika?

Ovo je jedan od najvažnijih koncepata u Djangu koji početnicima može biti zbunjujuć.

* **Projekt:** Možemo ga zamisliti kao "kontejner" ili "omot" za cijelu web stranicu ili web servis. Projekt se brine o globalnim postavkama (poput baze podataka, tajnih ključeva) i glavnoj URL konfiguraciji. Jedan projekt se sastoji od jedne ili više aplikacija.

* **Aplikacija:** Aplikacija (ili skraćeno *app*) je manja, samostalna programska cjelina koja obavlja jednu, specifičnu funkciju. Dobra Django aplikacija je:
    * **Fokusirana:** Radi jednu stvar i radi je dobro. (npr. blog, ankete, registracija korisnika).
    * **Modularna:** Samostalna je i ne ovisi previše o drugim dijelovima projekta.
    * **Ponovno iskoristiva (Reusable):** Idealno, dobro napisanu aplikaciju možete jednostavno "presaditi" iz jednog projekta u drugi.

> **Analogija:** Ako je vaš **projekt** kuća, onda su **aplikacije** sobe. Imate kuhinju (app za recepte), dnevni boravak (app za blog), spavaću sobu (app za korisničke profile). Svaka soba ima svoju specifičnu namjenu, ali sve zajedno čine funkcionalnu kuću.

## `startapp`: Stvaranje aplikacije

Kreirajmo aplikaciju koja će se baviti objavama na našem budućem blogu. Uobičajena konvencija je da se aplikacije nazivaju u množini.

1. Otvorite terminal i provjerite da se nalazite u korijenu vašeg Django projekta (u istom direktoriju gdje je i `manage.py`).
2. Pokrenite sljedeću naredbu:

        python manage.py startapp posts

    Ova naredba će stvoriti novi direktorij naziva `posts` sa sljedećom strukturom:

        posts/
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── migrations/
        │   └── __init__.py
        ├── models.py
        ├── tests.py
        └── views.py

### Struktura aplikacije

* `admin.py`: Konfiguracijska datoteka za registraciju modela u Djangovom admin sučelju.
* `apps.py`: Konfiguracijska datoteka za samu aplikaciju.
* `migrations/`: Direktorij u koji Django sprema "povijest" promjena vaših modela (strukture baze podataka).
* `models.py`: Mjesto gdje ćemo definirati naše **Modele** (strukturu podataka).
* `tests.py`: Datoteka za pisanje testova za vašu aplikaciju.
* `views.py`: Mjesto gdje ćemo pisati naše **Viewove** (poslovnu logiku).

## "Ožičavanje" aplikacije u projekt

Samo stvaranje aplikacije nije dovoljno. Moramo eksplicitno reći našem Django **projektu** da je svjestan postojanja nove aplikacije i da je treba uključiti.

1. Otvorite datoteku `myproject/settings.py` u vašem editoru koda.
2. Pronađite listu koja se zove `INSTALLED_APPS`.
3. Na dno te liste dodajte ime konfiguracijske klase vaše nove aplikacije. Konfiguracijska klasa se nalazi u `posts/apps.py` i obično se zove `[ImeAplikacije]Config` (u našem slučaju `PostsConfig`). Ime dodajemo kao string putanju do te klase.

    ```python
    # myproject/settings.py

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        
        # Naše aplikacije
        'posts.apps.PostsConfig',
    ]
    ```

> **Zašto `posts.apps.PostsConfig`?** Iako bi i samo `'posts'` radilo, eksplicitno navođenje putanje do konfiguracijske klase je modernija i preporučena praksa. Omogućuje bolju konfiguraciju aplikacije u budućnosti.

Sada je naš Django projekt svjestan `posts` aplikacije. To znači da će, na primjer, moći pronaći njezine modele kada budemo radili migracije baze podataka.

## Naš prvi "Hello World" View

Da bismo potvrdili da je sve ispravno povezano, napravit ćemo najjednostavniji mogući view.

1. **Kreiranje Viewa:** Otvorite `posts/views.py` i dodajte sljedeći kod:

    ```python
    # posts/views.py
    from django.http import HttpResponse

    def home(request):
        return HttpResponse("Pozdrav iz Posts aplikacije!")
    ```

2. **Kreiranje URL-ova za aplikaciju:** Unutar `posts` direktorija, stvorite novu datoteku `urls.py` (ne postoji po defaultu!) i dodajte sljedeće:

    ```python
    # posts/urls.py
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.home, name='posts-home'),
    ]
    ```

3. **Povezivanje URL-ova aplikacije s projektom:** Sada moramo reći glavnom `myproject/urls.py` da uključi URL-ove iz naše `posts` aplikacije. Otvorite `myproject/urls.py` i izmijenite ga da izgleda ovako:

    ```python
    # myproject/urls.py
    from django.contrib import admin
    from django.urls import path, include  # Dodajte 'include'

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('posts.urls')),  # Dodajte ovu liniju
    ]
    ```
    Ova linija govori Djangu: "Za svaku URL putanju koja počinje s praznim stringom (tj. korijenski URL), preusmjeri daljnje procesiranje na `posts.urls`."

4. **Testiranje:**
    *   Pokrenite razvojni server (`python manage.py runserver`).
    *   Posjetite [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Ako u pregledniku vidite poruku "Pozdrav iz Posts aplikacije!", uspješno ste stvorili, povezali i prikazali svoj prvi Django view unutar aplikacije.

Sada imamo čvrste temelje i potpunu strukturu za daljnji razvoj. Spremni smo zaroniti u srce Djanga: **Modele, Viewove i Template**.
