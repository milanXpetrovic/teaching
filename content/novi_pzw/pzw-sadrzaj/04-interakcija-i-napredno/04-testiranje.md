---
parent: 'Interakcija s Korisnikom i Napredne Teme'
nav_order: 4
has_children: false
title: 'Poglavlje 9: Testiranje'
---

# Poglavlje 9: Testiranje

"Moj kod radi, probao sam ga u pregledniku."

Ovo je rečenica koju svaki developer izgovori, ali ona, nažalost, nije ni blizu dovoljna za izgradnju stabilne i pouzdane aplikacije. Ručno testiranje je sporo, podložno ljudskim greškama i ne garantira da promjena na jednom mjestu nije slomila nešto naizgled nepovezano na drugom.

Rješenje je **automatizirano testiranje** – pisanje koda koji testira vaš kod.

## 9.1 Zašto uopće testirati?

Pisanje testova se na početku može činiti kao dodatan, spor i nepotreban posao. Međutim, dugoročno, ono je jedna od najboljih investicija koje možete uložiti u svoj projekt.

* **Pouzdanost (Confidence):** Kada imate dobar set testova, možete raditi promjene i refaktorirati kod sa sigurnošću da niste ništa slomili. Ako testovi prođu, vaša aplikacija vjerojatno i dalje radi ispravno.
* **Sprječavanje regresija:** Regresija je greška (bug) koja se ponovno pojavi u kodu koji je nekada radio. Dobar test koji je "uhvatio" grešku osigurava da se ta ista greška više nikada ne vrati.
* **Bolji dizajn koda:** Pisanje koda koji se može testirati često vas prisili na bolju organizaciju i modularniji dizajn. Ako je nešto teško testirati, vjerojatno je previše kompleksno ili loše strukturirano.
* **Živuća dokumentacija:** Testovi služe kao izvršna dokumentacija. Gledajući testove za određenu funkciju, možete točno vidjeti kako se ona treba ponašati u različitim situacijama.

> **Two Scoops Savjet:** "Testiranje nije opcija, ono je dio posla." Profesionalni developeri pišu testove. Usvajanje te navike od samog početka je ono što razlikuje amatera od profesionalca.

---

## 9.2 Djangov Testni Okvir

Django dolazi s moćnim testnim okvirom koji se temelji na standardnoj Pythonovoj `unittest` biblioteci. On proširuje `unittest` s nizom alata specifičnih za web razvoj.

### Struktura testova

* Kada kreirate aplikaciju, Django automatski stvori datoteku `tests.py`.
* Dobra praksa za veće aplikacije je zamijeniti tu datoteku s **`tests/` paketom** (direktorijem s `__init__.py` datotekom). Unutar tog paketa, testove organiziramo po namjeni: `test_models.py`, `test_views.py`, `test_forms.py`, itd.

### Pokretanje testova

Testove pokrećemo jednostavnom `manage.py` naredbom:

    # Pokreni sve testove u svim aplikacijama
    python manage.py test

    # Pokreni testove samo za 'posts' aplikaciju
    python manage.py test posts

    # Pokreni specifičnu testnu klasu
    python manage.py test posts.tests.test_models.PostModelTests

### `django.test.TestCase`

Ovo je osnovna klasa koju ćete najčešće nasljeđivati za pisanje testova. Ona je posebna jer:
* **Stvara privremenu, čistu bazu podataka** za svaki testni ciklus, osiguravajući da su testovi izolirani.
* Dolazi s ugrađenim **testnim klijentom** (`self.client`) koji simulira web preglednik, omogućujući nam da "posjećujemo" URL-ove i testiramo viewove.

---

## 9.3 Testiranje Modela

Testiranje modela se fokusira na provjeru prilagođene logike koju ste dodali: `__str__` metode, `get_absolute_url`, prilagođene metode ili validacijska pravila.

**Primjer za `posts/tests/test_models.py`:**

    from django.test import TestCase
    from django.contrib.auth.models import User
    from ..models import Post

    class PostModelTests(TestCase):
        
        @classmethod
        def setUpTestData(cls):
            # setUpTestData se izvršava JEDNOM na početku za cijelu klasu.
            # Idealno je za stvaranje objekata koji se neće mijenjati.
            cls.user = User.objects.create_user(username='testuser', password='password')
            cls.post = Post.objects.create(
                title="Testni Naslov",
                content="Neki sadržaj.",
                author=cls.user
            )

        def test_model_content(self):
            self.assertEqual(self.post.title, "Testni Naslov")
            self.assertEqual(self.post.content, "Neki sadržaj.")
            self.assertEqual(self.post.author.username, 'testuser')

        def test_str_representation(self):
            # Provjeravamo vraća li __str__ metoda ispravno naslov.
            self.assertEqual(str(self.post), "Testni Naslov")

---

## 9.4 Testiranje Viewova i URL-ova

Testiranje viewova je ključno. Ovdje provjeravamo:
1. Vraća li određeni URL ispravan statusni kod (npr. 200 OK, 404 Not Found, 302 Redirect).
2. Koristi li view ispravan template.
3. Sadrži li odgovor očekivani sadržaj.
4. Ponaša li se view ispravno za prijavljene i neprijavljene korisnike.

**Primjer za `posts/tests/test_views.py`:**

    from django.test import TestCase, Client
    from django.urls import reverse
    from ..models import Post
    from django.contrib.auth.models import User

    class PostViewTests(TestCase):

        @classmethod
        def setUpTestData(cls):
            cls.user = User.objects.create_user(username='testuser', password='password')
            cls.post = Post.objects.create(
                title="Testni Naslov",
                content="Neki sadržaj.",
                author=cls.user
            )

        def test_post_list_view(self):
            # Koristimo reverse() da dobijemo URL iz njegovog imena
            url = reverse('post-list')
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'posts/post_list.html')
            self.assertContains(response, "Testni Naslov")

        def test_post_detail_view(self):
            url = reverse('post-detail', args=[self.post.pk])
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'posts/post_detail.html')
            self.assertContains(response, "Neki sadržaj.")
            self.assertNotContains(response, "Ovo ne bi smjelo biti ovdje.")

---

## 9.6 Testiranje Formi

Kod formi, najvažnije je testirati **validaciju**. Želimo biti sigurni da naša forma ispravno prihvaća valjane podatke i ispravno odbija nevaljane.

**Primjer za `posts/tests/test_forms.py`:**

    from django.test import TestCase
    from ..forms import PostForm

    class PostFormTests(TestCase):
        
        def test_post_form_valid_data(self):
            form_data = {'title': 'Validan Naslov', 'content': 'Neki sadržaj.'}
            form = PostForm(data=form_data)
            self.assertTrue(form.is_valid())

        def test_post_form_no_data(self):
            form = PostForm(data={})
            self.assertFalse(form.is_valid())
            # Provjeravamo da imamo greške na 2 polja
            self.assertEqual(len(form.errors), 2)

---

## 9.7 Fixture i `factory-boy`: Generiranje Testnih Podataka

Ponekad su vam za testiranje potrebne kompleksnije početne postavke podataka.

* **Fixture:** Djangov ugrađeni mehanizam za učitavanje predefiniranih podataka iz datoteka (npr. JSON, YAML). Mogu biti korisni, ali "Two Scoops of Django" upozorava da mogu postati teški za održavanje kako se model mijenja.

* **`factory-boy` (Preporučeni pristup):** Vanjska biblioteka (`pip install factory-boy`) koja vam omogućuje da definirate "tvornice" za vaše modele. To je puno fleksibilniji i moćniji način za generiranje testnih podataka u Pythonu.

**Primjer s `factory-boy`:**

1. Definirate tvornicu:

        # posts/factories.py
        import factory
        from .models import Post, User

        class UserFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = User
            username = factory.Faker('user_name')

        class PostFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = Post
            title = factory.Faker('sentence')
            content = factory.Faker('text')
            author = factory.SubFactory(UserFactory)

2. Koristite je u testovima:

        # posts/tests/test_views.py
        from .factories import PostFactory

        class SomeOtherTests(TestCase):
            def setUp(self):
                # Stvara post i automatski stvara i povezuje korisnika!
                self.post1 = PostFactory()
                self.post2 = PostFactory(title="Specifičan naslov")
            
            def test_something(self):
                self.assertEqual(Post.objects.count(), 2)

---

Testiranje je ogromna tema, ali ovo su temelji. Započnite pisanjem jednostavnih testova za vaše modele i viewove. S vremenom, kako vaša aplikacija raste, vaši testovi će postajati složeniji i, što je najvažnije, postat će vaša sigurnosna mreža koja vam omogućuje da razvijate brže i sa više samopouzdanja.