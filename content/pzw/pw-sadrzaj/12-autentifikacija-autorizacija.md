---
author: Milan Petrović
title: "12. Autentifikacija, autorizacija i upravljanje korisnicima"
layout: default
parent: PZW
nav_order: 12
has_children: false
has_toc: true
nav_exclude: true
---

# Autentifikacija, autorizacija i upravljanje korisnicima
{: .no_toc }

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Osnovni pojmovi

- **Autentifikacija** odgovara na pitanje "tko si ti?": provjera identiteta, najčešće korisničkim imenom i lozinkom.
- **Autorizacija** odgovara na pitanje "što smiješ raditi?": provjera ovlasti već prijavljenog korisnika.

HTTP ne pamti stanje između zahtjeva. Nakon uspješne prijave Django zato stvara **sesiju**: podatke o korisniku sprema na poslužitelju, a pregledniku šalje kolačić `sessionid` s nasumičnim identifikatorom. Preglednik taj kolačić šalje uz svaki sljedeći zahtjev, a Django prema njemu zna tko je korisnik i postavlja `request.user`.

Sesiju možemo koristiti i za vlastite podatke:

``` python
def homepage(request):
    request.session["broj_posjeta"] = request.session.get("broj_posjeta", 0) + 1
    # ...
```

Sustav autentifikacije (`django.contrib.auth`) već je uključen u svaki novi projekt i sadrži:

| Dio | Namjena |
| --- | ------- |
| model `User` | korisnici, lozinke (spremljene kao sažeci, nikad u čistom obliku), oznake `is_staff`, `is_superuser`, `is_active` |
| modeli `Group` i `Permission` | grupe korisnika i ovlasti |
| `AuthenticationMiddleware` | postavlja `request.user` za svaki zahtjev |
| gotovi pogledi | prijava, odjava, promjena i obnova lozinke |
| obrasci | `AuthenticationForm`, `UserCreationForm`, `PasswordChangeForm`... |
| dekoratori i mixini | ograničavanje pristupa pogledima |

## Postavljanje u projektu

Nastavljamo s projektom `knjiznica`. Ako radite novi projekt, nakon stvaranja primijenite migracije i stvorite administratora naredbom `python manage.py createsuperuser`.

Datoteka `knjiznica/urls.py`:

``` python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("main.urls")),
]
```

Uključivanjem `django.contrib.auth.urls` dobivamo sljedeće adrese:

| Adresa | Ime URL-a |
| ------ | --------- |
| `accounts/login/` | `login` |
| `accounts/logout/` | `logout` |
| `accounts/password_change/` | `password_change` |
| `accounts/password_change/done/` | `password_change_done` |
| `accounts/password_reset/` | `password_reset` |
| `accounts/password_reset/done/` | `password_reset_done` |
| `accounts/reset/<uidb64>/<token>/` | `password_reset_confirm` |
| `accounts/reset/done/` | `password_reset_complete` |

## Prijava

Posjetite `http://127.0.0.1:8000/accounts/login/`. Javit će se greška `TemplateDoesNotExist at /accounts/login/`, a iz poruke `Exception Value: registration/login.html` vidimo da Django ne može pronaći traženi predložak. Pogled za prijavu postoji, ali predložak moramo napisati sami.

{: .zadatak }
> Unutar direktorija `templates/registration` stvorite `login.html`.

**Rješenje zadatka.** Datoteka `templates/registration/login.html`:

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block content %}
<h2>Prijava</h2>

{% if form.errors %}
    <p>Korisničko ime ili lozinka nisu ispravni. Pokušajte ponovno.</p>
{% endif %}

{% if next %}
    {% if user.is_authenticated %}
        <p>Vaš račun nema pristup ovoj stranici. Za nastavak se prijavite
        računom koji ima pristup.</p>
    {% else %}
        <p>Za pregled ove stranice morate se prijaviti.</p>
    {% endif %}
{% endif %}

<form method="post" action="{% url 'login' %}">
    {% csrf_token %}
    <table>
        <tr>
            <td>{{ form.username.label_tag }}</td>
            <td>{{ form.username }}</td>
        </tr>
        <tr>
            <td>{{ form.password.label_tag }}</td>
            <td>{{ form.password }}</td>
        </tr>
    </table>
    <input type="submit" value="Prijava">
    <input type="hidden" name="next" value="{{ next }}">
</form>

<p><a href="{% url 'password_reset' %}">Zaboravili ste lozinku?</a></p>
{% endblock %}
```
{% endraw %}

Skriveno polje `next` sadrži adresu na koju se korisnik vraća nakon prijave. Popunjava se kada korisnika na prijavu preusmjeri zaštićena stranica (npr. `/accounts/login/?next=/knjige/nova/`). Detaljnije o [CSRF tokenu](https://docs.djangoproject.com/en/6.1/ref/csrf/).

Kamo se korisnik usmjerava nakon prijave i odjave, ako `next` nije zadan, određujemo u `settings.py`:

``` python
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "main:homepage"
LOGOUT_REDIRECT_URL = "main:homepage"
```

Vrijednosti mogu biti imena URL-ova ili adrese. Bez `LOGIN_REDIRECT_URL` Django korisnika šalje na `/accounts/profile/`, koji ne postoji.

## Odjava

Od Djanga 5.0 odjava radi **isključivo metodom POST**, kako tuđa stranica ne bi mogla korisnika odjaviti običnom poveznicom ili slikom. Zato je umjesto poveznice potreban mali obrazac.

Izbornik u `templates/base_generic.html` dopunjujemo prikazom stanja prijave:

{% raw %}
``` django
<ul>
    <li><a href="{% url 'main:homepage' %}">Početna</a></li>
    <li><a href="{% url 'main:book_list' %}">Knjige</a></li>
    <li><a href="{% url 'main:author_list' %}">Autori</a></li>
    {% if user.is_authenticated %}
        <li>Prijavljeni ste kao {{ user.username }}</li>
        <li>
            <form method="post" action="{% url 'logout' %}">
                {% csrf_token %}
                <button type="submit">Odjava</button>
            </form>
        </li>
    {% else %}
        <li><a href="{% url 'login' %}?next={{ request.path|urlencode }}">Prijava</a></li>
        <li><a href="{% url 'main:register' %}">Registracija</a></li>
    {% endif %}
</ul>
```
{% endraw %}

{% raw %}
Varijabla `user` dostupna je u svim predlošcima zahvaljujući kontekstnom procesoru `auth`. Za neprijavljenog posjetitelja `user` je objekt `AnonymousUser`, kojem je `user.is_authenticated` jednako `False`.
{% endraw %}

Poveznica na registraciju proradit će kada u nastavku dodamo taj pogled.

## Registracija

Za registraciju koristimo gotov obrazac `UserCreationForm`, koji sadrži korisničko ime i dvostruki unos lozinke te provjerava snagu lozinke prema `AUTH_PASSWORD_VALIDATORS` iz `settings.py`.

Funkcija `register()` u `main/views.py`:

``` python
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # odmah prijavljujemo novog korisnika
            return redirect("main:homepage")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})
```

Metoda `form.save()` vraća stvorenog korisnika, pa ga možemo odmah prijaviti funkcijom `login()`. (Alternativa je ponovna provjera korisničkog imena i lozinke funkcijom `authenticate()` prije poziva `login()`.)

U `main/urls.py`:

``` python
path("registracija/", views.register, name="register"),
```

Datoteka `templates/registration/register.html`:

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block content %}
<h2>Registracija</h2>
<form method="post" action="{% url 'main:register' %}">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Registriraj se">
</form>
{% endblock %}
```
{% endraw %}

{: .zadatak }
> Registrirajte novog korisnika i provjerite da ste nakon registracije prijavljeni. Pokušajte se registrirati s lozinkom `12345678` i pročitajte greške.

### Registracija s e-mail adresom

`UserCreationForm` možemo proširiti dodatnim poljima. U `main/forms.py`:

``` python
from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="E-mail", required=True)

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")
```

U pogledu `register` zatim umjesto `UserCreationForm` koristite `RegisterForm`.

## Ograničavanje pristupa

### Samo za prijavljene korisnike

Funkcijske poglede štitimo dekoratorom `@login_required`:

``` python
from django.contrib.auth.decorators import login_required


@login_required
def book_create(request):
    ...
```

Za klase koristimo mixin `LoginRequiredMixin`, koji mora biti **prvi s lijeva** u popisu roditeljskih klasa:

``` python
from django.contrib.auth.mixins import LoginRequiredMixin


class BookCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Book
    form_class = BookForm
    success_message = "Knjiga „%(title)s” je dodana."
```

Neprijavljeni korisnik se preusmjerava na `LOGIN_URL` s parametrom `next`.

{: .napomena }
> Od Djanga 5.1 postoji i `LoginRequiredMiddleware`: kada se doda u `MIDDLEWARE` (iza `AuthenticationMiddleware`), **sve** stranice zahtijevaju prijavu, a javne se izuzimaju dekoratorom `@login_not_required`. To je sigurniji pristup za aplikacije u kojima je većina stranica privatna, jer se ne može dogoditi da zaboravimo zaštititi novu stranicu.

### Ovlasti

Za svaki model Django automatski stvara četiri ovlasti: `add`, `change`, `delete` i `view`. Puni naziv ovlasti je `<aplikacija>.<radnja>_<model>`, npr. `main.add_book` ili `main.delete_author`.

Provjera u Pythonu:

``` python
>>> user.has_perm("main.add_book")
>>> user.has_perms(["main.add_book", "main.change_book"])
```

Superkorisnik (`is_superuser=True`) ima sve ovlasti.

Zaštita pogleda:

``` python
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin


@permission_required("main.change_book", raise_exception=True)
def book_update(request, pk):
    ...


class BookDelete(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = "main.delete_book"
    model = Book
    success_url = reverse_lazy("main:book_list")
    success_message = "Knjiga je obrisana."
```

`PermissionRequiredMixin` neprijavljenog korisnika šalje na prijavu, a prijavljenom korisniku bez ovlasti vraća 403.

{% raw %}
U predlošcima su ovlasti dostupne kroz varijablu `perms`, pa poveznice prikazujemo samo onima koji ih smiju koristiti:

``` django
{% if perms.main.add_book %}
    <a href="{% url 'main:book_create' %}">Dodaj knjigu</a>
{% endif %}
```
{% endraw %}

{: .upozorenje }
> Skrivanje poveznice nije zaštita. Korisnik adresu može upisati ručno, pa **pogled** uvijek mora provjeravati ovlasti.

Vlastite ovlasti dodajemo u klasi `Meta` modela (nakon toga napravite migraciju):

``` python
class Book(models.Model):
    # ...
    class Meta:
        ordering = ["-publication_date"]
        permissions = [
            ("feature_book", "Može označiti knjigu kao istaknutu"),
        ]
```

### Grupe

Dodjeljivanje ovlasti svakom korisniku zasebno je nepraktično. Ovlasti se zato dodjeljuju **grupama**, a korisnici se dodaju u grupe. Kroz administratorsko sučelje ili u ljusci:

``` python
>>> from django.contrib.auth.models import Group, Permission, User
>>> knjiznicari = Group.objects.create(name="Knjižničari")
>>> ovlasti = Permission.objects.filter(
...     content_type__app_label="main",
...     codename__in=["add_book", "change_book", "delete_book"],
... )
>>> knjiznicari.permissions.set(ovlasti)
>>> ivo = User.objects.create_user("ivo", password="neka-dugacka-lozinka")
>>> ivo.groups.add(knjiznicari)
>>> ivo = User.objects.get(username="ivo")   # ponovno dohvaćanje, ovlasti se spremaju u međuspremnik objekta
>>> ivo.has_perm("main.add_book")
True
```

Grupu koja mora postojati u svakoj instalaciji najbolje je stvoriti podatkovnom migracijom (vidi [poglavlje 9](09-testni-podaci-i-sijanje.md#podatkovne-migracije)).

### Ovlasti nad pojedinim objektom

Ovlast `main.change_book` dopušta izmjenu **svih** knjiga. Često želimo da korisnik smije mijenjati samo zapise koje je sam stvorio. Dodajmo knjizi korisnika koji ju je unio:

``` python
from django.conf import settings


class Book(models.Model):
    # ...
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="books_added",
    )
```

Model korisnika referenciramo s `settings.AUTH_USER_MODEL`, a ne izravnim uvozom modela `User` (vidi u nastavku). Opcija `editable=False` isključuje polje iz obrazaca.

Pri stvaranju knjige korisnika postavljamo u pogledu, nikad iz obrasca:

``` python
class BookCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Book
    form_class = BookForm
    success_message = "Knjiga „%(title)s” je dodana."

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)
```

Pri uređivanju ograničavamo skup knjiga koje korisnik uopće može dohvatiti:

``` python
class BookUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Book
    form_class = BookForm
    success_message = "Knjiga „%(title)s” je izmijenjena."

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm("main.change_book"):
            return queryset                                    # knjižničari mijenjaju sve
        return queryset.filter(added_by=self.request.user)     # ostali samo svoje
```

Korisnik koji pokuša urediti tuđu knjigu dobiva 404, jer za njega ta knjiga "ne postoji". Za složenije uvjete postoji `UserPassesTestMixin` s metodom `test_func()`.

## Vlastiti model korisnika

Za nove projekte Django preporučuje da se **na samom početku**, prije prve migracije, definira vlastiti model korisnika, čak i ako je zasad jednak ugrađenom. Kasnija promjena je vrlo zahtjevna.

``` python
# korisnici/models.py
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
```

``` python
# settings.py
AUTH_USER_MODEL = "korisnici.User"
```

U kodu tada model korisnika nikad ne uvozimo izravno, nego koristimo `settings.AUTH_USER_MODEL` u definicijama modela, odnosno `django.contrib.auth.get_user_model()` u ostalom kodu.

## Obnova zaboravljene lozinke

Pogledi za obnovu lozinke šalju e-poruku s jednokratnom poveznicom. Za vrijeme razvoja poruke možemo ispisivati u terminal umjesto stvarnog slanja:

``` python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

{: .napomena }
> Django 6.1 uvodi i postavke e-pošte u obliku rječnika. Prije postavljanja slanja e-pošte u stvarnom projektu provjerite [dokumentaciju za verziju koju koristite](https://docs.djangoproject.com/en/6.1/topics/email/).

{: .zadatak }
> Posjetite `accounts/password_reset/`, upišite e-mail adresu postojećeg korisnika i u terminalu poslužitelja pronađite poveznicu za obnovu. Otvorite je i postavite novu lozinku. Predlošci za ove stranice dolaze iz administratorskog sučelja, a možete ih nadjačati vlastitim predlošcima u `templates/registration/`.

## Zadaci za vježbu

{: .zadatak }
> - Zaštitite poglede za stvaranje, uređivanje i brisanje knjiga i autora iz [poglavlja 8](08-obrasci-get-post-modelforms.md): stvaranje smiju svi prijavljeni korisnici, brisanje samo članovi grupe `Knjižničari`.
> - Prikažite poveznice "Uredi" i "Obriši" na stranici knjige samo korisnicima koji tu radnju smiju napraviti.
> - Napravite stranicu `moje-knjige/` koja prijavljenom korisniku prikazuje knjige koje je on dodao.
> - Napravite stranicu profila (`accounts/profile/`) s korisničkim imenom, e-mail adresom, popisom grupa i poveznicom na promjenu lozinke.
> - Na početnoj stranici pomoću sesije prikažite koliko je puta korisnik posjetio stranicu.