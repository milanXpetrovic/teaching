---
parent: 'Srce Djanga: Modeli, Viewovi, Templatei (MVT)'
nav_order: 4
title: 'Projekt: Izgradnja jednostavne Blog aplikacije'
---

# Samostalni Projekt: Izgradnja jednostavne Blog aplikacije

Do sada smo prošli kroz temeljne komponente Djanga: Modele, Viewove, Template i URL-ove. Sada je vrijeme da sve to znanje spojimo i samostalno izgradimo funkcionalnu, iako jednostavnu, web aplikaciju.

**Cilj projekta:** Napraviti jednostavnu blog aplikaciju koja omogućuje prikaz svih postova i detaljan prikaz pojedinog posta.

Ovaj projekt će vas provesti kroz cijeli razvojni ciklus jedne Django funkcionalnosti, od baze podataka do korisničkog sučelja.

---

## Priprema Projekta

Ako već niste, slijedite korake iz prethodnih poglavlja:

1. Kreirajte novi Django projekt (npr. naziva `myblog`).
2. Unutar projekta, kreirajte novu aplikaciju naziva `posts`.
3. Ne zaboravite dodati `'posts.apps.PostsConfig'` u `INSTALLED_APPS` unutar `settings.py`.
4. Konfigurirajte URL-ove tako da glavni `urls.py` projekta uključuje `urls.py` iz aplikacije `posts` (npr. na putanji `''`).

## Faza 1: Modeliranje Podataka

Naš blog treba negdje spremati postove. Definirat ćemo model koji će opisivati strukturu jednog posta.

**Zadatak:**

1. Otvorite `posts/models.py`.
2. Importajte `User` model iz `django.contrib.auth.models` jer će svaki post imati autora.
3. Kreirajte klasu `Post` koja nasljeđuje `models.Model`.
4. Dodajte sljedeća polja u `Post` model:
    * `title`: `CharField` s maksimalnom duljinom od 200 znakova.
    * `content`: `TextField` za duži sadržaj posta.
    * `date_posted`: `DateTimeField` koji će automatski spremiti trenutni datum i vrijeme **samo prilikom prvog kreiranja** objekta. (Istražite opcije `auto_now` i `auto_now_add`).
    * `author`: `ForeignKey` veza prema `User` modelu. Razmislite što bi se trebalo dogoditi s postovima ako se autor obriše (koja `on_delete` opcija je najlogičnija?).
5. Definirajte `__str__` metodu koja će vraćati naslov (`title`) posta.

Nakon što ste definirali model, ne zaboravite **kreirati i primijeniti migracije**:

    python manage.py makemigrations
    python manage.py migrate

## Faza 2: Django Admin

Najbrži način da unesemo nekoliko testnih postova u našu bazu je putem Djangovog admin sučelja.

**Zadatak:**

1. Kreirajte superusera (administratora) kako biste se mogli prijaviti u admin sučelje:

        python manage.py createsuperuser

    Pratite upute za unos korisničkog imena, emaila i lozinke.

2. Otvorite `posts/admin.py`.
3. Registrirajte svoj `Post` model kako bi postao vidljiv u admin sučelju.
4. Pokrenite server (`python manage.py runserver`) i posjetite `http://127.0.0.1:8000/admin/`.
5. Prijavite se s podacima koje ste upravo kreirali.
6. Unutar admin sučelja, **kreirajte 2-3 primjera postova**. Za autora odaberite superusera kojeg ste kreirali.

## Faza 3: Prikazivanje Podataka (Viewovi i Templatei)

Sada kada imamo podatke u bazi, vrijeme je da ih prikažemo korisnicima. Kreirat ćemo dvije stranice: jednu za prikaz liste svih postova i drugu za prikaz detalja pojedinog posta.

**Zadatak:**

1. **Kreirajte Template strukturu:**
    * U korijenu projekta stvorite `templates` direktorij. Unutar njega, stvorite `base.html`.
    * Definirajte osnovni HTML kostur u `base.html` s `{% block content %}` unutar `<body>` taga.
    * Unutar `posts` aplikacije, stvorite direktorije `templates/posts/`.
    * Unutar `posts/templates/posts/` stvorite dvije prazne datoteke: `post_list.html` i `post_detail.html`.

2. **View za listu postova (`PostListView`):**
    * U `posts/views.py`, kreirajte klasni view `PostListView` koji nasljeđuje `ListView`.
    * Povežite ga s `Post` modelom.
    * Definirajte `template_name` da pokazuje na `posts/post_list.html`.
    * Postavite `context_object_name` na `'posts'` radi lakšeg korištenja u templateu.
    * **Bonus:** Poredajte postove od najnovijeg prema najstarijem. (Istražite `ordering` atribut u `ListView` ili `Meta` klasu u modelu).

3. **Template za listu postova (`post_list.html`):**
    * U `post_list.html`, naslijedite `base.html`.
    * Unutar `{% block content %}`, prođite kroz `posts` listu (kontekst varijablu) koristeći `{% for %}` petlju.
    * Za svaki `post` u petlji, prikažite njegov naslov, autora (`post.author.username`) i datum objave. Naslov posta neka bude link koji vodi na detaljni prikaz tog posta. (Savjet: Trebat će vam `{% url %}` tag i `post.id` ili `post.pk`).

4. **View za detalje posta (`PostDetailView`):**
    * U `posts/views.py`, kreirajte `PostDetailView` koji nasljeđuje `DetailView`.
    * Povežite ga s `Post` modelom i `posts/post_detail.html` templateom.
    * Postavite `context_object_name` na `'post'`.

5. **Template za detalje posta (`post_detail.html`):**
    * U `post_detail.html`, naslijedite `base.html`.
    * Unutar `{% block content %}`, prikažite sve detalje `post` objekta: naslov (`post.title`), sadržaj (`post.content`), autora i datum.

## Faza 4: Povezivanje URL-ova

Na kraju, moramo povezati naše nove viewove s URL-ovima.

**Zadatak:**

1. Otvorite `posts/urls.py`.
2. Kreirajte dva URL uzorka:
    * Jedan za korijenski URL aplikacije (`''`) koji pokazuje na `PostListView`. Dajte mu `name='post-list'`.
    * Jedan dinamički URL za detalje posta koji hvata integer `pk` (npr. `post/<int:pk>/`). Neka pokazuje na `PostDetailView`. Dajte mu `name='post-detail'`.

---

### Završna provjera

Pokrenite server i testirajte funkcionalnost:

* Posjetite `http://127.0.0.1:8000/`. Trebali biste vidjeti listu svih postova koje ste unijeli.
* Kliknite na naslov bilo kojeg posta. URL bi se trebao promijeniti (npr. u `/post/1/`) i trebali biste vidjeti detaljan prikaz samo tog posta.

**Čestitamo!** Uspješno ste izgradili temeljnu funkcionalnost blog aplikacije i primijenili sve ključne koncepte MVT arhitekture. Ovaj projekt je odlična osnova na koju možete nadograđivati nove funkcionalnosti poput kreiranja postova s web forme, uređivanja, brisanja, komentara i još mnogo toga.