---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Teorija brojeva i kombinatorika"
footer: "Programiranje za rješavanje složenih problema | Vježbe 2025/26"
---

# 1. Vizualizacija Sita Eratostena

Tekstualni opis križanja brojeva je teško pratiti. Animacija ili slika rešetke brojeva je ovdje obavezna.

* **Gdje ubaciti:** Slajd **"Sito Eratostena (Sieve of Eratosthenes)"**.
* **Što tražiti:** Tablica brojeva gdje su višekratnici broja 2, 3, 5 obojani različitim bojama.
* **Ključne riječi za pretragu:** `Sieve of Eratosthenes animation gif` ili `Sieve of Eratosthenes grid visualization`.
    ```markdown
    ![bg right:40% fit](https://upload.wikimedia.org/wikipedia/commons/b/b9/Sieve_of_Eratosthenes_animation.gif)
    ```
    *(Ovaj link s Wikipedije je klasik i odlično radi).*

### 2. Geometrijski prikaz Euklidovog algoritma (GCD)

GCD nije samo formula; to je način popločavanja pravokutnika kvadratima. Ovo je fantastična intuicija koju mnogi studenti nikad ne vide.

* **Gdje ubaciti:** Slajd **"Euklidov algoritam"**.
* **Što tražiti:** Pravokutnik dimenzija $a \times b$ koji se dijeli na kvadrate dok ne ostane najmanji zajednički kvadrat.
* **Ključne riječi:** `Euclidean algorithm geometry rectangle tiling`.
    *(Ili potraži sliku "Euclidean tiling animation").*

### 3. Modularna aritmetika kao sat

Najbolja analogija za modulo je sat. $13 \pmod{12} = 1$.

* **Gdje ubaciti:** Slajd **"Pravila modularne aritmetike"** ili naslovni slajd te sekcije.
* **Što tražiti:** Krug s brojevima (poput sata) koji prikazuje cikličnost.
* **Ključne riječi:** `Modular arithmetic clock cycle visualization`.

### 4. Pascalov trokut (Binomni koeficijenti)

Teško je pričati o $\binom{n}{k}$ bez prikaza trokuta.

* **Gdje ubaciti:** Slajd **"Binomni koeficijenti (n povrh k)"**.
* **Što tražiti:** Pascalov trokut gdje se vidi da je broj zbroj dva broja iznad njega.
* **Ključne riječi:** `Pascal triangle binomial coefficients`.

### 5. Vizualizacija Catalanovih brojeva

Budući da spominješ triangulaciju poligona i zagrade, slika koja to povezuje je zlata vrijedna.

* **Gdje ubaciti:** Slajd **"Catalanovi brojevi"**.
* **Što tražiti:** Prikaz triangulacije šesterokuta ili balansiranih zagrada.
* **Ključne riječi:** `Catalan numbers polygon triangulation example`.

### 6. Vennov dijagram (Uključivanje-Isključivanje)

Formula izgleda komplicirano, ali slika s tri kruga koja se preklapaju sve objašnjava.

slika
https://media.geeksforgeeks.org/wp-content/uploads/Screen-Shot-2018-03-14-at-5.30.27-PM.png

izvor
https://www.geeksforgeeks.org/competitive-programming/inclusion-exclusion-principle-for-competitive-programming/

* **Gdje ubaciti:** Slajd **"Princip uključivanja-isključivanja"**.
* **Što tražiti:** Vennov dijagram za 3 skupa s obojanim presjecima.
* **Ključne riječi:** `Inclusion-exclusion principle venn diagram 3 sets`.

### 7. Stars and Bars (Zadatak Distributing Apples)

Ovo je najteži koncept za vizualizirati mentalno. Slika je nužna.

* **Gdje ubaciti:** Slajd **"Analiza: Distributing Apples"** (kod dijela "Intuicija").
* **Što tražiti:** Dijagram koji prikazuje zvjezdice (predmete) i vertikalne crte (pregrade).
* **Ključne riječi:** `Stars and bars combinatorics diagram`.
* **Marp kod:**

    ```markdown
    ![bg right:50% fit](https://upload.wikimedia.org/wikipedia/commons/thumb/e/cd/Stars_and_bars.png/440px-Stars_and_bars.png)
    ```

---

---

<!-- _class: title -->
# Teorija brojeva i kombinatorika

Programiranje za rješavanje složenih problema

---

# Sadržaj

1. **Uvod i Motivacija**
   * Zašto su nam potrebni brojevi?
   * Izazovi: Veliki brojevi i efikasnost
2. **Osnovna Teorija Brojeva**
   * Prosti brojevi, GCD, Modularna aritmetika
3. **Osnove Kombinatorike**
   * Binomni koeficijenti, Catalanovi brojevi
   * Princip uključivanja-isključivanja
4. **Zadaci za vježbu**

---

<!-- _class: lead -->
# Uvod i motivacija

---

# Zašto su nam potrebni brojevi i prebrojavanje?

Teorija brojeva i kombinatorika su temelji diskretne matematike i "kralježnica" mnogih algoritamskih problema.

* **Teorija brojeva:**
  * Bavi se svojstvima cijelih brojeva.
  * Ključni pojmovi: prostost, djeljivost, modularna aritmetika.
  * Primjena: Kriptografija, hashing, optimizacija petlji.
* **Kombinatorika:**
  * Umjetnost prebrojavanja.
  * Klasično pitanje: *"Na koliko načina se nešto može dogoditi?"*
  * Primjena: Izračun složenosti, vjerojatnost, broj puteva u grafu.

---

# Izazovi: Veliki brojevi i efikasnost

U natjecateljskom programiranju susrećemo se s dva glavna problema:

1. **Veliki brojevi (Overflow):**
   * Rezultati često premašuju `long long` ($2^{63}-1$).
   * Rješenje: Računanje **modulo** neki veliki prosti broj (npr. $10^9 + 7$).
   * Zato je **modularna aritmetika** ključna vještina.

2. **Efikasnost (Time Limit):**
   * Naivno prebrojavanje ili provjera djeljivosti je prespora za $N=10^9$ ili $10^{18}$.
   * Rješenje: Pametni algoritmi ($O(\log N)$ ili $O(\sqrt{N})$).
   * Primjeri: Euklidov algoritam, brzo potenciranje.

---

# Preporučena literatura

Za dublje razumijevanje i dodatne zadatke:

* **CPH (Competitive Programmer's Handbook):**
  * Poglavlje 21: *Number theory*
  * Poglavlje 22: *Combinatorics*
* **CLRS (Introduction to Algorithms):**
  * Poglavlje 31: *Number-Theoretic Algorithms*

---

<!-- _class: lead -->
# Osnovna Teorija Brojeva

## Prosti brojevi i faktorizacija

---

# Prosti brojevi

**Definicije:**

* **Prosti broj:** Cijeli broj $n > 1$ djeljiv samo s 1 i samim sobom.
* **Faktorizacija:** Svaki broj $n > 1$ ima **jedinstven** rastav na proste faktore.
  * Primjer: $60 = 2^2 \cdot 3 \cdot 5$

**Kako brzo pronaći proste brojeve?**

* Provjera jednog broja: $O(\sqrt{n})$.
* Pronalaženje svih prostih do $N$: **Sito Eratostena**.

---

# Sito Eratostena (Sieve of Eratosthenes)

**Ideja:** Eliminacija višekratnika.

1. Kreni od 2 (prvi prosti).
2. Označi sve njegove višekratnike ($4, 6, 8, \dots$) kao složene.
3. Nađi idući neoznačeni broj (3) – on je prost. Označi njegove višekratnike ($6, 9, 12 \dots$).
4. Ponavljaj postupak.

**Složenost:** $O(N \log \log N)$ – gotovo linearno!

---

# Implementacija Sita (C++)

```cpp
const int MAXN = 1e6;
vector<bool> is_prime(MAXN + 1, true);

void sieve() {
    is_prime[0] = is_prime[1] = false; // 0 i 1 nisu prosti
    
    for (int p = 2; p * p <= MAXN; ++p) {
        // Ako p nije prekrižen, onda je prost
        if (is_prime[p]) {
            // Prekriži sve višekratnike od p
            // Optimizacija: krećemo od p*p
            for (int i = p * p; i <= MAXN; i += p)
                is_prime[i] = false;
        }
    }
}
```

---

<!-- _class: lead -->
# Najveći zajednički djelitelj (GCD)

---

# Euklidov algoritam

Najefikasniji način za računanje `gcd(a, b)` (Greatest Common Divisor).

**Matematička podloga:**
$$ \gcd(a, b) = \gcd(b, a \pmod b) $$
Bazni slučaj: $\gcd(a, 0) = a$.

**Implementacija:**

```cpp
int gcd(int a, int b) {
    while (b) {
        a %= b;
        swap(a, b);
    }
    return a;
}
```

**Složenost:** $O(\log(\min(a, b)))$.
*Napomena:* U C++17 postoji `std::gcd(a, b)` u `<numeric>`.

---

<!-- _class: lead -->
# Modularna Aritmetika

---

# Pravila modularne aritmetike

Kada radimo s velikim brojevima, zanimaju nas samo ostaci pri dijeljenju s $M$.

Osnovna svojstva:

1. **Zbrajanje:** $(a + b) \pmod M = ((a \pmod M) + (b \pmod M)) \pmod M$
2. **Množenje:** $(a \cdot b) \pmod M = ((a \pmod M) \cdot (b \pmod M)) \pmod M$
3. **Oduzimanje (PAZI!):**
   $$ (a - b) \pmod M = ((a \pmod M) - (b \pmod M) + M) \pmod M $$
   *Dodajemo $M$ prije modula da izbjegnemo negativne rezultate!*

---

# Modularno potenciranje (Binary Exponentiation)

**Problem:** Izračunati $a^b \pmod M$ za veliki $b$ (npr. $10^{18}$).

* Naivno množenje: $O(b)$ $\rightarrow$ Presporo (TLE).
* Binarno potenciranje: $O(\log b)$ $\rightarrow$ Trenutačno.

**Ideja (Podijeli pa vladaj):**

* Ako je $b$ paran: $a^b = (a^{b/2})^2$
* Ako je $b$ neparan: $a^b = a \cdot a^{b-1}$

---

# Implementacija potenciranja

```cpp
const long long MOD = 1e9 + 7;

long long power(long long base, long long exp) {
    long long res = 1;
    base %= MOD;
    
    while (exp > 0) {
        // Ako je eksponent neparan, pomnoži rezultat s bazom
        if (exp % 2 == 1) res = (res * base) % MOD;
        
        // Kvadriraj bazu za idući korak
        base = (base * base) % MOD;
        exp /= 2;
    }
    return res;
}
```

---

# Modularni inverz

Kod realnih brojeva, dijeljenje je množenje recipročnom vrijednošću ($a / b = a \cdot b^{-1}$).
U modularnoj aritmetici ne postoji "dijeljenje", ali postoji **modularni inverz**.

Tražimo broj $x$ takav da:
$$ a \cdot x \equiv 1 \pmod M $$
Zapisujemo ga kao $a^{-1}$.

**Mali Fermatov teorem:**
Ako je $M$ prost broj, vrijedi:
$$ a^{M-2} \equiv a^{-1} \pmod M $$

Dakle, inverz računamo pomoću funkcije `power(a, M-2)`.

---

<!-- _class: lead -->
# Osnove kombinatorike

## Binomni koeficijenti

---

# Binomni koeficijenti (n povrh k)

Broj načina za odabir $k$ elemenata iz skupa od $n$ elemenata.

**Formula:**
$$ \binom{n}{k} = \frac{n!}{k!(n-k)!} $$

**Problem:** Faktorijeli brzo postaju ogromni.
**Rješenja:**

1. **Paskalov trokut (DP):** $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$. Dobro za manje $N$.
2. **Faktorijeli + Inverzi:** Za velike $N$ uz modulo $M$.
   $$ \binom{n}{k} \pmod M = (n! \cdot (k!)^{-1} \cdot ((n-k)! )^{-1}) \pmod M $$

---

# Implementacija nCk (s inverzima)

```cpp
// Pretpostavka: fact[] i invFact[] su već predračunati 
// do MAXN koristeći modularno potenciranje

long long nCk(int n, int k, long long MOD) {
    if (k < 0 || k > n) return 0;
    
    // Formula: n! * inv(k!) * inv((n-k)!)
    return fact[n] * invFact[k] % MOD * invFact[n - k] % MOD;
}
```

*Ovaj pristup omogućuje odgovaranje na upite u $O(1)$ vremenu.*

---

# Catalanovi brojevi

Niz prirodnih brojeva koji se pojavljuje u raznim problemima prebrojavanja.
$$ C_n = \frac{1}{n+1} \binom{2n}{n} $$

**Primjeri primjene:**

1. Broj ispravnih izraza s $n$ parova zagrada: `((()))`, `()(())`...
2. Broj načina za triangulaciju konveksnog poligona s $n+2$ vrhova.
3. Broj binarnih stabala s $n$ čvorova.

---

# Princip uključivanja-isključivanja

Koristi se za prebrojavanje elemenata unije skupova.

**Formula za 2 skupa:**
$$ |A \cup B| = |A| + |B| - |A \cap B| $$

**Formula za 3 skupa:**
$$ |A \cup B \cup C| = |A| + |B| + |C| - (|A \cap B| + \dots) + |A \cap B \cap C| $$

**Primjer:** Koliko brojeva od 1 do $n$ je djeljivo s $p$ ili $q$?
$$ \text{Rezultat} = \lfloor \frac{n}{p} \rfloor + \lfloor \frac{n}{q} \rfloor - \lfloor \frac{n}{\text{lcm}(p, q)} \rfloor $$

---

<!-- _class: lead -->
# Zadaci za vježbu (CSES)

### Zadaci za početak i srednju razinu

* [Exponentiation I](<https://cses.fi/problemset/task/1095>)
* [Exponentiation II](<https://cses.fi/problemset/task/1712>)
* [Counting Divisors](<https://cses.fi/problemset/task/1713>)
* [Common Divisors](<https://cses.fi/problemset/task/1081>)
* [Binomial Coefficients](<https://cses.fi/problemset/task/1079>)
* [Creating Strings II](<https://cses.fi/problemset/task/1715>)
* [Distributing Apples](<https://cses.fi/problemset/task/1716>)

---

<!-- _class: lead -->
# [Exponentiation I](<https://cses.fi/problemset/task/1095>)

---

# Analiza: Exponentiation I

**Problem:** Izračunati $a^b \pmod{10^9 + 7}$.
**Ograničenja:** $a, b \le 10^9$, broj upita $n \le 2 \cdot 10^5$.

### Intuicija

1. **Naivni pristup:** Množenje u petlji `for (i=0; i<b; ++i)` ima složenost $O(b)$.
   * Ako je $b = 10^9$, ovo je presporo (TLE) jer imamo puno upita.
2. **Binarno potenciranje:**
   * Koristimo svojstvo:
     $$ a^b = \begin{cases} (a^{b/2})^2 & \text{ako je } b \text{ paran} \\ a \cdot a^{b-1} & \text{ako je } b \text{ neparan} \end{cases} $$
   * **Složenost:** $O(\log b)$. Za $b=10^9$, to je oko 30 operacija.

---

# Implementacija: Funkcija za potenciranje

```cpp
const long long MOD = 1e9 + 7;

long long binpow(long long base, long long exp) {
    long long res = 1;
    base %= MOD; // Osiguraj da je baza unutar modula
    
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % MOD; // Ako je bit 1, pomnoži
        
        base = (base * base) % MOD; // Kvadriraj bazu
        exp /= 2;                   // Pomakni bitove udesno (dijeli s 2)
    }
    return res;
}
```

---

# Rješenje: Exponentiation I

```cpp
#include <iostream>

using namespace std;

const long long MOD = 1e9 + 7;

// ... (funkcija binpow s prethodnog slajda) ...

void solve() {
    long long a, b;
    cin >> a >> b;
    cout << binpow(a, b) << "\n";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n;
    cin >> n;
    while(n--) {
        solve();
    }
    return 0;
}
```

---

<!-- _class: lead -->
# [Exponentiation II](<https://cses.fi/problemset/task/1712>)

---

# Analiza: Exponentiation II

**Problem:** Izračunati $a^{b^c} \pmod{10^9 + 7}$.
**Ograničenja:** $a, b, c \le 10^9$.

## Intuicija: Fermatov mali teorem

Želimo izračunati $a^X \pmod M$, gdje je $X = b^c$.
Eksponent $X$ može biti ogroman, ali nas zanima samo njegov ostatak.
**Važno pravilo:** U eksponentu ne računamo $\pmod M$, već $\pmod{M-1}$!

$$ a^{b^c} \equiv a^{b^c \pmod{M-1}} \pmod M $$

*Uvjet:* $M$ mora biti prost broj (što $10^9+7$ jest).

---

# Ključni dio koda: Dva modula

```cpp
const long long MOD = 1e9 + 7;

// Pazi: exponent se računa modulo (MOD - 1)
long long exponent_mod = MOD - 1;

long long solve(long long a, long long b, long long c) {
    
    // 1. Izračunaj eksponent: exp = b^c % (MOD - 1)
    long long exp = binpow(b, c, exponent_mod);
    
    // 2. Izračunaj konačni rezultat: a^exp % MOD
    
    long long res = binpow(a, exp, MOD);
    
    return res;
}
```

*Napomena: Funkciju `binpow` moramo prilagoditi da prima proizvoljan modul.*

---

# Rješenje: Exponentiation II

```cpp
#include <iostream>
using namespace std;

long long binpow(long long base, long long exp, long long mod) {
    long long res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % mod;
        base = (base * base) % mod;
        exp /= 2;
    }
    return res;
}

int main() {
    int n;
    cin >> n;
    while(n--) {
        long long a, b, c;
        cin >> a >> b >> c;
        long long exponent_part = binpow(b, c, 1e9 + 6); // MOD - 1
        cout << binpow(a, exponent_part, 1e9 + 7) << "\n";
    }
    return 0;
}
```

---

<!-- _class: lead -->
# [Counting Divisors](<https://cses.fi/problemset/task/1713>)

---

# Analiza: Counting Divisors

**Problem:** Za $n$ brojeva $x$, ispiši broj njihovih djelitelja.
**Ograničenja:** $n \le 10^5, x \le 10^6$.

### Intuicija

1. **Pristup A (Iteracija):** Za svaki $x$ provjerimo sve brojeve do $\sqrt{x}$.
   * Složenost po upitu: $O(\sqrt{x}) \approx 1000$.
   * Ukupno: $10^5 \times 1000 = 10^8$. Ovo prolazi unutar 1 sekunde u C++.

2. **Pristup B (Sito - brže):** Predračunamo najmanji prosti faktor (SPF) za svaki broj do $10^6$.
   * Faktorizacija broja $x$ traje $O(\log x)$.
   * Ako je $x = p_1^{a_1} p_2^{a_2} \dots$, broj djelitelja je $(a_1+1)(a_2+1)\dots$

---

# Kod: Pristup A (Dovoljno brz i jednostavan)

```cpp
int countDivisors(int x) {
    int divisors = 0;
    // Idemo samo do korijena iz x
    for (int i = 1; i * i <= x; i++) {
        if (x % i == 0) {
            // Ako je i * i == x, imamo samo jedan djelitelj (npr. 3*3=9)
            if (i * i == x) divisors++;
            // Inače imamo par (npr. 12: 3 i 4)
            else divisors += 2;
        }
    }
    return divisors;
}
```

---

# Rješenje: Counting Divisors

```cpp
#include <iostream>
using namespace std;

void solve() {
    int x;
    cin >> x;
    int cnt = 0;
    for (int i = 1; i * i <= x; i++) {
        if (x % i == 0) {
            cnt++; // i je djelitelj
            if (i * i != x) {
                cnt++; // x/i je također djelitelj
            }
        }
    }
    cout << cnt << "\n";
}

int main() {
    ios_base::sync_with_stdio(false); // Obavezno za brzi I/O
    cin.tie(NULL);
    int n;
    cin >> n;
    while(n--) solve();
    return 0;
}
```

---

<!-- _class: lead -->
# [Common Divisors](<https://cses.fi/problemset/task/1081>)

---

# Analiza: Common Divisors

**Problem:** Nađi najveći zajednički djelitelj (GCD) nekog para brojeva u nizu.
**Ograničenja:** $n \le 2 \cdot 10^5, x_i \le 10^6$.

### Intuicija

1. **Naivno:** Isprobati sve parove ($O(N^2)$). Presporo!
2. **Obrnuti pristup:** Umjesto da tražimo GCD parova, pitajmo se: **Koji je najveći broj $g$ koji dijeli barem dva broja u nizu?**
   * Raspon vrijednosti je do $10^6$ (nazovimo to $MAX$).
   * Krenemo od $g = MAX$ prema dolje ($10^6, 999999, \dots$).
   * Za svaki $g$, prebrojimo njegove višekratnike u nizu. Ako ih je $\ge 2$, to je rješenje!

---

# Ključni dio koda: Frequency Array

Koristimo niz `cnt` gdje `cnt[x]` govori koliko puta se broj `x` pojavljuje u ulazu.

```cpp
// Iteriramo kroz moguće GCD-ove od najvećeg prema 1
for (int gcd = 1000000; gcd >= 1; gcd--) {
    int multiples = 0;
    
    // Brojimo višekratnike od 'gcd' u nizu: gcd, 2*gcd, 3*gcd...
    for (int j = gcd; j <= 1000000; j += gcd) {
        multiples += cnt[j]; // Dodaj koliko puta se taj višekratnik pojavljuje
    }
    
    // Ako smo našli barem dva broja kojima je 'gcd' djelitelj
    if (multiples >= 2) {
        cout << gcd << endl;
        return 0;
    }
}
```

**Složenost:** $O(MAX \log MAX)$ zbog harmonijskog reda ($N/1 + N/2 + \dots$).

---

# Rješenje: Common Divisors

```cpp
#include <iostream>
#include <vector>
using namespace std;

const int MAX_VAL = 1000000;
int cnt[MAX_VAL + 1]; // Globalni niz je automatski nula

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        cnt[x]++;
    }

    for (int g = MAX_VAL; g >= 1; g--) {
        int multiples = 0;
        for (int j = g; j <= MAX_VAL; j += g) {
            multiples += cnt[j];
        }
        if (multiples >= 2) {
            cout << g << endl;
            return 0;
        }
    }
    return 0;
}
```

---

<!-- _class: lead -->
# [Binomial Coefficients](<https://cses.fi/problemset/task/1079>)

---

# Analiza: Binomial Coefficients

**Problem:** Izračunati $\binom{n}{k} \pmod{10^9 + 7}$ za mnogo upita.
**Ograničenja:** $n \le 10^6$, $10^5$ upita.

### Intuicija

Formula je $\binom{n}{k} = \frac{n!}{k!(n-k)!}$.
Trebamo ovo računati modulo $10^9+7$. Dijeljenje nije dozvoljeno, pa množimo s modularnim inverzom:
$$ \binom{n}{k} = n! \cdot (k!)^{-1} \cdot ((n-k)! )^{-1} \pmod M $$

**Strategija:**

1. Predračunaj faktorijele (`fact`) do $10^6$.
2. Predračunaj inverzne faktorijele (`invFact`) koristeći Fermatov teorem ($x^{MOD-2}$).

---

# Ključni dio koda: Predračun (Precomputation)

```cpp
long long fact[MAXN], invFact[MAXN];

// Funkcija za modularno potenciranje (za inverze)
long long power(long long base, long long exp) { ... }

// Inverz od n! je zapravo (n!)^(MOD-2)
long long inverse(long long n) {
    return power(n, MOD - 2);
}

void precompute() {
    fact[0] = 1;
    invFact[0] = 1;
    for (int i = 1; i < MAXN; i++) {
        fact[i] = (fact[i - 1] * i) % MOD;
        invFact[i] = inverse(fact[i]); // Može se optimizirati, ali ovo je OK
    }
}
```

---

# Rješenje: Binomial Coefficients

```cpp
#include <iostream>
using namespace std;

const int MAXN = 1000005;
const int MOD = 1e9 + 7;
long long fact[MAXN], invFact[MAXN];

long long power(long long base, long long exp) { /* Implementacija binpow */ }
long long inverse(long long n) { return power(n, MOD - 2); }

void precompute() {
    fact[0] = 1;
    invFact[0] = 1;
    for (int i = 1; i < MAXN; i++) {
        fact[i] = (fact[i - 1] * i) % MOD;
        // invFact se može računati i u O(N) unazad, ali O(N log MOD) je dovoljno brzo ovdje
        invFact[i] = inverse(fact[i]); 
    }
}

long long nCk(int n, int k) {
    if (k < 0 || k > n) return 0;
    return fact[n] * invFact[k] % MOD * invFact[n - k] % MOD;
}
// U main-u pozvati precompute() pa rješavati upite nCk(n, k)
```

---

<!-- _class: lead -->
# [Creating Strings II](<https://cses.fi/problemset/task/1715>)

[Link na zadatak](https://cses.fi/problemset/task/1715)

---

# Analiza: Creating Strings II

**Problem:** Koliko različitih stringova se može dobiti permutiranjem slova u zadanom stringu?
**Ulaz:** String (npr. "aabac").

### Intuicija

Ovo su **permutacije s ponavljanjem**.
Ako string ima duljinu $N$ i slova se pojavljuju $c_a, c_b, \dots, c_z$ puta, formula je:

$$ \text{Rezultat} = \frac{N!}{c_a! \cdot c_b! \cdot \dots \cdot c_z!} $$

To je isto kao:
$$ N! \cdot (c_a!)^{-1} \cdot (c_b!)^{-1} \dots $$

---

# Rješenje: Creating Strings II

Koristimo istu logiku s faktorijelima kao u prethodnom zadatku.

```cpp
int main() {
    precompute(); // Ista funkcija kao u Binomial Coefficients
    
    string s;
    cin >> s;
    
    int cnt[26] = {0}; // Brojač slova
    for (char c : s) cnt[c - 'a']++;
    
    long long res = fact[s.length()]; // Brojnik (N!)
    
    for (int i = 0; i < 26; i++) {
        if (cnt[i] > 1) {
            // Množimo s inverzom faktorijela broja pojavljivanja
            res = (res * invFact[cnt[i]]) % MOD;
        }
    }
    
    cout << res << endl;
    return 0;
}
```

---

<!-- _class: lead -->
# [Distributing Apples](<https://cses.fi/problemset/task/1716>)

[Link na zadatak](https://cses.fi/problemset/task/1716)

---

# Analiza: Distributing Apples

**Problem:** Na koliko načina možemo podijeliti $m$ jabuka među $n$ djece?
**Ograničenja:** $n, m \le 10^6$.

### Intuicija: Stars and Bars (Zvijezde i pregrade)

Zamislimo $m$ jabuka kao zvjezdice ($\star$) i $n-1$ pregrada ($|$) koje odvajaju djecu.
Primjer (3 jabuke, 3 djece $\rightarrow$ 2 pregrade):
$\star \star | \star |$ znači: dijete A dobiva 2, B dobiva 1, C dobiva 0.

Ukupan broj simbola je $m + (n - 1)$.
Trebamo odabrati pozicije za $m$ jabuka (ili $n-1$ pregrada).

**Formula:**
$$ \binom{n + m - 1}{m} \quad \text{ili} \quad \binom{n + m - 1}{n - 1} $$

---

# Rješenje: Distributing Apples

Zadatak se svodi na jedan poziv funkcije `nCk`.

```cpp
#include <iostream>
// ... uključiti precompute, fact, invFact ...

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    precompute(); // Važno!

    int n, m;
    cin >> n >> m;
    
    // Formula: (n + m - 1) povrh m
    cout << nCk(n + m - 1, m) << endl;

    return 0;
}
```

---

<!-- _class: title -->
# Sretno s kodiranjem

Vježba čini majstora.
