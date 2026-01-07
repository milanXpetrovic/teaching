---
parent: 'Interakcija s Korisnikom i Napredne Teme'
nav_order: 1
has_children: false
title: 'Poglavlje 6: Obrasci (Forms)'
---

# Poglavlje 6: Obrasci (Forms)

Do sada smo se bavili prikazivanjem podataka koje smo mi, kao developeri, unosili u bazu putem shella ili admin sučelja. Međutim, prava snaga web aplikacija leži u interakciji s korisnicima – omogućavanju da oni unose, mijenjaju i šalju podatke.

Za to koristimo HTML obrasce, a Django nam daje izuzetno moćan i siguran sustav za njihovu obradu: **Django Forms**.

## 6.1 HTML Obrasci i HTTP Metode (GET vs. POST)

U srcu svake forme je HTML `<form>` element. Ključna su dva atributa:
* `action`: URL na koji se podaci šalju na obradu.
* `method`: HTTP metoda koja se koristi za slanje. Dvije najvažnije su **GET** i **POST**.

### GET

* **Namjena:** Dohvaćanje podataka.
* **Kako radi:** Podaci iz forme se dodaju na kraj URL-a kao query parametri (npr. `?q=django&page=2`).
* **Kada koristiti:** Isključivo za akcije koje **ne mijenjaju stanje** na serveru, poput pretrage ili filtriranja.

### POST

* **Namjena:** Slanje podataka radi **stvaranja ili izmjene** resursa na serveru.
* **Kako radi:** Podaci se šalju u "tijelu" (body) HTTP zahtjeva i nisu vidljivi u URL-u.
* **Kada koristiti:** Uvijek kada forma mijenja podatke u bazi (kreiranje posta, registracija korisnika, uređivanje profila).

> **Two Scoops Pravilo:** Svaka forma koja mijenja podatke **MORA** koristiti `method="POST"`. Korištenje GET-a za takve operacije je nesigurno i protivno web standardima.

### CSRF Zaštita: `{% csrf_token %}`

Kada šaljete podatke putem POST metode, izlažete se sigurnosnom riziku zvanom **Cross-Site Request Forgery (CSRF)**. Django ima ugrađenu, automatsku zaštitu protiv ovoga.

Da bi zaštita radila, **svaka** vaša POST forma u templateu mora sadržavati `{% csrf_token %}` tag.

    <form method="post">
        {% csrf_token %}
        <!-- Ovdje idu polja forme -->
        <button type="submit">Pošalji</button>
    </form>

Ovaj tag generira skriveno (`hidden`) input polje s jedinstvenim tokenom. Django će prilikom obrade zahtjeva provjeriti je li taj token ispravan. Ako nije, ili ako nedostaje, zahtjev će biti odbijen.

---

## 6.2 Django Obrasci (Forms)

Ručno pisanje HTML formi i njihova validacija u viewu mogu biti naporni i podložni greškama. Django Forms sustav automatizira i pojednostavljuje ovaj proces.

Django forma je Python klasa koja:
1. **Generira HTML** za polja forme.
2. **Validira** poslane podatke.
3. **Prikazuje greške** korisniku.
4. **"Čisti"** podatke i pretvara ih u odgovarajuće Python tipove.

Postoje dva osnovna tipa formi: `forms.Form` i `forms.ModelForm`.

### `forms.ModelForm`: Kreiranje formi iz Modela

Ovo je najčešći i najkorisniji tip forme. `ModelForm` se automatski generira iz postojećeg Django **Modela**, preuzimajući njegova polja i osnovna pravila validacije.

Kreirajmo formu za dodavanje novog `Post` objekta u našoj blog aplikaciji.

1. Unutar `posts` aplikacije, stvorite novu datoteku `forms.py`.
2. U `posts/forms.py` dodajte sljedeći kod:

        # posts/forms.py
        from django import forms
        from .models import Post

        class PostForm(forms.ModelForm):
            class Meta:
                model = Post
                fields = ['title', 'content']

* `class PostForm(forms.ModelForm):` Nasljeđujemo `ModelForm`.
* `class Meta:` Unutarnja klasa koja sadrži meta-podatke o formi.
* `model = Post`: Govorimo formi da se bazira na našem `Post` modelu.
* `fields = ['title', 'content']`: Specificiramo koja polja iz modela želimo uključiti u formu.

### Obrada forme u Viewu

Sada nam treba view koji će prikazati i obraditi ovu formu. Najčešći uzorak je da isti view i prikazuje praznu formu (na GET zahtjev) i obrađuje poslane podatke (na POST zahtjev).

**Primjer s funkcijskim viewom (FBV):**

    # posts/views.py
    from django.shortcuts import render, redirect
    from .forms import PostForm

    def post_create(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                # Ovdje bi spremili post, ali ModelForm to radi za nas
                form.save()
                return redirect('post-list') # Preusmjeri na listu postova nakon uspjeha
        else:
            form = PostForm() # Prazna forma za GET zahtjev

        context = {
            'form': form
        }
        return render(request, 'posts/post_form.html', context)

* `form = PostForm(request.POST)`: Ako je metoda POST, kreiramo instancu forme i popunjavamo je s poslanim podacima.
* `form.is_valid()`: Ovo je magija! Ova metoda pokreće cijeli proces validacije. Provjerava jesu li sva obavezna polja popunjena, jesu li podaci ispravnog tipa, itd. Vraća `True` ili `False`.
* `form.save()`: Ako je forma validna, `ModelForm` ima `.save()` metodu koja automatski kreira ili ažurira odgovarajući objekt u bazi.

### Prikaz forme u Templateu

Sada nam treba `posts/post_form.html`:

    {% extends 'base.html' %}
    {% block content %}
      <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Spremi Post</button>
      </form>
    {% endblock %}

* `{{ form.as_p }}`: Django će automatski renderirati sva polja forme unutar `<p>` paragrafa, uključujući labele, inpute i eventualne greške validacije. Druge opcije su `.as_ul` (kao lista) i `.as_table` (kao tablica).

---

## 6.3 Generički Klasni bazirani Viewovi za forme (CBV Forms)

Kao i kod prikaza podataka, Django nudi generičke, klasne viewove koji drastično pojednostavljuju uobičajene operacije s formama.

* `CreateView`: Prikazuje i obrađuje formu za kreiranje novog objekta.
* `UpdateView`: Prikazuje i obrađuje formu za uređivanje postojećeg objekta.
* `DeleteView`: Prikazuje stranicu za potvrdu i obrađuje brisanje objekta.

Prepravimo naš `post_create` view koristeći `CreateView`.

**U `posts/views.py`:**

    # posts/views.py
    from django.views.generic import CreateView
    from .models import Post
    from .forms import PostForm
    from django.urls import reverse_lazy

    class PostCreateView(CreateView):
        model = Post
        form_class = PostForm
        template_name = 'posts/post_form.html'
        success_url = reverse_lazy('post-list')

I to je sve! Ova klasa od 5 linija koda radi **potpuno istu stvar** kao naša `post_create` funkcija. `CreateView` se sam brine o razlikovanju GET i POST zahtjeva, validaciji i spremanju.

* `model`: Model koji se kreira.
* `form_class`: Forma koja se koristi.
* `template_name`: Template koji će se renderirati.
* `success_url`: URL na koji će korisnik biti preusmjeren nakon uspješnog spremanja. Koristimo `reverse_lazy` jer se URL-ovi evaluiraju tek kada su potrebni.

Naravno, ne zaboravite ažurirati `posts/urls.py`:

    # posts/urls.py
    from .views import PostCreateView
    # ...

    urlpatterns = [
        # ...
        path('post/new/', PostCreateView.as_view(), name='post-create'),
    ]

---

Upravljanje formama je ključan dio svake web aplikacije. Iako se na prvi pogled može činiti komplicirano, Djangov Forms sustav, a posebno `ModelForm` i generički CBV-ovi, pružaju nevjerojatno moćan, siguran i efikasan način za obradu korisničkog unosa, omogućujući vam da se fokusirate na specifičnu logiku vaše aplikacije.