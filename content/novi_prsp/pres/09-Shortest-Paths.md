---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Traženje najkraćeg puta u grafu"
footer: "Programiranje za rješavanje složenih problema | Vježbe 2025/26"
---
<!-- _class: title -->

# Algoritmi za najkraći put

## Dijkstra, Bellman-Ford, Floyd-Warshall

---

# Sadržaj

1. **Uvod i Motivacija**
   * Problem najkraćeg puta vs. BFS
   * Pregled algoritama
2. **Dijkstrin algoritam**
   * Princip rada (Pohlepni pristup)
   * Implementacija (Priority Queue)
3. **Bellman-Ford algoritam**
   * Rad s negativnim težinama
   * Detekcija negativnih ciklusa
4. **Zadaci za vježbu**

---

# Uvod: Problem najkraćeg puta

Zadan je **težinski usmjeren graf** $G = (V, E)$ gdje svaka veza $(u, v)$ ima težinu $w(u, v)$.
Cilj: Pronaći put minimalne ukupne težine od izvora $s$ do cilja $t$.

**Primjene:**

* **GPS navigacija:** Najbrža ruta (vrijeme je težina).
* **Mreže:** Routing protokoli (OSPF).
* **Ekonomija:** Minimizacija troškova transakcija.

---

# Ključna razlika: BFS vs. Težinski grafovi

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
| **Dijkstra** | **Samo ne-negativne** ($w \ge 0$) | $O(M \log N)$ | Standardni izbor. Vrlo brz. |
| **Bellman-Ford** | Mogu biti **negativne** | $O(N \cdot M)$ | Sporiji. Detektira negativne cikluse. |
| **Floyd-Warshall** | Mogu biti **negativne** | $O(N^3)$ | Svi parovi čvorova. Samo za male grafove. |

---

<!-- _class: title -->

# Dijkstrin algoritam

## Najbrži algoritam za ne-negativne težine

---

# Dijkstra: Intuicija (1/2)

Dijkstra je **pohlepni algoritam**.
Princip rada sličan je širenju vala ili "kruga poznatog teritorija" iz izvora $S$.

**Postupak:**

1. Održavamo trenutne najkraće udaljenosti (`dist`) do svih čvorova (start = 0, ostali = $\infty$).
2. U svakom koraku biramo **neobrađeni** čvor $U$ s **najmanjom** trenutnom udaljenosti.
3. Fiksiramo udaljenost do $U$ (ona se više neće mijenjati).
4. **Relaksiramo** sve susjede čvora $U$:
   * Ako je `dist[U] + w(U, V) < dist[V]`, ažuriramo `dist[V]`.

---

# Dijkstra: Intuicija (2/2)

![w:550px center](/img/prsp/shortest-paths/dijkstra-animation.gif)

Izvor: [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

---

# Dijkstra: Implementacija (C++)

```cpp
const long long INF = 1e18;
priority_queue<pair<long long, int>> q;
distance[start] = 0;
q.push({0, start});

while (!q.empty()) {
    long long d = -q.top().first; // Vrati pozitivnu vrijednost
    int u = q.top().second;
    q.pop();

    if (d > distance[u]) continue; // Već smo našli bolji put ranije

    for (auto edge : adj[u]) {
        int v = edge.first; int w = edge.second;
        if (distance[u] + w < distance[v]) {
            distance[v] = distance[u] + w;
            q.push({-distance[v], v});
        }
    }
}
```

Koristimo `priority_queue` za brzo dohvaćanje najmanje udaljenosti.
*Trik:* C++ `priority_queue` je Max-Heap, pa spremamo `{ -udaljenost, čvor }`.

---

# Dijkstra: Analiza složenosti

* Svaki brid procesiramo točno jednom (pri relaksaciji).
* Svaki čvor dodajemo u prioritetni red najviše onoliko puta koliko ima ulaznih bridova (u najgorem slučaju).
* Operacije s redom (`push`/`pop`) traju $O(\log N)$.

**Ukupna složenost:**
$$ O(M \log N) $$
(Gdje je $N$ broj čvorova, a $M$ broj bridova).

---

<!-- _class: title -->

# Bellman-Ford Algoritam

## Rad s negativnim težinama i ciklusi

---

# Bellman-Ford: Intuicija

Što ako imamo negativne težine? Pohlepni pristup (Dijkstra) ne radi jer "skupi" put kasnije može postati "jeftin" prolaskom kroz negativni brid.

**Ideja (Dinamičko programiranje):**

* Najkraći put bez ciklusa može imati najviše $N-1$ bridova.
* U $i$-toj iteraciji nalazimo sve najkraće puteve koji koriste najviše $i$ bridova.

**Algoritam:**
Ponavljaj $N-1$ puta:
   Prođi kroz **SVE bridove** $(u, v)$ u grafu i probaj ih relaksirati:
   `dist[v] = min(dist[v], dist[u] + w)`

---

# Detekcija Negativnih Ciklusa

<div class="twocols">

**Negativni ciklus:** Ciklus čija je suma težina $< 0$.
Ako postoji, možemo se vrtjeti u krug i smanjivati udaljenost do $-\infty$. Najkraći put nije definiran.

**Kako ga detektirati?**
Nakon $N-1$ iteracija, svi putevi bi trebali biti finalni.
Pokrenemo **$N$-tu iteraciju**.

* Ako se ijedna udaljenost **smanji**, znači da postoji negativni ciklus dostupan iz izvora.

<p class="break"></p>

![w: 350](/img/prsp/shortest-paths/negative_cycle_detection.png)

</div>

---

# Bellman-Ford: Implementacija

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
for (auto e : edges) {
    if (dist[e.a] != INF && dist[e.a] + e.w < dist[e.b]) {
        cout << "Postoji negativni ciklus!" << endl;
    }
}
```

**Složenost:** $O(N \cdot M)$

---

# Zadaci za vježbu (CSES)

1. **[Shortest Routes I (CSES)](https://cses.fi/problemset/task/1671)**
   * Klasična Dijkstra. Pazi na `long long` za udaljenosti!
2. **[Shortest Routes II (CSES)](https://cses.fi/problemset/task/1672)**
   * $N \le 500$, traže se svi parovi $\to$ Floyd-Warshall.
3. **[High Score (CSES)](https://cses.fi/problemset/task/1673)**
   * Traži se **najduži** put.
   * Trik: Pomnoži sve težine s $-1$ i traži najkraći put Bellman-Fordom.
   * Pazi na pozitivne cikluse (koji postaju negativni u inverziji).
4. **[Flight Discount (CSES)](https://cses.fi/problemset/task/1195)**
   * Dijkstra na "state-space" grafu. Čvor nije samo `u`, već `(u, iskoristio_popust)`.

---
<!-- _class: title -->

# Zadaci za vježbu

## CSES Problem Set

---

# Shortest Routes I (CSES)

## Problem

Zadan je graf s $N$ gradova i $M$ letova (bridova). Svaki let ima određenu duljinu.
Moramo pronaći najkraći put od grada 1 do svih ostalih gradova.

### Ograničenja

* $N \le 10^5$, $M \le 2 \cdot 10^5$.
* Težine bridova su $\ge 0$.
* Graf je usmjeren.

---

# Shortest Routes I: Intuicija

Budući da su težine **ne-negativne**, ovo je klasičan primjer za **Dijkstrin algoritam**.

## Ključne točke za implementaciju:

1. **Veliki brojevi:** Duljina puta može premašiti $2^{31}-1$. Obavezno koristi `long long` za udaljenosti.
2. **Prioritetni red:** C++ `priority_queue` po defaultu vadi najveći element.
   * Opcija A: Koristi `priority_queue<pair<ll, int>, vector<...>, greater<...>>`.
   * Opcija B (Trik): Ubacuj negativne udaljenosti `{-dist, u}` pa će najmanja udaljenost (koja je "najmanje negativna") biti na vrhu, ali zapravo želimo najveću negativnu vrijednost (-1 je veće od -100). *Najjednostavnije:* Ubacuj `{-dist, u}` i kod vađenja stavi `d = -q.top().first`.

---

# Shortest Routes I: Kod

```cpp
priority_queue<pair<long long, int>> q;
dist[1] = 0;
q.push({0, 1}); // { -udaljenost, čvor }

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
```

---

# Sažetak: Shortest Routes I

1. **Tipovi podataka su bitni:** U grafovima s težinama, suma vrlo brzo pređe $2 \cdot 10^9$. Uvijek koristi `long long` za udaljenosti.
2. **Priority Queue Trik:** Ubacivanje negativnih brojeva `{-dist, u}` je standardni trik u C++ natjecateljskom programiranju jer je `priority_queue` *max-heap*, a mi trebamo najmanju udaljenost.
   * Alternativa je `greater<...>`, ali ovo je brže za napisati.

---

# Shortest Routes II (CSES)

**Problem:**
Zadan je graf s gradovima i cestama. Moramo odgovoriti na $Q$ upita.
Svaki upit traži najkraću udaljenost između dva grada $(a, b)$.

**Ograničenja:**

* $N \le 500$, $M \le N^2$.
* $Q \le 10^5$ (Puno upita!).

---

# Shortest Routes II: Intuicija (1/2)

1. **Zašto ne Dijkstra?**
   Pokrenuti Dijkstru za svaki upit bi trajalo $Q \cdot O(M \log N)$.
   $10^5 \cdot 500^2 \dots$ Previše sporo!

2. **Floyd-Warshall:**
   Budući da je $N$ malen ($500$), možemo izračunati udaljenosti između **svih parova** čvorova unaprijed u $O(N^3)$.
   $500^3 = 1.25 \cdot 10^8$, što prolazi unutar vremenskog limita (C++ je brz).
   Nakon toga, svaki upit rješavamo u $O(1)$ čitanjem iz matrice.

**Pazi na:**

* Inicijalizaciju matrice (INF, dijagonala 0).
* Višestruke bridove između istih čvorova (uzmi minimum).

---

# Shortest Routes II: Intuicija (2/2)

![center](/img/prsp/shortest-paths/floyd-warshall-matrix.png)

---

# Shortest Routes II: Inicijalizacija

```cpp
// 1. Inicijalizacija matrice
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= n; j++) {
        if (i == j) d[i][j] = 0;
        else d[i][j] = INF;
    }
}

// 2. Učitavanje (pazi na višestruke bridove!)
for (int i = 0; i < m; i++) {
    int u, v; long long w; cin >> u >> v >> w;
    d[u][v] = min(d[u][v], w);
    d[v][u] = min(d[v][u], w); // Ako je neusmjeren
}
```
---

# Shortest Routes II: Kod (Floyd-Warshall)

```cpp
// 3. Algoritam (k je VANJSKA petlja!)
for (int k = 1; k <= n; k++) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            if (d[i][k] < INF && d[k][j] < INF) // Pazi na overflow
                d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
        }
    }
}
```

---

# Sažetak: Shortest Routes II

## Kako prepoznati Floyd-Warshall?

Ključ nije u težini zadatka, već u **ograničenjima (Constraints)**.

* Ako vidite **$N \le 500$**, to je ogroman signal za algoritam složenosti **$O(N^3)$**.
* Ako se traže udaljenosti između **svih parova** (All-Pairs Shortest Path).
* Ako ima puno upita ($Q$) koji se moraju odgovoriti u $O(1)$.

> **Paziti:** Kod inicijalizacije matrice, ako postoje višestruki bridovi između dva grada, uvijek zadrži onaj s **minimalnom** težinom!

---

# 3. High Score (CSES)

**Problem:**
Želimo putovati od sobe 1 do sobe $N$. Svaki tunel povećava naš rezultat za $x$.
Želimo postići **maksimalan** mogući rezultat.
Možemo prolaziti kroz sobe više puta. Ispiši -1 ako možemo postići proizvoljno velik rezultat (pozitivni ciklus).

**Analiza:**

* Tražimo **najduži put**.
* Standardni algoritmi traže najkraći put.
* **Trik:** Pomnoži sve težine s $-1$. Sada tražimo **najkraći put**.
* "Beskonačno velik rezultat" u originalu $\Leftrightarrow$ "Beskonačno mali put" (negativni ciklus) u novom grafu.

---

# High Score: Strategija

Koristimo **Bellman-Ford** algoritam jer tražimo najkraći put u grafu s negativnim težinama.

**Problem ciklusa:**
Samo postojanje negativnog ciklusa nije dovoljno za ispisati -1.
Taj ciklus mora biti:

1. Dohvatljiv iz početnog čvora (1).
2. Mora moći doseći ciljni čvor ($N$).

**Rješenje:**

1. Pokreni Bellman-Ford $N-1$ puta.
2. Pokreni ga još $N$ puta. Ako se u nekom koraku udaljenost do čvora $u$ smanji, postavi `dist[u] = -INF`.
3. To `-INF` će se "proširiti" na sve čvorove do kojih taj ciklus može doći.
4. Na kraju, ako je `dist[N] == -INF`, rješenje je -1.

---

# High Score: Kod

```cpp
// Pretvorba problema: w = -w
vector<tuple<int,int,long long>> edges;

vector<long long> dist(n + 1, INF);
dist[1] = 0;

// Prvih N-1 iteracija (Standardni Bellman-Ford)
for (int i = 1; i < n; ++i) {
    for (auto [u, v, w] : edges) {
        if (dist[u] != INF && dist[u] + w < dist[v]) {
            dist[v] = dist[u] + w;
        }
    }
}

// Dodatne iteracije za propagaciju negativnih ciklusa
// Ako se nešto može smanjiti, to je dio ciklusa -> postavi na -INF
for (int i = 1; i < n; ++i) {
    for (auto [u, v, w] : edges) {
        if (dist[u] != INF) {
            if (dist[u] == -INF) dist[v] = -INF; // Propagiraj
            else if (dist[u] + w < dist[v]) {
                dist[v] = -INF; // Detektiran ciklus
            }
        }
    }
}

if (dist[n] == -INF) cout << -1 << endl;
else cout << -dist[n] << endl; // Vrati u pozitivno
```

---

# Sažetak: High Score

## Transformacija problema

Često se problemi "najdužeg puta" ili "maksimalnog profita" rješavaju pretvaranjem u **najkraći put s negativnim težinama** ($w' = -w$).

## Zamka "Nedostižnog ciklusa"

Nije svaki negativni ciklus bitan!

* Ako postoji negativni ciklus, ali do njega **ne možemo doći** iz starta $\to$ ne utječe na rješenje.
* Ako postoji negativni ciklus, ali iz njega **ne možemo doći** do cilja $\to$ ne utječe na rješenje.
* Zato u kodu provjeravamo dostižnost (propagaciju `-INF`).

---

# 4. Flight Discount (CSES)

**Problem:**
Put od grada 1 do $N$. Imamo kupon za **50% popusta** na točno jedan let.
Nađi minimalnu cijenu.

**Intuicija: Layered Graph (Slojeviti graf)**
Možemo zamisliti da se nalazimo u dva moguća stanja:

1. `State 0`: Još nismo iskoristili kupon.
2. `State 1`: Iskoristili smo kupon.

**Prijelazi:**

* Iz `(u, 0)` u `(v, 0)`: cijena $w$ (ne koristimo kupon).
* Iz `(u, 0)` u `(v, 1)`: cijena $w/2$ (koristimo kupon sada).
* Iz `(u, 1)` u `(v, 1)`: cijena $w$ (već iskorišten).

---

# Flight Discount: Implementacija

Ovo je zapravo **Dijkstra** na grafu koji ima $2N$ čvorova.
Udaljenosti pamtimo kao `dist[čvor][stanje]`.

```cpp
priority_queue<tuple<long long, int, int>> q; // {-cijena, u, state}
dist[1][0] = 0;
dist[1][1] = 0; // Oprez: u startu nismo iskoristili, ali tehnički dist[1][1] je nedostupno osim ako...
// Zapravo inicijaliziraj sve na INF, a dist[1][0] = 0.
q.push({0, 1, 0});

while (!q.empty()) {
    auto [d, u, state] = q.top(); q.pop(); d = -d;
    
    if (d > dist[u][state]) continue;

    for (auto [v, w] : adj[u]) {
        // Opcija 1: Ne koristi kupon (zadrži stanje)
        if (dist[u][state] + w < dist[v][state]) {
            dist[v][state] = dist[u][state] + w;
            q.push({-dist[v][state], v, state});
        }
        
        // Opcija 2: Iskoristi kupon (samo ako smo u state 0)
        if (state == 0) {
            if (dist[u][0] + w/2 < dist[v][1]) {
                dist[v][1] = dist[u][0] + w/2;
                q.push({-dist[v][1], v, 1});
            }
        }
    }
}
cout << dist[n][1] << endl; // Rezultat mora završiti u stanju 1? 
// Zapravo min(dist[n][0], dist[n][1]) jer možda je najjeftinije ne iskoristiti kupon (teoretski)
```

---

# Osvrt: Flight Discount

## Tehnika: Proširenje prostora stanja (State-Space Expansion)

Ovo je jedna od najvažnijih tehnika za teške grafovske zadatke.

Kada se pravila kretanja promijene (npr. "imaš 1 kupon", "možeš preskočiti 2 zida", "auto ima goriva za K km"), čvor više nije samo `u`.
**Čvor postaje `(u, stanje)`**.

* Broj čvorova raste s $N$ na $N \times \text{broj\_stanja}$.
* Ako je broj stanja malen (ovdje 2), Dijkstra radi savršeno.

---
<!-- _class: title -->

# Zaključak

## Što smo danas naučili?

---

# Algoritam: Stablo odlučivanja

Kada dobijete zadatak s grafom, postavite si ova pitanja redom:

1. **Jesu li težine bridova 1 (ili ne postoje)?**
   $\rightarrow$ Koristi **BFS** ($O(N+M)$).
2. **Jesu li težine bridova $\ge 0$?**
   $\rightarrow$ Koristi **Dijkstru** ($O(M \log N)$).
3. **Ima li negativnih težina (ali $N$ je velik)?**
   $\rightarrow$ Koristi **Bellman-Ford** ($O(N \cdot M)$).
4. **Je li $N$ malen ($N \le 500$) i trebaju nam svi parovi?**
   $\rightarrow$ Koristi **Floyd-Warshall** ($O(N^3)$).
5. **Postoje li posebna pravila (kuponi, gorivo, stanja)?**
   $\rightarrow$ Modificiraj Dijkstru na **Slojevitom grafu**.
