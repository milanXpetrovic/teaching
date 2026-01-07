---
parent: 'Srce Djanga: Modeli, Viewovi, Templatei (MVT)'
nav_order: 1
has_children: false
title: 'Poglavlje 3: Modeli i Baze Podataka (ORM)'
---

# Poglavlje 3: Modeli i Baze Podataka (ORM)

Dobrodošli u srce svake dinamičke web aplikacije – podatke. U ovoj cjelini, naučit ćemo kako Django pristupa, strukturira i upravlja podacima pomoću jednog od svojih najmoćnijih alata: **Object-Relational Mappera (ORM)**.

## 3.1 Uvod u Django ORM: Podaci kao Python Objekti

Većina web aplikacija treba spremati podatke u bazu podataka (npr. PostgreSQL, MySQL, SQLite). Tradicionalni način za to je pisanje SQL upita:

`SELECT * FROM posts WHERE author_id = 5;`

Pisanje SQL-a može biti zamorno, podložno greškama (SQL Injection!) i ovisno o specifičnoj bazi podataka koju koristite.

**Django ORM** rješava taj problem. On je moćan "prevoditelj" koji vam omogućuje da radite s bazom podataka koristeći jednostavan, intuitivan Python kod.

**Kako to radi?**

* **Vi pišete Python:** Definirate strukturu podataka kao Python klasu.
* **Django radi SQL:** ORM automatski prevodi vaš Python kod u optimizirane SQL upite.

**Glavne prednosti:**

* **Brži razvoj:** Pisanje Pythona je brže i jednostavnije od pisanja SQL-a.
* **Sigurnost:** ORM automatski "čisti" vaše upite i štiti vas od SQL injection napada.
* **Neovisnost o bazi:** Isti Python kod će raditi na PostgreSQL-u, MySQL-u, SQLite-u itd. Ako jednog dana odlučite promijeniti bazu, ne morate mijenjati svoj kod.

---

## 3.2 Definiranje Modela

Središnji dio ORM-a je **Model**. Model je Python klasa koja predstavlja jednu tablicu u vašoj bazi podataka.

Kreirajmo prvi model za našu blog aplikaciju. Želimo spremati postove, a svaki post treba imati naslov, sadržaj i datum kreiranja.

Otvorite datoteku `posts/models.py` i upišite sljedeći kod:

    # posts/models.py
    from django.db import models
    from django.utils import timezone

    class Post(models.Model):
        title = models.CharField(max_length=200)
        content = models.TextField()
        created_at = models.DateTimeField(default=timezone.now)

        def __str__(self):
            return self.title

### Anatomija Modela

* `class Post(models.Model):`
    Svaki Django model je Python klasa koja nasljeđuje `django.db.models.Model`.
* `title`, `content`, `created_at`:
    Ovo su **polja** (eng. *fields*) modela. Svako polje predstavlja jedan stupac u tablici baze podataka.
* `models.CharField`, `models.TextField`, `models.DateTimeField`:
    Ovo su **tipovi polja**. Django nudi širok spektar tipova polja za različite vrste podataka (tekst, brojevi, datumi, email adrese, itd.).
* `max_length=200`:
    Ovo je **opcija polja**. `CharField` (kratki tekst) zahtijeva da mu definiramo maksimalnu duljinu.
* `default=timezone.now`:
    Ova opcija postavlja zadanu vrijednost polja na trenutni datum i vrijeme kada se objekt kreira.
* `def __str__(self):`
    Ovo je standardna Python metoda. U kontekstu Djanga, izuzetno je važna jer definira "čitljiv" prikaz objekta. Kada negdje (npr. u admin sučelju) zatražimo prikaz `Post` objekta, vidjet ćemo njegov naslov, a ne nešto nečitljivo poput `<Post object (1)>`.

---

## 3.3 Migracije: Sinkronizacija Modela i Baze

Nakon što smo definirali naš model u Pythonu, moramo reći bazi podataka da stvori tablicu koja odgovara toj strukturi. Taj proces se zove **migracija** i sastoji se od dva koraka.

> **Analogija:** Zamislite da gradite kuću.
>
> 1. **Nacrt:** Prvo arhitekt napravi detaljan nacrt (`makemigrations`).
> 2. **Izgradnja:** Zatim građevinari uzmu taj nacrt i po njemu izgrade kuću (`migrate`).

### Korak 1: Stvaranje nacrta (`makemigrations`)

Ova naredba uspoređuje stanje vaših `models.py` datoteka sa stanjem migracijskih datoteka i automatski generira "nacrt" promjena.

U terminalu, unutar korijena projekta, pokrenite:

    python manage.py makemigrations

Django će detektirati da ste stvorili novi `Post` model i generirati novu datoteku unutar `posts/migrations/` direktorija, najčešće nazvanu `0001_initial.py`. Ta datoteka sadrži Python kod koji opisuje kako stvoriti `posts_post` tablicu.

### Korak 2: Primjena nacrta na bazu (`migrate`)

Sada kada imamo nacrt, vrijeme je da ga primijenimo na bazu podataka.

    python manage.py migrate

Ova naredba će proći kroz sve migracijske datoteke koje još nisu primijenjene i izvršiti potrebne SQL naredbe na bazi. Nakon ovoga, u vašoj bazi podataka (trenutno `db.sqlite3` datoteka) postoji tablica `posts_post` sa stupcima `id`, `title`, `content` i `created_at`.

> **Važno:** Svaki put kada napravite bilo kakvu promjenu na vašim modelima (dodate novo polje, obrišete staro, promijenite opcije), **morate ponoviti ovaj proces od dva koraka:** `makemigrations` pa `migrate`.

---

## 3.4 Interakcija s Bazom: Django Shell

Kako možemo raditi s podacima sada kada tablica postoji? Django nudi interaktivnu konzolu, **shell**, koja je idealna za testiranje i rad s podacima.

Pokrenite shell naredbom:

    python manage.py shell

Ovo otvara Python konzolu koja je već konfigurirana za rad s vašim projektom.

### CRUD Operacije (Create, Retrieve, Update, Delete)

Unutar shella, možemo izvoditi osnovne operacije s podacima.

1. **Importajmo naš model:**

        from posts.models import Post

2. **Create (Stvaranje):** Stvorimo novi post.

        post1 = Post(title="Moj prvi post", content="Ovo je sadržaj prvog posta.")
        post1.save()

3. **Retrieve (Dohvaćanje):** Dohvatimo sve postove iz baze. Svaki model ima `objects` manager preko kojeg radimo upite.

        svi_postovi = Post.objects.all()
        print(svi_postovi)

    Dohvatimo jedan specifičan post:

        prvi_post = Post.objects.get(id=1)
        print(prvi_post.title)

4. **Update (Ažuriranje):** Promijenimo naslov prvog posta.

        prvi_post.title = "Novi, bolji naslov"
        prvi_post.save()

5. **Delete (Brisanje):** Obrišimo post.

        prvi_post.delete()

Iza svake od ovih naredbi, Django ORM je generirao i izvršio odgovarajuću SQL naredbu (`INSERT`, `SELECT`, `UPDATE`, `DELETE`).

---

## 3.5 Relacije među Modelima

Rijetko kada podaci stoje izolirano. Obično su povezani. Naš blog bi bio puno korisniji da znamo tko je autor posta, i da postove možemo kategorizirati pomoću tagova.

Django podržava sve standardne relacije iz svijeta baza podataka.

### `ForeignKey` (Veza "više-na-jedan")

Ovo je najčešća veza. Koristimo je kada jedan objekt može biti povezan s više drugih, ali ne i obrnuto. Npr. **jedan autor može imati više postova**, ali jedan post ima samo jednog autora.

Proširimo naš `Post` model. Pretpostavit ćemo da koristimo Djangov ugrađeni `User` model.

    # posts/models.py
    from django.db import models
    from django.utils import timezone
    from django.contrib.auth.models import User # Importamo User model

    class Post(models.Model):
        title = models.CharField(max_length=200)
        content = models.TextField()
        created_at = models.DateTimeField(default=timezone.now)
        author = models.ForeignKey(User, on_delete=models.CASCADE) # Dodano polje

        def __str__(self):
            return self.title

* `models.ForeignKey(User, ...)`: Definira vezu prema `User` modelu.
* `on_delete=models.CASCADE`: Ovo je važno! Govori bazi što da radi s postovima ako se autor obriše. `CASCADE` znači "obriši i sve postove ovog autora".

### `ManyToManyField` (Veza "više-na-više")

Koristimo je kada više objekata jedne vrste može biti povezano s više objekata druge vrste. Npr. **jedan post može imati više tagova**, i **jedan tag može biti dodijeljen na više postova**.

Stvorimo `Tag` model i povežimo ga s `Post` modelom.

    # posts/models.py
    # ... (prethodni importi)

    class Tag(models.Model):
        name = models.CharField(max_length=50)

        def __str__(self):
            return self.name

    class Post(models.Model):
        # ... (prethodna polja)
        tags = models.ManyToManyField(Tag, blank=True)

* `models.ManyToManyField(Tag)`: Definira vezu. Django će automatski stvoriti pomoćnu (tzv. *junction*) tablicu u bazi koja će povezivati postove i tagove.

### `OneToOneField` (Veza "jedan-na-jedan")

Koristimo je kada jedan objekt može biti povezan s točno jednim drugim objektom. Često se koristi za proširivanje postojećih modela. Npr., želimo za svakog korisnika (`User`) spremiti dodatne informacije (slika, biografija), ali ne želimo dirati ugrađeni `User` model. **Jedan korisnik ima točno jedan profil**.

    # users/models.py (primjer u novoj 'users' aplikaciji)
    from django.db import models
    from django.contrib.auth.models import User

    class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        bio = models.TextField(blank=True)
        profile_picture = models.ImageField(upload_to='profile_pics', blank=True)

        def __str__(self):
            return f'{self.user.username} Profile'

Nakon svake od ovih promjena, ne zaboravite pokrenuti `makemigrations` i `migrate`!

---

Savladali ste osnove rada s podacima u Djangu. Razumijevanje modela i relacija je temelj na kojem ćemo graditi sve ostalo: logiku u *viewovima* i prikaz u *templateima*.
