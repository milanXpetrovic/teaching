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

### Ključni koraci ostaju isti:
1. **Definiraj stanje:** Koji minimalni parametri opisuju podproblem?
   * *Npr. "Koji podskup gradova smo posjetili?"*
2. **Pronađi prijelaz:** Veza između većeg i manjih problema.
3. **Redoslijed rješavanja:** Topološki redoslijed (od manjeg ka većem, ili od listova ka korijenu).

### Tri glavne teme danas:
1. **Knapsack:** Optimizacija resursa.
2. **Bitmask DP:** Problemi na podskupovima ($N \le 20$).
3. **Tree DP:** Problemi na stablima (bez ciklusa).

---

## 1. Problem Ruksaka (0-1 Knapsack)

**Zadatak:** Imamo ruksak kapaciteta $W$ i $N$ predmeta. Svaki predmet ima težinu $w_i$ i vrijednost $v_i$.
Svaki predmet možemo uzeti **jednom** (0 ili 1) ili ne uzeti. Maksimiziraj ukupnu vrijednost.

**Pokušaj (pohlepno):** Uzimati predmete s najboljim omjerom $v_i/w_i$?
* **Ne radi!** (Primjer: $W=4$, predmeti: $\{(3, 4), (2, 3), (2, 3)\}$. Pohlepno uzme prvi (val=4), optimalno je uzeti zadnja dva (val=6)).

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
* Ako je $j$-ti bit 1 $\to$ element $j$ je u skupu.

### Primjer: Traveling Salesperson Problem (TSP)
**Zadatak:** Obiđi $N$ gradova točno jednom i vrati se na početak, uz minimalan put.
**Stanje:** `dp[mask][i]`
* `mask`: Skup posjećenih gradova.
* `i`: Trenutni grad (zadnji posjećen).

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
1.  **Money Sums:** Knapsack varijacija (koje sume su moguće?).
2.  **Rectangle Cutting:** 2D DP (rezanje pravokutnika).
3.  **Elevator Rides:** Bitmask DP (pakiranje ljudi u liftove).
4.  **Projects:** DP na intervalima + Binary Search.
5.  **Tree Diameter:** Može se riješiti kao Tree DP (najduži put kroz $u$).
6.  **Tree Distances I & II:** Napredniji Tree DP (Rerooting technique).

### Codeforces
*   Traži tagove `dp`, `bitmask`, `trees`.

---

<!-- _class: lead -->

# Pitanja?

Sretno s rješavanjem!
```