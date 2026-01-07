---
parent: 'Srce Djanga: Modeli, Viewovi, Templatei (MVT)'
nav_order: 2
has_children: false
title: 'Poglavlje 4: URL-ovi i Viewovi'
---

# Poglavlje 4: URL-ovi i Viewovi (Logika zahtjeva i odgovora)

U prošlom poglavlju definirali smo strukturu naših podataka pomoću **Modela**. Međutim, ti podaci trenutno "sjede" u bazi i nitko ih ne može vidjeti. U ovom poglavlju, naučit ćemo kako kreirati logiku koja će te podatke dohvatiti i prikazati korisnicima, te kako tu logiku povezati s određenim web adresama (URL-ovima).

To je posao za **Viewove** i **URLconfs**.

## Što je View?

**View** (pogled) je srce dinamike u Djangu. To je Python funkcija (ili klasa) koja prima web zahtjev i vraća web odgovor. Njegova uloga je da bude posrednik:

1. **Prima zahtjev:** Dobiva `HttpRequest` objekt koji sadrži sve informacije o korisnikovom zahtjevu (koji URL je posjetio, koju HTTP metodu je koristio, je li ulogiran itd.).
2. **Obavlja logiku:** Dohvaća podatke iz baze putem **Modela**, izvršava izračune, provjerava dozvole, obrađuje forme.
3. **Vraća odgovor:** Kreira i vraća `HttpResponse` objekt koji će biti poslan natrag korisnikovom pregledniku. Najčešće je to HTML stranica, ali može biti i preusmjeravanje (redirect), 404 greška, JSON, slika, ili bilo što drugo.

## 4.1 URL Routing: Djangov prometnik

Kako Django zna koji `View` treba pozvati za određeni URL? Odgovor leži u `urls.py` datotekama, koje se zajednički nazivaju **URLconf** (URL configuration).

URLconf je poput prometnika ili telefonskog imenika. On sadrži listu **URL uzoraka** (eng. *URL patterns*) i mapira svaki uzorak na odgovarajući `View`.

### Glavni `urls.py` i `include()`

Kao što smo vidjeli, Django projekt ima glavni `myproject/urls.py`. Dobra praksa, koju preporučuje i "Two Scoops of Django", je da ovaj glavni `urls.py` bude što jednostavniji. Njegova glavna uloga je da preusmjerava zahtjeve na `urls.py` datoteke unutar pojedinih **aplikacija**. To radimo pomoću funkcije `include()`.

    # myproject/urls.py
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('posts/', include('posts.urls')), # Svi URL-ovi koji počinju s 'posts/' idu u posts.urls
    ]

### `urls.py` unutar aplikacije

Unutar naše `posts` aplikacije, kreirat ćemo `posts/urls.py` koji će se baviti samo URL-ovima vezanim za postove.

    # posts/urls.py
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.post_list, name='post-list'),
        path('<int:pk>/', views.post_detail, name='post-detail'),
    ]

* `path('', ...)`: Prazan string odgovara korijenskom URL-u aplikacije (u našem slučaju, `/posts/`). On poziva `post_list` view.
* `path('<int:pk>/', ...)`: Ovo je **dinamički URL**. Dio `<int:pk>` je "hvatač" (eng. *path converter*). On govori Djangu: "Očekuj ovdje cijeli broj (`int`) i proslijedi ga `Viewu` kao argument naziva `pk` (primary key)". Ovo će odgovarati URL-ovima poput `/posts/1/`, `/posts/42/`, itd.

---

## 4.2 Funkcijski bazirani Viewovi (FBV)

Najjednostavniji način za pisanje viewova su obične Python funkcije. Zovu se **Function-Based Views (FBVs)**.

Kreirajmo dva viewa koja smo definirali u `posts/urls.py`. Otvorite `posts/views.py`:

    # posts/views.py
    from django.http import HttpResponse
    from .models import Post

    def post_list(request):
        # Dohvaćamo sve objekte iz Post modela
        svi_postovi = Post.objects.all()

        # Kreiramo jednostavan HTML odgovor za prikaz
        response_html = "<h1>Lista svih postova</h1><ul>"
        for post in svi_postovi:
            response_html += f"<li>{post.title}</li>"
        response_html += "</ul>"

        return HttpResponse(response_html)

    def post_detail(request, pk):
        # Dohvaćamo jedan specifičan post prema njegovom 'pk' (primary key)
        try:
            post = Post.objects.get(pk=pk)
            response_html = f"<h1>{post.title}</h1><p>{post.content}</p>"
            return HttpResponse(response_html)
        except Post.DoesNotExist:
            return HttpResponse("Taj post ne postoji!", status=404)

Sada pokrenite server (`python manage.py runserver`) i posjetite:
* `http://127.0.0.1:8000/posts/` -> Vidjet ćete listu svih postova koje ste unijeli preko shella.
* `http://127.0.0.1:8000/posts/1/` -> Vidjet ćete detalje posta s ID-om 1.

Ovo funkcionira, ali je ružno i nepraktično pisati HTML unutar Pythona. Tu na scenu stupaju **Templatei**.

## 4.3 Prikazivanje Podataka iz Baze u Viewovima pomoću `render()`

Umjesto da vraćamo `HttpResponse` s ručno napisanim HTML-om, koristit ćemo funkciju `render()`. Ona radi tri stvari:
1. Učitava specificirani **Template**.
2. Popunjava ga s podacima koje joj proslijedimo (tzv. **kontekst**).
3. Vraća `HttpResponse` s generiranim HTML-om.

Prvo, moramo stvoriti template datoteke. Unutar `posts` aplikacije, stvorite direktorije `templates/posts/`:

    posts/
    └── templates/
        └── posts/
            ├── post_list.html
            └── post_detail.html

Sada uredimo `posts/views.py` da koristi `render()`:

    # posts/views.py
    from django.shortcuts import render, get_object_or_404
    from .models import Post

    def post_list(request):
        svi_postovi = Post.objects.all()
        context = {
            'posts': svi_postovi
        }
        return render(request, 'posts/post_list.html', context)

    def post_detail(request, pk):
        post = get_object_or_404(Post, pk=pk)
        context = {
            'post': post
        }
        return render(request, 'posts/post_detail.html', context)

* `context`: Ovo je Python rječnik (dictionary) koji mapira imena varijabli koje ćemo koristiti u templateu na stvarne Python objekte.
* `get_object_or_404()`: Ovo je vrlo koristan Djangov prečac. Radi isto što i naš `try/except` blok: pokušava dohvatiti objekt, a ako ne uspije, automatski podiže HTTP 404 grešku.

(Sadržaj template datoteka ćemo detaljnije obraditi u sljedećem poglavlju, ali za sada, zamislite da `post_list.html` sadrži petlju koja prolazi kroz `posts` varijablu, a `post_detail.html` prikazuje `post.title` i `post.content`).

---

## 4.4 Generički Klasni bazirani Viewovi (CBV)

Funkcijski bazirani viewovi su odlični za jedinstvenu logiku. Međutim, mnogi zadaci u web razvoju se ponavljaju: prikaz liste objekata, prikaz detalja jednog objekta, kreiranje objekta putem forme, itd.

Django nudi set pre-izgrađenih viewova, baziranih na klasama, koji enkapsuliraju te uobičajene uzorke. Zovu se **Generic Class-Based Views (CBVs)**.

**Prednosti:**
* **Manje koda:** Rješavaju uobičajene zadatke s vrlo malo koda.
* **DRY (Don't Repeat Yourself):** Ne morate iznova pisati istu logiku za dohvaćanje objekata.
* **Proširivost:** Lako možete naslijediti generički view i nadjačati samo one dijelove koji su vam potrebni.

Prepravimo naša dva viewa koristeći CBVs. U `posts/views.py`:

    # posts/views.py
    from django.views.generic import ListView, DetailView
    from .models import Post

    class PostListView(ListView):
        model = Post
        template_name = 'posts/post_list.html'
        context_object_name = 'posts'

    class PostDetailView(DetailView):
        model = Post
        template_name = 'posts/post_detail.html'
        context_object_name = 'post'

Sada moramo ažurirati naš `posts/urls.py` da poziva ove klase. Važno je pozvati `.as_view()` metodu na klasi:

    # posts/urls.py
    from django.urls import path
    from .views import PostListView, PostDetailView

    urlpatterns = [
        path('', PostListView.as_view(), name='post-list'),
        path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    ]

I to je to! S ovim kodom postigli smo potpuno istu funkcionalnost kao i s FBV-ima, ali na strukturiraniji i sažetiji način.

* `ListView` automatski dohvaća sve objekte iz navedenog `model`-a i prosljeđuje ih u `template_name` pod imenom definiranim u `context_object_name`.
* `DetailView` radi isto, ali dohvaća samo jedan objekt na temelju `pk` ili `slug` argumenta iz URL-a.

FBV ili CBV? "Two Scoops of Django" preporučuje korištenje CBV-a za sve uobičajene CRUD (Create, Retrieve, Update, Delete) operacije, a FBV-a za kompleksnu logiku koja ne spada u te kalupe.

---

U ovom poglavlju smo prešli put od URL zahtjeva do logike u viewu. Naučili smo kako Django mapira URL-ove na viewove i kako viewovi koriste modele za dohvaćanje podataka. Sada smo spremni za posljednji dio MVT slagalice: kako te podatke elegantno prikazati korisniku pomoću **Templatea**.