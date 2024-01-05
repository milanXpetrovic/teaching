---
layout: default
parent: PRSP
nav_order: 1
---

# Uvod

## Zadatak 1

Mladom asistentu potreban je program s pomoću kojeg provjerava ako je student ostvario pravo pristupa završnom ispitu. U program unosite ime studenta, broj ostvarenih bodova na kolokviju i ukupan broj bodova koji je prikupio tijekom semestra.

Student ima pravo pristupa završnom ako je prikupio 50% ili više bodova na kolokviju i ako je prikupio 35 ili više bodova tijekom semestra.

**Input**
Unos u program se sastoji od imena studenta, broja bodova na kolokviju $$k$$ $(0 <= k <= 30)$ i broj bodova prikupljenih tijekom semestra $s$

**Output**
Ispišite "Student `<ime studenta>` je ostvario pravo izlaska na završni ispit."

### Primjer

**Input:**

```text
Marko 20 50
```

**Output:**

```text
Student Marko je ostvario pravo izlaska na završni ispit.
```

## Zadatak 2

Potrebno je s pomoću for petlji kreirati zadani uzorak:

```text
1 
1 2 
1 2 3 
1 2 3 4 
```

**Input:** Visina piramide $n$ $(1 <= n <= 15)$

### Primjer

**Input:**

```text
5
```

**Output:**

```text
1 
1 2 
1 2 3 
1 2 3 4 
1 2 3 4 5
```

## Zadatak 3

Tijekom ljetnog odmora odlučili ste posjetiti kolegu koji je radio u restoranu. Ožednjeli ste i odlučili ste popiti piće da se osvježite. Sa sobom ste donijeli određenu svotu novca te morate provjeriti što si možete priuštiti.

**Input:**
Prvi unos u program je svota novca $n$ $(1 <= n <= 15)$. Sljedeći unos je lista $l$ koja sadrži cijene pića.

**Output:**
Sastoji se od liste s vrijednostima $1$ i $0$. Ako je vrijednost u listi $l$ manja ili jednaka vrijednosti $n$ onda iznosi $1$ inače je $0$.

### Primjer

**Input:**

```text
20
7 13 11 20 26 29 12 13 22 28 
```

**Output:**

```text
1 1 1 1 0 0 1 1 0 0
```

[Sljedeća lekcija: Vremenska složenost](../vremenska-slozenost){: .btn .btn-purple .float-right}
