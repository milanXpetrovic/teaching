---
parent: 'Interakcija s Korisnikom i Napredne Teme'
nav_order: 2
has_children: false
title: 'Poglavlje 7: Autentikacija i Autorizacija'
---

# Poglavlje 7: Autentikacija i Autorizacija

Do sada smo gradili aplikaciju koja je uglavnom anonimna. Vrijeme je da uvedemo korisnike! U ovom poglavlju naučit ćemo kako koristiti Djangov moćan, ugrađeni sustav za upravljanje korisnicima, što je temelj svake moderne web aplikacije.

Prvo, ključno je razumjeti razliku između dva temeljna sigurnosna pojma:

* **Autentikacija (Authentication):** Proces utvrđivanja **tko je korisnik**. Ovo je faza prijave (login), gdje korisnik pruža svoje kredencijale (npr. korisničko ime i lozinku) kako bi dokazao svoj identitet. Zamislite to kao pokazivanje osobne iskaznice na ulazu u klub.

* **Autorizacija (Authorization):** Proces utvrđivanja **što prijavljeni korisnik smije raditi**. Nakon što znamo tko je korisnik, provjeravamo ima li on dozvolu za ulazak u VIP sekciju kluba ili za naručivanje s posebnog menija.

Srećom, Django dolazi s "baterijama uključenim" i nudi robustan i siguran sustav za oba ova zadatka.

> **Najvažniji Sigurnosni Savjet:** Nikada, ali baš nikada, nemojte pokušavati sami "izumiti" sustav za autentikaciju (logiku za pohranu i provjeru lozinki, upravljanje sesijama, itd.). To je izuzetno teško napraviti ispravno i sigurno. Propusti u takvom sustavu mogu dovesti do katastrofalnih sigurnosnih problema. Uvijek se oslonite na provjerena i testirana rješenja poput onog ugrađenog u Django.

---

## 7.1 Djangov Ugrađeni Sustav Autentikacije

Kada ste kreirali projekt, Django je automatski dodao aplikaciju `django.contrib.auth` u vaš `INSTALLED_APPS`. Ona je temelj svega što ćemo raditi u ovom poglavlju i daje nam cijeli set alata:

* **`User` Model:** Fleksibilan model korisnika koji sadrži ključna polja:
    * `username`: Jedinstveno korisničko ime.
    * `password`: Lozinka, koja se **nikada ne sprema kao čisti tekst**. Django je automatski hešira (matematički "šifrira" u jednom smjeru) radi sigurnosti.
    * `email`, `first_name`, `last_name`: Osnovni podaci o korisniku.
    * `is_staff`: Boolean polje koje određuje smije li korisnik pristupiti admin sučelju.
    * `is_superuser`: Boolean polje koje korisniku daje sve dozvole bez potrebe za pojedinačnim dodjeljivanjem.
    * `is_active`: Boolean polje kojim možete deaktivirati korisnički račun bez brisanja.

* **`Group` Model:** Omogućuje grupiranje korisnika (npr. "Urednici", "Moderatori") i dodjeljivanje dozvola cijeloj grupi odjednom.

* **Sustav Dozvola (Permissions):** Za svaki model koji stvorite, Django automatski generira četiri osnovne dozvole u formatu `app_label.verb_modelname`:
    * `posts.add_post`: Dozvola za dodavanje postova.
    * `posts.change_post`: Dozvola za izmjenu postova.
    * `posts.delete_post`: Dozvola za brisanje postova.
    * `posts.view_post`: Dozvola za pregledavanje postova.

* **Forme i Viewove:** Pre-izgrađene forme (`AuthenticationForm`, `UserCreationForm`) i viewove (`LoginView`, `LogoutView`) za uobičajene zadatke, što nam drastično ubrzava razvoj.

---

## 7.2 Registracija Korisnika

Prvi korak za svakog novog korisnika je registracija. Koristit ćemo Djangovu ugrađenu formu `UserCreationForm` i generički `CreateView` da bismo ovo napravili brzo, sigurno i ispravno.

### Korak 1: Proširivanje `UserCreationForm`

Iako možemo koristiti `UserCreationForm` direktno, dobra je praksa stvoriti vlastitu formu koja ju nasljeđuje. To nam omogućuje laku prilagodbu u budućnosti.

1. Unutar `posts` aplikacije (ili, još bolje, unutar nove aplikacije naziva `users`), stvorite `forms.py`.
2. U tu datoteku dodajte sljedeći kod:

        # users/forms.py
        from django.contrib.auth.forms import UserCreationForm
        from django.contrib.auth.models import User

        class UserRegisterForm(UserCreationForm):
            class Meta(UserCreationForm.Meta):
                model = User
                # Odaberimo koja polja želimo prikazati na formi za registraciju.
                # Lozinka se automatski dodaje.
                fields = ('username', 'email')

    `UserCreationForm` je pametna `ModelForm` klasa. Ona ne samo da stvara korisnika, već se brine i za sigurnosne aspekte, poput ispravnog heširanja lozinke i provjere jesu li dvije unesene lozinke iste.

### Korak 2: View za Registraciju

Koristit ćemo `CreateView` jer je registracija u suštini "stvaranje" novog `User` objekta.

1. U `users/views.py` dodajte:

        # users/views.py
        from django.views.generic import CreateView
        from .forms import UserRegisterForm
        from django.urls import reverse_lazy

        class RegisterView(CreateView):
            form_class = UserRegisterForm
            template_name = 'registration/register.html'
            success_url = reverse_lazy('login') # Preusmjeri na login nakon uspješne registracije

    > **Zašto `reverse_lazy`?** `success_url` je atribut klase, što znači da se njegova vrijednost izračunava čim se server pokrene. U tom trenutku, Djangov URL sustav možda još nije učitao sve putanje. `reverse_lazy` odgađa izračunavanje URL-a do trenutka kada je on zaista potreban (nakon što je forma uspješno poslana), čime se izbjegavaju greške.

### Korak 3: Template za Registraciju

1. Unutar glavnog `templates` direktorija, stvorite poddirektorij `registration`.
2. Unutar njega, stvorite `register.html`:

        {% extends 'base.html' %}

        {% block content %}
            <h2>Registracija</h2>
            <form method="post">
                {% csrf_token %}
                {{ form.as_p }}
                <button type="submit">Registriraj se</button>
            </form>
        {% endblock %}

### Korak 4: Povezivanje URL-a

1. U glavnom `myproject/urls.py` povežite novi view:

        # myproject/urls.py
        from users.views import RegisterView
        # ...

        path('register/', RegisterView.as_view(), name='register'),

Sada, posjetom na `/register/`, korisnici će vidjeti formu za registraciju.

---

## 7.3 Prijava (Login) i Odjava (Logout)

Za prijavu i odjavu, Django nam posao čini još lakšim. Ne moramo pisati ni viewove ni forme; dovoljno je samo uključiti Djangove ugrađene.

### Korak 1: Povezivanje ugrađenih URL-ova

1. U glavnom `myproject/urls.py` dodajte jednu liniju koda koja će automatski kreirati sve potrebne URL-ove za autentikaciju:

        # myproject/urls.py
        from django.urls import path, include

        urlpatterns = [
            # ... vaše postojeće putanje
            path('accounts/', include('django.contrib.auth.urls')),
        ]

    Ovo će automatski stvoriti URL-ove:
    * `accounts/login/` (za prijavu)
    * `accounts/logout/` (za odjavu)
    * `accounts/password_change/` (za promjenu lozinke)
    * ...i nekoliko drugih za proces resetiranja lozinke.

### Korak 2: Konfiguracija preusmjeravanja

Recimo Djangu kamo da pošalje korisnika nakon uspješne prijave ili odjave. U `settings.py` dodajte:

    LOGIN_REDIRECT_URL = '/'  # Nakon prijave, idi na početnu stranicu.
    LOGOUT_REDIRECT_URL = '/' # Nakon odjave, idi na početnu stranicu.

### Korak 3: Kreiranje Login Templatea

Djangov ugrađeni `LoginView` po defaultu traži template na `registration/login.html`.

1. Kreirajte datoteku `templates/registration/login.html`:

        {% extends 'base.html' %}

        {% block content %}
            <h2>Prijava</h2>
            <form method="post">
                {% csrf_token %}
                {{ form.as_p }}
                <button type="submit">Prijavi se</button>
                <p><a href="{% url 'password_reset' %}">Zaboravili ste lozinku?</a></p>
            </form>
        {% endblock %}

### Korak 4: Dinamički Prikaz u Sučelju

Sada možemo prilagoditi naše sučelje. Kako template zna je li korisnik prijavljen? Django automatski dodaje varijablu `user` u kontekst svakog templatea (putem `django.contrib.auth.context_processors.auth`).

U `base.html` možemo dodati:

    {% if user.is_authenticated %}
        <p>Bok, {{ user.username }}! | <a href="{% url 'logout' %}">Odjava</a></p>
    {% else %}
        <a href="{% url 'login' %}">Prijava</a> |
        <a href="{% url 'register' %}">Registracija</a>
    {% endif %}

Atribut `user.is_authenticated` je `True` ako je korisnik prijavljen, a `False` ako nije.

---

## 7.4 Autorizacija: Kontrola Pristupa

Sada kada imamo prijavljene korisnike, moramo osigurati da samo autorizirani korisnici mogu raditi određene stvari, npr. kreirati novi post.

### Zaštita Viewova: `LoginRequiredMixin` i `@login_required`

* **Za Klasne Viewove (CBV):** Koristimo `LoginRequiredMixin`. On mora biti **prvi** na listi nasljeđivanja.

        from django.contrib.auth.mixins import LoginRequiredMixin

        class PostCreateView(LoginRequiredMixin, CreateView):
            # ...

* **Za Funkcijske Viewove (FBV):** Koristimo `@login_required` dekorator iznad definicije funkcije.

        from django.contrib.auth.decorators import login_required

        @login_required
        def my_protected_view(request):
            # ...

Ako neprijavljeni korisnik pokuša pristupiti, Django će ga automatski preusmjeriti na stranicu za prijavu, dodajući `?next=/putanja/do/zasticene/stranice/` u URL. Nakon uspješne prijave, bit će preusmjeren na stranicu koju je prvotno tražio.

### Dozvole (Permissions) u Templateima

Ponekad želite prikazati određeni gumb ili link samo korisnicima koji imaju dozvolu za to. U tu svrhu, Django u templateima daje pristup `perms` objektu.

    {% if perms.posts.add_post %}
        <a href="{% url 'post-create' %}">Novi Post</a>
    {% endif %}

### Napredna Autorizacija: `UserPassesTestMixin`

Što ako pravilo nije jednostavno "je li korisnik prijavljen"? Što ako želimo dopustiti uređivanje posta samo **autoru tog posta**? Za to koristimo `UserPassesTestMixin`.

    from django.contrib.auth.mixins import UserPassesTestMixin

    class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
        model = Post
        # ...

        def test_func(self):
            post = self.get_object()
            return self.request.user == post.author

    `test_func` mora vratiti `True` ako korisnik smije pristupiti stranici, a `False` ako ne smije. Ako vrati `False`, Django će prikazati `403 Forbidden` grešku.

---

## 7.5 Resetiranje Lozinke

Proces resetiranja lozinke je već ugrađen! Naš posao je samo kreirati template i konfigurirati slanje emaila.

1. **URL-ovi:** Već su postavljeni pod `accounts/` zahvaljujući `include('django.contrib.auth.urls')`.

2. **Templatei:** Kreirajte sljedeće datoteke unutar `templates/registration/`:
    * `password_reset_form.html`: Forma za unos email adrese.
    * `password_reset_done.html`: Poruka koja se prikazuje nakon slanja zahtjeva ("Email je poslan").
    * `password_reset_confirm.html`: Forma za unos nove lozinke (dolazi se preko linka iz emaila).
    * `password_reset_complete.html`: Poruka o uspješnoj promjeni lozinke.

3. **Konfiguracija emaila (za razvoj):**
    Za vrijeme razvoja, ne želimo slati prave emailove. Najlakše je ispisivati sadržaj emaila u konzolu. U `settings.py` dodajte:

        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

Sada, kada prođete kroz proces resetiranja lozinke, umjesto slanja emaila, Django će u terminalu ispisati cijeli sadržaj emaila, uključujući i link za resetiranje. Za produkciju, ovu postavku ćete promijeniti u postavke vašeg pravog SMTP servera.

---

Djangov sustav za autentikaciju i autorizaciju je robustan, siguran i štedi ogromnu količinu vremena. Njegovim korištenjem, pridržavamo se najboljih praksi i osiguravamo da je naša aplikacija sigurna od samog početka.