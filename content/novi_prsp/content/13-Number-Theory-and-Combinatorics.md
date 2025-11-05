---
nav_exclude: true
---

# Teorija Brojeva i Kombinatorika

## Sadržaj
1.  [Uvod i Motivacija](#uvod-i-motivacija)
    *   [Zašto su nam potrebni brojevi i prebrojavanje?](#zašto-su-nam-potrebni-brojevi-i-prebrojavanje)
    *   [Izazovi: Veliki brojevi i efikasnost](#izazovi-veliki-brojevi-i-efikasnost)
    *   [Preporučena Literatura](#preporučena-literatura)
2.  [Osnovna Teorija Brojeva](#osnovna-teorija-brojeva)
    *   [Prosti brojevi i faktorizacija](#prosti-brojevi-i-faktorizacija)
    *   [Najveći zajednički djelitelj (GCD)](#najveći-zajednički-djelitelj-gcd)
    *   [Modularna Aritmetika](#modularna-aritmetika)
    *   [Modularni inverz i rješavanje jednadžbi](#modularni-inverz-i-rješavanje-jednadžbi)
3.  [Osnove Kombinatorike](#osnove-kombinatorike)
    *   [Binomni koeficijenti](#binomni-koeficijenti)
    *   [Catalanovi brojevi](#catalanovi-brojevi)
    *   [Princip uključivanja-isključivanja](#princip-uključivanja-isključivanja)
4.  [Zadaci za Vježbu](#zadaci-za-vježbu)

---

## Uvod i Motivacija

### Zašto su nam potrebni brojevi i prebrojavanje?
Teorija brojeva i kombinatorika su temelji diskretne matematike i često se pojavljuju u algoritamskim problemima, ponekad na vrlo suptilne načine.
-   **Teorija brojeva** bavi se svojstvima cijelih brojeva. U natjecateljskom programiranju, to uključuje probleme vezane uz prostost, djeljivost i modularnu aritmetiku.
-   **Kombinatorika** je grana matematike koja se bavi prebrojavanjem. Klasično pitanje je: "Na koliko načina se nešto može dogoditi?".

### Izazovi: Veliki brojevi i efikasnost
Jedan od glavnih izazova u ovim problemima je rad s **velikim brojevima**. Rezultati mogu lako premašiti kapacitet standardnih tipova podataka poput `long long`. Zbog toga se često traži da se rezultat ispiše **modulo** neki veliki prosti broj (obično `10^9 + 7`). Modularna aritmetika je stoga ključna vještina.

Drugi izazov je **efikasnost**. Naivno prebrojavanje ili provjera djeljivosti je često prespora. Potrebni su nam pametni algoritmi poput Euklidovog algoritma, sita za proste brojeve i modularnog potenciranja.

### Preporučena Literatura
*   **CPH (Competitive Programmer's Handbook):**
    *   Poglavlje 21: *Number theory*
    *   Poglavlje 22: *Combinatorics*
*   **CLRS (Introduction to Algorithms):**
    *   Poglavlje 31: *Number-Theoretic Algorithms* (pruža dublji uvid u matematičke dokaze)

---

## Osnovna Teorija Brojeva

### Prosti brojevi i faktorizacija
-   **Prosti broj:** Cijeli broj veći od 1 koji je djeljiv samo s 1 i samim sobom.
-   **Faktorizacija:** Svaki cijeli broj `n > 1` ima jedinstvenu faktorizaciju na proste brojeve.

**Sito Eratostena (Sieve of Eratosthenes):** Efikasan algoritam za pronalaženje svih prostih brojeva do `n` u `O(n log log n)` vremenu.
**Ideja:** Krenemo od 2. Označimo ga kao prostog, a sve njegove višekratnike kao složene. Zatim uzmemo sljedeći neoznačeni broj (3), označimo ga kao prostog, a njegove višekratnike kao složene, i tako dalje.
```cpp
const int MAXN = 1e6;
vector<bool> is_prime(MAXN + 1, true);

void sieve() {
    is_prime = is_prime = false;
    for (int p = 2; p * p <= MAXN; ++p) {
        if (is_prime[p]) {
            for (int i = p * p; i <= MAXN; i += p)
                is_prime[i] = false;
        }
    }
}
```

### Najveći zajednički djelitelj (GCD)
**Euklidov algoritam** je klasičan i vrlo efikasan algoritam za pronalaženje `gcd(a, b)`.
**Ideja:** `gcd(a, b) = gcd(b, a % b)`. Bazni slučaj je `gcd(a, 0) = a`.
```cpp
int gcd(int a, int b) {
    while (b) {
        a %= b;
        swap(a, b);
    }
    return a;
}```
**Složenost:** `O(log(min(a, b)))`. U C++17 postoji i ugrađena funkcija `std::gcd`.

### Modularna Aritmetika
Sve operacije se izvode "po modulu" `m`. To znači da nas zanima samo ostatak pri dijeljenju s `m`.
-   `(a + b) % m = ((a % m) + (b % m)) % m`
-   `(a - b) % m = ((a % m) - (b % m) + m) % m` (dodajemo `m` da izbjegnemo negativne ostatke)
-   `(a * b) % m = ((a % m) * (b % m)) % m`

**Modularno potenciranje:** Kako efikasno izračunati `a^b % m`? Naivno množenje `b` puta je presporo. Koristimo tehniku "binarnog potenciranja" (poznatu i kao "eksponencijacija kvadriranjem").
**Ideja:** Ako je `b` paran, `a^b = (a^(b/2))²`. Ako je `b` neparan, `a^b = a * a^(b-1)`.
```cpp
long long power(long long base, long long exp) {
    long long res = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp /= 2;
    }
    return res;
}
```
**Složenost:** `O(log b)`.

### Modularni inverz i rješavanje jednadžbi
**Modularni inverz** broja `a` po modulu `m` je broj `a⁻¹` takav da je `(a * a⁻¹) % m = 1`. Inverz postoji ako i samo ako su `a` i `m` relativno prosti (`gcd(a, m) = 1`).
Ako je `m` prost broj, po Malom Fermatovom teoremu, `a^(m-1) ≡ 1 (mod m)`. Stoga, `a * a^(m-2) ≡ 1 (mod m)`, pa je **`a⁻¹ = a^(m-2) % m`**. Možemo ga izračunati u `O(log m)` vremenu.

Za općeniti `m`, koristimo **Prošireni Euklidov algoritam** za pronalaženje `x` i `y` takvih da je `ax + my = gcd(a, m)`. Ako je `gcd(a, m) = 1`, onda je `ax + my = 1`, pa je `ax ≡ 1 (mod m)`. Rješenje `x` je modularni inverz.

---

## Osnove Kombinatorike

### Binomni koeficijenti
Binomni koeficijent `(n povrh k)`, `C(n, k)` ili `nCk`, predstavlja broj načina za odabir `k` elemenata iz skupa od `n` elemenata.
**Formula:** `nCk = n! / (k! * (n-k)!)`

Izračunavanje direktno preko faktorijela je nepraktično zbog velikih brojeva. Koristimo dva pristupa:
1.  **Paskalov trokut:** `nCk = (n-1)C(k-1) + (n-1)Ck`. Možemo predračunati sve vrijednosti u `O(n²)`.
2.  **Modularni inverz:** Ako računamo `nCk % m` gdje je `m` prost, možemo izračunati:
    `n! * (k!)^-1 * ((n-k)!)^-1 (mod m)`
    Modularne inverze za faktorijele računamo efikasno.

**Kod (s modularnim inverzom):**
```cpp
// Pretpostavlja da su faktorijeli i njihovi inverzi predračunati
long long combinations(int n, int k, long long MOD) {
    if (k < 0 || k > n) return 0;
    return fact[n] * invFact[k] % MOD * invFact[n - k] % MOD;
}
```

### Catalanovi brojevi
Catalanovi brojevi `C_n` se pojavljuju u mnogim problemima prebrojavanja. Primjeri:
-   Broj ispravnih izraza sa `n` parova zagrada.
-   Broj načina za triangulaciju konveksnog poligona s `n+2` stranice.
**Formula:** `C_n = (1 / (n+1)) * (2n povrh n)`

### Princip uključivanja-isključivanja
Koristi se za prebrojavanje elemenata unije skupova. Za dva skupa:
`|A ∪ B| = |A| + |B| - |A ∩ B|`
Za tri skupa:
`|A ∪ B ∪ C| = |A|+|B|+|C| - (|A∩B|+|A∩C|+|B∩C|) + |A∩B∩C|`
Općenito, zbrajamo veličine svih pojedinačnih skupova, oduzimamo veličine svih presjeka parova, dodajemo veličine presjeka trojki, i tako dalje.

**Problem: Broj brojeva djeljivih s `p` ili `q`**
Koliko brojeva od 1 do `n` je djeljivo s `p` ili `q`?
-   Broj djeljivih s `p`: `n / p`
-   Broj djeljivih s `q`: `n / q`
-   Broj djeljivih s `p` i `q` (tj. s `lcm(p, q)`): `n / lcm(p, q)`
Rješenje: `n/p + n/q - n/lcm(p, q)`.

---

## Zadaci za Vježbu

### CSES Problem Set ([https://cses.fi/problemset/](https://cses.fi/problemset/))

*   **Exponentiation I & II:** Vježba za modularno potenciranje.
*   **Counting Divisors:** Zahtijeva efikasnu faktorizaciju ili sito.
*   **Common Divisors:** Povezano s GCD-om i faktorizacijom.
*   **Binomial Coefficients:** Računanje `nCk % m`. Zahtijeva predračunavanje faktorijela i modularnih inverza.
*   **Creating Strings II:** Prebrojavanje permutacija s ponavljanjem. Rješenje koristi binomne (multinomske) koeficijente.
*   **Distributing Apples:** Klasični "stars and bars" kombinatorički problem.

### Codeforces

*   **GCD Arrays** (Problem 1459B): Zanimljiv zadatak koji koristi osnovna svojstva GCD-a.
*   **LCM Challenge** (Problem 235A): Traži se `lcm` od tri broja iz skupa `1...n`. Uključuje analizu i svojstva `lcm` i `gcd`.
*   **Divisibility by Eight** (Problem 550C): Problem koji se može riješiti DP-om, ali ima i elegantno rješenje temeljeno na teoriji brojeva (svojstva djeljivosti).
*   **Ciel and Flowers** (Problem 321C): Kombinatorički zadatak koji se može riješiti pohlepnim pristupom, ali zahtijeva dobro razmišljanje o parnosti.
*   **Pashmak and Flowers** (Problem 459B): Kombinatorički zadatak koji uključuje pronalaženje minimuma/maksimuma i prebrojavanje parova.
