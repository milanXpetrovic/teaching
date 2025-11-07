---
nav_exclude: true
---

# Tjedan 7: Napredno Dinamičko Programiranje

## Sadržaj

1. [Uvod i Motivacija](#uvod-i-motivacija)
    * [Nadogradnja Osnovnih DP Koncepata](#nadogradnja-osnovnih-dp-koncepata)
    * [Tipovi Naprednih DP Problema](#tipovi-naprednih-dp-problema)
    * [Preporučena Literatura](#preporučena-literatura)
2. [Primjeri Zadataka i Objašnjenja](#primjeri-zadataka-i-objašnjenja)
    * [Problem 1: Problem Ruksaka (The Knapsack Problem)](#problem-1-problem-ruksaka-the-knapsack-problem)
    * [Problem 2: Dinamičko Programiranje na Podskupovima (Bitmask DP)](#problem-2-dinamičko-programiranje-na-podskupovima-bitmask-dp)
    * [Problem 3: Dinamičko Programiranje na Stablima](#problem-3-dinamičko-programiranje-na-stablima)
3. [Zadaci za Vježbu](#zadaci-za-vježbu)

---

## Uvod i Motivacija

### Nadogradnja Osnovnih DP Koncepata

Prošli tjedan smo naučili osnove dinamičkog programiranja: rješavanje problema rastavljanjem na preklapajuće podprobleme i pamćenjem njihovih rješenja. Vidjeli smo kako se jednostavni 1D i 2D problemi mogu riješiti tabulacijom.

Ovaj tjedan idemo korak dalje. Proučit ćemo probleme gdje definiranje "stanja" nije tako očito i gdje se DP primjenjuje na složenije strukture od običnih nizova. Ključni principi ostaju isti:

1. **Definiraj stanje:** Koji su minimalni parametri potrebni za opis podproblema?
2. **Pronađi prijelaz (rekurzivnu relaciju):** Kako rješenje većeg problema ovisi o rješenjima manjih?
3. **Riješi podprobleme u ispravnom redoslijedu.**

### Tipovi Naprednih DP Problema

Ovaj tjedan ćemo obraditi tri ključne kategorije naprednog DP-a:

1. **Problem ruksaka (Knapsack):** Klasičan problem optimizacije koji ima brojne varijacije i primjene.
2. **DP na podskupovima (Bitmask DP):** Tehnika koja omogućuje rješavanje problema s eksponencijalnom složenošću `O(n^k * 2^n)` kada je `n` dovoljno malo (obično `n <= 20`). Stanje DP-a je predstavljeno bit-maskom.
3. **DP na stablima:** Tehnika za rješavanje problema na stablima, gdje se rješenje za čvor računa na temelju rješenja za njegovu djecu.

### Preporučena Literatura

* **CPH (Competitive Programmer's Handbook):**
  * Poglavlje 7: *Dynamic programming* (nastavak)
  * Poglavlje 10.5: *Dynamic programming* (za Bitmask DP)
  * Poglavlje 14: *Tree algorithms* (uvod u DP na stablima)
* **CLRS (Introduction to Algorithms):**
  * Poglavlje 15.3: *Elements of dynamic programming*
  * Poglavlje 16.2: *Elements of the greedy strategy* (za usporedbu s 0-1 knapsack problemom)

---

## Primjeri Zadataka i Objašnjenja

### Problem 1: Problem Ruksaka (The Knapsack Problem)

Ovo je jedan od najpoznatijih problema u algoritamskom programiranju. Postoji nekoliko varijanti, a mi ćemo obraditi dvije najvažnije.

**Zadatak (0-1 Knapsack):** Lopov provaljuje u trgovinu i pronalazi `n` predmeta. Svaki predmet `i` ima težinu `w_i` i vrijednost `v_i`. Lopov može nositi najviše `W` težine u svom ruksaku. Koje predmete treba uzeti da bi maksimizirao ukupnu vrijednost? Svaki predmet može uzeti jednom (0-1 odluka).

#### Rješenje (O(n * W))

Ovaj problem se ne može riješiti pohlepnim pristupom (npr. uzimanjem predmeta s najboljim omjerom vrijednosti i težine). Ispravno rješenje koristi dinamičko programiranje.

1. **Stanje:** `dp[i][w]` = maksimalna vrijednost koju možemo postići koristeći prvih `i` predmeta s ukupnom težinom najviše `w`.
2. **Prijelaz:** Za `i`-ti predmet, imamo dvije opcije:
    * **Ne uzeti `i`-ti predmet:** Maksimalna vrijednost je ista kao i za prvih `i-1` predmeta: `dp[i-1][w]`.
    * **Uzeti `i`-ti predmet:** Ovo je moguće samo ako je `w >= w_i`. Vrijednost je `v_i` plus maksimalna vrijednost koju možemo postići s prvih `i-1` predmeta i preostalim kapacitetom `w - w_i`: `v_i + dp[i-1][w - w_i]`.
    Konačna relacija je: `dp[i][w] = max(dp[i-1][w], v_i + dp[i-1][w - w_i])`.
3. **Bazni slučaj:** `dp[0][w] = 0` za sve `w`.
4. **Optimizacija prostora:** Primjećujemo da `dp[i]` ovisi samo o `dp[i-1]`. Možemo smanjiti prostor na `O(W)` koristeći samo jednodimenzionalno polje. Ključni trik je da unutarnju petlju (po težinama) moramo vrtjeti **unatrag** kako ne bismo iskoristili isti predmet više puta u istom koraku.

**Kod (optimiziran prostor):**

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int n, W;
    cin >> n >> W;
    vector<int> weights(n), values(n);
    for(int i = 0; i < n; ++i) cin >> weights[i] >> values[i];

    vector<int> dp(W + 1, 0);

    for (int i = 0; i < n; ++i) {
        for (int w = W; w >= weights[i]; --w) {
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }

    cout << dp[W] << '\n';
    return 0;
}
```

**Složenost:** Vremenska `O(n * W)`, prostorna `O(W)`.

### Problem 2: Dinamičko Programiranje na Podskupovima (Bitmask DP)

Ova tehnika se koristi kada je `n` malo (obično `n <= 20`), a stanje DP-a ovisi o podskupu elemenata. Podskup predstavljamo `n`-bitnim brojem (maskom).

**Zadatak (Traveling Salesperson Problem - TSP):** Zadan je skup od `n` gradova i udaljenosti između svakog para gradova. Pronađi najkraći put koji počinje u gradu 1, posjećuje svaki grad točno jednom i vraća se u grad 1.

#### Rješenje (O(n² * 2^n))

1. **Stanje:** `dp[mask][i]` = duljina najkraćeg puta koji počinje u gradu 1, posjećuje točno skup gradova predstavljen `maskom`, i završava u gradu `i`. `mask` je `n`-bitni broj gdje `j`-ti bit označava je li grad `j+1` posjećen.
2. **Prijelaz:** Da bismo izračunali `dp[mask][i]`, moramo doći u grad `i` iz nekog drugog grada `j` koji je već u `mask`. Put do grada `j` mora posjetiti gradove `mask` bez `i`.
    `dp[mask][i] = min(dp[mask ^ (1 << i)][j] + dist[j][i])`
    za sve `j` takve da je `j`-ti bit u `mask` postavljen i `j != i`.
3. **Bazni slučaj:** `dp[1 << 0][0] = 0`. Put koji počinje i završava u gradu 1 (predstavljen indeksom 0) i posjećuje samo njega ima duljinu 0.
4. **Redoslijed:** Iteriramo po veličini maske, zatim po svim maskama te veličine, pa po svim krajnjim gradovima `i`.

**Kod:**

```cpp
// Pretpostavke: n <= 20, dist[i][j] je matrica udaljenosti
// Gradovi su indeksirani 0..n-1
vector<vector<int>> dp(1 << n, vector<int>(n, INF));

// Bazni slučaj: put počinje i završava u gradu 0
dp[1 << 0] = 0;

for (int mask = 1; mask < (1 << n); ++mask) {
    for (int i = 0; i < n; ++i) {
        if ((mask >> i) & 1) { // Ako je grad i u maski
            for (int j = 0; j < n; ++j) {
                if (j != i && (mask >> j) & 1) { // Ako je i grad j u maski
                    int prev_mask = mask ^ (1 << i);
                    dp[mask][i] = min(dp[mask][i], dp[prev_mask][j] + dist[j][i]);
                }
            }
        }
    }
}

int ans = INF;
int final_mask = (1 << n) - 1;
for (int i = 0; i < n; ++i) {
    ans = min(ans, dp[final_mask][i] + dist[i]);
}

cout << ans << '\n';
```

**Složenost:** **O(n² * 2^n)**.

### Problem 3: Dinamičko Programiranje na Stablima

DP na stablima je tehnika gdje se rješenje za čvor računa na temelju rješenja za njegovu djecu. Obično se implementira pomoću DFS-a.

**Zadatak (Maximum Weight Independent Set on a Tree):** Zadano je stablo gdje svaki čvor `u` ima težinu `w_u`. Pronađi neovisan skup čvorova (nijedna dva nisu povezana bridom) s maksimalnom ukupnom težinom.

#### Rješenje (O(N))

1. **Stanje:** Za svaki čvor `u`, trebamo dvije vrijednosti:
    * `dp[u][0]`: maksimalna težina neovisnog skupa u podstablu s korijenom `u`, pod uvjetom da čvor `u` **nije** uključen u skup.
    * `dp[u][1]`: maksimalna težina neovisnog skupa u podstablu s korijenom `u`, pod uvjetom da čvor `u` **jest** uključen u skup.
2. **Prijelaz (računato u DFS-u):** Nakon rekurzivnog poziva za svu djecu `v` od `u`:
    * Ako **ne uzmemo** `u` (`dp[u][0]`): za svako dijete `v`, možemo uzeti ili ne uzeti `v`. Biramo bolju opciju: `max(dp[v][0], dp[v][1])`. Zbrajamo te vrijednosti za svu djecu.
    * Ako **uzmemo** `u` (`dp[u][1]`): **ne smijemo** uzeti nijedno od njegove djece. Dakle, uzimamo `w_u` i zbrajamo `dp[v][0]` za svu djecu `v`.
    `dp[u][0] = sum(max(dp[v][0], dp[v][1]))`
    `dp[u][1] = w_u + sum(dp[v][0])`
3. **Bazni slučaj:** Za list `u`, `dp[u][0] = 0` i `dp[u][1] = w_u`.
4. **Rješenje:** Nakon DFS-a od korijena `r`, konačno rješenje je `max(dp[r][0], dp[r][1])`.

**Kod:**```cpp
vector<int> adj[N];
vector<int> weights(N);
vector<vector<long long>> dp(N, vector<long long>(2));

void dfs(int u, int p) {
    dp[u] = 0;
    dp[u] = weights[u];

    for (int v : adj[u]) {
        if (v == p) continue;
        dfs(v, u);
        // Ako ne uzmemo u, za dijete v možemo uzeti najbolje rješenje
        dp[u] += max(dp[v], dp[v]);
        // Ako uzmemo u, ne smijemo uzeti dijete v
        dp[u] += dp[v];
    }
}

// U main funkciji, nakon izgradnje stabla
dfs(1, 0); // Krenemo od korijena 1, roditelj 0
cout << max(dp, dp) << '\n';

```
**Složenost:** **O(N)**, jer radimo jedan DFS prolaz kroz stablo.

---

## Zadaci za Vježbu

### CSES Problem Set ([https://cses.fi/problemset/](https://cses.fi/problemset/))

*   **Money Sums:** Varijacija knapsack problema. Stanje je `dp[i]`, boolean vrijednost koja govori je li zbroj `i` moguć.
*   **Rectangle Cutting:** 2D DP. `dp[w][h]` je minimalan broj rezova za pravokutnik `w x h`.
*   **Projects:** DP na sortiranim događajima. `dp[i]` je maksimalan profit koristeći prvih `i` projekata. Zahtijeva binarno pretraživanje za optimizaciju prijelaza.
*   **Elevator Rides:** Klasičan bitmask DP. Stanje je `dp[mask] = {broj_voznji, tezina_zadnje_voznje}`.
*   **Counting Tilings:** Teži bitmask DP (tzv. "DP on profiles"). `dp[i][mask]` je broj načina za popločavanje prvih `i` stupaca s profilom `mask`.
*   **Tree Diameter:** Iako se može riješiti s dva DFS-a, može se riješiti i DP-om na stablu.
*   **Tree Distances I & II:** Dva dobra zadatka za vježbu DP-a na stablima.

### Codeforces

*   **Flowers** (Problem 474D): Dobar uvodni DP zadatak koji se kombinira s prefiksnim sumama.
*   **Booking System** (Problem 416C): Problem uparivanja koji se može riješiti pohlepno nakon sortiranja, ali ima i DP rješenje (varijanta knapsacka).
*   **Little Elephant and Bits** (Problem 258A): Pohlepni zadatak, ali dobar za razmišljanje o tome kada DP nije potreban.
*   **Choosing Capital for a Treeland** (Problem 219D): Klasičan problem DP-a na stablima koji zahtijeva dva DFS prolaza (jedan "dolje", jedan "gore").
