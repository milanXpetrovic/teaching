---
parent: 'Naprednije Teme za Kompletnog Django Developera'
nav_order: 3
has_children: false
title: 'Poglavlje 12: Sigurnost i Optimizacija'
---

# Poglavlje 12: Sigurnost i Optimizacija

Izgradili smo funkcionalnu aplikaciju. Ona radi. Ali, je li **sigurna**? Je li **brza**?

U ovom naprednom poglavlju, fokusirat ćemo se na dvije ključne teme koje dolaze do izražaja kada aplikacija pređe iz razvojne faze u stvarni svijet: osiguravanje od napada i optimizacija performansi. Mnoge od ovih preporuka su direktno inspirirane najboljim praksama iz knjige "Two Scoops of Django".

---

## 12.1 Sigurnosne Dobre Prakse

Django ima reputaciju vrlo sigurnog frameworka, i to s pravom. Dolazi s ugrađenom zaštitom od mnogih čestih web napada. Međutim, ta zaštita radi samo ako je ispravno koristimo. Sigurnost je proces, ne samo značajka.

### 1. Upravljanje `SECRET_KEY`-om: Nikad u Gitu!

U `settings.py` se nalazi `SECRET_KEY`. Ova varijabla je ključna za mnoge Djangove sigurnosne mehanizme, uključujući potpisivanje kolačića (cookies) i generiranje CSRF tokena.

**Pravilo:** `SECRET_KEY` **NIKADA** ne smije biti javan niti spremljen u Git repozitorij. Ako napadač dođe do vašeg `SECRET_KEY`-a, može lažirati kolačiće, preuzeti sesije korisnika i napraviti veliku štetu.

**Rješenje: Okolišne Varijable (Environment Variables)**

Najbolja praksa je čitati `SECRET_KEY` (i druge osjetljive podatke poput lozinki za bazu) iz okolišnih varijabli.

1.  **Instalirajte `python-decouple`:**
    Ovo je korisna biblioteka koja olakšava rad s okolišnim varijablama i `.env` datotekama.

        pip install python-decouple

2.  **Kreirajte `.env` datoteku:**
    U korijenu projekta (gdje je `manage.py`), stvorite datoteku `.env` i u nju spremite svoj ključ:

        SECRET_KEY=vas-izuzetno-dugacak-i-nasumican-kljuc

3.  **Dodajte `.env` u `.gitignore`:**
    **Ovo je ključan korak!** Osigurajte da ova datoteka nikada ne završi u Gitu.

        # .gitignore
        .env

4.  **Prilagodite `settings.py`:**
    Sada, umjesto hardkodiranog ključa, čitajte ga iz okoline:

        # settings.py
        from decouple import config

        # ...
        SECRET_KEY = config('SECRET_KEY')

### 2. Isključite `DEBUG` mod u produkciji

Već smo spomenuli, ali vrijedi ponoviti:

    DEBUG = False

Kada je `DEBUG = True`, Djangova "žuta stranica" otkriva ogromnu količinu informacija o vašoj aplikaciji – kod, postavke, putanje. To je neprocjenjivo za razvoj, ali katastrofalno za sigurnost u produkciji.

### 3. HTTPS Svugdje

U današnje vrijeme, **svaka** produkcijska stranica mora koristiti HTTPS. On enkriptira sav promet između korisnika i vašeg servera, štiteći podatke od prisluškivanja. U `settings.py`, uključite ove postavke da osigurate da se kolačići šalju samo preko sigurne veze:

    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

### 4. Djangov Sigurnosni Checklist

Django dolazi s ugrađenom naredbom koja provjerava vaš projekt na uobičajene sigurnosne propuste. Povremeno je pokrenite prije deploymenta:

    python manage.py check --deploy

Ova naredba će vas upozoriti ako je `DEBUG` `True`, ako `SECRET_KEY` nije postavljen sigurno, i na mnoge druge potencijalne probleme.

---

## 12.2 Optimizacija Performansi

Kada vaša aplikacija dobije više korisnika i više podataka, brzina može postati problem. Spora aplikacija vodi do lošeg korisničkog iskustva. Optimizacija je proces pronalaženja i uklanjanja "uskih grla" (bottlenecks).

### 1. Problem N+1 Upita: `select_related` i `prefetch_related`

Ovo je **najčešći** problem s performansama u Django aplikacijama.

**Scenarij:** Imate listu od 100 postova i za svaki post želite prikazati korisničko ime autora.

*   **Loš način (N+1 problem):**

        # views.py
        posts = Post.objects.all() # 1 UPIT za sve postove

        # templates/post_list.html
        {% for post in posts %}
            <p>{{ post.title }} - {{ post.author.username }}</p> <!-- N UPITA (jedan po postu za dohvaćanje autora) -->
        {% endfor %}

    Rezultat: **101** upit na bazu podataka! Ovo je izuzetno neefikasno.

**Rješenje:** Recite Djangu unaprijed koje povezane objekte da dohvati.

*   **`select_related()` (za ForeignKey i OneToOneField):**
    Koristi `JOIN` u SQL-u da dohvati povezane objekte u **jednom, jedinom upitu**.

        # views.py - ISPRAVAN NAČIN
        posts = Post.objects.select_related('author').all() # SAMO 1 UPIT za sve!

*   **`prefetch_related()` (za ManyToManyField i obrnute ForeignKey veze):**
    Radi sličnu stvar, ali u **dva upita** (jedan za glavne objekte, jedan za povezane), što je i dalje neusporedivo bolje od N+1.

        # views.py
        posts = Post.objects.prefetch_related('tags').all() # 2 UPITA, bez obzira na broj postova

### 2. Django Debug Toolbar

Kako uopće znati koliko upita vaša stranica radi? Ne možete optimizirati ono što ne mjerite.

**Django Debug Toolbar** je nezaobilazan alat za razvoj.

1.  **Instalacija:**

        pip install django-debug-toolbar

2.  **Konfiguracija:** Slijedite upute za instalaciju u `settings.py` i `urls.py` (zahtijeva nekoliko koraka).

Kada je postavljen, na desnoj strani ekrana u razvoju pojavit će se plutajući panel. Klikom na "SQL" tab, vidjet ćete **svaki pojedini SQL upit** koji je vaša stranica izvršila, koliko ih je bilo, i koliko je svaki trajao. Ovo je najbolji alat za otkrivanje N+1 problema.

### 3. Caching (Predmemoriranje)

Neke operacije su jednostavno spore – kompleksni upiti, izračuni, renderiranje dijelova stranice. Ako se rezultat tih operacija ne mijenja često, nema smisla ponavljati ih za svakog korisnika.

Rješenje je **caching** – spremanje rezultata skupe operacije u brzu memoriju (poput Memcacheda ili Redisa) na određeno vrijeme.

Django ima robustan i fleksibilan cache framework. Možete keširati:
*   **Cijelu stranicu:** Ako se stranica rijetko mijenja.
*   **Dijelove templatea:** Pomoću `{% cache %}` taga.
*   **Rezultate funkcija:** Ručno, koristeći low-level cache API.

**Primjer keširanja dijela templatea:**

    {% load cache %}

    {% cache 600 sidebar %}
        <!--
            Ovaj dio će se izvršiti samo jednom u 10 minuta (600 sekundi).
            Svi ostali korisnici će dobiti spremljenu (keširanu) verziju.
            Idealno za dijelove stranice koji su isti za sve korisnike.
        -->
        <h3>Najpopularniji postovi</h3>
        <ul>...</ul>
    {% endcache %}

### 4. Optimizacija slika i statičkih datoteka

Velike, neoptimizirane slike su čest uzrok sporog učitavanja stranica. Uvijek se pobrinite da su slike:
*   **Komprimirane:** Koristite alate poput `ImageOptim` ili online servise.
*   **Ispravne veličine:** Nemojte učitavati sliku od 4000px pa je smanjivati u CSS-u na 400px.
*   **Poslužene u modernim formatima:** Poput WebP-a, gdje je to moguće.

Slično vrijedi i za CSS i JavaScript. Alati poput `django-compressor` ili moderni front-end build procesi mogu automatski **minificirati** (ukloniti nepotrebne razmake) i **spojiti** više datoteka u jednu, smanjujući broj HTTP zahtjeva.

---

Sigurnost i performanse su duboke teme, ali primjenom ovih osnovnih praksi, vaša Django aplikacija će biti znatno robusnija, sigurnija i brža. Uvijek razmišljajte o ovim aspektima tijekom razvoja, a ne tek kada se pojavi problem.