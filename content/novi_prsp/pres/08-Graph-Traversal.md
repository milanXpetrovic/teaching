---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Pretraživanje grafova"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!--
Prijedlozi za slike (dodati ručno u prezentaciju):
1. Slajd "Dvije osnovne strategije": slika koja uspoređuje BFS (koncentrični slojevi) i DFS (put koji ide do kraja pa se vraća).
2. Slajd "Problem 1: Najkraći put u labirintu": 2D mreža sa crnim zidovima i obojenim putem.
3. Slajd "Problem 2: Povezane komponente": graf s 3 odvojena "otoka" čvorova.
-->

<!-- _paginate: false -->
<!-- _class: title -->

# Pretraživanje grafova

## DFS, BFS i primjene

---

# Sadržaj

1. **Uvod i reprezentacija grafa**
   * Modeliranje i lista susjedstva
2. **Osnovne strategije**
   * DFS (Depth-First Search)
   * BFS (Breadth-First Search)
3. **Primjeri i algoritmi**
   * Najkraći put u labirintu (BFS)
   * Povezane komponente (DFS)
   * Detekcija ciklusa (DFS)
4. **Zadaci za vježbu**

---

# Uvod: modeliranje problema

Grafovi su moćna apstrakcija. Čvorovi su objekti, bridovi su veze.

**Primjeri iz stvarnog svijeta:**

* **Mreže cesta:** gradovi (čvorovi) i ceste (bridovi).
* **Društvene mreže:** ljudi (čvorovi) i prijateljstva (bridovi).
* **Ovisnosti:** zadaci (čvorovi) i redoslijed izvršavanja (usmjereni bridovi).

> Pretraživanje grafa je temelj za otkrivanje strukture i odnosa.

---

# Reprezentacija: lista susjedstva

Za natjecateljsko programiranje **lista susjedstva** (adjacency list) je standard.
Efikasna je za **rijetke grafove** ($M \ll N^2$).

```cpp
const int MAXN = 1e5 + 5;
vector<int> adj[MAXN]; // Polje vektora

int main() {
    int n, m; cin >> n >> m;

    // Učitavanje m bridova neusmjerenog grafa
    for (int i = 0; i < m; i++) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v); // v je susjed od u
        adj[v].push_back(u); // u je susjed od v
    }
}
```

---

# Dvije osnovne strategije

**1. DFS (Depth-First Search): dubina**

* **Intuicija:** istražujemo jedan put do kraja ("udarimo u zid"), pa se vraćamo (backtrack).
* **Implementacija:** rekurzija (stog).
* **Primjene:** povezane komponente, detekcija ciklusa, topološko sortiranje.

**2. BFS (Breadth-First Search): širina**

* **Intuicija:** širimo se u slojevima (valovi u vodi). Prvo posjetimo sve susjede, pa susjede susjeda.
* **Implementacija:** red (queue).
* **Primjene:** **najkraći put** u grafu bez težina.

---

# BFS vs. DFS na istom grafu

Tražimo put od čvora 1 do cilja (zeleni obrub). Pretraga staje čim posjeti cilj. Broj ispod čvora = redoslijed posjeta.

<style scoped>
.gr-strat { margin-top: 0.4em; }
.gr-strat .chips { font-size: 20px; margin-bottom: 0.5em; }
.gr-strat .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.gr-strat .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gr-strat .row { display: flex; gap: 8px; }
.gr-strat .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-strat .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gr-strat .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.gr-strat .cell.todo .val { color: #b5b5b5; }
.gr-strat .cell.src { background: #f5db7e; }
.gr-strat .cell.best { background: #9fdc9f; }
.gr-strat .cell.cur { background: var(--main); color: #fff; }
.gr-strat .cell.cur .idx, .gr-strat .cell.cur .val { color: #fff; }
.gr-strat .line1, .gr-strat .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.gr-strat .line1 { margin-top: 0.7em; }
.gr-strat .line2 { font-weight: bold; }
.gr-strat .ctrl { margin-top: 0.7em; }
.gr-strat button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gr-strat button:hover { background: var(--main); color: #fff; }
.gr-strat .hint { font-size: 16px; color: #6e6e6e; }
.gr-strat .gwrap { display: flex; justify-content: center; }
.gr-strat svg .edge { stroke: #a0a0a0; stroke-width: 3; transition: stroke .25s; }
.gr-strat svg .edge.tree { stroke: var(--main); stroke-width: 5; }
.gr-strat svg .edge.chk { stroke: #e0a800; stroke-width: 6; }
.gr-strat svg .edge.path { stroke: #2e9e44; stroke-width: 7; }
.gr-strat svg .edge.back { stroke: #d62828; stroke-width: 7; }
.gr-strat svg .node circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.gr-strat svg .node .lbl { font-size: 20px; font-weight: bold; fill: #141414; }
.gr-strat svg .node .sub { font-size: 16px; font-weight: bold; fill: #6e6e6e; }
.gr-strat svg .node.vis circle { fill: #f5db7e; }
.gr-strat svg .node.c1 circle { fill: #a9c5ff; }
.gr-strat svg .node.c2 circle { fill: #ffc58f; }
.gr-strat svg .node.c3 circle { fill: #a8e0a8; }
.gr-strat svg .node.c4 circle { fill: #e3b3ff; }
.gr-strat svg .node.path circle { fill: #9fdc9f; }
.gr-strat svg .node.front circle { stroke: var(--main); stroke-width: 5; stroke-dasharray: 6 4; }
.gr-strat svg .node.bad circle { stroke: #d62828; stroke-width: 5; }
.gr-strat svg .node.cur circle { fill: var(--main); stroke: var(--main); }
.gr-strat svg .node.cur .lbl { fill: #fff; }
.gr-strat .panels { display: flex; gap: 30px; }
.gr-strat .ptitle { font-weight: bold; font-size: 22px; margin-bottom: 4px; }
.gr-strat .line1, .gr-strat .line2 { margin-top: 0.3em; }
.gr-strat svg .node.goal circle { stroke: #2e9e44; stroke-width: 6; }
</style>

<div class="gr-strat" data-pos="1:250,35;2:130,115;3:370,115;4:60,200;5:190,200;6:310,200;7:440,200;8:250,285" data-edges="1-2,1-3,2-4,2-5,3-6,3-7,5-8,8-7" data-target="7">
  <div class="panels">
    <div class="pan"><div class="ptitle">BFS (red)</div><div class="g1"></div></div>
    <div class="pan"><div class="ptitle">DFS (rekurzija / stog)</div><div class="g2"></div></div>
  </div>
  <div class="line1"></div>
  <div class="line2"></div>
  <div class="ctrl">
    <button data-act="prev">← Korak</button><button data-act="next">Korak →</button><button data-act="auto">Auto</button><button data-act="reset">Reset</button>
    <span class="hint">← / → koračaju kroz animaciju, Shift + ← / → mijenja slajd</span>
  </div>
</div>

<script>
(function () {
  // Ovaj blok namjerno ne sadrži znakove manje-od, veće-od ni ampersand,
  // jer ih build pretvara u HTML entitete i ruši skriptu.
  document.querySelectorAll('.gr-strat').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function show(v) { return v === Infinity ? '∞' : String(v); }
    function makeRow(box, count) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }

    var SVGNS = 'http://www.w3.org/2000/svg';
    function svgEl(tag, attrs) {
      var e = document.createElementNS(SVGNS, tag);
      for (var k in attrs) e.setAttribute(k, attrs[k]);
      return e;
    }
    function cp(o) { return JSON.parse(JSON.stringify(o)); }
    function makeGraph(box, posStr, edgeStr, W, H, scale) {
      var svg = svgEl('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W * scale, height: H * scale });
      box.appendChild(svg);
      var pos = {}, ids = [];
      posStr.split(';').forEach(function (t) {
        var a = t.split(':'), xy = a[1].split(',');
        pos[a[0]] = [Number(xy[0]), Number(xy[1])];
        ids.push(Number(a[0]));
      });
      var adj = {}, edges = [];
      ids.forEach(function (id) { adj[id] = []; });
      var eg = svgEl('g', {});
      svg.appendChild(eg);
      edgeStr.split(',').forEach(function (t) {
        var ab = t.split('-').map(Number);
        var line = svgEl('line', { x1: pos[ab[0]][0], y1: pos[ab[0]][1], x2: pos[ab[1]][0], y2: pos[ab[1]][1], 'class': 'edge' });
        eg.appendChild(line);
        edges.push({ a: ab[0], b: ab[1], el: line });
        adj[ab[0]].push(ab[1]);
        adj[ab[1]].push(ab[0]);
      });
      ids.forEach(function (id) { adj[id].sort(function (x, y) { return x - y; }); });
      var nodes = {};
      ids.forEach(function (id) {
        var g = svgEl('g', { 'class': 'node' });
        g.appendChild(svgEl('circle', { cx: pos[id][0], cy: pos[id][1], r: 22 }));
        var t = svgEl('text', { x: pos[id][0], y: pos[id][1] + 7, 'text-anchor': 'middle', 'class': 'lbl' });
        t.textContent = id;
        var sub = svgEl('text', { x: pos[id][0], y: pos[id][1] + 44, 'text-anchor': 'middle', 'class': 'sub' });
        g.appendChild(t);
        g.appendChild(sub);
        svg.appendChild(g);
        nodes[id] = { g: g, sub: sub };
      });
      function edgeKey(a, b) {
        var r = null;
        edges.forEach(function (e) { if (e.a === a ? e.b === b : (e.a === b ? e.b === a : false)) r = e; });
        return r;
      }
      return { ids: ids, adj: adj, edges: edges, nodes: nodes, edge: edgeKey };
    }
    function has(list, x) { return list.indexOf(x) !== -1; }
    function hasEdge(list, a, b) {
      var r = false;
      list.forEach(function (p) { if (p[0] === a ? p[1] === b : (p[0] === b ? p[1] === a : false)) r = true; });
      return r;
    }

    var G1 = makeGraph(root.querySelector('.g1'), root.dataset.pos, root.dataset.edges, 500, 330, 0.9);
    var G2 = makeGraph(root.querySelector('.g2'), root.dataset.pos, root.dataset.edges, 500, 330, 0.9);
    var adj = G1.adj, start = G1.ids[0], target = Number(root.dataset.target);
    function pathFrom(par, t) {
      var p = [t];
      while (p[0] !== start) p.unshift(par[p[0]]);
      return p;
    }

    // BFS: staje kad cilj skine s reda (kao u kodu za labirint)
    var B = [], vis = {}, par = {}, order = [], q = [start], bFound = false;
    vis[start] = true;
    while (q.length) {
      var u = q.shift();
      order.push(u);
      if (u === target) { bFound = true; B.push({ cur: u, order: order.slice(), front: q.slice(), path: [] }); break; }
      adj[u].forEach(function (v) { if (!vis[v]) { vis[v] = true; par[v] = u; q.push(v); } });
      B.push({ cur: u, order: order.slice(), front: q.slice(), path: [] });
    }

    // DFS: staje čim posjeti cilj; stog je tada upravo pronađeni put
    var D = [], dvis = {}, dord = [], stack = [], dFound = false, dPath = [];
    function dfs(u) {
      dvis[u] = true;
      dord.push(u);
      stack.push(u);
      D.push({ cur: u, order: dord.slice(), front: stack.slice(), path: [] });
      if (u === target) { dFound = true; dPath = stack.slice(); return; }
      adj[u].forEach(function (v) { if (!dFound) { if (!dvis[v]) dfs(v); } });
      if (!dFound) stack.pop();
    }
    dfs(start);

    function txt(name, L, k, sep) {
      if (k === L.length) return name + ': cilj je već pronađen, pretraga stoji';
      var st = L[k];
      if (st.cur === target) return name + ' posjet ' + (k + 1) + ': čvor ' + target + ' = cilj  → STOP';
      return name + ' posjet ' + (k + 1) + ': čvor ' + st.cur + '   ' + (name === 'BFS' ? 'red' : 'stog') + ' = [' + st.front.join(sep) + ']';
    }
    var snaps = [{ b: { cur: -1, order: [], front: [start], path: [] }, d: { cur: -1, order: [], front: [], path: [] },
      l1: 'BFS: red = [' + start + ']', l2: 'DFS: stog = [ ]' }];
    var steps = Math.max(B.length, D.length);
    for (var k = 0; k !== steps; k++) {
      snaps.push({ b: B[Math.min(k, B.length - 1)], d: D[Math.min(k, D.length - 1)],
        l1: txt('BFS', B, Math.min(k, B.length), ', '), l2: txt('DFS', D, Math.min(k, D.length), ' → ') });
    }
    var bLast = cp(B[B.length - 1]), dLast = cp(D[D.length - 1]);
    bLast.cur = -1; dLast.cur = -1; bLast.front = []; dLast.front = [];
    bLast.path = bFound ? pathFrom(par, target) : [];
    dLast.path = dFound ? dPath : [];
    snaps.push({ b: bLast, d: dLast,
      l1: bFound ? 'BFS: ' + B.length + ' posjeta, put ' + bLast.path.join(' → ') + ' (' + (bLast.path.length - 1) + ' brida, najkraći)' : 'BFS: cilj nije dostižan',
      l2: dFound ? 'DFS: ' + D.length + ' posjeta, put ' + dLast.path.join(' → ') + ' (' + (dLast.path.length - 1) + ' brida, nije nužno najkraći)' : 'DFS: cilj nije dostižan' });

    function paint(G, st) {
      G.ids.forEach(function (id) {
        var cls = 'node';
        var oi = st.order.indexOf(id);
        if (oi !== -1) cls += ' vis';
        if (has(st.path, id)) cls += ' path';
        if (id === target) cls += ' goal';
        if (has(st.front, id)) cls += ' front';
        if (id === st.cur) cls += ' cur';
        G.nodes[id].g.setAttribute('class', cls);
        G.nodes[id].sub.textContent = oi === -1 ? '' : '#' + (oi + 1);
      });
      G.edges.forEach(function (e) {
        var pi = st.path.indexOf(e.a), pj = st.path.indexOf(e.b);
        var on = pi !== -1 ? (pj !== -1 ? Math.abs(pi - pj) === 1 : false) : false;
        e.el.setAttribute('class', on ? 'edge path' : 'edge');
      });
    }
    function draw(s) { paint(G1, s.b); paint(G2, s.d); }

    var step = 0, timer = null, lastStep = snaps.length - 1;
    function render() {
      var s = snaps[step];
      draw(s);
      line1.textContent = s.l1;
      line2.textContent = s.l2;
    }
    function stopAuto() { clearInterval(timer); timer = null; }
    function next() { if (step !== lastStep) { step++; render(); return true; } stopAuto(); return false; }
    function prev() { if (step !== 0) { step--; render(); return true; } return false; }
    function reset() { stopAuto(); step = 0; render(); }
    var actions = {
      next: next, prev: prev, reset: reset,
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 900); }
    };

    root.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation(); b.blur(); actions[b.dataset.act]();
      });
    });

    // Strelice / razmaknica / klikač prvo koračaju kroz animaciju, a tek na kraju mijenjaju slajd
    window.addEventListener('keydown', function (e) {
      if (e.shiftKey || !slide || !slide.classList.contains('bespoke-marp-active')) return;
      var fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].indexOf(e.key) !== -1;
      var back = ['ArrowLeft', 'ArrowUp', 'PageUp'].indexOf(e.key) !== -1;
      var moved = false;
      if (fwd) moved = next();
      if (back) moved = prev();
      if (moved) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);

    render();
  });
})();
</script>

---

# Problem 1: Najkraći put u labirintu (BFS)

**Zadatak:**
Zadan je labirint (2D mreža, `#` zidovi, `.` prolaz). Treba naći duljinu najkraćeg puta od `A` do `B`.

**Zašto BFS?**
Graf je bez težina (svaki korak košta 1). BFS jamči pronalazak najkraćeg puta jer se širi koncentrično.

**Algoritam:**

1. Stavimo početak `A` u red (`queue`), uz `dist[A] = 0`.
2. Dok red nije prazan:
   * Uzmemo polje `(r, c)`.
   * Za svakog susjeda (gore, dolje, lijevo, desno):
     * Ako je slobodan i neposjećen: `dist[novi] = dist[stari] + 1` i dodamo ga u red.

---

# BFS implementacija (ključni dio)

```cpp
// dist[n][m] inicijaliziran na -1; start (sr, sc), cilj (er, ec)
queue<pair<int, int>> q;
q.push({sr, sc});
dist[sr][sc] = 0;

int dr[] = {-1, 1, 0, 0}; // Smjerovi redaka
int dc[] = {0, 0, -1, 1}; // Smjerovi stupaca

while (!q.empty()) {
    auto [r, c] = q.front(); q.pop();
    if (r == er && c == ec) break; // Nađen cilj

    for (int i = 0; i < 4; ++i) {
        int nr = r + dr[i];
        int nc = c + dc[i];

        // isValid provjerava granice mreže
        if (isValid(nr, nc) && grid[nr][nc] != '#' && dist[nr][nc] == -1) {
            dist[nr][nc] = dist[r][c] + 1;
            q.push({nr, nc});
        }
    }
}
```

**Složenost:** $O(N \cdot M)$. (Ne zovite varijablu `end`: sudara se sa `std::end`.)

---

# BFS u labirintu korak po korak

Plavi okvir = polja u redu, žuto = posjećena, broj = `dist`. Korak = jedno skidanje s reda.

<style scoped>
.gr-maze { margin-top: 0.4em; }
.gr-maze .chips { font-size: 20px; margin-bottom: 0.5em; }
.gr-maze .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.gr-maze .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gr-maze .row { display: flex; gap: 8px; }
.gr-maze .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-maze .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gr-maze .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.gr-maze .cell.todo .val { color: #b5b5b5; }
.gr-maze .cell.src { background: #f5db7e; }
.gr-maze .cell.best { background: #9fdc9f; }
.gr-maze .cell.cur { background: var(--main); color: #fff; }
.gr-maze .cell.cur .idx, .gr-maze .cell.cur .val { color: #fff; }
.gr-maze .line1, .gr-maze .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.gr-maze .line1 { margin-top: 0.7em; }
.gr-maze .line2 { font-weight: bold; }
.gr-maze .ctrl { margin-top: 0.7em; }
.gr-maze button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gr-maze button:hover { background: var(--main); color: #fff; }
.gr-maze .hint { font-size: 16px; color: #6e6e6e; }
.gr-maze .grid { display: grid; gap: 4px; justify-content: start; }
.gr-maze .gc { height: 48px; line-height: 44px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 5px; transition: background-color .25s, color .25s; }
.gr-maze .gc.wall { background: #141414; }
.gr-maze .gc.vis { background: #f5db7e; }
.gr-maze .gc.front { box-shadow: inset 0 0 0 4px var(--main); }
.gr-maze .gc.path { background: #9fdc9f; }
.gr-maze .gc.r1 { background: #a9c5ff; }
.gr-maze .gc.r2 { background: #ffc58f; }
.gr-maze .gc.r3 { background: #a8e0a8; }
.gr-maze .gc.r4 { background: #e3b3ff; }
.gr-maze .gc.cur { background: var(--main); color: #fff; }
</style>

<div class="gr-maze" data-grid="A..#.....|.#.#.###.|.#...#...|.####.#B.|......#..">
  <div class="grid"></div>
  <div class="line1"></div>
  <div class="line2"></div>
  <div class="ctrl">
    <button data-act="prev">← Korak</button><button data-act="next">Korak →</button><button data-act="auto">Auto</button><button data-act="reset">Reset</button>
    <span class="hint">← / → koračaju kroz animaciju, Shift + ← / → mijenja slajd</span>
  </div>
</div>

<script>
(function () {
  // Ovaj blok namjerno ne sadrži znakove manje-od, veće-od ni ampersand,
  // jer ih build pretvara u HTML entitete i ruši skriptu.
  document.querySelectorAll('.gr-maze').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function show(v) { return v === Infinity ? '∞' : String(v); }
    function makeRow(box, count) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }

    function cp(o) { return JSON.parse(JSON.stringify(o)); }
    var DR = [-1, 1, 0, 0], DC = [0, 0, -1, 1];
    function makeGrid(box, rows, size) {
      box.style.gridTemplateColumns = 'repeat(' + rows[0].length + ', ' + size + 'px)';
      var T = [];
      rows.forEach(function (row) {
        var rr = [];
        row.split('').forEach(function (ch) {
          var d = mk('div', ch === '#' ? 'gc wall' : 'gc');
          box.appendChild(d);
          rr.push(d);
        });
        T.push(rr);
      });
      return T;
    }
    function inList(list, r, c) {
      var f = false;
      list.forEach(function (p) { if (p[0] === r ? p[1] === c : false) f = true; });
      return f;
    }
    function fmtQ(q) {
      var parts = q.slice(0, 6).map(function (p) { return '(' + p[0] + ',' + p[1] + ')'; });
      if (q.length !== Math.min(q.length, 6)) parts.push('…');
      return parts.length ? parts.join(' ') : '(prazan)';
    }

    var Gs = root.dataset.grid.split('|');
    var R = Gs.length, C = Gs[0].length;
    var T = makeGrid(root.querySelector('.grid'), Gs, 56);
    var sr = 0, sc = 0, er = 0, ec = 0;
    Gs.forEach(function (row, r) {
      if (row.indexOf('A') !== -1) { sr = r; sc = row.indexOf('A'); }
      if (row.indexOf('B') !== -1) { er = r; ec = row.indexOf('B'); }
    });
    function free(r, c) {
      if (r === -1 || c === -1 || r === R || c === C) return false;
      return Gs[r][c] !== '#';
    }
    var dist = [], par = [];
    Gs.forEach(function (row) {
      dist.push(row.split('').map(function () { return -1; }));
      par.push(row.split('').map(function () { return -1; }));
    });
    var q = [[sr, sc]];
    dist[sr][sc] = 0;
    var snaps = [{ dist: cp(dist), cur: null, front: cp(q), path: [],
      l1: 'Start: A je u redu, dist[A] = 0', l2: 'Red: ' + fmtQ(q) }];
    var found = false;
    while (q.length) {
      var p = q.shift(), r = p[0], c = p[1];
      if (r === er ? c === ec : false) { found = true; break; }
      var added = [];
      for (var i = 0; i !== 4; i++) {
        var nr = r + DR[i], nc = c + DC[i];
        if (free(nr, nc) ? dist[nr][nc] === -1 : false) {
          dist[nr][nc] = dist[r][c] + 1;
          par[nr][nc] = i;
          q.push([nr, nc]);
          added.push('(' + nr + ',' + nc + ')');
        }
      }
      snaps.push({ dist: cp(dist), cur: [r, c], front: cp(q), path: [],
        l1: 'Uzimamo (' + r + ',' + c + '), dist = ' + dist[r][c] + '  → ' + (added.length ? 'dodajemo ' + added.join(' ') : 'nema novih susjeda'),
        l2: 'Red: ' + fmtQ(q) });
    }
    if (found) {
      var path = [], x = er, y = ec;
      while (x === sr ? y !== sc : true) {
        path.push([x, y]);
        var d = par[x][y];
        x -= DR[d];
        y -= DC[d];
      }
      path.push([sr, sc]);
      snaps.push({ dist: cp(dist), cur: [er, ec], front: [], path: path,
        l1: 'B je skinut s reda  → najkraći put ima ' + dist[er][ec] + ' koraka',
        l2: 'Zeleno: put koji BFS pronalazi (pratimo roditelje unatrag)' });
    } else {
      snaps.push({ dist: cp(dist), cur: null, front: [], path: [], l1: 'Red je prazan, B nije dostižan', l2: '' });
    }
    function draw(s) {
      T.forEach(function (row, r) {
        row.forEach(function (cell, c) {
          var ch = Gs[r][c];
          if (ch === '#') return;
          var cls = 'gc';
          if (s.dist[r][c] !== -1) cls += ' vis';
          if (inList(s.path, r, c)) cls += ' path';
          if (inList(s.front, r, c)) cls += ' front';
          if (s.cur ? (s.cur[0] === r ? s.cur[1] === c : false) : false) cls += ' cur';
          cell.className = cls;
          cell.textContent = ch === 'A' ? 'A' : (ch === 'B' ? 'B' : (s.dist[r][c] === -1 ? '' : s.dist[r][c]));
        });
      });
    }

    var step = 0, timer = null, lastStep = snaps.length - 1;
    function render() {
      var s = snaps[step];
      draw(s);
      line1.textContent = s.l1;
      line2.textContent = s.l2;
    }
    function stopAuto() { clearInterval(timer); timer = null; }
    function next() { if (step !== lastStep) { step++; render(); return true; } stopAuto(); return false; }
    function prev() { if (step !== 0) { step--; render(); return true; } return false; }
    function reset() { stopAuto(); step = 0; render(); }
    var actions = {
      next: next, prev: prev, reset: reset,
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 500); }
    };

    root.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation(); b.blur(); actions[b.dataset.act]();
      });
    });

    // Strelice / razmaknica / klikač prvo koračaju kroz animaciju, a tek na kraju mijenjaju slajd
    window.addEventListener('keydown', function (e) {
      if (e.shiftKey || !slide || !slide.classList.contains('bespoke-marp-active')) return;
      var fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].indexOf(e.key) !== -1;
      var back = ['ArrowLeft', 'ArrowUp', 'PageUp'].indexOf(e.key) !== -1;
      var moved = false;
      if (fwd) moved = next();
      if (back) moved = prev();
      if (moved) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);

    render();
  });
})();
</script>

---

# Problem 2: Povezane komponente (DFS)

**Zadatak:**
Koliko ima povezanih komponenata u grafu?

**Algoritam:**

1. Postavimo sve `visited` na false i `brojac = 0`.
2. Za svaki `i` od 1 do $N$:
   * Ako `i` nije posjećen:
     * `brojac++`
     * Pokrenemo `dfs(i)` $\to$ to će označiti cijelu komponentu kao posjećenu.

---

# DFS implementacija

```cpp
vector<int> adj[MAXN];
bool visited[MAXN];

void dfs(int u) {
    visited[u] = true;
    // Rekurzivno posjećujemo sve susjede
    for (int v : adj[u]) {
        if (!visited[v]) {
            dfs(v);
        }
    }
}

// U main funkciji:
int components = 0;
for (int i = 1; i <= n; ++i) {
    if (!visited[i]) {
        dfs(i);
        components++;
    }
}
```

**Složenost:** $O(V + E)$ (svaki čvor i brid jednom).

---

# Povezane komponente korak po korak

Vanjska petlja ide po čvorovima 1..N. Svaki neposjećeni čvor pokreće novi `dfs` i dobiva novu boju.

<style scoped>
.gr-comp { margin-top: 0.4em; }
.gr-comp .chips { font-size: 20px; margin-bottom: 0.5em; }
.gr-comp .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.gr-comp .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gr-comp .row { display: flex; gap: 8px; }
.gr-comp .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-comp .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gr-comp .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.gr-comp .cell.todo .val { color: #b5b5b5; }
.gr-comp .cell.src { background: #f5db7e; }
.gr-comp .cell.best { background: #9fdc9f; }
.gr-comp .cell.cur { background: var(--main); color: #fff; }
.gr-comp .cell.cur .idx, .gr-comp .cell.cur .val { color: #fff; }
.gr-comp .line1, .gr-comp .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.gr-comp .line1 { margin-top: 0.7em; }
.gr-comp .line2 { font-weight: bold; }
.gr-comp .ctrl { margin-top: 0.7em; }
.gr-comp button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gr-comp button:hover { background: var(--main); color: #fff; }
.gr-comp .hint { font-size: 16px; color: #6e6e6e; }
.gr-comp .gwrap { display: flex; justify-content: center; }
.gr-comp svg .edge { stroke: #a0a0a0; stroke-width: 3; transition: stroke .25s; }
.gr-comp svg .edge.tree { stroke: var(--main); stroke-width: 5; }
.gr-comp svg .edge.chk { stroke: #e0a800; stroke-width: 6; }
.gr-comp svg .edge.path { stroke: #2e9e44; stroke-width: 7; }
.gr-comp svg .edge.back { stroke: #d62828; stroke-width: 7; }
.gr-comp svg .node circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.gr-comp svg .node .lbl { font-size: 20px; font-weight: bold; fill: #141414; }
.gr-comp svg .node .sub { font-size: 16px; font-weight: bold; fill: #6e6e6e; }
.gr-comp svg .node.vis circle { fill: #f5db7e; }
.gr-comp svg .node.c1 circle { fill: #a9c5ff; }
.gr-comp svg .node.c2 circle { fill: #ffc58f; }
.gr-comp svg .node.c3 circle { fill: #a8e0a8; }
.gr-comp svg .node.c4 circle { fill: #e3b3ff; }
.gr-comp svg .node.path circle { fill: #9fdc9f; }
.gr-comp svg .node.front circle { stroke: var(--main); stroke-width: 5; stroke-dasharray: 6 4; }
.gr-comp svg .node.bad circle { stroke: #d62828; stroke-width: 5; }
.gr-comp svg .node.cur circle { fill: var(--main); stroke: var(--main); }
.gr-comp svg .node.cur .lbl { fill: #fff; }
</style>

<div class="gr-comp" data-pos="1:70,50;2:70,190;3:210,50;4:210,190;5:370,50;6:460,190;7:550,50;8:720,50;9:820,190" data-edges="1-2,1-3,2-4,3-4,5-6,6-7,8-9">
  <div class="gwrap g1"></div>
  <div class="line1"></div>
  <div class="line2"></div>
  <div class="ctrl">
    <button data-act="prev">← Korak</button><button data-act="next">Korak →</button><button data-act="auto">Auto</button><button data-act="reset">Reset</button>
    <span class="hint">← / → koračaju kroz animaciju, Shift + ← / → mijenja slajd</span>
  </div>
</div>

<script>
(function () {
  // Ovaj blok namjerno ne sadrži znakove manje-od, veće-od ni ampersand,
  // jer ih build pretvara u HTML entitete i ruši skriptu.
  document.querySelectorAll('.gr-comp').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function show(v) { return v === Infinity ? '∞' : String(v); }
    function makeRow(box, count) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }

    var SVGNS = 'http://www.w3.org/2000/svg';
    function svgEl(tag, attrs) {
      var e = document.createElementNS(SVGNS, tag);
      for (var k in attrs) e.setAttribute(k, attrs[k]);
      return e;
    }
    function cp(o) { return JSON.parse(JSON.stringify(o)); }
    function makeGraph(box, posStr, edgeStr, W, H, scale) {
      var svg = svgEl('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W * scale, height: H * scale });
      box.appendChild(svg);
      var pos = {}, ids = [];
      posStr.split(';').forEach(function (t) {
        var a = t.split(':'), xy = a[1].split(',');
        pos[a[0]] = [Number(xy[0]), Number(xy[1])];
        ids.push(Number(a[0]));
      });
      var adj = {}, edges = [];
      ids.forEach(function (id) { adj[id] = []; });
      var eg = svgEl('g', {});
      svg.appendChild(eg);
      edgeStr.split(',').forEach(function (t) {
        var ab = t.split('-').map(Number);
        var line = svgEl('line', { x1: pos[ab[0]][0], y1: pos[ab[0]][1], x2: pos[ab[1]][0], y2: pos[ab[1]][1], 'class': 'edge' });
        eg.appendChild(line);
        edges.push({ a: ab[0], b: ab[1], el: line });
        adj[ab[0]].push(ab[1]);
        adj[ab[1]].push(ab[0]);
      });
      ids.forEach(function (id) { adj[id].sort(function (x, y) { return x - y; }); });
      var nodes = {};
      ids.forEach(function (id) {
        var g = svgEl('g', { 'class': 'node' });
        g.appendChild(svgEl('circle', { cx: pos[id][0], cy: pos[id][1], r: 22 }));
        var t = svgEl('text', { x: pos[id][0], y: pos[id][1] + 7, 'text-anchor': 'middle', 'class': 'lbl' });
        t.textContent = id;
        var sub = svgEl('text', { x: pos[id][0], y: pos[id][1] + 44, 'text-anchor': 'middle', 'class': 'sub' });
        g.appendChild(t);
        g.appendChild(sub);
        svg.appendChild(g);
        nodes[id] = { g: g, sub: sub };
      });
      function edgeKey(a, b) {
        var r = null;
        edges.forEach(function (e) { if (e.a === a ? e.b === b : (e.a === b ? e.b === a : false)) r = e; });
        return r;
      }
      return { ids: ids, adj: adj, edges: edges, nodes: nodes, edge: edgeKey };
    }
    function has(list, x) { return list.indexOf(x) !== -1; }
    function hasEdge(list, a, b) {
      var r = false;
      list.forEach(function (p) { if (p[0] === a ? p[1] === b : (p[0] === b ? p[1] === a : false)) r = true; });
      return r;
    }

    var G = makeGraph(root.querySelector('.g1'), root.dataset.pos, root.dataset.edges, 880, 250, 1);
    var comp = {}, cnt = 0, stack = [], tree = [];
    function l2() {
      return 'components = ' + cnt + '   stog poziva: ' + (stack.length ? stack.map(function (x) { return 'dfs(' + x + ')'; }).join(' → ') : '—');
    }
    var snaps = [{ comp: {}, cur: -1, tree: [], l1: 'Svi čvorovi neposjećeni', l2: l2() }];
    function dfs(u) {
      comp[u] = cnt;
      stack.push(u);
      snaps.push({ comp: cp(comp), cur: u, tree: cp(tree),
        l1: 'dfs(' + u + '): označimo ' + u + ', susjedi: ' + G.adj[u].join(', '), l2: l2() });
      G.adj[u].forEach(function (v) {
        if (!comp[v]) { tree.push([u, v]); dfs(v); }
      });
      stack.pop();
    }
    G.ids.forEach(function (i) {
      if (comp[i]) {
        snaps.push({ comp: cp(comp), cur: -1, tree: cp(tree), l1: 'i = ' + i + ': već posjećen, preskačemo', l2: l2() });
      } else {
        cnt++;
        snaps.push({ comp: cp(comp), cur: -1, tree: cp(tree),
          l1: 'i = ' + i + ': neposjećen  → nova komponenta #' + cnt + ', pozivamo dfs(' + i + ')', l2: l2() });
        dfs(i);
      }
    });
    snaps.push({ comp: cp(comp), cur: -1, tree: cp(tree), l1: 'Gotovo: graf ima ' + cnt + ' komponente', l2: l2() });
    function draw(s) {
      G.ids.forEach(function (id) {
        var cls = 'node';
        if (s.comp[id]) cls += ' c' + Math.min(s.comp[id], 4);
        if (id === s.cur) cls += ' cur';
        G.nodes[id].g.setAttribute('class', cls);
      });
      G.edges.forEach(function (e) { e.el.setAttribute('class', hasEdge(s.tree, e.a, e.b) ? 'edge tree' : 'edge'); });
    }

    var step = 0, timer = null, lastStep = snaps.length - 1;
    function render() {
      var s = snaps[step];
      draw(s);
      line1.textContent = s.l1;
      line2.textContent = s.l2;
    }
    function stopAuto() { clearInterval(timer); timer = null; }
    function next() { if (step !== lastStep) { step++; render(); return true; } stopAuto(); return false; }
    function prev() { if (step !== 0) { step--; render(); return true; } return false; }
    function reset() { stopAuto(); step = 0; render(); }
    var actions = {
      next: next, prev: prev, reset: reset,
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 700); }
    };

    root.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation(); b.blur(); actions[b.dataset.act]();
      });
    });

    // Strelice / razmaknica / klikač prvo koračaju kroz animaciju, a tek na kraju mijenjaju slajd
    window.addEventListener('keydown', function (e) {
      if (e.shiftKey || !slide || !slide.classList.contains('bespoke-marp-active')) return;
      var fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].indexOf(e.key) !== -1;
      var back = ['ArrowLeft', 'ArrowUp', 'PageUp'].indexOf(e.key) !== -1;
      var moved = false;
      if (fwd) moved = next();
      if (back) moved = prev();
      if (moved) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);

    render();
  });
})();
</script>

---

# Problem 3: Detekcija ciklusa (DFS)

**Zadatak:**
Sadrži li neusmjereni graf ciklus?

**Ideja:**
Ako tijekom DFS-a naiđemo na susjeda `v` koji je **već posjećen**, a **nije** naš direktni roditelj `p` (iz kojeg smo došli), pronašli smo **povratni brid** (back-edge).

To znači da postoji drugi put do `v`, što zatvara ciklus.

---

# Detekcija ciklusa: kod

Modificiramo DFS da prati roditelja `p`.

```cpp
bool has_cycle = false;

void dfs_cycle(int u, int p) {
    visited[u] = true;

    for (int v : adj[u]) {
        if (v == p) continue; // Ignoriramo brid kojim smo došli

        if (visited[v]) {
            has_cycle = true; // Već viđen susjed -> CIKLUS!
            return;
        } else {
            dfs_cycle(v, u);
        }
    }
}
```

Kao i kod komponenata, `dfs_cycle` pokrećemo iz svakog neposjećenog čvora.

---

# Detekcija ciklusa korak po korak

Žuti brid je onaj koji upravo provjeravamo, plavi su bridovi DFS stabla. Crveno: povratni brid i ciklus.

<style scoped>
.gr-cycle { margin-top: 0.4em; }
.gr-cycle .chips { font-size: 20px; margin-bottom: 0.5em; }
.gr-cycle .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.gr-cycle .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gr-cycle .row { display: flex; gap: 8px; }
.gr-cycle .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-cycle .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gr-cycle .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.gr-cycle .cell.todo .val { color: #b5b5b5; }
.gr-cycle .cell.src { background: #f5db7e; }
.gr-cycle .cell.best { background: #9fdc9f; }
.gr-cycle .cell.cur { background: var(--main); color: #fff; }
.gr-cycle .cell.cur .idx, .gr-cycle .cell.cur .val { color: #fff; }
.gr-cycle .line1, .gr-cycle .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.gr-cycle .line1 { margin-top: 0.7em; }
.gr-cycle .line2 { font-weight: bold; }
.gr-cycle .ctrl { margin-top: 0.7em; }
.gr-cycle button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gr-cycle button:hover { background: var(--main); color: #fff; }
.gr-cycle .hint { font-size: 16px; color: #6e6e6e; }
.gr-cycle .gwrap { display: flex; justify-content: center; }
.gr-cycle svg .edge { stroke: #a0a0a0; stroke-width: 3; transition: stroke .25s; }
.gr-cycle svg .edge.tree { stroke: var(--main); stroke-width: 5; }
.gr-cycle svg .edge.chk { stroke: #e0a800; stroke-width: 6; }
.gr-cycle svg .edge.path { stroke: #2e9e44; stroke-width: 7; }
.gr-cycle svg .edge.back { stroke: #d62828; stroke-width: 7; }
.gr-cycle svg .node circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.gr-cycle svg .node .lbl { font-size: 20px; font-weight: bold; fill: #141414; }
.gr-cycle svg .node .sub { font-size: 16px; font-weight: bold; fill: #6e6e6e; }
.gr-cycle svg .node.vis circle { fill: #f5db7e; }
.gr-cycle svg .node.c1 circle { fill: #a9c5ff; }
.gr-cycle svg .node.c2 circle { fill: #ffc58f; }
.gr-cycle svg .node.c3 circle { fill: #a8e0a8; }
.gr-cycle svg .node.c4 circle { fill: #e3b3ff; }
.gr-cycle svg .node.path circle { fill: #9fdc9f; }
.gr-cycle svg .node.front circle { stroke: var(--main); stroke-width: 5; stroke-dasharray: 6 4; }
.gr-cycle svg .node.bad circle { stroke: #d62828; stroke-width: 5; }
.gr-cycle svg .node.cur circle { fill: var(--main); stroke: var(--main); }
.gr-cycle svg .node.cur .lbl { fill: #fff; }
</style>

<div class="gr-cycle" data-pos="1:60,130;2:200,130;3:340,50;4:340,210;5:480,130;6:620,130" data-edges="1-2,2-3,2-4,3-5,4-5,5-6">
  <div class="gwrap g1"></div>
  <div class="line1"></div>
  <div class="line2"></div>
  <div class="ctrl">
    <button data-act="prev">← Korak</button><button data-act="next">Korak →</button><button data-act="auto">Auto</button><button data-act="reset">Reset</button>
    <span class="hint">← / → koračaju kroz animaciju, Shift + ← / → mijenja slajd</span>
  </div>
</div>

<script>
(function () {
  // Ovaj blok namjerno ne sadrži znakove manje-od, veće-od ni ampersand,
  // jer ih build pretvara u HTML entitete i ruši skriptu.
  document.querySelectorAll('.gr-cycle').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function show(v) { return v === Infinity ? '∞' : String(v); }
    function makeRow(box, count) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }

    var SVGNS = 'http://www.w3.org/2000/svg';
    function svgEl(tag, attrs) {
      var e = document.createElementNS(SVGNS, tag);
      for (var k in attrs) e.setAttribute(k, attrs[k]);
      return e;
    }
    function cp(o) { return JSON.parse(JSON.stringify(o)); }
    function makeGraph(box, posStr, edgeStr, W, H, scale) {
      var svg = svgEl('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W * scale, height: H * scale });
      box.appendChild(svg);
      var pos = {}, ids = [];
      posStr.split(';').forEach(function (t) {
        var a = t.split(':'), xy = a[1].split(',');
        pos[a[0]] = [Number(xy[0]), Number(xy[1])];
        ids.push(Number(a[0]));
      });
      var adj = {}, edges = [];
      ids.forEach(function (id) { adj[id] = []; });
      var eg = svgEl('g', {});
      svg.appendChild(eg);
      edgeStr.split(',').forEach(function (t) {
        var ab = t.split('-').map(Number);
        var line = svgEl('line', { x1: pos[ab[0]][0], y1: pos[ab[0]][1], x2: pos[ab[1]][0], y2: pos[ab[1]][1], 'class': 'edge' });
        eg.appendChild(line);
        edges.push({ a: ab[0], b: ab[1], el: line });
        adj[ab[0]].push(ab[1]);
        adj[ab[1]].push(ab[0]);
      });
      ids.forEach(function (id) { adj[id].sort(function (x, y) { return x - y; }); });
      var nodes = {};
      ids.forEach(function (id) {
        var g = svgEl('g', { 'class': 'node' });
        g.appendChild(svgEl('circle', { cx: pos[id][0], cy: pos[id][1], r: 22 }));
        var t = svgEl('text', { x: pos[id][0], y: pos[id][1] + 7, 'text-anchor': 'middle', 'class': 'lbl' });
        t.textContent = id;
        var sub = svgEl('text', { x: pos[id][0], y: pos[id][1] + 44, 'text-anchor': 'middle', 'class': 'sub' });
        g.appendChild(t);
        g.appendChild(sub);
        svg.appendChild(g);
        nodes[id] = { g: g, sub: sub };
      });
      function edgeKey(a, b) {
        var r = null;
        edges.forEach(function (e) { if (e.a === a ? e.b === b : (e.a === b ? e.b === a : false)) r = e; });
        return r;
      }
      return { ids: ids, adj: adj, edges: edges, nodes: nodes, edge: edgeKey };
    }
    function has(list, x) { return list.indexOf(x) !== -1; }
    function hasEdge(list, a, b) {
      var r = false;
      list.forEach(function (p) { if (p[0] === a ? p[1] === b : (p[0] === b ? p[1] === a : false)) r = true; });
      return r;
    }

    var G = makeGraph(root.querySelector('.g1'), root.dataset.pos, root.dataset.edges, 680, 260, 1);
    var vis = {}, par = {}, tree = [], stack = [], found = false, cyc = [];
    var snaps = [{ vis: {}, cur: -1, tree: [], chk: null, cyc: [], l1: 'Pokrećemo dfs_cycle(' + G.ids[0] + ', 0)', l2: '' }];
    function st() { return 'stog: ' + stack.map(function (x) { return x + '(p=' + par[x] + ')'; }).join(' → '); }
    function push(u, chk, l1) { snaps.push({ vis: cp(vis), cur: u, tree: cp(tree), chk: chk, cyc: cp(cyc), l1: l1, l2: st() }); }
    function dfs(u, p) {
      vis[u] = true;
      par[u] = p;
      stack.push(u);
      push(u, null, 'dfs_cycle(' + u + ', ' + p + '): označimo ' + u + ' kao posjećen');
      for (var k = 0; k !== G.adj[u].length; k++) {
        if (found) return;
        var v = G.adj[u][k];
        if (v === p) {
          push(u, [u, v], 'susjed ' + v + ' je roditelj  → ignoriramo brid ' + u + '–' + v);
        } else if (vis[v]) {
          found = true;
          var x = u;
          cyc = [[u, v]];
          while (x !== v) { cyc.push([x, par[x]]); x = par[x]; }
          push(u, [u, v], 'susjed ' + v + ' je već posjećen i nije roditelj  → CIKLUS!');
          return;
        } else {
          tree.push([u, v]);
          push(u, [u, v], 'susjed ' + v + ' nije posjećen  → dfs_cycle(' + v + ', ' + u + ')');
          dfs(v, u);
        }
      }
      if (!found) stack.pop();
    }
    G.ids.forEach(function (i) { if (!found) { if (!vis[i]) dfs(i, 0); } });
    if (found) {
      var walk = [cyc[0][0]];
      cyc.slice(1).forEach(function (e) { walk.push(e[1]); });
      var nodesOnCycle = walk.reverse();
      nodesOnCycle.push(nodesOnCycle[0]);
      snaps.push({ vis: cp(vis), cur: -1, tree: cp(tree), chk: null, cyc: cp(cyc),
        l1: 'has_cycle = true', l2: 'Ciklus: ' + nodesOnCycle.join(' → ') });
    } else {
      snaps.push({ vis: cp(vis), cur: -1, tree: cp(tree), chk: null, cyc: [], l1: 'has_cycle = false', l2: 'Graf nema ciklusa' });
    }
    function draw(s) {
      G.ids.forEach(function (id) {
        var cls = 'node';
        if (s.vis[id]) cls += ' vis';
        if (id === s.cur) cls += ' cur';
        G.nodes[id].g.setAttribute('class', cls);
      });
      G.edges.forEach(function (e) {
        var cls = 'edge';
        if (hasEdge(s.tree, e.a, e.b)) cls = 'edge tree';
        if (s.chk ? hasEdge([s.chk], e.a, e.b) : false) cls = 'edge chk';
        if (hasEdge(s.cyc, e.a, e.b)) cls = 'edge back';
        e.el.setAttribute('class', cls);
      });
    }

    var step = 0, timer = null, lastStep = snaps.length - 1;
    function render() {
      var s = snaps[step];
      draw(s);
      line1.textContent = s.l1;
      line2.textContent = s.l2;
    }
    function stopAuto() { clearInterval(timer); timer = null; }
    function next() { if (step !== lastStep) { step++; render(); return true; } stopAuto(); return false; }
    function prev() { if (step !== 0) { step--; render(); return true; } return false; }
    function reset() { stopAuto(); step = 0; render(); }
    var actions = {
      next: next, prev: prev, reset: reset,
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 900); }
    };

    root.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation(); b.blur(); actions[b.dataset.act]();
      });
    });

    // Strelice / razmaknica / klikač prvo koračaju kroz animaciju, a tek na kraju mijenjaju slajd
    window.addEventListener('keydown', function (e) {
      if (e.shiftKey || !slide || !slide.classList.contains('bespoke-marp-active')) return;
      var fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].indexOf(e.key) !== -1;
      var back = ['ArrowLeft', 'ArrowUp', 'PageUp'].indexOf(e.key) !== -1;
      var moved = false;
      if (fwd) moved = next();
      if (back) moved = prev();
      if (moved) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);

    render();
  });
})();
</script>

---

# Zadaci za vježbu (CSES)

1. **[Counting Rooms](https://cses.fi/problemset/task/1192)**: dovršite kod (jedan uvjet).
   * Primjena DFS/BFS na 2D mreži za brojanje komponenata.
2. **[Labyrinth](https://cses.fi/problemset/task/1193)**: dobivate kostur, pišete BFS i rekonstrukciju.
   * BFS za najkraći put + rekonstrukcija puta (pamtimo `parent` polje).
3. **[Building Teams](https://cses.fi/problemset/task/1668)**: samostalno, uz hintove.
   * Provjera je li graf bipartitan (2-bojanje grafa).
4. **[Message Route](https://cses.fi/problemset/task/1667)**: samostalno, uz hintove.
   * Klasičan BFS na grafu (ne na mreži).
5. **[Round Trip](https://cses.fi/problemset/task/1669)**: samostalno, uz hintove.
   * Detekcija ciklusa iz Problema 3, uz ispis samog ciklusa.

---

<!-- _class: title -->
# 1. Counting Rooms (CSES)

## Brojanje povezanih komponenata na mreži

---

# Analiza: Counting Rooms

**Problem:**
Zadan je tlocrt zgrade veličine $N \times M$. Neka polja su zidovi (`#`), a neka pod (`.`).
Želimo prebrojati koliko ima "soba". Soba je skup podnih polja povezanih horizontalno ili vertikalno.

**Intuicija:**
Ovo je klasičan problem **brojanja povezanih komponenata**, ali na implicitnom grafu (mreži).
Svako polje `.` je čvor, a susjedna polja `.` povezana su bridom.

**Algoritam:**
Prolazimo kroz svako polje $(i, j)$ u mreži:

1. Ako je polje zid (`#`) ili već posjećeno $\to$ preskačemo ga.
2. Ako je polje pod (`.`) i nije posjećeno $\to$ pronašli smo novu sobu!
   - Povećamo brojač soba.
   - Pokrenemo DFS/BFS od tog polja da označimo cijelu sobu kao posjećenu.

---

# Counting Rooms korak po korak

Skeniramo polja redom. Svako neposjećeno podno polje pokreće `dfs` koji oboji cijelu sobu.

<style scoped>
.gr-rooms { margin-top: 0.4em; }
.gr-rooms .chips { font-size: 20px; margin-bottom: 0.5em; }
.gr-rooms .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.gr-rooms .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gr-rooms .row { display: flex; gap: 8px; }
.gr-rooms .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-rooms .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gr-rooms .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.gr-rooms .cell.todo .val { color: #b5b5b5; }
.gr-rooms .cell.src { background: #f5db7e; }
.gr-rooms .cell.best { background: #9fdc9f; }
.gr-rooms .cell.cur { background: var(--main); color: #fff; }
.gr-rooms .cell.cur .idx, .gr-rooms .cell.cur .val { color: #fff; }
.gr-rooms .line1, .gr-rooms .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.gr-rooms .line1 { margin-top: 0.7em; }
.gr-rooms .line2 { font-weight: bold; }
.gr-rooms .ctrl { margin-top: 0.7em; }
.gr-rooms button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gr-rooms button:hover { background: var(--main); color: #fff; }
.gr-rooms .hint { font-size: 16px; color: #6e6e6e; }
.gr-rooms .grid { display: grid; gap: 4px; justify-content: start; }
.gr-rooms .gc { height: 48px; line-height: 44px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 5px; transition: background-color .25s, color .25s; }
.gr-rooms .gc.wall { background: #141414; }
.gr-rooms .gc.vis { background: #f5db7e; }
.gr-rooms .gc.front { box-shadow: inset 0 0 0 4px var(--main); }
.gr-rooms .gc.path { background: #9fdc9f; }
.gr-rooms .gc.r1 { background: #a9c5ff; }
.gr-rooms .gc.r2 { background: #ffc58f; }
.gr-rooms .gc.r3 { background: #a8e0a8; }
.gr-rooms .gc.r4 { background: #e3b3ff; }
.gr-rooms .gc.cur { background: var(--main); color: #fff; }
</style>

<div class="gr-rooms" data-grid="########|#..#...#|####.#.#|#..#...#|########">
  <div class="grid"></div>
  <div class="line1"></div>
  <div class="line2"></div>
  <div class="ctrl">
    <button data-act="prev">← Korak</button><button data-act="next">Korak →</button><button data-act="auto">Auto</button><button data-act="reset">Reset</button>
    <span class="hint">← / → koračaju kroz animaciju, Shift + ← / → mijenja slajd</span>
  </div>
</div>

<script>
(function () {
  // Ovaj blok namjerno ne sadrži znakove manje-od, veće-od ni ampersand,
  // jer ih build pretvara u HTML entitete i ruši skriptu.
  document.querySelectorAll('.gr-rooms').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function show(v) { return v === Infinity ? '∞' : String(v); }
    function makeRow(box, count) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }

    function cp(o) { return JSON.parse(JSON.stringify(o)); }
    var DR = [-1, 1, 0, 0], DC = [0, 0, -1, 1];
    function makeGrid(box, rows, size) {
      box.style.gridTemplateColumns = 'repeat(' + rows[0].length + ', ' + size + 'px)';
      var T = [];
      rows.forEach(function (row) {
        var rr = [];
        row.split('').forEach(function (ch) {
          var d = mk('div', ch === '#' ? 'gc wall' : 'gc');
          box.appendChild(d);
          rr.push(d);
        });
        T.push(rr);
      });
      return T;
    }
    function inList(list, r, c) {
      var f = false;
      list.forEach(function (p) { if (p[0] === r ? p[1] === c : false) f = true; });
      return f;
    }
    function fmtQ(q) {
      var parts = q.slice(0, 6).map(function (p) { return '(' + p[0] + ',' + p[1] + ')'; });
      if (q.length !== Math.min(q.length, 6)) parts.push('…');
      return parts.length ? parts.join(' ') : '(prazan)';
    }

    var Gs = root.dataset.grid.split('|');
    var R = Gs.length, C = Gs[0].length;
    var T = makeGrid(root.querySelector('.grid'), Gs, 62);
    function free(r, c) {
      if (r === -1 || c === -1 || r === R || c === C) return false;
      return Gs[r][c] !== '#';
    }
    var room = [];
    Gs.forEach(function (row) { room.push(row.split('').map(function () { return 0; })); });
    var cnt = 0, depth = 0;
    var snaps = [{ room: cp(room), cur: null, l1: 'Nijedno polje još nije posjećeno', l2: 'rooms = 0' }];
    function dfs(x, y) {
      room[x][y] = cnt;
      depth++;
      snaps.push({ room: cp(room), cur: [x, y], l1: 'dfs(' + x + ', ' + y + ')  dubina rekurzije: ' + depth, l2: 'rooms = ' + cnt });
      for (var i = 0; i !== 4; i++) {
        var nx = x + DR[i], ny = y + DC[i];
        if (free(nx, ny) ? room[nx][ny] === 0 : false) dfs(nx, ny);
      }
      depth--;
    }
    for (var i = 0; i !== R; i++) {
      for (var j = 0; j !== C; j++) {
        if (Gs[i][j] === '.' ? room[i][j] === 0 : false) {
          cnt++;
          snaps.push({ room: cp(room), cur: [i, j], l1: 'Skeniramo (' + i + ', ' + j + '): pod i neposjećeno  → nova soba #' + cnt, l2: 'rooms = ' + cnt });
          dfs(i, j);
        }
      }
    }
    snaps.push({ room: cp(room), cur: null, l1: 'Skeniranje gotovo', l2: 'rooms = ' + cnt + '   ✓' });
    function draw(s) {
      T.forEach(function (row, r) {
        row.forEach(function (cell, c) {
          if (Gs[r][c] === '#') return;
          var cls = 'gc';
          if (s.room[r][c]) cls += ' r' + (1 + (s.room[r][c] - 1) % 4);
          if (s.cur ? (s.cur[0] === r ? s.cur[1] === c : false) : false) cls += ' cur';
          cell.className = cls;
          cell.textContent = s.room[r][c] ? s.room[r][c] : '';
        });
      });
    }

    var step = 0, timer = null, lastStep = snaps.length - 1;
    function render() {
      var s = snaps[step];
      draw(s);
      line1.textContent = s.l1;
      line2.textContent = s.l2;
    }
    function stopAuto() { clearInterval(timer); timer = null; }
    function next() { if (step !== lastStep) { step++; render(); return true; } stopAuto(); return false; }
    function prev() { if (step !== 0) { step--; render(); return true; } return false; }
    function reset() { stopAuto(); step = 0; render(); }
    var actions = {
      next: next, prev: prev, reset: reset,
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 600); }
    };

    root.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation(); b.blur(); actions[b.dataset.act]();
      });
    });

    // Strelice / razmaknica / klikač prvo koračaju kroz animaciju, a tek na kraju mijenjaju slajd
    window.addEventListener('keydown', function (e) {
      if (e.shiftKey || !slide || !slide.classList.contains('bespoke-marp-active')) return;
      var fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].indexOf(e.key) !== -1;
      var back = ['ArrowLeft', 'ArrowUp', 'PageUp'].indexOf(e.key) !== -1;
      var moved = false;
      if (fwd) moved = next();
      if (back) moved = prev();
      if (moved) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);

    render();
  });
})();
</script>

---

# Zadatak: dovršite Counting Rooms (1/2)

Kod je gotov osim **jednog uvjeta** u funkciji `dfs`. Nadopunite ga i predajte na [CSES](https://cses.fi/problemset/task/1192).

```cpp
#include <bits/stdc++.h>
using namespace std;

int n, m;
vector<string> grid;
vector<vector<bool>> visited;
int dx[] = {-1, 1, 0, 0};
int dy[] = {0, 0, -1, 1};

void dfs(int x, int y) {
    visited[x][y] = true;
    for (int i = 0; i < 4; ++i) {
        int nx = x + dx[i], ny = y + dy[i];
        // TODO: pozovite dfs(nx, ny) samo ako je susjed
        //   1) unutar mreže,
        //   2) pod ('.'),
        //   3) još neposjećen.
    }
}
```

---

# Zadatak: dovršite Counting Rooms (2/2)

```cpp
int main() {
    cin >> n >> m;
    grid.resize(n);
    for (auto &row : grid) cin >> row;
    visited.assign(n, vector<bool>(m, false));

    int rooms = 0;
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j)
            if (grid[i][j] == '.' && !visited[i][j]) {
                rooms++;
                dfs(i, j);
            }
    cout << rooms << "\n";
}
```

**Test:** primjer sa stranice zadatka (isti kao na animaciji) mora dati `3`.
**Pazite:** granice provjerite **prije** nego pročitate `grid[nx][ny]`.
**Oprez:** lokalno rušenje na velikoj mreži = preduboka rekurzija (mali stack), ne krivi uvjet.

---

<!-- _class: title -->
# 2. Labyrinth (CSES)

## Najkraći put i rekonstrukcija

---

# Analiza: Labyrinth

**Problem:**
Treba naći najkraći put od `A` do `B` u labirintu. Ako postoji, ispisujemo `YES`, duljinu i sam put (niz znakova `L`, `R`, `U`, `D`).

**Intuicija:**
Najkraći put u grafu bez težina $\to$ **BFS**.
Da bismo ispisali put, nije dovoljno pamtiti samo udaljenost. Moramo pamtiti **odakle smo došli**.

**Struktura za rekonstrukciju:**
Koristimo 2D polje `parent[N][M]` koje za svako polje pamti smjer kojim smo došli do njega.
Kada BFS dođe do `B`, krećemo od `B` i pratimo `parent` unatrag sve do `A`.

---

# Labyrinth korak po korak

BFS pamti smjer kojim je ušao u polje (strelica). Nakon što nađe `B`, put rekonstruiramo unatrag.

<style scoped>
.gr-lab { margin-top: 0.4em; }
.gr-lab .chips { font-size: 20px; margin-bottom: 0.5em; }
.gr-lab .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.gr-lab .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gr-lab .row { display: flex; gap: 8px; }
.gr-lab .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-lab .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gr-lab .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.gr-lab .cell.todo .val { color: #b5b5b5; }
.gr-lab .cell.src { background: #f5db7e; }
.gr-lab .cell.best { background: #9fdc9f; }
.gr-lab .cell.cur { background: var(--main); color: #fff; }
.gr-lab .cell.cur .idx, .gr-lab .cell.cur .val { color: #fff; }
.gr-lab .line1, .gr-lab .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.gr-lab .line1 { margin-top: 0.7em; }
.gr-lab .line2 { font-weight: bold; }
.gr-lab .ctrl { margin-top: 0.7em; }
.gr-lab button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gr-lab button:hover { background: var(--main); color: #fff; }
.gr-lab .hint { font-size: 16px; color: #6e6e6e; }
.gr-lab .grid { display: grid; gap: 4px; justify-content: start; }
.gr-lab .gc { height: 48px; line-height: 44px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 5px; transition: background-color .25s, color .25s; }
.gr-lab .gc.wall { background: #141414; }
.gr-lab .gc.vis { background: #f5db7e; }
.gr-lab .gc.front { box-shadow: inset 0 0 0 4px var(--main); }
.gr-lab .gc.path { background: #9fdc9f; }
.gr-lab .gc.r1 { background: #a9c5ff; }
.gr-lab .gc.r2 { background: #ffc58f; }
.gr-lab .gc.r3 { background: #a8e0a8; }
.gr-lab .gc.r4 { background: #e3b3ff; }
.gr-lab .gc.cur { background: var(--main); color: #fff; }
</style>

<div class="gr-lab" data-grid="########|#.A#...#|#.##.#B#|#......#|########">
  <div class="grid"></div>
  <div class="line1"></div>
  <div class="line2"></div>
  <div class="ctrl">
    <button data-act="prev">← Korak</button><button data-act="next">Korak →</button><button data-act="auto">Auto</button><button data-act="reset">Reset</button>
    <span class="hint">← / → koračaju kroz animaciju, Shift + ← / → mijenja slajd</span>
  </div>
</div>

<script>
(function () {
  // Ovaj blok namjerno ne sadrži znakove manje-od, veće-od ni ampersand,
  // jer ih build pretvara u HTML entitete i ruši skriptu.
  document.querySelectorAll('.gr-lab').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function show(v) { return v === Infinity ? '∞' : String(v); }
    function makeRow(box, count) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }

    function cp(o) { return JSON.parse(JSON.stringify(o)); }
    var DR = [-1, 1, 0, 0], DC = [0, 0, -1, 1];
    function makeGrid(box, rows, size) {
      box.style.gridTemplateColumns = 'repeat(' + rows[0].length + ', ' + size + 'px)';
      var T = [];
      rows.forEach(function (row) {
        var rr = [];
        row.split('').forEach(function (ch) {
          var d = mk('div', ch === '#' ? 'gc wall' : 'gc');
          box.appendChild(d);
          rr.push(d);
        });
        T.push(rr);
      });
      return T;
    }
    function inList(list, r, c) {
      var f = false;
      list.forEach(function (p) { if (p[0] === r ? p[1] === c : false) f = true; });
      return f;
    }
    function fmtQ(q) {
      var parts = q.slice(0, 6).map(function (p) { return '(' + p[0] + ',' + p[1] + ')'; });
      if (q.length !== Math.min(q.length, 6)) parts.push('…');
      return parts.length ? parts.join(' ') : '(prazan)';
    }

    var Gs = root.dataset.grid.split('|');
    var R = Gs.length, C = Gs[0].length;
    var T = makeGrid(root.querySelector('.grid'), Gs, 62);
    var ARR = ['↑', '↓', '←', '→'], LET = 'UDLR';
    var sr = 0, sc = 0, er = 0, ec = 0;
    Gs.forEach(function (row, r) {
      if (row.indexOf('A') !== -1) { sr = r; sc = row.indexOf('A'); }
      if (row.indexOf('B') !== -1) { er = r; ec = row.indexOf('B'); }
    });
    function free(r, c) {
      if (r === -1 || c === -1 || r === R || c === C) return false;
      return Gs[r][c] !== '#';
    }
    var vis = [], par = [];
    Gs.forEach(function (row) {
      vis.push(row.split('').map(function () { return false; }));
      par.push(row.split('').map(function () { return -1; }));
    });
    var q = [[sr, sc]];
    vis[sr][sc] = true;
    var snaps = [{ vis: cp(vis), par: cp(par), cur: null, front: cp(q), path: [],
      l1: 'Start: A u redu', l2: 'Red: ' + fmtQ(q) }];
    var found = false;
    while (q.length) {
      var p = q.shift(), x = p[0], y = p[1];
      if (x === er ? y === ec : false) { found = true; break; }
      var added = [];
      for (var i = 0; i !== 4; i++) {
        var nx = x + DR[i], ny = y + DC[i];
        if (free(nx, ny) ? !vis[nx][ny] : false) {
          vis[nx][ny] = true;
          par[nx][ny] = i;
          q.push([nx, ny]);
          added.push('(' + nx + ',' + ny + ') ' + LET[i]);
        }
      }
      snaps.push({ vis: cp(vis), par: cp(par), cur: [x, y], front: cp(q), path: [],
        l1: 'Uzimamo (' + x + ',' + y + ')  → ' + (added.length ? 'novi: ' + added.join(', ') : 'nema novih susjeda'),
        l2: 'Red: ' + fmtQ(q) });
    }
    if (found) {
      snaps.push({ vis: cp(vis), par: cp(par), cur: [er, ec], front: [], path: [[er, ec]],
        l1: 'B je skinut s reda  → YES, krećemo unatrag od B', l2: 'path = ""' });
      var cx = er, cy = ec, path = '', cells = [[er, ec]];
      while (cx === sr ? cy !== sc : true) {
        var d = par[cx][cy];
        path += LET[d];
        cx -= DR[d];
        cy -= DC[d];
        cells.push([cx, cy]);
        snaps.push({ vis: cp(vis), par: cp(par), cur: [cx, cy], front: [], path: cp(cells),
          l1: 'parent = ' + LET[d] + '  → dodamo „' + LET[d] + '“ i idemo suprotno, na (' + cx + ',' + cy + ')',
          l2: 'path = "' + path + '"' });
      }
      var rev = path.split('').reverse().join('');
      snaps.push({ vis: cp(vis), par: cp(par), cur: null, front: [], path: cp(cells),
        l1: 'Stigli smo do A, okrenemo string', l2: 'YES  ' + rev.length + '  ' + rev + '   ✓' });
    } else {
      snaps.push({ vis: cp(vis), par: cp(par), cur: null, front: [], path: [], l1: 'Red je prazan', l2: 'NO' });
    }
    function draw(s) {
      T.forEach(function (row, r) {
        row.forEach(function (cell, c) {
          var ch = Gs[r][c];
          if (ch === '#') return;
          var cls = 'gc';
          if (s.vis[r][c]) cls += ' vis';
          if (inList(s.path, r, c)) cls += ' path';
          if (inList(s.front, r, c)) cls += ' front';
          if (s.cur ? (s.cur[0] === r ? s.cur[1] === c : false) : false) cls += ' cur';
          cell.className = cls;
          cell.textContent = ch === 'A' ? 'A' : (ch === 'B' ? 'B' : (s.par[r][c] === -1 ? '' : ARR[s.par[r][c]]));
        });
      });
    }

    var step = 0, timer = null, lastStep = snaps.length - 1;
    function render() {
      var s = snaps[step];
      draw(s);
      line1.textContent = s.l1;
      line2.textContent = s.l2;
    }
    function stopAuto() { clearInterval(timer); timer = null; }
    function next() { if (step !== lastStep) { step++; render(); return true; } stopAuto(); return false; }
    function prev() { if (step !== 0) { step--; render(); return true; } return false; }
    function reset() { stopAuto(); step = 0; render(); }
    var actions = {
      next: next, prev: prev, reset: reset,
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 500); }
    };

    root.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation(); b.blur(); actions[b.dataset.act]();
      });
    });

    // Strelice / razmaknica / klikač prvo koračaju kroz animaciju, a tek na kraju mijenjaju slajd
    window.addEventListener('keydown', function (e) {
      if (e.shiftKey || !slide || !slide.classList.contains('bespoke-marp-active')) return;
      var fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].indexOf(e.key) !== -1;
      var back = ['ArrowLeft', 'ArrowUp', 'PageUp'].indexOf(e.key) !== -1;
      var moved = false;
      if (fwd) moved = next();
      if (back) moved = prev();
      if (moved) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);

    render();
  });
})();
</script>

---

# Zadatak: Labyrinth (kostur)

```cpp
// Učitavanje je gotovo: vi pišete BFS (TODO 1) i rekonstrukciju (TODO 2).
#include <bits/stdc++.h>
using namespace std;
int dx[] = {-1, 1, 0, 0};   // 0 = U, 1 = D, 2 = L, 3 = R
int dy[] = {0, 0, -1, 1};

int main() {
    int n, m; cin >> n >> m;
    vector<string> grid(n);
    int sr, sc, er, ec;
    for (int i = 0; i < n; ++i) {
        cin >> grid[i];
        for (int j = 0; j < m; ++j) {
            if (grid[i][j] == 'A') sr = i, sc = j;
            if (grid[i][j] == 'B') er = i, ec = j;
        }
    }
    vector<vector<bool>> visited(n, vector<bool>(m, false));
    vector<vector<int>> parent(n, vector<int>(m, -1));

    // TODO 1: BFS iz (sr, sc); za slobodnog, neposjećenog susjeda
    //         zapamtite parent[nx][ny] = i i dodajte ga u red.
    // TODO 2: ako B nije posjećen -> NO. Inače od B unatrag po parent
    //         do A, skupljajte "UDLR"[d], okrenite i ispišite YES, duljinu, put.
}
```

---

# Labyrinth: hintovi

1) BFS je isti kao u Problemu 1, samo umjesto `dist` pamtite `parent` (indeks smjera `i`).
2) `A` i `B` nisu zidovi: susjed je slobodan ako je unutar mreže i nije `#`.
3) Kad idete unatrag iz polja s `parent = d`, pomičete se **suprotno**: `x -= dx[d]`, `y -= dy[d]`.
4) Slova skupljate od `B` prema `A`, pa string na kraju treba okrenuti (`reverse`).
5) Mreža je do $1000 \times 1000$: BFS s redom, bez rekurzije.

**Test:** primjer sa stranice zadatka (isti kao na animaciji) daje `YES`, `9`, `LDDRRRRRU`. Prihvaća se bilo koji najkraći put. Predaja: [CSES](https://cses.fi/problemset/task/1193).

---

<!-- _class: title -->
# 3. Building Teams (CSES)

## Bipartitnost grafa (2-bojanje)

---

# Zadatak: Building Teams

[CSES 1668](https://cses.fi/problemset/task/1668): $n$ učenika i $m$ prijateljstava. Podijelite učenike u **dva tima** tako da nijedan par prijatelja nije u istom timu. Za svakog učenika ispišite tim (1 ili 2), a ako podjela nije moguća, ispišite `IMPOSSIBLE`.

**Primjer ulaza:**

```text
5 3
1 2
1 3
4 5
```

**Izlaz:** `1 2 2 1 2` (prihvaća se bilo koja ispravna podjela)

---

# Building Teams: hintovi

1) Učenici su čvorovi, prijateljstva su bridovi, a timovi su dvije **boje**.
2) Neobojanom čvoru dajte boju 1 i pokrenite BFS ili DFS, kao kod povezanih komponenti.
3) Svaki susjed mora dobiti **suprotnu** boju od trenutnog čvora.
4) Ako je susjed već obojan **istom** bojom kao trenutni čvor, odgovor je `IMPOSSIBLE`.
5) Graf ne mora biti povezan: vanjska petlja ide po svim čvorovima.
6) Za razmišljanje: konflikt se pojavi točno onda kad graf ima ciklus **neparne** duljine. Zašto?

---

<!-- _class: title -->
# 4. Message Route (CSES)

## Najkraći put u općem grafu

---

# Zadatak: Message Route

[CSES 1667](https://cses.fi/problemset/task/1667): $n$ računala i $m$ veza. Nađite put od računala 1 do računala $n$ koji prolazi kroz **najmanje računala**. Ispišite broj računala na putu i sam put, ili `IMPOSSIBLE`.

**Primjer ulaza:**

```text
5 5
1 2
1 3
1 4
2 3
5 4
```

**Izlaz:** `3`, zatim `1 4 5`

---

# Message Route: hintovi

1) Najkraći put u grafu bez težina $\to$ BFS iz čvora 1.
2) Isti princip kao Labyrinth, samo umjesto mreže imate listu susjedstva `adj`.
3) Kad prvi put dođete do `v` iz `u`, zapamtite `parent[v] = u`.
4) Ako `n` nije posjećen, ispišite `IMPOSSIBLE`.
5) Put složite od `n` prema 1 preko `parent`, pa ga okrenite.
6) Ispisuje se broj **računala** na putu, ne broj bridova (u primjeru 3, a ne 2).

---

<!-- _class: title -->
# 5. Round Trip (CSES)

## Pronalaženje i ispis ciklusa

---

# Zadatak: Round Trip

[CSES 1669](https://cses.fi/problemset/task/1669): $n$ gradova i $m$ cesta. Nađite obilazak koji kreće iz nekog grada, prolazi kroz barem dva druga različita grada i vraća se u početni. Ispišite broj gradova na obilasku i sam obilazak, ili `IMPOSSIBLE`.

**Primjer ulaza:**

```text
5 6
1 3
1 2
5 3
1 5
2 4
4 5
```

**Izlaz** (jedan od mogućih): `4`, zatim `3 5 1 3`

---

# Round Trip: hintovi

1) Ovo je detekcija ciklusa iz Problema 3, ali sad treba ispisati i sam ciklus.
2) U DFS-u za svaki čvor pamtite `parent[v] = u`.
3) Kad nađete susjeda `v` koji je posjećen i nije roditelj od `u`, ciklus je `v → … → u → v`.
4) Krenite od `u`, pratite `parent` dok ne dođete do `v`, a zatim dodajte `v` na oba kraja.
5) Graf ne mora biti povezan: DFS pokrećite iz svakog neposjećenog čvora.
6) Početni grad se u ispisu pojavljuje dvaput, pa je broj gradova duljina ciklusa + 1.

---

# Zadaci za vježbu (Codeforces)

Preporuka: filtrirajte zadatke s tagom `graphs` i težinom `800-1400`.

[Codeforces Graph Problems](https://codeforces.com/problemset?order=BY_RATING_ASC&tags=graphs)