---
nav_exclude: true
---

# Upiti nad rasponima (Range queries)

## Sadržaj

1. [Uvod i Motivacija](#uvod-i-motivacija)
    * [Što su upiti nad rasponima?](#što-su-upiti-nad-rasponima)
    * [Problem: Naivni pristup je prespor](#problem-naivni-pristup-je-prespor)
    * [Preporučena Literatura](#preporučena-literatura)
2. [Statički Upiti: Prefiksne Sume](#statički-upiti-prefiksnje-sume)
    * [Intuicija i Implementacija](#intuicija-i-implementacija)
    * [Primjena: Upiti o zbroju](#primjena-upiti-o-zbroju)
3. [Dinamički Upiti: Fenwick Stablo](#dinamički-upiti-fenwick-stablo)
    * [Motivacija: Ažuriranje i upiti](#motivacija-ažuriranje-i-upiti)
    * [Intuicija i Struktura](#intuicija-i-struktura)
    * [Implementacija i Analiza](#implementacija-i-analiza)
4. [Dinamički Upiti: Segmentno Stablo](#dinamički-upiti-segmentno-stablo)
    * [Najmoćniji Alat za Raspon](#najmoćniji-alat-za-raspon)
    * [Intuicija i Struktura](#intuicija-i-struktura-1)
    * [Implementacija i Analiza](#implementacija-i-analiza-1)
5. [Zadaci za Vježbu](#zadaci-za-vježbu)

---

## Uvod i Motivacija

### Što su upiti nad rasponima?

Upiti nad rasponima su fundamentalni tip problema gdje trebamo efikasno izračunati neku vrijednost nad kontinuiranim podnizom (rasponom) niza. Najčešći tipovi upita su:

* `sum(a, b)`: Izračunaj zbroj elemenata od indeksa `a` do `b`.
* `min(a, b)`: Pronađi minimalni element u rasponu od `a` do `b`.
* `max(a, b)`: Pronađi maksimalni element u rasponu od `a` do `b`.

### Problem: Naivni pristup je prespor

Naivno rješenje za svaki upit je proći kroz sve elemente u zadanom rasponu.

```cpp
// Naivni pristup za zbroj
long long sum_query(int a, int b) {
    long long sum = 0;
    for (int i = a; i <= b; ++i) {
        sum += array[i];
    }
    return sum;
}
```

Ako imamo `q` upita, a niz ima `n` elemenata, ukupna složenost može biti do **O(q * n)**. Za tipična natjecateljska ograničenja (`n, q ≈ 10^5`), ovo znači `10^10` operacija, što je presporo.

Cilj ovog poglavlja je naučiti strukture podataka koje omogućuju odgovaranje na upite i ažuriranje elemenata u **O(log n)** ili čak **O(1)** vremenu.

### Preporučena Literatura
*   **CPH (Competitive Programmer's Handbook):**
    *   Poglavlje 9: *Range Queries*
*   **CLRS (Introduction to Algorithms):**
    *   Poglavlje 14: *Augmenting Data Structures* (pruža teorijsku osnovu za dodavanje informacija u stabla, što je srž segmentnih stabala).

---

## Statički Upiti: Prefiksne Sume

Ako se niz **nikad ne mijenja** (statičan je), upite o zbroju možemo riješiti izuzetno efikasno.

### Intuicija i Implementacija
**Prefiksne sume** su polje `prefix` gdje `prefix[i]` sadrži zbroj prvih `i` elemenata originalnog niza `array`.
`prefix[i] = array[0] + array[1] + ... + array[i-1]`

Izgradnja ovog polja traje **O(n)**:
```cpp
vector<long long> prefix(n + 1, 0);
for (int i = 0; i < n; ++i) {
    prefix[i+1] = prefix[i] + array[i];
}
```

### Primjena: Upiti o zbroju

Nakon predračunanja, zbroj bilo kojeg raspona `[a, b]` (uključivo) možemo dobiti u **O(1)** vremenu formulom:
`sum(a, b) = prefix[b+1] - prefix[a]`

**Primjer:**
Niz: `[1, 3, 4, 8, 6, 1, 4, 2]`
Prefiksne sume: `[0, 1, 4, 8, 16, 22, 23, 27, 29]`
`sum(3, 6)` = `prefix[7] - prefix[3]` = `27 - 8` = `19`.
(Zbroj je `8+6+1+4=19`).

---

## Dinamički Upiti: Fenwick Stablo (Binary Indexed Tree - BIT)

Što ako se elementi niza mijenjaju između upita? Prefiksne sume više nisu efikasne jer svaka promjena zahtijeva `O(n)` ažuriranje.

### Motivacija: Ažuriranje i upiti

Fenwick stablo (BIT) je struktura koja podržava obje operacije u **O(log n)** vremenu:

1. **Ažuriranje vrijednosti na indeksu `k`**.
2. **Upit o zbroju prefiksa `[0, k]`**.

### Intuicija i Struktura

BIT je pametan način da se zbrojevi raspona, čije su duljine potencije broja 2, spreme u polje. Svaki indeks `k` u BIT-u odgovoran je za zbroj `p(k)` elemenata, gdje je `p(k)` najveća potencija broja 2 koja dijeli `k`.

Ova struktura omogućuje da se bilo koji prefiksni zbroj `sum(0, k)` dekomponira na samo `O(log k)` zbrojeva iz BIT-a.

### Implementacija i Analiza

Ključna operacija je `k & -k`, koja izolira zadnji postavljeni bit u broju `k`.

```cpp
// Dodaje 'delta' na poziciju 'idx'
void update(int idx, int delta) {
    for (; idx < n; idx = idx | (idx + 1))
        bit[idx] += delta;
}

// Vraća zbroj prefiksa [0, r]
long long query(int r) {
    long long res = 0;
    for (; r >= 0; r = (r & (r + 1)) - 1)
        res += bit[r];
    return res;
}

// Zbroj raspona [l, r]
long long query(int l, int r) {
    return query(r) - query(l - 1);
}
```

**Složenost:** I `update` i `query` operacije imaju složenost **O(log n)**. BIT je izuzetno brz u praksi zbog niskih konstantnih faktora.

---

## Dinamički Upiti: Segmentno Stablo

### Najmoćniji Alat za Raspon

Segmentno stablo je svestranija i moćnija struktura od Fenwick stabla. Podržava iste operacije (ažuriranje točke, upit o rasponu) u **O(log n)** vremenu, ali se može lako prilagoditi za različite vrste upita:
* Zbroj (sum)
* Minimum/Maksimum (min/max)
* Najveći zajednički djelitelj (GCD)
* Bitovne operacije (XOR, OR, AND)

### Intuicija i Struktura

Segmentno stablo je **binarno stablo** izgrađeno iznad niza.

* **Listovi** stabla odgovaraju pojedinačnim elementima niza.
* **Unutarnji čvorovi** predstavljaju neki **agregat** (zbroj, minimum...) vrijednosti svoje djece. Svaki čvor pokriva određeni raspon u originalnom nizu. Korijen pokriva cijeli niz.

**Upit:** Upit za raspon `[a, b]` se odgovara kombiniranjem vrijednosti iz `O(log n)` čvorova u stablu koji zajedno pokrivaju traženi raspon.

**Ažuriranje:** Promjena vrijednosti na indeksu `k` zahtijeva ažuriranje svih čvorova na putu od lista `k` do korijena, što je `O(log n)` čvorova.

### Implementacija i Analiza

Implementacija je obično rekurzivna i radi "od vrha prema dolje".

```cpp
vector<long long> tree;
int n;

void build(const vector<int>& a, int v, int tl, int tr) {
    if (tl == tr) {
        tree[v] = a[tl];
    } else {
        int tm = (tl + tr) / 2;
        build(a, 2*v, tl, tm);
        build(a, 2*v+1, tm+1, tr);
        tree[v] = tree[2*v] + tree[2*v+1]; // Kombiniranje
    }
}

long long query(int v, int tl, int tr, int l, int r) {
    if (l > r) return 0;
    if (l == tl && r == tr) return tree[v];
    int tm = (tl + tr) / 2;
    return query(2*v, tl, tm, l, min(r, tm)) + 
           query(2*v+1, tm+1, tr, max(l, tm+1), r);
}

void update(int v, int tl, int tr, int pos, int new_val) {
    if (tl == tr) {
        tree[v] = new_val;
    } else {
        int tm = (tl + tr) / 2;
        if (pos <= tm) {
            update(2*v, tl, tm, pos, new_val);
        } else {
            update(2*v+1, tm+1, tr, pos, new_val);
        }
        tree[v] = tree[2*v] + tree[2*v+1];
    }
}
```

**Složenost:** Izgradnja stabla je **O(n)**. Upiti i ažuriranja su **O(log n)**. Iako je implementacija složenija od Fenwick stabla, njegova fleksibilnost je ogromna prednost.

---

## Zadaci za Vježbu

### CSES Problem Set ([https://cses.fi/problemset/](https://cses.fi/problemset/))

* ***Static Range Sum Queries:** Idealno za vježbu prefiksnih suma.
* ***Static Range Minimum Queries:** Može se riješiti segmentnim stablom. Pokušajte implementirati rješenje za min, a ne za sum.
* ***Dynamic Range Sum Queries:** Riješite problem koristeći Fenwick stablo, a zatim i segmentno stablo, te usporedite implementacije.
* ***Dynamic Range Minimum Queries:** Klasičan problem za segmentno stablo.
* ***Range Xor Queries:** Primjer gdje Fenwick stablo nije direktno primjenjivo, ali segmentno stablo jest. Potrebno je samo promijeniti operaciju spajanja iz `+` u `^` (XOR).
* ***Hotel Queries:** Zanimljiv problem koji zahtijeva pretraživanje po segmentnom stablu. Traži se prvi hotel s dovoljno slobodnih soba, što je nestandardni upit, ali se efikasno rješava rekurzivnom prirodom segmentnog stabla.

### Codeforces

* **Xenia and Bitwise Operations** (Problem 339D): Odličan zadatak za vježbu segmentnog stabla gdje se operacija spajanja (OR ili XOR) mijenja ovisno o razini u stablu.
* **Little Artem and Matrix** (Problem 441E): Problem zahtijeva 2D strukturu, ali se može riješiti s `n` paralelnih segmentnih stabala (jedno za svaki redak), vježbajući primjenu na složenijem problemu.
* **Nested Segments** (Problem 652D): Problem koji se rješava tehnikom "sweep-line" u kombinaciji s Fenwick stablom.
* **Ants in Leaves** (Problem 932D): Problem na stablu koji se rješava tehnikom "binary lifting" i prefiksnim sumama na putu do korijena.

[Sljedeća lekcija: Teorija brojeva i kombinatorika](../13-Number-Theory-and-Combinatorics){: .btn .btn-purple .float-right}
