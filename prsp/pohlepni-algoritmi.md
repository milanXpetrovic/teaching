---
layout: default
parent: PRSP
nav_order: 4
---

# Pohlepni algoritmi
Pohlepni algoritam (eng. greedy algorithm) konstruira rješenje problema tako da uvijek odabire izbor koji u ovom trenutku izgleda najbolje. Pohlepni algoritam nikada ne povlači svoje odabire, već izravno konstruira konačno rješenje. Zbog toga su pohlepni algoritmi vrlo učinkoviti. Poteškoća u dizajniranju pohlepnih algoritama je pronaći pohlepnu strategiju koja uvijek proizvodi optimalno rješenje problema. Lokalno optimalni izbori u pohlepnom algoritmu također bi trebali biti globalno optimalni. Često je teško tvrditi da pohlepni algoritam radi.

## Zadatak 1: Problem s kovanicama
Razmatramo problem u kojem nam je dan skup kovanica $\{c_1, c_2, c_3,...,c_k\}$ i naš je zadatak oblikovati svotu novca $n$, pritom svaku kovanicu možemo koristiti koliko kod puta želimo. Koji je minimalan broj potrebnih kovanica?

Na primjer zadane su kovanice : $\{1, 2, 5, 10, 20, 50, 100, 200\}$. Zadatak je pomoću danih kovanica kreirati iznos $n$

Napišite program koji kao ulaz prima cijeli broj $n$ a kao rješenje ispisuje kovanice pomoću koji se može kreirati broj $n$, cilj programa je koristiti najmanji mogući broj kovanica, odnosno pohlepni pristup.

**Input:**
Cijeli broj $n$ $(1 <= n <= 10000)$ koji označava traženu sumu.

**Output:**
Lista vrijednosti na kovanicama $\{c_1, c_2, c_3,...,c_k\}$ na kovanicama.

**Input:**
```
530
```

**Output:**
```
200 200 100 20 10
```


## Zadatak 2: Kompresija podataka
{: .highlight-title}
> Tema seminara
>
> Huffman Data Compression

| character | codeword |
| --------- | -------- |
| A         | 00       |
| B         | 01       |
| C         | 10       |
| D         | 11       |

**Input:**
AABACDACA

**Output:**
000001001011001000


## Zadatak 3: Zakazivanje aktivnosti

Organiziraj upis predmeta tako da student upiše maksimalan broj predmeta bez preklapanja.

**Input:**
Prvi red sadrži jedan cijeli broj $c$ $(1 \le c \le 10^3)$ - broj testnih slučajeva.
Sljedećih $c$ linija sadržava dva cijela broja $t_start$ i $t_end$ koji označuju vrijeme početka i završetka predmeta.

**Output:**
Ispis popisa vremena $t_1$ i $t_2$ za predmete koje će student upisati.

### Primjer

**Input:**
```
7
8 9
11 13
9 10
8 14
15 17
10 12
8 10
```

**Output:**
```
8 9
9 10
10 12
15 17
```


## Zadatak 4: Domino
https://codeforces.com/problemset/problem/50/A

**Input:**

**Output:**

### Primjer

**Input:**
```
```

**Output:**
```
```


## Zadatak 5: 

**Input:**

**Output:**

### Primjer

**Input:**
```
```

**Output:**
```
```