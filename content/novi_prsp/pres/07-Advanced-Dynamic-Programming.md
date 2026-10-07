---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Napredno dinamičko programiranje"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!-- _paginate: false -->
<!-- _class: title -->

# Napredno dinamičko programiranje

## Knapsack, Bitmask DP i DP na stablima

---

# Sadržaj

1. **Uvod**
   - Nadogradnja osnovnih koncepata
2. **Problem ruksaka (Knapsack)**
   - 0-1 Knapsack i optimizacija prostora
3. **Bitmask DP**
   - Traveling Salesperson Problem (TSP)
4. **DP na stablima**
   - Maximum Weight Independent Set
5. **Zadaci za vježbu**

---

# Uvod: korak dalje od tablice

Prošli put: jednostavni 1D i 2D problemi (nizovi, matrice).
Danas: **složenija stanja i strukture.**

**Ključni koraci ostaju isti:**

1. **Definiramo stanje:** Koji minimalni parametri opisuju podproblem?
   - *Npr. "Koji podskup gradova smo posjetili?"*
2. **Pronađemo prijelaz:** Veza između većeg i manjih problema.
3. **Odredimo redoslijed rješavanja:** Topološki redoslijed (od manjeg prema većem, ili od listova prema korijenu).

**Tri glavne teme danas:**

1. **Knapsack:** Optimizacija resursa.
2. **Bitmask DP:** Problemi na podskupovima ($N \le 20$).
3. **Tree DP:** Problemi na stablima (bez ciklusa).

---

# 1. Problem ruksaka (0-1 Knapsack)

**Zadatak:** Imamo ruksak kapaciteta $W$ i $N$ predmeta. Svaki predmet ima težinu $w_i$ i vrijednost $v_i$.
Svaki predmet možemo uzeti **jednom** (0 ili 1) ili ne uzeti. Treba maksimizirati ukupnu vrijednost.

**Pokušaj (pohlepno):** Uzimati predmete s najboljim omjerom $v_i/w_i$?

- **Ne radi!** Primjer: $W=4$, predmeti (težina, vrijednost): $\{(3, 5), (2, 3), (2, 3)\}$.
- Prvi ima najbolji omjer ($5/3$), pa ga pohlepno uzimamo i dobivamo 5. Ostatak kapaciteta (1) nije dovoljan ni za što.
- Optimalno je uzeti zadnja dva: vrijednost 6.

---

# 0-1 Knapsack: DP formulacija

**DP stanje:**
`dp[i][w]` = maksimalna vrijednost koristeći prvih $i$ predmeta s kapacitetom $w$.

**Prijelaz:**
$$ dp[i][w] = \max(dp[i-1][w], \quad v_i + dp[i-1][w - w_i]) $$
*(Opcija 1: ne uzmemo predmet $i$. Opcija 2: uzmemo predmet $i$, samo ako je $w \ge w_i$.)*

---

# Knapsack: optimizacija prostora

Primijetimo: da bismo izračunali redak $i$, trebamo samo redak $i-1$.
Možemo koristiti **samo jedan niz** `dp[w]`.

**Ključni detalj:** Iteriramo po težini **unatrag**, da ne bismo iskoristili *isti predmet* više puta u istoj iteraciji.

```cpp
vector<int> dp(W + 1, 0);

for (int i = 0; i < n; ++i) {
    // Idemo UNATRAG da simuliramo "uzmi najviše jednom"
    for (int w = W; w >= weights[i]; --w) {
        dp[w] = max(dp[w], dp[w - weights[i]] + values[i]);
    }
}
cout << dp[W] << "\n";
```

**Složenost:** $O(N \cdot W)$.

---

# 2. DP na podskupovima (Bitmask DP)

Koristi se kad je $N$ mali ($N \le 20$), a stanje ovisi o **skupu** posjećenih/iskorištenih elemenata.
Skup prikazujemo kao **bitmasku** (integer).

- Ako je $j$-ti bit 1 $\to$ element $j$ je u skupu.

**Primjer: Traveling Salesperson Problem (TSP)**

**Zadatak:** Treba obići $N$ gradova točno jednom i vratiti se na početak, uz minimalan put.
**Stanje:** `dp[mask][i]`

- `mask`: skup posjećenih gradova.
- `i`: trenutni grad (zadnji posjećen).

**Vrijednost:** duljina najkraćeg puta koji prolazi kroz `mask` i završava u `i`.

---

# TSP: implementacija

**Prijelaz:** U grad `i` dolazimo iz nekog grada `j` koji je već u maski.
$$ dp[\text{mask}][i] = \min_{j \in \text{mask}, j \neq i} (dp[\text{mask} \setminus \{i\}][j] + \text{dist}[j][i]) $$

```cpp
// dp[mask][i] = INF (npr. 1e9, ne INT_MAX zbog zbrajanja), osim dp[1][0] = 0
for (int mask = 1; mask < (1 << n); ++mask) {
    for (int i = 0; i < n; ++i) {
        if ((mask >> i) & 1) { // Ako je grad 'i' u trenutnom skupu
            int prev_mask = mask ^ (1 << i); // Stanje prije dolaska u 'i'
            if (prev_mask == 0) continue;   // Bazni slučaj je već riješen

            for (int j = 0; j < n; ++j) {
                if ((prev_mask >> j) & 1) { // Pokušavamo doći iz 'j' u 'i'
                    dp[mask][i] = min(dp[mask][i], dp[prev_mask][j] + dist[j][i]);
                }
            }
        }
    }
}
```

**Povratak na početak:** odgovor je $\min_i (dp[\text{full}][i] + \text{dist}[i][0])$.
**Složenost:** $O(N^2 \cdot 2^N)$, pa je za TSP realno $N \le 16$ do $18$.

---

# 3. DP na stablima (Tree DP)

Stabla nemaju cikluse $\to$ idealno za DP.
Redoslijed rješavanja: **post-order DFS** (od listova prema korijenu).
Rješenje za čvor $u$ ovisi o rješenjima njegove djece $v$.

**Zadatak: Maximum Weight Independent Set**

Treba naći skup čvorova s najvećom ukupnom težinom tako da **nikoja dva čvora nisu susjedi**.

**Stanje za čvor $u$:**

1. `dp[u][0]`: ne uzimamo $u$. Djeca mogu biti uzeta ili ne.
2. `dp[u][1]`: uzimamo $u$. Djeca **ne smiju** biti uzeta.

**Prijelaz:**
$$ dp[u][0] = \sum_{v \in children(u)} \max(dp[v][0], dp[v][1]) $$
$$ dp[u][1] = w_u + \sum_{v \in children(u)} dp[v][0] $$

---

# Tree DP: implementacija

```cpp
long long dp[MAXN][2]; // 0: ne uzimamo, 1: uzimamo

void dfs(int u, int p) {
    dp[u][0] = 0;
    dp[u][1] = weights[u]; // Ako uzmemo u, imamo njegovu težinu

    for (int v : adj[u]) {
        if (v == p) continue; // Preskačemo roditelja
        dfs(v, u);            // Prvo rješavamo za djecu

        // Ako ne uzmemo u, za v biramo bolju opciju (uzeti ili ne)
        dp[u][0] += max(dp[v][0], dp[v][1]);

        // Ako uzmemo u, v ne smijemo uzeti
        dp[u][1] += dp[v][0];
    }
}

// U main: dfs(1, 0); cout << max(dp[1][0], dp[1][1]);
```

**Složenost:** $O(N)$ (jedan prolaz kroz stablo).

---

# Zadaci za vježbu (CSES i Codeforces)

**CSES Problem Set**

1. **[Money Sums](https://cses.fi/problemset/task/1745):** Knapsack varijacija (koje sume su moguće?).
2. **[Rectangle Cutting](https://cses.fi/problemset/task/1744):** 2D DP (rezanje pravokutnika).
3. **[Elevator Rides](https://cses.fi/problemset/task/1653):** Bitmask DP (pakiranje ljudi u liftove).
4. **[Projects](https://cses.fi/problemset/task/1140):** DP na intervalima + binarno pretraživanje.
5. **[Tree Diameter](https://cses.fi/problemset/task/1131):** Može se riješiti kao Tree DP (najduži put kroz $u$).
6. **[Tree Distances I](https://cses.fi/problemset/task/1132) i [II](https://cses.fi/problemset/task/1133):** Napredniji Tree DP (rerooting).

**Codeforces**

- Tražite tagove `dp`, `bitmasks`, `trees`.

---

<!-- _class: title -->
# Money Sums (CSES)

## Koje sume možemo formirati?

---

# Analiza: Money Sums (1/2)

**Problem:**
Imamo $N$ novčića s vrijednostima $x_1, \dots, x_N$.
Koje sve **različite sume** možemo formirati koristeći ove novčiće?
Npr. $\{4, 2, 5\}$ $\to$ sume: 2, 4, 5, 6 (2+4), 7 (2+5), 9 (4+5), 11 (2+4+5).

**Intuicija:**
Ovo je varijacija **Knapsack problema** (Subset Sum).
Umjesto maksimalne vrijednosti zanima nas **dostupnost** (boolean).
Maksimalna moguća suma je $N \times 1000 = 100 \times 1000 = 10^5$. To je dovoljno malo za DP tablicu.

---

# Analiza: Money Sums (2/2)

**DP stanje:**
`dp[s]` = je li moguće formirati sumu $s$? (true/false)

**Prijelaz:**
Kada razmatramo novčić vrijednosti $v$:
ako smo mogli formirati sumu $S$ bez ovog novčića, onda s ovim novčićem možemo formirati sumu $S + v$.

$$ dp[s] = dp[s] \lor dp[s - v] $$

**Redoslijed:**
Kao kod 0-1 Knapsacka, po sumama iteriramo **unatrag** (ili koristimo 2D polje, ali 1D je bolje).

---

# Implementacija: Money Sums

```cpp
int n; cin >> n;
vector<int> x(n);
for (int &v : x) cin >> v;

int max_sum = n * 1000;
vector<bool> dp(max_sum + 1, false);
dp[0] = true; // Sumu 0 možemo uvijek formirati (prazan skup)

for (int coin : x) {
    // Iteriramo unatrag da ne koristimo isti novčić više puta
    for (int s = max_sum; s >= coin; --s) {
        if (dp[s - coin]) dp[s] = true;
    }
}

vector<int> result;
for (int s = 1; s <= max_sum; ++s) if (dp[s]) result.push_back(s);

cout << result.size() << "\n";
for (int s : result) cout << s << " ";
cout << "\n";
```

---

<!-- _class: title -->
# Rectangle Cutting (CSES)

## 2D dinamičko programiranje

---

# Analiza: Rectangle Cutting (1/2)

**Problem:**
Pravokutnik dimenzija $a \times b$ želimo izrezati na kvadrate.
Koji je **minimalan broj rezova**?

**Intuicija:**
Svaki rez dijeli pravokutnik na dva manja pravokutnika.
Rez može biti:

1. **Vertikalan:** dijeli $w \times h$ na $i \times h$ i $(w-i) \times h$.
2. **Horizontalan:** dijeli $w \times h$ na $w \times j$ i $w \times (h-j)$.

Isprobamo **sve moguće rezove** i uzmemo onaj koji daje minimalan zbroj rezova za dva dobivena dijela.

---

# Analiza: Rectangle Cutting (2/2)

**Stanje:** `dp[w][h]` = min. broj rezova za pravokutnik $w \times h$.

**Baza:**
Ako je $w = h$, `dp[w][h] = 0` (već je kvadrat, ne treba rezati).

**Prijelaz:**
$$ dp[w][h] = 1 + \min \left( \min_{i=1}^{w-1}(dp[i][h] + dp[w-i][h]), \quad \min_{j=1}^{h-1}(dp[w][j] + dp[w][h-j]) \right) $$

*(1 + ... jer trenutni rez brojimo kao 1.)*

---

# Implementacija: Rectangle Cutting

```cpp
// dp tablica inicijalizirana na beskonačno
for (int w = 1; w <= a; ++w) {
    for (int h = 1; h <= b; ++h) {
        if (w == h) {
            dp[w][h] = 0;
        } else {
            // Probamo sve vertikalne rezove
            for (int i = 1; i < w; ++i)
                dp[w][h] = min(dp[w][h], 1 + dp[i][h] + dp[w-i][h]);

            // Probamo sve horizontalne rezove
            for (int i = 1; i < h; ++i)
                dp[w][h] = min(dp[w][h], 1 + dp[w][i] + dp[w][h-i]);
        }
    }
}
cout << dp[a][b] << "\n";
```

**Složenost:** $O(A \cdot B \cdot (A+B))$. Za $A, B \le 500$ to je oko $1,25 \cdot 10^8$ operacija, što prolazi.

---

<!-- _class: title -->
# Elevator Rides (CSES)

## Bitmask DP u praksi

---

# Analiza: Elevator Rides (1/2)

**Problem:**
$N$ ljudi s težinama $w_i$. Lift ima nosivost $X$.
Koliko je minimalno vožnji potrebno da se prevezu svi ljudi? ($N \le 20$)

**Zašto je ovo teško?**
Ovo je **Bin Packing problem**, koji je NP-težak. Pohlepni pristup (trpamo dok stane) ne daje optimalno rješenje.
Srećom, $N$ je mali ($N \le 20$), što dopušta eksponencijalnu složenost $O(2^N \cdot N)$.

**Ideja:**
Koristimo **Bitmask DP**. Maska predstavlja skup ljudi koji su već prevezeni.

---

# Analiza: Elevator Rides (2/2)

**Stanje:**
Nije dovoljno pamtiti samo broj vožnji. Trebamo znati koliko je mjesta ostalo u zadnjoj vožnji da vidimo stane li još netko.
`dp[mask]` = par `{broj_vožnji, težina_u_zadnjoj_vožnji}`.

**Cilj:**
Za svaku masku želimo:

1. Minimalan broj vožnji.
2. Uz minimalan broj vožnji, minimalnu težinu u zadnjoj (da ostane više mjesta za druge).

**Prijelaz:**
Pokušamo dodati osobu $i$ (koja nije u maski) u trenutno stanje.

- Ako stane u zadnju vožnju $\to$ dodamo je tamo.
- Ako ne stane $\to$ nova vožnja.

---

# Implementacija: Elevator Rides

```cpp
vector<pair<int, int>> dp(1 << n); // {rides, last_weight}
dp[0] = {1, 0}; // Počinjemo s jednom (praznom) vožnjom

for (int mask = 1; mask < (1 << n); ++mask) {
    dp[mask] = {n + 1, 0}; // Inicijalizacija lošim rješenjem

    for (int i = 0; i < n; ++i) {
        if ((mask >> i) & 1) { // Ako je osoba i u maski
            // Stanje prije nego smo dodali osobu i
            auto [rides, weight] = dp[mask ^ (1 << i)];

            if (weight + w[i] <= x) {
                weight += w[i];    // Stane u trenutnu vožnju
            } else {
                rides++;           // Mora u novu vožnju
                weight = w[i];
            }
            dp[mask] = min(dp[mask], {rides, weight});
        }
    }
}
cout << dp[(1 << n) - 1].first << "\n";
```

---

<!-- _class: title -->
# Projects (CSES)

## DP + binarno pretraživanje

---

# Analiza: Projects (1/2)

**Problem:**
Projekti s intervalima $[a, b]$ i nagradom $p$.
Treba odabrati skup projekata koji se ne preklapaju tako da je ukupna nagrada maksimalna.

**Intuicija:**
Ako sortiramo projekte po **vremenu završetka**, možemo koristiti DP.
Za $i$-ti projekt imamo odluku:

1. **Ne uzmemo ga:** rješenje je isto kao za $i-1$ projekata.
2. **Uzmemo ga:** dobivamo nagradu $p_i$, ali ne smijemo uzeti nijedan projekt koji se preklapa s njim. Vraćamo se na projekt $j$ koji završava prije nego što $i$ počinje.

---

# Analiza: Projects (2/2)

**Stanje:** `dp[i]` = max. nagrada koristeći podskup prvih $i$ (sortiranih) projekata.

**Prijelaz:**
$$ dp[i] = \max(dp[i-1], \quad \text{reward}_i + dp[j]) $$
gdje je $j$ najveći indeks takav da je $\text{end}_j < \text{start}_i$.

**Kako naći $j$?**
Budući da su projekti sortirani po kraju, koristimo **binarno pretraživanje** (`lower_bound`) nad vremenima završetka.

---

# Implementacija: Projects

```cpp
struct Project { int start, end, reward; };
// projects su sortirani po end; ends[i] = projects[i].end

vector<long long> dp(n);
dp[0] = projects[0].reward;

for (int i = 1; i < n; ++i) {
    long long take = projects[i].reward;

    // Zadnji projekt koji završava strogo prije početka projekta i
    int j = lower_bound(ends.begin(), ends.end(), projects[i].start)
            - ends.begin() - 1;

    if (j >= 0) take += dp[j];

    dp[i] = max(dp[i-1], take);
}
cout << dp[n-1] << "\n";
```

**Složenost:** $O(N \log N)$ zbog sortiranja i binarnog pretraživanja.

---

<!-- _class: title -->
# Tree Diameter (CSES)

## DP na stablu

---

# Analiza: Tree Diameter (1/2)

**Problem:**
Treba naći duljinu najduljeg puta u stablu (u bridovima). Postoji i rješenje s dva DFS-a, a ovdje gledamo DP pristup.

**Zašto DP?**
DP pristup računa promjer u jednom prolazu (post-order DFS) i lakše se generalizira na probleme gdje bridovi imaju težine ili dodatna ograničenja.

**Ideja:**
Za svaki čvor $u$ najdulji put koji prolazi kroz njega i ostaje u njegovom podstablu sastoji se od "kraka" prema jednom djetetu i "kraka" prema drugom djetetu.

---

# Analiza: Tree Diameter (2/2)

**DP stanje:**
`down(u)` = duljina najduljeg puta od $u$ prema dolje (u bridovima), pri čemu je `down(list) = 0`.
$$ down(u) = \max_{v \in children(u)} (1 + down(v)) $$

**Najdulji put kroz $u$:**
Zbroj dva najveća "kraka" $1 + down(v)$ po djeci $v$ (krak koji ne postoji računamo kao 0).

Konačno rješenje je maksimum toga po svim čvorovima $u$.

---

# Implementacija: Tree Diameter

```cpp
int diameter = 0;

// Vraća krak prema roditelju: 1 + down(u)
int dfs(int u, int p) {
    int max1 = 0, max2 = 0; // Dva najveća kraka prema djeci

    for (int v : adj[u]) {
        if (v == p) continue;
        int arm = dfs(v, u);

        if (arm > max1) {
            max2 = max1;
            max1 = arm;
        } else if (arm > max2) {
            max2 = arm;
        }
    }

    // Ažuriramo globalni promjer (put kroz u)
    diameter = max(diameter, max1 + max2);

    return 1 + max1;
}
```

---

<!-- _class: title -->
# Tree Distances I (CSES)

## Rerooting tehnika (Up-Down DP)

---

# Analiza: Tree Distances I (1/2)

**Problem:**
Za **svaki** čvor $u$ treba naći najveću udaljenost do bilo kojeg drugog čvora u stablu.

**Naivni pristup:**
BFS iz svakog čvora: $O(N^2)$. Presporo za $N=2 \cdot 10^5$.

**Intuicija:**
Najudaljeniji čvor od $u$ može biti:

1. U podstablu od $u$ (prema dolje).
2. Izvan podstabla od $u$ (prema gore, kroz roditelja).

---

# Analiza: Tree Distances I (2/2)

1. **DFS 1 (odozdo prema gore):** `in[u]` = najveća udaljenost od $u$ do čvora u njegovom podstablu (isto kao `down(u)` kod Tree Diameter).
2. **DFS 2 (odozgo prema dolje):** `out[u]` = najveća udaljenost od $u$ do čvora **izvan** njegovog podstabla, uz `out[korijen] = 0`.

Za dijete $u$ roditelja $p$:
$$ out[u] = 1 + \max\Big(out[p], \ \max_{s \ne u} (1 + in[s])\Big) $$
gdje $s$ ide po ostaloj djeci od $p$ (ako ih nema, uzimamo 0).

Da bi to bilo $O(1)$ po čvoru, za svaki $p$ pamtimo **dva najveća** kraka $1 + in[v]$: ako je $u$ dao najveći, koristimo drugi.
Odgovor za čvor $u$ je $\max(in[u], out[u])$.

---

<!-- _class: lead -->

# Pitanja?

Sretno s rješavanjem!