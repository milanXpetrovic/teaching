---
parent: PRSP
nav_order: 3
---

# Potpuno pretraživanje

Potpuno pretraživanje (*eng. Complete search*) opća je metoda koja se može koristiti za rješavanje gotovo svakog algoritamskog problema. Ideja je generirati sva moguća rješenja problema korištenjem grube sile (*eng. brute force*), a zatim odabrati najbolje rješenje ili prebrojati rješenja, ovisno o problemu.
Potpuna pretraga dobra je tehnika ako ima dovoljno vremena za prolazak kroz sva rješenja, jer je pretragu obično lako provesti i uvijek daje rješenje. Ako je potpuna pretraga prespora, možda će biti potrebne druge tehnike, poput pohlepnih algoritama ili dinamičkog programiranja.

## Zadatak 1: Generiranje podskupova

Zadan je skup $\{0, 1, 2, ..., n\}$, pomoću rekurzije generirajte sve podskupove od zadanoga skupa.
Prilikom ispisa ne treba voditi računa o redoslijedu ispisa podskupova.

### Primjer

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

{: .highlight }
`[]` označava prazan skup $\emptyset$.


## Zadatak 2: Binarna reprezentacija

Riješite prethodni zadatak pomoću reprezentacije brojeva u bianrnom zapisu.


## Zadatak 3: K-sum binarno

U zadanoj listi $l$ postoji li podlista ${a_1, ..., a_n}$ takva da je njena suma $k$?

**Input:**
U prvoj liniji unosi se tražena suma $k$, a u drugoj lista cjelih brojeva $l$.

**Output:**
Ispis brojeva čija suma iznosi $k$.


## Zadatak 3: K-sum Meet in the middle
Riješite prethodni zadatak pomoću metode Meet in the middle.


## Zadatak 4: Broj puteva koji pokrivaju polje

Zadano je polje dimenzija $n \times m$. Potrebno je odrediti koliko puteva postoji u polju koji počinju u gornjem lijevom kutu i zavšavaju u donjem desnom kutu. Put kroz polje mora posjetiti sva polja točno jednom.

**Input:**
Input su cjeli brojevi $n$ i $m$, gdje su ograničenja $3 \le n, m \le 6$.

**Output:**
Cjeli broj $k$ koji označuje broj puteva.ž

### Primjer
**Input:**
```
```
**Output:**
```
```


## Zadatak 5: Stvaranje stringova
Za zadani string $s$, zadatak je generirati sve različite string koji se mogu stvoriti pomoću znakova iz zadanog stringa. $s$.

**Input:**
Ulazni string duljine $n$ ($1 \le n \le 7$), koji se sastoji od slova od a do z.

**Output:**
Prvo ispišite cijeli broj $k$: ukupan broj stringova. Zatim u $k$ redaka ispišite stvorene stringove.

### Primjer
**Input:**
```
aabac
```

**Output:**
```
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

## Zadatak 6: Različite znamenke 
Kreirajte program koji za zadani broj godine, pronađite minimalni broj godine koji je strogo veći od zadanog i ima sve različite znamenke.

Napišite program koji na za zadanu godinu traži prvu sljedeću godinu koja sadrži sve različite znamenke.

**Input:**
Cijeli broj $y$ $(1000 ≤ y ≤ 9000)$ koji označava broj godine.

**Output:**
Cijeli broj - minimalna vrijednost godine koja je striktno veća od $y$ i sve znamenke su različite.

### Primjer
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


