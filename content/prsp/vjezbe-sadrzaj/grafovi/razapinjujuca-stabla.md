---
layout: default
title: Razapinjajuca stabla
parent: Grafovi
grand_parent: PRSP
nav_order: 4
---

# [Razapinjajuca stabla](https://cses.fi/book/book.pdf#chapter.15)

## Zadatak 5: Izgradnja cesta

Zemlja ima $n$ gradova i $m$ cesta između njih. Cilj je izgraditi nove ceste tako da postoji ruta između bilo koja dva grada.

Vaš zadatak je saznati minimalan broj potrebnih cesta, te odrediti koje ceste treba izgraditi.

**Input:**
U prvom retku za unos nalaze se dva cijela broja $n$ i $m$: broj gradova i cesta. Gradovi su označeni brojevima $1,2,…,n$.

Nakon toga slijedi $m$ redaka koji opisuju ceste. Svaki red ima dva cijela broja $a$ i $b$: ako postoji cesta između tih gradova.

Cesta uvijek povezuje dva različita grada, a između bilo koja dva grada postoji najviše jedna cesta.

**Output:**
Prvo ispišite cijeli broj $k$: broj potrebnih cesta.

Zatim ispišite $k$ redaka koji opisuju nove ceste. Možete ispisati bilo koje valjano rješenje.

**Input:**

```text
4 2
1 2
3 4
```

**Output:**

```text
1
2 3
```



## Zadatak 8: Popravak ceste

Postoji $n$ gradova i $m$ cesta između njih. Nažalost, stanje na cestama je toliko loše da se ne mogu koristiti. Vaš zadatak je popraviti neke od cesta kako bi između bilo koja dva grada postojala ruta.

Za svaku cestu znate njenu cijenu popravka i trebali biste pronaći rješenje gdje je ukupni trošak što je moguće manji.

**Input:**
U prvom retku za unos nalaze se dva cijela broja $n$ i $m$: broj gradova i cesta. Gradovi su označeni brojevima $1,2,…,n$.

Nakon toga slijedi $m$ redaka koji opisuju ceste. Svaki red ima tri cijela broja a, b i c koji označava da postoji cesta između gradova a i b, a cijena njezine popravke je c. Sve ceste su dvosmjerne.

Sve ceste su između dva različita grada, a između dva grada postoji najviše jedna cesta.

**Output:**

Ispišite jedan cijeli broj: minimalni ukupni trošak popravka. Međutim, ako nema rješenja, ispišite "NEMOGUĆE".

**Input:**

```text
5 6
1 2 3
2 3 5
2 4 2
3 4 8
5 1 7
5 4 4
```

**Output:**

```text
14
```