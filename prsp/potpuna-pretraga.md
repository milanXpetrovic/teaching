# Vježbe 3: Potpuna pretraga

Potpuna pretraga (*eng. Complete search*) opća je metoda koja se može koristiti za rješavanje gotovo svakog algoritamskog problema. Ideja je generirati sva moguća rješenja problema korištenjem grube sile (*eng. brute force*), a zatim odabrati najbolje rješenje ili prebrojati rješenja, ovisno o problemu.
Potpuna pretraga dobra je tehnika ako ima dovoljno vremena za prolazak kroz sva rješenja, jer je pretragu obično lako provesti i uvijek daje točan odgovor. Ako je potpuna pretraga prespora, možda će biti potrebne druge tehnike, poput pohlepnih algoritama ili dinamičkog programiranja.

- [ ] Uvod 1: rekurzija, generiranje podskupova
- [ ] Uvod 2: brute force
- [ ] Uvod 3: complete search
- [ ] Zadatak 1: Generiranje permutacija
- [ ] Zadatak 2: Backtracking
- [ ] Bonus: Meet in the middle

### Uvod

Zadan je skup $\{0, 1, 2, ..., n\}$, pomoću rekurzije generirajte sve podskupove od zadanoga skupa.
Prilikom ispisa ne treba voditi računa o redosljedu ispisa podskupova.

#### Primjer

**Input:**
```
0 1 2
```

**Output:**
```
[]
[2]
[1]
[1, 2]
[0]
[0, 2]
[0, 1]
[0, 1, 2]
```

**Napomena: ** `[]` označava prazan skup $\emptyset$.

# Uvod 2

Kreirajte program koji pogadja lozinku koja se sastoji od 6 nasumicno odabranih cjelih brojeva.

Ispišite vrijeme koje je bilo potrebno za pogoditi lozinku

# Uvod 3

Kreirajte program koji za zadani broj godine, pronađite minimalni broj godine koji je strogo veći od zadanog i ima samo različite znamenke.

Napišite program koji na za zadanu goidnu traži prvu sljedeću godinu koja sadrži sve različite znamenke.


**Input:**
Cijeli broj $y$ $(1000 ≤ y ≤ 9000)$ koji označava broj godine.

**Output:**

Cijeli broj - minimalna vrijednost godine koja je striktno veća od $y$ i sve znamenke su različite.

#### Primjer

**Input:**
```
1987
```
**Output:**
```
2013
```

**Input:**
```
2013
```
**Output:**
```
2014
```

# Zadatak 1

``` python

## https://codeforces.com/problemset/problem/352/A
## Zadano je n karti na svakoj karti nalayi se broj 0 ili 5. 
## pronadite najveci broj koji mozete generirati od dobivenih karti da je djeljiv sa 90.

from itertools import permutations

l = [x for x in input().split(" ")]
len_l = len(l)

max_n = -1

p = list(set(list(permutations(l, len_l))))
p = [int(n) for n in p]

for n in p:

    if len_l > len(n):
        continue

    if int(n) % 90 == 0:
        max_n = max(max_n, n)

print(max_n)
```

## Zadatak 2

U prostoriji dimenzija a x b potrebno je smjestiti n učenika. Oko svakog učenika potrebno je ostaviti jedno polje razmaka.

**Input:**
a b, dimenzije prostorije
n broj studenata

**Output:**
Ispiši 1 ako je moguće u zadanu prostoriju smjestiti n učenika inače -1.


Input
4, 4
3
Output
1

## Zadatak 3

Meet in the midle

Pronađi ako je moguće iz zadane liste brojeva l, zbrajanjem njenih članova dobiti broj x.