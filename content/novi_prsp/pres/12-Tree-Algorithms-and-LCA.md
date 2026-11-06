---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Algoritmi na stablima i LCA"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!-- _paginate: false -->
<!-- _class: title  -->
# Algoritmi na stablima i LCA

Programiranje za rješavanje složenih problema

---

# Sadržaj

1. **Osnovni pojmovi i svojstva**
   - Definicija stabla
   - Terminologija
2. **Obilazak stabla i DFS poredak**
   - Linearizacija (entry/exit times)
3. **Promjer stabla (Tree Diameter)**
   - Algoritam s dva DFS-a
4. **Najmanji zajednički predak (LCA)**
   - Binarno podizanje (Binary Lifting)
5. **Upiti nad putovima i podstablima**
   - Udaljenost, sume na putu
   - Flattening + BIT

---

<!-- _class: lead -->
# Osnovni pojmovi

## Što je stablo?

---

# Definicija i svojstva

**Stablo** je povezan graf koji se sastoji od $N$ čvorova i $N-1$ bridova te ne sadrži cikluse.

**Ključna svojstva:**

1. Između bilo koja dva čvora postoji točno jedan jednostavan put.
2. Dodavanjem bilo kojeg brida stvara se ciklus.
3. Micanjem bilo kojeg brida stablo prestaje biti povezano.

**Terminologija:**

- **Korijen (root):** fiksirani čvor od kojeg "visi" stablo.
- **List (leaf):** čvor bez djece (u ukorijenjenom stablu) ili stupnja 1.
- **Dubina (depth):** udaljenost čvora od korijena.
- **Podstablo (subtree):** čvor i svi njegovi potomci.

---

<!-- _class: lead -->
# Obilazak stabla

## DFS poredak i linearizacija

---

# Linearizacija stabla (tree flattening)

Osim samog posjećivanja, korisno je pamtiti **ulazna (entry)** i **izlazna (exit)** vremena za svaki čvor.
To nam omogućuje da stablo preslikamo na ravni niz.

```cpp
vector<int> adj[MAXN];
int tin[MAXN], tout[MAXN], timer;

void dfs(int u, int p) {
    tin[u] = ++timer; // Vrijeme ulaska

    for (int v : adj[u]) {
        if (v != p) dfs(v, u);
    }

    tout[u] = timer;  // Vrijeme izlaska (zadnji tin u podstablu)
}
```

**Svojstvo predaka:**
Čvor $u$ je predak čvora $v$ ako i samo ako vrijedi:
$$ tin[u] \le tin[v] \quad \text{i} \quad tout[u] \ge tout[v] $$

---

# DFS poredak korak po korak

Iznad čvora je `[tin, tout]`. Na kraju vidimo da svako podstablo zauzima uzastopni raspon u ravnom nizu.

<style scoped>
.tr-euler { margin-top: 0.3em; }
.tr-euler .chips { font-size: 20px; margin-bottom: 0.4em; }
.tr-euler .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.tr-euler .chip.take { background: #9fdc9f; }
.tr-euler .chip.skip, .tr-euler .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.tr-euler .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.tr-euler .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.tr-euler .row { display: flex; gap: 6px; }
.tr-euler .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.tr-euler .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.tr-euler .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.tr-euler .cell.todo .val { color: #b5b5b5; }
.tr-euler .cell.rng { background: #d6e6f5; }
.tr-euler .cell.best { background: #9fdc9f; }
.tr-euler .cell.src { background: #f5db7e; }
.tr-euler .cell.cur { background: var(--main); color: #fff; }
.tr-euler .cell.cur .idx, .tr-euler .cell.cur .val { color: #fff; }
.tr-euler .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.tr-euler .wrap { display: flex; gap: 28px; align-items: flex-start; }
.tr-euler .side { padding-top: 6px; }
.tr-euler .gsvg { display: block; overflow: visible; }
.tr-euler .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.tr-euler .e polygon { fill: #9a9a9a; }
.tr-euler .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.tr-euler .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.tr-euler .e.tree polygon { fill: #2f9e44; }
.tr-euler .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.tr-euler .e.off polygon { fill: #d5d5d5; }
.tr-euler .e.off .w { fill: #b5b5b5; }
.tr-euler .e.hid { opacity: 0; }
.tr-euler .e.bad line { stroke: #e03131; stroke-width: 6; }
.tr-euler .e.bad polygon { fill: #e03131; }
.tr-euler .e.on line { stroke: var(--main); stroke-width: 6; }
.tr-euler .e.on polygon { fill: var(--main); }
.tr-euler .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.tr-euler .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.tr-euler .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.tr-euler .n.c1 circle { fill: #ffd8a8; } .tr-euler .n.c2 circle { fill: #a5d8ff; } .tr-euler .n.c3 circle { fill: #b2f2bb; }
.tr-euler .n.c4 circle { fill: #fcc2d7; } .tr-euler .n.c5 circle { fill: #d0bfff; } .tr-euler .n.c6 circle { fill: #ffec99; }
.tr-euler .n.done circle { fill: #9fdc9f; }
.tr-euler .n.src circle { fill: #f5db7e; }
.tr-euler .n.cur circle { fill: var(--main); stroke: var(--main); }
.tr-euler .n.cur .id { fill: #fff; }
.tr-euler .tbl { display: grid; gap: 5px; }
.tr-euler .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.tr-euler .th.hl { background: var(--main); color: #fff; }
.tr-euler .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.tr-euler .tc.none { border-color: transparent; }
.tr-euler .tc.k { background: #e3ecf6; }
.tr-euler .tc.best { background: #9fdc9f; }
.tr-euler .tc.src { background: #f5db7e; }
.tr-euler .tc.cur { background: var(--main); color: #fff; }
.tr-euler .line1, .tr-euler .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.tr-euler .line1 { margin-top: 0.5em; }
.tr-euler .line2 { font-weight: bold; }
.tr-euler .ctrl { margin-top: 0.5em; }
.tr-euler button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.tr-euler button:hover { background: var(--main); color: #fff; }
.tr-euler .hint { font-size: 16px; color: #6e6e6e; }
.tr-euler .cell { width: 50px; }
.tr-euler .n .sub { font-size: 16px; }
</style>

<div class="tr-euler" data-edges="1-2,1-3,2-4,2-5,3-6,5-7,5-8,6-9" data-w="500" data-h="300" data-sub="2,3">
  <div class="wrap">
    <div class="graph"></div>
    <div class="side">
      <div class="lbl">tin[u]</div>
      <div class="row rin"></div>
      <div class="lbl">tout[u]</div>
      <div class="row rout"></div>
      <div class="lbl">Ravni niz (čvorovi po tin)</div>
      <div class="row rord"></div>
    </div>
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
  document.querySelectorAll('.tr-euler').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    var NS = 'http://www.w3.org/2000/svg';
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function sv(tag, attrs, parent) {
      var e = document.createElementNS(NS, tag);
      Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
      if (parent) parent.appendChild(e);
      return e;
    }
    function setc(el, cls) { el.setAttribute('class', cls); }
    function show(v) { return v === Infinity ? '∞' : (v === -Infinity ? '−∞' : String(v)); }
    function lt(a, b) { return a !== b ? Math.min(a, b) === a : false; }
    function le(a, b) { return Math.min(a, b) === a; }
    function fw(w) { return lt(w, 0) ? '(' + w + ')' : String(w); }
    function makeRow(box, count, base) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k + (base || 0)));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }
    function parsePos(s) {
      return s.trim().split(/\s+/).map(function (p) {
        var q = p.split(',').map(Number);
        return { x: q[0], y: q[1] };
      });
    }
    function parseEdges(s) {
      return s.split(',').map(function (t) {
        var q = t.trim().split(':'), ab = q[0].split('-');
        return { a: Number(ab[0]), b: Number(ab[1]), w: q.length === 2 ? Number(q[1]) : 0 };
      });
    }
    // Crta graf u SVG-u: čvorovi su numerirani od 1, bridovi su {a, b, w}
    function drawGraph(box, pos, edges, opt) {
      var R = opt.r || 22;
      var svg = sv('svg', { viewBox: '0 0 ' + opt.w + ' ' + opt.h, width: opt.w, height: opt.h, 'class': 'gsvg' }, box);
      var gE = sv('g', {}, svg), gN = sv('g', {}, svg);
      var E = edges.map(function (e) {
        var A = pos[e.a - 1], B = pos[e.b - 1];
        var dx = B.x - A.x, dy = B.y - A.y, L = Math.sqrt(dx * dx + dy * dy);
        var ux = dx / L, uy = dy / L;
        var x1 = A.x + ux * R, y1 = A.y + uy * R, x2 = B.x - ux * R, y2 = B.y - uy * R;
        var g = sv('g', { 'class': 'e' }, gE);
        sv('line', { x1: x1, y1: y1, x2: x2, y2: y2 }, g);
        if (opt.directed) {
          var bx = x2 - ux * 15, by = y2 - uy * 15;
          sv('polygon', { points: x2 + ',' + y2 + ' ' + (bx - uy * 7) + ',' + (by + ux * 7) + ' ' + (bx + uy * 7) + ',' + (by - ux * 7) }, g);
        }
        if (opt.weights) {
          var t = sv('text', { x: (A.x + B.x) / 2 - uy * 15, y: (A.y + B.y) / 2 + ux * 15, 'class': 'w' }, g);
          t.textContent = e.w;
        }
        return { g: g };
      });
      var N = pos.map(function (p, i) {
        var g = sv('g', { 'class': 'n' }, gN);
        sv('circle', { cx: p.x, cy: p.y, r: R }, g);
        var t = sv('text', { x: p.x, y: p.y, 'class': 'id' }, g);
        t.textContent = i + 1;
        var sub = sv('text', { x: p.x + (opt.subdx || 0), y: p.y + (opt.subdy === undefined ? -R - 13 : opt.subdy), 'class': 'sub' }, g);
        return { g: g, sub: sub };
      });
      return { E: E, N: N, svg: svg };
    }

    var tedges = parseEdges(root.dataset.edges);
    var n = tedges.length + 1;
    var adj = [];
    for (var i0 = 0; i0 !== n + 1; i0++) adj.push([]);
    tedges.forEach(function (e, k) { adj[e.a].push([e.b, k]); adj[e.b].push([e.a, k]); });
    // Raspored: listovi redom slijeva nadesno, roditelj iznad sredine svoje djece
    var px = [], py = [], par = [], parE = [], dep = [], leaf = 0, maxd = 0;
    for (var i1 = 0; i1 !== n + 1; i1++) { px.push(0); py.push(0); par.push(0); parE.push(-1); dep.push(0); }
    function layout(u, p, d) {
      par[u] = p; dep[u] = d; maxd = Math.max(maxd, d);
      var kids = adj[u].filter(function (q) { return q[0] !== p; });
      kids.forEach(function (q) { parE[q[0]] = q[1]; layout(q[0], u, d + 1); });
      if (kids.length === 0) { px[u] = leaf; leaf++; }
      else px[u] = (px[kids[0][0]] + px[kids[kids.length - 1][0]]) / 2;
    }
    layout(1, 0, 0);
    var TW = Number(root.dataset.w), TH = Number(root.dataset.h);
    var stepY = (TH - 70) / Math.max(1, maxd), stepX = (TW - 60) / Math.max(1, leaf - 1);
    var pos = [];
    for (var v0 = 1; v0 !== n + 1; v0++) pos.push({ x: 30 + px[v0] * stepX, y: 44 + dep[v0] * stepY });
    var G = drawGraph(root.querySelector('.graph'), pos, tedges, { w: TW, h: TH, directed: false, weights: false, r: Number(root.dataset.r || 20), subdx: root.dataset.subleft ? -36 : 0, subdy: root.dataset.subleft ? 0 : undefined });

    var tin = [], tout = [], order = [], clock = 0;
    for (var i2 = 0; i2 !== n + 1; i2++) { tin.push(0); tout.push(0); }
    var R1 = makeRow(root.querySelector('.rin'), n, 1);
    var R2 = makeRow(root.querySelector('.rout'), n, 1);
    var R3 = makeRow(root.querySelector('.rord'), n, 1);
    var snaps = [];
    function snap(o) {
      var s = { tin: tin.slice(), tout: tout.slice(), order: order.slice(), cur: -1, mode: '', sub: [], rng: [], l1: '', l2: '' };
      Object.keys(o).forEach(function (k) { s[k] = o[k]; });
      snaps.push(s);
    }
    snap({ l1: 'DFS iz korijena 1, timer = 0', l2: 'tin = vrijeme ulaska, tout = zadnji tin u podstablu' });
    function dfs(u, p) {
      tin[u] = ++clock; order.push(u);
      snap({ cur: u, mode: 'in', l1: 'Ulazimo u čvor ' + u + ':  tin[' + u + '] = ' + clock, l2: 'Čvor ' + u + ' dolazi na poziciju ' + clock + ' u ravnom nizu' });
      adj[u].forEach(function (q) { if (q[0] !== p) dfs(q[0], u); });
      tout[u] = clock;
      snap({ cur: u, mode: 'out', l1: 'Izlazimo iz čvora ' + u + ':  tout[' + u + '] = ' + clock, l2: 'Podstablo čvora ' + u + ' zauzima pozicije [' + tin[u] + ', ' + tout[u] + ']' });
    }
    dfs(1, 0);
    function subtree(u) { var r = [u]; adj[u].forEach(function (q) { if (q[0] !== par[u]) r = r.concat(subtree(q[0])); }); return r; }
    root.dataset.sub.split(',').map(Number).forEach(function (u) {
      var rng = [];
      for (var k = tin[u]; k !== tout[u] + 1; k++) rng.push(k);
      snap({ cur: u, sub: subtree(u), rng: rng,
        l1: 'Podstablo čvora ' + u + ' = uzastopni raspon [' + tin[u] + ', ' + tout[u] + '] u ravnom nizu',
        l2: 'Upit nad podstablom postaje upit nad rasponom niza (BIT ili segmentno stablo)   ✓' });
    });
    function draw(s) {
      G.N.forEach(function (nd, x) {
        var v = x + 1, c = 'n';
        if (s.tout[v]) c += ' done';
        if (s.sub.indexOf(v) !== -1) c += ' src';
        if (v === s.cur) c += ' cur';
        setc(nd.g, c);
        nd.sub.textContent = s.tin[v] ? '[' + s.tin[v] + ', ' + (s.tout[v] ? s.tout[v] : '…') + ']' : '';
      });
      G.E.forEach(function (e, k) {
        var b = tedges[k], ch = par[b.a] === b.b ? b.a : b.b;
        setc(e.g, s.tin[ch] ? 'e tree' : 'e');
      });
      R1.cells.forEach(function (cell, k) {
        var v = k + 1;
        setc(cell, (s.tin[v] ? 'cell' : 'cell todo') + (v === s.cur ? ' cur' : ''));
        R1.vals[k].textContent = s.tin[v] ? s.tin[v] : '';
      });
      R2.cells.forEach(function (cell, k) {
        var v = k + 1;
        setc(cell, (s.tout[v] ? 'cell' : 'cell todo') + (v === s.cur ? (s.mode === 'out' ? ' cur' : '') : ''));
        R2.vals[k].textContent = s.tout[v] ? s.tout[v] : '';
      });
      R3.cells.forEach(function (cell, k) {
        var c = 'cell';
        if (s.rng.indexOf(k + 1) !== -1) c += ' src';
        if (s.order[k] === s.cur) c += ' cur';
        setc(cell, c);
        R3.vals[k].textContent = s.order[k] === undefined ? '' : s.order[k];
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

<!-- _class: lead -->
# Promjer stabla

## Najdulji put u stablu

---

# Kako pronaći promjer?

**Promjer stabla** je maksimalna udaljenost između bilo koja dva čvora.

**Algoritam s dva DFS-a ($O(N)$)**

1. Odaberemo proizvoljan čvor $A$ (npr. korijen).
2. DFS-om pronađemo čvor najudaljeniji od $A$. Nazovimo ga $B$.
3. Pokrenemo DFS iz čvora $B$ i pronađemo čvor najudaljeniji od njega. Nazovimo ga $C$.
4. Udaljenost između $B$ i $C$ je promjer stabla.

*(Alternativa: dinamičko programiranje na stablu, gdje u svakom čvoru zbrojimo dva najdulja "kraka" prema djeci.)*

---

# Promjer stabla korak po korak

Broj iznad čvora je udaljenost od početka trenutnog DFS-a. Žuto je najdalji čvor pronađen do sada.

<style scoped>
.tr-diam { margin-top: 0.3em; }
.tr-diam .chips { font-size: 20px; margin-bottom: 0.4em; }
.tr-diam .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.tr-diam .chip.take { background: #9fdc9f; }
.tr-diam .chip.skip, .tr-diam .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.tr-diam .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.tr-diam .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.tr-diam .row { display: flex; gap: 6px; }
.tr-diam .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.tr-diam .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.tr-diam .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.tr-diam .cell.todo .val { color: #b5b5b5; }
.tr-diam .cell.rng { background: #d6e6f5; }
.tr-diam .cell.best { background: #9fdc9f; }
.tr-diam .cell.src { background: #f5db7e; }
.tr-diam .cell.cur { background: var(--main); color: #fff; }
.tr-diam .cell.cur .idx, .tr-diam .cell.cur .val { color: #fff; }
.tr-diam .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.tr-diam .wrap { display: flex; gap: 28px; align-items: flex-start; }
.tr-diam .side { padding-top: 6px; }
.tr-diam .gsvg { display: block; overflow: visible; }
.tr-diam .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.tr-diam .e polygon { fill: #9a9a9a; }
.tr-diam .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.tr-diam .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.tr-diam .e.tree polygon { fill: #2f9e44; }
.tr-diam .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.tr-diam .e.off polygon { fill: #d5d5d5; }
.tr-diam .e.off .w { fill: #b5b5b5; }
.tr-diam .e.hid { opacity: 0; }
.tr-diam .e.bad line { stroke: #e03131; stroke-width: 6; }
.tr-diam .e.bad polygon { fill: #e03131; }
.tr-diam .e.on line { stroke: var(--main); stroke-width: 6; }
.tr-diam .e.on polygon { fill: var(--main); }
.tr-diam .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.tr-diam .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.tr-diam .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.tr-diam .n.c1 circle { fill: #ffd8a8; } .tr-diam .n.c2 circle { fill: #a5d8ff; } .tr-diam .n.c3 circle { fill: #b2f2bb; }
.tr-diam .n.c4 circle { fill: #fcc2d7; } .tr-diam .n.c5 circle { fill: #d0bfff; } .tr-diam .n.c6 circle { fill: #ffec99; }
.tr-diam .n.done circle { fill: #9fdc9f; }
.tr-diam .n.src circle { fill: #f5db7e; }
.tr-diam .n.cur circle { fill: var(--main); stroke: var(--main); }
.tr-diam .n.cur .id { fill: #fff; }
.tr-diam .tbl { display: grid; gap: 5px; }
.tr-diam .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.tr-diam .th.hl { background: var(--main); color: #fff; }
.tr-diam .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.tr-diam .tc.none { border-color: transparent; }
.tr-diam .tc.k { background: #e3ecf6; }
.tr-diam .tc.best { background: #9fdc9f; }
.tr-diam .tc.src { background: #f5db7e; }
.tr-diam .tc.cur { background: var(--main); color: #fff; }
.tr-diam .line1, .tr-diam .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.tr-diam .line1 { margin-top: 0.5em; }
.tr-diam .line2 { font-weight: bold; }
.tr-diam .ctrl { margin-top: 0.5em; }
.tr-diam button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.tr-diam button:hover { background: var(--main); color: #fff; }
.tr-diam .hint { font-size: 16px; color: #6e6e6e; }
</style>

<div class="tr-diam" data-edges="1-2,1-3,2-4,2-5,3-6,5-7,5-8,6-9" data-w="620" data-h="300">
  <div class="graph"></div>
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
  document.querySelectorAll('.tr-diam').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    var NS = 'http://www.w3.org/2000/svg';
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function sv(tag, attrs, parent) {
      var e = document.createElementNS(NS, tag);
      Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
      if (parent) parent.appendChild(e);
      return e;
    }
    function setc(el, cls) { el.setAttribute('class', cls); }
    function show(v) { return v === Infinity ? '∞' : (v === -Infinity ? '−∞' : String(v)); }
    function lt(a, b) { return a !== b ? Math.min(a, b) === a : false; }
    function le(a, b) { return Math.min(a, b) === a; }
    function fw(w) { return lt(w, 0) ? '(' + w + ')' : String(w); }
    function makeRow(box, count, base) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k + (base || 0)));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }
    function parsePos(s) {
      return s.trim().split(/\s+/).map(function (p) {
        var q = p.split(',').map(Number);
        return { x: q[0], y: q[1] };
      });
    }
    function parseEdges(s) {
      return s.split(',').map(function (t) {
        var q = t.trim().split(':'), ab = q[0].split('-');
        return { a: Number(ab[0]), b: Number(ab[1]), w: q.length === 2 ? Number(q[1]) : 0 };
      });
    }
    // Crta graf u SVG-u: čvorovi su numerirani od 1, bridovi su {a, b, w}
    function drawGraph(box, pos, edges, opt) {
      var R = opt.r || 22;
      var svg = sv('svg', { viewBox: '0 0 ' + opt.w + ' ' + opt.h, width: opt.w, height: opt.h, 'class': 'gsvg' }, box);
      var gE = sv('g', {}, svg), gN = sv('g', {}, svg);
      var E = edges.map(function (e) {
        var A = pos[e.a - 1], B = pos[e.b - 1];
        var dx = B.x - A.x, dy = B.y - A.y, L = Math.sqrt(dx * dx + dy * dy);
        var ux = dx / L, uy = dy / L;
        var x1 = A.x + ux * R, y1 = A.y + uy * R, x2 = B.x - ux * R, y2 = B.y - uy * R;
        var g = sv('g', { 'class': 'e' }, gE);
        sv('line', { x1: x1, y1: y1, x2: x2, y2: y2 }, g);
        if (opt.directed) {
          var bx = x2 - ux * 15, by = y2 - uy * 15;
          sv('polygon', { points: x2 + ',' + y2 + ' ' + (bx - uy * 7) + ',' + (by + ux * 7) + ' ' + (bx + uy * 7) + ',' + (by - ux * 7) }, g);
        }
        if (opt.weights) {
          var t = sv('text', { x: (A.x + B.x) / 2 - uy * 15, y: (A.y + B.y) / 2 + ux * 15, 'class': 'w' }, g);
          t.textContent = e.w;
        }
        return { g: g };
      });
      var N = pos.map(function (p, i) {
        var g = sv('g', { 'class': 'n' }, gN);
        sv('circle', { cx: p.x, cy: p.y, r: R }, g);
        var t = sv('text', { x: p.x, y: p.y, 'class': 'id' }, g);
        t.textContent = i + 1;
        var sub = sv('text', { x: p.x + (opt.subdx || 0), y: p.y + (opt.subdy === undefined ? -R - 13 : opt.subdy), 'class': 'sub' }, g);
        return { g: g, sub: sub };
      });
      return { E: E, N: N, svg: svg };
    }

    var tedges = parseEdges(root.dataset.edges);
    var n = tedges.length + 1;
    var adj = [];
    for (var i0 = 0; i0 !== n + 1; i0++) adj.push([]);
    tedges.forEach(function (e, k) { adj[e.a].push([e.b, k]); adj[e.b].push([e.a, k]); });
    // Raspored: listovi redom slijeva nadesno, roditelj iznad sredine svoje djece
    var px = [], py = [], par = [], parE = [], dep = [], leaf = 0, maxd = 0;
    for (var i1 = 0; i1 !== n + 1; i1++) { px.push(0); py.push(0); par.push(0); parE.push(-1); dep.push(0); }
    function layout(u, p, d) {
      par[u] = p; dep[u] = d; maxd = Math.max(maxd, d);
      var kids = adj[u].filter(function (q) { return q[0] !== p; });
      kids.forEach(function (q) { parE[q[0]] = q[1]; layout(q[0], u, d + 1); });
      if (kids.length === 0) { px[u] = leaf; leaf++; }
      else px[u] = (px[kids[0][0]] + px[kids[kids.length - 1][0]]) / 2;
    }
    layout(1, 0, 0);
    var TW = Number(root.dataset.w), TH = Number(root.dataset.h);
    var stepY = (TH - 70) / Math.max(1, maxd), stepX = (TW - 60) / Math.max(1, leaf - 1);
    var pos = [];
    for (var v0 = 1; v0 !== n + 1; v0++) pos.push({ x: 30 + px[v0] * stepX, y: 44 + dep[v0] * stepY });
    var G = drawGraph(root.querySelector('.graph'), pos, tedges, { w: TW, h: TH, directed: false, weights: false, r: Number(root.dataset.r || 20), subdx: root.dataset.subleft ? -36 : 0, subdy: root.dataset.subleft ? 0 : undefined });

    var snaps = [], dist = [], best = -1, far = -1, from = [];
    function clearDist() { dist = []; from = []; for (var i = 0; i !== n + 1; i++) { dist.push(-1); from.push(-1); } best = -1; far = -1; }
    function snap(o) {
      var s = { dist: dist.slice(), far: far, cur: -1, a: -1, path: [], pathE: [], l1: '', l2: '' };
      Object.keys(o).forEach(function (k) { s[k] = o[k]; });
      snaps.push(s);
    }
    function dfs(u, p, d, hd) {
      dist[u] = d;
      var l1 = 'DFS posjećuje čvor ' + u + ' na udaljenosti ' + d;
      if (Math.max(d, best) !== best) { best = d; far = u; l1 += '  → novi najdalji čvor'; }
      snap({ cur: u, a: hd.a, l1: l1, l2: hd.t + ': najdalji do sada je čvor ' + far + ' (' + best + ')' });
      adj[u].forEach(function (q) { if (q[0] !== p) { from[q[0]] = q[1]; dfs(q[0], u, d + 1, hd); } });
    }
    clearDist();
    snap({ l1: 'Promjer = najdulji put u stablu. Rješenje: dva DFS-a, O(N).', l2: '1. DFS kreće iz proizvoljnog čvora (ovdje 1)' });
    dfs(1, 0, 0, { t: '1. DFS iz čvora 1', a: -1 });
    var A = far;
    snap({ far: A, a: A, l1: 'Najdalji čvor od 1 je A = ' + A + '. On je sigurno jedan kraj promjera.', l2: '2. DFS kreće iz A = ' + A });
    clearDist();
    dfs(A, 0, 0, { t: '2. DFS iz čvora ' + A, a: A });
    var B = far, path = [B], pe = [];
    for (var v = B; v !== A; ) {
      var e = tedges[from[v]];
      pe.push(from[v]);
      v = e.a === v ? e.b : e.a;
      path.push(v);
    }
    snap({ far: B, a: A, path: path, pathE: pe, l1: 'Najdalji čvor od A je B = ' + B + '. Put A → B je promjer.',
      l2: 'Promjer = ' + best + ' bridova: ' + path.slice().reverse().join(' – ') + '   ✓' });
    function draw(s) {
      G.N.forEach(function (nd, x) {
        var v = x + 1, c = 'n';
        if (s.dist[v] !== -1) c += ' done';
        if (s.path.indexOf(v) !== -1) c += ' done';
        if (v === s.far) c += ' src';
        if (v === s.a) c += ' src';
        if (v === s.cur) c += ' cur';
        setc(nd.g, c);
        nd.sub.textContent = s.dist[v] === -1 ? '' : s.dist[v];
      });
      G.E.forEach(function (e, k) { setc(e.g, s.pathE.indexOf(k) !== -1 ? 'e tree' : 'e'); });
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

<!-- _class: lead -->
# Najmanji zajednički predak (LCA)

## Lowest Common Ancestor

---

# Problem LCA

**Definicija:** LCA čvorova $u$ i $v$ je čvor koji je predak i od $u$ i od $v$, a nalazi se na najvećoj dubini (najdalje od korijena).

**Metoda: binarno podizanje (binary lifting)**
Unaprijed izračunamo pretke na udaljenostima $2^0, 2^1, 2^2, \dots$.
Neka je `up[u][i]` predak čvora $u$ na udaljenosti $2^i$.

**Rekurzivna relacija:**
$$ up[u][i] = up[up[u][i-1]][i-1] $$
*(Predak na udaljenosti $2^i$ je predak na udaljenosti $2^{i-1}$ od pretka na udaljenosti $2^{i-1}$.)*

**Složenost:**

- Preprocessing: $O(N \log N)$
- Upit: $O(\log N)$

---

# Implementacija: preprocessing

```cpp
const int LOG = 20;
int up[MAXN][LOG];
int depth[MAXN];

// Poziv: dfs_lca(korijen, 0, 0). Čvor 0 služi kao "iznad korijena".
void dfs_lca(int u, int p, int d) {
    depth[u] = d;
    up[u][0] = p; // 2^0 = 1. predak je roditelj

    for (int i = 1; i < LOG; i++) {
        up[u][i] = up[up[u][i-1]][i-1];
    }

    for (int v : adj[u]) {
        if (v != p) dfs_lca(v, u, d + 1);
    }
}
```

---

# Implementacija: LCA upit

```cpp
int get_lca(int u, int v) {
    if (depth[u] < depth[v]) swap(u, v); // Sada je u dublji

    // 1. Izjednačimo dubine: podižemo dubljeg u na razinu v
    for (int i = LOG - 1; i >= 0; i--) {
        if (depth[u] - (1 << i) >= depth[v]) {
            u = up[u][i];
        }
    }

    if (u == v) return u;

    // 2. Podižemo oba dok ne budu točno ispod LCA
    for (int i = LOG - 1; i >= 0; i--) {
        if (up[u][i] != up[v][i]) {
            u = up[u][i];
            v = up[v][i];
        }
    }
    return up[u][0]; // Vraćamo roditelja
}
```

---

# LCA (binary lifting) korak po korak

Gradimo tablicu `up`, izjednačimo dubine, zatim skačemo oba čvora dok su im preci različiti.

<style scoped>
.tr-lca { margin-top: 0.3em; }
.tr-lca .chips { font-size: 20px; margin-bottom: 0.4em; }
.tr-lca .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.tr-lca .chip.take { background: #9fdc9f; }
.tr-lca .chip.skip, .tr-lca .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.tr-lca .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.tr-lca .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.tr-lca .row { display: flex; gap: 6px; }
.tr-lca .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.tr-lca .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.tr-lca .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.tr-lca .cell.todo .val { color: #b5b5b5; }
.tr-lca .cell.rng { background: #d6e6f5; }
.tr-lca .cell.best { background: #9fdc9f; }
.tr-lca .cell.src { background: #f5db7e; }
.tr-lca .cell.cur { background: var(--main); color: #fff; }
.tr-lca .cell.cur .idx, .tr-lca .cell.cur .val { color: #fff; }
.tr-lca .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.tr-lca .wrap { display: flex; gap: 28px; align-items: flex-start; }
.tr-lca .side { padding-top: 6px; }
.tr-lca .gsvg { display: block; overflow: visible; }
.tr-lca .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.tr-lca .e polygon { fill: #9a9a9a; }
.tr-lca .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.tr-lca .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.tr-lca .e.tree polygon { fill: #2f9e44; }
.tr-lca .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.tr-lca .e.off polygon { fill: #d5d5d5; }
.tr-lca .e.off .w { fill: #b5b5b5; }
.tr-lca .e.hid { opacity: 0; }
.tr-lca .e.bad line { stroke: #e03131; stroke-width: 6; }
.tr-lca .e.bad polygon { fill: #e03131; }
.tr-lca .e.on line { stroke: var(--main); stroke-width: 6; }
.tr-lca .e.on polygon { fill: var(--main); }
.tr-lca .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.tr-lca .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.tr-lca .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.tr-lca .n.c1 circle { fill: #ffd8a8; } .tr-lca .n.c2 circle { fill: #a5d8ff; } .tr-lca .n.c3 circle { fill: #b2f2bb; }
.tr-lca .n.c4 circle { fill: #fcc2d7; } .tr-lca .n.c5 circle { fill: #d0bfff; } .tr-lca .n.c6 circle { fill: #ffec99; }
.tr-lca .n.done circle { fill: #9fdc9f; }
.tr-lca .n.src circle { fill: #f5db7e; }
.tr-lca .n.cur circle { fill: var(--main); stroke: var(--main); }
.tr-lca .n.cur .id { fill: #fff; }
.tr-lca .tbl { display: grid; gap: 5px; }
.tr-lca .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.tr-lca .th.hl { background: var(--main); color: #fff; }
.tr-lca .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.tr-lca .tc.none { border-color: transparent; }
.tr-lca .tc.k { background: #e3ecf6; }
.tr-lca .tc.best { background: #9fdc9f; }
.tr-lca .tc.src { background: #f5db7e; }
.tr-lca .tc.cur { background: var(--main); color: #fff; }
.tr-lca .line1, .tr-lca .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.tr-lca .line1 { margin-top: 0.5em; }
.tr-lca .line2 { font-weight: bold; }
.tr-lca .ctrl { margin-top: 0.5em; }
.tr-lca button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.tr-lca button:hover { background: var(--main); color: #fff; }
.tr-lca .hint { font-size: 16px; color: #6e6e6e; }
.tr-lca .th { font-size: 17px; }
.tr-lca .tc { font-size: 19px; }
.tr-lca .side { padding-top: 20px; }
.tr-lca .wrap { gap: 36px; }
</style>

<div class="tr-lca" data-edges="1-2,1-3,2-4,2-5,4-6,4-7,6-8,8-9,3-10,10-11,11-12" data-w="440" data-h="290" data-r="18" data-subleft="1" data-q="9,7|12,5">
  <div class="wrap">
    <div class="graph"></div>
    <div class="side">
      <div class="tbl"></div>
    </div>
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
  document.querySelectorAll('.tr-lca').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    var NS = 'http://www.w3.org/2000/svg';
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function sv(tag, attrs, parent) {
      var e = document.createElementNS(NS, tag);
      Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
      if (parent) parent.appendChild(e);
      return e;
    }
    function setc(el, cls) { el.setAttribute('class', cls); }
    function show(v) { return v === Infinity ? '∞' : (v === -Infinity ? '−∞' : String(v)); }
    function lt(a, b) { return a !== b ? Math.min(a, b) === a : false; }
    function le(a, b) { return Math.min(a, b) === a; }
    function fw(w) { return lt(w, 0) ? '(' + w + ')' : String(w); }
    function makeRow(box, count, base) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k + (base || 0)));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }
    function parsePos(s) {
      return s.trim().split(/\s+/).map(function (p) {
        var q = p.split(',').map(Number);
        return { x: q[0], y: q[1] };
      });
    }
    function parseEdges(s) {
      return s.split(',').map(function (t) {
        var q = t.trim().split(':'), ab = q[0].split('-');
        return { a: Number(ab[0]), b: Number(ab[1]), w: q.length === 2 ? Number(q[1]) : 0 };
      });
    }
    // Crta graf u SVG-u: čvorovi su numerirani od 1, bridovi su {a, b, w}
    function drawGraph(box, pos, edges, opt) {
      var R = opt.r || 22;
      var svg = sv('svg', { viewBox: '0 0 ' + opt.w + ' ' + opt.h, width: opt.w, height: opt.h, 'class': 'gsvg' }, box);
      var gE = sv('g', {}, svg), gN = sv('g', {}, svg);
      var E = edges.map(function (e) {
        var A = pos[e.a - 1], B = pos[e.b - 1];
        var dx = B.x - A.x, dy = B.y - A.y, L = Math.sqrt(dx * dx + dy * dy);
        var ux = dx / L, uy = dy / L;
        var x1 = A.x + ux * R, y1 = A.y + uy * R, x2 = B.x - ux * R, y2 = B.y - uy * R;
        var g = sv('g', { 'class': 'e' }, gE);
        sv('line', { x1: x1, y1: y1, x2: x2, y2: y2 }, g);
        if (opt.directed) {
          var bx = x2 - ux * 15, by = y2 - uy * 15;
          sv('polygon', { points: x2 + ',' + y2 + ' ' + (bx - uy * 7) + ',' + (by + ux * 7) + ' ' + (bx + uy * 7) + ',' + (by - ux * 7) }, g);
        }
        if (opt.weights) {
          var t = sv('text', { x: (A.x + B.x) / 2 - uy * 15, y: (A.y + B.y) / 2 + ux * 15, 'class': 'w' }, g);
          t.textContent = e.w;
        }
        return { g: g };
      });
      var N = pos.map(function (p, i) {
        var g = sv('g', { 'class': 'n' }, gN);
        sv('circle', { cx: p.x, cy: p.y, r: R }, g);
        var t = sv('text', { x: p.x, y: p.y, 'class': 'id' }, g);
        t.textContent = i + 1;
        var sub = sv('text', { x: p.x + (opt.subdx || 0), y: p.y + (opt.subdy === undefined ? -R - 13 : opt.subdy), 'class': 'sub' }, g);
        return { g: g, sub: sub };
      });
      return { E: E, N: N, svg: svg };
    }

    var tedges = parseEdges(root.dataset.edges);
    var n = tedges.length + 1;
    var adj = [];
    for (var i0 = 0; i0 !== n + 1; i0++) adj.push([]);
    tedges.forEach(function (e, k) { adj[e.a].push([e.b, k]); adj[e.b].push([e.a, k]); });
    // Raspored: listovi redom slijeva nadesno, roditelj iznad sredine svoje djece
    var px = [], py = [], par = [], parE = [], dep = [], leaf = 0, maxd = 0;
    for (var i1 = 0; i1 !== n + 1; i1++) { px.push(0); py.push(0); par.push(0); parE.push(-1); dep.push(0); }
    function layout(u, p, d) {
      par[u] = p; dep[u] = d; maxd = Math.max(maxd, d);
      var kids = adj[u].filter(function (q) { return q[0] !== p; });
      kids.forEach(function (q) { parE[q[0]] = q[1]; layout(q[0], u, d + 1); });
      if (kids.length === 0) { px[u] = leaf; leaf++; }
      else px[u] = (px[kids[0][0]] + px[kids[kids.length - 1][0]]) / 2;
    }
    layout(1, 0, 0);
    var TW = Number(root.dataset.w), TH = Number(root.dataset.h);
    var stepY = (TH - 70) / Math.max(1, maxd), stepX = (TW - 60) / Math.max(1, leaf - 1);
    var pos = [];
    for (var v0 = 1; v0 !== n + 1; v0++) pos.push({ x: 30 + px[v0] * stepX, y: 44 + dep[v0] * stepY });
    var G = drawGraph(root.querySelector('.graph'), pos, tedges, { w: TW, h: TH, directed: false, weights: false, r: Number(root.dataset.r || 20), subdx: root.dataset.subleft ? -36 : 0, subdy: root.dataset.subleft ? 0 : undefined });

    var LOG = 1;
    while (le(Math.pow(2, LOG), maxd)) LOG++;
    var tbl = root.querySelector('.tbl');
    tbl.style.gridTemplateColumns = '96px repeat(' + n + ', 40px)';
    tbl.appendChild(mk('div', 'th', 'u'));
    var CH = [null];
    for (var c0 = 1; c0 !== n + 1; c0++) CH.push(tbl.appendChild(mk('div', 'th', c0)));
    var T = [];
    for (var i = 0; i !== LOG; i++) {
      tbl.appendChild(mk('div', 'th', 'up[u][' + i + ']'));
      var row = [null];
      for (var c1 = 1; c1 !== n + 1; c1++) row.push(tbl.appendChild(mk('div', 'tc')));
      T.push(row);
    }
    var up = [];
    for (var i2 = 0; i2 !== LOG; i2++) { var r2 = []; for (var v2 = 0; v2 !== n + 1; v2++) r2.push(0); up.push(r2); }
    var snaps = [], filled = 0;
    function snap(o) {
      var s = { filled: filled, u: -1, v: -1, cell: null, ans: -1, l1: '', l2: '' };
      Object.keys(o).forEach(function (k) { s[k] = o[k]; });
      snaps.push(s);
    }
    snap({ l1: 'Brojevi lijevo od čvorova su dubine. Čvor 0 znači „iznad korijena”.', l2: 'up[u][i] = predak čvora u na udaljenosti 2^i' });
    for (var v3 = 1; v3 !== n + 1; v3++) up[0][v3] = par[v3];
    filled = 1;
    snap({ l1: 'up[u][0] = roditelj čvora u', l2: 'Prvi redak tablice čitamo izravno iz stabla' });
    for (var i3 = 1; i3 !== LOG; i3++) {
      for (var v4 = 1; v4 !== n + 1; v4++) up[i3][v4] = up[i3 - 1][up[i3 - 1][v4]];
      filled = i3 + 1;
      snap({ l1: 'up[u][' + i3 + '] = up[ up[u][' + (i3 - 1) + '] ][' + (i3 - 1) + ']', l2: 'Skok za ' + Math.pow(2, i3) + ' = dva skoka za ' + Math.pow(2, i3 - 1) });
    }
    root.dataset.q.split('|').forEach(function (qs) {
      var uv = qs.split(',').map(Number), u = uv[0], v = uv[1];
      var hd = 'LCA(' + u + ', ' + v + ')';
      snap({ u: u, v: v, l1: hd + ':  dubina[' + u + '] = ' + dep[u] + ', dubina[' + v + '] = ' + dep[v], l2: 'Plavi čvor je u, žuti je v' });
      if (lt(dep[u], dep[v])) { var t = u; u = v; v = t; snap({ u: u, v: v, l1: 'Zamjena: u mora biti dublji, sada u = ' + u + ', v = ' + v, l2: hd }); }
      for (var i = LOG - 1; i !== -1; i--) {
        var p = Math.pow(2, i);
        if (le(dep[v], dep[u] - p)) {
          var nu = up[i][u];
          snap({ u: u, v: v, cell: [i, u], l1: '1. faza, i = ' + i + ':  ' + dep[u] + ' − ' + p + ' = ' + (dep[u] - p) + ' ≥ ' + dep[v] + '  → u = up[' + u + '][' + i + '] = ' + nu, l2: hd + ': izjednačavamo dubine' });
          u = nu;
        } else {
          snap({ u: u, v: v, cell: [i, u], l1: '1. faza, i = ' + i + ':  ' + dep[u] + ' − ' + p + ' = ' + (dep[u] - p) + ' manje je od ' + dep[v] + '  → ne skačemo', l2: hd + ': izjednačavamo dubine' });
        }
      }
      snap({ u: u, v: v, l1: 'Dubine su jednake: u = ' + u + ', v = ' + v + (u === v ? ', isti čvor' : ', različiti čvorovi'), l2: hd });
      if (u === v) {
        snap({ ans: u, l1: 'u = v, pa je to traženi predak', l2: hd + ' = ' + u + '   ✓' });
        return;
      }
      for (var j = LOG - 1; j !== -1; j--) {
        var a = up[j][u], b = up[j][v];
        if (a !== b) {
          snap({ u: u, v: v, cell: [j, u], cell2: [j, v], l1: '2. faza, i = ' + j + ':  up[' + u + '][' + j + '] = ' + a + ', up[' + v + '][' + j + '] = ' + b + ' su različiti  → skačemo oba', l2: hd });
          u = a; v = b;
        } else {
          snap({ u: u, v: v, cell: [j, u], cell2: [j, v], l1: '2. faza, i = ' + j + ':  oba skoka vode u ' + a + '  → ne skačemo (bili bismo na LCA ili iznad)', l2: hd });
        }
      }
      snap({ u: u, v: v, ans: up[0][u], l1: 'u = ' + u + ' i v = ' + v + ' su točno ispod LCA, pa je odgovor njihov roditelj', l2: hd + ' = up[' + u + '][0] = ' + up[0][u] + '   ✓' });
    });
    function draw(s) {
      G.N.forEach(function (nd, x) {
        var w = x + 1, c = 'n';
        if (w === s.ans) c += ' done';
        if (w === s.v) c += ' src';
        if (w === s.u) c += ' cur';
        setc(nd.g, c);
        nd.sub.textContent = dep[w];
      });
      for (var i = 0; i !== LOG; i++) {
        for (var w = 1; w !== n + 1; w++) {
          var c = 'tc';
          if (s.cell ? (s.cell[0] === i ? s.cell[1] === w : false) : false) c += ' cur';
          if (s.cell2 ? (s.cell2[0] === i ? s.cell2[1] === w : false) : false) c += ' src';
          setc(T[i][w], c);
          T[i][w].textContent = Math.max(i, s.filled - 1) === s.filled - 1 ? up[i][w] : '';
        }
      }
      CH.forEach(function (h, w) { if (h) setc(h, w === s.u ? 'th hl' : 'th'); });
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

<!-- _class: lead -->
# Upiti nad putovima

## Udaljenosti i sume

---

# Udaljenost i sume na putu

Jednom kad imamo LCA, lako računamo udaljenosti. Put od $u$ do $v$ ide $u \to LCA \to v$.

**Udaljenost (broj bridova)**
$$ dist(u, v) = depth[u] + depth[v] - 2 \cdot depth[LCA(u, v)] $$

**Suma vrijednosti čvorova na putu**
Koristimo prefiksne sume od korijena do čvora (`P[u]`, uključujući i sam čvor $u$).
$$ PathSum(u, v) = P[u] + P[v] - 2 \cdot P[LCA(u, v)] + Value(LCA(u, v)) $$

*(Dodajemo `Value(LCA)` jer smo ga dvaput oduzeli, a on je dio puta.)*

---

<!-- _class: lead -->
# Upiti nad podstablima

## Subtree Queries

---

# Linearizacija + strukture podataka

Često imamo upite: "promijeni vrijednost čvora $u$" i "daj sumu podstabla $v$".

**Ključna ideja:**
Podstablo čvora $u$ odgovara kontinuiranom rasponu indeksa $[tin[u], tout[u]]$ u DFS obilasku.

**Rješenje:**

1. Vrijednosti čvorova preslikamo u niz na pozicije `tin[u]`.
2. Nad tim nizom izgradimo **Fenwickovo stablo (BIT)** ili **segmentno stablo**.
3. **Update:** ažuriramo indeks `tin[u]` u BIT-u.
4. **Query:** suma raspona $[tin[u], tout[u]]$ u BIT-u.

---

<!-- _class: lead -->
# Zadaci za vježbu

## CSES Problem Set

---

# Zadaci

1. **[Tree Diameter](https://cses.fi/problemset/task/1131)**
   - Promjer stabla (2x DFS).
2. **[Company Queries I](https://cses.fi/problemset/task/1687) i [II](https://cses.fi/problemset/task/1688)**
   - K-ti predak i LCA (binary lifting).
3. **[Distance Queries](https://cses.fi/problemset/task/1135)**
   - Udaljenost između čvorova pomoću LCA.
4. **[Subtree Queries](https://cses.fi/problemset/task/1137)**
   - Ažuriranje vrijednosti i suma podstabla (linearizacija + BIT).
5. **[Path Queries](https://cses.fi/problemset/task/1138)**
   - Ažuriranje i suma na putu od korijena (malo teže, ali sličan princip).

---

<!-- _class: title -->
# Tree Diameter (CSES)

## Najdulji put u stablu

---

# Analiza: Tree Diameter

**Problem:**
Zadano je stablo od $N$ čvorova. Treba pronaći promjer stabla (maksimalnu udaljenost između dva čvora).
**Ograničenja:** $N \le 2 \cdot 10^5$.

**Intuicija (2x DFS)**
Naivni pristup (BFS iz svakog čvora) je $O(N^2)$, presporo.
Postoji elegantan algoritam u $O(N)$:

1. Odaberemo proizvoljan čvor $x$ (npr. 1).
2. Pronađemo čvor najudaljeniji od $x$. Nazovimo ga $a$.
3. Pronađemo čvor najudaljeniji od $a$. Nazovimo ga $b$.
4. Udaljenost između $a$ i $b$ je promjer.

---

# Implementacija: Tree Diameter

```cpp
void dfs(int u, int p, int d, int &max_d, int &farthest_node) {
    if (d > max_d) {
        max_d = d;
        farthest_node = u;
    }
    for (int v : adj[u]) {
        if (v != p) dfs(v, u, d + 1, max_d, farthest_node);
    }
}

// U main funkciji:
int max_d = -1, node_a = -1, node_b = -1;
dfs(1, 0, 0, max_d, node_a);      // Prvi DFS nalazi node_a
max_d = -1;
dfs(node_a, 0, 0, max_d, node_b); // Drugi DFS nalazi node_b i promjer
cout << max_d << "\n";
```

---

<!-- _class: title -->
# Company Queries I & II (CSES)

## Binary lifting u akciji

---

# Analiza: Company Queries

**Problem I:** tko je $k$-ti šef (predak) zaposlenika $x$? (Ako ne postoji, ispisujemo $-1$.)
**Problem II:** tko je najniži zajednički šef (LCA) zaposlenika $a$ i $b$?

**Intuicija: binary lifting**
Ne možemo skakati po jednog pretka ($O(N)$ po upitu).
Pamtimo pretke na udaljenostima $1, 2, 4, 8, \dots$:
`up[u][i]` = predak čvora $u$ na udaljenosti $2^i$.

Ulaz direktno daje šefa svakog zaposlenika, pa je `up[u][0] = šef[u]`.

**Izgradnja ($O(N \log N)$):**
`up[u][i] = up[up[u][i-1]][i-1]`

---

# Implementacija: k-ti predak

Kako naći $k$-tog pretka u $O(\log N)$?
$k$ zapišemo binarno. Ako je $k = 13$ ($1101_2 = 8 + 4 + 1$), skačemo za 8, pa za 4, pa za 1.

```cpp
int get_kth_ancestor(int node, int k) {
    for (int i = 0; i < LOG; i++) {
        if ((k >> i) & 1) { // Ako je i-ti bit postavljen
            node = up[node][i];
        }
    }
    return node; // 0 ako takav predak ne postoji
}

// Company Queries I: ispis
int r = get_kth_ancestor(x, k);
cout << (r == 0 ? -1 : r) << "\n";
```

Za **Company Queries II** koristimo standardnu LCA funkciju opisanu ranije u prezentaciji.

---

<!-- _class: title -->
# Distance Queries (CSES)

## Primjena LCA

---

# Analiza: Distance Queries

**Problem:**
Zadano je stablo i $Q$ upita. Za svaki par čvorova $(u, v)$ treba ispisati njihovu udaljenost (broj bridova).

**Intuicija**
Put između $u$ i $v$ u stablu je jedinstven. Ide od $u$ gore do $LCA(u, v)$ i zatim dolje do $v$.
Udaljenost je zbroj udaljenosti od $u$ do LCA i od $v$ do LCA.

$$ dist(u, v) = depth[u] + depth[v] - 2 \cdot depth[LCA(u, v)] $$

---

# Implementacija: Distance Queries

```cpp
// Preprocessing: dubine i up[][] tablica (dfs_lca)

while (q--) {
    int u, v;
    cin >> u >> v;
    int lca = get_lca(u, v);
    cout << depth[u] + depth[v] - 2 * depth[lca] << "\n";
}
```

**Napomena:** ovo je standardni obrazac. Ako bridovi imaju težine, umjesto `depth` (broj bridova) koristimo `dist_from_root` (zbroj težina).

---

<!-- _class: title -->
# Subtree Queries (CSES)

## Linearizacija i BIT

---

# Analiza: Subtree Queries

**Problem:**

1. **Update:** vrijednost čvora $u$ postaje $x$.
2. **Query:** suma vrijednosti u cijelom podstablu čvora $u$.

**Intuicija**
Stabla su teška za rasponske upite, a nizovi su laki.
Koristimo **DFS ulazna (tin) i izlazna (tout)** vremena.
Podstablo čvora $u$ odgovara kontinuiranom rasponu $[tin[u], tout[u]]$ u nizu.

Problem svodimo na:

1. **Point update:** promjena vrijednosti na indeksu $tin[u]$.
2. **Range sum:** suma od $tin[u]$ do $tout[u]$.

Rješenje: **Fenwickovo stablo (BIT)**.

---

# Implementacija: Subtree Queries

```cpp
// 1. DFS za tin/tout
void dfs(int u, int p) {
    tin[u] = ++timer;
    // ... rekurzija ...
    tout[u] = timer;
}

// Na početku: bit_update(tin[u], val[u]) za svaki čvor u

// 2. Update (BIT radi s razlikama, pa pamtimo trenutnu vrijednost)
void update_node(int u, int new_val) {
    int diff = new_val - current_val[u];
    current_val[u] = new_val;
    bit_update(tin[u], diff); // Ažuriramo BIT na poziciji tin[u]
}

// 3. Query
long long query_subtree(int u) {
    return bit_query(tout[u]) - bit_query(tin[u] - 1);
}
```

---

<!-- _class: title -->
# Path Queries (CSES)

## Napredna linearizacija

---

# Analiza: Path Queries

**Problem:**

1. **Update:** vrijednost čvora $u$ postaje $x$.
2. **Query:** suma vrijednosti na putu od **korijena** do čvora $u$.

**Intuicija**
Ovo je obrnuto od Subtree Queries.
Kad promijenimo vrijednost čvora $u$, to utječe na sumu puta za $u$ i **sve njegove potomke**.
Dakle, update čvora $u$ zapravo je **range update** na rasponu podstabla $[tin[u], tout[u]]$.
Upit za čvor $u$ je **point query** na indeksu $tin[u]$.

Koristimo BIT za **range update, point query**.

---

# Implementacija: Path Queries

BIT inače podržava point update i range sum.
Za range update i point query koristimo trik s diferencijalnim nizom:

- Dodajemo $val$ na $[L, R]$ $\rightarrow$ `update(L, val)`, `update(R+1, -val)`.
- Vrijednost na $i$ je prefiksna suma do $i$ $\rightarrow$ `query(i)`.

```cpp
// BIT veličine n + 2, jer tout[u] + 1 može biti n + 1

// Update čvora u (dodajemo razliku na cijelo podstablo)
void update_val(int u, int diff) {
    bit_update(tin[u], diff);
    bit_update(tout[u] + 1, -diff);
}

// Query puta do u
long long query_path(int u) {
    return bit_query(tin[u]);
}
```

**Zaključak:** linearizacija stabla moćan je alat koji teške probleme na stablima pretvara u klasične probleme na nizovima.

---

<!-- _class: title -->
# Zaključak i najbitnije napomene

---

# Što smo danas naučili?

1. **Stabla su specifična:**
   - Jedinstveni putovi, $N-1$ bridova, nema ciklusa.
   - Ti uvjeti omogućuju brze algoritme ($O(N)$ ili $O(\log N)$).

2. **Moćni alati:**
   - **Linearizacija (flattening):** pretvara podstabla u raspone na nizu. Ključna je za upite nad podstablima.
   - **Binary lifting (LCA):** omogućuje "skakanje" po stablu i brzo računanje udaljenosti.
   - **Promjer stabla:** dva DFS-a su standardni trik.

---

# Osvrt na tehnike rješavanja

- **Transformacija problema:**
  - Ako zadatak traži sumu/min/max u **podstablu** $\rightarrow$ linearizacija + BIT/segmentno stablo.
  - Ako zadatak traži nešto na **putu** $\rightarrow$ LCA + prefiksne sume (ili HLD za teže slučajeve).

- **Binary lifting je univerzalan:**
  - Ne služi samo za LCA. Koristi se kad god trebate simulirati "kamo ću stići nakon $K$ koraka" u grafu u kojem svaki čvor ima točno jedan izlazni brid.