---
parent: 'Naprednije Teme za Kompletnog Django Developera'
nav_order: 1
has_children: false
title: 'Poglavlje 10: Django REST Framework (DRF)'
---

# Poglavlje 10: Django REST Framework (DRF)

Do sada smo gradili web stranice gdje Django renderira HTML i šalje ga pregledniku. To je klasičan, "monolitan" pristup. Međutim, moderni web se sve više oslanja na razdvajanje **front-enda** (ono što korisnik vidi u pregledniku) i **back-enda** (logika na serveru).

Kako bi naš front-end (npr. JavaScript aplikacija) ili mobilna aplikacija mogli komunicirati s našim Django back-endom, potreban im je zajednički jezik. Taj jezik je **API** (Application Programming Interface), a najpopularniji stil za izradu API-ja danas je **REST** (Representational State Transfer).

**Django REST Framework (DRF)** je moćna i fleksibilna biblioteka koja nam omogućuje da brzo i jednostavno izgradimo REST API-je povrh naših postojećih Django aplikacija.

## 10.1 Uvod u REST API

REST nije tehnologija, već **arhitektonski stil** – set pravila i preporuka za dizajniranje umreženih aplikacija. On koristi standardne HTTP metode za manipulaciju podacima.

Glavni koncepti REST-a su:
* **Resursi (Resources):** Svaki podatak u vašoj aplikaciji je "resurs" (npr. post, korisnik, komentar). Svaki resurs ima jedinstveni identifikator – svoj URL (npr. `/api/posts/1/`).
* **HTTP Metode (Verbs):** Standardne HTTP metode se koriste za izvođenje operacija (CRUD) na resursima.
    * `GET`: Dohvati resurs(e). (Read)
    * `POST`: Kreiraj novi resurs. (Create)
    * `PUT` / `PATCH`: Ažuriraj postojeći resurs. (Update)
    * `DELETE`: Obriši resurs. (Delete)
* **Reprezentacije (Representations):** Kada klijent zatraži resurs, server ne šalje sam objekt iz baze, već njegovu **reprezentaciju** u formatu koji klijent razumije. Danas je to gotovo uvijek **JSON** (JavaScript Object Notation).

## 10.2 Instalacija i Postavljanje DRF-a

1. **Instalacija:**
    U vašem aktivnom virtualnom okruženju, pokrenite:

        pip install djangorestframework

2. **Dodavanje u `INSTALLED_APPS`:**
    U `myproject/settings.py`, dodajte `rest_framework` na listu instaliranih aplikacija.

        INSTALLED_APPS = [
            # ...
            'rest_framework',
            'posts', # Naša aplikacija
        ]

Sada je DRF spreman za korištenje u našem projektu.

---

## 10.3 Serializeri: Prevoditelji Podataka

Prvi ključni koncept u DRF-u je **Serializer**. Njegov posao je da "prevodi" kompleksne tipove podataka, poput Django model objekata, u nativne Python tipove koje je zatim lako renderirati u JSON (i obrnuto).

* **Serializacija:** `Post` objekt → Python `dict` → JSON string (za slanje klijentu).
* **Deserializacija:** JSON string → Python `dict` → Validacija podataka → `Post` objekt (za spremanje u bazu).

`ModelSerializer` radi ovo gotovo automatski za naše modele.

**Kreirajmo serializer za naš `Post` model:**

1. Unutar `posts` aplikacije, stvorite novu datoteku `serializers.py`.
2. Dodajte sljedeći kod:

        # posts/serializers.py
        from rest_framework import serializers
        from .models import Post

        class PostSerializer(serializers.ModelSerializer):
            class Meta:
                model = Post
                fields = ['id', 'title', 'content', 'author', 'date_posted']

Ovo je vrlo slično definiciji `ModelForm`. Govorimo DRF-u da koristi `Post` model i da u reprezentaciji uključi navedena polja.

---

## 10.4 Viewovi za API

DRF nudi set generičkih, klasnih viewova koji su specijalizirani za izgradnju API endpointa, slično kao što Django nudi CBV-ove za HTML stranice.

Kreirajmo dva osnovna API endpointa za naše postove:
1. Endpoint za listu svih postova i kreiranje novog posta (`/api/posts/`).
2. Endpoint za detalje, ažuriranje i brisanje pojedinog posta (`/api/posts/<pk>/`).

**U `posts/views.py` (ili, još bolje, u `posts/api_views.py`):**

    # posts/api_views.py
    from rest_framework import generics
    from .models import Post
    from .serializers import PostSerializer

    class PostListCreateAPIView(generics.ListCreateAPIView):
        queryset = Post.objects.all()
        serializer_class = PostSerializer

    class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
        queryset = Post.objects.all()
        serializer_class = PostSerializer

* `generics.ListCreateAPIView`: Ovaj view automatski pruža `GET` (lista) i `POST` (kreiranje) funkcionalnost.
* `generics.RetrieveUpdateDestroyAPIView`: Ovaj view automatski pruža `GET` (detalji), `PUT`/`PATCH` (ažuriranje) i `DELETE` (brisanje) funkcionalnost.

**Povezivanje URL-ova:**

Sada moramo kreirati URL-ove za ove API viewove. Dobra je praksa držati ih odvojeno, npr. pod `/api/` prefiksom.

1. U `posts/urls.py` dodajte:

        # posts/urls.py
        from django.urls import path
        from . import api_views # Importamo naše nove API viewove

        urlpatterns = [
            path('api/posts/', api_views.PostListCreateAPIView.as_view(), name='api-post-list'),
            path('api/posts/<int:pk>/', api_views.PostRetrieveUpdateDestroyAPIView.as_view(), name='api-post-detail'),
        ]

**Testiranje u pregledniku:**

DRF dolazi s fantastičnim alatom: **Browsable API**. Ako sada pokrenete server i posjetite `http://127.0.0.1:8000/api/posts/` u svom pregledniku, nećete dobiti samo "goli" JSON. Dobit ćete lijepo formatirano HTML sučelje koje vam omogućuje da interaktivno pregledavate i šaljete podatke na vaš API!

---

## 10.5 Autentikacija i Dozvole u DRF-u

Po defaultu, naši API endpointi su javni. To rijetko kada želimo. Moramo ih osigurati.

DRF ima vlastiti sustav **autentikacije** i **dozvola (permissions)**, koji se nadovezuje na Djangov.

### Globalne postavke

Najlakši način je postaviti globalna pravila za cijeli API u `settings.py`.

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        ]
    }

* `DEFAULT_PERMISSION_CLASSES`: Lista klasa koje provjeravaju dozvole. `IsAuthenticated` jednostavno provjerava je li korisnik prijavljen. Ako nije, vraća `401 Unauthorized`.
* `DEFAULT_AUTHENTICATION_CLASSES`: Lista klasa koje pokušavaju autentificirati korisnika.
    * `SessionAuthentication`: Standardna Django autentikacija putem sesijskih kolačića. Idealno za JavaScript aplikacije na istoj domeni.
    * `TokenAuthentication`: Autentikacija putem jedinstvenog tokena koji se šalje u HTTP headeru. Idealno za mobilne i vanjske aplikacije.

### Prilagodba po Viewu

Globalne postavke možemo nadjačati na razini pojedinog viewa. Na primjer, ako želimo da lista postova bude javna, a samo kreiranje za prijavljene korisnike:

    from rest_framework.permissions import IsAuthenticatedOrReadOnly

    class PostListCreateAPIView(generics.ListCreateAPIView):
        queryset = Post.objects.all()
        serializer_class = PostSerializer
        permission_classes = [IsAuthenticatedOrReadOnly]

`IsAuthenticatedOrReadOnly` je ugrađena dozvola koja dopušta `GET` zahtjeve svima, ali `POST`, `PUT`, `DELETE` samo autentificiranim korisnicima.

### Kreiranje vlastitih dozvola

Za kompleksniju logiku, poput "samo autor smije uređivati post", pišemo vlastitu klasu za dozvole.

    # posts/permissions.py
    from rest_framework import permissions

    class IsAuthorOrReadOnly(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):
            # Dozvoli GET, HEAD, OPTIONS zahtjeve svima
            if request.method in permissions.SAFE_METHODS:
                return True
            # Dozvoli pisanje samo autoru posta
            return obj.author == request.user

I zatim je primijenimo na naš view:

    # posts/api_views.py
    from .permissions import IsAuthorOrReadOnly

    class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
        # ...
        permission_classes = [IsAuthorOrReadOnly]

---

Django REST Framework je duboka i moćna biblioteka. Ovo poglavlje je tek zagrebalo po površini. Prošli smo kroz ključne komponente – **Serializere**, **Generičke Viewove** i **Permissions** – koje vam omogućuju da u samo nekoliko linija koda stvorite siguran, robustan i za korištenje jednostavan REST API.

S ovim znanjem, spremni ste početi razdvajati svoj back-end i front-end, otvarajući vrata za izradu modernih, interaktivnih JavaScript aplikacija, mobilnih aplikacija i još mnogo toga.
