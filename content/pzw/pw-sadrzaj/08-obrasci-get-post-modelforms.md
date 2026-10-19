---
author: Milan Petrović
title: "8. HTML obrasci, HTTP metode GET i POST te ModelForms"
layout: default
parent: PZW
nav_order: 8
has_children: false
has_toc: false
nav_exclude: false
---

# HTML obrasci, HTTP metode GET i POST te ModelForms
{: .no_toc }

<details open markdown="block">
  <summary>Sadržaj</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## HTML obrasci

Obrazac (engl. *form*) je način na koji korisnik šalje podatke poslužitelju. U HTML-u ga čini element `<form>` s poljima za unos:

``` html
<form action="/pretraga/" method="get">
    <label for="q">Pojam:</label>
    <input type="text" id="q" name="q">
    <button type="submit">Traži</button>
</form>
```

- `action` je adresa na koju se podaci šalju (ako se izostavi, šalju se na trenutnu adresu).
- `method` je HTTP metoda, `get` ili `post`.
- `name` je ime pod kojim poslužitelj prima vrijednost polja. Polje bez atributa `name` se ne šalje.

Nastavljamo s projektom `knjiznica` iz [poglavlja 7](07-genericki-pogledi.md).

## Metode GET i POST

| | GET | POST |
| --- | --- | --- |
| gdje su podaci | u URL-u, iza `?`, npr. `?q=django&page=2` | u tijelu zahtjeva |
| vidljivost | vidljivi u adresi, povijesti preglednika i zapisima poslužitelja | nisu u adresi |
| spremanje u oznake | moguće, adresa se može podijeliti | nije moguće |
| namjena | dohvat podataka bez promjene stanja: pretraga, filtriranje, straničenje | promjena stanja: unos, izmjena, brisanje, prijava |
| u Djangu | `request.GET` | `request.POST` (datoteke u `request.FILES`) |

Pravilo: **sve što mijenja podatke na poslužitelju šalje se metodom POST.** GET zahtjev mora biti siguran za ponavljanje. Preglednici i tražilice ga slobodno ponavljaju i unaprijed učitavaju.

## Obrazac za pretragu metodom GET

{: .zadatak }
> Dodajte na popis knjiga obrazac za pretragu koji pronalazi knjige čiji naslov ili ime autora sadrži upisani pojam.

**Rješenje zadatka.** Pogled `BookList` u `main/views.py` nadjačava `get_queryset()` i čita parametar `q` iz `request.GET`:

``` python
from django.db.models import Q
from django.views.generic import ListView

from .models import Book


class BookList(ListView):
    model = Book
    paginate_by = 5

    def get_queryset(self):
        queryset = Book.objects.select_related("author", "publisher")
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(author__name__icontains=q))
        return queryset
```

Na početak bloka `content` u `templates/main/book_list.html` dodajemo obrazac:

{% raw %}
``` django
<form method="get" action="{% url 'main:book_list' %}">
    <input type="search" name="q" value="{{ request.GET.q }}" placeholder="Naslov ili autor">
    <button type="submit">Traži</button>
</form>
```
{% endraw %}

Atributom `value` upisani pojam ostaje u polju nakon pretrage.

{% raw %}
Straničenje iz prethodnog poglavlja ima problem: poveznica `?page=2` gubi parametar `q`. Oznaka `querystring` (dostupna od Djanga 5.1) zadržava postojeće parametre i mijenja samo navedene:

``` django
{% if page_obj.has_next %}
    <a href="{% querystring page=page_obj.next_page_number %}">sljedeća &raquo;</a>
{% endif %}
```
{% endraw %}

{: .zadatak }
> Ispravite obje poveznice straničenja u `book_list.html` i provjerite da pretraga ostaje sačuvana pri prelasku na sljedeću stranicu.

## Django obrasci

Ručno čitanje `request.POST` brzo postaje naporno: treba provjeriti je li svako polje poslano, je li ispravnog formata, pretvoriti tekst u brojeve i datume, prikazati greške i ponovno popuniti polja. Djangova klasa `Form` sve to radi umjesto nas:

- generira HTML polja,
- provjerava (validira) podatke i pretvara ih u Python tipove,
- prikazuje poruke o greškama uz odgovarajuća polja.

Obrasce pišemo u datoteci `main/forms.py`:

``` python
from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label="Ime", max_length=100)
    email = forms.EmailField(label="E-mail")
    subject = forms.CharField(label="Naslov", max_length=150)
    message = forms.CharField(label="Poruka", widget=forms.Textarea)
    cc_myself = forms.BooleanField(label="Pošalji kopiju meni", required=False)
```

Polja obrasca slična su poljima modela. Argument `widget` određuje HTML element (ovdje `<textarea>` umjesto `<input>`), a sva polja su obavezna osim ako je zadano `required=False`.

### Obrada obrasca u pogledu

Pogled koji prikazuje i obrađuje obrazac ima uvijek isti oblik:

``` python
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)       # obrazac popunjen poslanim podacima
        if form.is_valid():
            name = form.cleaned_data["name"]    # provjereni podaci
            # ovdje bi se npr. poslala e-pošta
            messages.success(request, f"Hvala, {name}! Poruka je poslana.")
            return redirect("main:contact")
    else:
        form = ContactForm()                    # prazan obrazac

    return render(request, "main/contact.html", {"form": form})
```

``` python
path("kontakt/", views.contact, name="contact"),
```

Tijek je sljedeći:

1. Prvi posjet stranici je GET: prikazuje se prazan obrazac.
2. Korisnik ispuni obrazac i pošalje ga metodom POST.
3. Ako podaci nisu ispravni, `is_valid()` vraća `False`. Isti obrazac, sada s greškama i upisanim vrijednostima, ponovno se prikazuje.
4. Ako su ispravni, podatke čitamo iz `form.cleaned_data` (već pretvorene u Python tipove), obradimo ih i **preusmjerimo** korisnika.

{: .napomena }
> Preusmjeravanje nakon uspješnog POST zahtjeva zove se uzorak **Post/Redirect/Get**. Bez njega bi osvježavanje stranice ponovno poslalo obrazac, npr. dvaput naručilo isti proizvod. Zato nakon uspješne obrade uvijek vraćamo `redirect()`, a ne `render()`.

Predložak `templates/main/contact.html`:

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block content %}
<h2>Kontakt</h2>
<form method="post">
    {% csrf_token %}
    {{ form }}
    <button type="submit">Pošalji</button>
</form>
{% endblock %}
```
{% endraw %}

{% raw %}
Oznaka `{% csrf_token %}` obavezna je u svakom obrascu koji se šalje metodom POST. Ona umeće skriveno polje s tokenom kojim Django provjerava da je zahtjev poslan s naše stranice, a ne s tuđe (zaštita od CSRF napada, vidi [poglavlje 13](13-sigurnost.md)). Bez tokena Django odbija zahtjev s greškom 403.
{% endraw %}

### Poruke korisniku

Poruke dodane s `messages.success()` (ili `info`, `warning`, `error`) prikazuju se jednom, na sljedećoj stranici. Prikaz dodajemo u `base_generic.html` iznad bloka `content`:

{% raw %}
``` django
{% if messages %}
<ul class="messages">
    {% for message in messages %}
        <li class="{{ message.tags }}">{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}
```
{% endraw %}

## Prikaz obrasca u predlošku

{% raw %}
Najjednostavniji prikaz je `{{ form }}`, koji od Djanga 5.0 svako polje omata elementom `<div>`. Postoje i `{{ form.as_p }}`, `{{ form.as_ul }}` i `{{ form.as_table }}`.

Kada trebamo potpunu kontrolu nad izgledom, polja prikazujemo ručno:

``` django
<form method="post">
    {% csrf_token %}
    {{ form.non_field_errors }}

    {% for field in form %}
        <div class="field">
            {{ field.label_tag }}
            {{ field }}
            {% if field.help_text %}<small>{{ field.help_text }}</small>{% endif %}
            {{ field.errors }}
        </div>
    {% endfor %}

    <button type="submit">Pošalji</button>
</form>
```

Pojedinom polju pristupamo i po imenu, npr. `{{ form.email }}` i `{{ form.email.errors }}`, a `{{ form.email.as_field_group }}` ispisuje oznaku, polje, pomoćni tekst i greške zajedno.
{% endraw %}

## Validacija

Kada pozovemo `is_valid()`, Django za svako polje redom provjerava je li obavezno polje popunjeno, može li se vrijednost pretvoriti u odgovarajući tip (broj, datum, e-mail), prolazi li kroz ugrađena ograničenja (`max_length`, `min_value`...) i dodatne validatore. Na kraju poziva naše metode.

### Provjera jednog polja: `clean_<ime_polja>()`

``` python
class ContactForm(forms.Form):
    # ... polja kao gore ...

    def clean_message(self):
        message = self.cleaned_data["message"]
        if len(message.split()) < 5:
            raise forms.ValidationError("Poruka mora imati barem 5 riječi.")
        return message
```

Metoda mora vratiti (po potrebi izmijenjenu) vrijednost polja.

### Provjera više polja: `clean()`

Kada provjera ovisi o više polja, nadjačavamo `clean()`:

``` python
    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get("subject", "")
        message = cleaned_data.get("message", "")
        if subject and subject.lower() in message.lower():
            raise forms.ValidationError("Poruka ne smije samo ponavljati naslov.")
        return cleaned_data
```

Greške iz `clean()` nisu vezane uz jedno polje, pa se prikazuju kroz `form.non_field_errors`. Grešku možemo vezati uz određeno polje s `self.add_error("message", "...")`.

{: .upozorenje }
> Provjera u pregledniku (atributi `required`, `type="email"` i sl.) služi samo za udobnost korisnika i lako se zaobilazi. Prava provjera je uvijek ona na poslužitelju. Za isprobavanje provjere na poslužitelju elementu `<form>` privremeno dodajte atribut `novalidate`.

## ModelForm: obrasci iz modela

Obrazac za unos knjige imao bi ista polja kao model `Book`. Da ih ne bismo pisali dvaput, koristimo `ModelForm`, koji polja i validaciju preuzima iz modela. U `main/forms.py`:

``` python
from django import forms
from django.utils import timezone

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "abstract", "author", "publisher", "publication_date"]
        labels = {
            "title": "Naslov",
            "abstract": "Sažetak",
            "author": "Autor",
            "publisher": "Izdavač",
            "publication_date": "Datum izdanja",
        }
        widgets = {
            "publication_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def clean_publication_date(self):
        date = self.cleaned_data["publication_date"]
        if date > timezone.localdate():
            raise forms.ValidationError("Datum izdanja ne može biti u budućnosti.")
        return date
```

Polje `author` je `ForeignKey`, pa ga `ModelForm` prikazuje kao padajući izbornik svih autora. `DateInput` s `type="date"` u pregledniku prikazuje kalendar, a `format` osigurava da preglednik razumije postojeći datum pri uređivanju.

{: .upozorenje }
> Uvijek izričito navedite polja u `fields`. Postavka `fields = "__all__"` uključuje i polja koja korisnik ne bi smio mijenjati (npr. vlasnika zapisa ili oznaku "odobreno"). Napadač ih može poslati čak i ako ih nema u HTML-u.

### Stvaranje i uređivanje u funkcijskom pogledu

``` python
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm
from .models import Book


def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()               # stvara i sprema objekt
            return redirect(book)            # preusmjerava na book.get_absolute_url()
    else:
        form = BookForm()
    return render(request, "main/book_form.html", {"form": form})


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)  # mijenjamo postojeći objekt
        if form.is_valid():
            form.save()
            return redirect(book)
    else:
        form = BookForm(instance=book)                # obrazac popunjen podacima knjige
    return render(request, "main/book_form.html", {"form": form, "book": book})
```

Jedina razlika između stvaranja i uređivanja je argument `instance`. Ako treba nešto postaviti prije spremanja, koristi se `form.save(commit=False)`, zatim izmjena objekta, pa `book.save()`.

## Generički pogledi za uređivanje

Kao što `ListView` i `DetailView` skraćuju prikaz, `CreateView`, `UpdateView` i `DeleteView` skraćuju obradu obrazaca. Isti pogledi kao gore:

``` python
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import BookForm
from .models import Book


class BookCreate(SuccessMessageMixin, CreateView):
    model = Book
    form_class = BookForm
    success_message = "Knjiga „%(title)s” je dodana."


class BookUpdate(SuccessMessageMixin, UpdateView):
    model = Book
    form_class = BookForm
    success_message = "Knjiga „%(title)s” je izmijenjena."


class BookDelete(SuccessMessageMixin, DeleteView):
    model = Book
    success_url = reverse_lazy("main:book_list")
    success_message = "Knjiga je obrisana."
```

Nakon uspjeha `CreateView` i `UpdateView` preusmjeravaju na `get_absolute_url()` objekta, a `DeleteView` na `success_url`. Koristimo `reverse_lazy` jer se atributi klase izračunavaju pri učitavanju modula, kada URL-ovi još nisu učitani.

``` python
urlpatterns = [
    # ... postojeći URL-ovi ...
    path("knjige/nova/", views.BookCreate.as_view(), name="book_create"),
    path("knjige/<int:pk>/uredi/", views.BookUpdate.as_view(), name="book_update"),
    path("knjige/<int:pk>/obrisi/", views.BookDelete.as_view(), name="book_delete"),
    path("kontakt/", views.contact, name="contact"),
]
```

`CreateView` i `UpdateView` koriste zajednički predložak `main/book_form.html`:

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block content %}
<h2>{% if object %}Uredi knjigu{% else %}Nova knjiga{% endif %}</h2>
<form method="post">
    {% csrf_token %}
    {{ form }}
    <button type="submit">Spremi</button>
</form>
{% endblock %}
```
{% endraw %}

`DeleteView` na GET zahtjev prikazuje stranicu za potvrdu, a briše tek na POST. Predložak `main/book_confirm_delete.html`:

{% raw %}
``` django
{% extends "base_generic.html" %}

{% block content %}
<h2>Brisanje knjige</h2>
<p>Jeste li sigurni da želite obrisati knjigu „{{ object.title }}”?</p>
<form method="post">
    {% csrf_token %}
    <button type="submit">Da, obriši</button>
    <a href="{{ object.get_absolute_url }}">Odustani</a>
</form>
{% endblock %}
```
{% endraw %}

{: .napomena }
> Brisanje nikad ne radimo poveznicom (GET zahtjevom) poput `<a href="/knjige/5/obrisi/">`. Preglednik, dodatak za ubrzavanje ili tražilica mogu takvu poveznicu posjetiti i obrisati podatke.

{: .zadatak }
> Na stranicu s detaljima knjige (`book_detail.html`) dodajte poveznice za uređivanje i brisanje, a na popis knjiga poveznicu "Dodaj knjigu". Isprobajte sve tri radnje.

U [poglavlju 12](12-autentifikacija-autorizacija.md) ove ćemo poglede zaštititi tako da ih smiju koristiti samo prijavljeni korisnici s odgovarajućim ovlastima.

## Zadaci za vježbu

{: .zadatak }
> - Napravite `AuthorForm` i generičke poglede za dodavanje, uređivanje i brisanje autora. Polja s datumima prikažite s kalendarom.
> - U `AuthorForm` dodajte provjeru u metodi `clean()`: datum smrti, ako je upisan, ne smije biti prije datuma rođenja.
> - Napravite obrazac za pretragu izdavača po gradu i državi (dva polja, metoda GET).
> - Napravite obrazac `ContactForm` sa stranicom `kontakt/` i dodajte poveznicu na nju u izbornik. Provjerite što se dogodi ako iz predloška uklonite oznaku za CSRF token.