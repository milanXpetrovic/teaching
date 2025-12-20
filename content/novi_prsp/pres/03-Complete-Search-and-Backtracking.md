---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Potpuna pretraga i backtracking"
footer: "Programiranje za rješavanje složenih problema | Vježbe 2025/26"
---

<!-- paginate: false -->
<!-- _class: title  -->
# Potpuna pretraga i backtracking

Programiranje za rješavanje složenih problema

---

# Sadržaj

1. **Uvod i motivacija**
   - Što je potpuna pretraga?
   - Kada je koristiti?
2. **Generiranje podskupova**
   - Rekurzija
   - Bitmaske
3. **Generiranje permutacija**
   - `std::next_permutation`
4. **Backtracking**
   - Koncept i *pruning*
   - Primjer: N-kraljica
5. **Zadaci za vježbu**

---

<!-- _class: lead -->

# Uvod i motivacija

## Brute force pristup

---

# Što je potpuna pretraga?

**Potpuna pretraga** (engl. *complete search* ili *brute force*) je tehnika rješavanja problema koja se svodi na generiranje **svih mogućih rješenja** i provjeru svakog od njih.

- Često se smatra "naivnom", ali je temelj mnogih algoritama.
- Garantira pronalazak točnog rješenja (ako ga nađemo u vremenskom limitu).

**Kada je primjenjiva?**

- Kada je prostor rješenja malen.
- Ako je $N$ dovoljno mali da složenost poput $O(2^N)$ ili $O(N!)$ prolazi unutar 1-2 sekunde.
- Uvijek prvo razmotrite potpunu pretragu! Ako je dovoljno brza, nema potrebe za kompliciranjem.

---

# Backtracking: Pametna potpuna pretraga

**Backtracking** je rekurzivna tehnika gradnje rješenja korak po korak.

**Ključna ideja:**

- Pokušavamo proširiti trenutno parcijalno rješenje.
- Ako shvatimo da trenutni put ne vodi do rješenja, **odustajemo** (engl. *pruning*) i vraćamo se korak unatrag (**backtrack**).

**Prednost:**

- *Pruning* drastično smanjuje broj stanja koja moramo obići u usporedbi s čistim *brute forceom*.

---

<!-- _class: lead -->
# Generiranje podskupova

## Problem ruksaka (Knapsack) za male N

---

# Problem: Generiranje svih podskupova

**Zadatak:**
Zadan je skup od $n$ predmeta s težinama. Pronađi podskup čija je suma težina što bliža, ali ne veća od kapaciteta $W$.

**Pristup:**
Svaki element možemo ili **uključiti** u podskup ili **ne uključiti**.
Ukupno ima $2^n$ mogućih podskupova.

---

# Rješenje 1: Rekurzija

Funkcija `search(k)` odlučuje za $k$-ti element.

```cpp
void search(int k, long long current_weight) {
    if (k == n) { // Svi elementi su razmotreni
        // Provjeri je li current_weight najbolje rješenje
        return;
    }

    // Opcija 1: Ne uključiti element k
    search(k + 1, current_weight);

    // Opcija 2: Uključiti element k (ako stane)
    if (current_weight + weights[k] <= W) {
        search(k + 1, current_weight + weights[k]);
    }
}
```

**Složenost:** $O(2^n)$.

---

# Rješenje 2: Bitmaske

Svaki podskup možemo predstaviti kao $n$-bitni broj.
Ako je $i$-ti bit **1**, element je u podskupu. Ako je **0**, nije.

```cpp
for (int mask = 0; mask < (1 << n); ++mask) {
    long long current_sum = 0;
    for (int i = 0; i < n; ++i) {
        if ((mask >> i) & 1) { // Provjera je li i-ti bit postavljen
            current_sum += weights[i];
        }
    }
    
    if (current_sum <= W) {
        best_sum = max(best_sum, current_sum);
    }
}
```

**Složenost:** $O(n \cdot 2^n)$.

---

<!-- _class: lead -->
# Generiranje permutacija

## Problem trgovačkog putnika (TSP) za male N

---

# Problem: Generiranje svih permutacija

**Zadatak:**
Zadan je skup od $n$ gradova. Pronađi najkraći put koji posjećuje svaki grad točno jednom.

**Rješenje:**
Isprobati sve moguće redoslijede (permutacije) gradova.
Broj permutacija je $n!$ (faktorijela).
Za $n=10$, $10! \approx 3.6 \cdot 10^6$ (brzo).
Za $n=20$, presporo.

---

# Rješenje: `std::next_permutation`

C++ STL ima ugrađenu funkciju za generiranje leksikografski sljedeće permutacije.

```cpp
vector<int> p(n);
for (int i = 0; i < n; ++i) p[i] = i; // Početna permutacija: 0, 1, 2...

long long min_path = -1;

do {
    // Izračunaj duljinu puta za trenutnu permutaciju p
    long long current_path = calculate_path(p);
    
    if (min_path == -1 || current_path < min_path) {
        min_path = current_path;
    }
} while (next_permutation(p.begin(), p.end()));
```

**Složenost:** $O(n \cdot n!)$.

---

<!-- _class: lead -->

# Problem N-kraljica

## Klasičan primjer backtrackinga

---

# Problem: N-kraljica

**Zadatak:**
Na šahovsku ploču $n \times n$ postavi $n$ kraljica tako da se nikoje dvije ne napadaju.
(Kraljica napada horizontalno, vertikalno i dijagonalno).

**Pristup:**
Postavljamo kraljice red po red. U svakom redu pokušamo staviti kraljicu u neki stupac.

**Pruning (Rezanje):**
Ako stavimo kraljicu na polje koje je već napadnuto, odmah stajemo i vraćamo se (ne idemo u dubinu).

---

# Implementacija: N-kraljica

```cpp
void search(int y) {
    if (y == n) { count++; return; } // Našli smo rješenje
    
    for (int x = 0; x < n; ++x) {
        // Ako je pozicija (y, x) napadnuta, preskoči (PRUNING)
        if (column[x] || diag1[x+y] || diag2[x-y+n-1]) continue;

        // Postavi kraljicu
        column[x] = diag1[x+y] = diag2[x-y+n-1] = true;
        
        search(y + 1); // Rekurzivni poziv za sljedeći red

        // BACKTRACK: Makni kraljicu da probamo drugu opciju
        column[x] = diag1[x+y] = diag2[x-y+n-1] = false;
    }
}
```

Koristimo pomoćna polja `column`, `diag1`, `diag2` za $O(1)$ provjeru napada.

---

<!-- _class: lead -->

# Zadaci za vježbu

## CSES i Codeforces

---

# CSES Problem Set

1. **[Apple Division](https://cses.fi/problemset/task/1623)**
   - Podijeli jabuke u dvije grupe s minimalnom razlikom težina.
   - *Rješenje:* Generiranje podskupova (rekurzija ili bitmaske).
2. **[Creating Strings](https://cses.fi/problemset/task/1622)**
   - Generiraj sve unikatne permutacije stringa.
   - *Rješenje:* `next_permutation` (pazi na duplikate slova).
3. **[Chessboard and Queens](https://cses.fi/problemset/task/1624)**
   - N-kraljica problem, ali su neka polja na ploči blokirana.
4. **[Grid Paths](https://cses.fi/problemset/task/1625)**
   - Napredniji backtracking s jakim optimizacijama.

---

<!-- _class: title -->
# Apple Division (CSES)

## Generiranje podskupova

---

# Analiza: Apple Division

**Problem:**
Imamo $n$ jabuka s težinama $p_1, p_2, \dots, p_n$. Treba ih podijeliti u dvije grupe tako da je razlika u ukupnim težinama grupa **minimalna**.
**Ograničenja:** $n \le 20$.

## Intuicija

Svaka jabuka može ići u **Grupu 1** ili **Grupu 2**.
To je binarni izbor za svaku od $n$ jabuka.
Ukupan broj načina je $2^n$. Za $n=20$, $2^{20} \approx 10^6$, što je vrlo brzo.

Možemo koristiti rekurziju koja prolazi kroz sve jabuke i održava trenutne sume obiju grupa.

---

# Implementacija: Apple Division

```cpp
long long n, p[20];

long long solve(int idx, long long sum1, long long sum2) {
    // Bazni slučaj: prošli smo sve jabuke
    if (idx == n) {
        return abs(sum1 - sum2);
    }

    // Opcija 1: Jabuka ide u prvu grupu
    long long diff1 = solve(idx + 1, sum1 + p[idx], sum2);

    // Opcija 2: Jabuka ide u drugu grupu
    long long diff2 = solve(idx + 1, sum1, sum2 + p[idx]);

    return min(diff1, diff2);
}
```

U `main` funkciji pozivamo `solve(0, 0, 0)`.

---

<!-- _class: title -->
# Creating Strings (CSES)

## Permutacije s ponavljanjem

---

# Analiza: Creating Strings

**Problem:**
Zadan je string (npr. `aabac`). Treba ispisati sve **različite** permutacije tog stringa po abecednom redu.
**Ograničenja:** Duljina stringa $\le 8$.

## Intuicija

Broj permutacija za duljinu 8 je $8! = 40320$, što je malo.
Glavni izazov su **duplikati** (npr. zamjena dva slova 'a' ne stvara novi string).

C++ funkcija `std::next_permutation` pametno generira samo leksikografski sljedeću **unikatnu** permutaciju.

---

# Implementacija: Creating Strings

```cpp
string s;
cin >> s;
sort(s.begin(), s.end()); // Obavezno sortirati za next_permutation

vector<string> permutations;
do {
    permutations.push_back(s);
} while (next_permutation(s.begin(), s.end()));

cout << permutations.size() << endl;
for (const string& p : permutations) {
    cout << p << endl;
}
```

**Napomena:** Ako koristimo rekurziju, morali bismo koristiti `std::set` ili pamtiti frekvencije slova da izbjegnemo duplikate.

---

<!-- _class: title -->
# Chessboard and Queens (CSES)

## Backtracking s ograničenjima

---

# Analiza: Chessboard and Queens

**Problem:**
Postavi 8 kraljica na $8 \times 8$ ploču tako da se ne napadaju. Dodatno, neka polja su označena s `*` i na njih **ne smijemo** staviti kraljicu.

## Intuicija

Ovo je standardni problem N-kraljica ($N=8$), uz jedan dodatni uvjet.
U rekurzivnoj funkciji, prije nego postavimo kraljicu na `(y, x)`, provjeravamo:

1. Je li stupac/dijagonala slobodna?
2. Je li polje `board[y][x]` slobodno (nije `*`)?

---

# Implementacija: Chessboard and Queens

```cpp
// board[8][8] sadrži ulaz ('.' ili '*')
void search(int y) {
    if (y == 8) { ans++; return; }

    for (int x = 0; x < 8; x++) {
        // Dodatna provjera: board[y][x] == '*'
        if (col[x] || d1[x+y] || d2[x-y+7] || board[y][x] == '*') 
            continue;

        col[x] = d1[x+y] = d2[x-y+7] = true;
        search(y + 1);
        col[x] = d1[x+y] = d2[x-y+7] = false; // Backtrack
    }
}
```

Složenost je manja od klasičnih 8-kraljica zbog dodatnih ograničenja (manje grana stabla).

---

<!-- _class: title -->

# Grid Paths (CSES)

## Optimizacija backtrackinga

---

# Analiza: Grid Paths

**Problem:**
Pronađi broj puteva duljine 48 od `(0,0)` do `(6,6)` u mreži $7 \times 7$ koji posjećuju svako polje točno jednom.
Ulazni string definiraju smjerove (npr. `????D...`) koje moramo poštovati.

## Intuicija

Naivni backtracking ($4^{48}$) je nemoguć. Trebamo **jako rezanje (pruning)**.

**Ključne optimizacije:**

1. Ako udarimo u zid (ili posjećeno polje), a možemo ići lijevo i desno $\rightarrow$ mreža se dijeli na dva nepovezana dijela. Ne možemo posjetiti sve $\rightarrow$ **RETURN**.
2. Ako stignemo na cilj `(6,6)` prije 48. koraka $\rightarrow$ **RETURN**.

---

# Implementacija: Grid Paths (Optimizacija)

```cpp
// (r, c) trenutna pozicija, step je broj koraka
void solve(int r, int c, int step) {
    // Stigli na cilj
    if (r == 6 && c == 0) { 
        if (step == 48) count++; 
        return; 
    }
    
    // OPTIMIZACIJA: Zid ispred, a lijevo i desno slobodno -> Split
    if (visited[r+dr[dir]][c+dc[dir]] && 
        !visited[r+dr[left]][c+dc[left]] && 
        !visited[r+dr[right]][c+dc[right]]) 
            return;

    visited[r][c] = true;
    // ... rekurzivni pozivi za 4 smjera ...
    visited[r][c] = false;
}
```

Ovaj problem je poznat kao jedan od najtežih u uvodnoj sekciji zbog potrebe za specifičnim optimizacijama.

---

# Codeforces

Preporuka: Rješavati zadatke s tagom `brute force` težine do 1200.

[Codeforces Brute Force Problems](https://codeforces.com/problemset?tags=brute%20force)

---
