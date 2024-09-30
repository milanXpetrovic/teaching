---
layout: default
title: Usmjereni graf
parent: Grafovi
grand_parent: PRSP
nav_order: 5
---

#[Usmjereni grafovi](https://cses.fi/book/book.pdf#chapter.16)



## Zadatak 9: Upis predmeta

U zadanom usmjerenom grafu, vrhovi predstavljaju predmete, neki od tih predmeta imaju predmete koji prethodno moraju biti položeni da bi se mogli upisati što je predstavljeno vezama. Odnosno, veza iz vrha A u vrh B nam predstavlja da je predmet A preduvjet za upisati predmet B.

Pomoću topološkog sortiranja ispišite redosljed polaganja predmeta tako da se ne dogodi problem s upisom predmeta a da pritom nije položen predmet koji je preduvjet.

**Input:**
U prvom retku za unos nalaze se dva cijela broja $n$ i $m$: broj predmeta, nakon toga slijedi $m$ redaka koji navode veze.

**Output:**
Ispišite topološki sortirani graf.

**Input:**

```text
A B
A C
B D
B E
C F
```

**Output:**

```text
A C F B E D
```