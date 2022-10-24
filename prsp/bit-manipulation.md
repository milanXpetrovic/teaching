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
- Pomicanje bita - Lijevi pomak bita `x << k `dodaje $k$ nula bitova broju, a desni pomak bita `x >> k` uklanja zadnjih $k$ bitova iz broja. Na primjer, `14 << 2 = 56`, jer 14 i 56 odgovaraju 1110 i 111000. Slično, `49 >> 3 = 6`, jer 49 i 6 odgovaraju 110001 i 110. Imajte na umu da x << k odgovara množenju $x$ s $2^k$, a `x >> k` odgovara dijeljenju $x$ s $2^k$ zaokruženo na cijeli broj.



## Zadatak 1: 

**Input:**
**Output:**

### Primjer
**Input:**
```
```
**Output:**
```
```