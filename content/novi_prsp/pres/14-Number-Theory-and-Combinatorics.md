---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Teorija brojeva i kombinatorika"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!--
Prijedlozi za slike (dodati ručno):

1. Sito Eratostena (slajd "Sito Eratostena"):
   ![bg right:40% fit](https://upload.wikimedia.org/wikipedia/commons/b/b9/Sieve_of_Eratosthenes_animation.gif)
2. Geometrijski prikaz Euklidovog algoritma (slajd "Euklidov algoritam"):
   pretraga "Euclidean algorithm geometry rectangle tiling".
3. Modularna aritmetika kao sat (slajd "Pravila modularne aritmetike"):
   pretraga "Modular arithmetic clock cycle visualization".
4. Pascalov trokut (slajd "Binomni koeficijenti"):
   pretraga "Pascal triangle binomial coefficients".
5. Catalanovi brojevi (slajd "Catalanovi brojevi"):
   pretraga "Catalan numbers polygon triangulation example".
6. Vennov dijagram (slajd "Princip uključivanja-isključivanja"):
   https://media.geeksforgeeks.org/wp-content/uploads/Screen-Shot-2018-03-14-at-5.30.27-PM.png
   izvor: https://www.geeksforgeeks.org/competitive-programming/inclusion-exclusion-principle-for-competitive-programming/
7. Stars and bars (slajd "Analiza: Distributing Apples"):
   ![bg right:50% fit](https://upload.wikimedia.org/wikipedia/commons/thumb/e/cd/Stars_and_bars.png/440px-Stars_and_bars.png)
-->

<!-- _paginate: false -->
<!-- _class: title -->
# Teorija brojeva i kombinatorika

Programiranje za rješavanje složenih problema

---

# Sadržaj

1. **Uvod i motivacija**
   * Zašto su nam potrebni brojevi?
   * Izazovi: veliki brojevi i efikasnost
2. **Osnovna teorija brojeva**
   * Prosti brojevi, GCD, modularna aritmetika
3. **Osnove kombinatorike**
   * Binomni koeficijenti, Catalanovi brojevi
   * Princip uključivanja-isključivanja
4. **Zadaci za vježbu**

---

<!-- _class: lead -->
# Uvod i motivacija

---

# Zašto su nam potrebni brojevi i prebrojavanje?

Teorija brojeva i kombinatorika temelji su diskretne matematike i "kralježnica" mnogih algoritamskih problema.

* **Teorija brojeva:**
  * Bavi se svojstvima cijelih brojeva.
  * Ključni pojmovi: prostost, djeljivost, modularna aritmetika.
  * Primjena: kriptografija, hashing, optimizacija petlji.
* **Kombinatorika:**
  * Umjetnost prebrojavanja.
  * Klasično pitanje: *"Na koliko se načina nešto može dogoditi?"*
  * Primjena: izračun složenosti, vjerojatnost, broj putova u grafu.

---

# Izazovi: veliki brojevi i efikasnost

U natjecateljskom programiranju susrećemo se s dva glavna problema:

1. **Veliki brojevi (overflow):**
   * Rezultati često premašuju `long long` ($2^{63}-1$).
   * Rješenje: računanje **modulo** neki veliki prosti broj (npr. $10^9 + 7$).
   * Zato je **modularna aritmetika** ključna vještina.

2. **Efikasnost (time limit):**
   * Naivno prebrojavanje ili provjera djeljivosti prespori su za $N=10^9$ ili $10^{18}$.
   * Rješenje: pametni algoritmi ($O(\log N)$ ili $O(\sqrt{N})$).
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
# Osnovna teorija brojeva

## Prosti brojevi i faktorizacija

---

# Prosti brojevi

**Definicije:**

* **Prosti broj:** cijeli broj $n > 1$ djeljiv samo s 1 i samim sobom.
* **Faktorizacija:** svaki broj $n > 1$ ima **jedinstven** rastav na proste faktore.
  * Primjer: $60 = 2^2 \cdot 3 \cdot 5$

**Kako brzo pronaći proste brojeve?**

* Provjera jednog broja: $O(\sqrt{n})$.
* Pronalaženje svih prostih brojeva do $N$: **Eratostenovo sito**.

---

# Sito Eratostena (Sieve of Eratosthenes)

**Ideja:** eliminacija višekratnika.

1. Krenemo od 2 (prvi prosti broj).
2. Sve njegove višekratnike ($4, 6, 8, \dots$) označimo kao složene.
3. Nađemo idući neoznačeni broj (3): on je prost. Označimo njegove višekratnike ($6, 9, 12 \dots$).
4. Ponavljamo postupak.

**Složenost:** $O(N \log \log N)$, gotovo linearno!

---

# Implementacija sita (C++)

```cpp
const int MAXN = 1e6;
vector<bool> is_prime(MAXN + 1, true);

void sieve() {
    is_prime[0] = is_prime[1] = false; // 0 i 1 nisu prosti

    for (int p = 2; p * p <= MAXN; ++p) {
        // Ako p nije prekrižen, onda je prost
        if (is_prime[p]) {
            // Prekrižimo sve višekratnike od p
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
$$ \gcd(a, b) = \gcd(b, a \bmod b) $$
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
*Napomena:* u C++17 postoji `std::gcd(a, b)` u `<numeric>`.

---

<!-- _class: lead -->
# Modularna aritmetika

---

# Pravila modularne aritmetike

Kada radimo s velikim brojevima, zanimaju nas samo ostaci pri dijeljenju s $M$.

Osnovna svojstva:

1. **Zbrajanje:** $(a + b) \bmod M = ((a \bmod M) + (b \bmod M)) \bmod M$
2. **Množenje:** $(a \cdot b) \bmod M = ((a \bmod M) \cdot (b \bmod M)) \bmod M$
3. **Oduzimanje (PAZITE!):**
   $$ (a - b) \bmod M = ((a \bmod M) - (b \bmod M) + M) \bmod M $$
   *Dodajemo $M$ prije modula da izbjegnemo negativne rezultate!*

---

# Modularno potenciranje (binary exponentiation)

**Problem:** izračunati $a^b \bmod M$ za veliki $b$ (npr. $10^{18}$).

* Naivno množenje: $O(b)$ $\rightarrow$ presporo (TLE).
* Binarno potenciranje: $O(\log b)$ $\rightarrow$ trenutačno.

**Ideja (podijeli pa vladaj):**

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
        // Ako je eksponent neparan, rezultat množimo bazom
        if (exp % 2 == 1) res = (res * base) % MOD;

        // Kvadriramo bazu za idući korak
        base = (base * base) % MOD;
        exp /= 2;
    }
    return res;
}
```

---

# Modularni inverz

Kod realnih brojeva dijeljenje je množenje recipročnom vrijednošću ($a / b = a \cdot b^{-1}$).
U modularnoj aritmetici ne postoji "dijeljenje", ali postoji **modularni inverz** (ako je $\gcd(a, M) = 1$).

Tražimo broj $x$ takav da je:
$$ a \cdot x \equiv 1 \pmod M $$
Zapisujemo ga kao $a^{-1}$.

**Mali Fermatov teorem:**
Ako je $M$ prost broj i $a$ nije djeljiv s $M$, vrijedi:
$$ a^{M-2} \equiv a^{-1} \pmod M $$

Dakle, inverz računamo pomoću funkcije `power(a, M-2)`.

---

<!-- _class: lead -->
# Osnove kombinatorike

## Binomni koeficijenti

---

# Binomni koeficijenti ($n$ povrh $k$)

Broj načina za odabir $k$ elemenata iz skupa od $n$ elemenata.

**Formula:**
$$ \binom{n}{k} = \frac{n!}{k!(n-k)!} $$

**Problem:** faktorijeli brzo postaju ogromni.
**Rješenja:**

1. **Pascalov trokut (DP):** $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$. Dobro za manje $N$.
2. **Faktorijeli + inverzi:** za velike $N$ uz modulo $M$.
   $$ \binom{n}{k} \bmod M = (n! \cdot (k!)^{-1} \cdot ((n-k)! )^{-1}) \bmod M $$

---

# Implementacija nCk (s inverzima)

```cpp
// Pretpostavka: fact[] i invFact[] su već predračunati do MAXN

long long nCk(int n, int k) {
    if (k < 0 || k > n) return 0;

    // Formula: n! * inv(k!) * inv((n-k)!)
    return fact[n] * invFact[k] % MOD * invFact[n - k] % MOD;
}
```

*Ovaj pristup omogućuje odgovor na upit u $O(1)$ vremena.*

---

# Catalanovi brojevi

Niz prirodnih brojeva koji se pojavljuje u raznim problemima prebrojavanja.
$$ C_n = \frac{1}{n+1} \binom{2n}{n} $$

**Primjeri primjene:**

1. Broj ispravnih izraza s $n$ parova zagrada: `((()))`, `()(())`...
2. Broj načina za triangulaciju konveksnog poligona s $n+2$ vrha.
3. Broj binarnih stabala s $n$ čvorova.

---

# Princip uključivanja-isključivanja

Koristi se za prebrojavanje elemenata unije skupova.

**Formula za 2 skupa:**
$$ |A \cup B| = |A| + |B| - |A \cap B| $$

**Formula za 3 skupa:**
$$ |A \cup B \cup C| = |A| + |B| + |C| - (|A \cap B| + |A \cap C| + |B \cap C|) + |A \cap B \cap C| $$

**Primjer:** koliko je brojeva od 1 do $n$ djeljivo s $p$ ili $q$?
$$ \text{Rezultat} = \lfloor \frac{n}{p} \rfloor + \lfloor \frac{n}{q} \rfloor - \lfloor \frac{n}{\text{lcm}(p, q)} \rfloor $$

---

<!-- _class: lead -->
# Zadaci za vježbu (CSES)

## Zadaci za početak i srednju razinu

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

**Problem:** izračunati $a^b \bmod (10^9 + 7)$.
**Ograničenja:** $a, b \le 10^9$, broj upita $n \le 2 \cdot 10^5$.

**Intuicija**

1. **Naivni pristup:** množenje u petlji `for (i=0; i<b; ++i)` ima složenost $O(b)$.
   * Za $b = 10^9$ to je presporo (TLE), pogotovo uz puno upita.
2. **Binarno potenciranje:**
   * Koristimo svojstvo:
     $$ a^b = \begin{cases} (a^{b/2})^2 & \text{ako je } b \text{ paran} \\ a \cdot a^{b-1} & \text{ako je } b \text{ neparan} \end{cases} $$
   * **Složenost:** $O(\log b)$. Za $b=10^9$ to je oko 30 koraka.

---

# Implementacija: funkcija za potenciranje

```cpp
const long long MOD = 1e9 + 7;

long long binpow(long long base, long long exp) {
    long long res = 1;
    base %= MOD; // Baza mora biti unutar modula

    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % MOD; // Ako je bit 1, množimo

        base = (base * base) % MOD; // Kvadriramo bazu
        exp /= 2;                   // Pomak bitova udesno (dijeljenje s 2)
    }
    return res;
}
```

(Ista funkcija kao `power` iz uvodnog dijela.)

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
    while (n--) {
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

**Problem:** izračunati $a^{b^c} \bmod (10^9 + 7)$.
**Ograničenja:** $a, b, c \le 10^9$.

**Intuicija: mali Fermatov teorem**

Želimo izračunati $a^X \bmod M$, gdje je $X = b^c$.
Eksponent $X$ može biti ogroman, ali nas zanima samo njegov ostatak.
**Važno pravilo:** eksponent ne računamo $\bmod M$, nego $\bmod (M-1)$!

$$ a^{b^c} \equiv a^{b^c \bmod (M-1)} \pmod M $$

*Uvjet:* $M$ mora biti prost (što $10^9+7$ jest), a $a$ ne smije biti djeljiv s $M$.

---

# Ključni dio koda: dva modula

```cpp
const long long MOD = 1e9 + 7;

long long solve(long long a, long long b, long long c) {
    // 1. Eksponent: exp = b^c mod (MOD - 1)
    long long exp = binpow(b, c, MOD - 1);

    // 2. Konačni rezultat: a^exp mod MOD
    return binpow(a, exp, MOD);
}
```

*Napomena: funkciju `binpow` moramo prilagoditi da prima proizvoljan modul.*

---

# Rješenje: Exponentiation II

```cpp
#include <iostream>
using namespace std;

const long long MOD = 1e9 + 7;

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
    while (n--) {
        long long a, b, c;
        cin >> a >> b >> c;
        long long exponent_part = binpow(b, c, MOD - 1);
        cout << binpow(a, exponent_part, MOD) << "\n";
    }
    return 0;
}
```

---

<!-- _class: lead -->
# [Counting Divisors](<https://cses.fi/problemset/task/1713>)

---

# Analiza: Counting Divisors

**Problem:** za $n$ brojeva $x$ treba ispisati broj njihovih djelitelja.
**Ograničenja:** $n \le 10^5, x \le 10^6$.

**Intuicija**

1. **Pristup A (iteracija):** za svaki $x$ provjerimo sve brojeve do $\sqrt{x}$.
   * Složenost po upitu: $O(\sqrt{x}) \approx 1000$.
   * Ukupno: $10^5 \times 1000 = 10^8$. To u C++ obično prolazi unutar 1 sekunde.

2. **Pristup B (sito, brže):** predračunamo najmanji prosti faktor (SPF) za svaki broj do $10^6$.
   * Faktorizacija broja $x$ tada traje $O(\log x)$.
   * Ako je $x = p_1^{a_1} p_2^{a_2} \dots$, broj djelitelja je $(a_1+1)(a_2+1)\dots$

---

# Kod: pristup A (dovoljno brz i jednostavan)

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
            cnt++;                // i je djelitelj
            if (i * i != x) cnt++; // x/i je također djelitelj
        }
    }
    cout << cnt << "\n";
}

int main() {
    ios_base::sync_with_stdio(false); // Obavezno za brzi I/O
    cin.tie(NULL);
    int n;
    cin >> n;
    while (n--) solve();
    return 0;
}
```

---

<!-- _class: lead -->
# [Common Divisors](<https://cses.fi/problemset/task/1081>)

---

# Analiza: Common Divisors

**Problem:** treba naći najveći zajednički djelitelj (GCD) nekog para brojeva u nizu.
**Ograničenja:** $n \le 2 \cdot 10^5, x_i \le 10^6$.

**Intuicija**

1. **Naivno:** isprobati sve parove ($O(N^2)$). Presporo!
2. **Obrnuti pristup:** umjesto da tražimo GCD parova, pitamo se: **koji je najveći broj $g$ koji dijeli barem dva broja u nizu?**
   * Raspon vrijednosti je do $10^6$ (nazovimo to $MAX$).
   * Krenemo od $g = MAX$ prema dolje ($10^6, 999999, \dots$).
   * Za svaki $g$ prebrojimo njegove višekratnike u nizu. Ako ih je $\ge 2$, to je rješenje!

---

# Ključni dio koda: frequency array

Koristimo niz `cnt` gdje `cnt[x]` govori koliko se puta broj `x` pojavljuje u ulazu.

```cpp
// Iteriramo kroz moguće GCD-ove od najvećeg prema 1
for (int g = 1000000; g >= 1; g--) {
    int multiples = 0;

    // Brojimo višekratnike od g u nizu: g, 2*g, 3*g...
    for (int j = g; j <= 1000000; j += g) {
        multiples += cnt[j]; // Koliko se puta taj višekratnik pojavljuje
    }

    // Ako smo našli barem dva broja kojima je g djelitelj
    if (multiples >= 2) {
        cout << g << "\n";
        return 0;
    }
}
```

**Složenost:** $O(MAX \log MAX)$ zbog harmonijskog reda ($MAX/1 + MAX/2 + MAX/3 + \dots$).

---

# Rješenje: Common Divisors

```cpp
#include <iostream>
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
            cout << g << "\n";
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

**Problem:** izračunati $\binom{n}{k} \bmod (10^9 + 7)$ za mnogo upita.
**Ograničenja:** $n \le 10^6$, $10^5$ upita.

**Intuicija**

Formula je $\binom{n}{k} = \frac{n!}{k!(n-k)!}$.
Trebamo je računati modulo $10^9+7$. Dijeljenje nije dozvoljeno, pa množimo modularnim inverzom:
$$ \binom{n}{k} = n! \cdot (k!)^{-1} \cdot ((n-k)! )^{-1} \pmod M $$

**Strategija:**

1. Predračunamo faktorijele (`fact`).
2. Predračunamo inverzne faktorijele (`invFact`) pomoću Fermatova teorema ($x^{MOD-2}$).

---

# Ključni dio koda: predračun (precomputation)

```cpp
long long fact[MAXN], invFact[MAXN];

long long power(long long base, long long exp); // Binarno potenciranje

void precompute() {
    fact[0] = 1;
    for (int i = 1; i < MAXN; i++)
        fact[i] = fact[i - 1] * i % MOD;

    // Samo JEDAN inverz Fermatom, ostali unatrag u O(N):
    // (i-1)!^(-1) = i!^(-1) * i
    invFact[MAXN - 1] = power(fact[MAXN - 1], MOD - 2);
    for (int i = MAXN - 1; i > 0; i--)
        invFact[i - 1] = invFact[i] * i % MOD;
}
```

(Može i `invFact[i] = power(fact[i], MOD - 2)` za svaki $i$: to je $O(N \log MOD)$, sporije, ali i dalje prolazi.)

---

# Rješenje: Binomial Coefficients

```cpp
#include <iostream>
using namespace std;

const int MAXN = 2000005; // 2*10^6: dovoljno i za Distributing Apples (n + m - 1)
const long long MOD = 1e9 + 7;
long long fact[MAXN], invFact[MAXN];

long long power(long long base, long long exp) { /* binpow kao ranije */ }

void precompute() { /* kao na prethodnom slajdu */ }

long long nCk(int n, int k) {
    if (k < 0 || k > n) return 0;
    return fact[n] * invFact[k] % MOD * invFact[n - k] % MOD;
}

int main() {
    precompute();
    int q; cin >> q;
    while (q--) {
        int a, b; cin >> a >> b;
        cout << nCk(a, b) << "\n";
    }
}
```

---

<!-- _class: lead -->
# [Creating Strings II](<https://cses.fi/problemset/task/1715>)

---

# Analiza: Creating Strings II

**Problem:** koliko se različitih stringova može dobiti permutiranjem slova u zadanom stringu?
**Ulaz:** string (npr. "aabac").

**Intuicija**

Ovo su **permutacije s ponavljanjem**.
Ako string ima duljinu $N$, a slova se pojavljuju $c_a, c_b, \dots, c_z$ puta, formula je:

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
        // Množimo inverzom faktorijela broja pojavljivanja
        res = res * invFact[cnt[i]] % MOD;
    }

    cout << res << "\n";
    return 0;
}
```

---

<!-- _class: lead -->
# [Distributing Apples](<https://cses.fi/problemset/task/1716>)

---

# Analiza: Distributing Apples

**Problem:** na koliko načina možemo podijeliti $m$ jabuka među $n$ djece?
**Ograničenja:** $n, m \le 10^6$.

**Intuicija: stars and bars (zvjezdice i pregrade)**

Zamislimo $m$ jabuka kao zvjezdice ($\star$) i $n-1$ pregrada ($|$) koje odvajaju djecu.
Primjer (3 jabuke, 3 djece $\rightarrow$ 2 pregrade):
$\star \star | \star |$ znači: dijete A dobiva 2, B dobiva 1, C dobiva 0.

Ukupan broj simbola je $m + (n - 1)$.
Trebamo odabrati pozicije za $m$ jabuka (ili za $n-1$ pregrada).

**Formula:**
$$ \binom{n + m - 1}{m} \quad \text{ili} \quad \binom{n + m - 1}{n - 1} $$

**Pazite:** $n + m - 1$ može biti gotovo $2 \cdot 10^6$, pa faktorijeli moraju ići do $2 \cdot 10^6$!

---

# Rješenje: Distributing Apples

Zadatak se svodi na jedan poziv funkcije `nCk`.

```cpp
#include <iostream>
// ... precompute, fact, invFact (MAXN = 2000005!) ...

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    precompute(); // Važno!

    int n, m;
    cin >> n >> m;

    // Formula: (n + m - 1) povrh m
    cout << nCk(n + m - 1, m) << "\n";

    return 0;
}
```

---

<!-- _class: title -->
# Sretno s kodiranjem

Vježba čini majstora.
