---
parent: 'Django Temelji: Od Projekta do Prve Aplikacije'
nav_order: 4
title: '2.4 Dokumentacija i Debugging'
---

# 2.4 Dokumentacija i Debugging

Kreirali smo projekt i prvu aplikaciju. Prije nego što zaronimo dublje u pisanje koda, važno je usvojiti dvije vještine koje će vam uštedjeti sate (ako ne i dane) frustracije: **učinkovito korištenje dokumentacije** i **osnovne tehnike debugginga**.

Profesionalni razvoj softvera nije samo pisanje koda; velik dio vremena provodi se u čitanju, istraživanju i rješavanju problema.

## Umjetnost Korištenja Dokumentacije

Nitko ne zna sve napamet. Odlika dobrog developera nije pamćenje svake funkcije, već znanje gdje i kako brzo pronaći točnu informaciju.

### 1. Službena Django Dokumentacija

**Ovo je vaš najvažniji resurs.** Djangova dokumentacija je poznata kao jedna od najboljih u svijetu softvera – detaljna je, precizna i puna primjera.

* **Link:** [https://docs.djangoproject.com/](https://docs.djangoproject.com/)

**Kako je koristiti?**
* **Tutorial:** Ako ste potpuni početnik, službeni tutorial je odlično mjesto za početak.
* **Tematski vodiči (Topic guides):** Kada želite naučiti o nekom konceptu u dubinu (npr. "kako rade forme" ili "kako se spojiti na PostgreSQL"), ovo je vaša sekcija.
* **Referentni vodiči (Reference guides):** Kada znate što tražite, ali trebate točne detalje o nekoj funkciji, klasi ili postavci (npr. "koje sve opcije prima `CharField`?"), idete ovdje.

> Naviknite se tražiti odgovore prvo u službenoj dokumentaciji. To je najpouzdaniji izvor informacija.

### 2. Stack Overflow

Stack Overflow je najveća Q&A (pitanja i odgovori) zajednica za programere. Gotovo svaki problem na koji naiđete, netko je već imao i vjerojatno riješio.

**Kako ga koristiti?**
* **Pretraživanje:** Kada dobijete grešku, kopirajte ključni dio poruke o grešci i zalijepite je u Google, često dodajući "django" na kraj. Prvih nekoliko rezultata će gotovo sigurno biti sa Stack Overflowa.
* **Pitanje:** Ako ne možete pronaći rješenje, možete postaviti svoje pitanje.

> **Two Scoops Savjet: Kako postaviti dobro pitanje?**
>
> Da biste dobili brz i koristan odgovor, vaše pitanje mora biti jasno. Uvijek uključite:
>
> 1. **Što pokušavate postići?** (Kontekst)
> 2. **Što ste već probali?** (Pokažite svoj kod)
> 3. **Kakvu grešku dobivate?** (Kopirajte **cijeli** traceback)
> 4. **Što ste očekivali da će se dogoditi?**
>
> Pitanja bez koda ili poruke o grešci se najčešće ignoriraju.

## Debugging: Kada Stvari Pođu po Zlu

Pisanje koda bez grešaka je mit. Debugging (otklanjanje grešaka) je normalan i neizbježan dio procesa. Srećom, Django vam daje moćne alate za to.

### 1. Djangova Stranica za Debugging ("Žuti Ekran Smrti")

Kada se u vašem kodu dogodi greška dok je `DEBUG = True` u `settings.py`, Django će u pregledniku prikazati detaljnu stranicu s informacijama o grešci. Nemojte je se bojati – ona je vaš najbolji prijatelj!

Ključni dijelovi ove stranice su:
* **Traceback:** Ovo je najvažniji dio. To je detaljan ispis poziva funkcija, korak po korak, koji je doveo do greške. **Čitajte ga odozdo prema gore!** Na samom dnu je točna greška (npr. `NameError: name 'my_variable' is not defined`), a redci iznad vam pokazuju točno u kojoj datoteci i liniji koda se greška dogodila.
* **Lokalne varijable:** Za svaki korak u tracebacku, Django vam pokazuje vrijednosti svih lokalnih varijabli u tom trenutku. To je neprocjenjivo za razumijevanje stanja vaše aplikacije u trenutku greške.

> **SIGURNOSNO UPOZORENJE:** `DEBUG` mora **UVIJEK** biti postavljen na `False` u produkcijskom okruženju! Prikazivanje ove stranice na javnoj web stranici je ogroman sigurnosni rizik jer otkriva osjetljive informacije o vašem kodu i konfiguraciji.

### 2. Dobri, stari `print()`

Najjednostavnija tehnika debugginga na svijetu je ispisivanje vrijednosti varijabli u konzolu.

Ako želite provjeriti vrijednost nečega unutar vašeg `view`-a, jednostavno dodajte `print()`:

    # posts/views.py
    from django.http import HttpResponse

    def home(request):
        my_variable = "Testna vrijednost"
        print("VRIJEDNOST VARIJABLE JE:", my_variable)
        return HttpResponse("Pozdrav iz Posts aplikacije!")

Kada sada osvježite stranicu u pregledniku, u **terminalu** u kojem ste pokrenuli `runserver` vidjet ćete ispis:

    VRIJEDNOST VARIJABLE JE: Testna vrijednost

Ovo je brz i "prljav" način da provjerite vrijednosti, ali je izuzetno koristan za brze provjere.

---

Usvajanje ovih osnovnih vještina – čitanja dokumentacije i razumijevanja Djangove debug stranice – postavit će vas na pravi put. S ovim alatima, spremni ste se suočiti s izazovima koji slijede dok gradimo funkcionalnosti naše aplikacije.

Sljedeći korak: zaranjamo u MVT arhitekturu i počinjemo s **Modelima**.
