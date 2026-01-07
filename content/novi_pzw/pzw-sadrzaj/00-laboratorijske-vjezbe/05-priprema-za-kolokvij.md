Naravno, izrada kvalitetnih pripremnih materijala za ispit je ključna. Pripremio sam sveobuhvatnu skriptu koja pokriva sve navedene teme.

Struktura je osmišljena tako da studentima pruži jasan pregled gradiva, istakne najvažnije koncepte koje moraju znati i ponudi im konkretna pitanja za samoprovjeru. Svaka cjelina sadrži i izravne poveznice na detaljnija objašnjenja koja smo prethodno generirali, čineći ovo idealnim sažetkom za učenje.

Evo prijedloga `.md` datoteke za pripremu ispita.

---
---
parent: 'Ispitni Materijali'
nav_order: 1
title: 'Priprema za Ispit: Osnove Djanga'
---

# Priprema za Ispit: Osnove Djanga

Ovaj dokument služi kao sažetak ključnog gradiva i vodič za pripremu ispita iz osnova Django frameworka. Cilj je da vam pomogne strukturirati učenje, ponoviti najvažnije koncepte i provjeriti vlastito znanje.

### Kako koristiti ovaj vodič?
1.  **Prođite kroz svaku cjelinu:** Za svaku cjelinu, prvo pročitajte sažetak kako biste se podsjetili o čemu se radi.
2.  **Pregledajte Ključne Koncepte:** Ovo je vaša "checklist-a". Morate biti u stanju objasniti svaki od navedenih pojmova.
3.  **Odgovorite na Pitanja za Provjeru:** Pokušajte usmeno ili pismeno odgovoriti na postavljena pitanja bez gledanja u materijale. Ako niste sigurni, to je znak da trebate ponoviti taj dio gradiva.
4.  **Koristite Poveznice:** Ako zapnete na nekom konceptu ili pitanju, koristite priložene poveznice za povratak na detaljnije objašnjenje u skripti.

---

## 1. Uvod i Razvojno Okruženje

Ova cjelina pokriva temelje potrebne za početak bilo kakvog rada u Djangu. Bez ispravno postavljenog okruženja, ne možemo ni napisati prvu liniju koda.

### Ključni Koncepti:
*   Što je Django i njegova "batteries-included" filozofija.
*   Virtualna okruženja (`venv`): zašto su važna i kako ih koristiti.
*   `pip` i `requirements.txt`: instalacija paketa i upravljanje zavisnostima.
*   Naredbe: `python -m venv venv`, `source venv/bin/activate`, `deactivate`, `pip install`, `pip freeze`.
*   Naredbe: `django-admin startproject`, `python manage.py runserver`.
*   Razlika između **projekta** i **aplikacije**.
*   Struktura Django projekta (`manage.py`, `settings.py`, `urls.py`).
*   Struktura Django aplikacije (`models.py`, `views.py`, `admin.py`, `apps.py`).
*   `INSTALLED_APPS`: Kako i zašto registriramo aplikacije.

### Pitanja za Provjeru Znanja:
1.  Zašto koristimo virtualna okruženja? Kakav problem ona rješavaju?
2.  Koja je razlika između `django-admin startproject myproject` i `django-admin startproject myproject .`? Koji je pristup preporučen i zašto?
3.  Objasnite ulogu `manage.py` datoteke.
4.  Što je `INSTALLED_APPS` i zašto je važno dodati novu aplikaciju u tu listu?
5.  Koja je fundamentalna razlika između Django **projekta** i Django **aplikacije**?

### Poveznice na Gradivo:
*   [Poglavlje 1: Razvojna Okolina i Git](/01-okolina-i-git/) (posebno `1.3 Virtualna Okruženja`)
*   [Poglavlje 2: Uvod u Django i Postavljanje Projekta](/02-django-temelji/)

---

## 2. Modeli i Baze Podataka

Modeli su "jedini izvor istine" o našim podacima. Ova cjelina pokriva kako strukturiramo podatke, kako te promjene primjenjujemo na bazu i kako definiramo odnose među podacima.

### Ključni Koncepti:
*   Django **ORM** (Object-Relational Mapper): što je i koje su njegove prednosti.
*   Klasa `models.Model`.
*   Tipovi polja: `CharField`, `TextField`, `DateTimeField`, `BooleanField`, `ForeignKey`, `ManyToManyField`.
*   Opcije polja: `max_length`, `default`, `blank=True`, `null=True`.
*   Metoda `__str__(self)`: čemu služi?
*   **Migracije:** Proces u dva koraka (`makemigrations` i `migrate`).
*   Relacije među modelima:
    *   **Više-na-jedan** (`ForeignKey`): Što je i kada se koristi? Što znači `on_delete=models.CASCADE`?
    *   **Više-na-više** (`ManyToManyField`): Što je i kada se koristi? Kako Django upravlja ovom vezom u bazi?

### Pitanja za Provjeru Znanja:
1.  Objasnite što je Django ORM. Zašto ga koristimo umjesto pisanja čistog SQL-a?
2.  Opišite proces migracije u dva koraka. Što radi `makemigrations`, a što `migrate`?
3.  Kada biste koristili `ForeignKey`, a kada `ManyToManyField`? Navedite konkretan primjer za svaku relaciju (npr. Autor i Knjiga, Post i Tag).
4.  Zašto je važno definirati `__str__` metodu na modelu? Gdje se njezin rezultat najčešće vidi?

### Poveznice na Gradivo:
*   [Poglavlje 3: Modeli i Baze Podataka (ORM)](/03-mvt-moduli/01-modeli-i-baze.md)

---

## 3. URL-ovi i Viewovi

Viewovi sadrže poslovnu logiku, a URL-ovi ih povezuju sa svijetom. Ova cjelina pokriva kako Django obrađuje korisnički zahtjev i vraća odgovor.

### Ključni Koncepti:
*   **Request-Response ciklus:** Što se događa od trenutka kada korisnik upiše URL do prikaza stranice.
*   Uloga `urls.py` datoteka (URLconf).
*   Funkcija `path()` i njeni argumenti (`route`, `view`, `name`).
*   Funkcija `include()` za modularno uključivanje URL-ova iz aplikacija.
*   **Dinamički URL-ovi** i "hvatači" (npr. `<int:pk>`).
*   **View funkcija:** prima `request` objekt, vraća `HttpResponse` objekt.
*   Funkcija `render()`: njena tri argumenta (`request`, `template_name`, `context`).
*   **Kontekst (context):** Što je i kako se koristi za slanje podataka iz viewa u template.

### Pitanja za Provjeru Znanja:
1.  Opišite ukratko Request-Response ciklus u Djangu.
2.  Koja je svrha `include()` funkcije u glavnom `urls.py` projektu? Zašto je to dobra praksa?
3.  Kako biste kreirali URL koji može prihvatiti ID nekog objekta, npr. `/knjige/5/`? Napišite `path()` funkciju.
4.  Što je "kontekst" (context) i koja je njegova uloga u `render()` funkciji?

### Poveznice na Gradivo:
*   [Poglavlje 4: URL-ovi i Viewovi](/03-mvt-moduli/02-url-i-viewovi.md)

---

## 4. Generički Viewovi i Generiranje Podataka

Django nudi prečace za uobičajene zadatke poput prikaza liste objekata. Također, za razvoj nam trebaju podaci koje ne želimo unositi ručno.

### Ključni Koncepti:
*   **Generički Klasni Viewovi (CBV):** Koje su njihove prednosti u odnosu na funkcijske viewove (FBV).
*   `ListView` i `DetailView`: Njihova namjena i osnovna konfiguracija.
*   Ključni atributi CBV-ova: `model`, `template_name`, `context_object_name`.
*   Nadjačavanje metoda u CBV-ovima: `get_queryset()` za prilagođeno filtriranje podataka.
*   Kreiranje vlastitih `manage.py` naredbi.
*   Biblioteke za generiranje podataka: `factory-boy` i `Faker`.

### Pitanja za Provjeru Znanja:
1.  Koja je glavna prednost korištenja `ListView` umjesto pisanja vlastite funkcije za prikaz liste objekata?
2.  Ako `ListView` po defaultu dohvaća sve objekte (`Model.objects.all()`), kako biste ga natjerali da prikazuje samo filtrirane rezultate (npr. samo objave iz 2024. godine)? Koju metodu biste nadjačali?
3.  Zašto bismo kreirali vlastitu `manage.py` naredbu? Navedite jedan praktičan primjer.

### Poveznice na Gradivo:
*   [Poglavlje 4.4: Generički Klasni bazirani Viewovi (CBV)](/03-mvt-moduli/02-url-i-viewovi.md#44-generički-klasni-bazirani-viewovi-cbv)
*   [Priprema za Labos 3: Generiranje Podataka i Napredno Filtriranje](/putanja/do/lab3-pripreme.md)

---

## 5. Django Predlošci (Templates)

Templatei su zaduženi za prezentacijski sloj. Ovdje učimo kako dinamički generirati HTML koristeći podatke iz viewa.

### Ključni Koncepti:
*   **Django Template Language (DTL):** Njegova tri osnovna elementa.
*   **Varijable:** `{{ varijabla }}` i pristup atributima objekata (`{{ post.author.username }}`).
*   **Oznake (Tags):** `{% tag %}`. Najvažniji tagovi: `{% for %}`, `{% if %}`, `{% extends %}`, `{% block %}`, `{% url %}`, `{% static %}`.
*   **Filteri:** `|`. Primjeri: `|date`, `|truncatewords`, `|upper`.
*   **Nasljeđivanje predložaka:** Uloga `base.html` i kako ga proširiti.
*   **Statičke datoteke:** Konfiguracija (`STATIC_URL`, `STATICFILES_DIRS`) i korištenje u templateu.

### Pitanja za Provjeru Znanja:
1.  Objasnite princip nasljeđivanja predložaka u Djangu. Koja dva taga su ključna za taj proces?
2.  Koja je razlika između `{{ ... }}` i `{% ... %}` u Django templateima?
3.  Kako biste u templateu generirali link na stranicu čija URL putanja ima `name='post-detail'` i prima `pk` argument?
4.  Opišite proces uključivanja CSS datoteke u vaš projekt, od `settings.py` do `base.html`.

### Poveznice na Gradivo:
*   [Poglavlje 5: Predlošci i Datoteke](/03-mvt-moduli/03-predlosci-statika.md)

---

**Sretno na ispitu!**