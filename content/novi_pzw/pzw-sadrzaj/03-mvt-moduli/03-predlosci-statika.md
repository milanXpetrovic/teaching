---
parent: 'Srce Djanga: Modeli, Viewovi, Templatei (MVT)'
nav_order: 3
has_children: false
title: 'Poglavlje 5: Predlošci i Datoteke'
---

# Poglavlje 5: Predlošci (Templates) i Datoteke

Do sada smo definirali naše podatke (Modeli) i napisali logiku za njihovo dohvaćanje (Viewovi). Sada je vrijeme za posljednji i vizualno najvažniji korak: prikazati te podatke korisniku na lijep i strukturiran način. To je posao **Django Templatea**.

Osim HTML strukture, svaka moderna web stranica treba i stil (CSS), interaktivnost (JavaScript) i slike. Naučit ćemo kako Django upravlja **statičkim** i **medijskim** datotekama.

## 5.1 Django Template Language (DTL)

Django dolazi s vlastitim, moćnim, ali namjerno ograničenim template jezikom. Njegova filozofija je da **templatei trebaju biti zaduženi za prezentaciju, a ne za poslovnu logiku**. Stoga, u njima ne možete pisati kompleksan Python kod, što vas prisiljava da logiku držite tamo gdje joj je mjesto – u viewovima.

DTL ima tri osnovna gradivna bloka:

### 1. Varijable (`{{ ... }}`)

Varijable služe za ispisivanje vrijednosti koje je `View` poslao u template unutar **konteksta**. Pišu se unutar dvostrukih vitičastih zagrada.

**Primjer za `post_detail.html`:**
Ako je naš `context` u viewu bio `{'post': post_objekt}`, u templateu možemo pristupiti atributima tog objekta:

    <h1>{{ post.title }}</h1>
    <p>{{ post.content }}</p>
    <p>Objavljeno: {{ post.created_at }}</p>

### 2. Oznake (Tags) (`{% ... %}`)

Oznake (tagovi) omogućuju osnovnu programsku logiku unutar templatea, poput petlji i uvjetnih izraza. Pišu se unutar vitičastih zagrada s postotkom.

**Primjer za `post_list.html`:**
Ako je naš `context` bio `{'posts': lista_post_objekata}`, možemo proći kroz listu pomoću `{% for %}` taga:

    <ul>
        {% for post in posts %}
            <li>
                <h2>{{ post.title }}</h2>
                <p>Napisao: {{ post.author.username }}</p>
            </li>
        {% empty %}
            <li>Nema dostupnih postova.</li>
        {% endfor %}
    </ul>

*   `{% for post in posts %}`: Započinje petlju.
*   `{% empty %}`: Opcionalni blok koji se prikazuje ako je lista `posts` prazna.
*   `{% endfor %}`: Zatvara `for` petlju.

### 3. Filteri (`|`)

Filteri omogućuju jednostavnu transformaciju varijabli prije prikaza. Koriste se unutar `{{ ... }}` bloka, odvojeni od varijable znakom `|`.

**Primjeri:**

    <!-- Prikazuje naslov velikim slovima -->
    {{ post.title|upper }}

    <!-- Prikazuje samo prvih 20 riječi sadržaja -->
    {{ post.content|truncatewords:20 }}

    <!-- Formatira datum -->
    {{ post.created_at|date:"d. M Y." }}

Django dolazi s desecima ugrađenih filtera.

---

## 5.2 Nasljeđivanje Predložaka (Template Inheritance)

Većina stranica na jednoj web lokaciji dijeli isti osnovni izgled – zaglavlje (header), podnožje (footer), navigaciju. Bilo bi izuzetno neefikasno kopirati taj isti HTML kod u svaku pojedinu template datoteku.

DTL rješava ovaj problem pomoću moćnog koncepta **nasljeđivanja**.

1.  **Stvorite osnovni kostur (`base.html`):**
    Prvo kreiramo "roditeljski" template koji sadrži svu zajedničku strukturu. Unutar njega definiramo `{% block %}` oznake kao prazna mjesta koja će "djeca" popuniti.

    Stvorimo `templates/base.html` (u korijenskom `templates` direktoriju projekta, ne unutar aplikacije):

        <!DOCTYPE html>
        <html>
        <head>
            <title>{% block title %}Moj Blog{% endblock %}</title>
        </head>
        <body>
            <header>
                <h1>Dobrodošli na Moj Blog</h1>
            </header>
            <main>
                {% block content %}{% endblock %}
            </main>
            <footer>
                <p>&copy; 2025 Moj Blog</p>
            </footer>
        </body>
        </html>

2.  **Proširite osnovni kostur (`{% extends %}`):**
    Sada, naši "dječji" templatei (npr. `post_list.html`) mogu naslijediti `base.html` i samo popuniti definirane blokove.

    **Primjer za `posts/post_list.html`:**

        {% extends 'base.html' %}

        {% block title %}Lista Postova - Moj Blog{% endblock %}

        {% block content %}
            <h1>Svi postovi</h1>
            <ul>
                {% for post in posts %}
                    <li>{{ post.title }}</li>
                {% endfor %}
            </ul>
        {% endblock %}

Kada Django renderira `post_list.html`, on će:
1.  Učitati `base.html`.
2.  Pronaći `{% block title %}` i `{% block content %}` u `base.html`.
3.  Zamijeniti njihov sadržaj sa sadržajem tih istih blokova iz `post_list.html`.
4.  Vratiti kompletan, spojen HTML.

Ovo je temelj DRY (Don't Repeat Yourself) principa na front-endu.

---

## 5.3 Statičke Datoteke (CSS, JavaScript, Slike)

Statičke datoteke su one datoteke koje se ne mijenjaju dinamički – CSS za stil, JavaScript za interaktivnost, slike, fontovi. One nisu dio MVT ciklusa, već se poslužuju direktno.

### Konfiguracija

1.  **`STATIC_URL`:** U `myproject/settings.py`, već postoji postavka:
    `STATIC_URL = 'static/'`
    Ovo je URL prefiks koji će se koristiti za pristup statičkim datotekama na webu (npr. `/static/css/style.css`).

2.  **`STATICFILES_DIRS`:** Moramo reći Djangu gdje da traži naše statičke datoteke. Uobičajena praksa je stvoriti `static` direktorij u korijenu projekta. Na dno `myproject/settings.py` dodajte:

        import os

        STATICFILES_DIRS = [
            os.path.join(BASE_DIR, 'static'),
        ]

3.  **Kreiranje direktorija:** U korijenu projekta (gdje je `manage.py`), stvorite `static` direktorij, a unutar njega `css` direktorij i datoteku `style.css`.

### Korištenje u Templateima

Da bismo koristili statičke datoteke u templateu, moramo:
1.  Učitati `static` tag library na vrhu templatea.
2.  Koristiti `{% static %}` tag za generiranje ispravne URL putanje.

Uredimo naš `base.html`:

    {% load static %}
    <!DOCTYPE html>
    <html>
    <head>
        <title>{% block title %}Moj Blog{% endblock %}</title>
        <link rel="stylesheet" href="{% static 'css/style.css' %}">
    </head>
    ...

Django će automatski zamijeniti `{% static 'css/style.css' %}` s ispravnom putanjom, npr. `/static/css/style.css`.

---

## 5.4 Media Datoteke (Uploadane Datoteke)

**Statičke datoteke** su dio vašeg koda i vi ih kao developer dodajete. **Medijske datoteke** su one koje korisnici uploadaju putem aplikacije (npr. profilne slike, dokumenti).

Django ih tretira odvojeno.

### Konfiguracija

Slično kao za statičke datoteke, moramo reći Djangu gdje da sprema i kako da poslužuje medijske datoteke. Na dno `myproject/settings.py` dodajte:

    # Postavke za Media datoteke
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

*   `MEDIA_ROOT`: Apsolutna putanja do direktorija gdje će se datoteke fizički spremati na serveru.
*   `MEDIA_URL`: URL prefiks za pristup tim datotekama putem weba.

Za razvojno okruženje, moramo također dodati pravilo u naš glavni `myproject/urls.py` kako bi razvojni server znao posluživati te datoteke:

    # myproject/urls.py
    from django.conf import settings
    from django.conf.urls.static import static
    # ... (ostali importi)

    urlpatterns = [
        # ... (ostali url-ovi)
    ]

    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

### Korištenje u Modelima

Za upload datoteka, koristimo `FileField` ili `ImageField` u našim modelima. `ImageField` je specijalizirani `FileField` s dodatnom validacijom za slike (i zahtijeva `Pillow` biblioteku: `pip install Pillow`).

**Primjer:**

    class Profile(models.Model):
        # ...
        profile_picture = models.ImageField(upload_to='profile_pics/')

Kada korisnik uploada sliku, ona će biti spremljena u `media/profile_pics/ime_datoteke.jpg`.

### Prikaz u Templateima

Za prikaz, jednostavno koristimo `.url` atribut na polju modela:

    <img src="{{ profile.profile_picture.url }}" alt="Profilna slika">

---

Sada imate kompletan pregled Djangovog MVT sustava! Znate kako definirati podatke (Modeli), kako napisati logiku za njihovu obradu (Viewovi), i kako ih prikazati (Templatei), uključujući i serviranje stilova, skripti i slika.

S ovim temeljnim znanjem, spremni ste za gradnju kompleksnijih i interaktivnijih funkcionalnosti.