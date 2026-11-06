---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Potpuna pretraga i backtracking"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!-- _paginate: false -->
<!-- _class: title  -->
# Potpuna pretraga i backtracking

Programiranje za rješavanje složenih problema

---

# Sadržaj

1. **Uvod i motivacija**
   - Što je potpuna pretraga?
   - Kada je koristiti?
2. **Generiranje podskupova**
   - Rekurzija
   - Bitmaske
3. **Generiranje permutacija**
   - `std::next_permutation`
4. **Backtracking**
   - Koncept i *pruning*
   - Primjer: N-kraljica
5. **Zadaci za vježbu**

---

<!-- _class: lead -->

# Uvod i motivacija

## Brute force pristup

---

# Što je potpuna pretraga?

**Potpuna pretraga** (engl. *complete search* ili *brute force*) je tehnika rješavanja problema koja se svodi na generiranje **svih mogućih rješenja** i provjeru svakog od njih.

- Često se smatra "naivnom", ali je temelj mnogih algoritama.
- Garantira pronalazak točnog rješenja (ako ga nađemo u vremenskom limitu).

**Kada je primjenjiva?**

- Kada je prostor rješenja malen.
- Ako je $N$ dovoljno mali da složenost poput $O(2^N)$ ili $O(N!)$ prolazi unutar 1-2 sekunde.
- Uvijek prvo razmotrite potpunu pretragu! Ako je dovoljno brza, nema potrebe za kompliciranjem.

---

# Backtracking: Pametna potpuna pretraga

**Backtracking** je rekurzivna tehnika gradnje rješenja korak po korak.

**Ključna ideja:**

- Pokušavamo proširiti trenutno parcijalno rješenje.
- Ako shvatimo da trenutni put ne vodi do rješenja, **odustajemo** (engl. *pruning*) i vraćamo se korak unatrag (**backtrack**).

**Prednost:**

- *Pruning* drastično smanjuje broj stanja koja moramo obići u usporedbi s čistim *brute forceom*.

---

<!-- _class: lead -->
# Generiranje podskupova

## Zbroj podskupa (Subset Sum) za male N

---

# Problem: Generiranje svih podskupova

**Zadatak:**
Zadan je skup od $n$ predmeta s težinama. Treba pronaći podskup čija je suma težina što bliža kapacitetu $W$, ali ne veća od njega.
(Ovo je pojednostavljeni problem ruksaka, bez vrijednosti predmeta.)

**Pristup:**
Svaki element možemo ili **uključiti** u podskup ili **ne uključiti**.
Ukupno ima $2^n$ mogućih podskupova.

---

# Rješenje 1: Rekurzija

Funkcija `search(k, current_weight)` odlučuje za $k$-ti element.

```cpp
long long best = 0;

void search(int k, long long current_weight) {
    if (k == n) { // Svi elementi su razmotreni
        best = max(best, current_weight);
        return;
    }

    // Opcija 1: ne uključujemo element k
    search(k + 1, current_weight);

    // Opcija 2: uključujemo element k (ako stane)
    if (current_weight + weights[k] <= W) {
        search(k + 1, current_weight + weights[k]);
    }
}
```

**Složenost:** $O(2^n)$.

---

# Stablo rekurzije korak po korak

Lijevo dijete znači „ne uzimamo predmet”, desno (zeleni brid) „uzimamo”. Crveni čvor je grana koju odrežemo jer premašuje `W`.

<style scoped>
.bt-subsets { margin-top: 0.3em; }
.bt-subsets .chips { font-size: 20px; margin-bottom: 0.4em; }
.bt-subsets .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.bt-subsets .chip.take { background: #9fdc9f; }
.bt-subsets .chip.skip, .bt-subsets .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.bt-subsets .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.bt-subsets .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.bt-subsets .row { display: flex; gap: 6px; }
.bt-subsets .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.bt-subsets .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.bt-subsets .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.bt-subsets .cell.todo .val { color: #b5b5b5; }
.bt-subsets .cell.rng { background: #d6e6f5; }
.bt-subsets .cell.best { background: #9fdc9f; }
.bt-subsets .cell.src { background: #f5db7e; }
.bt-subsets .cell.cur { background: var(--main); color: #fff; }
.bt-subsets .cell.cur .idx, .bt-subsets .cell.cur .val { color: #fff; }
.bt-subsets .rows .row { margin-bottom: 6px; }
.bt-subsets .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.bt-subsets .prow { margin-top: -4px; }
.bt-subsets .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.bt-subsets .cell.dim { opacity: .3; }
.bt-subsets .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.bt-subsets .wrap { display: flex; gap: 28px; align-items: flex-start; }
.bt-subsets .side { padding-top: 6px; }
.bt-subsets .gsvg { display: block; overflow: visible; }
.bt-subsets .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.bt-subsets .e polygon { fill: #9a9a9a; }
.bt-subsets .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.bt-subsets .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.bt-subsets .e.tree polygon { fill: #2f9e44; }
.bt-subsets .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.bt-subsets .e.off polygon { fill: #d5d5d5; }
.bt-subsets .e.off .w { fill: #b5b5b5; }
.bt-subsets .e.hid { opacity: 0; }
.bt-subsets .e.bad line { stroke: #e03131; stroke-width: 6; }
.bt-subsets .e.bad polygon { fill: #e03131; }
.bt-subsets .e.on line { stroke: var(--main); stroke-width: 6; }
.bt-subsets .e.on polygon { fill: var(--main); }
.bt-subsets .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.bt-subsets .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.bt-subsets .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.bt-subsets .n.c1 circle { fill: #ffd8a8; } .bt-subsets .n.c2 circle { fill: #a5d8ff; } .bt-subsets .n.c3 circle { fill: #b2f2bb; }
.bt-subsets .n.c4 circle { fill: #fcc2d7; } .bt-subsets .n.c5 circle { fill: #d0bfff; } .bt-subsets .n.c6 circle { fill: #ffec99; }
.bt-subsets .n.done circle { fill: #9fdc9f; }
.bt-subsets .n.src circle { fill: #f5db7e; }
.bt-subsets .n.cur circle { fill: var(--main); stroke: var(--main); }
.bt-subsets .n.cur .id { fill: #fff; }
.bt-subsets .tbl { display: grid; gap: 5px; }
.bt-subsets .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.bt-subsets .th.hl { background: var(--main); color: #fff; }
.bt-subsets .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.bt-subsets .tc.none { border-color: transparent; }
.bt-subsets .tc.k { background: #e3ecf6; }
.bt-subsets .tc.best { background: #9fdc9f; }
.bt-subsets .tc.src { background: #f5db7e; }
.bt-subsets .tc.cur { background: var(--main); color: #fff; }
.bt-subsets .line1, .bt-subsets .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.bt-subsets .line1 { margin-top: 0.5em; }
.bt-subsets .line2 { font-weight: bold; }
.bt-subsets .ctrl { margin-top: 0.5em; }
.bt-subsets button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.bt-subsets button:hover { background: var(--main); color: #fff; }
.bt-subsets .hint { font-size: 16px; color: #6e6e6e; }
.bt-subsets .lvl { font-size: 15px; font-weight: bold; fill: #6e6e6e; dominant-baseline: central; }
.bt-subsets .te { stroke: #9a9a9a; stroke-width: 2.5; transition: opacity .25s; }
.bt-subsets .te.yes { stroke: #2f9e44; }
.bt-subsets .n .id { font-size: 17px; }
.bt-subsets .n.hidn { opacity: 0; }
.bt-subsets .n.out circle { fill: #ffc9c9; stroke: #e03131; }
.bt-subsets .n.best circle { fill: #2f9e44; stroke: #2f9e44; }
.bt-subsets .n.best .id { fill: #fff; }
</style>

<div class="bt-subsets" data-w="2,3,5,6" data-cap="10">
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
  document.querySelectorAll('.bt-subsets').forEach(function (root) {
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
    // Redak s oznakom: [oznaka] [ćelija] [ćelija] ...
    function lrow(box, label, count, base, idx) {
      var r = mk('div', 'row');
      r.appendChild(mk('div', 'rl', label));
      box.appendChild(r);
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        if (idx) cell.appendChild(mk('div', 'idx', k + (base || 0)));
        var v = mk('div', 'val');
        cell.appendChild(v);
        r.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals, row: r };
    }
    // Redak pokazivača ispod niza (l, mid, r, i, j ...)
    function prow(box, count) {
      var r = mk('div', 'row prow');
      r.appendChild(mk('div', 'rl', ''));
      box.appendChild(r);
      var cells = [];
      for (var k = 0; k !== count; k++) cells.push(r.appendChild(mk('div', 'pc')));
      return cells;
    }
    function setPtrs(cells, pairs) {
      var m = {};
      pairs.forEach(function (p) { if (p[1] !== -1) m[p[1]] = m[p[1]] ? m[p[1]] + ', ' + p[0] : p[0]; });
      cells.forEach(function (c, k) { c.textContent = m[k] || ''; });
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

    var w = root.dataset.w.split(',').map(Number), W = Number(root.dataset.cap), n = w.length;
    var TW = 960, LH = 62, X0 = 130, H = 50 + n * LH;
    var svg = sv('svg', { viewBox: '0 0 ' + TW + ' ' + H, width: TW, height: H, 'class': 'gsvg' }, root.querySelector('.graph'));
    function pos(d, i) { var c = Math.pow(2, d); return { x: X0 + (i + 0.5) * (TW - X0) / c, y: 26 + d * LH }; }
    for (var d0 = 0; d0 !== n + 1; d0++) {
      var t = sv('text', { x: 4, y: 26 + d0 * LH, 'class': 'lvl' }, svg);
      t.textContent = d0 === n ? 'k = n (list)' : 'k = ' + d0 + ': w = ' + w[d0];
    }
    var gE = sv('g', {}, svg), gN = sv('g', {}, svg), N = {}, E = {};
    for (var d = 0; d !== n + 1; d++) {
      for (var i = 0; i !== Math.pow(2, d); i++) {
        var p = pos(d, i), k = d + '-' + i;
        if (d !== 0) {
          var q = pos(d - 1, Math.floor(i / 2));
          E[k] = sv('line', { x1: q.x, y1: q.y + 18, x2: p.x, y2: p.y - 18, 'class': i % 2 ? 'te yes' : 'te' }, gE);
        }
        var g = sv('g', { 'class': 'n' }, gN);
        sv('circle', { cx: p.x, cy: p.y, r: 18 }, g);
        var tx = sv('text', { x: p.x, y: p.y, 'class': 'id' }, g);
        N[k] = { g: g, t: tx };
      }
    }
    var vis = {}, cls = {}, best = -1, bestKey = null, snaps = [], leaves = 0;
    function snap(cur, l1) {
      snaps.push({ vis: Object.assign({}, vis), cls: Object.assign({}, cls), cur: cur, bk: null, l1: l1,
        l2: 'best = ' + (best === -1 ? '—' : best) + ',  W = ' + W });
    }
    function search(d, i, cw) {
      var k = d + '-' + i;
      vis[k] = cw; cls[k] = 'done';
      if (d === n) {
        leaves++;
        var b = lt(best, cw);
        if (b) { best = cw; bestKey = k; }
        snap(k, 'k == n: svi predmeti razmotreni, težina ' + cw + (b ? '  → novi best' : ''));
        return;
      }
      snap(k, 'search(' + d + ', ' + cw + '): lijevo ne uzimamo predmet ' + d + ', desno ga uzimamo (+' + w[d] + ')');
      search(d + 1, 2 * i, cw);
      if (le(cw + w[d], W)) search(d + 1, 2 * i + 1, cw + w[d]);
      else {
        var pk = (d + 1) + '-' + (2 * i + 1);
        vis[pk] = cw + w[d]; cls[pk] = 'out';
        snap(pk, cw + ' + ' + w[d] + ' = ' + (cw + w[d]) + ' veće je od W  → tu granu ne otvaramo (pruning)');
      }
    }
    snap(null, 'Svaki čvor je poziv search(k, težina); broj u čvoru je trenutna težina');
    snaps[0].vis = {}; snaps[0].cls = {};
    search(0, 0, 0);
    var fin = { vis: Object.assign({}, vis), cls: Object.assign({}, cls), cur: null, bk: bestKey,
      l1: 'Obišli smo ' + leaves + ' od ' + Math.pow(2, n) + ' listova; crvene grane su odrezane',
      l2: 'Najbolja težina ≤ ' + W + ' je ' + best + '   ✓' };
    snaps.push(fin);
    function draw(s) {
      Object.keys(N).forEach(function (k) {
        var on = s.vis[k] !== undefined;
        var c = on ? 'n ' + s.cls[k] : 'n hidn';
        if (k === s.bk) c += ' best';
        if (k === s.cur) c += ' cur';
        setc(N[k].g, c);
        N[k].t.textContent = on ? s.vis[k] : '';
        if (E[k]) E[k].style.opacity = on ? 1 : 0;
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

# Rješenje 2: Bitmaske

Svaki podskup možemo predstaviti kao $n$-bitni broj.
Ako je $i$-ti bit **1**, element je u podskupu. Ako je **0**, nije.

```cpp
for (int mask = 0; mask < (1 << n); ++mask) {
    long long current_sum = 0;
    for (int i = 0; i < n; ++i) {
        if ((mask >> i) & 1) { // Provjera je li i-ti bit postavljen
            current_sum += weights[i];
        }
    }

    if (current_sum <= W) {
        best_sum = max(best_sum, current_sum);
    }
}
```

**Složenost:** $O(n \cdot 2^n)$.

---

# Bitmaske korak po korak

Svaki stupac je jedan `mask`. Plava polja su postavljeni bitovi (predmeti u podskupu), crvena suma premašuje `W`.

<style scoped>
.bt-mask { margin-top: 0.3em; }
.bt-mask .chips { font-size: 20px; margin-bottom: 0.4em; }
.bt-mask .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.bt-mask .chip.take { background: #9fdc9f; }
.bt-mask .chip.skip, .bt-mask .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.bt-mask .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.bt-mask .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.bt-mask .row { display: flex; gap: 6px; }
.bt-mask .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.bt-mask .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.bt-mask .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.bt-mask .cell.todo .val { color: #b5b5b5; }
.bt-mask .cell.rng { background: #d6e6f5; }
.bt-mask .cell.best { background: #9fdc9f; }
.bt-mask .cell.src { background: #f5db7e; }
.bt-mask .cell.cur { background: var(--main); color: #fff; }
.bt-mask .cell.cur .idx, .bt-mask .cell.cur .val { color: #fff; }
.bt-mask .rows .row { margin-bottom: 6px; }
.bt-mask .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.bt-mask .prow { margin-top: -4px; }
.bt-mask .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.bt-mask .cell.dim { opacity: .3; }
.bt-mask .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.bt-mask .wrap { display: flex; gap: 28px; align-items: flex-start; }
.bt-mask .side { padding-top: 6px; }
.bt-mask .gsvg { display: block; overflow: visible; }
.bt-mask .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.bt-mask .e polygon { fill: #9a9a9a; }
.bt-mask .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.bt-mask .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.bt-mask .e.tree polygon { fill: #2f9e44; }
.bt-mask .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.bt-mask .e.off polygon { fill: #d5d5d5; }
.bt-mask .e.off .w { fill: #b5b5b5; }
.bt-mask .e.hid { opacity: 0; }
.bt-mask .e.bad line { stroke: #e03131; stroke-width: 6; }
.bt-mask .e.bad polygon { fill: #e03131; }
.bt-mask .e.on line { stroke: var(--main); stroke-width: 6; }
.bt-mask .e.on polygon { fill: var(--main); }
.bt-mask .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.bt-mask .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.bt-mask .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.bt-mask .n.c1 circle { fill: #ffd8a8; } .bt-mask .n.c2 circle { fill: #a5d8ff; } .bt-mask .n.c3 circle { fill: #b2f2bb; }
.bt-mask .n.c4 circle { fill: #fcc2d7; } .bt-mask .n.c5 circle { fill: #d0bfff; } .bt-mask .n.c6 circle { fill: #ffec99; }
.bt-mask .n.done circle { fill: #9fdc9f; }
.bt-mask .n.src circle { fill: #f5db7e; }
.bt-mask .n.cur circle { fill: var(--main); stroke: var(--main); }
.bt-mask .n.cur .id { fill: #fff; }
.bt-mask .tbl { display: grid; gap: 5px; }
.bt-mask .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.bt-mask .th.hl { background: var(--main); color: #fff; }
.bt-mask .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.bt-mask .tc.none { border-color: transparent; }
.bt-mask .tc.k { background: #e3ecf6; }
.bt-mask .tc.best { background: #9fdc9f; }
.bt-mask .tc.src { background: #f5db7e; }
.bt-mask .tc.cur { background: var(--main); color: #fff; }
.bt-mask .line1, .bt-mask .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.bt-mask .line1 { margin-top: 0.5em; }
.bt-mask .line2 { font-weight: bold; }
.bt-mask .ctrl { margin-top: 0.5em; }
.bt-mask button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.bt-mask button:hover { background: var(--main); color: #fff; }
.bt-mask .hint { font-size: 16px; color: #6e6e6e; }
.bt-mask .tc { font-size: 18px; }
.bt-mask .tc.bad { background: #ffc9c9; }
.bt-mask .th { font-size: 16px; }
</style>

<div class="bt-mask" data-w="2,3,5,6" data-cap="10">
  <div class="tbl"></div>
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
  document.querySelectorAll('.bt-mask').forEach(function (root) {
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
    // Redak s oznakom: [oznaka] [ćelija] [ćelija] ...
    function lrow(box, label, count, base, idx) {
      var r = mk('div', 'row');
      r.appendChild(mk('div', 'rl', label));
      box.appendChild(r);
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        if (idx) cell.appendChild(mk('div', 'idx', k + (base || 0)));
        var v = mk('div', 'val');
        cell.appendChild(v);
        r.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals, row: r };
    }
    // Redak pokazivača ispod niza (l, mid, r, i, j ...)
    function prow(box, count) {
      var r = mk('div', 'row prow');
      r.appendChild(mk('div', 'rl', ''));
      box.appendChild(r);
      var cells = [];
      for (var k = 0; k !== count; k++) cells.push(r.appendChild(mk('div', 'pc')));
      return cells;
    }
    function setPtrs(cells, pairs) {
      var m = {};
      pairs.forEach(function (p) { if (p[1] !== -1) m[p[1]] = m[p[1]] ? m[p[1]] + ', ' + p[0] : p[0]; });
      cells.forEach(function (c, k) { c.textContent = m[k] || ''; });
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

    var w = root.dataset.w.split(',').map(Number), W = Number(root.dataset.cap), n = w.length, M = Math.pow(2, n);
    var tbl = root.querySelector('.tbl');
    tbl.style.gridTemplateColumns = '130px repeat(' + M + ', 46px)';
    tbl.appendChild(mk('div', 'th', 'mask'));
    var H = [];
    for (var m0 = 0; m0 !== M; m0++) H.push(tbl.appendChild(mk('div', 'th', m0)));
    var BR = [];
    for (var i = 0; i !== n; i++) {
      tbl.appendChild(mk('div', 'th', 'bit ' + i + ' (' + w[i] + ')'));
      var r = [];
      for (var m1 = 0; m1 !== M; m1++) r.push(tbl.appendChild(mk('div', 'tc')));
      BR.push(r);
    }
    tbl.appendChild(mk('div', 'th', 'suma'));
    var SR = [];
    for (var m2 = 0; m2 !== M; m2++) SR.push(tbl.appendChild(mk('div', 'tc')));
    function bit(m, i) { return Math.floor(m / Math.pow(2, i)) % 2; }
    var sums = [], best = -1, bm = -1, snaps = [{ upto: -1, bm: -1, fin: false, l1: 'Podskup = n-bitni broj: i-ti bit 1 znači da je i-ti predmet u podskupu', l2: 'mask ide od 0 do 2^' + n + ' − 1 = ' + (M - 1) }];
    for (var m = 0; m !== M; m++) {
      var s = 0, parts = [], bin = '';
      for (var j = 0; j !== n; j++) if (bit(m, j)) { s += w[j]; parts.push(w[j]); }
      for (var j2 = n - 1; j2 !== -1; j2--) bin += bit(m, j2);
      sums.push(s);
      var ok = le(s, W), b = ok ? lt(best, s) : false;
      if (b) { best = s; bm = m; }
      snaps.push({ upto: m, bm: bm, fin: false,
        l1: 'mask = ' + m + ' = ' + bin + '₂:  suma = ' + (parts.length ? parts.join(' + ') : '0') + ' = ' + s + (ok ? ' ≤ ' + W : ' veće od ' + W + ', ne vrijedi'),
        l2: 'best_sum = ' + (best === -1 ? '—' : best) + (b ? '   (novi best)' : '') });
    }
    snaps.push({ upto: M - 1, bm: bm, fin: true, l1: 'Prošli smo svih 2^' + n + ' = ' + M + ' podskupova, svaki u O(n): ukupno O(n · 2^n)', l2: 'best_sum = ' + best + ' (mask ' + bm + ')   ✓' });
    function draw(st) {
      for (var m = 0; m !== M; m++) {
        var shown = le(m, st.upto);
        setc(H[m], m === st.upto ? (st.fin ? 'th' : 'th hl') : 'th');
        for (var i = 0; i !== n; i++) {
          var on = shown ? bit(m, i) === 1 : false;
          setc(BR[i][m], 'tc' + (on ? ' k' : '') + (shown ? '' : ' none'));
          BR[i][m].textContent = shown ? (on ? w[i] : '0') : '';
        }
        var c = 'tc';
        if (!shown) c += ' none';
        else if (lt(W, sums[m])) c += ' bad';
        if (shown ? m === st.bm : false) c += ' best';
        if (m === st.upto ? !st.fin : false) c += ' cur';
        setc(SR[m], c);
        SR[m].textContent = shown ? sums[m] : '';
      }
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

<!-- _class: lead -->
# Generiranje permutacija

## Problem trgovačkog putnika (TSP) za male N

---

# Problem: Generiranje svih permutacija

**Zadatak:**
Zadan je skup od $n$ gradova. Treba pronaći najkraći put koji posjećuje svaki grad točno jednom.

**Rješenje:**
Isprobati sve moguće redoslijede (permutacije) gradova.
Broj permutacija je $n!$ (faktorijela).
Za $n=10$, $10! \approx 3,6 \cdot 10^6$ (brzo).
Za $n=20$, $20! \approx 2,4 \cdot 10^{18}$ (presporo).

---

# Rješenje: `std::next_permutation`

C++ STL ima ugrađenu funkciju za generiranje leksikografski sljedeće permutacije.

```cpp
vector<int> p(n);
for (int i = 0; i < n; ++i) p[i] = i; // Početna permutacija: 0, 1, 2...

long long min_path = -1;

do {
    // Duljina puta za trenutnu permutaciju p
    long long current_path = calculate_path(p);

    if (min_path == -1 || current_path < min_path) {
        min_path = current_path;
    }
} while (next_permutation(p.begin(), p.end()));
```

**Složenost:** $O(n \cdot n!)$.

---

<!-- _class: lead -->

# Problem N-kraljica

## Klasičan primjer backtrackinga

---

# Problem: N-kraljica

**Zadatak:**
Na šahovsku ploču $n \times n$ treba postaviti $n$ kraljica tako da se nikoje dvije ne napadaju.
(Kraljica napada horizontalno, vertikalno i dijagonalno.)

**Pristup:**
Postavljamo kraljice red po red. U svakom redu pokušamo staviti kraljicu u neki stupac.

**Pruning (Rezanje):**
Ako je polje već napadnuto, kraljicu tamo ni ne stavljamo, nego odmah probamo sljedeći stupac (ne idemo u dubinu).

---

# Implementacija: N-kraljica

```cpp
void search(int y) {
    if (y == n) { ans++; return; } // Našli smo rješenje

    for (int x = 0; x < n; ++x) {
        // Ako je polje (y, x) napadnuto, preskačemo ga (PRUNING)
        if (column[x] || diag1[x+y] || diag2[x-y+n-1]) continue;

        // Postavljamo kraljicu
        column[x] = diag1[x+y] = diag2[x-y+n-1] = true;

        search(y + 1); // Rekurzivni poziv za sljedeći red

        // BACKTRACK: mičemo kraljicu da probamo sljedeću opciju
        column[x] = diag1[x+y] = diag2[x-y+n-1] = false;
    }
}
```

Pomoćna polja `column`, `diag1`, `diag2` daju $O(1)$ provjeru napada.
Brojač zovemo `ans`, jer se globalni `count` sudara sa `std::count`.

---

# N-kraljica korak po korak

Crvenkasta polja napadaju već postavljene kraljice. Desno su pomoćna polja koja daju provjeru napada u O(1).

<style scoped>
.bt-queens { margin-top: 0.3em; }
.bt-queens .chips { font-size: 20px; margin-bottom: 0.4em; }
.bt-queens .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.bt-queens .chip.take { background: #9fdc9f; }
.bt-queens .chip.skip, .bt-queens .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.bt-queens .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.bt-queens .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.bt-queens .row { display: flex; gap: 6px; }
.bt-queens .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.bt-queens .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.bt-queens .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.bt-queens .cell.todo .val { color: #b5b5b5; }
.bt-queens .cell.rng { background: #d6e6f5; }
.bt-queens .cell.best { background: #9fdc9f; }
.bt-queens .cell.src { background: #f5db7e; }
.bt-queens .cell.cur { background: var(--main); color: #fff; }
.bt-queens .cell.cur .idx, .bt-queens .cell.cur .val { color: #fff; }
.bt-queens .rows .row { margin-bottom: 6px; }
.bt-queens .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.bt-queens .prow { margin-top: -4px; }
.bt-queens .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.bt-queens .cell.dim { opacity: .3; }
.bt-queens .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.bt-queens .wrap { display: flex; gap: 28px; align-items: flex-start; }
.bt-queens .side { padding-top: 6px; }
.bt-queens .gsvg { display: block; overflow: visible; }
.bt-queens .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.bt-queens .e polygon { fill: #9a9a9a; }
.bt-queens .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.bt-queens .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.bt-queens .e.tree polygon { fill: #2f9e44; }
.bt-queens .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.bt-queens .e.off polygon { fill: #d5d5d5; }
.bt-queens .e.off .w { fill: #b5b5b5; }
.bt-queens .e.hid { opacity: 0; }
.bt-queens .e.bad line { stroke: #e03131; stroke-width: 6; }
.bt-queens .e.bad polygon { fill: #e03131; }
.bt-queens .e.on line { stroke: var(--main); stroke-width: 6; }
.bt-queens .e.on polygon { fill: var(--main); }
.bt-queens .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.bt-queens .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.bt-queens .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.bt-queens .n.c1 circle { fill: #ffd8a8; } .bt-queens .n.c2 circle { fill: #a5d8ff; } .bt-queens .n.c3 circle { fill: #b2f2bb; }
.bt-queens .n.c4 circle { fill: #fcc2d7; } .bt-queens .n.c5 circle { fill: #d0bfff; } .bt-queens .n.c6 circle { fill: #ffec99; }
.bt-queens .n.done circle { fill: #9fdc9f; }
.bt-queens .n.src circle { fill: #f5db7e; }
.bt-queens .n.cur circle { fill: var(--main); stroke: var(--main); }
.bt-queens .n.cur .id { fill: #fff; }
.bt-queens .tbl { display: grid; gap: 5px; }
.bt-queens .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.bt-queens .th.hl { background: var(--main); color: #fff; }
.bt-queens .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.bt-queens .tc.none { border-color: transparent; }
.bt-queens .tc.k { background: #e3ecf6; }
.bt-queens .tc.best { background: #9fdc9f; }
.bt-queens .tc.src { background: #f5db7e; }
.bt-queens .tc.cur { background: var(--main); color: #fff; }
.bt-queens .line1, .bt-queens .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.bt-queens .line1 { margin-top: 0.5em; }
.bt-queens .line2 { font-weight: bold; }
.bt-queens .ctrl { margin-top: 0.5em; }
.bt-queens button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.bt-queens button:hover { background: var(--main); color: #fff; }
.bt-queens .hint { font-size: 16px; color: #6e6e6e; }
.bt-queens .board { display: grid; gap: 0; border: 2px solid #141414; }
.bt-queens .sq { width: 64px; height: 64px; line-height: 64px; text-align: center; font-size: 44px; background: #fff; transition: background-color .2s; }
.bt-queens .sq.dark { background: #ececec; }
.bt-queens .sq.att { background: #ffd6d6; }
.bt-queens .sq.dark.att { background: #f5c2c2; }
.bt-queens .sq.cur { background: var(--main); color: #fff; }
.bt-queens .sq.bad { background: #e03131; color: #fff; }
.bt-queens .cell { width: 40px; }
.bt-queens .val { font-size: 18px; height: 28px; line-height: 28px; }
.bt-queens .idx { font-size: 12px; }
.bt-queens .rl { width: 160px; font-size: 16px; }
.bt-queens .sols { margin-top: 0.4em; }
</style>

<div class="bt-queens" data-n="4">
  <div class="wrap">
    <div class="board"></div>
    <div class="side">
      <div class="rows"></div>
      <div class="sols chips"></div>
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
  document.querySelectorAll('.bt-queens').forEach(function (root) {
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
    // Redak s oznakom: [oznaka] [ćelija] [ćelija] ...
    function lrow(box, label, count, base, idx) {
      var r = mk('div', 'row');
      r.appendChild(mk('div', 'rl', label));
      box.appendChild(r);
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        if (idx) cell.appendChild(mk('div', 'idx', k + (base || 0)));
        var v = mk('div', 'val');
        cell.appendChild(v);
        r.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals, row: r };
    }
    // Redak pokazivača ispod niza (l, mid, r, i, j ...)
    function prow(box, count) {
      var r = mk('div', 'row prow');
      r.appendChild(mk('div', 'rl', ''));
      box.appendChild(r);
      var cells = [];
      for (var k = 0; k !== count; k++) cells.push(r.appendChild(mk('div', 'pc')));
      return cells;
    }
    function setPtrs(cells, pairs) {
      var m = {};
      pairs.forEach(function (p) { if (p[1] !== -1) m[p[1]] = m[p[1]] ? m[p[1]] + ', ' + p[0] : p[0]; });
      cells.forEach(function (c, k) { c.textContent = m[k] || ''; });
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

    var n = Number(root.dataset.n);
    var board = root.querySelector('.board');
    board.style.gridTemplateColumns = 'repeat(' + n + ', 64px)';
    var C = [];
    for (var y0 = 0; y0 !== n; y0++) { var r0 = []; for (var x0 = 0; x0 !== n; x0++) r0.push(board.appendChild(mk('div', 'sq'))); C.push(r0); }
    var box = root.querySelector('.rows');
    var RC = lrow(box, 'column[x]', n, 0, true);
    var R1 = lrow(box, 'diag1[x+y]', 2 * n - 1, 0, true);
    var R2 = lrow(box, 'diag2[x−y+n−1]', 2 * n - 1, 0, true);
    var sol = root.querySelector('.sols');
    var col = [], d1 = [], d2 = [], q = [], ans = 0, sols = [], snaps = [];
    for (var k = 0; k !== 2 * n; k++) { col.push(false); d1.push(false); d2.push(false); }
    function snap(o) {
      var s = { q: q.slice(), col: col.slice(), d1: d1.slice(), d2: d2.slice(), sols: sols.slice(), at: null, bad: false, l1: '', l2: '' };
      Object.keys(o).forEach(function (k) { s[k] = o[k]; });
      snaps.push(s);
    }
    snap({ l1: 'Postavljamo kraljice red po red (y), u svakom redu probamo stupce x redom', l2: 'Rješenja: 0' });
    function search(y) {
      if (y === n) {
        ans++; sols.push(q.slice());
        snap({ l1: 'y == n: svih ' + n + ' kraljica je postavljeno', l2: 'Rješenje #' + ans + ' pronađeno! ans = ' + ans });
        return;
      }
      for (var x = 0; x !== n; x++) {
        var why = [];
        if (col[x]) why.push('stupac');
        if (d1[x + y]) why.push('dijagonala ↗');
        if (d2[x - y + n - 1]) why.push('dijagonala ↘');
        if (why.length) {
          snap({ at: [y, x], bad: true, l1: '(' + y + ', ' + x + ') je napadnuto: ' + why.join(', ') + '  → preskačemo (pruning)', l2: 'Rješenja: ' + ans });
          continue;
        }
        col[x] = d1[x + y] = d2[x - y + n - 1] = true; q.push(x);
        snap({ at: [y, x], l1: 'Postavljamo kraljicu na (' + y + ', ' + x + ')  → search(' + (y + 1) + ')', l2: 'Rješenja: ' + ans });
        search(y + 1);
        col[x] = d1[x + y] = d2[x - y + n - 1] = false; q.pop();
        snap({ at: [y, x], back: true, l1: 'Backtrack: mičemo kraljicu s (' + y + ', ' + x + ') i probamo sljedeći stupac', l2: 'Rješenja: ' + ans });
      }
    }
    search(0);
    snap({ l1: 'Isprobali smo sve stupce u redu 0, pretraga je gotova.', l2: 'Ukupno rješenja za n = ' + n + ': ' + ans + '   ✓' });
    function draw(s) {
      for (var y = 0; y !== n; y++) {
        for (var x = 0; x !== n; x++) {
          var hasQ = s.q[y] === x;
          var att = false;
          s.q.forEach(function (qx, qy) { if (qy !== y ? (qx === x ? true : (qx + qy === x + y ? true : qx - qy === x - y)) : false) att = true; });
          var c = 'sq' + ((x + y) % 2 ? ' dark' : '');
          if (att ? !hasQ : false) c += ' att';
          if (s.at ? (s.at[0] === y ? s.at[1] === x : false) : false) c += s.bad ? ' bad' : ' cur';
          setc(C[y][x], c);
          C[y][x].textContent = hasQ ? '♛' : '';
        }
      }
      var ty = s.at ? s.at[0] : -1, tx = s.at ? s.at[1] : -1;
      function paint(R, arr, hi) {
        R.cells.forEach(function (c, k) { setc(c, 'cell' + (arr[k] ? ' rng' : '') + (k === hi ? ' src' : '')); R.vals[k].textContent = arr[k] ? 1 : 0; });
      }
      paint(RC, s.col, tx);
      paint(R1, s.d1, s.at ? tx + ty : -1);
      paint(R2, s.d2, s.at ? tx - ty + n - 1 : -1);
      sol.textContent = 'Rješenja (stupac po redu):';
      if (s.sols.length === 0) sol.appendChild(mk('span', 'muted', 'još nijedno'));
      s.sols.forEach(function (p) { sol.appendChild(mk('span', 'chip take', '[' + p.join(', ') + ']')); });
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

<!-- _class: lead -->

# Zadaci za vježbu

## CSES i Codeforces

---

# CSES Problem Set

1. **[Apple Division](https://cses.fi/problemset/task/1623)**
   - Podjela jabuka u dvije grupe s minimalnom razlikom težina.
   - *Rješenje:* Generiranje podskupova (rekurzija ili bitmaske).
2. **[Creating Strings](https://cses.fi/problemset/task/1622)**
   - Ispis svih različitih permutacija stringa.
   - *Rješenje:* `next_permutation` na prethodno sortiranom stringu.
3. **[Chessboard and Queens](https://cses.fi/problemset/task/1624)**
   - Problem 8 kraljica, ali su neka polja na ploči blokirana.
4. **[Grid Paths](https://cses.fi/problemset/task/1625)**
   - Napredniji backtracking s jakim optimizacijama.

---

<!-- _class: title -->
# Apple Division (CSES)

## Generiranje podskupova

---

# Analiza: Apple Division

**Problem:**
Imamo $n$ jabuka s težinama $p_1, p_2, \dots, p_n$. Treba ih podijeliti u dvije grupe tako da je razlika u ukupnim težinama grupa **minimalna**.
**Ograničenja:** $n \le 20$, $p_i \le 10^9$ (sume trebaju `long long`).

**Intuicija:**
Svaka jabuka može ići u **Grupu 1** ili **Grupu 2**.
To je binarni izbor za svaku od $n$ jabuka.
Ukupan broj načina je $2^n$. Za $n=20$, $2^{20} \approx 10^6$, što je vrlo brzo.

Možemo koristiti rekurziju koja prolazi kroz sve jabuke i održava trenutne sume obiju grupa.

---

# Implementacija: Apple Division

```cpp
long long n, p[20];

long long solve(int idx, long long sum1, long long sum2) {
    // Bazni slučaj: prošli smo sve jabuke
    if (idx == n) {
        return abs(sum1 - sum2);
    }

    // Opcija 1: Jabuka ide u prvu grupu
    long long diff1 = solve(idx + 1, sum1 + p[idx], sum2);

    // Opcija 2: Jabuka ide u drugu grupu
    long long diff2 = solve(idx + 1, sum1, sum2 + p[idx]);

    return min(diff1, diff2);
}
```

U `main` funkciji pozivamo `solve(0, 0, 0)`.

---

<!-- _class: title -->
# Creating Strings (CSES)

## Permutacije s ponavljanjem

---

# Analiza: Creating Strings

**Problem:**
Zadan je string (npr. `aabac`). Treba ispisati sve **različite** permutacije tog stringa po abecednom redu.
**Ograničenja:** Duljina stringa $\le 8$.

**Intuicija:**
Broj permutacija za duljinu 8 je $8! = 40320$, što je malo.
Glavni izazov su **duplikati** (npr. zamjena dva slova 'a' ne stvara novi string).

C++ funkcija `std::next_permutation` pametno generira samo leksikografski sljedeću **unikatnu** permutaciju.

---

# Implementacija: Creating Strings

```cpp
string s;
cin >> s;
sort(s.begin(), s.end()); // Obavezno sortirati za next_permutation

vector<string> permutations;
do {
    permutations.push_back(s);
} while (next_permutation(s.begin(), s.end()));

cout << permutations.size() << "\n";
for (const string& p : permutations) {
    cout << p << "\n";
}
```

**Napomena:** Ako koristimo rekurziju, morali bismo koristiti `std::set` ili pamtiti frekvencije slova da izbjegnemo duplikate.

---

# next_permutation korak po korak

Plavo je pivot `s[i]`, žuto `s[j]` s kojim ga mijenjamo, a sufiks iza `i` se nakon zamjene okreće.

<style scoped>
.bt-perm { margin-top: 0.3em; }
.bt-perm .chips { font-size: 20px; margin-bottom: 0.4em; }
.bt-perm .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.bt-perm .chip.take { background: #9fdc9f; }
.bt-perm .chip.skip, .bt-perm .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.bt-perm .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.bt-perm .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.bt-perm .row { display: flex; gap: 6px; }
.bt-perm .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.bt-perm .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.bt-perm .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.bt-perm .cell.todo .val { color: #b5b5b5; }
.bt-perm .cell.rng { background: #d6e6f5; }
.bt-perm .cell.best { background: #9fdc9f; }
.bt-perm .cell.src { background: #f5db7e; }
.bt-perm .cell.cur { background: var(--main); color: #fff; }
.bt-perm .cell.cur .idx, .bt-perm .cell.cur .val { color: #fff; }
.bt-perm .rows .row { margin-bottom: 6px; }
.bt-perm .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.bt-perm .prow { margin-top: -4px; }
.bt-perm .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.bt-perm .cell.dim { opacity: .3; }
.bt-perm .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.bt-perm .wrap { display: flex; gap: 28px; align-items: flex-start; }
.bt-perm .side { padding-top: 6px; }
.bt-perm .gsvg { display: block; overflow: visible; }
.bt-perm .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.bt-perm .e polygon { fill: #9a9a9a; }
.bt-perm .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.bt-perm .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.bt-perm .e.tree polygon { fill: #2f9e44; }
.bt-perm .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.bt-perm .e.off polygon { fill: #d5d5d5; }
.bt-perm .e.off .w { fill: #b5b5b5; }
.bt-perm .e.hid { opacity: 0; }
.bt-perm .e.bad line { stroke: #e03131; stroke-width: 6; }
.bt-perm .e.bad polygon { fill: #e03131; }
.bt-perm .e.on line { stroke: var(--main); stroke-width: 6; }
.bt-perm .e.on polygon { fill: var(--main); }
.bt-perm .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.bt-perm .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.bt-perm .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.bt-perm .n.c1 circle { fill: #ffd8a8; } .bt-perm .n.c2 circle { fill: #a5d8ff; } .bt-perm .n.c3 circle { fill: #b2f2bb; }
.bt-perm .n.c4 circle { fill: #fcc2d7; } .bt-perm .n.c5 circle { fill: #d0bfff; } .bt-perm .n.c6 circle { fill: #ffec99; }
.bt-perm .n.done circle { fill: #9fdc9f; }
.bt-perm .n.src circle { fill: #f5db7e; }
.bt-perm .n.cur circle { fill: var(--main); stroke: var(--main); }
.bt-perm .n.cur .id { fill: #fff; }
.bt-perm .tbl { display: grid; gap: 5px; }
.bt-perm .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.bt-perm .th.hl { background: var(--main); color: #fff; }
.bt-perm .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.bt-perm .tc.none { border-color: transparent; }
.bt-perm .tc.k { background: #e3ecf6; }
.bt-perm .tc.best { background: #9fdc9f; }
.bt-perm .tc.src { background: #f5db7e; }
.bt-perm .tc.cur { background: var(--main); color: #fff; }
.bt-perm .line1, .bt-perm .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.bt-perm .line1 { margin-top: 0.5em; }
.bt-perm .line2 { font-weight: bold; }
.bt-perm .ctrl { margin-top: 0.5em; }
.bt-perm button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.bt-perm button:hover { background: var(--main); color: #fff; }
.bt-perm .hint { font-size: 16px; color: #6e6e6e; }
.bt-perm .perms { margin-top: 0.5em; }
.bt-perm .rl { width: 40px; }
</style>

<div class="bt-perm" data-s="caab">
  <div class="rows"></div>
  <div class="perms chips"></div>
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
  document.querySelectorAll('.bt-perm').forEach(function (root) {
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
    // Redak s oznakom: [oznaka] [ćelija] [ćelija] ...
    function lrow(box, label, count, base, idx) {
      var r = mk('div', 'row');
      r.appendChild(mk('div', 'rl', label));
      box.appendChild(r);
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        if (idx) cell.appendChild(mk('div', 'idx', k + (base || 0)));
        var v = mk('div', 'val');
        cell.appendChild(v);
        r.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals, row: r };
    }
    // Redak pokazivača ispod niza (l, mid, r, i, j ...)
    function prow(box, count) {
      var r = mk('div', 'row prow');
      r.appendChild(mk('div', 'rl', ''));
      box.appendChild(r);
      var cells = [];
      for (var k = 0; k !== count; k++) cells.push(r.appendChild(mk('div', 'pc')));
      return cells;
    }
    function setPtrs(cells, pairs) {
      var m = {};
      pairs.forEach(function (p) { if (p[1] !== -1) m[p[1]] = m[p[1]] ? m[p[1]] + ', ' + p[0] : p[0]; });
      cells.forEach(function (c, k) { c.textContent = m[k] || ''; });
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

    var s = root.dataset.s.split('').sort();
    var n = s.length;
    var box = root.querySelector('.rows');
    var R = lrow(box, 's', n, 0, true);
    var P = prow(box, n);
    var chipBox = root.querySelector('.perms');
    var list = [s.join('')];
    function code(c) { return c.charCodeAt(0); }
    var snaps = [{ arr: s.slice(), i: -1, j: -1, suf: [], list: list.slice(), l1: 'Prvo sortiramo: "' + s.join('') + '" je leksikografski najmanja permutacija', l2: 'Permutacija #1' }];
    while (true) {
      var i = n - 2;
      while (i !== -1 ? !lt(code(s[i]), code(s[i + 1])) : false) i--;
      if (i === -1) {
        snaps.push({ arr: s.slice(), i: -1, j: -1, suf: [], list: list.slice(), l1: 'Ne postoji i sa s[i] manjim od s[i + 1]: niz je padajući, next_permutation vraća false',
          l2: 'Ukupno ' + list.length + ' različitih stringova (duplikati se nikad ne generiraju)   ✓' });
        break;
      }
      var j = n - 1;
      while (!lt(code(s[i]), code(s[j]))) j--;
      var suf = [];
      for (var t = i + 1; t !== n; t++) suf.push(t);
      snaps.push({ arr: s.slice(), i: i, j: j, suf: suf, list: list.slice(),
        l1: 'Zdesna prvi i za koji je s[i] manji od s[i + 1]: i = ' + i + ' (' + s[i] + ')',
        l2: 'Najdesniji s[j] veći od s[i]: j = ' + j + ' (' + s[j] + '). Zamijenimo ih i okrenemo sve iza i.' });
      var tmp = s[i]; s[i] = s[j]; s[j] = tmp;
      var tail = s.slice(i + 1).reverse();
      s = s.slice(0, i + 1).concat(tail);
      list.push(s.join(''));
      snaps.push({ arr: s.slice(), i: i, j: -1, suf: suf, done: true, list: list.slice(),
        l1: 'Nakon zamjene i okretanja: "' + s.join('') + '"', l2: 'Permutacija #' + list.length });
    }
    function draw(st) {
      R.cells.forEach(function (c, k) {
        var cl = 'cell';
        if (st.suf.indexOf(k) !== -1) cl += st.done ? ' best' : ' rng';
        if (k === st.j) cl += ' src';
        if (k === st.i) cl += ' cur';
        setc(c, cl);
        R.vals[k].textContent = st.arr[k];
      });
      setPtrs(P, [['i', st.i], ['j', st.j]]);
      chipBox.textContent = '';
      st.list.forEach(function (p, k) { chipBox.appendChild(mk('span', k === st.list.length - 1 ? 'chip on' : 'chip', p)); });
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

<!-- _class: title -->
# Chessboard and Queens (CSES)

## Backtracking s ograničenjima

---

# Analiza: Chessboard and Queens

**Problem:**
Na ploču $8 \times 8$ treba postaviti 8 kraljica tako da se ne napadaju. Neka polja su označena s `*` i na njih se kraljica **ne smije** staviti.
Treba prebrojati na koliko je načina to moguće.

**Intuicija:**
Ovo je standardni problem N-kraljica ($N=8$), uz jedan dodatni uvjet.
U rekurzivnoj funkciji, prije nego postavimo kraljicu na `(y, x)`, provjeravamo:

1. Je li stupac/dijagonala slobodna?
2. Je li polje `board[y][x]` slobodno (nije `*`)?

---

# Implementacija: Chessboard and Queens

```cpp
// board[8][8] sadrži ulaz ('.' ili '*')
void search(int y) {
    if (y == 8) { ans++; return; }

    for (int x = 0; x < 8; x++) {
        // Dodatna provjera: board[y][x] == '*'
        if (col[x] || d1[x+y] || d2[x-y+7] || board[y][x] == '*')
            continue;

        col[x] = d1[x+y] = d2[x-y+7] = true;
        search(y + 1);
        col[x] = d1[x+y] = d2[x-y+7] = false; // Backtrack
    }
}
```

Složenost je manja od klasičnih 8 kraljica zbog dodatnih ograničenja (manje grana stabla).

---

<!-- _class: title -->

# Grid Paths (CSES)

## Optimizacija backtrackinga

---

# Analiza: Grid Paths

**Problem:**
U mreži $7 \times 7$ treba prebrojati putove od **gornjeg lijevog** do **donjeg lijevog** kuta koji posjećuju svako polje točno jednom (48 koraka).
Ulazni string od 48 znakova propisuje smjer svakog koraka (`D`, `U`, `L`, `R`), a `?` znači bilo koji smjer.

**Intuicija:**
Naivni backtracking (do $4^{48}$ grana) je nemoguć. Trebamo **jako rezanje (pruning)**.

**Ključne optimizacije:**

1. Ako stignemo u donji lijevi kut prije 48. koraka $\rightarrow$ **RETURN**.
2. Ako su polja iznad i ispod nas blokirana, a lijevo i desno slobodna (ili obrnuto), mreža se dijeli na dva dijela koja ne možemo oba posjetiti $\rightarrow$ **RETURN**.

---

# Implementacija: Grid Paths (Optimizacija)

```cpp
// visited[9][9]: rub (redak/stupac 0 i 8) unaprijed je označen kao posjećen,
// pa ne trebamo provjeravati granice. Start je (1,1), cilj (7,1).
void solve(int r, int c, int step) {
    if (r == 7 && c == 1) {            // Stigli smo u donji lijevi kut
        if (step == 48) ans++;
        return;
    }

    // OPTIMIZACIJA: mreža se dijeli na dva dijela
    if (visited[r-1][c] && visited[r+1][c] &&
        !visited[r][c-1] && !visited[r][c+1]) return;
    if (visited[r][c-1] && visited[r][c+1] &&
        !visited[r-1][c] && !visited[r+1][c]) return;

    visited[r][c] = true;
    // ... za svaki smjer dopušten znakom s[step]:
    //     ako susjed nije posjećen, solve(susjed, step + 1)
    visited[r][c] = false;
}
```

Ovaj zadatak je među najtežima u uvodnom dijelu CSES-a jer bez optimizacija ne prolazi.

---

# Codeforces

Preporuka: rješavajte zadatke s tagom `brute force` težine do 1200.

[Codeforces Brute Force Problems](https://codeforces.com/problemset?tags=brute%20force)
