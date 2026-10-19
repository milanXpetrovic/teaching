---
author: Milan Petrović
title: "13. Sigurnost Django web aplikacija"
layout: default
parent: PZW
nav_order: 13
has_children: false
has_toc: true
nav_exclude: true
---

# Sigurnost Django web aplikacija
{: .no_toc }

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Uvod

Web aplikacija je izložena svima na internetu, uključujući automatizirane alate koji neprestano traže poznate propuste. Django ima ugrađenu zaštitu od najčešćih napada, ali ona radi samo ako je ne isključimo i ako aplikaciju ispravno konfiguriramo.

Popis najčešćih sigurnosnih rizika web aplikacija održava organizacija OWASP ([OWASP Top 10](https://owasp.org/www-project-top-ten/)). U tablici su neki od tih rizika i kako ih Django ublažava:

| Rizik | Zaštita u Djangu | Odjeljak |
| ----- | ---------------- | -------- |
| neispravna kontrola pristupa | `login_required`, ovlasti, filtriranje upita po korisniku | [Kontrola pristupa](#kontrola-pristupa) |
| injekcija (SQL) | ORM s parametriziranim upitima | [SQL injekcija](#sql-injekcija) |
| XSS | automatsko zaštićivanje u predlošcima, CSP | [XSS](#cross-site-scripting-xss) |
| neispravna konfiguracija | `check --deploy`, `DEBUG = False` | [Postavke za produkciju](#postavke-za-produkciju) |
| propusti u autentifikaciji | sažeci lozinki, validatori lozinki | [Lozinke](#lozinke) |
| ranjive komponente | ažuriranje ovisnosti | [Ovisnosti](#ovisnosti-i-azuriranja) |

## Tajni podaci izvan koda

{: .opasnost }
> Pazite da `SECRET_KEY` ne bude javno vidljiv, npr. na GitHubu. Njime se potpisuju kolačići sesije, tokeni za obnovu lozinke i drugi podaci. Zlonamjerni pojedinac s tim ključem može se lažno predstaviti kao bilo koji korisnik, uključujući administratora, i upravljati vašom stranicom.

Isto vrijedi za lozinke baze podataka, API ključeve i slično. Takve vrijednosti čitamo iz **varijabli okruženja**, a ne pišemo u kod:

``` python
import os

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
```

Za vrijeme razvoja varijable se obično drže u datoteci `.env` koja se **ne** stavlja u Git (vidi [poglavlje 15](15-timski-razvoj-git-dokumentacija.md)). Paketi poput `django-environ` ili `python-decouple` tu datoteku učitavaju automatski:

``` text
# .env
DJANGO_SECRET_KEY=ovdje-dugacak-nasumicni-niz
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

Novi tajni ključ generirate naredbom:

``` shell
$ python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

{: .upozorenje }
> Ako je ključ ikada bio u javnom repozitoriju, smatrajte ga kompromitiranim i zamijenite ga. Brisanje iz zadnjeg commita ne pomaže jer ostaje u povijesti.

## Postavke za produkciju

### `DEBUG = False`

S `DEBUG = True` Django pri grešci prikazuje stranicu s izvornim kodom, postavkama, SQL upitima i varijablama okruženja. To je izvrsno za razvoj i katastrofalno u produkciji. Kada je `DEBUG = False`, obavezno je postaviti `ALLOWED_HOSTS` na domene na kojima stranica radi, npr. `["knjiznica.example.com"]`.

### Provjera postavki

Django ima ugrađenu provjeru sigurnosnih postavki:

``` shell
$ python manage.py check --deploy
```

{: .zadatak }
> Pokrenite `python manage.py check --deploy` na projektu `knjiznica` i pročitajte upozorenja. Za svako upozorenje pronađite u [dokumentaciji](https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/) što znači.

### HTTPS i kolačići

U produkciji sav promet mora ići preko HTTPS-a. Uobičajene postavke:

``` python
SECURE_SSL_REDIRECT = True            # HTTP zahtjevi se preusmjeravaju na HTTPS
SESSION_COOKIE_SECURE = True          # kolačić sesije šalje se samo preko HTTPS-a
CSRF_COOKIE_SECURE = True             # isto za CSRF kolačić
SECURE_HSTS_SECONDS = 31536000        # preglednik godinu dana koristi samo HTTPS
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

{: .upozorenje }
> HSTS je teško poništiti: preglednici koji su primili zaglavlje odbijat će HTTP veze do isteka zadanog vremena. Prvo ga isprobajte s malom vrijednošću (npr. 3600 sekundi).

Kolačić sesije je zadano `HttpOnly`, pa mu JavaScript ne može pristupiti. To otežava krađu sesije putem XSS-a.

## Cross-Site Request Forgery (CSRF)

Kod CSRF napada zlonamjerna stranica natjera preglednik prijavljenog korisnika da pošalje zahtjev našoj aplikaciji. Preglednik uz taj zahtjev automatski šalje kolačić sesije, pa bi aplikacija mislila da je zahtjev poslao korisnik. Primjer: skriveni obrazac na tuđoj stranici koji šalje `POST /knjige/5/obrisi/`.

Django se brani `CsrfViewMiddleware`-om: svaki POST, PUT, PATCH i DELETE zahtjev mora sadržavati tajni token koji tuđa stranica ne može znati.

{% raw %}
- U obrascima token dodaje oznaka `{% csrf_token %}`.
- Kod zahtjeva iz JavaScripta token se šalje u zaglavlju `X-CSRFToken`, a vrijednost se čita iz kolačića `csrftoken`.
{% endraw %}

Zaštita radi samo ako se **promjene stanja nikad ne rade GET zahtjevom** (vidi [poglavlje 8](08-obrasci-get-post-modelforms.md#metode-get-i-post)).

{: .opasnost }
> Dekorator `@csrf_exempt` isključuje zaštitu za pogled. Ne koristite ga kako biste "riješili" grešku 403, nego pronađite zašto token nedostaje.

## Cross-Site Scripting (XSS)

Kod XSS napada napadač u stranicu ubaci vlastiti JavaScript, npr. kroz komentar ili naslov knjige. Kada drugi korisnik otvori stranicu, skripta se izvršava u njegovom pregledniku s njegovim ovlastima.

{% raw %}
Django predlošci sve varijable automatski zaštićuju: naslov `<script>alert(1)</script>` prikazuje se kao tekst. Zaštita se gubi ako je sami isključimo:

``` django
{{ book.abstract|safe }}            {# OPASNO ako je sažetak upisao korisnik #}
{% autoescape off %}...{% endautoescape %}  {# isto #}
```
{% endraw %}

I u Pythonu treba paziti:

``` python
from django.utils.html import format_html
from django.utils.safestring import mark_safe

# OPASNO: korisnikov unos označen kao siguran HTML
html = mark_safe(f"<b>{book.title}</b>")

# ISPRAVNO: format_html zaštićuje umetnute vrijednosti
html = format_html("<b>{}</b>", book.title)
```

### Content Security Policy

Dodatni sloj zaštite je zaglavlje **Content-Security-Policy** (CSP), kojim pregledniku kažemo s kojih izvora smije učitavati skripte, stilove i slike. Čak i kada napadač uspije ubaciti `<script>`, preglednik ga ne izvršava jer nije s dopuštenog izvora. Od Djanga 6.0 podrška za CSP je ugrađena:

``` python
from django.utils.csp import CSP

MIDDLEWARE = [
    # ...
    "django.middleware.csp.ContentSecurityPolicyMiddleware",
]

SECURE_CSP = {
    "default-src": [CSP.SELF],
    "script-src": [CSP.SELF, CSP.NONCE],
    "img-src": [CSP.SELF, "data:"],
}
```

{% raw %}
Uz kontekstni procesor `django.template.context_processors.csp`, dopušteni ugrađeni (inline) skriptni blokovi označavaju se jednokratnom vrijednošću: `<script nonce="{{ csp_nonce }}">`. Novu politiku najprije isprobajte s postavkom `SECURE_CSP_REPORT_ONLY`, koja prekršaje samo prijavljuje, a ne blokira ([dokumentacija](https://docs.djangoproject.com/en/6.1/howto/csp/)).
{% endraw %}

## SQL injekcija

Kod SQL injekcije napadač podacima mijenja strukturu SQL upita. ORM sve vrijednosti šalje bazi kao parametre, odvojeno od samog upita, pa je ovaj kod siguran bez obzira na sadržaj varijable `q`:

``` python
Book.objects.filter(title__icontains=q)
```

Opasnost nastaje kod ručno pisanog SQL-a:

``` python
# OPASNO: q = "' OR '1'='1" vraća sve knjige, a gore su moguće i druge radnje
Book.objects.raw(f"SELECT * FROM main_book WHERE title = '{q}'")

# ISPRAVNO: vrijednost se predaje kao parametar
Book.objects.raw("SELECT * FROM main_book WHERE title = %s", [q])
```

Isto vrijedi za `cursor.execute()`, `extra()` i `RawSQL`: nikad ne slažite SQL f-stringom, `+` ili `%` operatorom.

## Clickjacking

Kod clickjackinga napadač našu stranicu učita u nevidljivi `<iframe>` na svojoj stranici i navede korisnika da klikne na gumb koji ne vidi. Middleware `XFrameOptionsMiddleware` (zadano uključen) šalje zaglavlje `X-Frame-Options: DENY` koje pregledniku zabranjuje prikaz stranice u okviru na drugoj domeni.

## Kontrola pristupa

Neispravna kontrola pristupa jedan je od najčešćih stvarnih propusta. Tipičan primjer je **IDOR** (engl. *Insecure Direct Object Reference*): korisnik promijeni broj u adresi `/narudzbe/1001/` u `/narudzbe/1002/` i vidi tuđu narudžbu.

``` python
# OPASNO: provjerava se samo je li korisnik prijavljen
@login_required
def narudzba(request, pk):
    narudzba = get_object_or_404(Narudzba, pk=pk)

# ISPRAVNO: objekt se traži samo među korisnikovim narudžbama
@login_required
def narudzba(request, pk):
    narudzba = get_object_or_404(Narudzba, pk=pk, kupac=request.user)
```

Pravila:

- Svaki pogled koji nije javan mora provjeravati prijavu i ovlasti (vidi [poglavlje 12](12-autentifikacija-autorizacija.md)). Razmislite o `LoginRequiredMiddleware`.
- Skrivanje gumba u predlošku nije zaštita.
- Obrasci i serializatori moraju izričito navoditi polja (`fields = [...]`), nikad `"__all__"`. Inače napadač može poslati i polja poput `added_by` ili `is_staff`.
- Administratorsko sučelje premjestite s predvidljive adrese `/admin/` i dajte pristup samo osobama koje ga trebaju.

## Lozinke

Django lozinke nikad ne sprema u čistom obliku, nego kao sažetak dobiven algoritmom PBKDF2 s nasumičnom soli i velikim brojem iteracija. Snažniji algoritam Argon2 može se uključiti instalacijom paketa `argon2-cffi` i postavkom:

``` python
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]
```

Postojeće lozinke se automatski prebacuju na novi algoritam pri sljedećoj prijavi korisnika.

Postavka `AUTH_PASSWORD_VALIDATORS` određuje pravila za nove lozinke: minimalnu duljinu, sličnost s korisničkim imenom, popis čestih lozinki i lozinke sastavljene samo od brojeva.

Django ne ograničava broj neuspjelih prijava. Za zaštitu od pogađanja lozinki (engl. *brute force*) koristi se paket [django-axes](https://django-axes.readthedocs.io/), koji zaključava račun ili IP adresu nakon zadanog broja neuspjelih pokušaja.

## Učitane datoteke

Datoteke koje šalju korisnici obrađene su u [poglavlju 10](10-static-i-multimedija.md#sigurnost-ucitanih-datoteka). Ukratko: ograničite vrstu i veličinu, ne vjerujte imenu ni nastavku datoteke, ne dopuštajte HTML i SVG koji bi se prikazivali na vašoj domeni i nikad ne izvršavajte učitane datoteke.

## Ovisnosti i ažuriranja
{: #ovisnosti-i-azuriranja }

Sigurnosni propusti redovito se otkrivaju i u Djangu i u paketima koje koristimo. Django tim ih ispravlja u sigurnosnim izdanjima, pa je bitno:

- koristiti podržanu verziju Djanga (popis na [stranici za preuzimanje](https://www.djangoproject.com/download/)),
- redovito ažurirati pakete,
- provjeravati poznate ranjivosti alatom `pip-audit`:

``` shell
$ python -m pip install pip-audit
$ pip-audit -r requirements.txt
```

## Zapisivanje događaja

Kada se dogodi napad, zapisi (engl. *logs*) su često jedini trag. Zapisujte neuspjele prijave, odbijene zahtjeve i greške, ali **nikad** lozinke, tokene ni druge osjetljive podatke. Django zapisivanje konfigurira postavkom `LOGGING` ([dokumentacija](https://docs.djangoproject.com/en/6.1/topics/logging/)).

## Zadaci za vježbu

{: .zadatak }
> - Premjestite `SECRET_KEY`, `DEBUG` i `ALLOWED_HOSTS` projekta `knjiznica` u varijable okruženja učitane iz datoteke `.env`. Dodajte `.env` u `.gitignore`, a u repozitorij stavite `.env.example` bez stvarnih vrijednosti.
> - U predlošku `book_detail.html` privremeno dodajte filter `safe` na sažetak, kroz administratorsko sučelje upišite sažetak `<script>alert("XSS")</script>` i otvorite stranicu knjige. Zatim uklonite filter i ponovite.
> - Napišite pogled koji pretražuje knjige pomoću `Book.objects.raw()` sa f-stringom i pokažite da upis `' OR '1'='1` vraća sve knjige. Ispravite pogled.
> - Uključite CSP u načinu `SECURE_CSP_REPORT_ONLY` i u konzoli preglednika pronađite prijavljene prekršaje (npr. CSS s CDN-a iz [poglavlja 10](10-static-i-multimedija.md)).
> - Prijavite se kao korisnik koji nije dodao neku knjigu i pokušajte je urediti upisivanjem adrese `/knjige/<pk>/uredi/`. Provjerite da dobivate odgovor 404.