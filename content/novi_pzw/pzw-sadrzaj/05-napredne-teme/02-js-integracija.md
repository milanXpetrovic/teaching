---
parent: 'Naprednije Teme za Kompletnog Django Developera'
nav_order: 2
has_children: false
title: 'Poglavlje 11: Konzumiranje REST API-ja s JavaScriptom'
---

# Poglavlje 11: Konzumiranje REST API-ja s JavaScriptom

U prethodnom poglavlju izgradili smo moćan Django REST Framework (DRF) API. Naš back-end sada može slati i primati podatke u univerzalnom JSON formatu. Ali, tko će te podatke koristiti i kako?

Odgovor je: **klijent**. To može biti mobilna aplikacija, drugi server, ili, što je najčešći slučaj, JavaScript kod koji se izvršava u web pregledniku korisnika.

U ovom poglavlju, prebacit ćemo se na "drugu stranu" i naučiti kako s jednostavnim, modernim JavaScriptom možemo "razgovarati" s našim Django API-jem kako bismo stvorili dinamično i interaktivno korisničko iskustvo.

> **Važna napomena:** Za ovo poglavlje pretpostavit ćemo da **ne koristimo** nikakve velike JavaScript frameworke poput Reacta, Vuea ili Angulara. Koristit ćemo **"Vanilla JS"** – čisti JavaScript koji je ugrađen u svaki moderni preglednik. Principi su potpuno isti, bez obzira koji alat koristili na front-endu.

---

## 11.1 Osnove Fetch API-ja: Razgovor sa Serverom

**Fetch API** je moderno sučelje ugrađeno u preglednike koje nam omogućuje slanje i primanje HTTP zahtjeva. Puno je jednostavniji i moćniji od starijeg `XMLHttpRequest` objekta.

Osnovna struktura `fetch` poziva za dohvaćanje podataka (GET zahtjev) izgleda ovako:

    fetch('https://api.example.com/data/')
        .then(response => response.json())
        .then(data => {
            console.log(data); // Ovdje radimo nešto s podacima
        })
        .catch(error => {
            console.error('Došlo je do greške:', error);
        });

**Što se ovdje događa?**
`fetch` radi **asinkrono**. To znači da ne zaustavlja izvršavanje ostatka koda dok čeka odgovor od servera. Umjesto toga, on koristi "Obećanja" (Promises), što vidimo kroz `.then()` blokove.

1.  `fetch(...)`: Šalje zahtjev na zadani URL. Vraća *Promise* koji će se riješiti s `Response` objektom.
2.  `.then(response => response.json())`: Kada stigne odgovor od servera, uzimamo taj `Response` objekt i pozivamo `.json()` metodu na njemu. Ova metoda također vraća *Promise* koji će se riješiti s parsiranim JSON podacima (pretvara JSON string u JavaScript objekt).
3.  `.then(data => { ... })`: Kada su podaci konačno parsirani, ovaj blok se izvršava. Sada imamo JavaScript objekt (`data`) s kojim možemo raditi – prikazati ga na stranici, filtrirati, itd.
4.  `.catch(error => { ... })`: Ako se u bilo kojem od prethodnih koraka dogodi greška (npr. server je nedostupan, JSON je neispravan), ovaj blok će se izvršiti.

---

## 11.2 Prikazivanje podataka s API-ja (GET zahtjev)

Vratimo se na naš blog API. Želimo na jednoj stranici, bez ponovnog učitavanja, prikazati listu svih postova koje dohvatimo s našeg `/api/posts/` endpointa.

**1. Priprema HTML-a i Django Templatea:**
Prvo, potreban nam je Django view koji će poslužiti osnovnu HTML stranicu i prazan "kontejner" gdje će JavaScript umetnuti podatke.

*   U `posts/views.py`:

        from django.shortcuts import render

        def posts_frontend(request):
            return render(request, 'posts/posts_frontend.html')

*   U `templates/posts/posts_frontend.html`:

        {% extends 'base.html' %}
        {% load static %}

        {% block content %}
            <h1>Postovi učitani pomoću JavaScripta</h1>
            <div id="posts-container">
                <p>Učitavanje...</p>
            </div>

            <script src="{% static 'js/posts.js' %}"></script>
        {% endblock %}

*   Povežite ovaj view s nekim URL-om, npr. `/frontend/posts/`.

**2. Pisanje JavaScript koda:**
Sada, u našoj `static/js/posts.js` datoteci, pišemo logiku za dohvaćanje i prikaz podataka.

    // static/js/posts.js

    // Čekamo da se cijeli HTML dokument učita prije izvršavanja skripte
    document.addEventListener('DOMContentLoaded', function() {
        
        const postsContainer = document.getElementById('posts-container');
        const apiUrl = '/api/posts/'; // Naš Django API endpoint

        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Mrežni odgovor nije bio u redu');
                }
                return response.json();
            })
            .then(posts => {
                // Očistimo poruku "Učitavanje..."
                postsContainer.innerHTML = ''; 

                if (posts.length === 0) {
                    postsContainer.innerHTML = '<p>Nema postova za prikaz.</p>';
                    return;
                }
                
                // Kreiramo HTML za svaki post
                posts.forEach(post => {
                    const postElement = document.createElement('div');
                    postElement.classList.add('post-item');
                    postElement.innerHTML = `
                        <h2><a href="/api/posts/${post.id}">${post.title}</a></h2>
                        <p>${post.content.substring(0, 100)}...</p>
                    `;
                    postsContainer.appendChild(postElement);
                });
            })
            .catch(error => {
                console.error('Greška pri dohvaćanju postova:', error);
                postsContainer.innerHTML = '<p>Nije moguće učitati postove. Pokušajte ponovno kasnije.</p>';
            });

    });

Sada, kada posjetite `/frontend/posts/`, stranica će se prvo učitati s porukom "Učitavanje...", a zatim će JavaScript u pozadini dohvatiti podatke s vašeg API-ja i dinamički ih ispuniti na stranici.

---

## 11.3 Slanje podataka na API (POST/PUT zahtjevi)

Dohvaćanje je samo pola priče. Prava interaktivnost dolazi kada omogućimo korisnicima da šalju podatke **na** server.

Za slanje podataka, `fetch` poziv je malo kompleksniji. Moramo mu proslijediti drugi argument, objekt s opcijama koji definira:
*   `method`: HTTP metoda (npr. `'POST'`, `'PUT'`).
*   `headers`: Informacije o tipu sadržaja i, što je ključno, **CSRF token**.
*   `body`: Podaci koje šaljemo, obično kao JSON string.

### Slanje CSRF tokena s AJAX/Fetch zahtjevima

Django nas štiti od CSRF napada i za AJAX/Fetch zahtjeve. Moramo osigurati da se CSRF token pošalje uz svaki `POST`, `PUT`, `PATCH` ili `DELETE` zahtjev.

**"Two Scoops" preporučeni pristup:**
U vašem glavnom `base.html` templateu, unutar `<head>` taga, dodajte:

    <script>
        const csrftoken = '{{ csrf_token }}';
    </script>

Ovo će Djangov `csrf_token` učiniti dostupnim kao globalnu JavaScript varijablu. Sada ga možemo koristiti u našim `fetch` pozivima.

**Primjer: Slanje novog posta (POST zahtjev):**
Pretpostavimo da imamo HTML formu s `id="new-post-form"` i poljima `title` i `content`.

    // static/js/posts.js
    const form = document.getElementById('new-post-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Sprječavamo klasično slanje forme

        const title = document.getElementById('title-input').value;
        const content = document.getElementById('content-input').value;
        const apiUrl = '/api/posts/';

        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken // Koristimo globalnu varijablu!
            },
            body: JSON.stringify({
                title: title,
                content: content
                // Pretpostavljamo da API view postavlja autora na temelju prijavljenog korisnika
            })
        })
        .then(response => response.json())
        .then(newPost => {
            console.log('Uspješno kreiran post:', newPost);
            // Ovdje možemo dodati logiku za osvježavanje liste postova
            // ili preusmjeravanje korisnika.
            window.location.reload(); 
        })
        .catch(error => {
            console.error('Greška pri kreiranju posta:', error);
        });
    });

Ovaj primjer pokazuje kompletan ciklus:
1.  Hvatamo događaj slanja forme.
2.  Sprječavamo defaultno ponašanje preglednika.
3.  Prikupljamo podatke iz input polja.
4.  Konstruiramo `fetch` **POST** zahtjev, uključujući ispravne headere i JSON tijelo.
5.  Obrađujemo odgovor od servera.

Ovim ste povezali svoj Django back-end i JavaScript front-end, stvarajući modernu, dinamičnu web aplikaciju gdje se korisničko sučelje može ažurirati bez potrebe za ponovnim učitavanjem cijele stranice.