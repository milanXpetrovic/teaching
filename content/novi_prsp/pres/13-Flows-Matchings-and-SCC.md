---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Mrežni tokovi, uparivanja i jake komponente"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!--
Slike (dodati ručno):
- Uvod i motivacija (protok):
  http://www.b4b.com.lv/blog-1/params/post/4802130/system-constraint-bottleneck-dialogue-part-2
  https://site-2143475.mozfiles.com/files/2143475/toc1.png
- Ford-Fulkerson / Edmonds-Karp:
  https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm
  https://upload.wikimedia.org/wikipedia/commons/a/ad/FordFulkersonDemo.gif
  https://commons.wikimedia.org/wiki/File:FordFulkerson.gif
  https://inginious.org/course/competitive-programming/graphs-maxflow
  https://inginious.org/course/competitive-programming/graphs-maxflow/anim.gif
- Rezidualni graf
- Min-Cut teorem:
  https://samarthmittal94.medium.com/graph-theory-max-min-flow-9aa0b378683d
  https://miro.medium.com/v2/resize:fit:640/format:webp/1*JMGSruP13HaLSpIfSpc2Gw.png
- Maksimalno uparivanje / SCC:
  https://cp-algorithms.com/graph/strongly-connected-components.html
  https://cp-algorithms.com/graph/strongly-connected-components-tikzpicture/graph.svg
- Kosaraju (transponirani graf):
  https://en.wikipedia.org/wiki/Transpose_graph
  transposed-graph.jpg
- Police Chase:
  https://www.telegram.hr/vijesti/ovo-je-zagreb-danas-zbog-mimohoda-zatvorene-brojne-ulice-dosta-je-promjena-i-u-javnom-prijevozu/
-->

<!-- _paginate: false -->
<!-- _class: title -->

# Mrežni tokovi, uparivanja i jake komponente

## Ford-Fulkerson, Edmonds-Karp, bipartitno uparivanje, Kosaraju

---

# Sadržaj

1. **Uvod i motivacija**
   - Protok materijala i resursa
   - Problem dodjele (assignment problem)
2. **Maksimalni tok (maximum flow)**
   - Definicije i rezidualni graf
   - Ford-Fulkerson i Edmonds-Karp
   - Min-Cut teorem
3. **Maksimalno uparivanje**
   - Bipartitni grafovi
4. **Jake komponente (SCC)**
   - Kosarajuov algoritam
   - 2-SAT problem
5. **Zadaci za vježbu**

---

# Uvod i motivacija

**1. Protok (flow)**

Zamislite mrežu cijevi. Želimo poslati **maksimalnu količinu vode** od izvora do ponora.

- Primjeri: promet u gradu, podaci u računalnoj mreži, logistika.

**2. Uparivanje (matching)**

Imamo radnike i poslove. Svaki radnik može raditi samo određene poslove.

- Cilj: zaposliti što više ljudi (maksimalno uparivanje).

**3. Struktura grafova (SCC)**

Kako analizirati grafove koji imaju cikluse?

- **Jako povezana komponenta (SCC):** unutar nje možemo doći od svakog čvora do svakog.
- Ako sažmemo SCC-ove, dobivamo **DAG** (usmjereni aciklički graf).

---

# Maksimalni tok: definicije

Imamo usmjereni graf s izvorom $s$ i ponorom $t$.
Svaki brid $(u, v)$ ima **kapacitet** $c(u, v)$.

**Pravila toka $f(u, v)$:**

1. **Kapacitet:** $0 \le f(u, v) \le c(u, v)$ (ne možemo poslati više nego što cijev prima).
2. **Očuvanje toka:** sve što uđe u čvor (osim $s$ i $t$) mora i izaći.

---

# Ključni koncept: rezidualni graf

Kako znamo možemo li poslati još toka? Gledamo **rezidualni graf**.

Za svaki brid $(u, v)$ s kapacitetom $C$ i trenutnim tokom $F$:

1. **Forward edge $(u, v)$:** preostali kapacitet je $C - F$.
2. **Backward edge $(v, u)$:** kapacitet je $F$.
   - *Ovo je ključno!* Omogućuje nam da "poništimo" odluku i preusmjerimo tok ako nađemo bolji put.

---

# Ford-Fulkerson metoda

Ideja: dok god postoji put od $s$ do $t$ u rezidualnom grafu, šaljemo tok tim putem!

1. Tok inicijaliziramo na 0.
2. Tražimo put od $s$ do $t$ (bilo kojim algoritmom) na kojem svaki brid ima $kapacitet > 0$.
3. Nađemo "usko grlo" (najmanji kapacitet na tom putu).
4. Povećamo tok na bridovima puta i smanjimo ga na obrnutim bridovima.
5. Ponavljamo dok takvog puta nema.

**Edmonds-Karp algoritam**

Specifična implementacija Ford-Fulkersona koja put traži **BFS-om**.

- **Složenost:** $O(V \cdot E^2)$
- BFS uvijek bira najkraći put (u broju bridova), što jamči zaustavljanje i polinomnu složenost.

---

# Edmonds-Karp: implementacija

```cpp
// capacity[u][v] = preostali kapacitet; adj sadrži i obrnute bridove!
int bfs(int s, int t, vector<int>& parent) {
    fill(parent.begin(), parent.end(), -1);
    parent[s] = -2;
    queue<pair<int, int>> q;
    q.push({s, INF});
    while (!q.empty()) {
        auto [u, flow] = q.front(); q.pop();
        for (int v : adj[u]) {
            if (parent[v] == -1 && capacity[u][v] > 0) {
                parent[v] = u;
                int new_flow = min(flow, capacity[u][v]);
                if (v == t) return new_flow;  // Našli smo put
                q.push({v, new_flow});
            }
        }
    }
    return 0; // Nema više puta
}

long long maxflow(int s, int t) {
    long long flow = 0;
    vector<int> parent(MAXN);
    int new_flow;
    while ((new_flow = bfs(s, t, parent)) > 0) {
        flow += new_flow;
        for (int cur = t; cur != s; cur = parent[cur]) { // Unatrag od t do s
            int prev = parent[cur];
            capacity[prev][cur] -= new_flow;
            capacity[cur][prev] += new_flow;
        }
    }
    return flow;
}
```

---

# Min-Cut teorem

**Definicija reza:** podjela čvorova na dva skupa: $S$ (sadrži izvor) i $T$ (sadrži ponor).
**Kapacitet reza:** zbroj kapaciteta bridova koji idu iz $S$ u $T$.

> **Teorem:** vrijednost maksimalnog toka jednaka je kapacitetu minimalnog reza.

**Primjena:**
Nakon što algoritam završi, svi čvorovi do kojih možemo doći iz $s$ u rezidualnom grafu čine skup $S$. Bridovi koji izlaze iz $S$ su "usko grlo" mreže.

---

# Maksimalno uparivanje (bipartitni graf)

Imamo dva skupa čvorova, $L$ (lijevo) i $R$ (desno). Bridovi idu samo iz $L$ u $R$.
Želimo odabrati maksimalan broj bridova koji nemaju zajedničkih vrhova.

**Svođenje na max flow:**

1. Dodamo **izvor $s$** i spojimo ga sa svim čvorovima u $L$ (kapacitet 1).
2. Dodamo **ponor $t$** i spojimo sve čvorove iz $R$ s njim (kapacitet 1).
3. Svi bridovi između $L$ i $R$ imaju kapacitet 1.
4. Max flow u ovoj mreži = veličina maksimalnog uparivanja.

---

# Jako povezane komponente (SCC)

**Definicija:** podskup čvorova u kojem za svaki par postoje putovi $u \to v$ i $v \to u$.

**Kosarajuov algoritam $O(N+M)$**

Koristi dva prolaza DFS-a.

1. **Prvi prolaz (DFS):**
   DFS po grafu. Bilježimo redoslijed završetka obrade čvorova (stavljamo ih na stog).

2. **Drugi prolaz (DFS po obrnutom grafu):**
   Transponiramo graf (okrenemo sve bridove: $u \to v$ postaje $v \to u$).
   Uzimamo čvorove sa stoga (obrnutim redoslijedom završetka).
   Ako čvor nije posjećen, pokrenemo DFS: svi dohvatljivi čvorovi čine jednu **SCC**.

---

# Kosaraju: implementacija

```cpp
vector<int> order, component;
vector<bool> visited;

void dfs1(int u) { // 1. prolaz
    visited[u] = true;
    for (int v : adj[u]) if (!visited[v]) dfs1(v);
    order.push_back(u); // Bilježimo vrijeme izlaska
}

void dfs2(int u) { // 2. prolaz, na obrnutom grafu
    visited[u] = true;
    component.push_back(u);
    for (int v : rev_adj[u]) if (!visited[v]) dfs2(v);
}

// Main:
// 1. dfs1 iz svakog neposjećenog čvora
// 2. reverse(order)
// 3. visited resetiramo na false
// 4. dfs2 za čvorove iz order -> svaki novi poziv je nova SCC
```

---

# Primjena: 2-SAT problem

Imamo logičku formulu: $(x_1 \lor \neg x_2) \land (\neg x_1 \lor x_3) \dots$
Može li se zadovoljiti?

**Svođenje na SCC:**

- Svaka varijabla ima dva čvora: $x_i$ i $\neg x_i$.
- Klauzula $(a \lor b)$ isto je što i $(\neg a \implies b)$ i $(\neg b \implies a)$.
- Za implikacije dodajemo bridove.

**Rješenje:**
Formula je **nezadovoljiva** ako i samo ako se $x_i$ i $\neg x_i$ nalaze u **istoj SCC** (to znači $x_i \implies \neg x_i$ i obrnuto, što je kontradikcija).

CSES zadatak za vježbu: **[Giant Pizza](https://cses.fi/problemset/task/1684)**.

---

<!-- _class: title -->

# Zadaci za vježbu

---

<!-- _class: title -->

# Police Chase (CSES)

## Primjena Max-Flow Min-Cut teorema

---

# Zadatak: Police Chase

**Problem:**
Kaaleppi je opljačkao banku (čvor 1) i bježi prema luci (čvor $n$). Policija želi spriječiti bijeg zatvaranjem ulica.

**Ulaz:**

- $n$ križanja ($2 \le n \le 500$) i $m$ ulica.
- Ulice su dvosmjerne.

**Izlaz:**

1. **Minimalni broj ulica** koje treba zatvoriti da ne postoji put od 1 do $n$.
2. Popis tih ulica.

---

# Intuicija i modeliranje

Ovo je klasičan problem **minimalnog reza (Min-Cut)**.

- Graf želimo podijeliti na dva dijela: jedan sadrži izvor (banku), a drugi ponor (luku).
- Cijena reza je broj bridova koje "presijecamo".
- Želimo minimizirati tu cijenu.

**Teorem o maksimalnom toku i minimalnom rezu:**
> Vrijednost maksimalnog toka u mreži jednaka je kapacitetu minimalnog reza.

**Ideja rješenja:**

1. Svakoj ulici dodijelimo **kapacitet 1**.
2. Izračunamo **maksimalni tok** od 1 do $n$. Vrijednost toka = broj ulica.
3. Koje su to ulice, otkrivamo analizom **rezidualnog grafa**.

---

# Korak 1: izgradnja grafa

Budući da su ulice dvosmjerne, a graf toka usmjeren, svaka ulica između $u$ i $v$ postaje:

- brid $u \to v$ s kapacitetom 1,
- brid $v \to u$ s kapacitetom 1.

Zašto 1? Jer zatvaranje jedne ulice "košta" 1.

```cpp
for (int i = 0; i < m; ++i) {
    int u, v; cin >> u >> v;
    // Pamtimo originalne bridove za ispis rješenja na kraju
    original_edges.push_back({u, v});

    // Gradimo graf za max flow
    adj[u].push_back(v);
    adj[v].push_back(u);
    capacity[u][v] = 1;
    capacity[v][u] = 1;
}
```

---

# Korak 2: izračun maksimalnog toka

Koristimo **Edmonds-Karp** (funkciju `maxflow` iz uvodnog dijela).
Tok je najviše $n - 1$ (toliko bridova najviše izlazi iz čvora 1), a svaki BFS je $O(m)$, pa je ovo dovoljno brzo.

```cpp
long long max_flow = maxflow(1, n); // 1 je izvor, n je ponor
```

---

# Korak 3: rekonstrukcija reza (ključni dio!)

Kad max flow algoritam završi, kako znamo koje ulice zatvoriti?

**Definicija min-cuta:**

Minimalni rez dijeli čvorove na dva skupa:

- **Skup S:** čvorovi koji su i dalje **dohvatljivi** iz izvora u *rezidualnom grafu*.
- **Skup T:** čvorovi koji su postali nedohvatljivi jer su bridovi "zasićeni".

**Algoritam za rekonstrukciju:**

1. Pokrenemo BFS/DFS iz izvora (čvor 1) koristeći **samo bridove s preostalim kapacitetom > 0**.
2. Svi posjećeni čvorovi čine skup $S$.
3. Rješenje su sve **originalne ulice** $(u, v)$ kojima je jedan kraj u $S$, a drugi u $T$.

---

# Implementacija rekonstrukcije

```cpp
// 1. Označimo sve dohvatljive čvorove u rezidualnom grafu
vector<bool> visited(n + 1, false);
queue<int> q;
q.push(1);
visited[1] = true;

while (!q.empty()) {
    int u = q.front(); q.pop();
    for (int v : adj[u]) {
        // Ključno: možemo li proći bridom u rezidualnom grafu?
        if (!visited[v] && capacity[u][v] > 0) {
            visited[v] = true;
            q.push(v);
        }
    }
}

// 2. Ispisujemo bridove koji prelaze iz S u T
cout << max_flow << "\n";
for (auto [u, v] : original_edges) {
    // Ako je jedan kraj dohvatljiv, a drugi nije -> to je brid reza
    if (visited[u] != visited[v]) cout << u << " " << v << "\n";
}
```

---

# Sažetak rješenja

1. **Modeliramo problem:**
   - Čvorovi = križanja.
   - Bridovi = ulice (dvosmjerne, kapacitet 1).
   - Izvor = 1, ponor = $N$.

2. **Izračunamo max flow:**
   - Rezultat (broj) je minimalni broj ulica koje treba zatvoriti.
   - Ovo "zasićuje" usko grlo mreže.

3. **Pronađemo min cut:**
   - Nađemo sve čvorove do kojih još uvijek možemo doći iz izvora (skup $S$).
   - Bridovi koji povezuju $S$ i ostatak grafa su tražene ulice.

---

<!-- _class: title -->

# School Dance (CSES)

## Maksimalno uparivanje u bipartitnom grafu

---

# Zadatak: School Dance

**Problem:**
U školi je $N$ dječaka i $M$ djevojčica. Postoji $K$ potencijalnih parova (dječak i djevojčica koji žele plesati zajedno).
Svaki učenik može plesati **najviše s jednim** partnerom.

**Cilj:**
Pronaći **maksimalan broj parova** koji mogu plesati istovremeno i ispisati te parove.

**Ograničenja:**

- $N, M \le 500$
- $K \le 1000$

---

# Intuicija: bipartitni graf

Ovo je problem na **bipartitnom grafu** jer čvorove možemo podijeliti u dvije skupine:

1. **Lijeva strana:** dječaci (1 do $N$).
2. **Desna strana:** djevojčice (1 do $M$).

Bridovi postoje **samo** između lijeve i desne strane.

Tražimo **maksimalno uparivanje (matching):** skup bridova bez zajedničkih vrhova.

---

# Rješenje: svođenje na maksimalni tok

Problem rješavamo pretvaranjem u mrežu toka.

1. **Dodamo super-izvor ($S$):** spojimo ga sa svim dječacima.
   - Kapacitet bridova $S \to \text{Boy}_i$ je **1** (svaki dječak sudjeluje u najviše 1 paru).

2. **Dodamo super-ponor ($T$):** spojimo sve djevojčice s njim.
   - Kapacitet bridova $\text{Girl}_j \to T$ je **1** (svaka djevojčica sudjeluje u najviše 1 paru).

3. **Veza dječak-djevojčica:**
   - Ako dječak $i$ i djevojčica $j$ žele plesati, dodamo brid $\text{Boy}_i \to \text{Girl}_j$ s kapacitetom **1**.

**Rezultat:** maksimalni tok u ovoj mreži = maksimalan broj parova.

---

# Implementacija: numeracija čvorova

U ulazu su dječaci $1..N$ i djevojčice $1..M$, pa čvorove moramo jedinstveno označiti:

- **Izvor ($S$):** čvor 0.
- **Dječaci ($1 \dots N$):** čvorovi $1 \dots N$.
- **Djevojčice ($1 \dots M$):** čvorovi $N+1 \dots N+M$.
- **Ponor ($T$):** čvor $N+M+1$.

```cpp
int n, m, k; cin >> n >> m >> k;
int s = 0, t = n + m + 1;

auto add_edge = [&](int u, int v) {   // Brid kapaciteta 1 + obrnuti brid
    adj[u].push_back(v); adj[v].push_back(u);
    capacity[u][v] = 1;
};

for (int i = 0; i < k; ++i) {
    int u, v; cin >> u >> v;
    add_edge(u, n + v);               // Dječak u -> djevojčica v (čvor n+v)
}
for (int i = 1; i <= n; ++i) add_edge(s, i);      // Izvor -> dječaci
for (int i = 1; i <= m; ++i) add_edge(n + i, t);  // Djevojčice -> ponor
```

---

# Izračun toka (Edmonds-Karp)

Koristimo istu funkciju `maxflow` kao i dosad:

```cpp
long long max_pairs = maxflow(s, t);
```

S jediničnim kapacitetima tok je najviše $\min(N, M)$, a svaki BFS je $O(K + N + M)$. Ukupno je to dovoljno brzo za ova ograničenja.
(Postoji i specijalizirani, brži algoritam za bipartitno uparivanje, Hopcroft-Karp, ali ovdje nije potreban.)

---

# Rekonstrukcija rješenja

Kad algoritam završi, ispisujemo parove.
Gledamo bridove koji idu od **dječaka** prema **djevojčicama**.

Ako je kapacitet brida $\text{Boy}_i \to \text{Girl}_j$ postao **0** (a bio je 1), tok je prošao tuda: **oni su par!**

```cpp
cout << max_pairs << "\n";

for (int i = 1; i <= n; ++i) {          // Iteriramo kroz dječake
    for (int v : adj[i]) {
        // Susjed je djevojčica (indeks > n), a ne izvor/ponor
        if (v > n && v != t && capacity[i][v] == 0) {
            cout << i << " " << (v - n) << "\n"; // Originalni indeksi
        }
    }
}
```

---

# Sažetak

1. **Modeliranje:**
   - Izvor $\to$ dječaci (kapacitet 1).
   - Djevojčice $\to$ ponor (kapacitet 1).
   - Dječak $\to$ djevojčica (kapacitet 1).

2. **Algoritam:**
   - Pustimo max flow.
   - Vrijednost toka je broj parova.

3. **Ispis:**
   - Provjerimo zasićene bridove između dječaka i djevojčica.
   - Pazimo na mapiranje indeksa ($v - n$ za djevojčice).

---

<!-- _class: title -->

# CSES: Distinct Routes

## Bridno disjunktni putovi i rekonstrukcija toka

---

# Zadatak: Distinct Routes

**Problem:**
Igra se odvija u $N$ soba povezanih teleporterima. Cilj je doći od sobe 1 do sobe $N$.
Svaki teleporter (brid) može se iskoristiti **najviše jednom** tijekom cijele igre (kroz sve dane).

**Pitanje:**
Koliko najviše dana možemo igrati (tj. koliko različitih putova možemo pronaći) i koji su to putovi?

**Ograničenja:**

- $N \le 500$, $M \le 1000$.
- Bridovi su usmjereni.

---

# Modeliranje: max flow

Ovo je školski primjer problema **bridno disjunktnih putova**.

1. **Kapaciteti:**
   Svakom teleporteru dodijelimo **kapacitet 1**.
   - Tako kroz njega tok može proći najviše jednom.

2. **Tok:**
   Pustimo maksimalni tok od čvora 1 do čvora $N$.

3. **Značenje rezultata:**
   - **Vrijednost max flowa ($K$)** = maksimalni broj dana (putova).
   - Svaka jedinica toka koja stigne u ponor predstavlja jedan valjani put.

---

# Korak 1: izračun toka

Koristimo Edmonds-Karp ili Dinic. Ovdje je zgodnije bridove pamtiti kao strukture (umjesto matrice kapaciteta), kako bismo kasnije mogli provjeriti koji su bridovi iskorišteni.

```cpp
struct Edge {
    int v;          // Kamo vodi
    int flow;       // Trenutni tok
    int capacity;   // Kapacitet (1 za originalni brid, 0 za obrnuti)
    int rev;        // Indeks obrnutog brida u adj[v]
};

// ... inicijalizacija i max flow algoritam ...
// Nakon izvršenja imamo max_flow = K.
cout << max_flow << "\n";
```

Nakon što algoritam završi, bridovi koji su dio rješenja imaju `flow == 1`.

---

# Korak 2: rekonstrukcija putova (izazov)

Kroz mrežu "teče" $K$ jedinica toka. Kako ih razdvojiti u $K$ zasebnih putova?

**Ideja (ljuštenje grafa):**

1. Znamo da imamo $K$ putova.
2. Pokrenemo petlju $K$ puta.
3. U svakoj iteraciji radimo **DFS** (ili jednostavnu šetnju) od izvora (1) do ponora ($N$).
4. Krećemo se **samo po bridovima koji imaju `flow == 1`**.
5. **Ključno:** kad prođemo kroz brid, postavimo mu `flow = 0`.
   - Time ga "brišemo" iz grafa da ga idući put ne koristi.
   - Zbog očuvanja toka sigurno ćemo stići do ponora.

---

# Implementacija rekonstrukcije

```cpp
for (int k = 0; k < max_flow; ++k) {
    vector<int> current_path;
    int curr = 1;

    while (curr != n) {
        current_path.push_back(curr);

        for (auto& edge : adj[curr]) {
            // Brid je dio toka (flow == 1) i nije obrnuti brid (capacity == 1)
            if (edge.capacity == 1 && edge.flow == 1) {
                edge.flow = 0;  // Uklanjamo brid
                curr = edge.v;  // Pomičemo se na idući čvor
                break;          // Izlazimo iz for petlje, nastavljamo while
            }
        }
    }
    current_path.push_back(n); // Dodajemo krajnji čvor

    // Ispis
    cout << current_path.size() << "\n";
    for (int node : current_path) cout << node << " ";
    cout << "\n";
}
```

---

# Sažetak

1. **Problem:** naći što više putova koji ne dijele bridove.
2. **Alat:** maksimalni tok s kapacitetima bridova 1.
3. **Rezultat:** vrijednost toka je broj putova.
4. **Ispis:**
   - Graf sada sadrži superpoziciju svih putova.
   - Koristimo pohlepni prolaz (šetnju) prateći bridove s tokom.
   - **Destruktivno čitanje:** kad brid iskoristimo za jedan put, brišemo mu tok da ga ne bismo koristili za drugi put.

---

<!-- _class: title -->

# CSES: Coin Collector

## Kondenzacija grafa i DP na DAG-u

---

# Zadatak: Coin Collector

**Problem:**
Imamo $N$ soba i $M$ jednosmjernih tunela. Svaka soba sadrži određeni broj novčića $k_i$.
Možemo početi u bilo kojoj sobi i završiti u bilo kojoj.

**Cilj:**
Sakupiti **maksimalan ukupan broj novčića**.
(Napomena: ako se vrtimo u krug, možemo pokupiti novčiće iz svih soba u tom krugu.)

**Ograničenja:**

- $N \le 10^5$, $M \le 2 \cdot 10^5$.
- Novčići $k_i \le 10^9$.
- **Pazite:** ukupna suma može premašiti 32-bitni integer $\to$ koristite `long long`.

---

# Intuicija i analiza

1. **Ciklusi:**
   Ako uđemo u skup soba koje čine ciklus (ili jače: **jako povezanu komponentu, SCC**), možemo se vrtjeti u krug koliko god želimo.
   $\Rightarrow$ **Uvijek uzimamo SVE novčiće iz cijele komponente.**

2. **Kondenzacija grafa:**
   Svaku SCC možemo promatrati kao jedan **"super-čvor"**.
   Težina tog super-čvora je zbroj svih novčića u toj komponenti.

3. **Struktura:**
   Kada graf sažmemo u SCC-ove, dobivamo **DAG** (Directed Acyclic Graph).
   Problem se svodi na pronalaženje puta s najvećom težinom u DAG-u.

---

# Korak 1: pronalaženje SCC-ova

Komponente identificiramo **Kosarajuovim algoritmom** (ili Tarjanovim).
Istovremeno računamo sumu novčića za svaku komponentu.

```cpp
// 1. prolaz (DFS): računanje poretka
void dfs1(int u) {
    visited[u] = true;
    for (int v : adj[u]) if (!visited[v]) dfs1(v);
    order.push_back(u);
}

// 2. prolaz (DFS po obrnutom grafu): formiranje komponenata
void dfs2(int u, int comp_id) {
    visited[u] = true;
    component[u] = comp_id;
    scc_coins[comp_id] += coins[u]; // Zbrajamo novčiće u komponenti!
    for (int v : rev_adj[u]) if (!visited[v]) dfs2(v, comp_id);
}
```

---

# Korak 2: izgradnja kondenziranog grafa (DAG)

Sada gradimo novi graf u kojem su čvorovi indeksi komponenata.

```cpp
// adj_scc[u] sadrži listu susjednih KOMPONENATA
vector<int> adj_scc[MAXN];

for (int u = 1; u <= n; ++u) {
    for (int v : adj[u]) {
        // Ako postoji brid između dvije RAZLIČITE komponente
        if (component[u] != component[v]) {
            adj_scc[component[u]].push_back(component[v]);
        }
    }
}
```

*Napomena:* ovdje možemo dobiti višestruke bridove između istih komponenata. DP-u to ne smeta (samo ćemo isti max uzeti više puta), a za čišći graf možemo koristiti `std::unique` ili `std::set`.

---

# Korak 3: DP na DAG-u

Tražimo najdulji (težinski) put u DAG-u. Budući da nema ciklusa, možemo koristiti **memoizaciju** (rekurziju s pamćenjem).

**Stanje:** `dp[u]` = maksimalan broj novčića koje možemo skupiti počevši od komponente `u`.
**Prijelaz:** `dp[u] = scc_coins[u] + max(dp[v])` za sve susjedne komponente `v`.

```cpp
long long memo[MAXN];
bool visited_dp[MAXN];

long long solve_dp(int u) {
    if (visited_dp[u]) return memo[u];

    long long max_next = 0;
    for (int v : adj_scc[u]) {
        max_next = max(max_next, solve_dp(v));
    }

    visited_dp[u] = true;
    return memo[u] = scc_coins[u] + max_next;
}
```

---

# Glavni program

```cpp
int main() {
    // ... učitavanje, Kosarajuov algoritam ...

    // Izračunamo SCC-ove i popunimo scc_coins
    // Izgradimo adj_scc graf

    long long ans = 0;

    // Rješenje je maksimum DP-a pokrenutog iz svake komponente
    // (možemo početi bilo gdje)
    for (int i = 1; i <= scc_count; ++i) {
        ans = max(ans, solve_dp(i));
    }

    cout << ans << "\n";
}
```

**Složenost:**

- Kosaraju: $O(N + M)$
- Izgradnja DAG-a: $O(N + M)$
- DP (svaki brid i čvor DAG-a jednom): $O(N_{scc} + M_{scc})$
- **Ukupno:** $O(N + M)$, što je idealno za $10^5$.

---

# Sažetak rješenja

1. **Prepoznajemo SCC:** ako možemo kružiti, uzimamo sve.
   $\to$ Kondenziramo graf u komponente.
2. **Računamo težine:** svaki čvor u novom grafu ima težinu jednaku sumi novčića u toj komponenti.
3. **Gradimo DAG:** bridovi idu samo između različitih komponenata.
4. **DP:** nađemo put s najvećom sumom u DAG-u.
   - `dp[u] = weight[u] + max(dp[neighbours])`

---

<!-- _class: title -->

# CSES: Planets and Kingdoms

## Direktna primjena jakih komponenata (SCC)

---

# Zadatak: Planets and Kingdoms

**Problem:**
Imamo $N$ planeta i $M$ jednosmjernih teleportera.
Definicija kraljevstva: dva planeta $A$ i $B$ pripadaju istom kraljevstvu **ako i samo ako** postoji put od $A$ do $B$ **i** put od $B$ do $A$.

**Cilj:**

1. Odrediti ukupan broj kraljevstava.
2. Svakom planetu dodijeliti oznaku kraljevstva (broj od $1$ do $K$).

**Ograničenja:**

- $N \le 10^5$, $M \le 2 \cdot 10^5$.
- Potrebna složenost: linearna, $O(N+M)$.

---

# Teorija: što je zapravo "kraljevstvo"?

Uvjet zadatka ($A \to B$ i $B \to A$) točna je matematička definicija **jako povezane komponente (Strongly Connected Component, SCC)**.

Zadatak se svodi na:

1. Pronalazak svih SCC-ova u grafu.
2. Njihovo prebrojavanje.
3. Pridruživanje ID-a komponente svakom čvoru.

Koristit ćemo **Kosarajuov algoritam** (dva prolaza DFS-a).

---

# Kosarajuov algoritam: pregled

Algoritam radi u dva koraka koristeći DFS:

1. **Prvi prolaz (originalni graf):**
   - Cilj je odrediti "topološki" poredak završetka obrade.
   - Kad DFS završi s čvorom $u$, stavimo ga na **stog** (ili u listu).

2. **Drugi prolaz (transponirani graf):**
   - "Okrenemo" sve bridove ($u \to v$ postaje $v \to u$).
   - Uzimamo čvorove sa stoga (zadnji obrađen $\to$ prvi).
   - Ako čvor nije posjećen, pokrećemo DFS. Svi dohvatljivi čvorovi u ovom koraku čine **jedno kraljevstvo**.

---

# Korak 1: prvi DFS (punjenje stoga)

Trebamo pratiti poredak izlaska iz DFS-a.

```cpp
vector<int> adj[MAXN], rev_adj[MAXN];
vector<int> order;
bool visited[MAXN];

void dfs1(int u) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) dfs1(v);
    }
    // Ključno: u listu dodajemo tek kad smo obradili svu djecu
    order.push_back(u);
}
```

*Napomena:* pri učitavanju bridova odmah gradimo i `rev_adj` (obrnuti graf):
`rev_adj[v].push_back(u)` za svaki ulaz `u -> v`.

---

# Korak 2: drugi DFS (označavanje kraljevstava)

Sada radimo na **obrnutom** grafu. Svaki put kad pokrenemo `dfs2` iz glavne petlje, nalazimo novo kraljevstvo.

```cpp
int kingdom[MAXN]; // Ovdje spremamo rješenje

void dfs2(int u, int k_id) {
    visited[u] = true;
    kingdom[u] = k_id; // Planetu pridružujemo ID kraljevstva

    for (int v : rev_adj[u]) {
        if (!visited[v]) dfs2(v, k_id);
    }
}
```

---

# Glavni program

```cpp
int main() {
    // ... učitavamo N, M, gradimo adj i rev_adj ...

    // 1. prolaz
    fill(visited, visited + n + 1, false);
    for (int i = 1; i <= n; ++i) {
        if (!visited[i]) dfs1(i);
    }

    // 2. prolaz
    fill(visited, visited + n + 1, false);
    reverse(order.begin(), order.end()); // Bitno! Krećemo od zadnjeg završenog

    int kingdom_count = 0;
    for (int u : order) {
        if (!visited[u]) {
            kingdom_count++;
            dfs2(u, kingdom_count);
        }
    }

    // Ispis rezultata
    cout << kingdom_count << "\n";
    for (int i = 1; i <= n; ++i) cout << kingdom[i] << " ";
    cout << "\n";
}
```

---

# Analiza složenosti

1. **Izgradnja grafa:** $O(N + M)$ (učitavamo i gradimo normalni i obrnuti graf).
2. **Prvi DFS:** posjećuje svaki čvor i brid točno jednom. $O(N + M)$.
3. **Drugi DFS:** također posjećuje svaki čvor i brid točno jednom (na obrnutom grafu). $O(N + M)$.

**Ukupna složenost:** **$O(N + M)$**
Vremenski limit od 1 s sasvim je dovoljan za $N=10^5$.
Memorijski limit je također siguran (koristimo nekoliko nizova veličine $N$).

---

# Sažetak

1. Problem traži particioniranje grafa na skupove uzajamno dohvatljivih čvorova.
2. To je definicija **jako povezanih komponenata (SCC)**.
3. Rješenje je "udžbenička" primjena **Kosarajuovog algoritma**:
   - DFS1 (poredak po vremenu završetka).
   - Okrenemo bridove.
   - DFS2 (brojimo komponente i označavamo ih).