---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Podijeli pa vladaj i binarno pretraživanje"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!-- _paginate: false -->
<!-- _class: title -->

# Podijeli pa vladaj i binarno pretraživanje

## Divide and Conquer, Binary Search, BS on Answer

---

# Sadržaj

1. **Uvod i motivacija**
   - Princip "podijeli pa vladaj"
   - Binarno pretraživanje
   - Binarno pretraživanje po rješenju
2. **Primjeri zadataka**
   - Maksimalni zbroj podniza (D&C)
   - Pronalaženje fiksne točke
   - Agresivne krave (BS on Answer)
3. **Zadaci za vježbu**

---

# Princip "podijeli pa vladaj" (Divide & Conquer)

Moćna paradigma koja rješava problem u tri koraka:

1. **Podijeli (Divide):** Problem razbijemo na manje podprobleme istog tipa.
2. **Vladaj (Conquer):** Podprobleme riješimo rekurzivno (ili direktno ako su mali).
3. **Kombiniraj (Combine):** Rješenja podproblema spojimo u konačno rješenje.

**Primjeri:**

- **Merge Sort:** Niz podijelimo na pola, sortiramo polovice i spojimo sortirane nizove ($O(N \log N)$).
- **Binarno pretraživanje:** Specijalni slučaj u kojem rješavamo samo jedan podproblem.

---

# Binarno pretraživanje

Traženje elementa u **sortiranom** nizu.

1. **Podijeli:** Nađemo sredinu (`mid`).
2. **Vladaj:**
   - Ako je `arr[mid] == target` $\to$ kraj.
   - Ako je `arr[mid] > target` $\to$ tražimo lijevo.
   - Ako je `arr[mid] < target` $\to$ tražimo desno.
3. **Kombiniraj:** Nema (rezultat podproblema je rezultat cijelog problema).

**Složenost:** **$O(\log N)$**.
Svakim korakom odbacujemo polovicu prostora pretrage.

---

# Binarno pretraživanje u STL-u

Na sortiranom nizu ili `set`/`multiset` strukturi:

```cpp
vector<int> v = {1, 3, 3, 5, 8};

binary_search(v.begin(), v.end(), 3);   // true: postoji li 3?

auto lo = lower_bound(v.begin(), v.end(), 3); // prvi element >= 3 (indeks 1)
auto hi = upper_bound(v.begin(), v.end(), 3); // prvi element  > 3 (indeks 3)

int cnt = hi - lo;                       // broj pojavljivanja broja 3 (= 2)
```

Za `set` i `multiset` koristimo metode: `s.lower_bound(x)`, `s.upper_bound(x)`.
Sve su $O(\log N)$.

---

# Binarno pretraživanje po rješenju (BS on Answer)

Jedna od najkorisnijih tehnika u natjecateljskom programiranju.
Koristi se za **optimizacijske probleme** (minimizacija/maksimizacija).

**Ideja:**
Umjesto traženja optimalnog $X$, pitamo se:
> *"Je li moguće postići rješenje s vrijednošću $X$?"*

**Uvjet:** Problem mora biti **monoton**.

- Ako je moguće za $X$, moguće je i za sve manje od $X$ (ili veće, ovisno o problemu).
- To nam omogućuje binarnu pretragu po mogućim vrijednostima rješenja.

---

# Problem 1: Maksimalni zbroj podniza

**Zadatak:** Treba naći podniz s najvećim zbrojem.
*(Znamo Kadaneov algoritam $O(N)$, ali riješimo ovo D&C pristupom.)*

**Strategija ($O(N \log N)$):**
Maksimalni podniz se nalazi ili:

1. Potpuno u **lijevoj** polovici.
2. Potpuno u **desnoj** polovici.
3. **Prelazi preko sredine** (dio lijevo + dio desno).

Rješenje je `max(Lijevo, Desno, Crossing)`.

---

# Max Subarray Sum: podniz preko sredine

```cpp
long long maxCrossingSum(const vector<int>& arr, int l, int m, int r) {
    long long sum = 0, left_sum = LLONG_MIN;
    for (int i = m; i >= l; i--) { // Od sredine nalijevo
        sum += arr[i];
        left_sum = max(left_sum, sum);
    }

    sum = 0;
    long long right_sum = LLONG_MIN;
    for (int i = m + 1; i <= r; i++) { // Od sredine nadesno
        sum += arr[i];
        right_sum = max(right_sum, sum);
    }
    return left_sum + right_sum;
}
```

Podniz koji prelazi sredinu mora sadržavati `arr[m]` i `arr[m+1]`.

---

# Max Subarray Sum: rekurzija

```cpp
long long maxSubarraySum(const vector<int>& arr, int l, int r) {
    if (l == r) return arr[l]; // Bazni slučaj: jedan element

    int m = l + (r - l) / 2;
    return max({
        maxSubarraySum(arr, l, m),      // Lijevo
        maxSubarraySum(arr, m + 1, r),  // Desno
        maxCrossingSum(arr, l, m, r)    // Preko sredine
    });
}
```

Svaka razina rekurzije radi $O(N)$ posla, a razina ima $O(\log N)$ $\Rightarrow$ $O(N \log N)$.

---

# Problem 2: Fiksna točka

**Zadatak:** Zadan je sortiran niz različitih cijelih brojeva (indeksi od 0). Treba naći indeks $i$ takav da je $A[i] = i$.

**Analiza:**
Definirajmo $B[i] = A[i] - i$. Tražimo $i$ takav da je $B[i] = 0$.
Kako su elementi $A$ različiti cijeli brojevi i sortirani, niz $A$ raste barem za 1 u svakom koraku.
$\implies B$ je **monotono neopadajući**.
Možemo koristiti binarno pretraživanje na $B$ (implicitno).

---

# Fiksna točka: Implementacija

```cpp
int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;

    int l = 0, r = n - 1, ans = -1;

    while (l <= r) {
        int mid = l + (r - l) / 2;

        if (a[mid] == mid) {
            ans = mid;
            break; // Našli smo!
        } else if (a[mid] > mid) {
            // Vrijednost je prevelika, rješenje mora biti lijevo
            // (indeks raste sporije od vrijednosti)
            r = mid - 1;
        } else {
            // Vrijednost je premala, rješenje mora biti desno
            l = mid + 1;
        }
    }
    cout << ans << "\n";
}
```

---

# Problem 3: Agresivne krave (Aggressive Cows)

**Zadatak:** Imamo $N$ štala na pozicijama $x_1, \dots, x_N$ i $C$ krava.
Krave treba rasporediti u štale tako da je **minimalna udaljenost** između bilo koje dvije krave **maksimalna**.

**Pristup (BS on Answer):**
Umjesto traženja udaljenosti, pitamo se:
> *"Možemo li smjestiti $C$ krava tako da je razmak barem $D$?"*

Ako možemo s razmakom $D$, probamo veći. Ako ne možemo, probamo manji.

*Zadatak je na SPOJ-u: [AGGRCOW](https://www.spoj.com/problems/AGGRCOW/) (ulaz ima više test primjera).*

---

# Provjera rješenja (Greedy Check)

Funkcija `check(d)` vraća `true` ako možemo postaviti krave s razmakom $\ge d$.

```cpp
bool check(long long d, int c, const vector<int>& stalls) {
    int cows_placed = 1;
    int last_pos = stalls[0]; // Prvu kravu uvijek stavimo u prvu štalu

    for (size_t i = 1; i < stalls.size(); ++i) {
        if (stalls[i] - last_pos >= d) {
            cows_placed++;
            last_pos = stalls[i];
        }
    }
    return cows_placed >= c;
}
```

*Napomena: štale moraju biti sortirane!*

---

# Agresivne krave: glavna petlja

```cpp
int main() {
    int n, c; cin >> n >> c;
    vector<int> stalls(n);
    for (int i = 0; i < n; ++i) cin >> stalls[i];

    sort(stalls.begin(), stalls.end()); // Obavezno sortiranje

    long long l = 0, r = 1e9, ans = 0;

    while (l <= r) {
        long long mid = l + (r - l) / 2;

        if (check(mid, c, stalls)) {
            ans = mid;   // Ovo je moguće rješenje, spremamo ga
            l = mid + 1; // Pokušavamo naći veće
        } else {
            r = mid - 1; // Razmak je prevelik, smanjujemo
        }
    }
    cout << ans << "\n";
}
```

Složenost: $O(N \log D)$, gdje je $D$ najveća moguća udaljenost.

---

# Zadaci za vježbu

**CSES Problem Set**

1. **[Sum of Two Values](https://cses.fi/problemset/task/1640):** Dva broja koja daju zbroj $X$ (sortiranje + binarno pretraživanje ili dva pokazivača).
2. **[Factory Machines](https://cses.fi/problemset/task/1620):** Minimalno vrijeme za proizvodnju $t$ proizvoda (BS on Answer).
3. **[Towers](https://cses.fi/problemset/task/1073):** Slaganje tornjeva (`upper_bound` na `multiset`).

**Codeforces**

- Pretražite tagove: `binary search`, `divide and conquer`.
- Zadaci težine 800-1200 za početak.

---

<!-- _class: title -->
# Sum of Two Values (CSES)

## Two Pointers ili Binary Search

---

# Analiza: Sum of Two Values

**Problem:**
Zadan je niz od $n$ cijelih brojeva i ciljni zbroj $x$.
Treba pronaći **indekse** dva broja čiji je zbroj točno $x$.

**Pristup 1: sortiranje + binarno pretraživanje**

1. Spremimo parove `{vrijednost, originalni_indeks}` i sortiramo ih.
2. Za svaki element $a$ tražimo $x - a$ u ostatku niza binarnim pretraživanjem.

**Pristup 2: dva pokazivača**

1. Sortiramo niz i postavimo $L=0$, $R=N-1$.
2. Ako je $A[L] + A[R] = x$, našli smo par.
3. Ako je $A[L] + A[R] < x \implies L$++, a ako je $> x \implies R$--.

Oba pristupa su $O(N \log N)$ zbog sortiranja.

---

# Implementacija: Sum of Two Values

```cpp
int n, target; cin >> n >> target;
vector<pair<int, int>> a(n);
for (int i = 0; i < n; ++i) {
    cin >> a[i].first;
    a[i].second = i + 1; // 1-based indeksiranje
}
sort(a.begin(), a.end());

int l = 0, r = n - 1;
while (l < r) {
    int sum = a[l].first + a[r].first;
    if (sum == target) {
        cout << a[l].second << " " << a[r].second << "\n";
        return 0;
    }
    if (sum < target) l++;
    else r--;
}
cout << "IMPOSSIBLE" << "\n";
```

---

<!-- _class: title -->
# Factory Machines (CSES)

## Binarno pretraživanje po rješenju

---

# Analiza: Factory Machines

**Problem:**
Imamo $n$ strojeva. Stroj $i$ treba $k_i$ sekundi za jedan proizvod.
Koliko je minimalno vremena potrebno za proizvodnju $t$ proizvoda?

**Intuicija (BS on Answer):**
Ako možemo proizvesti $t$ proizvoda u vremenu $T$, možemo i u vremenu $T+1$.
Funkcija "možemo li proizvesti" je monotona.

**Check funkcija:**
Za zadano vrijeme `time` stroj $i$ proizvede $\lfloor \text{time} / k_i \rfloor$ proizvoda.
Ukupno proizvoda $= \sum \lfloor \text{time} / k_i \rfloor$.
Pazite na overflow: čim suma dosegne $t$, prekidamo zbrajanje.

---

# Implementacija: Factory Machines

```cpp
long long n, t; cin >> n >> t;
vector<long long> k(n);
for (int i = 0; i < n; ++i) cin >> k[i];

long long l = 0, r = 1e18, ans = 1e18; // 1e18 je sigurna gornja granica

while (l <= r) {
    long long mid = l + (r - l) / 2;
    long long products = 0;
    for (long long x : k) {
        products += mid / x;
        if (products >= t) break; // Optimizacija i zaštita od overflowa
    }

    if (products >= t) {
        ans = mid;
        r = mid - 1;
    } else {
        l = mid + 1;
    }
}
cout << ans << "\n";
```

---

<!-- _class: title -->
# Towers (CSES)

## Pohlepni pristup s multisetom

---

# Analiza: Towers

**Problem:**
Kocke dolaze jedna po jedna (veličine se mogu ponavljati). Kocku veličine $X$ možemo staviti na vrh postojećeg tornja ako je vrh tog tornja **strogo veći** od $X$.
Inače započinjemo novi toranj. Treba minimizirati broj tornjeva.

**Intuicija:**
Pohlepno: kocku $X$ stavljamo na toranj čiji je vrh **najmanji mogući, ali strogo veći od $X$**.
Zašto? Čuvamo velike vrhove za velike kocke koje dolaze kasnije.
Trebamo strukturu koja podržava:

1. Pronalazak najmanjeg elementa $> X$.
2. Brisanje tog elementa i ubacivanje $X$.

Koristimo `std::multiset` i `upper_bound` (ne `lower_bound`, jer jednaku kocku ne smijemo staviti na vrh).

---

# Implementacija: Towers

```cpp
int n; cin >> n;
multiset<int> towers;

for (int i = 0; i < n; ++i) {
    int x; cin >> x;

    // upper_bound vraća iterator na prvi element strogo veći od x
    auto it = towers.upper_bound(x);

    if (it == towers.end()) {
        // Nema većeg elementa -> novi toranj
        towers.insert(x);
    } else {
        // Našli smo toranj -> mijenjamo vrh
        towers.erase(it);
        towers.insert(x);
    }
}
cout << towers.size() << "\n";
```

---

<!-- _class: lead -->

# Pitanja?

Sljedeća lekcija: Uvod u dinamičko programiranje
