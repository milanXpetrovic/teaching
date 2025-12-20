---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "NASLOV"
footer: "Programiranje za rješavanje složenih problema | Vježbe 2025/26"
---

<!-- _class: title -->

# Uvod u dinamičko programiranje
## Memoizacija, Tabulacija i Klasični Problemi

---

## Sadržaj

1. **Uvod i Teorija**
   - Što je DP?
   - Fibonaccijev niz: Zašto nam treba DP?
   - Memoizacija vs. Tabulacija
   - Recept za rješavanje DP problema
2. **Primjeri Zadataka**
   - Problem novčića (Minimizacija)
   - Problem novčića (Broj načina)
   - Najduži rastući podniz (LIS)
   - Udaljenost uređivanja (Edit Distance)
3. **Zadaci za vježbu**

---

## Što je Dinamičko Programiranje?

**Definicija:** Tehnika za rješavanje problema koji se mogu rastaviti na **preklapajuće podprobleme**.

Spaja najbolje od dva svijeta:
1. **Potpuna pretraga:** Garantira točnost (ispituje sve mogućnosti).
2. **Pohlepni algoritmi:** Efikasnost (ne računa istu stvar dvaput).

**Dva ključna svojstva problema:**
1. **Optimalna podstruktura:** Rješenje problema sadrži optimalna rješenja manjih podproblema.
2. **Preklapajući podproblemi:** Isti podproblemi se ponavljaju više puta tijekom izračuna.

---

## Primjer: Fibonaccijev niz

Definicija: $F(n) = F(n-1) + F(n-2)$.

**Naivna rekurzija:**
```cpp
int fib(int n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);
}
```
**Problem:** Eksponencijalna složenost $O(2^n)$.
Za `fib(5)` računamo `fib(3)` dvaput, `fib(2)` triput...

**Rješenje:** Pamtimo rezultate!

---

## Dva pristupa: Top-Down vs Bottom-Up

### 1. Memoizacija (Top-Down)
Zadržavamo rekurziju, ali dodajemo "cache" (mapu ili polje).
* Ako je rješenje u cache-u $\to$ vrati ga.
* Inače $\to$ izračunaj, **spremi** i vrati.

### 2. Tabulacija (Bottom-Up)
Iterativno rješavanje od najmanjih problema prema većima.
* Popunjavamo tablicu (polje) redom: `dp[0], dp[1], dp[2]...`
* Kada računamo `dp[i]`, vrijednosti `dp[i-1]` i `dp[i-2]` su već spremne.
* **Standard u natjecateljskom programiranju** (izbjegava overhead rekurzije).

---

## Koraci u rješavanju DP problema

1. **Definiraj stanje (State):**
   Što jedinstveno opisuje podproblem?
   * Npr. `dp[i]` = rješenje za prvih $i$ elemenata.

2. **Pronađi prijelaz (Transition):**
   Rekurzivna relacija koja povezuje stanje `dp[i]` s manjim stanjima.
   * Npr. `dp[i] = dp[i-1] + dp[i-2]`.

3. **Bazni slučajevi (Base cases):**
   Trivijalna rješenja koja znamo unaprijed.
   * Npr. `dp[0] = 0`.

4. **Redoslijed računanja:**
   Kako iterirati kroz stanja? (Obično `for i = 1 to n`).

---

## Problem 1: Minimizacija novčića

**Zadatak:** Imamo novčiće $\{c_1, c_2, \dots, c_k\}$ i iznos $N$. Nađi **minimalan** broj novčića za iznos $N$.

1. **Stanje:** `dp[x]` = min. broj novčića za iznos $x$.
2. **Prijelaz:** Zadnji dodani novčić može biti bilo koji $c_i$.
   $$ dp[x] = 1 + \min_{c \in coins} (dp[x - c]) $$
3. **Baza:** `dp[0] = 0` (0 novčića za iznos 0).
4. **Redoslijed:** $x$ od $1$ do $N$.

---

## Kod: Minimizacija novčića

```cpp
int main() {
    int n; cin >> n;
    vector<int> coins = {1, 3, 4};
    
    // Inicijaliziramo na "beskonačno"
    vector<int> dp(n + 1, 1e9);
    dp[0] = 0;

    for (int x = 1; x <= n; ++x) {
        for (int c : coins) {
            if (x - c >= 0) {
                dp[x] = min(dp[x], dp[x - c] + 1);
            }
        }
    }

    if (dp[n] == 1e9) cout << "Nemoguće\n";
    else cout << dp[n] << "\n";
}
```
**Složenost:** $O(N \cdot K)$.

---

## Problem 2: Broj načina (Coin Combinations)

**Zadatak:** Isti novčići i iznos $N$. Na **koliko načina** možemo formirati iznos $N$? (Redoslijed je bitan: 1+3 i 3+1 su različiti).

1. **Stanje:** `dp[x]` = broj načina za iznos $x$.
2. **Prijelaz:** Umjesto `min`, sada **zbrajamo** sve mogućnosti.
   $$ dp[x] = \sum_{c \in coins} dp[x - c] $$
3. **Baza:** `dp[0] = 1` (Jedan način da dobijemo 0 - ne uzmemo ništa).

---

## Kod: Broj načina

```cpp
int main() {
    int n; cin >> n;
    vector<int> coins = {1, 3, 4};
    long long MOD = 1e9 + 7;
    
    vector<long long> dp(n + 1, 0);
    dp[0] = 1;

    for (int x = 1; x <= n; ++x) {
        for (int c : coins) {
            if (x - c >= 0) {
                dp[x] = (dp[x] + dp[x - c]) % MOD;
            }
        }
    }
    cout << dp[n] << "\n";
}
```
**Razlika:** Samo smo promijenili `min` u `+` i maknuli `+1` (jer ne brojimo novčiće, već načine).

---

## Problem 3: Najduži rastući podniz (LIS)

**Zadatak:** Nađi duljinu najdužeg podniza (ne nužno uzastopnog) koji je strogo rastući.
Niz: `[6, 2, 5, 1, 7, 4, 8, 3]` $\to$ LIS: `[2, 5, 7, 8]` (duljina 4).

1. **Stanje:** `dp[i]` = duljina LIS-a koji **završava** na indeksu $i$.
2. **Prijelaz:** Gledamo sve prethodne elemente $j < i$. Ako je $A[j] < A[i]$, možemo produžiti niz.
   $$ dp[i] = 1 + \max(\{dp[j] \mid j < i, A[j] < A[i]\} \cup \{0\}) $$
3. **Rješenje:** $\max(dp[0] \dots dp[n-1])$.

---

## Kod: LIS ($O(N^2)$)

```cpp
int main() {
    int n; cin >> n;
    vector<int> a(n);
    for(int &x : a) cin >> x;

    vector<int> dp(n, 1); // Svaki element je LIS duljine 1 sam za sebe

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < i; ++j) {
            if (a[j] < a[i]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
    }
    
    // Tražimo maksimum u cijelom dp polju
    int ans = 0;
    for(int x : dp) ans = max(ans, x);
    cout << ans << "\n";
}
```

---

## Problem 4: Udaljenost uređivanja (Edit Distance)

**Zadatak:** Minimalan broj operacija (umetni, obriši, zamijeni) da pretvorimo string $A$ u $B$.
$A=$ "LOVE", $B=$ "MOVIE" $\to$ 2 operacije.

1. **Stanje:** `dp[i][j]` = cijena za prefikse $A[0..i]$ i $B[0..j]$.
2. **Prijelaz:**
   * Ako $A[i] == B[j]$: `dp[i-1][j-1]` (nema cijene).
   * Inače: $1 + \min($
     `dp[i-1][j]`,   // Brisanje
     `dp[i][j-1]`,   // Umetanje
     `dp[i-1][j-1]`  // Zamjena
   $)$

---

## Kod: Edit Distance ($O(N \cdot M)$)

```cpp
// Inicijalizacija: dp[i][0] = i (brisanja), dp[0][j] = j (umetanja)
for (int i = 0; i <= n; ++i) dp[i][0] = i;
for (int j = 0; j <= m; ++j) dp[0][j] = j;

for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= m; ++j) {
        if (A[i-1] == B[j-1]) {
            dp[i][j] = dp[i-1][j-1];
        } else {
            dp[i][j] = 1 + min({
                dp[i-1][j],    // Delete
                dp[i][j-1],    // Insert
                dp[i-1][j-1]   // Replace
            });
        }
    }
}
cout << dp[n][m] << "\n";
```

---

## Zadaci za vježbu (CSES)

**Link:** [cses.fi/problemset/](https://cses.fi/problemset/) (Sekcija Dynamic Programming)

1.  **Dice Combinations:** Koliko načina da dobijemo zbroj bacanjem kocke?
2.  **Minimizing Coins:** Problem 1 iz lekcije.
3.  **Coin Combinations I:** Problem 2 iz lekcije.
4.  **Removing Digits:** Od broja $N$ oduzimamo jednu od njegovih znamenki dok ne dođemo do 0. Min koraka?
5.  **Grid Paths I:** Broj puteva u mreži s preprekama.
6.  **Book Shop:** 0-1 Knapsack (sljedeći put detaljnije).
7.  **Edit Distance:** Problem 4 iz lekcije.

---

<!-- _class: lead -->

# Pitanja?

Sljedeći put: Napredno dinamičko programiranje (Knapsack, Bitmask).
```