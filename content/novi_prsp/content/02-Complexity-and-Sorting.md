---
nav_exclude: true
parent: PRSP
layout: default 
nav_order: 2
---

# Analiza složenosti i sortiranje

## Sadržaj

* [**Tjedan 2: Analiza Složenosti i Sortiranje**](#analiza-složenosti-i-sortiranje)
  * [Uvod i Motivacija](#uvod-i-motivacija)
  * [Primjeri Zadataka i Objašnjenja](#primjeri-zadataka-i-objašnjenja)
    * [Problem 1: Broj različitih elemenata](#problem-1-broj-različitih-elemenata)
    * [Problem 2: Raspoređivanje događaja (Activity Selection)](#problem-2-raspoređivanje-događaja-activity-selection)
    * [Problem 3: Dodjela stanova (Two Pointers tehnika)](#problem-3-dodjela-stanova-two-pointers-tehnika)
    * [Problem 4: Maksimalni zbroj podniza (Maximum Subarray Sum)](#problem-4-maksimalni-zbroj-podniza-maximum-subarray-sum)
  * [Zadaci za Vježbu (Tjedan 2)](#zadaci-za-vježbu-tjedan-2)

## Uvod i motivacija

**Zašto je brzina važna?**

U natjecateljskom programiranju, rješenje nije dovoljno samo ako je točno; ono mora biti i **efikasno**. Programi se testiraju na skupu ulaznih podataka, od kojih su neki vrlo veliki. Standardno vremensko ograničenje je 1-2 sekunde. Ako je vaš algoritam prespor, neće proći sve testne primjere.

## Big O notacija: mjera efikasnosti

**Vremenska složenost** (ili Big O notacija) opisuje kako se vrijeme izvršavanja algoritma mijenja s porastom veličine ulaza (`n`). Ona nam omogućuje da procijenimo efikasnost algoritma bez da ga moramo implementirati i testirati.

Najčešće složenosti: **O(1)**, **O(log n)**, **O(n)**, **O(n log n)**, **O(n²)**, **O(2^n)**, **O(n!)**.

## Sortiranje kao temeljni alat

Sortiranje je jedan od najvažnijih alata. Mnogi složeni problemi postaju trivijalni ako su ulazni podaci sortirani. U C++-u, koristimo `std::sort` funkciju, koja ima prosječnu složenost O(n log n).

## Preporučena Literatura

* **CPH (Competitive Programmer's Handbook):**
  * Poglavlje 2: *Time complexity*
  * Poglavlje 3: *Sorting*
* **CLRS (Introduction to Algorithms):**
  * Poglavlje 2: *Getting Started* (Analiza Insertion Sorta i Merge Sorta)
  * Poglavlje 3: *Growth of Functions* (Formalna definicija asimptotske notacije)
  * Poglavlje 7: *Quicksort*
  * Poglavlje 8: *Sorting in Linear Time* (Donja granica za sortiranje usporedbom)


### Primjeri Zadataka i Objašnjenja

#### Problem 1: Broj različitih elemenata

... (tekst ostaje isti kao u prethodnoj verziji) ...

#### Problem 2: Raspoređivanje događaja (Activity Selection)

... (tekst ostaje isti kao u prethodnoj verziji) ...

#### Problem 3: Dodjela stanova (Two Pointers tehnika)

... (tekst ostaje isti kao u prethodnoj verziji) ...

#### Problem 4: Maksimalni zbroj podniza (Maximum Subarray Sum)

Ovaj klasični problem savršeno ilustrira kako različiti algoritamski pristupi dovode do drastično različitih performansi.

**Zadatak:** Zadan je niz od `n` brojeva (uključujući i negativne). Pronađi podniz (kontinuirani dio niza) čiji je zbroj elemenata najveći. Ako su svi brojevi negativni, rješenje je 0 (prazan podniz).

**Primjer:** Ulaz: `[-1, 2, 4, -3, 5, 2, -5, 2]`. Izlaz: `10` (podniz `[2, 4, -3, 5, 2]`).

##### Rješenje 1: Brute-force (O(n³))

Najjednostavniji pristup je isprobati svaki mogući podniz, izračunati njegov zbroj i pronaći maksimum.

**Algoritam:**

1. Koristi dvije petlje za generiranje svih mogućih početnih (`a`) i završnih (`b`) indeksa podniza.
2. Unutar tih petlji, trećom petljom (`k`) prođi kroz elemente od `a` do `b` i izračunaj njihov zbroj.
3. Ažuriraj maksimalni zbroj pronađen do sada.

**Kod:**

```cpp
long long best = 0;
for (int a = 0; a < n; ++a) {
    for (int b = a; b < n; ++b) {
        long long sum = 0;
        for (int k = a; k <= b; ++k) {
            sum += array[k];
        }
        best = max(best, sum);
    }
}
cout << best << '\n';
```

**Analiza:** Tri ugniježđene petlje, svaka ide do otprilike `n` puta u najgorem slučaju. Složenost je **O(n³)**. Ovo rješenje je presporo za `n > 500`.

##### Rješenje 2: Poboljšani brute-force (O(n²))

Možemo primijetiti da je unutarnja petlja u prethodnom rješenju nepotrebna. Dok fiksiramo početak podniza `a`, možemo inkrementalno računati zbroj kako pomičemo kraj podniza `b`.

**Algoritam:**

1. Vanjskom petljom fiksiraj početni indeks `a`.
2. Unutarnjom petljom pomiči završni indeks `b` od `a` do kraja niza. Održavaj trenutni zbroj tako da na svakom koraku samo dodaš novi element `array[b]`.
3. Ažuriraj maksimalni zbroj.

**Kod:**

```cpp
long long best = 0;
for (int a = 0; a < n; ++a) {
    long long sum = 0;
    for (int b = a; b < n; ++b) {
        sum += array[b];
        best = max(best, sum);
    }
}
cout << best << '\n';
```

**Analiza:** Dvije ugniježđene petlje daju složenost **O(n²)**. Ovo rješenje je prihvatljivo za `n` do otprilike 5000.

##### Rješenje 3: Kadaneov algoritam (O(n))

Najefikasnije rješenje koristi dinamičko programiranje (ili pohlepni pristup, ovisno o perspektivi) i rješava problem u samo jednom prolazu.

**Algoritam:**

1. Prođi kroz niz s lijeva na desno.
2. Održavaj dvije vrijednosti: `best` (maksimalni zbroj pronađen do sada) i `current_sum` (maksimalni zbroj podniza koji završava na trenutnoj poziciji).
3. Za svaki element `x`, ažuriraj `current_sum`. Novi `current_sum` je ili sam `x` (ako započinjemo novi podniz odavde) ili `x + current_sum` (ako nastavljamo postojeći podniz). Dakle, `current_sum = max(x, current_sum + x)`.
4. Nakon svakog koraka, ažuriraj `best = max(best, current_sum)`.

**Objašnjenje koda:** Varijabla `current_sum` prati zbroj trenutnog podniza. Ako u nekom trenutku `current_sum` postane negativan, nema smisla nastavljati taj podniz jer bi svaki sljedeći podniz imao veći zbroj da krene od nule. Stoga, ako je `current_sum < 0`, resetiramo ga na 0 (što je ekvivalentno `max(x, 0 + x)`).

```cpp
long long best = 0;
long long current_sum = 0;
for (int i = 0; i < n; ++i) {
    current_sum += array[i];
    if (current_sum < 0) {
        current_sum = 0;
    }
    best = max(best, current_sum);
}
cout << best << '\n';

// Alternativna, sažetija implementacija
long long best = 0, sum = 0;
for (int k = 0; k < n; k++) {
    sum = max((long long)array[k], sum + array[k]);
    best = max(best, sum);
}
cout << best << '\n';
```

**Analiza:** Algoritam prolazi kroz niz samo jednom. Složenost je **O(n)**. Ovo je optimalno rješenje i radi trenutno čak i za `n = 10^7`.

---

### Zadaci za Vježbu (Tjedan 2)

Preporučeni zadaci za vježbu nalaze se na online platformama. Pokušajte riješiti što više zadataka kako biste utvrdili gradivo.

#### CSES Problem Set ([https://cses.fi/problemset/](https://cses.fi/problemset/))

* **Distinct Numbers:** Direktan primjer korištenja sortiranja ili `set` strukture.
* **Apartments:** Implementacija tehnike dva pokazivača koju smo upravo obradili.
* **Ferris Wheel:** Još jedan dobar problem za vježbu pohlepnog pristupa i tehnike dva pokazivača nakon sortiranja.
* **Concert Tickets:** Problem koji se može riješiti sortiranjem, ali zahtijeva i korištenje neke strukture podataka (`multiset` ili binarno pretraživanje) za efikasno pronalaženje.
* **Maximum Subarray Sum:** Implementirajte sva tri rješenja i testirajte ih.

#### Codeforces

* **T-primes** (Problem 230B): Ovaj zadatak kombinira sito za pronalaženje prostih brojeva (koje ćemo detaljnije raditi kasnije) i binarno pretraživanje na sortiranom nizu "T-prime" brojeva.
* **Worms** (Problem 474B): Klasičan problem koji se rješava pomoću prefiksnih suma i binarnog pretraživanja (`lower_bound` funkcija je idealna za ovo).
* **Books** (Problem 279B): Problem koji se može riješiti tehnikom dva pokazivača ili binarnim pretraživanjem po odgovoru.

03-Complete-Search-and-Backtracking

[Sljedeća lekcija: Potpuna pretraga i backtracking](../03-Complete-Search-and-Backtracking/){: .btn .btn-purple .float-right}
