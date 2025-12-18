
<!-- _class: title -->

# Flight Routes Check (CSES)

## Jaka povezanost u usmjerenim grafovima

---

# Analiza Zadatka: Flight Routes Check

## Opis problema: Flight Routes Check

Imamo $n$ gradova i $m$ **jednosmjernih** letova.
Moramo provjeriti možemo li od **bilo kojeg** grada doći do **bilo kojeg drugog** grada.

### Ključna razlika

U neusmjerenim grafovima (kao "Road Reparation"), dovoljno je pokrenuti DFS/BFS iz jednog čvora i vidjeti jesmo li posjetili sve.
U **usmjerenim** grafovima to nije dovoljno!

- Možda možemo doći iz $1 \to 2$, ali ne možemo iz $2 \to 1$.
- Ovo svojstvo zove se **Jaka Povezanost (Strong Connectivity)**.

---

# Strategija: Ideja "Huba"

Umjesto da provjeravamo sve parove (presporo $O(N^2)$), odaberimo proizvoljan čvor, npr. **Grad 1**.

Graf je jako povezan ako i samo ako vrijede dva uvjeta:

1. **Iz Grada 1 možemo doći do svih ostalih gradova.**
2. **Iz svih ostalih gradova možemo doći do Grada 1.**

Ako vrijedi oboje, onda put $A \to B$ izgleda ovako: $A \to \dots \to 1 \to \dots \to B$.

---

# Algoritam: Dva prolaza (Forward & Backward) (1/2)

![w:600px center](../../../img/transposed-graph.jpg)
**Transponirani graf**
Izvor: [Transpose graph](https://en.wikipedia.org/wiki/Transpose_graph)

---

# Algoritam: Dva prolaza (Forward & Backward) (2/2)

Kako efikasno provjeriti uvjete?

1. **Forward Pass:** Pokreni DFS iz Grada 1 na **originalnom grafu**.
   - Ako neki čvor $X$ nije posjećen $\rightarrow$ Ne možemo doći $1 \to X$.
   - **Rješenje:** NO, $1 \space X$.

2. **Backward Pass:** Pokreni DFS iz Grada 1 na **obrnutom (transponiranom) grafu**.
   - Obrnuti graf ima sve bridove usmjerene suprotno ($A \to B$ postaje $B \to A$).
   - Ako u obrnutom grafu dođemo od $1$ do $Y$, to znači da u originalnom postoji put $Y \to 1$.
   - Ako neki čvor $Y$ nije posjećen $\rightarrow$ Ne možemo doći $Y \to 1$.
   - **Rješenje:** NO, $Y \space 1$.

---

# Implementacija: Priprema

Trebaju nam dvije liste susjedstva: jedna za pravi smjer, jedna za obrnuti.

```cpp
#include <iostream>
#include <vector>

using namespace std;

const int MAXN = 100005;
vector<int> adj[MAXN];      // Originalni graf
vector<int> adj_rev[MAXN];  // Obrnuti graf
bool visited[MAXN];
int n;

void dfs(int u, vector<int> graph[]) {
    visited[u] = true;
    for (int v : graph[u]) {
        if (!visited[v]) dfs(v, graph);
    }
}
```

---

# Implementacija: Glavna logika

```cpp
int main() {
    int m;
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v);      // Brid u pravom smjeru
        adj_rev[v].push_back(u);  // Brid u obrnutom smjeru
    }

    // 1. FORWARD PASS (Provjera 1 -> Svi)
    dfs(1, adj);
    for (int i = 1; i <= n; i++) {
        if (!visited[i]) {
            cout << "NO\n1 " << i << endl; // Nismo mogli doći do i
            return 0;
        }
    }
    // ... nastavlja se
```

---

# Implementacija: Drugi prolaz

```cpp
    // Resetiramo visited niz
    for (int i = 1; i <= n; i++) visited[i] = false;

    // 2. BACKWARD PASS (Provjera Svi -> 1)
    // DFS na obrnutom grafu iz 1 simulira traženje tko sve može doći do 1
    dfs(1, adj_rev);

    for (int i = 1; i <= n; i++) {
        if (!visited[i]) {
            cout << "NO\n" << i << " 1" << endl; // i ne može doći do 1
            return 0;
        }
    }

    cout << "YES" << endl;
    return 0;
}
```

---

# Sažetak rješenja: Flight Routes Check

1. **Jaka povezanost:** U usmjerenom grafu svatko mora moći do svakoga.
2. **Trik s obrnutim grafom:**
   - Provjeri $1 \to \text{svi}$ (običan DFS).
   - Provjeri $\text{svi} \to 1$ (DFS na grafu s obrnutim bridovima).
3. **Kontraprimjer:** Prvi neposjećeni čvor u bilo kojem prolazu daje nam odgovor "NO" i par gradova koji nisu povezani.
4. **Složenost:** $O(N + M)$ – dva linearna prolaza.





---

# Pregled algoritama

## 1. Floyd-Warshall

- **Što radi:** Najkraći putevi između *svih* parova čvorova.
- **Kada koristiti:** Mali grafovi ($N \le 400$), gusti grafovi, negativne težine (bez ciklusa).
- **Složenost:** $O(N^3)$.

---

# Ključne napomene

Prilikom rješavanja zadataka, obratite pažnju na sljedeće:

1. **Ograničenja ($N$):**
   - $N \le 400 \rightarrow$ Vjerojatno **Floyd-Warshall**.
   - $N \le 10^5 \rightarrow$ Vjerojatno **BFS/DFS, Dijkstra, Kruskal**.