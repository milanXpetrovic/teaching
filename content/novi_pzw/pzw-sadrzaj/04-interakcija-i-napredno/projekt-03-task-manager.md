---
parent: 'Interakcija s Korisnikom i Napredne Teme'
nav_order: 5
title: 'Projekt: Task Manager s CRUD operacijama'
---

# Samostalni Projekt: Task Manager s Autentikacijom i CRUD operacijama

U prethodnom projektu izgradili smo aplikaciju za prikazivanje podataka. Sada idemo korak dalje i gradimo potpuno interaktivnu aplikaciju gdje će korisnici moći upravljati vlastitim podacima. Izgradit ćemo jednostavan **Task Manager** (aplikaciju za upravljanje zadacima).

**Cilj projekta:** Stvoriti web aplikaciju u kojoj se korisnici mogu registrirati, prijaviti i upravljati vlastitom listom zadataka. Svaki korisnik smije vidjeti i uređivati samo svoje zadatke.

Ovaj projekt će vas provesti kroz cijeli **CRUD** (Create, Read, Update, Delete) ciklus i integrirati Djangov sustav autentikacije i autorizacije.

---

## Priprema Projekta

1. Kreirajte novi Django projekt (npr. `taskmanager`).
2. Unutar projekta, kreirajte novu aplikaciju naziva `tasks`.
3. Dodajte `'tasks.apps.TasksConfig'` u `INSTALLED_APPS` u `settings.py`.
4. Konfigurirajte URL-ove tako da glavni `urls.py` uključuje `django.contrib.auth.urls` (za login/logout) i `urls.py` iz vaše `tasks` aplikacije.
5. Postavite `LOGIN_REDIRECT_URL` i `LOGOUT_REDIRECT_URL` u `settings.py`.

## Faza 1: Model i Admin

Prvo, moramo definirati kako će zadatak (`Task`) izgledati u bazi podataka.

**Zadatak:**

1. Otvorite `tasks/models.py`.
2. Kreirajte model `Task` sa sljedećim poljima:
    * `title`: `CharField` s maksimalnom duljinom 150.
    * `description`: `TextField`, može biti prazan (`blank=True`).
    * `completed`: `BooleanField`, sa zadanom vrijednošću `False`.
    * `created_at`: `DateTimeField` koji automatski postavlja datum i vrijeme kreiranja.
    * `user`: `ForeignKey` veza prema Djangovom `User` modelu. Svaki zadatak mora imati vlasnika. Razmislite o `on_delete` opciji.
3. Definirajte `__str__` metodu da vraća naslov zadatka.
4. **Bonus:** Definirajte `get_absolute_url` metodu koja će vraćati URL do detaljnog prikaza tog zadatka. Ovo će nam kasnije pojednostaviti preusmjeravanja.
5. Napravite i primijenite migracije.
6. Registrirajte `Task` model u `tasks/admin.py` kako biste mogli lako dodavati testne podatke.

## Faza 2: CRUD - Read (Čitanje podataka)

Prvo ćemo napraviti stranice za prikaz liste zadataka i detalja jednog zadatka. Važno je osigurati da korisnici vide **samo svoje zadatke**.

**Zadatak:**

1. **View za listu zadataka (`TaskListView`):**
    * U `tasks/views.py`, kreirajte `TaskListView` koji nasljeđuje `LoginRequiredMixin` i `ListView`.
    *   Povežite ga s `Task` modelom i kreirajte odgovarajući template (`tasks/task_list.html`).
    * **Ključni dio:** Nadjačajte (`override`) metodu `get_queryset(self)`. Unutar te metode, vratite samo one zadatke koji pripadaju trenutno prijavljenom korisniku (`self.request.user`).
    * Poredajte zadatke tako da se prvo prikažu oni koji nisu dovršeni.

2. **Template za listu zadataka (`task_list.html`):**
    * Prikažite listu zadataka. Za svaki zadatak, prikažite njegov naslov i status (dovršen/nedovršen).
    * Naslov svakog zadatka neka bude link koji vodi na stranicu s detaljima tog zadatka.
    * Dodajte link/gumb "Novi zadatak" koji vodi na stranicu za kreiranje.

3. **View za detalje zadatka (`TaskDetailView`):**
    * Kreirajte `TaskDetailView` (`LoginRequiredMixin`, `DetailView`).
    * Povežite ga s `Task` modelom i templateom (`tasks/task_detail.html`).
    * **Autorizacija:** Budući da `DetailView` po defaultu dohvaća bilo koji objekt, moramo osigurati da korisnik može vidjeti detalje samo **svog** zadatka. Najlakši način je nadjačati `get_queryset` na isti način kao i u `ListView`.

4. **Povežite URL-ove** za listu i detalje u `tasks/urls.py`.

## Faza 3: CRUD - Create (Stvaranje podataka)

Omogućimo korisnicima da sami dodaju nove zadatke.

**Zadatak:**

1. **Forma (`TaskForm`):**
    * U `tasks/forms.py`, kreirajte `TaskForm` klasu koja nasljeđuje `forms.ModelForm`.
    * U `Meta` klasi, povežite je s `Task` modelom i uključite samo polja `title` i `description`. Polja `user` i `completed` ne smiju biti direktno vidljiva korisniku na ovoj formi.

2. **View za kreiranje zadatka (`TaskCreateView`):**
    * U `tasks/views.py`, kreirajte `TaskCreateView` (`LoginRequiredMixin`, `CreateView`).
    * Povežite ga s `Task` modelom, `TaskForm` formom i `tasks/task_form.html` templateom.
    * Postavite `success_url` da preusmjerava na listu zadataka.
    * **Ključni dio:** `CreateView` ne zna kojeg korisnika treba dodijeliti novom zadatku. Moramo mu pomoći. Nadjačajte metodu `form_valid(self, form)`. Unutar te metode, prije nego što pozovete `super().form_valid(form)`, postavite autora zadatka: `form.instance.user = self.request.user`.

3. **Template za formu (`task_form.html`):**
    * Kreirajte generički template za prikaz forme koji se može koristiti i za kreiranje i za uređivanje. Prikazat će formu unutar `<form method="post">` taga s `{% csrf_token %}`.

4. **Povežite URL** za kreiranje zadatka.

## Faza 4: CRUD - Update i Delete (Izmjena i Brisanje)

Sada dodajmo funkcionalnost za uređivanje i brisanje postojećih zadataka.

**Zadatak:**

1. **View za uređivanje zadatka (`TaskUpdateView`):**
    * Kreirajte `TaskUpdateView` (`LoginRequiredMixin`, `UpdateView`).
    * Povežite ga s modelom, formom i `task_form.html` templateom.
    * Postavite `success_url`.
    * **Autorizacija:** Kao i kod `DetailView`, morate osigurati da korisnik može uređivati samo svoje zadatke. Opet, nadjačajte `get_queryset`.

2. **View za brisanje zadatka (`TaskDeleteView`):**
    * Kreirajte `TaskDeleteView` (`LoginRequiredMixin`, `DeleteView`).
    * Povežite ga s modelom i postavite `success_url`.
    * Django će automatski tražiti template `tasks/task_confirm_delete.html`. Kreirajte ga. Taj template treba prikazati poruku za potvrdu i formu s gumbom "Potvrdi brisanje".
    * **Autorizacija:** I ovdje je nužno nadjačati `get_queryset`.

3. **Povežite URL-ove** za `update` i `delete` viewove. Oni će, kao i `detail`, očekivati `pk` u URL-u.

## Faza 5: "Uljepšavanje"

Sada kada sve radi, poboljšajte korisničko iskustvo.

**Zadatak:**

* Na `TaskDetailView` stranici, dodajte linkove/gumbe "Uredi" i "Obriši".
* Prilagodite `base.html` i dodajte navigaciju.
* Koristeći `if` uvjete u templateima, prilagodite prikaz. Na primjer, prekrižite naslov zadatka ako je `task.completed` `True`.
* **Bonus:** Umjesto `UpdateView` za označavanje zadatka kao dovršenog, pokušajte napraviti poseban, jednostavniji view koji na POST zahtjev samo promijeni `completed` status i preusmjeri korisnika natrag na listu.

---

### Završna provjera

Testirajte cijeli tijek rada:

1. Registrirajte dva različita korisnika.
2. Prijavite se kao prvi korisnik i dodajte nekoliko zadataka.
3. Odjavite se i prijavite kao drugi korisnik. On **ne smije** vidjeti zadatke prvog korisnika.
4. Pokušajte ručno u URL upisati putanju do detalja, uređivanja ili brisanja zadatka prvog korisnika. Trebali biste dobiti `404 Not Found` grešku (jer `get_queryset` ne pronalazi objekt za tog korisnika).

Čestitamo! Uspješno ste izgradili kompletnu CRUD aplikaciju s ispravnom autentikacijom i autorizacijom, koristeći najbolje prakse i generičke viewove koje Django nudi.