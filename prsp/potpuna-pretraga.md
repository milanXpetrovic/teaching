---
parent: PRSP
nav_order: 3
---

# Vježbe 3: Potpuna pretraga

Potpuna pretraga (*eng. Complete search*) opća je metoda koja se može koristiti za rješavanje gotovo svakog algoritamskog problema. Ideja je generirati sva moguća rješenja problema korištenjem grube sile (*eng. brute force*), a zatim odabrati najbolje rješenje ili prebrojati rješenja, ovisno o problemu.
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


## Zadatak 2: Problem $n$ kraljica 
Problem $n$ kraljica je problem postavljanja $n$ kraljica na šahovsku ploču dimenzija $n \times n$ tako da se kraljice međusobno ne napadaju. Cilj je odrediti ukupan broj načina postavljanja kraljica na ploču.

{: .highlight-title}
> Kako kraljica napada?
>
> Prikaz ploče dimenzija 8 x 8 i polja koja kraljica (Q) napada (\*).
>
> ```
> -  –  *  –  –  –  *  –
> –  –  *  –  -  *  –  –
> *  –  *  –  *  –  –  -
> –  *  *  *  –  -  –  –
> *  *  Q  *  *  *  *  *
> –  *  *  *  –  –  -  –
> *  -  *  –  *  –  –  –
> –  –  *  -  –  *  –  –
> ```

U primjeru gdje je $n = 4$, postoje 2 načina za rasporediti kraljice.

```
-  Q  –  –
-  –  –  Q
Q  –  –  –
-  –  Q  –
```

```
-  -  Q  –
Q  –  –  -
-  –  –  Q
-  Q  -  –
```

Zadatak je napisati program koji ispisuje ukupan broj mogućnosti za postavljanje kraljica na ploču.

**Input:**
Broj $n$ označava broj kraljica i dimenzije ploče $n \times n$ $(4 \le n \le 8)$. 

**Output:**
Broj $m$ načina na koje možete postaviti kraljice.


### Primjer
**Input:**
```
4
```

**Output:**
```
2
```

**Input:**
```
8
```

**Output:**
```
92
```


## Zadatak 2: Kombinacije brojeva od 1 do $n$
Za dan pozitivan cijeli broj $n$ $(2 \le n \le 1000)$, ispišite sve kombinacije brojeva između 1 i $n$, gdje njihov zbroj iznosi $n$.

**Input:**
Cijeli broj $n$ $(1 <= n <= 1000)$ koji označava traženu sumu.

**Output:**


### Primjer
**Input:**
```
4
```

**Output:**
```
4
1 3
2 2
1 1 2
1 1 1 1
```

**Input:**
```
5
```

**Output:**
```
5
1 4
2 3
1 1 3
1 2 2
1 1 1 2
1 1 1 1 1
```


## Zadatak 4: Stvaranje stringova
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

## Zadatak 5: Različite znamenke 
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

## Zadatak 6: Pruning the search

**Input:**
**Output:**

### Primjer
**Input:**
```
```
**Output:**
```
```

