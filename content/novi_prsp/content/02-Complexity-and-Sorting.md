
# Programiranje za Rješavanje Složenih Problema: Tjedan 1 i 2

## Sadržaj

*   [**Tjedan 1: Uvod u Natjecateljsko Programiranje i Osnove C++-a**](#tjedan-1-uvod-u-natjecateljsko-programiranje-i-osnove-c-a)
    *   [Što je Natjecateljsko Programiranje?](#što-je-natjecateljsko-programiranje)
    *   [C++ kao Jezik Izbora](#c-kao-jezik-izbora)
    *   [Postavljanje Efikasnog C++ Okruženja](#postavljanje-efikasnog-c-okruženja)
    *   [Osnove Ulaza i Izlaza (I/O)](#osnove-ulaza-i-izlaza-io)
    *   [Osnovne Strukture Podataka (STL)](#osnovne-strukture-podataka-stl)
    *   [Zadaci za Vježbu (Tjedan 1)](#zadaci-za-vježbu-tjedan-1)

*   [**Tjedan 2: Analiza Složenosti i Sortiranje**](#tjedan-2-analiza-složenosti-i-sortiranje)
    *   [Uvod i Motivacija](#uvod-i-motivacija)
    *   [Primjeri Zadataka i Objašnjenja](#primjeri-zadataka-i-objašnjenja)
        *   [Problem 1: Broj različitih elemenata](#problem-1-broj-različitih-elemenata)
        *   [Problem 2: Raspoređivanje događaja (Activity Selection)](#problem-2-raspoređivanje-događaja-activity-selection)
        *   [Problem 3: Dodjela stanova (Two Pointers tehnika)](#problem-3-dodjela-stanova-two-pointers-tehnika)
        *   [Problem 4: Maksimalni zbroj podniza (Maximum Subarray Sum)](#problem-4-maksimalni-zbroj-podniza-maximum-subarray-sum)
    *   [Zadaci za Vježbu (Tjedan 2)](#zadaci-za-vježbu-tjedan-2)

---

## Tjedan 1: Uvod u Natjecateljsko Programiranje i Osnove C++-a

### Što je Natjecateljsko Programiranje?

Natjecateljsko programiranje je misaoni sport u kojem sudionici rješavaju algoritamske probleme unutar zadanih vremenskih i memorijskih ograničenja. Rješavanje problema sastoji se od dva ključna dijela:

1.  **Dizajn algoritma:** Analiza problema, prepoznavanje poznatih struktura i osmišljavanje rješenja koje je **točno** i **efikasno**.
2.  **Implementacija algoritma:** Pisanje čistog, sažetog i ispravnog koda koji uspješno prolazi sve testne primjere unutar zadanih resursa.

Za razliku od tradicionalnog softverskog inženjerstva, programi su obično kratki (do stotinjak linija koda), ne zahtijevaju dugoročno održavanje, a fokus je na performansama i brzini implementacije.

### C++ kao Jezik Izbora

Iako se problemi mogu rješavati u raznim jezicima (Python, Java), C++ je daleko najpopularniji izbor u natjecateljskom programiranju iz nekoliko razloga:

*   **Performanse:** C++ je izuzetno brz jezik, što je ključno kada se programi izvršavaju na velikim ulaznim podacima unutar strogih vremenskih ograničenja (obično 1-2 sekunde).
*   **Standardna Biblioteka Predložaka (STL):** C++ nudi moćnu biblioteku gotovih struktura podataka (poput dinamičkih polja, skupova, mapa) i algoritama (sortiranje, pretraživanje) koje drastično ubrzavaju implementaciju.
*   **Kontrola nad memorijom:** Omogućuje precizno upravljanje memorijom, što je važno za probleme s ograničenom memorijom.

### Postavljanje Efikasnog C++ Okruženja

#### Kompajler
Koristit ćemo `g++` kompajler, koji je standard na većini natjecateljskih platformi. Na Windowsima se može instalirati putem MinGW-a ili WSL-a (Windows Subsystem for Linux). Na Linuxu i macOS-u je obično već dostupan.

#### Osnovni Predložak (Template)
Većina natjecatelja koristi osnovni predložak koda kako bi ubrzali pisanje. Naš početni predložak izgledat će ovako:

```cpp
#include <bits/stdc++.h> // Uključuje sve standardne biblioteke (samo g++)

using namespace std;

int main() {
    // Brzi I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    // Rješenje zadatka dolazi ovdje

    return 0;
}
```

#### Kompajliranje koda
Kod kompajliramo koristeći naredbu u terminalu:
`g++ -std=c++11 -O2 -Wall solution.cpp -o solution`
*   `-std=c++11`: Koristi C++11 standard (ili noviji, npr. `c++17`).
*   `-O2`: Optimizira kod za brzinu.
*   `-Wall`: Prikazuje sva upozorenja, što je korisno za otkrivanje potencijalnih grešaka.
*   `-o solution`: Ime izvršne datoteke.

### Osnove Ulaza i Izlaza (I/O)

Standardni `cin` i `cout` mogu biti spori. Na početku `main` funkcije uvijek dodajte linije za ubrzanje (kao u predlošku). Također, umjesto `endl` koristite `'\n'` za ispis novog reda.

#### Čitanje Ulaza
Uobičajeni način čitanja podataka:
```cpp
int a, b;
string s;
cin >> a >> b >> s; // Čita "10 20 rijec"
```

Za čitanje cijele linije, uključujući razmake:
```cpp
string line;
getline(cin, line);
```

### Osnovne Strukture Podataka (STL)

STL je vaš najvažniji alat. Ovaj tjedan fokusiramo se na najosnovnije.

#### `vector` (Dinamičko polje)
```cpp
vector<int> v;
v.push_back(5); // Dodaje element na kraj:
v.push_back(2); //

cout << v; // Ispisuje 5

// Iteracija kroz vektor
for (int x : v) {
    cout << x << " ";
}
cout << '\n';
```

#### `string`
```cpp
string a = "test";
string b = "iranje";
string s = a + b; // s = "testiranje"
cout << s.substr(2, 4); // Ispisuje "stir" (podstring od indeksa 2, duljine 4)
```

#### `pair` i `tuple`
```cpp
pair<int, string> p = {1, "rijec"};
cout << p.first << " " << p.second << '\n'; // 1 rijec

tuple<int, char, double> t = {5, 'a', 3.14};
cout << get<0>(t) << '\n'; // 5
```

#### `sort` algoritam
Funkcija `sort` sortira elemente u rasponu. Za `vector` se koristi ovako:
```cpp
vector<int> v = {4, 2, 5, 3, 5, 8, 3};
sort(v.begin(), v.end()); // v sada sadrži
```

### Zadaci za Vježbu (Tjedan 1)

1.  **Postavite Svoje Okruženje:** Instalirajte g++ kompajler i odaberite editor (npr. VS Code s C++ ekstenzijama). Napravite svoj osnovni predložak koda.
2.  **Jednostavan Ulaz/Izlaz:** Riješite zadatak koji zahtijeva čitanje nekoliko brojeva i stringova, izvođenje jednostavne matematičke operacije i ispis rezultata.
3.  **Sortiranje Parova:** Napišite program koji čita `n` parova brojeva, sortira ih primarno po prvom elementu, a sekundarno po drugom, te ispisuje sortirane parove.
4.  **Manipulacija Stringovima:** Riješite zadatak koji zahtijeva čitanje stringa, pronalaženje podstringa i ispis rezultata.
5.  **Vježba na Online Judgeu:** Riješite nekoliko jednostavnih "ad-hoc" ili implementacijskih zadataka na platformi poput Codeforces (npr. Div2 A/B razina) kako biste se navikli na format natjecanja.

---

## Tjedan 2: Analiza Složenosti i Sortiranje

### Uvod i Motivacija

#### Zašto je brzina važna?
U natjecateljskom programiranju, rješenje nije dovoljno samo ako je točno; ono mora biti i **efikasno**. Programi se testiraju na skupu ulaznih podataka, od kojih su neki vrlo veliki. Standardno vremensko ograničenje je 1-2 sekunde. Ako je vaš algoritam prespor, neće proći sve testne primjere.

#### Big O Notacija: Mjera Efikasnosti
**Vremenska složenost** (ili Big O notacija) opisuje kako se vrijeme izvršavanja algoritma mijenja s porastom veličine ulaza (`n`). Ona nam omogućuje da procijenimo efikasnost algoritma bez da ga moramo implementirati i testirati.

Najčešće složenosti: **O(1)**, **O(log n)**, **O(n)**, **O(n log n)**, **O(n²)**, **O(2^n)**, **O(n!)**.

#### Sortiranje kao Temeljni Alat
Sortiranje je jedan od najvažnijih alata. Mnogi složeni problemi postaju trivijalni ako su ulazni podaci sortirani. U C++-u, koristimo `std::sort` funkciju, koja ima prosječnu složenost O(n log n).

#### Preporučena Literatura
*   **CPH (Competitive Programmer's Handbook):**
    *   Poglavlje 2: *Time complexity*
    *   Poglavlje 3: *Sorting*
*   **CLRS (Introduction to Algorithms):**
    *   Poglavlje 2: *Getting Started* (Analiza Insertion Sorta i Merge Sorta)
    *   Poglavlje 3: *Growth of Functions* (Formalna definicija asimptotske notacije)
    *   Poglavlje 7: *Quicksort*
    *   Poglavlje 8: *Sorting in Linear Time* (Donja granica za sortiranje usporedbom)

---

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
1.  Koristi dvije petlje za generiranje svih mogućih početnih (`a`) i završnih (`b`) indeksa podniza.
2.  Unutar tih petlji, trećom petljom (`k`) prođi kroz elemente od `a` do `b` i izračunaj njihov zbroj.
3.  Ažuriraj maksimalni zbroj pronađen do sada.

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
1.  Vanjskom petljom fiksiraj početni indeks `a`.
2.  Unutarnjom petljom pomiči završni indeks `b` od `a` do kraja niza. Održavaj trenutni zbroj tako da na svakom koraku samo dodaš novi element `array[b]`.
3.  Ažuriraj maksimalni zbroj.

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
1.  Prođi kroz niz s lijeva na desno.
2.  Održavaj dvije vrijednosti: `best` (maksimalni zbroj pronađen do sada) i `current_sum` (maksimalni zbroj podniza koji završava na trenutnoj poziciji).
3.  Za svaki element `x`, ažuriraj `current_sum`. Novi `current_sum` je ili sam `x` (ako započinjemo novi podniz odavde) ili `x + current_sum` (ako nastavljamo postojeći podniz). Dakle, `current_sum = max(x, current_sum + x)`.
4.  Nakon svakog koraka, ažuriraj `best = max(best, current_sum)`.

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
cout << best << '\n';```
**Analiza:** Algoritam prolazi kroz niz samo jednom. Složenost je **O(n)**. Ovo je optimalno rješenje i radi trenutno čak i za `n = 10^7`.

---

### Zadaci za Vježbu (Tjedan 2)

Preporučeni zadaci za vježbu nalaze se na online platformama. Pokušajte riješiti što više zadataka kako biste utvrdili gradivo.

#### CSES Problem Set ([https://cses.fi/problemset/](https://cses.fi/problemset/))

*   **Distinct Numbers:** Direktan primjer korištenja sortiranja ili `set` strukture.
*   **Apartments:** Implementacija tehnike dva pokazivača koju smo upravo obradili.
*   **Ferris Wheel:** Još jedan dobar problem za vježbu pohlepnog pristupa i tehnike dva pokazivača nakon sortiranja.
*   **Concert Tickets:** Problem koji se može riješiti sortiranjem, ali zahtijeva i korištenje neke strukture podataka (`multiset` ili binarno pretraživanje) za efikasno pronalaženje.
*   **Maximum Subarray Sum:** Implementirajte sva tri rješenja i testirajte ih.

#### Codeforces

*   **T-primes** (Problem 230B): Ovaj zadatak kombinira sito za pronalaženje prostih brojeva (koje ćemo detaljnije raditi kasnije) i binarno pretraživanje na sortiranom nizu "T-prime" brojeva.
*   **Worms** (Problem 474B): Klasičan problem koji se rješava pomoću prefiksnih suma i binarnog pretraživanja (`lower_bound` funkcija je idealna za ovo).
*   **Books** (Problem 279B): Problem koji se može riješiti tehnikom dva pokazivača ili binarnim pretraživanjem po odgovoru.























03-Complete-Search-and-Backtracking





