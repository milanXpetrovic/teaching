---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Upiti nad rasponima (Range Queries)"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!-- _paginate: false -->
<!-- _class: title -->

# Upiti nad rasponima

## Prefiksne sume, Fenwick stablo i segmentno stablo

---

# Sadržaj

1. **Uvod i motivacija**
   - Što su upiti nad rasponima?
   - Zašto je naivni pristup prespor?
2. **Statički upiti**
   - Prefiksne sume
3. **Dinamički upiti (ažuriranje točke)**
   - Fenwick stablo (Binary Indexed Tree)
   - Segmentno stablo
4. **Zadaci za vježbu**

---

# Uvod: što su upiti nad rasponima?

Imamo niz $A$. Želimo efikasno odgovarati na pitanja o podnizu (rasponu) $[L, R]$.

**Najčešći tipovi upita:**

1. **Sum:** zbroj elemenata od $L$ do $R$.
2. **Min/Max:** najmanji/najveći element u rasponu.
3. **Najveći zajednički djelitelj (GCD), XOR, ...:** ostale asocijativne operacije.

**Problem naivnog pristupa**

Ako za svaki upit vrtimo petlju od $L$ do $R$:

- Složenost jednog upita: $O(N)$
- Za $Q$ upita: **$O(N \cdot Q)$**
- Za $N, Q = 10^5$ to je $10^{10}$ operacija $\to$ **Time Limit Exceeded (TLE)**.

Cilj: **$O(\log N)$** ili **$O(1)$** po upitu.

---

# Statički upiti: prefiksne sume (1/2)

Ako se niz **ne mijenja**, možemo koristiti prefiksne sume.

**Ideja:** `P[i]` sadrži zbroj prvih $i$ elemenata: $A[0] + \dots + A[i-1]$.

**Izgradnja $O(N)$:**

```cpp
vector<long long> P(n + 1, 0);
for (int i = 0; i < n; ++i) {
    P[i+1] = P[i] + a[i];
}
```

**Upit $O(1)$:** zbroj raspona $[L, R]$ (inkluzivno, 0-indeksirano) je:
$$ \text{sum}(L, R) = P[R+1] - P[L] $$

---

# Statički upiti: prefiksne sume (2/2)

![w:900px center](../../../img/prsp/range-queries/prefiksne-sume-vizualizacija.png)

---

# Dinamički upiti: motivacija

Što ako se vrijednosti u nizu **mijenjaju**?

- Prefiksne sume zahtijevaju ponovnu izgradnju: $O(N)$ po promjeni.
- Trebamo strukturu koja brzo podržava i **update** i **query**.

**Fenwick stablo (Binary Indexed Tree, BIT)**

- Podržava **point update** i **range sum**.
- Složenost: **$O(\log N)$** za obje operacije.
- Memorija: **$O(N)$**.
- Jako malo koda, temelji se na bitovnim operacijama.

**Intuicija:** svaki indeks $k$ pamti sumu raspona čija je duljina najveća potencija broja 2 koja dijeli $k$ (LSB). LSB (Least Significant Bit) je najdesniji bit koji je 1 u binarnom zapisu broja.

---

# Fenwick stablo

![center](../../../img/prsp/range-queries/fenwick-tree-structure-fixed.png)

---

# Logika: tko je za što odgovoran?

Ključ razumijevanja je u **binarnom zapisu** indeksa. Svaki čvor u nizu ne čuva samo svoju vrijednost, već sumu određenog bloka.

- Duljina bloka određena je **najmanjim bitom jedinice** (LSB).
- **Pravilo:** indeks pokriva raspon `[indeks - LSB + 1, indeks]`.

**Primjeri (1-based notacija):**

- `12` (`1100`) $\rightarrow$ LSB je 4. Pokriva 4 elementa: `[9, 10, 11, 12]`.
- `6` (`0110`) $\rightarrow$ LSB je 2. Pokriva 2 elementa: `[5, 6]`.
- `7` (`0111`) $\rightarrow$ LSB je 1. Pokriva 1 element: `[7]`.

---

# Fenwick stablo: ažuriranje vrijednosti

![center](../../../img/prsp/range-queries/fenwick-update-path-fixed.png)

---

# Logika kretanja: gore i dolje

Kako se krećemo po stablu ovisi o operaciji:

1. **Upit (query/read):** krećemo se **DOLJE** (prema 0).
    - Uzimamo sumu trenutnog bloka.
    - Oduzimamo duljinu bloka da skočimo na kraj prethodnog raspona.
    - *Cilj:* sakupiti sve dijelove prefiksa.

2. **Ažuriranje (update):** krećemo se **GORE** (prema N).
    - Ažuriramo trenutni čvor.
    - Dodajemo duljinu bloka da nađemo prvog "roditelja" koji nas sadrži.
    - *Cilj:* obavijestiti sve veće blokove da se dio njih promijenio.

---

# Računanje sume raspona $[L, R]$

Fenwick stablo ne može izravno vratiti sumu od $L$ do $R$. Ono uvijek vraća **prefiksnu sumu** (od početka do nekog indeksa).

Koristimo princip oduzimanja prefiksa: $Suma(L, R) = Suma(1, R) - Suma(1, L-1)$

**Vizualno:**

1. Tražimo sumu plavog dijela (od $L$ do $R$).
2. Izračunamo sumu do $R$ (`query(R)`).
3. Oduzmemo sumu do $L-1$ (`query(L-1)`).
4. Ostatak je traženi raspon.

*Vremenska složenost ostaje $O(\log N)$ jer radimo samo dva upita.*

---

# Primjer: upit za raspon $[5, 13]$ (1-based)

Želimo izračunati sumu elemenata od indeksa 5 do 13: `Rezultat = query(13) - query(4)`

**1. korak: `query(13)` (suma $[1, 13]$).** Algoritam kreće od 13 i skuplja blokove unatrag (prema 0):

- Uzima **blok 13** (pokriva samo sebe). $\rightarrow$ *skače na 12*
- Uzima **blok 12** (pokriva $[9, 12]$). $\rightarrow$ *skače na 8*
- Uzima **blok 8** (pokriva $[1, 8]$). $\rightarrow$ *skače na 0 (kraj)*

> $\text{Suma}_A = \text{tree}[13] + \text{tree}[12] + \text{tree}[8]$

**2. korak: `query(4)` (suma $[1, 4]$).** Algoritam kreće od 4 (jer je to $L-1$):

- Uzima **blok 4** (pokriva $[1, 4]$). $\rightarrow$ *skače na 0 (kraj)*

> $\text{Suma}_B = \text{tree}[4]$

**3. korak: oduzimanje.** `Rezultat` = $\text{Suma}_A - \text{Suma}_B$: od sume prvih 13 brojeva "odrezali" smo prva 4. Ostaje točno suma od 5 do 13.

---

# Fenwick stablo: implementacija (1-based)

Ključna operacija: `idx & -idx` (dohvaća LSB).

```cpp
vector<long long> bit; // Veličina n + 1, indeksi 1..n

// Dodaje 'delta' na indeks 'idx' (krećemo se GORE)
void update(int idx, long long delta) {
    for (; idx <= n; idx += idx & -idx)
        bit[idx] += delta;
}

// Vraća sumu prefiksa [1, idx] (krećemo se DOLJE)
long long query(int idx) {
    long long res = 0;
    for (; idx > 0; idx -= idx & -idx)
        res += bit[idx];
    return res;
}

// Suma raspona [l, r]
long long query(int l, int r) {
    return query(r) - query(l - 1);
}
```

---

# Napomena: 0-based varijanta

Ako baš želimo indekse od 0, formule se prilagođavaju:

- **Kretanje gore (update):** `idx = idx | (idx + 1)`
  Postavlja najniži bit koji je 0 na 1. Npr. `0011` (3) $\to$ `0111` (7) $\to$ `1111` (15)...
- **Kretanje dolje (query):** `r = (r & (r + 1)) - 1`
  Efektivno "skida" zadnji blok raspona.

```cpp
void update(int idx, long long delta) {
    for (; idx < n; idx = idx | (idx + 1)) bit[idx] += delta;
}
long long query(int r) { // Suma [0, r]
    long long res = 0;
    for (; r >= 0; r = (r & (r + 1)) - 1) res += bit[r];
    return res;
}
```

Blokovi tada nisu isti kao na slikama (1-based), pa je za učenje lakše držati se 1-based verzije.

---

# Segmentno stablo

Fleksibilnije od Fenwick stabla. Podržava:

- Sum, Min, Max, GCD, XOR...
- Čak i složenije operacije (npr. max subsegment sum).

**Struktura:**

- Binarno stablo izgrađeno nad nizom.
- **Listovi:** elementi originalnog niza.
- **Unutarnji čvorovi:** agregat (npr. zbroj) svoje djece.
- **Korijen:** agregat cijelog niza $[0, N-1]$.

**Složenost:**

- Izgradnja: $O(N)$
- Upit i ažuriranje: $O(\log N)$

---

# Segmentno stablo: vizualizacija

![w:900px center](../../../img/prsp/range-queries/segment-tree-structure.png)

---

# Kako pamtimo stablo u nizu?

Iako je logička struktura stablo, fizički koristimo običan niz.
Koristimo **heap-like indeksiranje**, slično kao kod binarne gomile (binary heap).

Ako je čvor na indeksu `k`:

- Njegovo **lijevo dijete** je na `2 * k`.
- Njegovo **desno dijete** je na `2 * k + 1`.
- Korijen je na indeksu `1`.

> Zato alociramo niz veličine `4 * N`.
> *(Sigurna granica jer stablo nije uvijek savršeno popunjeno ako N nije potencija broja 2.)*

---

# Segmentno stablo: izgradnja (build)

Rekurzivno dijelimo niz na polovice dok ne dođemo do listova. Zatim se vraćamo i računamo sume.

```cpp
long long tree[4 * MAXN]; // 4x veličina niza

// Poziv: build(1, 0, n-1)
void build(int node, int start, int end) {
    if (start == end) {
        tree[node] = A[start];  // Došli smo do lista
    } else {
        int mid = (start + end) / 2;
        build(2*node, start, mid);      // Rekurzivno gradimo djecu
        build(2*node+1, mid+1, end);
        tree[node] = tree[2*node] + tree[2*node+1]; // Spajamo rezultate
    }
}
```

---

# Segmentno stablo: ažuriranje (update)

Slično binarnoj pretrazi. Tražimo list koji treba promijeniti, a pri povratku ažuriramo sve pretke.

```cpp
// Ažuriranje (point update)
void update(int node, int start, int end, int idx, long long val) {
    if (start == end) {
        tree[node] = val;
    } else {
        int mid = (start + end) / 2;
        if (idx <= mid)
            update(2*node, start, mid, idx, val);     // Lijevo
        else
            update(2*node+1, mid+1, end, idx, val);   // Desno

        tree[node] = tree[2*node] + tree[2*node+1];
    }
}
```

---

# Logika upita: tri slučaja

Kad tražimo sumu raspona $[L, R]$, svaki čvor provjerava svoj raspon $[start, end]$ u odnosu na traženi $[L, R]$.

Postoje samo 3 situacije:

1. 🔴 **Bez preklapanja:** čvor je potpuno izvan $[L, R]$.
    - *Akcija:* vratimo `0` (neutralni element).
2. 🟢 **Potpuno preklapanje:** čvor je cijeli unutar $[L, R]$.
    - *Akcija:* vratimo vrijednost čvora `tree[node]`. **Ne idemo dublje!**
3. 🟡 **Djelomično preklapanje:** dio čvora je unutra, dio vani.
    - *Akcija:* dijelimo se! Pozivamo upit za lijevo i desno dijete.

---

# Segmentno stablo: upit (kod)

Implementacija tri slučaja:

```cpp
long long query(int node, int start, int end, int l, int r) {
    // 1. Potpuno izvan (🔴)
    if (r < start || end < l) return 0;

    // 2. Potpuno unutar (🟢)
    if (l <= start && end <= r) return tree[node];

    // 3. Djelomično (🟡) -> pitamo djecu
    int mid = (start + end) / 2;
    long long p1 = query(2*node, start, mid, l, r);
    long long p2 = query(2*node+1, mid+1, end, l, r);

    return p1 + p2;
}
```

---

# Primjer izvršavanja upita

Niz: `[1, 2, 3, 4, 5, 6, 7, 8]` (indeksi 0-7).
Upit: **suma od 2 do 6** (`[2, 6]`). Očekujemo $3+4+5+6+7 = 25$.

- **Korijen [0, 7]:** djelomično $\rightarrow$ pitamo djecu.
  - **Lijevo [0, 3]:** djelomično.
    - **[0, 1]:** potpuno izvan $\rightarrow$ `0`.
    - **[2, 3]:** potpuno unutar $\rightarrow$ **7**.
    - *Lijeva suma = 0 + 7 = 7.*
  - **Desno [4, 7]:** djelomično.
    - **[4, 5]:** potpuno unutar $\rightarrow$ **11**.
    - **[6, 7]:** djelomično: **[6, 6]** unutra $\rightarrow$ **7**, **[7, 7]** vani $\rightarrow$ `0`.
    - *Desna suma = 11 + 7 = 18.*

**Konačni rezultat:** $7 + 18 = 25$.

---

# Segmentno stablo: vizualizacija upita

![w:900px center](../../../img/prsp/range-queries/segment-tree-query-decomposition.png)

---

<!-- _class: title -->
# Zadaci za vježbu

---

<!-- _class: title -->

# CSES: Static Range Sum Queries

## Uvod u prefiksne sume

---

# Zadatak: Static Range Sum Queries

**Problem:**
Zadan je niz od $N$ cijelih brojeva. Trebamo odgovoriti na $Q$ upita.
Svaki upit traži zbroj elemenata u rasponu $[a, b]$.

**Ulaz:**

- $N, Q$ ($1 \le N, Q \le 2 \cdot 10^5$)
- Niz vrijednosti $x_i$ ($1 \le x_i \le 10^9$)
- $Q$ linija s parovima $(a, b)$.

**Izlaz:**

- Zbroj elemenata za svaki upit.

---

# Zašto naivni pristup ne radi?

Naivno rješenje bi za svaki upit vrtjelo petlju od $a$ do $b$.

```cpp
// Naivno rješenje
for (int i = 0; i < q; ++i) {
    long long sum = 0;
    for (int j = a; j <= b; ++j) sum += x[j]; // O(N) u najgorem slučaju
    cout << sum << "\n";
}
```

**Analiza složenosti:**

- Jedan upit: $O(N)$
- $Q$ upita: $O(N \cdot Q)$
- Uvrštavanje ograničenja: $(2 \cdot 10^5) \times (2 \cdot 10^5) = 4 \cdot 10^{10}$ operacija.
- Limit je 1 sekunda ($\approx 10^8$ operacija). Ovo je **presporo (TLE)**.

---

# Rješenje: prefiksne sume

Budući da se niz **ne mijenja** (statičan je), možemo unaprijed izračunati zbrojeve.

Definiramo niz `P` (prefiksne sume) gdje je:
$$ P[i] = x[1] + x[2] + \dots + x[i] $$
*(zbroj prvih $i$ elemenata)*.

**Rekurzivna formula:**
$$ P[i] = P[i-1] + x[i] $$
(uzimamo zbroj svega prije i dodamo trenutni element).

---

# Intuicija: oduzimanje raspona

Kako dobiti zbroj od $a$ do $b$ koristeći samo `P`?

Zbroj $[a, b]$ je zapravo:
(zbroj svega od 1 do $b$) **MANJE** (zbroj svega od 1 do $a-1$).

$$ \text{Sum}(a, b) = P[b] - P[a-1] $$

**Složenost:**

- **Izgradnja P:** $O(N)$ (jedan prolaz kroz niz).
- **Upit:** $O(1)$ (samo jedno oduzimanje).
- **Ukupno:** $O(N + Q)$. Ovo je vrlo brzo.

---

# Implementacija: detalji

1. **Indeksiranje:** zadatak koristi 1-based indeksiranje ($1 \dots N$). Najlakše je alocirati niz veličine `N+1` i postaviti `P[0] = 0`. Tako formula `P[b] - P[a-1]` radi i kada je $a=1$.
2. **Tip podataka:** maksimalni zbroj može biti $2 \cdot 10^5 \times 10^9 = 2 \cdot 10^{14}$. To ne stane u `int`. **Obavezno koristite `long long`**.

---

# Kod rješenja (C++)

```cpp
int main() {
    // Brži I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    cin >> n >> q;

    // P[i] čuva sumu x[1]...x[i], P[0] je 0
    vector<long long> P(n + 1, 0);

    for (int i = 1; i <= n; i++) {
        int x;
        cin >> x;
        P[i] = P[i-1] + x; // Trenutni prefiks = prethodni prefiks + trenutna vrijednost
    }

    while (q--) {
        int a, b;
        cin >> a >> b;
        cout << P[b] - P[a-1] << "\n"; // Formula za sumu raspona
    }

    return 0;
}
```

---

# Osvrt: Static Range Sum Queries

**Ključne lekcije**

1. **Long long:** zbroj niza od $2 \cdot 10^5$ elemenata veličine $10^9$ može biti $2 \cdot 10^{14}$. To ne stane u `int`.
2. **1-based indeksiranje:** iako C++ koristi 0-based, kod prefiksnih suma često je lakše koristiti 1-based (`P[0]=0`), kako bi formula `P[R] - P[L-1]` radila i za $L=1$ bez dodatnih `if` uvjeta.
3. **Ograničenje:** ova metoda radi isključivo za **statične** nizove. Ako se dogodi *update*, moramo ponovno izračunati cijeli niz $P$ u $O(N)$.

---

<!-- _class: title -->

# CSES: Static Range Minimum Queries

## Uvod u Sparse Table

---

# Zadatak: Static Range Minimum Queries

**Problem:**
Zadan je niz od $N$ cijelih brojeva. Trebamo odgovoriti na $Q$ upita.
Svaki upit traži **minimalnu vrijednost** u rasponu $[a, b]$.

**Ograničenja:**

- $N, Q \le 2 \cdot 10^5$.
- Niz je statičan (nema `update` operacija).

**Zašto ne prefiksne sume?**
Kod zbrajanja vrijedi `sum(a, b) = P[b] - P[a-1]`.
Kod minimuma **ne postoji inverzna operacija**. Minimum ne možemo "oduzeti".
$$ \min(a, b) \neq \text{prefMin}[b] - \text{prefMin}[a-1] $$

---

# Rješenje: Sparse Table

Za statičke upite nad operacijama kao što su `min`, `max`, `gcd` (tzv. idempotentne operacije) **Sparse Table** je najmoćnija struktura.

**Performanse:**

- **Izgradnja:** $O(N \log N)$
- **Upit:** $O(1)$ (konstantno vrijeme!)

**Ideja:**
Unaprijed izračunamo minimum za sve raspone čija je duljina **potencija broja 2**.
`st[i][j]` = minimum raspona koji počinje na indeksu `i` i ima duljinu $2^j$.

Raspon pokriven s `st[i][j]` je $[i, i + 2^j - 1]$.

---

# Izgradnja tablice (precomputation)

Koristimo dinamičko programiranje.
Raspon duljine $2^j$ možemo podijeliti na dva raspona duljine $2^{j-1}$.

**Rekurzivna veza:**
Minimum raspona duljine $2^j$ je manji od minimuma:

1. Prve polovice (duljina $2^{j-1}$, počinje na $i$)
2. Druge polovice (duljina $2^{j-1}$, počinje na $i + 2^{j-1}$)

$$ st[i][j] = \min(st[i][j-1], \quad st[i + 2^{j-1}][j-1]) $$

---

# Implementacija izgradnje

```cpp
const int MAXN = 200005;
const int K = 20;     // Dovoljno jer 2^20 > 2*10^5
int st[MAXN][K];      // Sparse Table
int logs[MAXN];       // Za brzo računanje logaritma ("log" bi se sudario sa std::log)

// 1. Inicijalizacija (bazni slučaj: duljina 2^0 = 1)
for (int i = 0; i < n; i++)
    st[i][0] = a[i];

// 2. DP gradnja
for (int j = 1; j < K; j++) {             // Za svaku potenciju j
    for (int i = 0; i + (1 << j) <= n; i++) {
        // Kombiniramo dvije polovice
        st[i][j] = min(st[i][j-1], st[i + (1 << (j-1))][j-1]);
    }
}
```

---

# Kako odgovoriti na upit u $O(1)$? (1/2)

Želimo minimum u $[L, R]$. Duljina raspona je $len = R - L + 1$.
Nađemo najveću potenciju $k$ takvu da je $2^k \le len$.

Cijeli raspon $[L, R]$ možemo pokriti s **dva preklapajuća** raspona duljine $2^k$:

1. Prvi počinje na $L$: pokriva $[L, L + 2^k - 1]$
2. Drugi završava na $R$: pokriva $[R - 2^k + 1, R]$

Budući da je $\min(A, B) = \min(A, B, B)$ (preklapanje ne smeta), rješenje je:

$$ \min(st[L][k], \quad st[R - 2^k + 1][k]) $$

---

# Kako odgovoriti na upit u $O(1)$? (2/2)

![w:900px center](../../../img/prsp/range-queries/sparse_table_overlap.png)

---

# Implementacija: priprema konstanti

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

const int MAXN = 200005; // Maksimalni N (2e5 + 5, da smo sigurni)
const int K = 20;        // Broj razina: 2^20 > 200 000 (dovoljno je i 18)

int st[MAXN][K]; // Glavna tablica
int logs[MAXN];  // Tablica za brzi logaritam
```

---

# Implementacija: glavni dio

```cpp
int main() {
    int n, q; cin >> n >> q;
    // Učitavamo i postavljamo nultu razinu (duljina 1)
    for (int i = 0; i < n; i++) cin >> st[i][0];

    // Precompute: logs[i] = floor(log2(i))
    logs[1] = 0;
    for (int i = 2; i <= n; i++) logs[i] = logs[i/2] + 1;

    // Gradimo Sparse Table
    for (int j = 1; j < K; j++)
        for (int i = 0; i + (1 << j) <= n; i++)
            st[i][j] = min(st[i][j-1], st[i + (1 << (j-1))][j-1]);

    while (q--) {
        int L, R; cin >> L >> R;
        L--; R--; // Prilagodba na 0-based indeksiranje
        int j = logs[R - L + 1];
        // O(1) upit preklapanjem
        cout << min(st[L][j], st[R - (1 << j) + 1][j]) << "\n";
    }
}
```

---

# Alternativa: segmentno stablo

Ovaj zadatak može se riješiti i **segmentnim stablom**.

- **Složenost:** $O(N)$ izgradnja, $O(\log N)$ upit.
- **Prednost:** radi i ako se niz mijenja (dinamička ažuriranja).
- **Nedostatak:** sporije od Sparse Table za statičke podatke (zbog rekurzije i $\log N$ faktora).

Za ovaj zadatak ($2 \cdot 10^5$ upita) Sparse Table je elegantnije rješenje, ali i segmentno stablo prolazi unutar limita.

---

<!-- _class: title -->

# CSES: Dynamic Range Sum Queries

## Fenwickovo stablo (Binary Indexed Tree)

---

# Zadatak: Dynamic Range Sum Queries

**Problem:**

Zadan je niz od $N$ cijelih brojeva. Trebamo obraditi $Q$ upita dva tipa:

1. **Update:** vrijednost na poziciji $k$ postaje $u$.
2. **Sum:** zbroj u rasponu $[a, b]$.

**Ograničenja:**

- $N, Q \le 2 \cdot 10^5$.
- Vremenski limit: 1 s.

**Ključna razlika od prošlog zadatka:**

Vrijednosti se **mijenjaju**.

- Prefiksne sume trebale bi $O(N)$ za svaki update $\to$ presporo ($O(NQ)$).
- Običan niz trebao bi $O(N)$ za svaki zbroj $\to$ presporo.

---

# Rješenje: Fenwickovo stablo (BIT)

Trebamo strukturu koja obje operacije (update i query) radi u **$O(\log N)$**.
Fenwickovo stablo savršen je kandidat za probleme sume.

**Ideja:**
Pamtimo parcijalne sume na indeksima definiranim binarnim zapisom broja.
Svaki indeks `i` pokriva raspon duljine $2^k$, gdje je $k$ broj nula na kraju binarnog zapisa od `i`.

**Operacije:**

- **Update:** dodajemo vrijednost na indeks `i` i sve njegove "roditelje" u BIT-u (krećemo se gore).
- **Query(i):** zbrajamo vrijednosti spuštajući se po stablu (oduzimamo LSB).

---

# Implementacija BIT-a (1-based)

Fenwick stablo prirodno radi s indeksima od 1 do $N$, što odgovara ulazu zadatka.
Kod je isti kao u uvodnom dijelu:

```cpp
vector<long long> bit;
int n;

// Dodaje 'delta' na indeks 'idx' (i na sve relevantne nad-segmente)
void update(int idx, long long delta) {
    for (; idx <= n; idx += idx & -idx)
        bit[idx] += delta;
}

// Vraća zbroj prefiksa [1, idx]
long long query(int idx) {
    long long sum = 0;
    for (; idx > 0; idx -= idx & -idx)
        sum += bit[idx];
    return sum;
}
```

---

# Zamka: "set" vs. "add"

Zadatak traži: "vrijednost na indeksu $k$ postaje $u$" (**assignment**).
BIT podržava: "dodaj $x$ na indeks $k$" (**increment**).

Kako to pomiriti?

1. Trenutno stanje niza pamtimo u običnom polju `arr`.
2. Izračunamo razliku: `diff = nova_vrijednost - stara_vrijednost`.
3. Ažuriramo BIT tom razlikom.
4. Ažuriramo `arr`.

```cpp
// Update upit: k, u
long long diff = u - arr[k];
update(k, diff);
arr[k] = u;
```

---

# Upit za raspon $[a, b]$

BIT funkcija `query(i)` vraća sumu prefiksa $[1, i]$.
Zbroj raspona $[a, b]$ dobivamo isto kao kod prefiksnih suma:

$$ \text{Sum}(a, b) = \text{query}(b) - \text{query}(a - 1) $$

---

# Potpuni kod rješenja: inicijalizacija

```cpp
#include <iostream>
#include <vector>
using namespace std;

int n;
vector<long long> bit;
vector<int> arr; // Pamtimo trenutne vrijednosti

void update(int idx, long long delta) {
    for (; idx <= n; idx += idx & -idx) bit[idx] += delta;
}

long long query(int idx) {
    long long sum = 0;
    for (; idx > 0; idx -= idx & -idx) sum += bit[idx];
    return sum;
}
```

---

# Potpuni kod rješenja

```cpp
int main() {
    int q; cin >> n >> q;
    bit.resize(n + 1, 0);
    arr.resize(n + 1);

    // Inicijalna izgradnja
    for (int i = 1; i <= n; i++) {
        cin >> arr[i];
        update(i, arr[i]);
    }

    while (q--) {
        int type; cin >> type;
        if (type == 1) { // Update
            int k, u; cin >> k >> u;
            update(k, (long long)u - arr[k]); // Dodajemo razliku
            arr[k] = u;                       // Ažuriramo lokalno polje
        } else {         // Query
            int a, b; cin >> a >> b;
            cout << query(b) - query(a - 1) << "\n";
        }
    }
}
```

---

# Alternativa: segmentno stablo

Ovaj zadatak može se riješiti i **segmentnim stablom**.

- **Prednosti:** intuitivnije za "set value" operaciju (ne treba računati razliku), lakše se proširuje na složenije upite (min/max).
- **Mane:** više koda, veća potrošnja memorije ($4N$ vs. $N$), malo sporija konstanta.

Za sumu s ažuriranjem točke **Fenwick stablo** je obično preferirani izbor u natjecateljskom programiranju zbog brzine pisanja.

---

<!-- _class: title -->

# CSES: Dynamic Range Minimum Queries

---

# Zadatak: Dynamic Range Minimum Queries

**Problem:**
Zadan je niz od $N$ cijelih brojeva. Trebamo obraditi $Q$ upita dva tipa:

1. **Update:** vrijednost na poziciji $k$ postaje $u$.
2. **Minimum:** minimalna vrijednost u rasponu $[a, b]$.

**Ograničenja:**

- $N, Q \le 2 \cdot 10^5$.
- Vremenski limit: 1 s.

**Zašto ne prethodne metode?**

- **Prefiksne sume/BIT:** operacija `min` nema inverz (minimum ne možemo "oduzeti").
- **Sparse Table:** ne podržava efikasno ažuriranje vrijednosti (zahtijeva ponovnu izgradnju).

Rješenje: **segmentno stablo**.

---

# Segmentno stablo: struktura

Segmentno stablo je binarno stablo izgrađeno nad nizom.

- **Listovi:** sadrže elemente originalnog niza.
- **Unutarnji čvorovi:** sadrže minimum svoje djece.
    `tree[v] = min(tree[2*v], tree[2*v+1])`

**Svojstva:**

- Visina stabla je $O(\log N)$.
- Svaki raspon $[a, b]$ može se rastaviti na $O(\log N)$ čvorova stabla.
- Promjena elementa utječe samo na put od lista do korijena ($O(\log N)$ čvorova).

---

# Implementacija: izgradnja (build)

Koristimo polje `tree` veličine $4N$.
Funkcija `build` rekurzivno gradi stablo.

```cpp
const int INF = 1e9 + 7;
vector<int> tree;
vector<int> arr;

// v = indeks čvora u stablu, tl/tr = granice raspona koji čvor pokriva
void build(int v, int tl, int tr) {
    if (tl == tr) {
        tree[v] = arr[tl]; // List
    } else {
        int tm = (tl + tr) / 2;
        build(2*v, tl, tm);       // Lijevo dijete
        build(2*v+1, tm+1, tr);   // Desno dijete
        // Operacija spajanja: MINIMUM
        tree[v] = min(tree[2*v], tree[2*v+1]);
    }
}
```

---

# Implementacija: ažuriranje (update)

Vrijednost na poziciji `pos` postaje `new_val`.
Tražimo put do lista koji pokriva `pos`, ažuriramo ga, a pri povratku iz rekurzije ažuriramo roditelje.

```cpp
void update(int v, int tl, int tr, int pos, int new_val) {
    if (tl == tr) {
        tree[v] = new_val; // Ažuriramo list
    } else {
        int tm = (tl + tr) / 2;
        if (pos <= tm)
            update(2*v, tl, tm, pos, new_val);
        else
            update(2*v+1, tm+1, tr, pos, new_val);

        // Ponovno računamo vrijednost roditelja
        tree[v] = min(tree[2*v], tree[2*v+1]);
    }
}
```

---

# Implementacija: upit (query)

Tražimo minimum u rasponu $[l, r]$. Ova varijanta pri spuštanju **sužava** $[l, r]$ na raspon djeteta, pa se slučaj "potpuno izvan" prepoznaje kao $l > r$:

1. Potpuno izvan ($l > r$): vraćamo neutralni element (`INF`).
2. Potpuno unutar: vraćamo vrijednost čvora.
3. Djelomično preklapanje: pozivamo rekurzivno za djecu i uzimamo `min`.

```cpp
int query(int v, int tl, int tr, int l, int r) {
    if (l > r)
        return INF;     // Neutralni element za min
    if (l == tl && r == tr)
        return tree[v]; // Potpuno preklapanje

    int tm = (tl + tr) / 2;
    return min(
        query(2*v, tl, tm, l, min(r, tm)),
        query(2*v+1, tm+1, tr, max(l, tm+1), r)
    );
}
```

---

# Glavni program

Pazite na indeksiranje! CSES koristi 1-based indekse, pa i segmentno stablo interno koristi 1-based (`tl, tr`).

```cpp
int main() {
    int n, q;
    cin >> n >> q;
    arr.resize(n + 1);
    tree.resize(4 * n + 1);
    for (int i = 1; i <= n; i++) cin >> arr[i];
    build(1, 1, n); // Korijen je 1, pokriva [1, n]
    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int k, u; cin >> k >> u;
            update(1, 1, n, k, u);
        } else {
            int a, b; cin >> a >> b;
            cout << query(1, 1, n, a, b) << "\n";
        }
    }
}
```

---

# Sažetak složenosti

Za niz veličine $N$ i $Q$ upita:

- **Build:** $O(N)$ (posjećujemo svaki čvor jednom).
- **Update:** $O(\log N)$ (visina stabla).
- **Query:** $O(\log N)$ (u najgorem slučaju posjećujemo 4 čvora po razini).

Segmentno stablo je **univerzalan alat**.
Promjenom jedne linije koda (`min` u `+`, `max`, `gcd`, `xor`) rješavamo potpuno druge probleme.

---

<!-- _class: title -->

# CSES: Range Xor Queries

## Prefiksne sume s XOR operacijom

---

# Zadatak: Range Xor Queries

**Problem:**
Zadan je niz od $N$ cijelih brojeva. Trebamo odgovoriti na $Q$ upita.
Svaki upit traži **XOR sumu** vrijednosti u rasponu $[a, b]$.
$$ x_a \oplus x_{a+1} \oplus \dots \oplus x_b $$

**Ograničenja:**

- $N, Q \le 2 \cdot 10^5$.
- Niz je statičan (nema izmjena).

**Pitanje:**
Možemo li koristiti segmentno stablo?
Da, ali to je $O(Q \log N)$. Budući da je niz statičan, možemo li brže?

---

# Svojstva XOR operacije

Prisjetimo se ključnih svojstava XOR-a ($\oplus$):

1. **Komutativnost i asocijativnost:** redoslijed nije bitan.
2. **Inverz:** broj XOR-an sam sa sobom daje 0.
    $$ A \oplus A = 0 $$
3. **Neutralni element:** $A \oplus 0 = A$.

**Zaključak:**
XOR se ponaša slično kao zbrajanje/oduzimanje.
Ako je $A \oplus B = C$, onda je $C \oplus B = A$.
Utjecaj nekog broja možemo "poništiti" ponovnim XOR-anjem.

---

# Rješenje: prefiksni XOR

Definiramo niz `P` (prefiksni XOR):
`P[i]` = $x_1 \oplus x_2 \oplus \dots \oplus x_i$

Kako dobiti XOR sumu raspona $[a, b]$?

$$ \text{XorSum}(a, b) = P[b] \oplus P[a-1] $$

**Zašto ovo radi?**
$$ P[b] = (x_1 \oplus \dots \oplus x_{a-1}) \oplus (x_a \oplus \dots \oplus x_b) $$
$$ P[a-1] = (x_1 \oplus \dots \oplus x_{a-1}) $$

U $P[b] \oplus P[a-1]$ dio $(x_1 \dots x_{a-1})$ pojavljuje se dvaput i poništava se (postaje 0), pa ostaje samo željeni raspon $(x_a \dots x_b)$.

---

# Implementacija

```cpp
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    cin >> n >> q;
    vector<int> P(n + 1, 0); // P[i] sadrži XOR sumu x[1]...x[i]

    for (int i = 1; i <= n; i++) {
        int x; cin >> x;
        P[i] = P[i-1] ^ x;
    }

    while (q--) {
        int a, b;
        cin >> a >> b;
        cout << (P[b] ^ P[a-1]) << "\n"; // O(1) upit
    }
    return 0;
}
```

---

# Što ako bi niz bio dinamičan?

Ako bi zadatak imao **update** operacije ("vrijednost na indeksu $k$ postaje ..."), prefiksni niz više ne bi bio efikasan ($O(N)$ update).

Tada bismo koristili **Fenwickovo stablo** ili **segmentno stablo**.

Jedina promjena u odnosu na "Range Sum Queries":

- Umjesto `+` koristimo `^` (XOR).
- Kod Fenwick stabla `update` operacija je: `add(k, val ^ current_val)`.

Segmentno stablo za XOR:

```cpp
tree[v] = tree[2*v] ^ tree[2*v+1]; // Merge funkcija u segmentnom stablu
```

---

# Zadatak: Hotel Queries

**Pretraživanje po segmentnom stablu (tree descent)**

**Problem:**
Imamo $N$ hotela. Za svaki hotel znamo broj slobodnih soba ($h_i$).
Dolazi $M$ grupa turista. Svaka grupa traži $r_j$ soba.
Pravilo dodjele: grupa ide u **prvi** (najljeviji) hotel koji ima **dovoljno** soba ($h_i \ge r_j$).
Nakon dodjele broj soba u tom hotelu se smanjuje.

**Ulaz:**

- $N, M \le 2 \cdot 10^5$.
- Kapaciteti do $10^9$.

**Izlaz:**

- Za svaku grupu indeks hotela (ili 0 ako nema mjesta).

---

# Zašto naivni pristup ne radi?

Za svaku grupu morali bismo prolaziti kroz hotele od 1 do $N$ dok ne nađemo prvi slobodan.

```cpp
// Naivno rješenje
for (int i = 0; i < m; ++i) {         // Za svaku grupu
    int assigned = 0;
    for (int j = 1; j <= n; ++j) {    // Prolazimo hotele
        if (hotels[j] >= required) {
            hotels[j] -= required;
            assigned = j;
            break;
        }
    }
    cout << assigned << " ";
}
```

**Složenost:** $O(N \cdot M)$. Za $N, M = 2 \cdot 10^5$ to je $4 \cdot 10^{10}$ operacija $\to$ **TLE**.
Trebamo rješenje brže od linearnog pretraživanja, idealno **$O(\log N)$** po grupi.

---

# Intuicija: max segmentno stablo (1/2)

Kako brzo naći prvi broj $\ge X$?
Ako u čvoru segmentnog stabla pamtimo **MAKSIMUM** raspona, možemo donositi odluke:

`tree[v]` = maksimalni broj slobodnih soba u rasponu koji čvor `v` pokriva.

**Logika spuštanja (tree walk):**
Stojimo u čvoru. Trebamo hotel s barem $r$ soba.

1. Ako je `tree[v] < r`, u ovom rasponu nema dovoljno velikog hotela (vraćamo 0).
2. Inače rješenje sigurno postoji. Gdje je *prvi* takav?
   - Gledamo **lijevo dijete**: ako je `tree[2*v] >= r`, rješenje je lijevo (prednost lijevom jer tražimo prvi indeks).
   - Inače rješenje mora biti **desno** (znamo da postoji u trenutnom čvoru, a nije lijevo).

---

# Intuicija: max segmentno stablo (2/2)

![w:900px center](../../../img/prsp/range-queries/segment-tree-query-decomposition.png)

---

# Hotel Queries: spuštanje po stablu

`build` i `update` su isti kao kod Dynamic Range Minimum Queries, samo s `max` umjesto `min`.

```cpp
// Vraća indeks prvog hotela s barem r slobodnih soba (0 ako ga nema)
int find_first(int v, int tl, int tr, int r) {
    if (tree[v] < r) return 0;      // Nema dovoljno velikog hotela
    if (tl == tr) return tl;        // List: to je traženi hotel

    int tm = (tl + tr) / 2;
    if (tree[2*v] >= r)             // Prednost lijevom djetetu
        return find_first(2*v, tl, tm, r);
    return find_first(2*v+1, tm+1, tr, r);
}
```

---

# Glavni program: Hotel Queries

Logika za svaku grupu:

1. Indeks hotela pronađemo pomoću `find_first`.
2. Ako postoji, smanjimo kapacitet tog hotela i ažuriramo segmentno stablo.
3. Ispišemo indeks (ili 0).

```cpp
for (int i = 0; i < m; i++) {
    int r; cin >> r;
    int h = find_first(1, 1, n, r);
    if (h != 0) {
        arr[h] -= r;
        update(1, 1, n, h, arr[h]); // Max segmentno stablo
    }
    cout << h << " ";
}
cout << "\n";
```

---

# Analiza složenosti

- **Izgradnja:** $O(N)$.
- **Upit (spuštanje):** od korijena do lista. U svakom koraku radimo jednu usporedbu i idemo lijevo ili desno. Visina stabla je $\log N$ $\to O(\log N)$.
- **Ažuriranje:** standardno $O(\log N)$.
- **Ukupno:** $O(M \log N)$.

Za $N, M = 2 \cdot 10^5$ je $\log N \approx 18$.
Ukupno je to $\approx 3,6 \cdot 10^6$ operacija, što je znatno ispod limita od $10^8$.

---

# Sažetak: segment tree walk

Ovo je moćna tehnika. Umjesto binarnog pretraživanja *nad rješenjem* ($O(\log^2 N)$) koristimo strukturu stabla za binarno pretraživanje ($O(\log N)$).

Ključni uvjeti:

1. Čvor mora sadržavati dovoljno informacija da odlučimo "lijevo" ili "desno" (ovdje: max).
2. Problem mora tražiti "prvi" ili "k-ti" element s nekim svojstvom.

---

<!-- _class: title -->

# Zaključak

## Pregled današnjih vježbi

---

# Koju strukturu odabrati?

| Struktura | Update | Query | Izgradnja | Memorija | Koristite kad... |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Prefiksne sume** | Sporo $O(N)$ | $O(1)$ | $O(N)$ | $O(N)$ | Niz je statičan, traži se suma/XOR. |
| **Sparse Table** | Nije podržan | $O(1)$ | $O(N \log N)$ | $O(N \log N)$ | Statičan niz, traži se min/max/GCD. |
| **Fenwick (BIT)** | $O(\log N)$ | $O(\log N)$ | $O(N \log N)$ | $O(N)$ | Dinamičan niz, traži se prefiksna suma. Malo koda. |
| **Segmentno stablo** | $O(\log N)$ | $O(\log N)$ | $O(N)$ | $O(N)$ (niz od $4N$) | Dinamičan niz, složeni upiti (min/max na rasponu). |