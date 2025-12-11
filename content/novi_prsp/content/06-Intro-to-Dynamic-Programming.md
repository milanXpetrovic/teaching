---
nav_exclude: true
---

# Uvod u dinamičko programiranje

## Sadržaj

1. [Uvod i Motivacija](#uvod-i-motivacija)
    * [Što je Dinamičko Programiranje?](#što-je-dinamičko-programiranje)
    * [Ključne Ideje: Preklapajući Podproblemi i Optimalna Podstruktura](#ključne-ideje-preklapajući-podproblemi-i-optimalna-podstruktura)
    * [Dva Pristupa: Memoizacija (Top-Down) i Tabulacija (Bottom-Up)](#dva-pristupa-memoizacija-top-down-i-tabulacija-bottom-up)
    * [Koraci u Rješavanju DP Problema](#koraci-u-rješavanju-dp-problema)
    * [Preporučena Literatura](#preporučena-literatura)
2. [Primjeri Zadataka i Objašnjenja](#primjeri-zadataka-i-objašnjenja)
    * [Problem 1: Problem novčića (Minimizacija)](#problem-1-problem-novčića-minimizacija)
    * [Problem 2: Problem novčića (Prebrojavanje rješenja)](#problem-2-problem-novčića-prebrojavanje-rješenja)
    * [Problem 3: Najduži rastući podniz (Longest Increasing Subsequence - LIS)](#problem-3-najduži-rastući-podniz-longest-increasing-subsequence---lis)
    * [Problem 4: Udaljenost uređivanja (Edit Distance)](#problem-4-udaljenost-uređivanja-edit-distance)
3. [Zadaci za Vježbu](#zadaci-za-vježbu)

---

## Uvod i motivacija

### Što je dinamičko programiranje?

**Dinamičko programiranje (DP)** je moćna tehnika za rješavanje optimizacijskih i prebrojavačkih problema. Ona spaja ispravnost potpune pretrage s efikasnošću pohlepnih algoritama. DP se primjenjuje na probleme koji se mogu rastaviti na **preklapajuće podprobleme**, a čija rješenja se mogu kombinirati da bi se dobilo rješenje originalnog problema.

### Ključne ideje: Preklapajući podproblemi i optimalna podstruktura

Da bismo mogli primijeniti DP, problem mora imati dva svojstva:

1. **Optimalna podstruktura (Optimal substructure):** Optimalno rješenje problema sadrži u sebi optimalna rješenja manjih podproblema.
2. **Preklapajući podproblemi (Overlapping subproblems):** Naivno rekurzivno rješenje rješava iste podprobleme više puta.

**Intuitivni primjer: Fibonaccijev niz**
Definiran je s `F(n) = F(n-1) + F(n-2)`. Naivna rekurzivna implementacija:

```cpp
int fib(int n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);
}
```

Ovaj kod je izuzetno spor (složenost `O(2^n)`). Zašto? Pogledajmo stablo poziva za `fib(5)`:

```text
      fib(5)
     /      \
  fib(4)    fib(3)
 /    \      /    \
fib(3) fib(2) fib(2) fib(1)
...   ...
```

Primjećujemo da se `fib(3)` računa dvaput, `fib(2)` triput, itd. Ovo je klasičan primjer **preklapajućih podproblema**. Dinamičko programiranje rješava ovaj problem tako da **pamti** rješenje svakog podproblema nakon što ga prvi put izračuna.

### Dva pristupa: memoizacija (Top-Down) i tabulacija (Bottom-Up)

1. **Memoizacija (Top-Down):** Zadržavamo prirodnu rekurzivnu strukturu, ali dodajemo mehanizam za pamćenje (obično polje ili mapa). Prije nego što izračunamo rješenje za podproblem, provjerimo jesmo li ga već riješili.

    ```cpp
    map<int, long long> memo;
    long long fib_memo(int n) {
        if (n <= 1) return n;
        if (memo.count(n)) return memo[n]; // Vrati spremljeni rezultat
        memo[n] = fib_memo(n-1) + fib_memo(n-2); // Izračunaj i spremi
        return memo[n];
    }
    ```

    Ovo rješenje ima složenost **O(n)** jer se `fib_memo(k)` za svako `k` izračunava samo jednom.

2. **Tabulacija (Bottom-Up):** Rješavamo podprobleme iterativno, od najmanjih prema većima, i spremamo rješenja u tablicu (polje). Kada dođemo do nekog podproblema, rješenja za sve manje podprobleme koje trebamo su već izračunata.

    ```cpp
    vector<long long> dp(n + 1);
    dp = 0;
    dp = 1;
    for (int i = 2; i <= n; ++i) {
        dp[i] = dp[i-1] + dp[i-2];
    }
    // Rješenje je u dp[n]
    ```

    Ovo je također **O(n)**, ali u praksi često brže zbog manjeg overhead-a (nema rekurzivnih poziva). **Tabulacija je standardni pristup u natjecateljskom programiranju.**

### Koraci u rješavanju DP problema

1. **Definiraj stanje:** Što je podproblem? Odredi parametre koji jedinstveno opisuju podproblem. Npr. `dp[i]` može biti rješenje za prvih `i` elemenata.
2. **Pronađi rekurzivnu relaciju:** Kako se rješenje za `dp[i]` može izračunati pomoću rješenja manjih podproblema (npr. `dp[i-1]`, `dp[j]` za `j < i`)?
3. **Definiraj bazne slučajeve:** Koji su najmanji podproblemi čija rješenja znamo unaprijed? Npr. `dp[0]`.
4. **Odredi redoslijed računanja:** Kojim redom treba popunjavati DP tablicu? (Obično od manjih indeksa prema većima).

### Preporučena literatura

* **CPH (Competitive Programmer's Handbook):**
  * Poglavlje 7: *Dynamic programming*
* **CLRS (Introduction to Algorithms):**
  * Poglavlje 15: *Dynamic Programming* (pruža odličan teorijski uvod)

---

## Primjeri zadataka i objašnjenja

### Problem 1: Problem novčića (Minimizacija)

**Zadatak:** Zadan je skup denominacija novčića `{c1, c2, ..., ck}` i ciljani iznos `n`. Pronađi minimalan broj novčića potreban za formiranje iznosa `n`.

**Primjer:** Iznos `n = 10`, Kovanice `{1, 3, 4}`. Optimalno rješenje je `3+3+4`, što zahtijeva 3 novčića.

#### Rješenje (Bottom-Up DP)

1. **Stanje:** `dp[x]` = minimalan broj novčića za iznos `x`. Naš cilj je `dp[n]`.
2. **Rekurzivna relacija:** Za iznos `x`, zadnji novčić koji dodamo može biti bilo koji `c` iz skupa kovanica. Ako odaberemo novčić `c`, preostaje nam formirati iznos `x-c` s minimalnim brojem novčića. Stoga, isprobavamo sve mogućnosti:
    `dp[x] = 1 + min(dp[x - ci])` za sve `ci <= x`.
3. **Bazni slučaj:** `dp[0] = 0`. Za iznos 0 potrebno je 0 novčića.
4. **Redoslijed:** Računamo `dp[x]` za `x` od 1 do `n`.

**Kod:**

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

const int INF = 1e9;

int main() {
    //  I/O 
    int n; // Ciljani iznos
    cin >> n;
    vector<int> coins = {1, 3, 4};
    
    vector<int> dp(n + 1, INF);
    dp = 0;

    for (int x = 1; x <= n; ++x) {
        for (int c : coins) {
            if (x - c >= 0) {
                dp[x] = min(dp[x], dp[x - c] + 1);
            }
        }
    }

    if (dp[n] == INF) {
        cout << "Nije moguće." << '\n';
    } else {
        cout << dp[n] << '\n';
    }

    return 0;
}
```

**Složenost:** **O(n * k)**, gdje je `k` broj denominacija. Dvije ugniježđene petlje.

### Problem 2: Problem novčića (Prebrojavanje rješenja)

**Zadatak:** Zadan je isti skup novčića i iznos `n`. Na koliko načina možemo formirati iznos `n`?

**Primjer:** Iznos `n = 5`, Kovanice `{1, 3, 4}`. Načini su:

* 1+1+1+1+1
* 1+1+3
* 1+4
* 1+3+1
* 3+1+1
* 4+1

Ukupno 6 načina.

#### Rješenje (Bottom-Up DP)

1. **Stanje:** `dp[x]` = broj načina za formiranje iznosa `x`.
2. **Rekurzivna relacija:** Za formiranje iznosa `x`, zadnji dodani novčić može biti `c`. Zbroj svih načina za formiranje `x-c` daje ukupan broj načina za `x`.
    `dp[x] = sum(dp[x - ci])` za sve `ci <= x`.
3. **Bazni slučaj:** `dp[0] = 1` (prazan skup je jedini način za formiranje iznosa 0).
4. **Redoslijed:** Računamo `dp[x]` za `x` od 1 do `n`.

**Kod:**

```cpp
// ...
vector<long long> dp(n + 1, 0);
dp = 1;
long long MOD = 1e9 + 7; // Za velike brojeve

for (int x = 1; x <= n; ++x) {
    for (int c : coins) {
        if (x - c >= 0) {
            dp[x] = (dp[x] + dp[x - c]) % MOD;
        }
    }
}
cout << dp[n] << '\n';
```

**Složenost:** Opet **O(n * k)**.

### Problem 3: Najduži rastući podniz (Longest Increasing Subsequence - LIS)

**Zadatak:** Zadan je niz od `n` brojeva. Pronađi duljinu najdužeg podniza koji je strogo rastući. Podniz ne mora biti kontinuiran.

**Primjer:** Niz `[6, 2, 5, 1, 7, 4, 8, 3]`. Najduži rastući podniz je `[2, 5, 7, 8]`, duljine 4.

#### Rješenje ($O(n^2)$)

1. **Stanje:** `dp[i]` = duljina najdužeg rastućeg podniza koji **završava** na indeksu `i`.
2. **Rekurzivna relacija:** Za `dp[i]`, možemo proširiti bilo koji LIS koji završava na indeksu `j < i` ako je `array[j] < array[i]`. Želimo onaj najduži.
    `dp[i] = 1 + max({dp[j] | j < i and array[j] < array[i]})`.
    Ako takav `j` ne postoji, `dp[i] = 1`.
3. **Bazni slučaj:** `dp[i] = 1` za sve `i`, jer svaki element sam za sebe čini LIS duljine 1.
4. **Redoslijed:** Računamo `dp[i]` za `i` od 0 do `n-1`. Konačno rješenje je `max(dp[0], ..., dp[n-1])`.

**Kod:**

```cpp
vector<int> dp(n, 1);
for (int i = 0; i < n; ++i) {
    for (int j = 0; j < i; ++j) {
        if (array[j] < array[i]) {
            dp[i] = max(dp[i], dp[j] + 1);
        }
    }
}
cout << *max_element(dp.begin(), dp.end()) << '\n';
```

**Složenost:** **O(n²)** zbog dvije ugniježđene petlje. Postoji i O(n log n) rješenje, ali je naprednije.

### Problem 4: Udaljenost uređivanja (Edit Distance)

**Zadatak:** Zadana su dva stringa, A i B. Koja je minimalna cijena transformacije stringa A u string B koristeći operacije: umetanje, brisanje i zamjena znaka? Svaka operacija ima cijenu 1.

**Primjer:** A = "LOVE", B = "MOVIE". Udaljenost je 2.

1. LOVE -> MOVE (zamjena L sa M)
2. MOVE -> MOVIE (umetanje I)

#### Rješenje (2D DP, O(n*m))

1. **Stanje:** `dp[i][j]` = udaljenost uređivanja između prefiksa `A[0..i-1]` i `B[0..j-1]`.
2. **Rekurzivna relacija:** Za `dp[i][j]`, imamo tri mogućnosti:
    * **Umetanje:** Transformiramo `A[0..i-1]` u `B[0..j-2]`, a zatim umetnemo `B[j-1]`. Cijena: `dp[i][j-1] + 1`.
    * **Brisanje:** Transformiramo `A[0..i-2]` u `B[0..j-1]`, a zatim obrišemo `A[i-1]`. Cijena: `dp[i-1][j] + 1`.
    * **Zamjena/Podudaranje:** Transformiramo `A[0..i-2]` u `B[0..j-2]`.
        * Ako je `A[i-1] == B[j-1]`, nema dodatne cijene. Cijena: `dp[i-1][j-1]`.
        * Ako je `A[i-1] != B[j-1]`, zamijenimo znak. Cijena: `dp[i-1][j-1] + 1`.
    Konačna relacija: `dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)`.
3. **Bazni slučajevi:**
    * `dp[0][j] = j` (transformacija praznog stringa u prefiks od `j` znakova zahtijeva `j` umetanja).
    * `dp[i][0] = i` (transformacija prefiksa od `i` znakova u prazan string zahtijeva `i` brisanja).
4. **Redoslijed:** Popunjavamo `dp` tablicu redak po redak, stupac po stupac.

**Kod:**

```cpp
vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
for (int i = 0; i <= n; ++i) dp[i] = i;
for (int j = 0; j <= m; ++j) dp[j] = j;

for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= m; ++j) {
        int cost = (A[i-1] == B[j-1]) ? 0 : 1;
        dp[i][j] = min({dp[i-1][j] + 1,        // Brisanje
                        dp[i][j-1] + 1,        // Umetanje
                        dp[i-1][j-1] + cost}); // Zamjena/Podudaranje
    }
}
cout << dp[n][m] << '\n';
```

**Složenost:** **O(n * m)**, gdje su `n` i `m` duljine stringova.

---

## Zadaci za vježbu

### CSES Problem Set ([https://cses.fi/problemset/](https://cses.fi/problemset/))

Na stranici CSES se nalazi cijela kategorija zadataka Dynamic Programming. Neki od njih su:

* **[Dice Combinations](https://cses.fi/problemset/task/1633):** Klasičan 1D DP. Stanje `dp[i]` je broj načina da se dobije zbroj `i`.
* **[Minimizing Coins](https://cses.fi/problemset/task/1634):** Točno problem novčića (minimizacija) koji smo obradili.
* **[Coin Combinations I](https://cses.fi/problemset/task/1635):** Točno problem novčića (prebrojavanje) koji smo obradili.
* **[Coin Combinations II](https://cses.fi/problemset/task/1636):** Slično kao I, ali redoslijed novčića nije bitan. Zahtijeva malo drugačiji DP pristup.
* **[Removing Digits](https://cses.fi/problemset/task/1637):** Pohlepno rješenje radi, ali je i dobar uvod u "digit DP". `dp[n]` je minimalan broj koraka od `n` do 0.
* **[Grid Paths I](https://cses.fi/problemset/task/1638):** 2D DP na mreži, ali s preprekama.
* **[Book Shop](https://cses.fi/problemset/task/1158):** Klasičan 0-1 knapsack problem.
* **[Edit Distance](https://cses.fi/problemset/task/1639):** Točno problem udaljenosti uređivanja.

### Codeforces

Na stracnici Codeforces možete riješiti sve zadatke iz kategorije `dp` krenite od težine `800`, zadatke možete pronaći na [poveznici](https://codeforces.com/problemset?order=BY_RATING_ASC&tags=dp).

* **[Hit the Lottery](https://codeforces.com/problemset/problem/996/A):** (Problem 996A): Jednostavan pohlepni zadatak (problem novčića gdje pohlepni pristup radi). Dobar za usporedbu s DP-om.
* **[Vanya and Lanterns](https://codeforces.com/problemset/problem/492/B):** (Problem 492B): Ovaj problem se rješava sortiranjem i pohlepnim razmišljanjem, ali se može promatrati kao problem pokrivanja, što ima veze s DP-om.

[Sljedeća lekcija: Napredno dinamičko programiranje](../07-Advanced-Dynamic-Programming/){: .btn .btn-purple .float-right}
