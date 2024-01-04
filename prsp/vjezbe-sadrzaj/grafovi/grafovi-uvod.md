---
layout: default
parent: PRSP
nav_order: 7
nav_exclude: false
---

# [Grafovi: uvod](https://cses.fi/book/book.pdf#chapter.11)

Mnogi programski problemi mogu se riješiti modeliranjem problema kao problema grafa i korištenjem odgovarajućih algoritmova nad tim grafovima.  Često su grafovi idealni za predstavljanje veza i odnosa među elementima u raznim situacijama. Tipičan primjer grafa je mreža cesta i gradova u zemlji. Ponekad, je graf skriven u problemu i teško ga je otkriti. Ovaj dio vježbi govori o algoritmima nad grafovima.

U sklopu tematske cjeline Grafovi proći ćemo kroz nekoliko ključnih područija koja su:

- [Putovanje kroz graf](.../putovanje-kroz-graf)ž
- [Traženje najkraćeg puta](../najkraci-putovi.md)
- [Stabla](../stabla.md)
- [Razapinjujuća stabla](../razapinjujuca-stabla.md)
- [Usmjereni grafovi](../usmjereni-grafovi.md)
- [Staze i ciklusi](../staze-i-ciklusi.md)
- [Dodatne teme](../grafovi-dodatno.md)

## Stvaranje grafa

```python
def make_adj_dict(n):
    g = {}
    for i in range(0, n):
        neighbours = random.sample(range(0, n), random.randint(0, n))
        neighbours = [str(x) for x in neighbours]
        g.update({str(i): neighbours})

    return g
```

## BFS

```python
def bfs(graph, start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend([i for i in graph[vertex] if i not in list(visited)])

    return visited
```

## DFS

```python
def dfs(graph, start):
    visited, stack = [], [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.append(vertex)
            stack.extend([i for i in graph[vertex] if i not in visited])
    return visited
```

## Zadaci za vježbu

- Isprobajte BFS i DFS algoritam nad grafom veličine 50.

- Ispišite ako u vašem grafu postoje čvorovi iz kojih možemo posjetiti sve ostale čvorove. Ako ne onda ispišite -1.

- Provjerite ako je vaš graf potpuno povezan. Graf je potpuno povezan ako iz svakog čvora možemo posjetiti sve ostale čvorove u grafu.

- Konstruirajte algoritam za bojanje vrhova u vašem grafu, pokušajte odrediti najmanji broj boja potreban za pobojati graf.

- Pronađite najdulji put u vašem grafu.
