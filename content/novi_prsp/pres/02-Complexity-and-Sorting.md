---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Složenost i sortiranje"
footer: "Programiranje za rješavanje složenih problema | Vježbe 2025/26"
---

<!-- paginate: false -->
<!-- _class: title  -->
# Složenost i sortiranje

Programiranje za rješavanje složenih problema

---

# Sadržaj

1. **Vremenska složenost**
   - Big O notacija
   - Procjena vremena izvođenja
2. **Primjer: Najveći zbroj podniza**
   - Od $O(n^3)$ do $O(n)$
3. **Mjerenje vremena**
4. **Sortiranje**
   - `std::sort`
   - Custom comparators
5. **Zadaci za vježbu**

---

<!-- _class: lead -->
# Vremenska složenost

## Kako procijeniti brzinu algoritma?

---

# Big O notacija

Opisuje kako vrijeme izvođenja raste s veličinom ulaza ($n$).

- **$O(1)$**: Konstantno vrijeme (pristup elementu niza).
- **$O(\log n)$**: Logaritamsko (binarno pretraživanje).
- **$O(n)$**: Linearno (prolaz kroz niz).
- **$O(n \log n)$**: Linearno-logaritamsko (efikasno sortiranje).
- **$O(n^2)$**: Kvadratno (ugniježđene petlje).

**Pravilo palca:**
Moderno računalo izvodi $\approx 10^8$ operacija u sekundi.
Ako je limit 1s, a $n=10^5$, algoritam mora biti $O(n)$ ili $O(n \log n)$.

---

<!-- _class: lead -->
# Primjer: Najveći zbroj podniza

## Optimizacija algoritma

---

# Problem: Najveći zbroj podniza

**Zadatak:**
Zadan je niz od $n$ brojeva. Pronađi najveći mogući zbroj uzastopnih elemenata.

**Primjer:**
Niz: `2, -3, 1, 5, -2, 3, 5, -2`
Najveći zbroj: **12** (podniz `1, 5, -2, 3, 5`)

---

# Rješenje 1: $O(n^3)$

Provjeravamo sve moguće podnizove $(i, j)$ i za svaki računamo sumu.

```cpp
int best = INT_MIN;
for (int i = 0; i < n; i++) {
    for (int j = i; j < n; j++) {
        int sum = 0;
        for (int k = i; k <= j; k++) {
            sum += array[k];
        }
        best = max(best, sum);
    }
}
cout << best << "\n";
```

- Tri ugniježđene petlje.
- Za $n=1000$, $n^3 = 10^9$ (presporo za 1s).

---

# Rješenje 2: $O(n^2)$

Možemo računati sumu u hodu, bez treće petlje.

```cpp
int best = INT_MIN;
for (int i = 0; i < n; i++) {
    int sum = 0;
    for (int j = i; j < n; j++) {
        sum += array[j];
        best = max(best, sum);
    }
}
cout << best << "\n";
```

- Dvije ugniježđene petlje.
- Za $n=10^4$, $n^2 = 10^8$ (prolazi).
- Za $n=10^5$, $n^2 = 10^{10}$ (presporo).

---

# Rješenje 3: $O(n)$ - Kadaneov algoritam

**Ideja:**
Za svaku poziciju $k$, koji je maksimalni zbroj podniza koji **završava** na toj poziciji?

Ili je to samo element na poziciji $k$, ili produžujemo prethodni podniz.

```cpp
long long best = -1e18;
long long sum = 0;

for (int k = 0; k < n; k++) {
    // Nastavljamo niz ili krećemo ispočetka od array[k]
    sum = max((long long)array[k], sum + array[k]);
    best = max(best, sum);
}
cout << best << "\n";
```

- Jedna petlja.
- Za $n=10^6$, $10^6$ operacija (trenutno).

---

# Mjerenje brzine izvođenja

Kako provjeriti je li naš algoritam stvarno brži?

```cpp
#include <chrono>

auto start = chrono::high_resolution_clock::now();

// ... kod koji mjerimo ...

auto stop = chrono::high_resolution_clock::now();
auto duration = chrono::duration_cast<chrono::microseconds>(stop - start);

cout << "Vrijeme: " << duration.count() << " mikrosekundi" << endl;
```

---

<!-- _class: lead -->
# Sortiranje

## Uređivanje podataka

---

# Zašto sortirati?

Mnogi problemi postaju jednostavniji ako su podaci sortirani.

- Binarno pretraživanje ($O(\log n)$).
- Pohlepni algoritmi (npr. raspored aktivnosti).
- Pronalaženje duplikata ili jedinstvenih elemenata.

**Složenost sortiranja:**
Standardni algoritmi (Merge Sort, Quick Sort, Heap Sort) rade u **$O(n \log n)$**.
U C++ koristimo `std::sort`.

---

# Korištenje `std::sort`

```cpp
#include <algorithm>
#include <vector>

vector<int> v = {4, 2, 5, 3, 5, 8, 3};

// Sortiranje u rastućem poretku
sort(v.begin(), v.end()); 

// Sortiranje u padajućem poretku
sort(v.rbegin(), v.rend());
```

---

# Custom Comparator (Usporedba)

Što ako želimo sortirati strukture ili po posebnom kriteriju?

```cpp
struct Point {
    int x, y;
};

// Sortiraj po x, ako su x isti, onda po y
bool comparePoints(const Point& a, const Point& b) {
    if (a.x != b.x) return a.x < b.x;
    return a.y < b.y;
}

vector<Point> points = { {1, 2}, {3, 1}, {1, 5} };
sort(points.begin(), points.end(), comparePoints);
```

---

<!-- _class: lead -->
# Zadaci za vježbu

## CSES Sorting and Searching

---

# Zadaci

1. **[Distinct Numbers](https://cses.fi/problemset/task/1621)**
   - Koliko različitih brojeva ima u nizu?
   - *Hint:* Sortiraj pa broj promjene ili koristi `set`.
2. **[Apartments](https://cses.fi/problemset/task/1084)**
   - Dodijeli stanove podstanarima (pohlepno + sortiranje).
3. **[Ferris Wheel](https://cses.fi/problemset/task/1090)**
   - Optimizacija parova (Two pointers na sortiranom nizu).

---

<!-- _class: title -->
# Distinct Numbers (CSES)

## Analiza i rješenje

---

# Analiza: Distinct Numbers

**Problem:**
Zadan je niz od $n$ cijelih brojeva. Treba izračunati koliko ima **različitih** vrijednosti.

**Ograničenja:** $n \le 2 \cdot 10^5$.

### Intuicija

1. **Pristup sa `std::set`:**
   - Ubacimo sve brojeve u `set`. On automatski miče duplikate.
   - Rješenje je `s.size()`.
   - **Složenost:** $O(n \log n)$ zbog strukture stabla.

2. **Pristup sortiranjem (Brže i manje memorije):**
   - Ako sortiramo niz, svi isti brojevi će biti jedan do drugog (npr. `1, 1, 2, 2, 2, 5`).
   - Samo trebamo prebrojati koliko puta se broj promijeni u odnosu na prethodni.

---

# Implementacija: Distinct Numbers

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> x(n);
    for (int i = 0; i < n; i++) cin >> x[i];

    sort(x.begin(), x.end()); // O(n log n)

    int distinct_count = 1; // Prvi broj je uvijek jedinstven (ako n > 0)
    for (int i = 1; i < n; i++) {
        // Ako je trenutni broj različit od prethodnog, našli smo novi
        if (x[i] != x[i-1]) {
            distinct_count++;
        }
    }
    cout << distinct_count << endl;
    return 0;
}
```

---

<!-- _class: title -->
# Apartments (CSES)

## Pohlepni pristup i dva pokazivača

---

# Analiza: Apartments

**Problem:**
Imamo $n$ podstanara i $m$ stanova.

- Podstanar želi stan veličine $a$, ali prihvaća bilo što u rasponu $[a-k, a+k]$.
- Svaki stan ima fiksnu veličinu $b$.
- Cilj: Dodijeliti stanove tako da usrećimo **maksimalan broj** ljudi.

### Intuicija (Greedy)

Trebamo li malom stanu pridružiti nekoga tko traži mali stan ili veliki?
Logično je da **najmanji stan** pokušamo dati onome tko traži **najmanju kvadraturu**. Ako njemu ne odgovara (jer je stan premalen), nikome drugome neće odgovarati (jer svi ostali traže još veće stanove).

**Strategija:**

1. Sortiraj želje podstanara.
2. Sortiraj veličine stanova.
3. Koristi dva pokazivača (`i` za ljude, `j` za stanove).

---

# Algoritam s dva pokazivača

Neka su `applicants` i `apartments` sortirani nizovi.

Iteriramo dok imamo ljudi i stanova:

1. Ako je stan `j` **premalen** za osobu `i` (`apartments[j] < applicants[i] - k`):
   - Taj stan ne može uzeti nitko (jer ostali traže još više). Odbaci stan (`j++`).
2. Ako je stan `j` **prevelik** za osobu `i` (`apartments[j] > applicants[i] + k`):
   - Ovoj osobi ne možemo naći stan (jer su ostali stanovi još veći). Odbaci osobu (`i++`).
3. Inače (stan je taman):
   - **Match!** Dodijeli stan, povećaj brojač, pomakni oba pokazivača (`i++`, `j++`).

---

# Implementacija: Apartments

```cpp
sort(applicants.begin(), applicants.end());
sort(apartments.begin(), apartments.end());

int i = 0, j = 0, matches = 0;

while (i < n && j < m) {
    // Stan je premalen za trenutnog podstanara
    if (apartments[j] < applicants[i] - k) {
        j++; 
    }
    // Stan je prevelik za trenutnog podstanara
    else if (apartments[j] > applicants[i] + k) {
        i++;
    }
    // Stan odgovara!
    else {
        matches++;
        i++;
        j++;
    }
}
cout << matches << endl;
```

---

<!-- _class: title -->
# Ferris Wheel (CSES)

## Optimizacija parova

---

# Analiza: Ferris Wheel

**Problem:**
Imamo $n$ djece s težinama $p_i$. Gondola nosi **maksimalno dvoje** djece i ima limit težine $X$.
Cilj: Minimizirati broj gondola.

### Intuicija

Želimo iskoristiti svaku gondolu što bolje.
Najkritičnije je **najteže dijete**. Ono sigurno mora ići u neku gondolu.
Pitanje je: *Može li itko ići s njim?*

Ako najteže dijete može ići s ikim, najbolje je da ide s **najlakšim** djetetom.

- Ako najteži + najlakši $\le X$, super! Riješili smo dvoje djece jednom gondolom.
- Ako najteži + najlakši $> X$, onda najteži ne može ići ni s kim (jer je najlakši bio najbolja šansa). Najteži ide sam.

---

# Algoritam (Two Pointers)

1. Sortiraj djecu po težini.
2. Postavi pokazivač `i` na početak (najlakši) i `j` na kraj (najteži).
3. Dok se pokazivači ne susretnu (`i <= j`):
   - Uvijek uzimamo najtežeg (`j`).
   - Provjeri stane li i najlakši (`i`) s njim: `weight[i] + weight[j] <= X`.
     - Ako stane: uzmi i njega (`i++`).
   - U svakom slučaju, najteži odlazi (`j--`) i koristimo jednu gondolu (`gondolas++`).

---

# Implementacija: Ferris Wheel

```cpp
sort(p.begin(), p.end());

int i = 0;          // Pokazivač na najlakše dijete
int j = n - 1;      // Pokazivač na najteže dijete
int gondolas = 0;

while (i <= j) {
    // Ako su najlakši i najteži zajedno unutar limita
    if (p[i] + p[j] <= x) {
        i++; // Uzimamo i najlakšeg
        j--; // Uzimamo i najtežeg
    } else {
        // Najteži mora ići sam
        j--;
    }
    gondolas++; // U svakom koraku jedna gondola odlazi
}
cout << gondolas << endl;
```

**Zaključak:** Sortiranje nam je omogućilo da pohlepno donosimo optimalne odluke s krajeva niza. Složenost: $O(n \log n)$.

---

<!-- _class: title -->
# Zaključak i najbitnije napomene

---

# Što smo danas naučili?

1. **Analiza složenosti je ključna:**
   - Prije pisanja koda, procijenite hoće li algoritam proći vremensko ograničenje.
   - $10^8$ operacija $\approx 1$ sekunda.

2. **Sortiranje je moćan alat:**
   - Mnogi problemi postaju trivijalni na sortiranom nizu (npr. *Distinct Numbers*).
   - Omogućuje korištenje **pohlepnih algoritama** i **tehnike dva pokazivača** (*Apartments*, *Ferris Wheel*).

3. **Efikasnost C++-a:**
   - `std::sort` je brz ($O(N \log N)$).
   - Koristite `vector` i reference (`&`) za prosljeđivanje velikih struktura.

---

# Zlatna pravila za rješavanje zadataka

- **Provjeri ograničenja ($N$):**
  - Ako je $N=10^5$, rješenje mora biti $O(N)$ ili $O(N \log N)$. $O(N^2)$ neće proći.
- **Paziti na `overflow`:**
  - Ako zbrajaš puno brojeva ili množiš, koristi `long long`.
- **Rubni slučajevi:**
  - Što ako je niz prazan? Što ako su svi brojevi isti? Što ako je $N=1$?
- **Ne kompliciraj:**
  - Ako postoji jednostavno rješenje (npr. sortiranje), vjerojatno je bolje od komplicirane strukture podataka.
