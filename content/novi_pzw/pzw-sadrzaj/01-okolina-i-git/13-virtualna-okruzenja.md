---
parent: Razvojna Okolina i Git
nav_order: 3
title: 1.3 Virtualna Okruženja (venv)
---

# 1.3 Virtualna Okruženja (venv)

Sada kada imamo Python i znamo osnove terminala, vrijeme je da naučimo jedan od najvažnijih koncepata u modernom Python razvoju: **virtualna okruženja**.

## Problem: Pakao zavisnosti (Dependency Hell)

Zamislimo da radite na dva Django projekta:

* **Projekt A** je stariji projekt koji zahtijeva `Django verziju 3.2`.
* **Projekt B** je novi projekt koji želite započeti s najnovijom `Django verzijom 4.1`.

Ako biste globalno na svom računalu instalirali Django (`pip install django`), mogli biste imati samo **jednu** verziju. Instalacija verzije 4.1 bi "pregazila" verziju 3.2, što bi moglo slomiti Projekt A. Pokušaj vraćanja na 3.2 bi slomio Projekt B. Ovo se zove "pakao zavisnosti".

## Rješenje: Izolacija s `venv`

Virtualno okruženje je **izolirani direktorij** koji sadrži specifičnu verziju Pythona i sve pakete (biblioteke) potrebne samo za taj jedan, specifični projekt.

**Prednosti:**

* **Izolacija:** Svaki projekt ima svoje pakete i njihove verzije, neovisno o drugima.
* **Čistoća:** Vaš globalni Python ostaje čist, bez stotina paketa.
* **Prenosivost:** Lako je replicirati točno okruženje na drugom računalu (npr. kolege u timu ili na produkcijskom serveru) pomoću datoteke `requirements.txt`.

Python dolazi s ugrađenim modulom za stvaranje virtualnih okruženja koji se zove `venv`.

---

## Rad s `venv`: Praktični koraci

Proces uvijek slijedi ista tri koraka: **1. Stvori**, **2. Aktiviraj**, **3. Koristi**.

### Korak 1: Stvaranje virtualnog okruženja

1. Pomoću terminala, navigirajte do direktorija gdje želite započeti svoj novi projekt (`cd putanja/do/projekata`).
2. Stvorite direktorij za projekt: `mkdir moj-django-projekt`.
3. Uđite u taj direktorij: `cd moj-django-projekt`.
4. Sada, unutar direktorija projekta, stvorite virtualno okruženje. Uobičajena konvencija je nazvati ga `venv`.

    ```bash
    # Na macOS/Linux
    python3 -m venv venv

    # Na Windows
    python -m venv venv
    ```

    Ova naredba će stvoriti novi direktorij naziva `venv` unutar `moj-django-projekt`. Unutar `venv` direktorija nalazi se kopija Pythona i `pip`-a.

### Korak 2: Aktiviranje virtualnog okruženja

Stvaranje okruženja nije dovoljno; moramo ga "uključiti" ili **aktivirati** za našu trenutnu terminalsku sesiju.

* **Na macOS/Linux:**

```bash
source venv/bin/activate
```

* **Na Windows (PowerShell):**

```bash
.\venv\Scripts\activate
```

Nakon aktivacije, primijetit ćete da se vaš terminalski prompt promijenio i sada ispred njega piše `(venv)`. To je znak da je virtualno okruženje aktivno!

```bash
(venv) korisnik@racunalo:~/projekti/moj-django-projekt$
```

### Korak 3: Korištenje i instalacija paketa

Sada kada je (`venv`) aktivan, svaka pip naredba će instalirati pakete **samo unutar ovog okruženja**.

Instalirajmo Django:

```bash
pip install django
```

Django će sada biti instaliran unutar `moj-django-projekt/venv/` i neće utjecati na vaš globalni Python ili druge projekte.

### Korak 4: Deaktivacija

Kada završite s radom na projektu, možete deaktivirati virtualno okruženje jednostavnom naredbom:

```bash
deactivate
```

Prompt će se vratiti u normalno stanje, a pip će opet pokazivati na globalne pakete.

### Upravljanje zavisnostima: `requirements.txt`

Kako bismo znali koji su sve paketi instalirani u našem okruženju i kako bismo omogućili drugima da postave identično okruženje, koristimo datoteku requirements.txt.

1. Generiranje datoteke: Dok je vaše virtualno okruženje aktivno, pokrenite:
  
    ```bash  
    pip freeze > requirements.txt
    ```

    Ovo će stvoriti datoteku requirements.txt sa popisom svih instaliranih paketa i njihovih točnih verzija.

2. Instalacija iz datoteke: Kada netko drugi (ili vi na drugom računalu) preuzme vaš projekt, trebat će samo stvoriti i aktivirati novo virtualno okruženje te pokrenuti:
  
    ```bash
        pip install -r requirements.txt
    ```
  
    Ova naredba će automatski instalirati sve pakete navedene u datoteci.

**Dobra praksa**: Uvijek koristite virtualno okruženje za svaki novi Python projekt, bez iznimke. To je temelj profesionalnog i organiziranog razvoja.
