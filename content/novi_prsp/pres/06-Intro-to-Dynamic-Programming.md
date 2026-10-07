---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Uvod u dinamičko programiranje"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!-- _paginate: false -->
<!-- _class: title -->

# Uvod u dinamičko programiranje

## Memoizacija, tabulacija i klasični problemi

---

# Sadržaj

1. **Uvod i teorija**
   - Što je DP?
   - Fibonaccijev niz: zašto nam treba DP?
   - Memoizacija vs. tabulacija
   - Recept za rješavanje DP problema
2. **Primjeri zadataka**
   - Problem novčića (minimizacija)
   - Problem novčića (broj načina)
   - Najduži rastući podniz (LIS)
   - Udaljenost uređivanja (Edit Distance)
3. **Analiza CSES zadataka** (detaljna rješenja)

---

# Što je dinamičko programiranje?

**Definicija:** Tehnika za rješavanje problema koji se mogu rastaviti na **preklapajuće podprobleme**.

Spaja najbolje od dva svijeta:

1. **Potpuna pretraga:** točnost (razmatra sve mogućnosti).
2. **Pohlepni algoritmi:** efikasnost.

Efikasnost postiže tako što **svaki podproblem računa samo jednom**.

**Dva ključna svojstva problema:**

1. **Optimalna podstruktura:** Rješenje problema sadrži optimalna rješenja manjih podproblema.
2. **Preklapajući podproblemi:** Isti podproblemi se ponavljaju više puta tijekom izračuna.

---

# Primjer: Fibonaccijev niz

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

# Dva pristupa: top-down vs. bottom-up

**1. Memoizacija (top-down)**

Zadržavamo rekurziju, ali dodajemo "cache" (mapu ili polje).

- Ako je rješenje u cacheu $\to$ vratimo ga.
- Inače $\to$ izračunamo ga, **spremimo** i vratimo.

**2. Tabulacija (bottom-up)**

Iterativno rješavanje od najmanjih problema prema većima.

- Popunjavamo tablicu (polje) redom: `dp[0], dp[1], dp[2]...`
- Kada računamo `dp[i]`, vrijednosti `dp[i-1]` i `dp[i-2]` su već spremne.
- **Standard u natjecateljskom programiranju** (izbjegava overhead rekurzije).

---

# Fibonacci: memoizacija i tabulacija u kodu

```cpp
// Memoizacija (top-down)
long long memo[93];
bool done[93];

long long fib(int n) {
    if (n <= 1) return n;
    if (done[n]) return memo[n];   // Već izračunato
    done[n] = true;
    return memo[n] = fib(n-1) + fib(n-2);
}

// Tabulacija (bottom-up), za n >= 1
vector<long long> dp(n + 1);
dp[0] = 0; dp[1] = 1;
for (int i = 2; i <= n; i++) dp[i] = dp[i-1] + dp[i-2];
```

Obje verzije su $O(n)$. (`long long` drži $F(n)$ do $n = 92$.)

---

# Koraci u rješavanju DP problema

1. **Definiramo stanje (State):**
   Što jedinstveno opisuje podproblem?
   - Npr. `dp[i]` = rješenje za prvih $i$ elemenata.

2. **Pronađemo prijelaz (Transition):**
   Rekurzivna relacija koja povezuje stanje `dp[i]` s manjim stanjima.
   - Npr. `dp[i] = dp[i-1] + dp[i-2]`.

3. **Postavimo bazne slučajeve (Base cases):**
   Trivijalna rješenja koja znamo unaprijed.
   - Npr. `dp[0] = 0`.

4. **Odredimo redoslijed računanja:**
   Kako iterirati kroz stanja? (Obično `for i = 1 to n`.)

---

# Problem 1: Minimizacija novčića

**Zadatak:** Imamo novčiće $\{c_1, c_2, \dots, c_k\}$ i iznos $N$. Treba naći **minimalan** broj novčića za iznos $N$.

1. **Stanje:** `dp[x]` = min. broj novčića za iznos $x$.
2. **Prijelaz:** Zadnji dodani novčić može biti bilo koji $c_i$.
   $$ dp[x] = 1 + \min_{c \in coins} (dp[x - c]) $$
3. **Baza:** `dp[0] = 0` (0 novčića za iznos 0).
4. **Redoslijed:** $x$ od $1$ do $N$.

---

# Kod: Minimizacija novčića

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

# Problem 2: Broj načina (Coin Combinations)

**Zadatak:** Isti novčići i iznos $N$. Na **koliko načina** možemo formirati iznos $N$? (Redoslijed je bitan: 1+3 i 3+1 su različiti.)

1. **Stanje:** `dp[x]` = broj načina za iznos $x$.
2. **Prijelaz:** Umjesto `min`, sada **zbrajamo** sve mogućnosti.
   $$ dp[x] = \sum_{c \in coins} dp[x - c] $$
3. **Baza:** `dp[0] = 1` (jedan način da dobijemo 0: ne uzmemo ništa).

---

# Kod: Broj načina

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
**Ako redoslijed nije bitan** (1+3 = 3+1): zamijenimo petlje, vanjska ide po novčićima, a unutarnja po iznosu.

---

# Problem 3: Najduži rastući podniz (LIS)

**Zadatak:** Treba naći duljinu najdužeg podniza (ne nužno uzastopnog) koji je strogo rastući.
Niz: `[6, 2, 5, 1, 7, 4, 8, 3]` $\to$ LIS: `[2, 5, 7, 8]` (duljina 4).

1. **Stanje:** `dp[i]` = duljina LIS-a koji **završava** na indeksu $i$.
2. **Prijelaz:** Gledamo sve prethodne elemente $j < i$. Ako je $A[j] < A[i]$, možemo produžiti niz.
   $$ dp[i] = 1 + \max(\{dp[j] \mid j < i, A[j] < A[i]\} \cup \{0\}) $$
3. **Rješenje:** $\max(dp[0] \dots dp[n-1])$.

---

# Kod: LIS ($O(N^2)$)

```cpp
int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;

    vector<int> dp(n, 1); // Svaki element je sam za sebe LIS duljine 1

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < i; ++j) {
            if (a[j] < a[i]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
    }

    // Tražimo maksimum u cijelom dp polju
    int ans = 0;
    for (int x : dp) ans = max(ans, x);
    cout << ans << "\n";
}
```

Za $n$ do $2 \cdot 10^5$ (CSES Increasing Subsequence) treba $O(N \log N)$ verzija s binarnim pretraživanjem.

---

# Problem 4: Udaljenost uređivanja (Edit Distance)

**Zadatak:** Minimalan broj operacija (umetanje, brisanje, zamjena) da pretvorimo string $A$ u $B$.
$A=$ "LOVE", $B=$ "MOVIE" $\to$ 2 operacije.

1. **Stanje:** `dp[i][j]` = minimalan broj operacija za pretvaranje prvih $i$ znakova od $A$ u prvih $j$ znakova od $B$.
2. **Prijelaz:**
   - Ako je `A[i-1] == B[j-1]`: `dp[i][j] = dp[i-1][j-1]` (nema cijene).
   - Inače: `dp[i][j]` $= 1 + \min$ od:
     - `dp[i-1][j]` (brisanje)
     - `dp[i][j-1]` (umetanje)
     - `dp[i-1][j-1]` (zamjena)

---

# Kod: Edit Distance ($O(N \cdot M)$)

```cpp
vector<vector<int>> dp(n + 1, vector<int>(m + 1));

// Inicijalizacija: dp[i][0] = i (brisanja), dp[0][j] = j (umetanja)
for (int i = 0; i <= n; ++i) dp[i][0] = i;
for (int j = 0; j <= m; ++j) dp[0][j] = j;

for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= m; ++j) {
        if (A[i-1] == B[j-1]) {
            dp[i][j] = dp[i-1][j-1];
        } else {
            dp[i][j] = 1 + min({
                dp[i-1][j],    // Brisanje
                dp[i][j-1],    // Umetanje
                dp[i-1][j-1]   // Zamjena
            });
        }
    }
}
cout << dp[n][m] << "\n";
```

---

# Odgovarajući CSES zadaci

- **[Minimizing Coins](https://cses.fi/problemset/task/1634):** Problem 1.
- **[Coin Combinations I](https://cses.fi/problemset/task/1635):** Problem 2 (redoslijed je bitan).
- **[Coin Combinations II](https://cses.fi/problemset/task/1636):** Problem 2 (redoslijed nije bitan).
- **[Increasing Subsequence](https://cses.fi/problemset/task/1145):** Problem 3 ($O(N \log N)$).
- **[Edit Distance](https://cses.fi/problemset/task/1639):** Problem 4.

---

<!-- _class: title -->
# Analiza: CSES zadaci

## Primjena naučenog na konkretnim problemima

---

<!-- _class: title -->
# 1. Dice Combinations (CSES)

## Varijacija problema novčića

---

# Analiza: Dice Combinations (1/2)

**Problem:**
Želimo dobiti zbroj $N$ bacanjem kocke (vrijednosti 1-6). Na koliko načina to možemo učiniti?
Npr. $N=3$: `1+1+1`, `1+2`, `2+1`, `3`. (Ukupno 4.)

**Intuicija:**
Zamislimo da želimo dobiti zbroj $i$. Koje je bilo **zadnje** bacanje?
Moglo je biti 1, 2, 3, 4, 5 ili 6.

- Ako je zadnje bacanje bilo **1**, prethodni zbroj je morao biti $i-1$.
- Ako je zadnje bacanje bilo **2**, prethodni zbroj je morao biti $i-2$.
- ...
- Ako je zadnje bacanje bilo **6**, prethodni zbroj je morao biti $i-6$.

Ukupan broj načina za $i$ je zbroj načina za sva ta prethodna stanja.

---

# Analiza: Dice Combinations (2/2)

**Definicija DP stanja:**
`dp[i]` = broj načina da dobijemo zbroj $i$.

**Rekurzivna veza (prijelaz):**
$$ dp[i] = dp[i-1] + dp[i-2] + dp[i-3] + dp[i-4] + dp[i-5] + dp[i-6] $$
*(Uzimamo u obzir samo članove čiji je indeks $\ge 0$.)*

**Bazni slučaj:**
`dp[0] = 1`. Postoji točno jedan način da dobijemo zbroj 0 (tako da kocku ne bacimo nijednom).

---

# Implementacija: Dice Combinations

```cpp
int n; cin >> n;
vector<long long> dp(n + 1, 0);
dp[0] = 1;
long long MOD = 1e9 + 7;

for (int i = 1; i <= n; ++i) {
    // Pokušavamo svaku moguću vrijednost kocke (1 do 6)
    for (int j = 1; j <= 6; ++j) {
        if (i - j >= 0) {
            dp[i] = (dp[i] + dp[i - j]) % MOD;
        }
    }
}
cout << dp[n] << "\n";
```

**Složenost:** $O(N)$ (unutarnja petlja je konstantna, vrti se 6 puta).

---

<!-- _class: title -->
# 2. Removing Digits (CSES)

## Pohlepno ili DP?

---

# Analiza: Removing Digits (1/2)

**Problem:**
Imamo broj $N$. U jednom koraku možemo oduzeti bilo koju znamenku koja se trenutno nalazi u broju.
Cilj: doći do 0 u **minimalnom** broju koraka.
Npr. $27 \to 27-7=20 \to 20-2=18 \dots$

**Intuicija:**
Ovo je problem minimizacije. Iz trenutnog stanja (broj $i$) možemo prijeći u više novih stanja.
Ako broj $i$ ima znamenke $\{d_1, d_2, \dots\}$, možemo prijeći u stanja $i-d_1, i-d_2, \dots$.
Budući da tražimo minimum, želimo odabrati potez koji nas najbrže vodi do 0.

---

# Analiza: Removing Digits (2/2)

**Pristupi:**

1. **Pohlepni pristup:** Uvijek oduzmemo **najveću** znamenku.
   - Za ovaj problem pohlepno daje optimalno rješenje, ali dokaz nije trivijalan.
   - Oprez: intuicija "najbrže smanjujemo broj" ista je ona koja je pala kod novčića $\{1, 3, 4\}$.

2. **DP pristup (sigurniji i općenitiji):**
   - **Stanje:** `dp[i]` = min. broj koraka od $i$ do 0.
   - **Prijelaz:** `dp[i] = 1 + min(dp[i - d])` za svaku znamenku $d$ u broju $i$.
   - **Baza:** `dp[0] = 0`.

---

# Implementacija: Removing Digits (DP)

```cpp
int n; cin >> n;
vector<int> dp(n + 1, 1e9); // Inicijalizacija na beskonačno
dp[0] = 0;

for (int i = 1; i <= n; ++i) {
    // Izdvajanje znamenki broja i
    int temp = i;
    while (temp > 0) {
        int digit = temp % 10;
        temp /= 10;

        // Prijelaz: ako oduzmemo 'digit', dolazimo u stanje 'i - digit'
        // i treba nam 1 korak više nego za to stanje.
        if (digit > 0) {
            dp[i] = min(dp[i], dp[i - digit] + 1);
        }
    }
}
cout << dp[n] << "\n";
```

---

<!-- _class: title -->
# 3. Grid Paths I (CSES)

## 2D dinamičko programiranje

---

# Analiza: Grid Paths I (1/2)

**Problem:**
Mreža $N \times N$. Neka polja su prazna (`.`), neka su zamke (`*`).
Možemo se kretati samo **dolje** i **desno**.
Na koliko načina možemo doći od $(0,0)$ do $(N-1, N-1)$?

**Intuicija:**
Na polje $(i, j)$ možemo doći samo iz dva smjera:

1. **Odozgo:** s polja $(i-1, j)$.
2. **Slijeva:** s polja $(i, j-1)$.

Dakle, broj načina da dođemo do $(i, j)$ jednak je zbroju načina da dođemo do gornjeg i do lijevog polja.

---

# Analiza: Grid Paths I (2/2)

**Definicija DP stanja:**
`dp[i][j]` = broj putova od $(0,0)$ do $(i,j)$.

**Prijelaz:**

- Ako je `grid[i][j] == '*'`: `dp[i][j] = 0` (ne možemo stati na zamku).
- Inače: `dp[i][j] = dp[i-1][j] + dp[i][j-1]`.
  *(Pazite na rubove matrice gdje je $i=0$ ili $j=0$.)*

**Baza:**

- Ako je `grid[0][0] == '.'`, onda je `dp[0][0] = 1`.
- Inače je `dp[0][0] = 0`.

---

# Implementacija: Grid Paths I

```cpp
int n; cin >> n;
vector<string> grid(n);
for (int i = 0; i < n; ++i) cin >> grid[i];

vector<vector<int>> dp(n, vector<int>(n, 0));
long long MOD = 1e9 + 7;

// Baza: ako start nije zamka, postoji 1 način da budemo na startu
if (grid[0][0] == '.') dp[0][0] = 1;

for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
        if (grid[i][j] == '*') {
            dp[i][j] = 0; // Zamka - ne možemo doći ovdje
        } else {
            // Zbrajamo putove odozgo i slijeva
            if (i > 0) dp[i][j] = (dp[i][j] + dp[i-1][j]) % MOD;
            if (j > 0) dp[i][j] = (dp[i][j] + dp[i][j-1]) % MOD;
        }
    }
}
cout << dp[n-1][n-1] << "\n";
```

---

<!-- _class: title -->
# 4. Book Shop (CSES)

## 0-1 Knapsack Problem

---

# Analiza: Book Shop (1/2)

**Problem:**
Imamo $N$ knjiga. Svaka ima cijenu $price_i$ i broj stranica $pages_i$.
Imamo budžet $X$. Želimo kupiti knjige tako da maksimiziramo ukupan broj stranica, a da ne prijeđemo budžet.

**Tip problema:**
Ovo je školski primjer **0-1 Knapsack problema**.

- "0-1" znači da svaku knjigu možemo uzeti ili ne uzeti (ne možemo uzeti pola, niti više komada iste knjige).

**Pohlepni pristup ne radi:**
Ne možemo samo uzimati knjige s najboljim omjerom stranica/cijena.

---

# Analiza: Book Shop (2/2)

**DP stanje:**
`dp[w]` = maksimalan broj stranica koje možemo dobiti uz potrošnju **najviše** $w$.

**Prijelaz:**
Kada razmatramo novu knjigu s cijenom $P$ i stranicama $S$, za svaki mogući budžet $w$ imamo dvije opcije:

1. **Ne kupimo knjigu:** broj stranica ostaje `dp[w]`.
2. **Kupimo knjigu:** trošimo $P$, pa nam ostaje $w-P$. Broj stranica je `dp[w-P] + S`.

Uzimamo maksimum: `dp[w] = max(dp[w], dp[w-P] + S)`.

**Ključni trik:**
Da bismo koristili 1D niz, moramo iterirati po budžetu **unatrag** (od $X$ do $P$). Ako idemo unaprijed, mogli bismo istu knjigu iskoristiti više puta.

---

# Implementacija: Book Shop

```cpp
int n, x; cin >> n >> x;
vector<int> price(n), pages(n);
for (int &p : price) cin >> p;
for (int &p : pages) cin >> p;

// dp[w] = max stranica uz potrošnju najviše w
vector<int> dp(x + 1, 0);

for (int i = 0; i < n; ++i) {
    // Iteracija unatrag je KLJUČNA za 0-1 Knapsack s 1D nizom!
    // Osigurava da svaku knjigu koristimo najviše jednom.
    for (int w = x; w >= price[i]; --w) {
        dp[w] = max(dp[w], dp[w - price[i]] + pages[i]);
    }
}
cout << dp[x] << "\n";
```

**Složenost:** $O(N \cdot X)$.

---

<!-- _class: lead -->

# Pitanja?

Sljedeći put: Napredno dinamičko programiranje (Knapsack varijacije, Bitmask).
