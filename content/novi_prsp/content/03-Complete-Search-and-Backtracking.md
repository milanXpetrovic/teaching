---
nav_exclude: true
parent: PRSP
layout: default 
nav_order: 3
---

# Potpuna pretraga i backtracking

## Sadržaj

1. [Uvod i Motivacija](#uvod-i-motivacija)
    * Što je potpuna pretraga?
    * Kada je potpuna pretraga primjenjiva?
    * Backtracking: Pametna potpuna pretraga
    * Preporučena Literatura
2. [Primjeri Zadataka i Objašnjenja](#primjeri-zadataka-i-objašnjenja)
    * [Problem 1: Generiranje svih podskupova](#problem-1-generiranje-svih-podskupova)
    * [Problem 2: Generiranje svih permutacija](#problem-2-generiranje-svih-permutacija)
    * [Problem 3: N-kraljica problem (Backtracking)](#problem-3-n-kraljica-problem-backtracking)
3. [Zadaci za Vježbu](#zadaci-za-vježbu)

### Preporučena literatura

Za bolje razumijevanje tema obrađenih u ovoj skripti, preporučuje se sljedeća literatura:

* **CPH (Competitive Programmer's Handbook)**
    Poglavlje 5: Complete search – detaljno objašnjava metode potpune pretrage i backtrackinga.
* **CLRS (Introduction to Algorithms)**
    Iako CLRS nema posebno poglavlje posvećeno potpunoj pretrazi, koncept backtrackinga je obrađen u kontekstu rješavanja problema, npr. u uvodu u NP-potpunost (Poglavlje 34). Primarni izvor za ovu temu je CPH.

## Uvod i motivacija

### Što je potpuna pretraga?

**Potpuna pretraga** (engl. *complete search* ili *brute force*) je osnovna tehnika rješavanja problema koja se svodi na generiranje svih mogućih rješenja i provjeru svakog od njih. Iako se često čini "naivnom" ili neefikasnom, ona je temelj mnogih naprednijih algoritama i često je najbolje rješenje za probleme s malim ulaznim ograničenjima.

### Kada je potpuna pretraga primjenjiva?

Ključ za primjenu potpune pretrage leži u analizi složenosti. Ako je prostor svih mogućih rješenja dovoljno malen da ga računalo može proći unutar vremenskog ograničenja (obično 1-2 sekunde), potpuna pretraga je valjana strategija.
Uvijek je dobra ideja prvo razmotriti rješenje potpunom pretragom. Ako je dovoljno brzo, nema potrebe za kompliciranijim algoritmima. Ako nije, analiza prostora rješenja nam daje uvid zašto trebamo optimizirati.

### Backtracking: Pametna potpuna pretraga

**Backtracking** je tehnika koja formalizira potpunu pretragu na rekurzivan način. Ideja je graditi rješenje korak po korak. Na svakom koraku pokušavamo proširiti trenutno parcijalno rješenje.

* Ako ga možemo proširiti, napravimo rekurzivni poziv.
* Nakon što se rekurzivni poziv vrati, **poništimo** zadnji korak (to je "backtrack" dio) i pokušamo s drugom opcijom.

Ključna prednost backtrackinga je **rezanje pretrage** (engl. *pruning*). Ako u nekom koraku shvatimo da trenutno parcijalno rješenje ne može dovesti do valjanog ili optimalnog konačnog rješenja, odmah odustajemo od tog puta i ne istražujemo ga dalje.

## Primjeri zadataka i objašnjenja

### Problem 1: Generiranje svih podskupova

**Zadatak:** Zadan je skup od `n` predmeta, svaki sa svojom težinom. Pronađi podskup predmeta čija je ukupna težina što bliža, ali ne veća od, kapaciteta `W`. (Ovo je 0-1 knapsack problem, koji za male `n` rješavamo potpunom pretragom).

#### Rješenje 1: Rekurzija

Gradimo podskup tako da za svaki element odlučujemo hoćemo li ga uključiti ili ne.

**Algoritam:** Definiramo rekurzivnu funkciju `search(k, current_weight)`.

* `k`: indeks elementa kojeg trenutno razmatramo.
* `current_weight`: težina podskupa do sada.
U funkciji `search(k, ...)` imamo dvije opcije:

1. Ne uključiti element `k` i pozvati `search(k+1, ...)`.
2. Uključiti element `k` (ako stane) i pozvati `search(k+1, ...)`.

**Kod:**

```cpp
vector<int> weights;
int n;
long long max_weight = 0;

void search(int k, long long current_weight) {
    if (k == n) { // Svi elementi su razmotreni
        max_weight = max(max_weight, current_weight);
        return;
    }

    // Opcija 1: Ne uključiti element k
    search(k + 1, current_weight);

    // Opcija 2: Uključiti element k (ako stane)
    if (current_weight + weights[k] <= W) {
        search(k + 1, current_weight + weights[k]);
    }
}

// Početni poziv
search(0, 0);
```

**Složenost:** O(2^n), jer za svaki od `n` elemenata imamo 2 izbora.

#### Rješenje 2: Bitmaske

Svaki podskup skupa od `n` elemenata možemo predstaviti `n`-bitnim brojem (bitmaskom). Ako je `i`-ti bit postavljen na 1, `i`-ti element je u podskupu.

**Algoritam:**

1. Iteriraj kroz sve brojeve od `0` do `2^n - 1`.
2. Za svaki broj (masku), iteriraj od `i = 0` do `n-1`.
3. Ako je `i`-ti bit maske postavljen, dodaj `i`-ti element u zbroj.
4. Ažuriraj optimalno rješenje.

**Kod:**

```cpp
long long best_sum = 0;
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
cout << best_sum << '\n';
```

**Složenost:** O(n * 2^n). Vanjska petlja se vrti `2^n` puta, a unutarnja `n` puta.

### Problem 2: Generiranje svih permutacija

**Zadatak:** (TSP za male n) Zadan je skup od `n` gradova i udaljenosti između njih. Pronađi najkraći put koji posjećuje svaki grad točno jednom i vraća se u početni grad.

#### Rješenje 1: C++ `next_permutation`

STL nudi funkciju `next_permutation` koja generira sljedeću leksikografski veću permutaciju.

**Algoritam:**

1. Napravi `vector` koji sadrži indekse gradova, npr. `[0, 1, ..., n-1]`.
2. Koristi `do-while` petlju s `next_permutation` za generiranje svih permutacija.
3. Za svaku permutaciju, izračunaj duljinu puta i ažuriraj minimum.

**Kod:**

```cpp
vector<int> p(n);
for (int i = 0; i < n; ++i) p[i] = i;

long long min_path = -1;

do {
    long long current_path = 0;
    for (int i = 0; i < n - 1; ++i) {
        current_path += distance[p[i]][p[i+1]];
    }
    current_path += distance[p[n-1]][p]; // Povratak na početak

    if (min_path == -1 || current_path < min_path) {
        min_path = current_path;
    }
} while (next_permutation(p.begin(), p.end()));

cout << min_path << '\n';
```

**Složenost:** O(n * n!), jer ima `n!` permutacija, a za svaku računamo duljinu puta u O(n).

### Problem 3: N-kraljica problem (Backtracking)

**Zadatak:** Na šahovsku ploču dimenzija `n x n` postavi `n` kraljica tako da se nikoje dvije ne napadaju. Prebroji broj mogućih rješenja.

**Rješenje:** Koristimo backtracking. Postavljamo jednu kraljicu po retku.

**Algoritam:**
Definiramo rekurzivnu funkciju `search(y)` koja pokušava postaviti kraljicu u red `y`.

1. **Bazni slučaj:** Ako je `y == n`, uspjeli smo postaviti svih `n` kraljica. Povećaj brojač rješenja.
2. **Rekurzivni korak:** Za svaku stupac `x` u retku `y`:
    * Provjeri je li pozicija `(y, x)` sigurna (ne napada je nijedna prethodno postavljena kraljica).
    * Ako je sigurna:
        * Označi poziciju kao zauzetu.
        * Pozovi `search(y + 1)`.
        * **Backtrack:** Poništi oznaku zauzetosti kako bi se omogućila pretraga drugih mogućnosti.

**Kod:** Za efikasnu provjeru sigurnosti, koristimo pomoćna polja za stupce i dijagonale.

```cpp
int n;
int count = 0;
vector<bool> column, diag1, diag2;

void search(int y) {
    if (y == n) {
        count++;
        return;
    }
    for (int x = 0; x < n; ++x) {
        // Provjera je li pozicija (y, x) sigurna
        if (column[x] || diag1[x+y] || diag2[x-y+n-1]) continue;

        // Postavi kraljicu
        column[x] = diag1[x+y] = diag2[x-y+n-1] = true;
        
        search(y + 1);

        // Backtrack
        column[x] = diag1[x+y] = diag2[x-y+n-1] = false;
    }
}

// U main funkciji:
// ... čitanje n ...
column.resize(n, false);
diag1.resize(2*n-1, false);
diag2.resize(2*n-1, false);
search(0);
cout << count << '\n';
```

**Analiza:** Iako je složenost i dalje eksponencijalna, `pruning` (preskakanje grana stabla pretrage gdje postoji konflikt) drastično smanjuje broj stanja koje moramo istražiti u odnosu na naivno isprobavanje svih `n^n` mogućih pozicija.

---

## Zadaci za Vježbu

## Zadatak 1: Generiranje podskupova

Zadan je skup $\{0, 1, 2, ..., n\}$, s pomoću rekurzije generirajte sve podskupove od zadanoga skupa.
Prilikom ispisa ne treba voditi računa o redoslijedu ispisa podskupova.

**Primjer**

**Input:**

```text
0 1 2
```

**Output:**

```text
[]
[2]
[1]
[1, 2]
[0]
[0, 2]
[0, 1]
[0, 1, 2]
```

{: .highlight }
`[]` označava prazan skup $\emptyset$.

## Zadatak 2: K-sum

Provjerite ako u zadanoj listi $l$ postoji podlista ${a_1, ..., a_n}$ takva da je njena suma $k$?

**Input:**
U prvoj liniji unosi se tražena suma $k$, u drugoj broj elemenata u listi $n$,
a u tre'oj lista cijelih brojeva $l$.

**Output:**
Ispis brojeva čija suma iznosi $k$.

**Primjer**

**Input:**

```text
6
3
1 2 4
```

**Output:**

```text
2 4
```

## Zadatak 3: K-sum Meet in the middle

S pomoću metode Meet in the middle provjerite ako u zadanoj listi $l$ postoji skup ${a_1, ..., a_n}$ takva da je njena suma $k$?

Razmotrimo problem gdje nam je dana lista $l$ koja sadržava $n$ brojeva i broj $k$, te želimo saznati ako je moguće odabrati brojeve s liste $l$ tako da njihov zbroj bude $k$.

**Input:**
U prvoj liniji unosi se tražena suma $k$, a u drugoj lista cijelih brojeva $l$.

**Output:**
Ispis "YES" ako je moguće generirati sumu, u protivnom se ispisuje -1.

**Input:**

```text
15
2,4,5,9
```

**Output:**

```text
YES
```

**Input:**

```text
15
7,11,5,9
```

**Output:**

```text
-1
```

## Zadatak 4: Stvaranje stringova

Za zadani string $s$, zadatak je generirati sve različite stringove koji se mogu stvoriti s pomoću znakova iz zadanog stringa $s$.

**Input:**
Ulazni string duljine $n$ ($1 \le n \le 7$), koji se sastoji od slova od a do z.

**Output:**
Prvo ispišite cijeli broj $k$: ukupan broj stringova. Zatim u $k$ redaka ispišite stvorene stringove.

### Primjer

**Input:**

```text
aabac
```

**Output:**

```text
20
aaabc
aaacb
aabac
aabca
aacab
aacba
abaac
abaca
abcaa
acaab
acaba
acbaa
baaac
baaca
bacaa
bcaaa
caaab
caaba
cabaa
cbaaa
```

## Zadatak 5: Postavljanje N-kraljica

Napišite program koji traži od korisnika da unese broj `n`, što predstavlja veličinu šahovske ploče (n x n). Program treba izračunati i ispisati broj mogućnosti za postavljanje `n` kraljica na šahovskoj ploči tako da nijedna kraljica ne napada drugu. Kraljica može napasti u svim smjerovima: horizontalno, vertikalno i dijagonalno.

**Ulaz**

* Jedan cijeli broj `n` (1 ≤ n ≤ 15), koji predstavlja veličinu šahovske ploče.

**Izlaz**

* Jedan cijeli broj, koji predstavlja broj mogućnosti za postavljanje `n` kraljica na šahovskoj ploči.

### Primjer 1

**Ulaz:**

```text
4
```

**Izlaz:**

```text
2
```

### Primjer 2

**Ulaz:**

```text
5
```

**Izlaz:**

```text
10
```

### CSES Problem Set ([https://cses.fi/problemset/](https://cses.fi/problemset/))

* **[Apple Division](https://cses.fi/problemset/task/1623):** Zadan je skup težina. Podijeli ga na dva podskupa tako da je razlika njihovih zbrojeva minimalna. (Klasičan problem koji se rješava generiranjem podskupova).
* **[Creating Strings](https://cses.fi/problemset/task/1622):** Zadan je string. Ispiši sve različite permutacije (anagrame) stringa.
* **[Chessboard and Queens](https://cses.fi/problemset/task/1624):** Varijacija N-kraljica problema gdje su neka polja zabranjena.
* **[Grid Paths](https://cses.fi/problemset/task/1625):** Pronađi broj puteva od gornjeg lijevog do donjeg desnog kuta `7x7` mreže koji posjećuju svako polje točno jednom. (Klasičan backtracking s jakim pruningom).

### Codeforces

Na stracnici Codeforces možete riješavati zadatke iz kategorije `brute force` težijne `800` i `900`, koje možete pronaći na [poveznici](https://codeforces.com/problemset?tags=greedy,-900).

[Sljedeća lekcija: Potpuna pretraga i backtracking](../04-Greedy-Algorithms/){: .btn .btn-purple .float-right}
