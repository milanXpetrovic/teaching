---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Napredno dinamičko programiranje"
footer: "Programiranje za rješavanje složenih problema | Vježbe 2025/26"
---

<!-- _class: title -->

# Napredno dinamičko programiranje

## Knapsack, Bitmask DP i DP na stablima

---

## Sadržaj

1. **Uvod**
   - Nadogradnja osnovnih koncepta
2. **Problem Ruksaka (Knapsack)**
   - 0-1 Knapsack i optimizacija prostora
3. **Bitmask DP**
   - Traveling Salesperson Problem (TSP)
4. **DP na Stablima**
   - Maximum Weight Independent Set
5. **Zadaci za vježbu**

---

## Uvod: Korak dalje od tablice

Prošli put: Jednostavni 1D i 2D problemi (nizovi, matrice).
Danas: **Složenija stanja i strukture.**

### Ključni koraci ostaju isti

1. **Definiraj stanje:** Koji minimalni parametri opisuju podproblem?
   - *Npr. "Koji podskup gradova smo posjetili?"*
2. **Pronađi prijelaz:** Veza između većeg i manjih problema.
3. **Redoslijed rješavanja:** Topološki redoslijed (od manjeg ka većem, ili od listova ka korijenu).

### Tri glavne teme danas

1. **Knapsack:** Optimizacija resursa.
2. **Bitmask DP:** Problemi na podskupovima ($N \le 20$).
3. **Tree DP:** Problemi na stablima (bez ciklusa).

---

## 1. Problem Ruksaka (0-1 Knapsack)

**Zadatak:** Imamo ruksak kapaciteta $W$ i $N$ predmeta. Svaki predmet ima težinu $w_i$ i vrijednost $v_i$.
Svaki predmet možemo uzeti **jednom** (0 ili 1) ili ne uzeti. Maksimiziraj ukupnu vrijednost.

**Pokušaj (pohlepno):** Uzimati predmete s najboljim omjerom $v_i/w_i$?
- **Ne radi!** (Primjer: $W=4$, predmeti: $\{(3, 4), (2, 3), (2, 3)\}$. Pohlepno uzme prvi (val=4), optimalno je uzeti zadnja dva (val=6)).

**DP Stanje:**
`dp[i][w]` = Maksimalna vrijednost koristeći prvih $i$ predmeta s kapacitetom $w$.

**Prijelaz:**
$$ dp[i][w] = \max(dp[i-1][w], \quad v_i + dp[i-1][w - w_i]) $$
*(Opcija 1: Ne uzmi predmet $i$ vs. Opcija 2: Uzmi predmet $i$)*

---

## Knapsack: Optimizacija prostora

Primijetimo: Da bismo izračunali redak $i$, trebamo samo redak $i-1$.
Možemo koristiti **samo jedan niz** `dp[w]`.

**Ključni detalj:** Iteriramo po težini $W$ **unatrag**.
Zašto? Da ne bismo iskoristili *isti predmet* više puta u istoj iteraciji.

```cpp
int main() {
    int n, W; cin >> n >> W;
    vector<int> weights(n), values(n);
    for(int i=0; i<n; ++i) cin >> weights[i] >> values[i];

    vector<int> dp(W + 1, 0);

    for (int i = 0; i < n; ++i) {
        // Idemo UNATRAG da simuliramo "uzmi najviše jednom"
        for (int w = W; w >= weights[i]; --w) {
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }
    cout << dp[W] << endl;
}
```

**Složenost:** $O(N \cdot W)$.

---

## 2. DP na podskupovima (Bitmask DP)

Koristi se kad je $N$ mali ($N \le 20$), a stanje ovisi o **skupu** posjećenih/iskorištenih elemenata.
Skup prikazujemo kao **bitmasku** (integer).
- Ako je $j$-ti bit 1 $\to$ element $j$ je u skupu.

### Primjer: Traveling Salesperson Problem (TSP)

**Zadatak:** Obiđi $N$ gradova točno jednom i vrati se na početak, uz minimalan put.
**Stanje:** `dp[mask][i]`
- `mask`: Skup posjećenih gradova.
- `i`: Trenutni grad (zadnji posjećen).

**Vrijednost:** Duljina najkraćeg puta koji prolazi kroz `mask` i završava u `i`.

---

## TSP: Implementacija

**Prijelaz:** Dolazimo u grad `i` iz nekog grada `j` koji je već u maski.
$$ dp[\text{mask}][i] = \min_{j \in \text{mask}, j \neq i} (dp[\text{mask} \setminus \{i\}][j] + \text{dist}[j][i]) $$

```cpp
// dp[mask][i] inicijaliziran na INF, osim dp[1][0] = 0 (početak u 0)
for (int mask = 1; mask < (1 << n); ++mask) {
    for (int i = 0; i < n; ++i) {
        if ((mask >> i) & 1) { // Ako je grad 'i' u trenutnom skupu
            int prev_mask = mask ^ (1 << i); // Stanje prije dolaska u 'i'
            if (prev_mask == 0) continue; // Bazni slučaj je već riješen
            
            for (int j = 0; j < n; ++j) {
                if ((prev_mask >> j) & 1) { // Pokušaj doći iz 'j' u 'i'
                    dp[mask][i] = min(dp[mask][i], dp[prev_mask][j] + dist[j][i]);
                }
            }
        }
    }
}
```

**Složenost:** $O(N^2 \cdot 2^N)$.

---

## 3. DP na Stablima (Tree DP)

Stabla nemaju cikluse $\to$ idealno za DP.
Redoslijed rješavanja: **Post-order DFS** (od listova prema korijenu).
Rješenje za čvor $u$ ovisi o rješenjima njegove djece $v$.

### Zadatak: Maximum Weight Independent Set

Nađi skup čvorova s najvećom težinom tako da **niti jedna dva čvora nisu susjedi**.

**Stanje za čvor $u$:**

1. `dp[u][0]`: Ne uzimamo $u$. Djeca mogu biti uzeta ili ne.
2. `dp[u][1]`: Uzimamo $u$. Djeca **ne smiju** biti uzeta.

**Prijelaz:**
$$ dp[u][0] = \sum_{v \in children(u)} \max(dp[v][0], dp[v][1]) $$
$$ dp[u][1] = w_u + \sum_{v \in children(u)} dp[v][0] $$

---

## Tree DP: Implementacija

```cpp
vector<long long> dp[MAXN][2]; // 0: skip, 1: take

void dfs(int u, int p) {
    dp[u][0] = 0;
    dp[u][1] = weights[u]; // Ako uzmemo u, imamo njegovu težinu

    for (int v : adj[u]) {
        if (v == p) continue; // Preskoči roditelja
        dfs(v, u); // Prvo riješi za djecu

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

## Zadaci za vježbu (CSES & Codeforces)

### CSES Problem Set

1. **Money Sums:** Knapsack varijacija (koje sume su moguće?).
2. **Rectangle Cutting:** 2D DP (rezanje pravokutnika).
3. **Elevator Rides:** Bitmask DP (pakiranje ljudi u liftove).
4. **Projects:** DP na intervalima + Binary Search.
5. **Tree Diameter:** Može se riješiti kao Tree DP (najduži put kroz $u$).
6. **Tree Distances I & II:** Napredniji Tree DP (Rerooting technique).

### Codeforces
*   Traži tagove `dp`, `bitmask`, `trees`.

---

<!-- _class: title -->
# Money Sums (CSES)

## Koje sume možemo formirati?

---

# Analiza: Money Sums (1/2)

**Problem:**
Imamo $N$ novčića s vrijednostima $x_1, \dots, x_N$.
Koje sve **različite sume** možemo formirati koristeći ove novčiće?
Npr. $\{4, 2, 5\}$ $\to$ Sume: 2, 4, 5, 6 (2+4), 7 (2+5), 9 (4+5), 11 (2+4+5).

**Intuicija:**
Ovo je varijacija **Knapsack problema** (Subset Sum).
Umjesto da tražimo maksimalnu vrijednost, zanima nas **dostupnost** (boolean).
Maksimalna moguća suma je $N \times 1000 = 100 \times 1000 = 10^5$. To je dovoljno malo za DP tablicu.

---

# Analiza: Money Sums (2/2)

**DP Stanje:**
`dp[s]` = Je li moguće formirati sumu $s$? (True/False).

**Prijelaz:**
Kada razmatramo novčić vrijednosti $v$:
Ako smo mogli formirati sumu $S$ bez ovog novčića, onda s ovim novčićem možemo formirati sumu $S + v$.

$$ dp[s] = dp[s] \lor dp[s - v] $$

**Redoslijed:**
Kao kod 0-1 Knapsacka, moramo iterirati po sumama **unatrag** ili koristiti 2D polje (ali 1D je bolje).

---

# Implementacija: Money Sums

```cpp
int n; cin >> n;
vector<int> x(n);
for(int &v : x) cin >> v;

int max_sum = n * 1000;
vector<bool> dp(max_sum + 1, false);
dp[0] = true; // Sumu 0 možemo uvijek formirati (prazan skup)

for (int coin : x) {
    // Iteriramo unatrag da ne koristimo isti novčić više puta za istu sumu
    for (int s = max_sum; s >= coin; --s) {
        if (dp[s - coin]) {
            dp[s] = true;
        }
    }
}

// Ispis: Prebroji i ispiši sve indekse s gdje je dp[s] == true
vector<int> result;
for (int s = 1; s <= max_sum; ++s) if (dp[s]) result.push_back(s);
// ... ispis result ...
```

---

<!-- _class: title -->
# Rectangle Cutting (CSES)

## 2D Dinamičko programiranje

---

# Analiza: Rectangle Cutting (1/2)

**Problem:**
Pravokutnik dimenzija $a \times b$. Želimo ga izrezati na kvadrate.
Koji je **minimalan broj rezova**?

**Intuicija:**
Svaki rez dijeli pravokutnik na dva manja pravokutnika.
Rez može biti:
1. **Vertikalan:** Dijeli $w \times h$ na $i \times h$ i $(w-i) \times h$.
2. **Horizontalan:** Dijeli $w \times h$ na $w \times j$ i $w \times (h-j)$.

Želimo isprobati **sve moguće rezove** i uzeti onaj koji daje minimalan zbroj rezova za dva dobivena dijela.

---

# Analiza: Rectangle Cutting (2/2)

**Stanje:** `dp[w][h]` = min rezova za pravokutnik $w \times h$.

**Baza:**
Ako je $w == h$, `dp[w][h] = 0` (već je kvadrat, ne treba rezati).

**Prijelaz:**
$$ dp[w][h] = 1 + \min \left( 
\min_{i=1}^{w-1}(dp[i][h] + dp[w-i][h]), \quad
\min_{j=1}^{h-1}(dp[w][j] + dp[w][h-j]) 
\right) $$

*(1 + ... jer trenutni rez brojimo kao 1)*

---

# Implementacija: Rectangle Cutting

```cpp
// dp tablica inicijalizirana na beskonačno
for (int w = 1; w <= a; ++w) {
    for (int h = 1; h <= b; ++h) {
        if (w == h) {
            dp[w][h] = 0;
        } else {
            // Probaj sve vertikalne rezove
            for (int i = 1; i < w; ++i) 
                dp[w][h] = min(dp[w][h], 1 + dp[i][h] + dp[w-i][h]);
            
            // Probaj sve horizontalne rezove
            for (int i = 1; i < h; ++i) 
                dp[w][h] = min(dp[w][h], 1 + dp[w][i] + dp[w][h-i]);
        }
    }
}
cout << dp[a][b] << endl;
```
**Složenost:** $O(A \cdot B \cdot (A+B))$. Za $A, B \le 500$, ovo je oko $500^3 \approx 1.25 \cdot 10^8$, što prolazi.

---

<!-- _class: title -->
# Elevator Rides (CSES)

## Bitmask DP u praksi

---

# Analiza: Elevator Rides (1/2)

**Problem:**
$N$ ljudi s težinama $w_i$. Lift ima nosivost $X$.
Minimalan broj vožnji da se prevezu svi ljudi? ($N \le 20$).

**Zašto je ovo teško?**
Ovo je **Bin Packing Problem**, koji je NP-težak. Pohlepni pristup (trpaj dok stane) ne radi optimalno.
Srećom, $N$ je mali ($N \le 20$), što sugerira eksponencijalnu složenost $O(2^N \cdot N)$.

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
- Ako stane u zadnju vožnju $\to$ dodaj je tamo.
- Ako ne stane $\to$ nova vožnja.

---

# Implementacija: Elevator Rides

```cpp
pair<int, int> dp[1 << n]; // {rides, last_weight}
dp[0] = {1, 0}; // 1 vožnja (prazna) za početak (ili 0 vožnji, ovisi o impl.)

for (int mask = 1; mask < (1 << n); ++mask) {
    dp[mask] = {n + 1, 0}; // Init s lošim rješenjem
    
    for (int i = 0; i < n; ++i) {
        if ((mask >> i) & 1) { // Ako je osoba i u maski
            // Stanje prije nego smo dodali osobu i
            auto [rides, weight] = dp[mask ^ (1 << i)];
            
            if (weight + w[i] <= x) {
                // Stane u trenutnu vožnju
                weight += w[i];
            } else {
                // Mora u novu vožnju
                rides++;
                weight = w[i];
            }
            dp[mask] = min(dp[mask], {rides, weight});
        }
    }
}
cout << dp[(1 << n) - 1].first << endl;
```

---

<!-- _class: title -->
# Projects (CSES)

## DP s kompresijom koordinata

---

# Analiza: Projects (1/2)

**Problem:**
Projekti s intervalima $[a, b]$ i nagradom $p$.
Odaberi skup projekata koji se ne preklapaju tako da je ukupna nagrada maksimalna.

**Intuicija:**
Ako sortiramo projekte po **vremenu završetka**, možemo koristiti DP.
Za $i$-ti projekt imamo odluku:
1. **Ne uzmi ga:** Rješenje je isto kao za $i-1$ projekata.
2. **Uzmi ga:** Dobivamo nagradu $p_i$, ali ne smijemo uzeti nijedan projekt koji se preklapa s njim. Moramo se vratiti na projekt $j$ koji završava prije nego $i$ počinje.

---

# Analiza: Projects (2/2)

**Stanje:** `dp[i]` = max nagrada koristeći podskup prvih $i$ (sortiranih) projekata.

**Prijelaz:**
$$ dp[i] = \max(dp[i-1], \quad \text{reward}_i + dp[j]) $$
Gdje je $j$ indeks najvećeg projekta takvog da je $\text{end}_j < \text{start}_i$.

**Kako naći $j$?**
Budući da su projekti sortirani po kraju, možemo koristiti **binarno pretraživanje** (`lower_bound` ili `upper_bound`) nad vremenima završetka.

---

# Implementacija: Projects

```cpp
struct Project { int start, end, reward; };
// Sortiraj po end vremenu

vector<long long> dp(n);
dp[0] = projects[0].reward;

for (int i = 1; i < n; ++i) {
    long long take = projects[i].reward;
    
    // Tražimo zadnji projekt koji završava prije nego ovaj počinje
    // Binary search nad end_times
    int j = binary_search_last_non_overlapping(i); 
    
    if (j != -1) take += dp[j];
    
    dp[i] = max(dp[i-1], take);
}
cout << dp[n-1] << endl;
```
**Složenost:** $O(N \log N)$ zbog sortiranja i binarnog pretraživanja.

---

<!-- _class: title -->
# Tree Diameter (CSES)

## DP na stablu

---

# Analiza: Tree Diameter (1/2)

**Problem:**
Najduži put u stablu. (Već smo spomenuli 2x DFS, ali ovo je DP pristup).

**Zašto DP?**
DP pristup nam omogućuje da izračunamo promjer u jednom prolazu (post-order DFS) i lakše se generalizira na probleme gdje bridovi imaju težine ili dodatna ograničenja.

**Ideja:**
Za svaki čvor $u$, najduži put koji prolazi kroz njega i ostaje u njegovom podstablu izgleda kao "krak" prema jednom djetetu + "krak" prema drugom djetetu.

---

# Analiza: Tree Diameter (2/2)

**DP Stanje:**
Za svaki čvor $u$ računamo:
1. `toLeaf(u)`: Najduži put od $u$ prema dolje do najdaljeg lista u njegovom podstablu.
   $$ toLeaf(u) = 1 + \max_{v \in children(u)} (toLeaf(v)) $$
2. `maxLength(u)`: Najduži put koji prolazi kroz $u$ (spaja dva najdublja podstabla).
   $$ maxLength(u) = \text{max\_1st}(toLeaf(v)) + \text{max\_2nd}(toLeaf(v)) + 2 $$

Konačno rješenje je $\max_u (\text{maxLength}(u))$.

---

# Implementacija: Tree Diameter

```cpp
int diameter = 0;

int dfs(int u, int p) {
    int max1 = 0, max2 = 0; // Dvije najveće dubine djece
    
    for (int v : adj[u]) {
        if (v == p) continue;
        int depth = dfs(v, u);
        
        if (depth > max1) {
            max2 = max1;
            max1 = depth;
        } else if (depth > max2) {
            max2 = depth;
        }
    }
    
    // Ažuriraj globalni promjer (put kroz u)
    diameter = max(diameter, max1 + max2);
    
    // Vrati najduži put prema dolje
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
Za **svaki** čvor $u$, nađi maksimalnu udaljenost do bilo kojeg drugog čvora u stablu.

**Naivni pristup:**
BFS iz svakog čvora: $O(N^2)$. Presporo za $N=2 \cdot 10^5$.

**Intuicija:**
Najudaljeniji čvor od $u$ može biti:
1. U podstablu od $u$ (prema dolje).
2. Izvan podstabla od $u$ (prema gore, kroz roditelja).

---

# Analiza: Tree Distances I (2/2)

**Rješenje (2 prolaza):**

1. **DFS 1 (Bottom-Up):** Računa `in[u]` = max udaljenost u podstablu (isto kao `toLeaf` u prošlom zadatku).
2. **DFS 2 (Top-Down):** Računa `out[u]` = max udaljenost izvan podstabla.
   
   Kako izračunati `out[u]`?
   Roditelj $p$ ima put prema gore (`out[p]`) i puteve prema drugoj djeci.
   `out[u] = 1 + max(out[p], max_path_in_siblings_of_u)`.

   Da bismo efikasno našli `max_path_in_siblings`, pamtimo **dvije najveće** `in` vrijednosti za svakog čvora.

---

<!-- _class: lead -->

# Pitanja?

Sretno s rješavanjem!
