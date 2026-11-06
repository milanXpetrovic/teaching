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
   - Modeliranje i lista susjedstva
2. **Osnovne strategije**
   - DFS (Depth-First Search)
   - BFS (Breadth-First Search)
3. **Primjeri i algoritmi**
   - Najkraći put u labirintu (BFS)
   - Povezane komponente (DFS)
   - Detekcija ciklusa (DFS)
4. **Zadaci za vježbu**

---

# Uvod: modeliranje problema

Grafovi su moćna apstrakcija. Čvorovi su objekti, bridovi su veze.

**Primjeri iz stvarnog svijeta:**

- **Mreže cesta:** gradovi (čvorovi) i ceste (bridovi).
- **Društvene mreže:** ljudi (čvorovi) i prijateljstva (bridovi).
- **Ovisnosti:** zadaci (čvorovi) i redoslijed izvršavanja (usmjereni bridovi).

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

- **Intuicija:** istražujemo jedan put do kraja ("udarimo u zid"), pa se vraćamo (backtrack).
- **Implementacija:** rekurzija (stog).
- **Primjene:** povezane komponente, detekcija ciklusa, topološko sortiranje.

**2. BFS (Breadth-First Search): širina**

- **Intuicija:** širimo se u slojevima (valovi u vodi). Prvo posjetimo sve susjede, pa susjede susjeda.
- **Implementacija:** red (queue).
- **Primjene:** **najkraći put** u grafu bez težina.

---

# BFS vs. DFS na istom grafu

Isti graf, isti početni čvor 1, susjedi se obilaze uzlazno. Broj ispod čvora je redoslijed posjeta.

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
</style>

<div class="gr-strat" data-pos="1:250,35;2:130,115;3:370,115;4:60,200;5:190,200;6:310,200;7:440,200;8:190,280" data-edges="1-2,1-3,2-4,2-5,3-6,3-7,5-8">
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
    var adj = G1.adj, start = G1.ids[0];

    var B = [], vis = {}, order = [], q = [start];
    vis[start] = true;
    while (q.length) {
      var u = q.shift();
      order.push(u);
      adj[u].forEach(function (v) { if (!vis[v]) { vis[v] = true; q.push(v); } });
      B.push({ cur: u, order: order.slice(), front: q.slice() });
    }
    var D = [], dvis = {}, dord = [], stack = [];
    function dfs(u) {
      dvis[u] = true;
      dord.push(u);
      stack.push(u);
      D.push({ cur: u, order: dord.slice(), front: stack.slice() });
      adj[u].forEach(function (v) { if (!dvis[v]) dfs(v); });
      stack.pop();
    }
    dfs(start);

    var snaps = [{ b: { cur: -1, order: [], front: [start] }, d: { cur: -1, order: [], front: [] },
      l1: 'BFS: red = [' + start + ']', l2: 'DFS: stog = [ ]' }];
    B.forEach(function (b, k) {
      var d = D[k];
      snaps.push({ b: b, d: d,
        l1: 'BFS posjet ' + (k + 1) + ': čvor ' + b.cur + '   red = [' + b.front.join(', ') + ']',
        l2: 'DFS posjet ' + (k + 1) + ': čvor ' + d.cur + '   stog = [' + d.front.join(' → ') + ']' });
    });

    function paint(G, st) {
      G.ids.forEach(function (id) {
        var cls = 'node';
        var oi = st.order.indexOf(id);
        if (oi !== -1) cls += ' vis';
        if (has(st.front, id)) cls += ' front';
        if (id === st.cur) cls += ' cur';
        G.nodes[id].g.setAttribute('class', cls);
        G.nodes[id].sub.textContent = oi === -1 ? '' : '#' + (oi + 1);
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
   - Uzmemo polje `(r, c)`.
   - Za svakog susjeda (gore, dolje, lijevo, desno):
     - Ako je slobodan i neposjećen: `dist[novi] = dist[stari] + 1` i dodamo ga u red.

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
   - Ako `i` nije posjećen:
     - `brojac++`
     - Pokrenemo `dfs(i)` $\to$ to će označiti cijelu komponentu kao posjećenu.

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

1. **[Counting Rooms](https://cses.fi/problemset/task/1192)**
   - Primjena DFS/BFS na 2D mreži za brojanje komponenata.
2. **[Labyrinth](https://cses.fi/problemset/task/1193)**
   - BFS za najkraći put + rekonstrukcija puta (pamtimo `parent` polje).
3. **[Building Teams](https://cses.fi/problemset/task/1668)**
   - Provjera je li graf bipartitan (2-bojanje grafa).
4. **[Message Route](https://cses.fi/problemset/task/1667)**
   - Klasičan BFS na grafu (ne na mreži).
5. **[Round Trip](https://cses.fi/problemset/task/1669)**
   - Detekcija ciklusa iz Problema 3, uz ispis samog ciklusa.

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

# Implementacija: Counting Rooms

```cpp
int n, m;
vector<string> grid;
vector<vector<bool>> visited;
int dx[] = {-1, 1, 0, 0};
int dy[] = {0, 0, -1, 1};

void dfs(int x, int y) {
    visited[x][y] = true;
    for (int i = 0; i < 4; ++i) {
        int nx = x + dx[i], ny = y + dy[i];
        if (nx >= 0 && nx < n && ny >= 0 && ny < m &&
            grid[nx][ny] == '.' && !visited[nx][ny]) {
            dfs(nx, ny);
        }
    }
}

// U main-u:
int rooms = 0;
for (int i = 0; i < n; ++i)
    for (int j = 0; j < m; ++j)
        if (grid[i][j] == '.' && !visited[i][j]) { rooms++; dfs(i, j); }
```

**Oprez:** rekurzija na mreži $1000 \times 1000$ može ići u dubinu do $10^6$. Lokalno (posebno na Windowsima) to može srušiti program zbog malog stacka, pa je BFS sigurniji izbor.

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

# Implementacija: Labyrinth (BFS)

```cpp
// Smjerovi: 0 = U, 1 = D, 2 = L, 3 = R
int dx[] = {-1, 1, 0, 0};
int dy[] = {0, 0, -1, 1};

queue<pair<int, int>> q;
q.push({sr, sc});
visited[sr][sc] = true;

while (!q.empty()) {
    auto [x, y] = q.front(); q.pop();
    if (x == er && y == ec) break; // Našli smo B

    for (int i = 0; i < 4; ++i) {
        int nx = x + dx[i], ny = y + dy[i];
        // isValid provjerava granice i zid
        if (isValid(nx, ny) && !visited[nx][ny]) {
            visited[nx][ny] = true;
            parent[nx][ny] = i; // Pamtimo indeks smjera
            q.push({nx, ny});
        }
    }
}
```

---

# Labyrinth: rekonstrukcija puta

Ako je `visited[er][ec]` true, idemo od `B` unatrag prema `A`:

```cpp
string path;
int x = er, y = ec;
while (x != sr || y != sc) {
    int d = parent[x][y];
    path += "UDLR"[d];   // Slovo za smjer kojim smo došli
    x -= dx[d];          // Pomak u suprotnom smjeru
    y -= dy[d];
}
reverse(path.begin(), path.end()); // Išli smo od kraja prema početku

cout << "YES\n" << path.size() << "\n" << path << "\n";
```

Ako `B` nije posjećen, ispisujemo `NO`.

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

<!-- _class: title -->
# 3. Building Teams (CSES)

## Bipartitnost grafa (2-bojanje)

---

# Analiza: Building Teams

**Problem:**
Treba podijeliti učenike u dva tima tako da nijedan par prijatelja nije u istom timu.

**Intuicija:**
Ovo je problem provjere je li graf **bipartitan**.
Graf je bipartitan ako se njegovi čvorovi mogu obojiti s 2 boje tako da svaki brid spaja čvorove različitih boja.

**Algoritam (BFS ili DFS):**

1. Prvi neobojani čvor obojimo bojom 1.
2. Sve njegove susjede obojimo bojom 2.
3. Sve susjede susjeda obojimo bojom 1...
4. Ako naiđemo na susjeda koji je već obojan **istom** bojom kao trenutni čvor $\to$ **IMPOSSIBLE** (postoji neparan ciklus).

---

# Implementacija: Building Teams

```cpp
vector<int> color(n + 1, 0); // 0: neobojano, 1: tim 1, 2: tim 2
bool possible = true;

for (int i = 1; i <= n; ++i) {
    if (color[i] == 0) { // Nova komponenta
        queue<int> q;
        q.push(i);
        color[i] = 1;

        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) {
                if (color[v] == 0) {
                    color[v] = (color[u] == 1) ? 2 : 1; // Suprotna boja
                    q.push(v);
                } else if (color[v] == color[u]) {
                    possible = false; // Konflikt!
                }
            }
        }
    }
}
if (!possible) cout << "IMPOSSIBLE\n";
else { for (int i = 1; i <= n; ++i) cout << color[i] << " "; cout << "\n"; }
```

---

# Building Teams korak po korak

Plavo = tim 1, narančasto = tim 2. Brid između dvaju čvorova iste boje je konflikt (neparan ciklus).

<style scoped>
.gr-teams { margin-top: 0.4em; }
.gr-teams .chips { font-size: 20px; margin-bottom: 0.5em; }
.gr-teams .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.gr-teams .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gr-teams .row { display: flex; gap: 8px; }
.gr-teams .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-teams .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gr-teams .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.gr-teams .cell.todo .val { color: #b5b5b5; }
.gr-teams .cell.src { background: #f5db7e; }
.gr-teams .cell.best { background: #9fdc9f; }
.gr-teams .cell.cur { background: var(--main); color: #fff; }
.gr-teams .cell.cur .idx, .gr-teams .cell.cur .val { color: #fff; }
.gr-teams .line1, .gr-teams .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.gr-teams .line1 { margin-top: 0.7em; }
.gr-teams .line2 { font-weight: bold; }
.gr-teams .ctrl { margin-top: 0.7em; }
.gr-teams button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gr-teams button:hover { background: var(--main); color: #fff; }
.gr-teams .hint { font-size: 16px; color: #6e6e6e; }
.gr-teams .gwrap { display: flex; justify-content: center; }
.gr-teams svg .edge { stroke: #a0a0a0; stroke-width: 3; transition: stroke .25s; }
.gr-teams svg .edge.tree { stroke: var(--main); stroke-width: 5; }
.gr-teams svg .edge.chk { stroke: #e0a800; stroke-width: 6; }
.gr-teams svg .edge.path { stroke: #2e9e44; stroke-width: 7; }
.gr-teams svg .edge.back { stroke: #d62828; stroke-width: 7; }
.gr-teams svg .node circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.gr-teams svg .node .lbl { font-size: 20px; font-weight: bold; fill: #141414; }
.gr-teams svg .node .sub { font-size: 16px; font-weight: bold; fill: #6e6e6e; }
.gr-teams svg .node.vis circle { fill: #f5db7e; }
.gr-teams svg .node.c1 circle { fill: #a9c5ff; }
.gr-teams svg .node.c2 circle { fill: #ffc58f; }
.gr-teams svg .node.c3 circle { fill: #a8e0a8; }
.gr-teams svg .node.c4 circle { fill: #e3b3ff; }
.gr-teams svg .node.path circle { fill: #9fdc9f; }
.gr-teams svg .node.front circle { stroke: var(--main); stroke-width: 5; stroke-dasharray: 6 4; }
.gr-teams svg .node.bad circle { stroke: #d62828; stroke-width: 5; }
.gr-teams svg .node.cur circle { fill: var(--main); stroke: var(--main); }
.gr-teams svg .node.cur .lbl { fill: #fff; }
.gr-teams svg .node.c2 circle { fill: #ffb067; }
</style>

<div class="gr-teams" data-pos="1:60,130;2:190,50;3:190,210;4:320,130;5:450,130;6:600,50;7:600,210" data-edges="1-2,1-3,2-4,3-4,4-5,6-7">
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
  document.querySelectorAll('.gr-teams').forEach(function (root) {
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
    var color = {}, possible = true, bad = [];
    var snaps = [{ color: {}, cur: -1, front: [], bad: [], l1: 'Svi čvorovi neobojani (color = 0)', l2: '' }];
    G.ids.forEach(function (i) {
      if (color[i]) return;
      color[i] = 1;
      var q = [i];
      snaps.push({ color: cp(color), cur: -1, front: cp(q), bad: cp(bad),
        l1: 'Čvor ' + i + ' je neobojan  → nova komponenta, ' + i + ' ide u tim 1', l2: 'red = [' + q.join(', ') + ']' });
      while (q.length) {
        var u = q.shift(), msg = [];
        G.adj[u].forEach(function (v) {
          if (!color[v]) {
            color[v] = color[u] === 1 ? 2 : 1;
            q.push(v);
            msg.push(v + ' → tim ' + color[v]);
          } else if (color[v] === color[u]) {
            possible = false;
            if (!hasEdge(bad, u, v)) bad.push([u, v]);
            msg.push('KONFLIKT ' + u + '–' + v);
          }
        });
        snaps.push({ color: cp(color), cur: u, front: cp(q), bad: cp(bad),
          l1: 'Uzimamo ' + u + ' (tim ' + color[u] + ')  → ' + (msg.length ? msg.join(', ') : 'svi susjedi već ispravno obojani'),
          l2: 'red = [' + q.join(', ') + ']' });
      }
    });
    snaps.push({ color: cp(color), cur: -1, front: [], bad: cp(bad),
      l1: possible ? 'Nema konflikata: graf je bipartitan' : 'Postoji konflikt: graf nije bipartitan',
      l2: possible ? 'Izlaz: ' + G.ids.map(function (id) { return color[id]; }).join(' ') + '   ✓' : 'IMPOSSIBLE' });
    function draw(s) {
      G.ids.forEach(function (id) {
        var cls = 'node';
        if (s.color[id]) cls += ' c' + s.color[id];
        if (has(s.front, id)) cls += ' front';
        if (id === s.cur) cls += ' cur';
        G.nodes[id].g.setAttribute('class', cls);
        G.nodes[id].sub.textContent = s.color[id] ? 'tim ' + s.color[id] : '';
      });
      G.edges.forEach(function (e) { e.el.setAttribute('class', hasEdge(s.bad, e.a, e.b) ? 'edge back' : 'edge'); });
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

<!-- _class: title -->
# 4. Message Route (CSES)

## Najkraći put u općem grafu

---

# Analiza: Message Route

**Problem:**
Mreža računala. Treba naći najkraći put (minimalan broj konekcija) od računala 1 do računala $N$.

**Sličnost s Labyrinthom:**
Isti princip (BFS za najkraći put + rekonstrukcija), ali struktura je **graf** (lista susjedstva), a ne 2D mreža.

**Struktura:**

- `adj[N]`: lista susjedstva.
- `dist[N]`: udaljenost od izvora (inicijalno $-1$, tj. neposjećen).
- `parent[N]`: prethodni čvor na putu (za rekonstrukciju).

---

# Implementacija: Message Route

```cpp
vector<int> dist(n + 1, -1), parent(n + 1, 0);
queue<int> q;
q.push(1);
dist[1] = 0;

while (!q.empty()) {
    int u = q.front(); q.pop();
    if (u == n) break; // Stigli smo do cilja

    for (int v : adj[u]) {
        if (dist[v] == -1) { // Ako nije posjećen
            dist[v] = dist[u] + 1;
            parent[v] = u;   // Pamtimo odakle smo došli
            q.push(v);
        }
    }
}

if (dist[n] == -1) { cout << "IMPOSSIBLE\n"; return 0; }

// Rekonstrukcija od n do 1 (parent[1] = 0 označava početak)
vector<int> path;
for (int curr = n; curr != 0; curr = parent[curr]) path.push_back(curr);
reverse(path.begin(), path.end());

cout << path.size() << "\n";
for (int x : path) cout << x << " ";
cout << "\n";
```

---

# Message Route korak po korak

Ispod čvora je `dist`, plavi bridovi su `parent` veze. Kad skinemo čvor N, put čitamo unatrag po roditeljima.

<style scoped>
.gr-route { margin-top: 0.4em; }
.gr-route .chips { font-size: 20px; margin-bottom: 0.5em; }
.gr-route .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.gr-route .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gr-route .row { display: flex; gap: 8px; }
.gr-route .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-route .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gr-route .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.gr-route .cell.todo .val { color: #b5b5b5; }
.gr-route .cell.src { background: #f5db7e; }
.gr-route .cell.best { background: #9fdc9f; }
.gr-route .cell.cur { background: var(--main); color: #fff; }
.gr-route .cell.cur .idx, .gr-route .cell.cur .val { color: #fff; }
.gr-route .line1, .gr-route .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.gr-route .line1 { margin-top: 0.7em; }
.gr-route .line2 { font-weight: bold; }
.gr-route .ctrl { margin-top: 0.7em; }
.gr-route button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gr-route button:hover { background: var(--main); color: #fff; }
.gr-route .hint { font-size: 16px; color: #6e6e6e; }
.gr-route .gwrap { display: flex; justify-content: center; }
.gr-route svg .edge { stroke: #a0a0a0; stroke-width: 3; transition: stroke .25s; }
.gr-route svg .edge.tree { stroke: var(--main); stroke-width: 5; }
.gr-route svg .edge.chk { stroke: #e0a800; stroke-width: 6; }
.gr-route svg .edge.path { stroke: #2e9e44; stroke-width: 7; }
.gr-route svg .edge.back { stroke: #d62828; stroke-width: 7; }
.gr-route svg .node circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.gr-route svg .node .lbl { font-size: 20px; font-weight: bold; fill: #141414; }
.gr-route svg .node .sub { font-size: 16px; font-weight: bold; fill: #6e6e6e; }
.gr-route svg .node.vis circle { fill: #f5db7e; }
.gr-route svg .node.c1 circle { fill: #a9c5ff; }
.gr-route svg .node.c2 circle { fill: #ffc58f; }
.gr-route svg .node.c3 circle { fill: #a8e0a8; }
.gr-route svg .node.c4 circle { fill: #e3b3ff; }
.gr-route svg .node.path circle { fill: #9fdc9f; }
.gr-route svg .node.front circle { stroke: var(--main); stroke-width: 5; stroke-dasharray: 6 4; }
.gr-route svg .node.bad circle { stroke: #d62828; stroke-width: 5; }
.gr-route svg .node.cur circle { fill: var(--main); stroke: var(--main); }
.gr-route svg .node.cur .lbl { fill: #fff; }
</style>

<div class="gr-route" data-pos="1:80,130;2:240,50;3:240,210;4:400,130;5:560,130" data-edges="1-2,1-3,1-4,2-3,5-4">
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
  document.querySelectorAll('.gr-route').forEach(function (root) {
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

    var G = makeGraph(root.querySelector('.g1'), root.dataset.pos, root.dataset.edges, 640, 260, 1);
    var n = Math.max.apply(null, G.ids);
    var dist = {}, parent = {}, tree = [];
    G.ids.forEach(function (id) { dist[id] = -1; parent[id] = 0; });
    var q = [1];
    dist[1] = 0;
    var snaps = [{ dist: cp(dist), cur: -1, front: [1], tree: [], path: [], l1: 'Start: 1 u redu, dist[1] = 0', l2: 'red = [1]' }];
    var found = false;
    while (q.length) {
      var u = q.shift();
      if (u === n) { found = true; break; }
      var added = [];
      G.adj[u].forEach(function (v) {
        if (dist[v] === -1) {
          dist[v] = dist[u] + 1;
          parent[v] = u;
          tree.push([u, v]);
          q.push(v);
          added.push(v + ' (dist ' + dist[v] + ')');
        }
      });
      snaps.push({ dist: cp(dist), cur: u, front: cp(q), tree: cp(tree), path: [],
        l1: 'Uzimamo ' + u + '  → ' + (added.length ? 'novi: ' + added.join(', ') : 'svi susjedi već posjećeni'),
        l2: 'red = [' + q.join(', ') + ']' });
    }
    if (found) {
      var path = [];
      for (var c = n; c !== 0; c = parent[c]) {
        path.unshift(c);
        snaps.push({ dist: cp(dist), cur: c, front: [], tree: cp(tree), path: path.slice(),
          l1: c === n ? 'Skinuli smo ' + n + ' s reda  → rekonstrukcija od ' + n : 'parent = ' + c,
          l2: 'put (unatrag): ' + path.slice().reverse().join(' ← ') });
      }
      snaps.push({ dist: cp(dist), cur: -1, front: [], tree: cp(tree), path: path.slice(),
        l1: 'Okrenemo put: ' + path.length + ' računala', l2: path.join(' ') + '   ✓' });
    } else {
      snaps.push({ dist: cp(dist), cur: -1, front: [], tree: cp(tree), path: [], l1: 'Red je prazan', l2: 'IMPOSSIBLE' });
    }
    function draw(s) {
      G.ids.forEach(function (id) {
        var cls = 'node';
        if (s.dist[id] !== -1) cls += ' vis';
        if (has(s.path, id)) cls += ' path';
        if (has(s.front, id)) cls += ' front';
        if (id === s.cur) cls += ' cur';
        G.nodes[id].g.setAttribute('class', cls);
        G.nodes[id].sub.textContent = s.dist[id] === -1 ? '' : 'd=' + s.dist[id];
      });
      G.edges.forEach(function (e) {
        var cls = hasEdge(s.tree, e.a, e.b) ? 'edge tree' : 'edge';
        var pi = s.path.indexOf(e.a), pj = s.path.indexOf(e.b);
        if (pi !== -1 ? (pj !== -1 ? Math.abs(pi - pj) === 1 : false) : false) cls = 'edge path';
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

# Zadaci za vježbu (Codeforces)

Preporuka: filtrirajte zadatke s tagom `graphs` i težinom `800-1200`.

[Codeforces Graph Problems](https://codeforces.com/problemset?order=BY_RATING_ASC&tags=graphs)