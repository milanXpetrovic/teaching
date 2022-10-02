---
---

# Vježbe 1: Uvod

## Uvod u kolegij

Obaveze na vježbama: Kolokvij i završni (praktični dio)
Prag na kolokviju i završnom: 50%

Potrebno poznavanje osnoba u programskom jeziku [Python](https://www.python.org/)

## Vjezbe 1:

### Zadatak 1

Mladom asistentu Petroviću potreban je program pomoću kojeg provjerava ako je student ostvario pravo pristupa završnom ispitu. U program unosite ime studenta, broj ostvarenih bodova na kolokviju i ukupan broj bodova koji je prikupio tijekom semestra.

Student ima pravo pristupa završnom ako je prikupiuo 50% ili više bodova na kolokviju i ako je prikupio 35 ili više bodova tijekom semestra.

**Input**
Unos u program se sastoji od imena studenta, broja bodova na kolokviju $k$ $(0 <= k <= 30)$ i broj bodova prikupljenih tokom semestra $s$

**Output**
Ispišite "Student `<ime studenta>` je ostvario pravo izlaska na završni ispit."

#### Primjer

**Input:**
```
Marko 20 50
```

**Output:**
```
Student Marko je ostvario pravo izlaska na završni ispit.
```

### Zadatak 2

Potrebno je pomoću for petlji kreirati zadani uzorak:
```
1 
1 2 
1 2 3 
1 2 3 4 
```


**Input:** Visina piramide $n$ $(1 <= n <= 15)$

#### Primjer

**Input:**
```
5
```

**Output:**
```
1 
1 2 
1 2 3 
1 2 3 4 
1 2 3 4 5
```

### Zadatak 3

Tijekom ljetnog odmora odlučili ste posjetiti kolegu koji je radio u restoranu. Ožednili ste i odlučili ste popiti piće da se osvježite. Sa sobom ste donjeli određenu svotu novca te morate provjeriti što si možete priuštiti.

**Input:**
Prvi unos u program je svota novca $n$ $(1 <= n <= 15)$. Sljedeći unos je lista $l$ koja sadrži cjene pića.

**Output:**
Sastoji se od liste sa vrijednostima $1$ i $0$. Ako je vrijednost u listi $l$ manja ili jednaka vrijednosti $n$ onda iznosi $1$ inače je $0$.

#### Primjer

**Input:**
```
20
7 13 11 20 26 29 12 13 22 28 
```


**Output:**
```
1 1 1 1 0 0 1 1 0 0
```

---