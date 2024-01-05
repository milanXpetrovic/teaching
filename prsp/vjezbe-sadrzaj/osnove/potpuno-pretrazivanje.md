---
parent: PRSP
nav_order: 3
---

# [Potpuno pretraživanje](https://cses.fi/book/book.pdf#chapter.5)

Potpuno pretraživanje (*eng. Complete search*) opća je metoda koja se može koristiti za rješavanje gotovo svakog algoritamskog problema. Ideja je generirati sva moguća rješenja problema korištenjem grube sile (*eng. brute force*), a zatim odabrati najbolje rješenje ili prebrojati rješenja, ovisno o problemu.
Potpuna pretraga dobra je tehnika ako ima dovoljno vremena za prolazak kroz sva rješenja, jer je pretragu obično lako provesti i uvijek daje rješenje. Ako je potpuna pretraga prespora, možda će biti potrebne druge tehnike, poput pohlepnih algoritama ili dinamičkog programiranja.

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

## Zadatak 2: Binarna reprezentacija

Riješite prethodni zadatak s pomoću reprezentacije brojeva u binarnom zapisu.

{: .highlight }
> Da bi `x` pretvorili u binarni zapis možete koristiti `format(x, 'b')`.
>
> Funkcija `zfill(n)`, popunjava string s `0` dok on nema duljinu `n`.

## Zadatak 3: K-sum binarno

S pomoću binarne reprezentacije provjerite ako u zadanoj listi $l$ postoji podlista ${a_1, ..., a_n}$ takva da je njena suma $k$?

**Input:**
U prvoj liniji unosi se tražena suma $k$, a u drugoj lista cijelih brojeva $l$.

**Output:**
Ispis brojeva čija suma iznosi $k$.

## Zadatak 4: K-sum Meet in the middle

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

## Zadatak 5: Stvaranje stringova

Za zadani string $s$, zadatak je generirati sve različite stringove koji se mogu stvoriti s pomoću znakova iz zadanog stringa $s$.

{: .highlight }
Za generiranje permutacija može se koristiti funkcija `permutations` koja se poziva s pomoću `from itertools import permutations`.

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

## Zadatak 6: Niz

Razmotrimo znakovni niz koji se sastoji od svih pozitivnih cijelih brojeva u rastućem redoslijedu:

```text
12345678910111213141516171819202122232425...
```

Zadatak je pronaći u $q$ upita koja znamenka se nalazi na poziciji $k$.

Polje kreće od indeksa 1, tako će primjerice upit za broj 6, vratiti broj 6 a ne 7.

**Input:**
Prva linija sadrži broj $q$ koji nam govori koliko imamo upita.
Nakon toga slijedi $q$ linija gdje se nalazi $k$, odnosno indeks broja kojeg tražimo.

**Output:**
Za svaki upit ispišite pronađenu znamenku na indeksu $k$.

**Input:**

```text
3
7
19
12
```

**Output:**

```text
7
4
1
```

## Dodatni zadaci

- [Chessboard and Queens](https://cses.fi/problemset/task/1624)
- [Grid Paths](https://cses.fi/problemset/task/1625)
- [Sail](https://codeforces.com/problemset/problem/298/B)