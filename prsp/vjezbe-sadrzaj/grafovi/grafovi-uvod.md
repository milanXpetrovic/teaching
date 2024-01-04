---
layout: default
parent: PRSP
nav_order: 7
nav_exclude: false
---

# [Grafovi: uvod](https://cses.fi/book/book.pdf#chapter.11)

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
