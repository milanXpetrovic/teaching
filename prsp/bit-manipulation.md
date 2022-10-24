---
layout: default
parent: PRSP
nav_order: 6
---

# Bit manipulation
Svi podaci u računalnim programima interno su pohranjeni kao bitovi, tj. kao brojevi 0 i 1. Ovo poglavlje raspravlja o bit reprezentaciji cijelih brojeva i pokazuje primjere kako koristiti operacije s bitovima. Ispostavilo se da postoje mnoge upotrebe za manipulaciju bitovima u programiranju algoritama. Operacije koje se korisete u zdacima:
- and (`&`) - Operacija `x & y` daje broj koji ima jedan bit na mjestima gdje i $x$ i $y$ imaju jedan bit. 
- or (`|`) - Operacija or `x | y` daje broj koji ima jedan bit na pozicijama gdje ili $x$ ili $y$ ima jedan bit.
- xor (`^`) - Operacija `x ^ y` daje broj koji ima jedan bit na mjestima gdje točno jedan od $x$ i $y$ ima jedan bit.
- not (`~`) - Operacija `~x` daje broj gdje su bili svi bitovi od $x$
obrnuti.
- Pomicanje bita - Lijevi pomak bita `x << k `dodaje $k$ nula bitova broju, a desni pomak bita `x >> k` uklanja zadnjih $k$ bitova iz broja. Na primjer, `14 << 2 = 56`, jer 14 i 56 odgovaraju 1110 i 111000. Slično, `49 >> 3 = 6`, jer 49 i 6 odgovaraju 110001 i 110. Imajte na umu da `x << k` odgovara množenju $x$ s $2^k$, a `x >> k` odgovara dijeljenju $x$ s $2^k$ zaokruženo na cijeli broj.


## Zadatak 1: Element bez ponavljanja
U zadanoj listi cjelih brojeva $l$ svi elementi se ponavljaju osim jednog. Potrebno je pronaći taj element. 

Rješenje mora biti implementirano s linearnom složenošću vremena izvođenja i konstantnom prostornom složenošću.

**Input:**
Lista cjelih brojeva $l$.

**Output:**
Cjeli broj $k$ koji se ne ponavlja u zadanoj listi $l$.

### Primjeri
**Input:**
```
2 2 1
```
**Output:**
```
1
```
**Input:**
```
2 3 2 1 5 3 1
```
**Output:**
```
5
```

## Zadatak 2: Hammingova težina

Napišite program koji prima kao input cijeli broj u binarnom formatu i vraća broj bitova '1' koje ima (poznato i kao Hammingova težina).

{: .highlight-title}
> Unos binarnih brojeva
>
> U Pythonu binarne brojeve možete unositi kao string i pretvarati ih > u int pomoću `int(s,2)`, gdje je `s` uneseni string.

**Input:**
String $s$ koji reprezentira zadani binarni broj.

**Output:**
Broj $k$ koji označava ukupan broj `1` u zadanom stringu.

### Primjer
**Input:**
```
0001011
```
**Output:**
```
3
```

## Zadatak 3: Nedostaje broj
U program se unosi lista $l$ koja sadrži $n$ cjelobrojnih vrijednosti koje su u rasponu od $0$ do $n$, u unesenoj listi nedostaje jedan broj iz intervala od $0$ do $n$. Program zatim ispisuje broj koji nedostaje u unesenoj listi.

**Input:**
Lista cjelih brojeva $l$.

**Output:**
Broj $k$ koji nedostaje u listi $l$.

### Primjeri
**Input:**
```
0 1 3
```
**Output:**
```
2
```
**Input:**
```
9 0 1 5 3 2 4 6 8 
```
**Output:**
```
7
```