---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Traženje najkraćeg puta u grafu"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!-- _paginate: false -->
<!-- _class: title -->

# Algoritmi za najkraći put

## Dijkstra, Bellman-Ford, Floyd-Warshall

---

# Sadržaj

1. **Uvod i motivacija**
   * Problem najkraćeg puta vs. BFS
   * Pregled algoritama
2. **Dijkstrin algoritam**
   * Princip rada (pohlepni pristup)
   * Implementacija (priority queue)
3. **Bellman-Ford algoritam**
   * Rad s negativnim težinama
   * Detekcija negativnih ciklusa
4. **Floyd-Warshall algoritam** (kroz zadatak Shortest Routes II)
5. **Zadaci za vježbu**

---

# Uvod: problem najkraćeg puta

Zadan je **težinski usmjeren graf** $G = (V, E)$ gdje svaka veza $(u, v)$ ima težinu $w(u, v)$.
Cilj: pronaći put minimalne ukupne težine od izvora $s$ do cilja $t$.

**Primjene:**

* **GPS navigacija:** najbrža ruta (vrijeme je težina).
* **Mreže:** routing protokoli (OSPF).
* **Ekonomija:** minimizacija troškova transakcija.

---

# Ključna razlika: BFS vs. težinski grafovi

<div class="twocols">

Zašto ne koristimo BFS?

1. **BFS (Breadth-First Search):**
   * Nalazi put s **najmanjim brojem bridova**.
   * Pretpostavlja da svaki brid ima težinu 1.

2. **Težinski algoritmi (Dijkstra/Bellman-Ford):**
   * Nalaze put s **najmanjom sumom težina**.
   * Put s više bridova može biti "jeftiniji" od puta s jednim bridom.

<p class="break"></p>

![w: 350](/img/prsp/shortest-paths/bfs_vs_dijkstra_counterexample.png)

</div>

---

# Pregled algoritama

Koji algoritam odabrati?

| Algoritam | Težine bridova | Složenost | Napomena |
| :--- | :--- | :--- | :--- |
| **Dijkstra** | **Samo nenegativne** ($w \ge 0$) | $O(M \log N)$ | Standardni izbor. Vrlo brz. |
| **Bellman-Ford** | Mogu biti **negativne** | $O(N \cdot M)$ | Sporiji. Detektira negativne cikluse. |
| **Floyd-Warshall** | Mogu biti **negativne** | $O(N^3)$ | Svi parovi čvorova. Samo za male grafove. |

---

<!-- _class: title -->

# Dijkstrin algoritam

## Najbrži algoritam za nenegativne težine

---

# Dijkstra: intuicija (1/2)

Dijkstra je **pohlepni algoritam**.
Princip rada sličan je širenju vala ili "kruga poznatog teritorija" iz izvora $S$.

**Postupak:**

1. Održavamo trenutne najkraće udaljenosti (`dist`) do svih čvorova (start = 0, ostali = $\infty$).
2. U svakom koraku biramo **neobrađeni** čvor $U$ s **najmanjom** trenutnom udaljenosti.
3. Fiksiramo udaljenost do $U$ (ona se više neće mijenjati).
4. **Relaksiramo** sve susjede čvora $U$:
   * Ako je `dist[U] + w(U, V) < dist[V]`, ažuriramo `dist[V]`.

---

# Dijkstra: intuicija (2/2)

![w:550px center](/img/prsp/shortest-paths/dijkstra-animation.gif)

Izvor: [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

---

# Dijkstra: implementacija (C++)

```cpp
const long long INF = 1e18;
vector<long long> dist(n + 1, INF);  // Ne "distance": sudara se sa std::distance
priority_queue<pair<long long, int>> q;
dist[start] = 0;
q.push({0, start});

while (!q.empty()) {
    long long d = -q.top().first; // Vraćamo pozitivnu vrijednost
    int u = q.top().second;
    q.pop();

    if (d > dist[u]) continue; // Već smo ranije našli bolji put

    for (auto [v, w] : adj[u]) {
        if (dist[u] + w < dist[v]) {
            dist[v] = dist[u] + w;
            q.push({-dist[v], v});
        }
    }
}
```

*Trik:* C++ `priority_queue` je max-heap, pa spremamo `{-udaljenost, čvor}`.

---

# Dijkstra: analiza složenosti

* Svaki čvor obrađujemo jednom (zbog provjere `d > dist[u]`), pa svaki brid relaksiramo jednom.
* Svaki čvor dodajemo u prioritetni red najviše onoliko puta koliko ima ulaznih bridova.
* Operacije s redom (`push`/`pop`) traju $O(\log N)$.

**Ukupna složenost:**
$$ O(M \log N) $$
(gdje je $N$ broj čvorova, a $M$ broj bridova).

---

<!-- _class: title -->

# Bellman-Ford algoritam

## Rad s negativnim težinama i ciklusi

---

# Bellman-Ford: intuicija

Što ako imamo negativne težine? Pohlepni pristup (Dijkstra) ne radi jer "skupi" put kasnije može postati "jeftin" prolaskom kroz negativni brid.

**Ideja (dinamičko programiranje):**

* Najkraći put bez ciklusa može imati najviše $N-1$ bridova.
* U $i$-toj iteraciji nalazimo sve najkraće putove koji koriste najviše $i$ bridova.

**Algoritam:**
Ponavljamo $N-1$ puta: prolazimo kroz **SVE bridove** $(u, v)$ u grafu i pokušavamo ih relaksirati:
`dist[v] = min(dist[v], dist[u] + w)`

---

# Detekcija negativnih ciklusa

<div class="twocols">

**Negativni ciklus:** ciklus čija je suma težina $< 0$.
Ako postoji, možemo se vrtjeti u krug i smanjivati udaljenost do $-\infty$. Najkraći put nije definiran.

**Kako ga detektirati?**
Nakon $N-1$ iteracija svi bi putovi trebali biti konačni.
Pokrenemo **$N$-tu iteraciju**.

* Ako se ijedna udaljenost **smanji**, postoji negativni ciklus dostupan iz izvora.

<p class="break"></p>

![w: 350](/img/prsp/shortest-paths/negative_cycle_detection.png)

</div>

---

# Bellman-Ford: implementacija

Koristimo listu bridova (`struct Edge { int a, b, w; }`).

```cpp
vector<long long> dist(n + 1, INF);
dist[start] = 0;

// 1. Relaksacija N-1 puta
for (int i = 0; i < n - 1; ++i) {
    for (auto e : edges) {
        if (dist[e.a] != INF && dist[e.a] + e.w < dist[e.b]) {
            dist[e.b] = dist[e.a] + e.w;
        }
    }
}

// 2. Detekcija negativnog ciklusa
bool neg_cycle = false;
for (auto e : edges) {
    if (dist[e.a] != INF && dist[e.a] + e.w < dist[e.b]) {
        neg_cycle = true;
        break;
    }
}
```

**Složenost:** $O(N \cdot M)$

---

# Zadaci za vježbu (CSES)

1. **[Shortest Routes I](https://cses.fi/problemset/task/1671)**
   * Klasična Dijkstra. Pazite na `long long` za udaljenosti!
2. **[Shortest Routes II](https://cses.fi/problemset/task/1672)**
   * $N \le 500$, traže se svi parovi $\to$ Floyd-Warshall.
3. **[High Score](https://cses.fi/problemset/task/1673)**
   * Traži se **najduži** put.
   * Trik: sve težine pomnožimo s $-1$ i tražimo najkraći put Bellman-Fordom.
   * Pazite na pozitivne cikluse (koji nakon množenja s $-1$ postaju negativni).
4. **[Flight Discount](https://cses.fi/problemset/task/1195)**
   * Dijkstra na "state-space" grafu. Čvor nije samo `u`, već `(u, iskoristio_popust)`.

---

<!-- _class: title -->

# Zadaci za vježbu

## CSES Problem Set

---

# Shortest Routes I (CSES)

**Problem:**
Zadan je graf s $N$ gradova i $M$ letova (bridova). Svaki let ima određenu duljinu.
Treba pronaći najkraći put od grada 1 do svih ostalih gradova.

**Ograničenja:**

* $N \le 10^5$, $M \le 2 \cdot 10^5$.
* Težine bridova su $\ge 0$.
* Graf je usmjeren.

---

# Shortest Routes I: intuicija

Budući da su težine **nenegativne**, ovo je klasičan primjer za **Dijkstrin algoritam**.

**Ključne točke za implementaciju:**

1. **Veliki brojevi:** duljina puta može premašiti $2^{31}-1$. Obavezno koristite `long long` za udaljenosti.
2. **Prioritetni red:** C++ `priority_queue` po defaultu vadi najveći element.
   * Opcija A: `priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>>`.
   * Opcija B (trik): ubacujemo `{-dist, u}`. Najmanja udaljenost postaje najveći (najmanje negativan) broj, pa je na vrhu heapa (npr. $-1 > -100$). Pri vađenju uzimamo `d = -q.top().first`.

---

# Shortest Routes I: kod

```cpp
vector<long long> dist(n + 1, INF);
priority_queue<pair<long long, int>> q;  // { -udaljenost, čvor }
dist[1] = 0;
q.push({0, 1});

while (!q.empty()) {
    long long d = -q.top().first;
    int u = q.top().second;
    q.pop();

    if (d > dist[u]) continue; // Već smo našli bolji put

    for (auto [v, w] : adj[u]) {
        if (dist[u] + w < dist[v]) {
            dist[v] = dist[u] + w;
            q.push({-dist[v], v});
        }
    }
}

for (int i = 1; i <= n; i++) cout << dist[i] << " ";
cout << "\n";
```

---

# Sažetak: Shortest Routes I

1. **Tipovi podataka su bitni:** u grafovima s težinama suma vrlo brzo prijeđe $2 \cdot 10^9$. Za udaljenosti uvijek koristite `long long`.
2. **Priority queue trik:** ubacivanje negativnih brojeva `{-dist, u}` standardni je trik u C++ natjecateljskom programiranju jer je `priority_queue` *max-heap*, a nama treba najmanja udaljenost.
   * Alternativa je `greater<...>`, ali trik je brži za napisati.

---

# Shortest Routes II (CSES)

**Problem:**
Zadan je graf s gradovima i (dvosmjernim) cestama. Treba odgovoriti na $Q$ upita.
Svaki upit traži najkraću udaljenost između dva grada $(a, b)$, ili $-1$ ako put ne postoji.

**Ograničenja:**

* $N \le 500$, $M \le N^2$.
* $Q \le 10^5$ (puno upita!).

---

# Shortest Routes II: intuicija (1/2)

1. **Zašto ne Dijkstra?**
   Pokretanje Dijkstre za svaki upit trajalo bi $Q \cdot O(M \log N)$.
   $10^5 \cdot 500^2 \dots$ Presporo!

2. **Floyd-Warshall:**
   Budući da je $N$ malen ($500$), udaljenosti između **svih parova** čvorova možemo izračunati unaprijed u $O(N^3)$.
   $500^3 = 1,25 \cdot 10^8$, što prolazi unutar vremenskog limita.
   Nakon toga svaki upit rješavamo u $O(1)$ čitanjem iz matrice.

**Pazite na:**

* Inicijalizaciju matrice (INF, dijagonala 0).
* Višestruke bridove između istih čvorova (uzimamo minimum).

---

# Shortest Routes II: intuicija (2/2)

![center](/img/prsp/shortest-paths/floyd-warshall-matrix.png)

---

# Shortest Routes II: inicijalizacija

```cpp
// 1. Inicijalizacija matrice
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= n; j++) {
        if (i == j) d[i][j] = 0;
        else d[i][j] = INF;
    }
}

// 2. Učitavanje (pazite na višestruke bridove!)
for (int i = 0; i < m; i++) {
    int u, v; long long w; cin >> u >> v >> w;
    d[u][v] = min(d[u][v], w);
    d[v][u] = min(d[v][u], w); // Ceste su dvosmjerne
}
```

---

# Shortest Routes II: kod (Floyd-Warshall)

```cpp
// 3. Algoritam (k je VANJSKA petlja!)
for (int k = 1; k <= n; k++) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            if (d[i][k] < INF && d[k][j] < INF) // Pazimo na overflow
                d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
        }
    }
}

// 4. Upiti
while (q--) {
    int a, b; cin >> a >> b;
    cout << (d[a][b] == INF ? -1 : d[a][b]) << "\n";
}
```

---

# Sažetak: Shortest Routes II

**Kako prepoznati Floyd-Warshall?**

Ključ nije u težini zadatka, već u **ograničenjima (constraints)**.

* Ako vidite **$N \le 500$**, to je jak signal za algoritam složenosti **$O(N^3)$**.
* Ako se traže udaljenosti između **svih parova** (All-Pairs Shortest Path).
* Ako ima puno upita ($Q$) na koje treba odgovoriti u $O(1)$.

> **Pazite:** ako pri inicijalizaciji matrice postoje višestruki bridovi između dva grada, uvijek zadržite onaj s **minimalnom** težinom!

---

# 3. High Score (CSES)

**Problem:**
Želimo putovati od sobe 1 do sobe $N$. Svaki tunel povećava naš rezultat za $x$.
Želimo postići **maksimalan** mogući rezultat.
Kroz sobe možemo prolaziti više puta. Ispisujemo $-1$ ako možemo postići proizvoljno velik rezultat (pozitivni ciklus).

**Analiza:**

* Tražimo **najduži put**.
* Standardni algoritmi traže najkraći put.
* **Trik:** sve težine pomnožimo s $-1$. Sada tražimo **najkraći put**.
* "Beskonačno velik rezultat" u originalu $\Leftrightarrow$ "beskonačno mali put" (negativni ciklus) u novom grafu.

---

# High Score: strategija

Koristimo **Bellman-Ford** jer tražimo najkraći put u grafu s negativnim težinama.

**Problem ciklusa:**
Samo postojanje negativnog ciklusa nije dovoljno da ispišemo $-1$.
Taj ciklus mora:

1. Biti dohvatljiv iz početnog čvora (1).
2. Moći doseći ciljni čvor ($N$).

**Rješenje:**

1. Pokrenemo Bellman-Ford $N-1$ puta.
2. Pokrenemo još $N-1$ iteracija. Ako se u nekom koraku udaljenost do čvora $v$ smanji, postavimo `dist[v] = -INF`.
3. Taj `-INF` "proširi" se na sve čvorove do kojih ciklus može doći.
4. Na kraju, ako je `dist[N] == -INF`, rješenje je $-1$.

---

# High Score: kod

```cpp
// Pri učitavanju spremamo bridove kao (u, v, -x)
vector<tuple<int, int, long long>> edges;

vector<long long> dist(n + 1, INF);
dist[1] = 0;

// Prvih N-1 iteracija (standardni Bellman-Ford)
for (int i = 1; i < n; ++i)
    for (auto [u, v, w] : edges)
        if (dist[u] != INF && dist[u] + w < dist[v])
            dist[v] = dist[u] + w;

// Dodatne iteracije: sve što se još može smanjiti dio je ciklusa -> -INF
for (int i = 1; i < n; ++i) {
    for (auto [u, v, w] : edges) {
        if (dist[u] == INF) continue;
        if (dist[u] == -INF) dist[v] = -INF;           // Propagacija
        else if (dist[u] + w < dist[v]) dist[v] = -INF; // Detektiran ciklus
    }
}

if (dist[n] == -INF) cout << -1 << "\n";
else cout << -dist[n] << "\n"; // Vraćamo u pozitivno
```

---

# Sažetak: High Score

**Transformacija problema**

Problemi "najduljeg puta" ili "maksimalnog profita" često se rješavaju pretvaranjem u **najkraći put s negativnim težinama** ($w' = -w$).

**Zamka "nedostižnog ciklusa"**

Nije svaki negativni ciklus bitan!

* Ako postoji negativni ciklus, ali do njega **ne možemo doći** iz starta $\to$ ne utječe na rješenje.
* Ako postoji negativni ciklus, ali iz njega **ne možemo doći** do cilja $\to$ ne utječe na rješenje.
* Zato u kodu provjeravamo dostižnost (propagaciju `-INF`).

---

# 4. Flight Discount (CSES)

**Problem:**
Put od grada 1 do $N$. Imamo kupon za **50% popusta** (zaokruženo nadolje) na točno jedan let.
Treba naći minimalnu cijenu.

**Intuicija: slojeviti graf (layered graph)**
Možemo zamisliti da se nalazimo u jednom od dva stanja:

1. `stanje 0`: još nismo iskoristili kupon.
2. `stanje 1`: iskoristili smo kupon.

**Prijelazi:**

* Iz `(u, 0)` u `(v, 0)`: cijena $w$ (ne koristimo kupon).
* Iz `(u, 0)` u `(v, 1)`: cijena $\lfloor w/2 \rfloor$ (koristimo kupon sada).
* Iz `(u, 1)` u `(v, 1)`: cijena $w$ (kupon je već iskorišten).

---

# Flight Discount: implementacija

Ovo je **Dijkstra** na grafu s $2N$ čvorova. Udaljenosti pamtimo kao `dist[čvor][stanje]`.

```cpp
// dist[u][0] i dist[u][1] inicijalizirani na INF
priority_queue<tuple<long long, int, int>> q; // {-cijena, u, stanje}
dist[1][0] = 0;
q.push({0, 1, 0});

while (!q.empty()) {
    auto [d, u, state] = q.top(); q.pop();
    d = -d;
    if (d > dist[u][state]) continue;

    for (auto [v, w] : adj[u]) {
        // Opcija 1: ne koristimo kupon (stanje ostaje isto)
        if (dist[u][state] + w < dist[v][state]) {
            dist[v][state] = dist[u][state] + w;
            q.push({-dist[v][state], v, state});
        }
        // Opcija 2: koristimo kupon (samo iz stanja 0)
        if (state == 0 && dist[u][0] + w / 2 < dist[v][1]) {
            dist[v][1] = dist[u][0] + w / 2;
            q.push({-dist[v][1], v, 1});
        }
    }
}
// Kupon nikad ne povećava cijenu, pa je dist[n][1] <= dist[n][0]
cout << dist[n][1] << "\n";
```

---

# Osvrt: Flight Discount

**Tehnika: proširenje prostora stanja (State-Space Expansion)**

Ovo je jedna od najvažnijih tehnika za teže grafovske zadatke.

Kada se pravila kretanja promijene (npr. "imamo 1 kupon", "možemo preskočiti 2 zida", "auto ima goriva za K km"), čvor više nije samo `u`.
**Čvor postaje `(u, stanje)`**.

* Broj čvorova raste s $N$ na $N \cdot S$, gdje je $S$ broj stanja.
* Ako je broj stanja malen (ovdje 2), Dijkstra radi savršeno.

---

<!-- _class: title -->

# Zaključak

## Što smo danas naučili?

---

# Algoritam: stablo odlučivanja

Kada dobijete zadatak s grafom, postavite si ova pitanja redom:

1. **Jesu li težine bridova 1 (ili ne postoje)?**
   $\rightarrow$ Koristite **BFS** ($O(N+M)$).
2. **Jesu li težine bridova $\ge 0$?**
   $\rightarrow$ Koristite **Dijkstru** ($O(M \log N)$).
3. **Ima li negativnih težina (a $N$ je velik)?**
   $\rightarrow$ Koristite **Bellman-Ford** ($O(N \cdot M)$).
4. **Je li $N$ malen ($N \le 500$) i trebaju li nam svi parovi?**
   $\rightarrow$ Koristite **Floyd-Warshall** ($O(N^3)$).
5. **Postoje li posebna pravila (kuponi, gorivo, stanja)?**
   $\rightarrow$ Modificirajte Dijkstru na **slojevitom grafu**.