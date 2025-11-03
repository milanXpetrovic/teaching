---
---

# Podijeli pa Vladaj i Binarno Pretraživanje

## Sadržaj
1.  [Uvod i Motivacija](#uvod-i-motivacija)
    *   [Princip "Podijeli pa Vladaj"](#princip-podijeli-pa-vladaj)
    *   [Binarno Pretraživanje kao Specijalni Slučaj](#binarno-pretraživanje-kao-specijalni-slučaj)
    *   [Binarno Pretraživanje po Rješenju](#binarno-pretraživanje-po-rješenju)
    *   [Preporučena Literatura](#preporučena-literatura)
2.  [Primjeri Zadataka i Objašnjenja](#primjeri-zadataka-i-objašnjenja)
    *   [Problem 1: Maksimalni zbroj podniza (Divide and Conquer pristup)](#problem-1-maksimalni-zbroj-podniza-divide-and-conquer-pristup)
    *   [Problem 2: Pronalaženje fiksne točke](#problem-2-pronalaženje-fiksne-točke)
    *   [Problem 3: Agresivne krave (Binarno pretraživanje po rješenju)](#problem-3-agresivne-krave-binarno-pretraživanje-po-rješenju)
3.  [Zadaci za Vježbu](#zadaci-za-vježbu)

---

## Uvod i Motivacija

### Princip "Podijeli pa Vladaj"
"Podijeli pa vladaj" (engl. *Divide and Conquer*) je moćna algoritamska paradigma koja rješava problem rekurzivno, slijedeći tri koraka:
1.  **Podijeli (Divide):** Problem se dijeli na jedan ili više manjih podproblema istog tipa.
2.  **Vladaj (Conquer):** Podproblemi se rješavaju rekurzivno. Ako su podproblemi dovoljno mali, rješavaju se direktno.
3.  **Kombiniraj (Combine):** Rješenja podproblema se spajaju kako bi se dobilo rješenje originalnog problema.

Primjer koji smo već vidjeli je Merge Sort, gdje se niz dijeli na dvije polovice, svaka se rekurzivno sortira, a zatim se sortirane polovice spajaju. Algoritmi temeljeni na ovoj paradigmi često imaju složenost oblika `O(n log n)`.

### Binarno Pretraživanje kao Specijalni Slučaj
**Binarno pretraživanje** je savršen i vrlo jednostavan primjer "podijeli pa vladaj" tehnike:
1.  **Podijeli:** Pronađi srednji element sortiranog niza. Time se niz dijeli na dvije polovice.
2.  **Vladaj:** Usporedi traženi element sa srednjim. Odluči se za jednu od polovica (lijevu ili desnu) u kojoj se element može nalaziti i rekurzivno nastavi pretragu samo u toj polovici.
3.  **Kombiniraj:** Nema koraka kombiniranja; rješenje podproblema je rješenje cijelog problema.

Zbog toga što u svakom koraku odbacujemo polovicu preostalih elemenata, binarno pretraživanje ima izuzetno efikasnu složenost **O(log n)**.

### Binarno Pretraživanje po Rješenju
Ovo je jedna od najmoćnijih tehnika u natjecateljskom programiranju. Primjenjuje se na optimizacijske probleme gdje tražimo **minimalnu** ili **maksimalnu** vrijednost koja zadovoljava određeni uvjet.

**Ideja:** Umjesto da direktno tražimo optimalnu vrijednost, transformiramo problem u jednostavniji, **odlučivački** problem: "Je li moguće postići rješenje s vrijednošću barem/najviše `x`?".

Ako za problem vrijedi svojstvo **monotonosti** (ako je rješenje `x` moguće, onda je moguće i svako rješenje manje od `x` za maksimizacijske probleme, ili veće od `x` za minimizacijske), tada možemo binarno pretraživati prostor mogućih rješenja kako bismo pronašli optimalnu vrijednost `x`.

### Preporučena Literatura
*   **CPH (Competitive Programmer's Handbook):**
    *   Poglavlje 3.3: *Binary search*
*   **CLRS (Introduction to Algorithms):**
    *   Poglavlje 4: *Divide-and-Conquer* (posebno 4.1: Maximum-subarray problem)
    *   Poglavlje 2.3: *Designing algorithms* (uvod u Merge Sort kao D&C)

---

## Primjeri Zadataka i Objašnjenja

### Problem 1: Maksimalni zbroj podniza (Divide and Conquer pristup)
Iako smo ovaj problem riješili u O(n) vremenu koristeći Kadaneov algoritam, on je također klasičan primjer "podijeli pa vladaj" pristupa.

**Zadatak:** Zadan je niz od `n` brojeva. Pronađi podniz čiji je zbroj elemenata najveći.

**Algoritam (O(n log n)):**
1.  **Podijeli:** Podijeli niz na dvije polovice, lijevu i desnu.
2.  **Vladaj:** Rekurzivno pronađi maksimalni zbroj podniza u lijevoj polovici (`max_left`) i u desnoj polovici (`max_right`).
3.  **Kombiniraj:** Pronađi maksimalni zbroj podniza koji prelazi sredinu (`max_crossing`). To se radi tako da se pronađe maksimalni zbroj koji završava na sredini i ide ulijevo, te maksimalni zbroj koji počinje od sredine i ide udesno. Njihov zbroj je `max_crossing`.
4.  Rješenje je `max(max_left, max_right, max_crossing)`.

**Kod (samo ključni dio):**
```cpp
// Funkcija za pronalaženje max zbroja koji prelazi sredinu
long long maxCrossingSum(const vector<int>& arr, int l, int m, int r) {
    long long sum = 0;
    long long left_sum = -1e18; // Vrlo mali broj
    for (int i = m; i >= l; i--) {
        sum += arr[i];
        if (sum > left_sum) left_sum = sum;
    }

    sum = 0;
    long long right_sum = -1e18;
    for (int i = m + 1; i <= r; i++) {
        sum += arr[i];
        if (sum > right_sum) right_sum = sum;
    }
    return left_sum + right_sum;
}

// Rekurzivna funkcija
long long maxSubarraySum(const vector<int>& arr, int l, int r) {
    if (l == r) return arr[l];
    int m = l + (r - l) / 2;
    long long max_left = maxSubarraySum(arr, l, m);
    long long max_right = maxSubarraySum(arr, m + 1, r);
    long long max_cross = maxCrossingSum(arr, l, m, r);
    return max({max_left, max_right, max_cross});
}```
**Analiza:** Rekurzija je `T(n) = 2T(n/2) + O(n)`, što po Master teoremu daje složenost **O(n log n)**. Iako sporije od Kadaneovog algoritma, ovo je sjajan primjer D&C paradigme.

### Problem 2: Pronalaženje fiksne točke

**Zadatak:** Zadan je sortiran niz `a` od `n` različitih cijelih brojeva. Pronađi postoji li indeks `i` takav da je `a[i] = i`.

**Primjer:** Za `a = [-10, -5, 0, 3, 7]`, fiksna točka je na indeksu 3, jer `a[3] = 3`.

**Rješenje (O(log n)):**
Definirajmo novu funkciju `b[i] = a[i] - i`. Sada tražimo indeks `i` takav da je `b[i] = 0`.
Niz `a` je strogo rastući. Što je s nizom `b`?
`b[i+1] - b[i] = (a[i+1] - (i+1)) - (a[i] - i) = (a[i+1] - a[i]) - 1`.
Budući da su elementi u `a` različiti cijeli brojevi, `a[i+1] - a[i] >= 1`. Stoga je `b[i+1] - b[i] >= 0`. Niz `b` je **monotono neopadajući**.
Sada možemo binarno pretraživati niz `b` za vrijednost 0.

**Algoritam:**
1.  Primijeni binarno pretraživanje na rasponu indeksa `[0, n-1]`.
2.  Na svakom koraku, provjeri srednji indeks `mid`.
    *   Ako je `a[mid] == mid`, pronašli smo rješenje.
    *   Ako je `a[mid] > mid`, fiksna točka (ako postoji) mora biti u lijevoj polovici (indeksi `< mid`).
    *   Ako je `a[mid] < mid`, fiksna točka (ako postoji) mora biti u desnoj polovici (indeksi `> mid`).

**Kod:**
```cpp
int l = 0, r = n - 1, ans = -1;
while (l <= r) {
    int mid = l + (r - l) / 2;
    if (a[mid] == mid) {
        ans = mid;
        break; // ili r = mid - 1 za prvu fiksnu točku
    } else if (a[mid] > mid) {
        r = mid - 1;
    } else {
        l = mid + 1;
    }
}
```
**Složenost:** Klasično binarno pretraživanje, **O(log n)**.

### Problem 3: Agresivne krave (Binarno pretraživanje po rješenju)

**Zadatak:** Zadan je niz od `n` pozicija štala i `c` krava. Smjesti krave u štale tako da je minimalna udaljenost između bilo koje dvije krave što veća.

**Primjer:** Štale na pozicijama `[1, 2, 4, 8, 9]` i `c = 3` krave.
Optimalno je postaviti krave na pozicije `1, 4, 8` ili `1, 4, 9`. Minimalna udaljenost je 3.

**Rješenje:** Umjesto da tražimo optimalnu udaljenost `d`, pitajmo se: "Je li moguće smjestiti `c` krava tako da je minimalna udaljenost među njima **barem** `d`?".

**Monotonost:** Ako je moguće smjestiti krave s minimalnom udaljenošću `d`, onda je sigurno moguće smjestiti ih i s bilo kojom manjom udaljenošću. Ovo svojstvo nam omogućuje binarno pretraživanje po odgovoru `d`.

**`check(d)` funkcija:**
Ova funkcija provjerava je li moguće smjestiti `c` krava s minimalnom udaljenošću `d`. Ovo se može provjeriti pohlepno:
1.  Postavi prvu kravu u prvu štalu.
2.  Iteriraj kroz preostale štale. Postavi sljedeću kravu u prvu štalu koja je na udaljenosti barem `d` od prethodno postavljene krave.
3.  Ako uspijemo postaviti svih `c` krava, vrati `true`. Inače `false`.

**Algoritam:**
1.  Sortiraj pozicije štala.
2.  Definiraj prostor pretrage za udaljenost `d`, npr. od `0` do `10^9`.
3.  Binarno pretražuj taj prostor:
    *   Za srednju vrijednost `mid`, pozovi `check(mid)`.
    *   Ako je `check(mid)` `true`, znači da je udaljenost `mid` moguća. Možda postoji i veća, pa tražimo u desnoj polovici: `l = mid + 1`.
    *   Ako je `check(mid)` `false`, udaljenost `mid` nije moguća. Moramo smanjiti udaljenost: `r = mid - 1`.

**Kod:**
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

bool check(long long d, int c, const vector<int>& stalls) {
    int cows_placed = 1;
    int last_pos = stalls;
    for (size_t i = 1; i < stalls.size(); ++i) {
        if (stalls[i] - last_pos >= d) {
            cows_placed++;
            last_pos = stalls[i];
            if (cows_placed == c) return true;
        }
    }
    return false;
}

int main() {
    // ... Brzi I/O ...
    int n, c;
    cin >> n >> c;
    vector<int> stalls(n);
    for (int i = 0; i < n; ++i) cin >> stalls[i];
    
    sort(stalls.begin(), stalls.end());

    long long l = 0, r = 1e9, ans = 0;
    while (l <= r) {
        long long mid = l + (r - l) / 2;
        if (check(mid, c, stalls)) {
            ans = mid;
            l = mid + 1;
        } else {
            r = mid - 1;
        }
    }
    cout << ans << '\n';
    return 0;
}
```
**Složenost:** Sortiranje je O(n log n). Binarno pretraživanje radi O(log R) iteracija (gdje je R raspon udaljenosti), a `check` funkcija traje O(n). Ukupna složenost je **O(n log n + n log R)**.

---

## Zadaci za Vježbu

### CSES Problem Set ([https://cses.fi/problemset/](https://cses.fi/problemset/))

*   **Sum of Two Values:** Riješite problem koristeći sortiranje i binarno pretraživanje za svaki element (O(n log n)). Zatim usporedite s rješenjem koje koristi dva pokazivača.
*   **Factory Machines:** Klasičan problem za binarno pretraživanje po rješenju. "Rješenje" je vrijeme. Funkcija `check(t)` provjerava koliko proizvoda se može napraviti u vremenu `t`.
*   **Towers:** Iako se rješava pohlepno, razmislite kako binarno pretraživanje (`upper_bound`) može pomoći u implementaciji pohlepne strategije.

### Codeforces

*   **Hamburgers** (Problem 371B): Odličan zadatak za binarno pretraživanje po rješenju. "Rješenje" je broj hamburgera. `check(k)` funkcija izračunava koliko novca je potrebno za `k` hamburgera.
*   **Pipeline** (Problem 287B): Još jedan dobar problem za binarno pretraživanje po rješenju. `check` funkcija je jednostavan zbroj.
