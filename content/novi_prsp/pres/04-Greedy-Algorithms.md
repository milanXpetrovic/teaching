---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Pohlepni algoritmi"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!-- _paginate: false -->
<!-- _class: title  -->

# Pohlepni algoritmi

## Lokalno optimalno = Globalno optimalno?

Programiranje za rješavanje složenih problema

---

# Sadržaj

1. **Uvod i motivacija**
   - Što je pohlepni algoritam?
   - Usporedba s dinamičkim programiranjem
2. **Problem novčića (Coin Problem)**
   - Kada radi, a kada ne?
3. **Raspoređivanje događaja (Activity Selection)**
   - Strategija ranog završetka
4. **Huffmanovo kodiranje**
   - Kompresija podataka
5. **Zadaci za vježbu**

---

<!-- _class: lead -->
# Uvod i motivacija

## Strategija donošenja odluka

---

# Što je pohlepni algoritam?

**Definicija:** Strategija koja na svakom koraku donosi **lokalno optimalan izbor** u nadi da će to dovesti do **globalno optimalnog rješenja**.

**Karakteristike:**

- **Konačnost odluke:** Jednom napravljen izbor se ne preispituje (nema *backtrackinga*).
- **Brzina:** Obično vrlo efikasni ($O(N)$ ili $O(N \log N)$ zbog sortiranja).
- **Jednostavnost:** Lako se implementiraju, ali...
- **Izazov:** Teško je dokazati da su ispravni za svaki slučaj.

---

# Pohlepni vs. Dinamičko Programiranje

Obje tehnike koriste svojstvo **optimalne podstrukture**, ali pristupaju problemu drugačije:

| Dinamičko programiranje | Pohlepni algoritmi |
| :--- | :--- |
| Prvo rješava podprobleme, a zatim na temelju njih donosi odluku. | Prvo donosi odluku, a zatim rješava preostali podproblem. |
| Razmatra **sve** opcije. | Razmatra **samo jednu** (pohlepnu) opciju. |
| Sporije, ali uvijek točno. | Brže, ali ne radi uvijek. |

---

# Ključna svojstva

Da bi pohlepni pristup bio ispravan, problem mora zadovoljiti:

1. **Svojstvo pohlepnog izbora (Greedy-choice property):**
   Globalno optimalno rješenje možemo izgraditi nizom lokalno optimalnih izbora. Prvi izbor nas ne sprječava da dođemo do rješenja.

2. **Optimalna podstruktura (Optimal substructure):**
   Optimalno rješenje problema sadrži optimalna rješenja svojih podproblema.

---

<!-- _class: lead -->
# Problem novčića

## Coin Problem

---

# Problem novčića

**Zadatak:** Treba pronaći minimalan broj novčića za iznos $N$ koristeći zadane denominacije.

**Pohlepna strategija:**
Uvijek uzimamo **najveći mogući novčić** koji nije veći od preostalog iznosa.

**Primjer (euro centi: 1, 2, 5, 10, 20, 50):** $N = 48$

1. Uzimamo 20 (ostaje 28)
2. Uzimamo 20 (ostaje 8)
3. Uzimamo 5 (ostaje 3)
4. Uzimamo 2 (ostaje 1)
5. Uzimamo 1 (ostaje 0)

**Rješenje:** 5 novčića. (Optimalno!)

---

# Kada pohlepni pristup NE radi?

Pohlepna strategija radi za "kanonske" sustave (euro, dolar), ali ne za sve.

**Kontraprimjer:**

- Kovanice: $\{1, 3, 4\}$
- Cilj: $6$

**Pohlepno:** $4 + 1 + 1$ $\rightarrow$ **3 novčića**.
**Optimalno:** $3 + 3$ $\rightarrow$ **2 novčića**.

**Zaključak:** Za općeniti skup kovanica moramo koristiti **dinamičko programiranje**.

---

# Problem novčića korak po korak

Isti pohlepni postupak na dva skupa novčića: na euro centima daje optimum, a na `{1, 3, 4}` griješi.

<style scoped>
.gr-coins { margin-top: 0.3em; }
.gr-coins .chips { font-size: 20px; margin-bottom: 0.4em; }
.gr-coins .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.gr-coins .chip.take { background: #9fdc9f; }
.gr-coins .chip.skip, .gr-coins .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.gr-coins .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gr-coins .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.gr-coins .row { display: flex; gap: 6px; }
.gr-coins .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-coins .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gr-coins .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.gr-coins .cell.todo .val { color: #b5b5b5; }
.gr-coins .cell.rng { background: #d6e6f5; }
.gr-coins .cell.best { background: #9fdc9f; }
.gr-coins .cell.src { background: #f5db7e; }
.gr-coins .cell.cur { background: var(--main); color: #fff; }
.gr-coins .cell.cur .idx, .gr-coins .cell.cur .val { color: #fff; }
.gr-coins .rows .row { margin-bottom: 6px; }
.gr-coins .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.gr-coins .prow { margin-top: -4px; }
.gr-coins .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.gr-coins .cell.dim { opacity: .3; }
.gr-coins .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.gr-coins .wrap { display: flex; gap: 28px; align-items: flex-start; }
.gr-coins .side { padding-top: 6px; }
.gr-coins .gsvg { display: block; overflow: visible; }
.gr-coins .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.gr-coins .e polygon { fill: #9a9a9a; }
.gr-coins .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.gr-coins .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.gr-coins .e.tree polygon { fill: #2f9e44; }
.gr-coins .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.gr-coins .e.off polygon { fill: #d5d5d5; }
.gr-coins .e.off .w { fill: #b5b5b5; }
.gr-coins .e.hid { opacity: 0; }
.gr-coins .e.bad line { stroke: #e03131; stroke-width: 6; }
.gr-coins .e.bad polygon { fill: #e03131; }
.gr-coins .e.on line { stroke: var(--main); stroke-width: 6; }
.gr-coins .e.on polygon { fill: var(--main); }
.gr-coins .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.gr-coins .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.gr-coins .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.gr-coins .n.c1 circle { fill: #ffd8a8; } .gr-coins .n.c2 circle { fill: #a5d8ff; } .gr-coins .n.c3 circle { fill: #b2f2bb; }
.gr-coins .n.c4 circle { fill: #fcc2d7; } .gr-coins .n.c5 circle { fill: #d0bfff; } .gr-coins .n.c6 circle { fill: #ffec99; }
.gr-coins .n.done circle { fill: #9fdc9f; }
.gr-coins .n.src circle { fill: #f5db7e; }
.gr-coins .n.cur circle { fill: var(--main); stroke: var(--main); }
.gr-coins .n.cur .id { fill: #fff; }
.gr-coins .tbl { display: grid; gap: 5px; }
.gr-coins .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.gr-coins .th.hl { background: var(--main); color: #fff; }
.gr-coins .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-coins .tc.none { border-color: transparent; }
.gr-coins .tc.k { background: #e3ecf6; }
.gr-coins .tc.best { background: #9fdc9f; }
.gr-coins .tc.src { background: #f5db7e; }
.gr-coins .tc.cur { background: var(--main); color: #fff; }
.gr-coins .line1, .gr-coins .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.gr-coins .line1 { margin-top: 0.5em; }
.gr-coins .line2 { font-weight: bold; }
.gr-coins .ctrl { margin-top: 0.5em; }
.gr-coins button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gr-coins button:hover { background: var(--main); color: #fff; }
.gr-coins .hint { font-size: 16px; color: #6e6e6e; }
.gr-coins .chip.bad { background: #ffc9c9; }
.gr-coins .chips { font-size: 22px; margin-bottom: 0.6em; }
.gr-coins .chip { font-size: 21px; min-width: 40px; }
</style>

<div class="gr-coins" data-cases="1,2,5,10,20,50:48|1,3,4:6">
  <div class="cc chips"></div>
  <div class="cg chips"></div>
  <div class="co chips"></div>
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
  document.querySelectorAll('.gr-coins').forEach(function (root) {
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

    var cases = root.dataset.cases.split('|').map(function (c) {
      var q = c.split(':');
      return { coins: q[0].split(',').map(Number).sort(function (a, b) { return a - b; }), n: Number(q[1]) };
    });
    var cBox = root.querySelector('.cc'), gBox = root.querySelector('.cg'), oBox = root.querySelector('.co');
    var snaps = [];
    cases.forEach(function (cs, ci) {
      var rest = cs.n, picks = [];
      snaps.push({ cs: ci, on: -1, picks: [], opt: null, l1: (ci + 1) + '. primjer: novčići {' + cs.coins.join(', ') + '}, iznos N = ' + cs.n, l2: 'Pohlepno: uvijek najveći novčić koji nije veći od preostalog iznosa' });
      while (rest !== 0) {
        var c = -1;
        cs.coins.forEach(function (v, k) { if (le(v, rest)) c = k; });
        rest -= cs.coins[c];
        picks.push(cs.coins[c]);
        snaps.push({ cs: ci, on: c, picks: picks.slice(), opt: null, l1: 'Uzimamo ' + cs.coins[c] + ', ostaje ' + rest, l2: 'Pohlepno: ' + picks.length + ' novčića' });
      }
      var dp = [0], from = [0];
      for (var x = 1; x !== cs.n + 1; x++) {
        dp.push(Infinity); from.push(0);
        cs.coins.forEach(function (v) { if (le(v, x)) if (lt(dp[x - v] + 1, dp[x])) { dp[x] = dp[x - v] + 1; from[x] = v; } });
      }
      var opt = [];
      for (var y = cs.n; y !== 0; y -= from[y]) opt.push(from[y]);
      opt.sort(function (a, b) { return b - a; });
      var same = opt.length === picks.length;
      snaps.push({ cs: ci, on: -1, picks: picks.slice(), opt: opt, bad: !same,
        l1: 'Optimalno (DP): ' + opt.join(' + ') + ' = ' + cs.n + ', ' + opt.length + ' novčića',
        l2: same ? 'Pohlepno je ovdje optimalno (kanonski sustav)   ✓' : 'Pohlepno daje ' + picks.length + ', a optimum je ' + opt.length + ': pohlepni pristup NE radi za ovaj skup!' });
    });
    function draw(s) {
      var cs = cases[s.cs];
      cBox.textContent = 'Novčići:';
      cs.coins.forEach(function (v, k) { cBox.appendChild(mk('span', k === s.on ? 'chip on' : 'chip', v)); });
      gBox.textContent = 'Pohlepno:';
      if (s.picks.length === 0) gBox.appendChild(mk('span', 'muted', 'još ništa'));
      s.picks.forEach(function (v, k) { gBox.appendChild(mk('span', s.opt ? (s.bad ? 'chip bad' : 'chip take') : (k === s.picks.length - 1 ? 'chip on' : 'chip'), v)); });
      oBox.textContent = s.opt ? 'Optimalno:' : '';
      if (s.opt) s.opt.forEach(function (v) { oBox.appendChild(mk('span', 'chip take', v)); });
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
# Raspoređivanje događaja

## Activity Selection Problem

---

# Problem: Activity Selection

**Zadatak:** Treba odabrati maksimalan broj događaja koji se ne preklapaju. Svaki događaj ima `start` i `end` vrijeme.

**Koja je ispravna pohlepna strategija?**

1. ~~Najkraći događaj?~~ (Ne, kratak može biti u sredini dva duga)
2. ~~Najraniji početak?~~ (Ne, jedan dugi može blokirati sve ostale)
3. **Najraniji završetak!**

**Intuicija:**
Odabirom događaja koji **najranije završava**, oslobađamo resurs što je prije moguće za ostale događaje.

---

# Algoritam

1. **Sortiramo** događaje po vremenu završetka.
2. Uzimamo prvi događaj.
3. Uzimamo sljedeći koji počinje **nakon** što je prethodni završio.

**Složenost:** $O(N \log N)$ zbog sortiranja.

---

# Implementacija: Activity Selection

```cpp
struct Event { int start, end; };

// Sortiramo po vremenu završetka
bool compareEvents(const Event& a, const Event& b) {
    return a.end < b.end;
}

sort(events.begin(), events.end(), compareEvents);

int ans = 1;
int last_end = events[0].end;

for (int i = 1; i < n; ++i) {
    if (events[i].start >= last_end) { // Ako se ne preklapa
        ans++;
        last_end = events[i].end;
    }
}
```

---

# Activity Selection korak po korak

Događaji su sortirani po kraju. Uzimamo događaj ako počinje najranije kad prethodno odabrani završi.

<style scoped>
.gr-act { margin-top: 0.3em; }
.gr-act .chips { font-size: 20px; margin-bottom: 0.4em; }
.gr-act .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.gr-act .chip.take { background: #9fdc9f; }
.gr-act .chip.skip, .gr-act .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.gr-act .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gr-act .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.gr-act .row { display: flex; gap: 6px; }
.gr-act .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-act .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gr-act .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.gr-act .cell.todo .val { color: #b5b5b5; }
.gr-act .cell.rng { background: #d6e6f5; }
.gr-act .cell.best { background: #9fdc9f; }
.gr-act .cell.src { background: #f5db7e; }
.gr-act .cell.cur { background: var(--main); color: #fff; }
.gr-act .cell.cur .idx, .gr-act .cell.cur .val { color: #fff; }
.gr-act .rows .row { margin-bottom: 6px; }
.gr-act .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.gr-act .prow { margin-top: -4px; }
.gr-act .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.gr-act .cell.dim { opacity: .3; }
.gr-act .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.gr-act .wrap { display: flex; gap: 28px; align-items: flex-start; }
.gr-act .side { padding-top: 6px; }
.gr-act .gsvg { display: block; overflow: visible; }
.gr-act .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.gr-act .e polygon { fill: #9a9a9a; }
.gr-act .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.gr-act .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.gr-act .e.tree polygon { fill: #2f9e44; }
.gr-act .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.gr-act .e.off polygon { fill: #d5d5d5; }
.gr-act .e.off .w { fill: #b5b5b5; }
.gr-act .e.hid { opacity: 0; }
.gr-act .e.bad line { stroke: #e03131; stroke-width: 6; }
.gr-act .e.bad polygon { fill: #e03131; }
.gr-act .e.on line { stroke: var(--main); stroke-width: 6; }
.gr-act .e.on polygon { fill: var(--main); }
.gr-act .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.gr-act .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.gr-act .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.gr-act .n.c1 circle { fill: #ffd8a8; } .gr-act .n.c2 circle { fill: #a5d8ff; } .gr-act .n.c3 circle { fill: #b2f2bb; }
.gr-act .n.c4 circle { fill: #fcc2d7; } .gr-act .n.c5 circle { fill: #d0bfff; } .gr-act .n.c6 circle { fill: #ffec99; }
.gr-act .n.done circle { fill: #9fdc9f; }
.gr-act .n.src circle { fill: #f5db7e; }
.gr-act .n.cur circle { fill: var(--main); stroke: var(--main); }
.gr-act .n.cur .id { fill: #fff; }
.gr-act .tbl { display: grid; gap: 5px; }
.gr-act .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.gr-act .th.hl { background: var(--main); color: #fff; }
.gr-act .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-act .tc.none { border-color: transparent; }
.gr-act .tc.k { background: #e3ecf6; }
.gr-act .tc.best { background: #9fdc9f; }
.gr-act .tc.src { background: #f5db7e; }
.gr-act .tc.cur { background: var(--main); color: #fff; }
.gr-act .line1, .gr-act .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.gr-act .line1 { margin-top: 0.5em; }
.gr-act .line2 { font-weight: bold; }
.gr-act .ctrl { margin-top: 0.5em; }
.gr-act button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gr-act button:hover { background: var(--main); color: #fff; }
.gr-act .hint { font-size: 16px; color: #6e6e6e; }
.gr-act .tl { display: grid; grid-auto-rows: 24px; row-gap: 3px; }
.gr-act .ax { font-size: 14px; color: #6e6e6e; margin-left: -6px; }
.gr-act .flab { font-size: 14px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; }
.gr-act .blk { grid-column: 2 / 3; background: #ececec; border-radius: 3px; z-index: 0; }
.gr-act .ev { z-index: 1; border: 2px solid #141414; border-radius: 5px; background: #fff; font-size: 14px; font-weight: bold; text-align: center; line-height: 20px; transition: background-color .25s; }
.gr-act .ev.take { background: #9fdc9f; }
.gr-act .ev.skip { opacity: .35; }
.gr-act .ev.cur { border-color: var(--main); border-width: 3px; box-shadow: 0 0 0 2px var(--main); }
.gr-act .line1 { margin-top: 0.3em; }
</style>

<div class="gr-act" data-ev="1-4,3-5,0-6,5-7,3-9,5-9,6-10,8-11,8-12,2-14,12-16">
  <div class="tl"></div>
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
  document.querySelectorAll('.gr-act').forEach(function (root) {
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

    var ev = parseEdges(root.dataset.ev).map(function (e) { return { s: e.a, e: e.b }; });
    ev.sort(function (a, b) { return a.e - b.e || a.s - b.s; });
    var T = 0;
    ev.forEach(function (e) { T = Math.max(T, e.e); });
    var g = root.querySelector('.tl');
    g.style.gridTemplateColumns = '70px repeat(' + T + ', 46px) 20px';
    for (var t = 0; t !== T + 1; t++) {
      var ax = mk('div', 'ax', t);
      ax.style.gridRow = '1'; ax.style.gridColumn = String(t + 2);
      g.appendChild(ax);
    }
    var bars = [], blks = [];
    ev.forEach(function (e, k) {
      var lab = mk('div', 'flab', '#' + (k + 1));
      lab.style.gridRow = String(k + 2); lab.style.gridColumn = '1';
      g.appendChild(lab);
      var blk = mk('div', 'blk');
      blk.style.gridRow = String(k + 2);
      g.appendChild(blk); blks.push(blk);
      var b = mk('div', 'ev', e.s + '–' + e.e);
      b.style.gridRow = String(k + 2); b.style.gridColumn = (e.s + 2) + ' / ' + (e.e + 2);
      g.appendChild(b); bars.push(b);
    });
    var st = ev.map(function () { return ''; }), last = 0, ans = 0;
    var snaps = [{ st: st.slice(), cur: -1, last: 0, l1: 'Događaji su sortirani po vremenu završetka', l2: 'Siva zona = vrijeme prije last_end (resurs je zauzet)' }];
    ev.forEach(function (e, k) {
      var ok = le(last, e.s), l1;
      if (ok) { st[k] = 'take'; ans++; l1 = 'Događaj ' + e.s + '–' + e.e + ': počinje u ' + e.s + ' ≥ last_end = ' + last + '  → uzimamo'; last = e.e; }
      else { st[k] = 'skip'; l1 = 'Događaj ' + e.s + '–' + e.e + ': počinje u ' + e.s + ', prije last_end = ' + last + '  → preklapa se, preskačemo'; }
      snaps.push({ st: st.slice(), cur: k, last: last, l1: l1, l2: 'ans = ' + ans + ', last_end = ' + last });
    });
    snaps.push({ st: st.slice(), cur: -1, last: 0, l1: 'Svaki put smo uzeli događaj koji najranije završava', l2: 'Maksimalno ' + ans + ' događaja bez preklapanja   ✓' });
    function draw(s) {
      bars.forEach(function (b, k) {
        var c = 'ev';
        if (s.st[k]) c += ' ' + s.st[k];
        if (k === s.cur) c += ' cur';
        setc(b, c);
        blks[k].style.gridColumn = '2 / ' + (s.last + 2);
        blks[k].style.display = s.last === 0 ? 'none' : 'block';
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
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 800); }
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
# Huffmanovo kodiranje

## Kompresija podataka

---

# Huffmanovo kodiranje

**Cilj:** Prikazati podatke koristeći što manje bitova (kompresija). Česti znakovi trebaju imati kraće kodove.
**Uvjet:** Kodovi moraju biti **prefiksni** (nijedan kod nije početak drugog).

**Pohlepna strategija:**
Gradimo stablo odozdo prema gore. U svakom koraku spajamo **dva čvora s najmanjom frekvencijom**.

**Alat:** Prioritetni red (`std::priority_queue`).

---

# Algoritam (Huffman)

1. Kreiramo list za svaki znak (težina = frekvencija).
2. Ubacimo sve u **min-heap**.
3. Dok u heapu ima više od 1 čvora:
   - Izvadimo dva najmanja: $A$ i $B$.
   - Kreiramo novi čvor $C$ s težinom $freq(A) + freq(B)$.
   - Postavimo $A$ i $B$ kao djecu od $C$.
   - Vratimo $C$ u heap.

**Rezultat:** Stablo gdje put lijevo znači `0`, a desno `1`.

---

# Implementacija: čvor i usporedba

```cpp
struct Node {
    char ch;
    int freq;
    Node *left = nullptr, *right = nullptr;
    Node(char c, int f) : ch(c), freq(f) {}
};

// Min-heap: čvor s manjom frekvencijom ima veći prioritet
struct Compare {
    bool operator()(Node* a, Node* b) {
        return a->freq > b->freq;
    }
};

priority_queue<Node*, vector<Node*>, Compare> minHeap;
```

---

# Implementacija: gradnja stabla

```cpp
// Inicijalizacija: za svaki znak ubacimo list u minHeap

while (minHeap.size() > 1) {
    // Uzimamo dva najmanja
    Node* a = minHeap.top(); minHeap.pop();
    Node* b = minHeap.top(); minHeap.pop();

    // Spajamo ih u novi čvor ('$' označava unutarnji čvor)
    Node* c = new Node('$', a->freq + b->freq);
    c->left = a;
    c->right = b;

    minHeap.push(c);
}
// minHeap.top() je korijen Huffmanovog stabla
```

**Složenost:** $O(N \log N)$, gdje je $N$ broj različitih znakova.

---

# Huffmanovo kodiranje korak po korak

U svakom koraku iz min-heapa vadimo dva čvora s najmanjom težinom i spajamo ih u novi čvor.

<style scoped>
.gr-huff { margin-top: 0.3em; }
.gr-huff .chips { font-size: 20px; margin-bottom: 0.4em; }
.gr-huff .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.gr-huff .chip.take { background: #9fdc9f; }
.gr-huff .chip.skip, .gr-huff .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.gr-huff .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gr-huff .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.gr-huff .row { display: flex; gap: 6px; }
.gr-huff .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-huff .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gr-huff .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.gr-huff .cell.todo .val { color: #b5b5b5; }
.gr-huff .cell.rng { background: #d6e6f5; }
.gr-huff .cell.best { background: #9fdc9f; }
.gr-huff .cell.src { background: #f5db7e; }
.gr-huff .cell.cur { background: var(--main); color: #fff; }
.gr-huff .cell.cur .idx, .gr-huff .cell.cur .val { color: #fff; }
.gr-huff .rows .row { margin-bottom: 6px; }
.gr-huff .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.gr-huff .prow { margin-top: -4px; }
.gr-huff .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.gr-huff .cell.dim { opacity: .3; }
.gr-huff .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.gr-huff .wrap { display: flex; gap: 28px; align-items: flex-start; }
.gr-huff .side { padding-top: 6px; }
.gr-huff .gsvg { display: block; overflow: visible; }
.gr-huff .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.gr-huff .e polygon { fill: #9a9a9a; }
.gr-huff .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.gr-huff .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.gr-huff .e.tree polygon { fill: #2f9e44; }
.gr-huff .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.gr-huff .e.off polygon { fill: #d5d5d5; }
.gr-huff .e.off .w { fill: #b5b5b5; }
.gr-huff .e.hid { opacity: 0; }
.gr-huff .e.bad line { stroke: #e03131; stroke-width: 6; }
.gr-huff .e.bad polygon { fill: #e03131; }
.gr-huff .e.on line { stroke: var(--main); stroke-width: 6; }
.gr-huff .e.on polygon { fill: var(--main); }
.gr-huff .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.gr-huff .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.gr-huff .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.gr-huff .n.c1 circle { fill: #ffd8a8; } .gr-huff .n.c2 circle { fill: #a5d8ff; } .gr-huff .n.c3 circle { fill: #b2f2bb; }
.gr-huff .n.c4 circle { fill: #fcc2d7; } .gr-huff .n.c5 circle { fill: #d0bfff; } .gr-huff .n.c6 circle { fill: #ffec99; }
.gr-huff .n.done circle { fill: #9fdc9f; }
.gr-huff .n.src circle { fill: #f5db7e; }
.gr-huff .n.cur circle { fill: var(--main); stroke: var(--main); }
.gr-huff .n.cur .id { fill: #fff; }
.gr-huff .tbl { display: grid; gap: 5px; }
.gr-huff .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.gr-huff .th.hl { background: var(--main); color: #fff; }
.gr-huff .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-huff .tc.none { border-color: transparent; }
.gr-huff .tc.k { background: #e3ecf6; }
.gr-huff .tc.best { background: #9fdc9f; }
.gr-huff .tc.src { background: #f5db7e; }
.gr-huff .tc.cur { background: var(--main); color: #fff; }
.gr-huff .line1, .gr-huff .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.gr-huff .line1 { margin-top: 0.5em; }
.gr-huff .line2 { font-weight: bold; }
.gr-huff .ctrl { margin-top: 0.5em; }
.gr-huff button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gr-huff button:hover { background: var(--main); color: #fff; }
.gr-huff .hint { font-size: 16px; color: #6e6e6e; }
.gr-huff .he line { stroke: #9a9a9a; stroke-width: 3; }
.gr-huff .he .bitl { font-size: 17px; font-weight: bold; fill: var(--main); text-anchor: middle; dominant-baseline: central; }
.gr-huff .he.hidn, .gr-huff .n.hidn { opacity: 0; }
.gr-huff .n .chl { font-size: 18px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; }
.gr-huff .side { max-width: 470px; padding-top: 20px; }
</style>

<div class="gr-huff" data-f="A:5,B:9,C:12,D:13,E:16,F:45">
  <div class="wrap">
    <div class="graph"></div>
    <div class="side">
      <div class="heap chips"></div>
      <div class="codes chips"></div>
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
  document.querySelectorAll('.gr-huff').forEach(function (root) {
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

    var items = root.dataset.f.split(',').map(function (t) { var q = t.split(':'); return { ch: q[0], f: Number(q[1]) }; });
    var nodes = items.map(function (it, k) { return { id: k, f: it.f, ch: it.ch, l: -1, r: -1, born: 0 }; });
    var heap = nodes.map(function (x) { return x.id; });
    function byF(a, b) { return nodes[a].f - nodes[b].f || a - b; }
    var merges = [];
    while (heap.length !== 1) {
      heap.sort(byF);
      var a = heap.shift(), b = heap.shift();
      var c = { id: nodes.length, f: nodes[a].f + nodes[b].f, ch: '', l: a, r: b, born: merges.length + 1 };
      nodes.push(c); heap.push(c.id);
      merges.push([a, b, c.id]);
    }
    var rootId = heap[0];
    // raspored: listovi po in-orderu, unutarnji čvor iznad sredine djece
    var leafIx = 0, maxd = 0;
    function lay(v, d) {
      var x = nodes[v]; x.d = d; maxd = Math.max(maxd, d);
      if (x.l === -1) { x.px = leafIx; leafIx++; return; }
      lay(x.l, d + 1); lay(x.r, d + 1);
      x.px = (nodes[x.l].px + nodes[x.r].px) / 2;
    }
    lay(rootId, 0);
    var TW = 560, TH = 300;
    var sx = (TW - 60) / Math.max(1, leafIx - 1), sy = (TH - 80) / Math.max(1, maxd);
    var svg = sv('svg', { viewBox: '0 0 ' + TW + ' ' + TH, width: TW, height: TH, 'class': 'gsvg' }, root.querySelector('.graph'));
    var gE = sv('g', {}, svg), gN = sv('g', {}, svg);
    nodes.forEach(function (x) { x.X = 30 + x.px * sx; x.Y = 26 + x.d * sy; });
    nodes.forEach(function (x) {
      if (x.l !== -1) {
        x.eg = [x.l, x.r].map(function (c, k) {
          var y = nodes[c], g = sv('g', { 'class': 'he' }, gE);
          sv('line', { x1: x.X, y1: x.Y, x2: y.X, y2: y.Y }, g);
          sv('text', { x: (x.X + y.X) / 2 + (k ? 10 : -10), y: (x.Y + y.Y) / 2 - 8, 'class': 'bitl' }, g).textContent = k;
          return g;
        });
      }
      x.g = sv('g', { 'class': 'n' }, gN);
      sv('circle', { cx: x.X, cy: x.Y, r: 20 }, x.g);
      sv('text', { x: x.X, y: x.Y, 'class': 'id' }, x.g).textContent = x.f;
      if (x.ch) sv('text', { x: x.X, y: x.Y + 34, 'class': 'chl' }, x.g).textContent = x.ch;
    });
    var hBox = root.querySelector('.heap'), cBox = root.querySelector('.codes');
    var codes = {};
    function walk(v, p) { var x = nodes[v]; if (x.l === -1) { codes[x.ch] = p || '0'; return; } walk(x.l, p + '0'); walk(x.r, p + '1'); }
    walk(rootId, '');
    function label(id) { var x = nodes[id]; return x.ch ? x.ch + ':' + x.f : String(x.f); }
    var snaps = [], h = items.map(function (it, k) { return k; });
    snaps.push({ born: 0, heap: h.slice(), pick: [], cur: -1, codes: false, l1: 'Svaki znak je list s težinom = frekvencija; svi su u min-heapu', l2: 'Dok heap ima više od jednog čvora: spajamo dva najmanja' });
    merges.forEach(function (m, k) {
      h.sort(byF);
      snaps.push({ born: k, heap: h.slice(), pick: [m[0], m[1]], cur: -1, codes: false,
        l1: 'Vadimo dva najmanja: ' + label(m[0]) + ' i ' + label(m[1]), l2: 'Heap: ' + h.length + ' čvorova' });
      h = h.filter(function (v) { return v !== m[0] ? v !== m[1] : false; });
      h.push(m[2]); h.sort(byF);
      snaps.push({ born: k + 1, heap: h.slice(), pick: [m[0], m[1]], cur: m[2], codes: false,
        l1: 'Novi čvor ' + nodes[m[0]].f + ' + ' + nodes[m[1]].f + ' = ' + nodes[m[2]].f + ' vraćamo u heap', l2: 'Heap: ' + h.length + ' čvorova' });
    });
    var total = 0;
    items.forEach(function (it) { total += it.f * codes[it.ch].length; });
    snaps.push({ born: merges.length, heap: [rootId], pick: [], cur: -1, codes: true,
      l1: 'Kod znaka čitamo od korijena: lijevo 0, desno 1. Česti znakovi imaju kraće kodove.',
      l2: 'Duljina kodiranog teksta: ' + total + ' bita, a s fiksnim 3-bitnim kodom ' + (3 * items.reduce(function (s, it) { return s + it.f; }, 0)) + '   ✓' });
    function draw(s) {
      nodes.forEach(function (x) {
        var vis = le(x.born, s.born);
        var c = vis ? 'n' : 'n hidn';
        if (s.pick.indexOf(x.id) !== -1) c += ' src';
        if (x.id === s.cur) c += ' cur';
        if (s.codes ? x.l === -1 : false) c += ' done';
        setc(x.g, c);
        if (x.eg) x.eg.forEach(function (g) { setc(g, vis ? 'he' : 'he hidn'); });
      });
      hBox.textContent = 'Heap:';
      s.heap.forEach(function (id) { hBox.appendChild(mk('span', s.pick.indexOf(id) !== -1 ? 'chip on' : 'chip', label(id))); });
      cBox.textContent = s.codes ? 'Kodovi:' : '';
      if (s.codes) items.forEach(function (it) { cBox.appendChild(mk('span', 'chip take', it.ch + ' = ' + codes[it.ch])); });
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
# Zadaci za vježbu

## CSES i Codeforces

---

# CSES Problem Set

1. **[Movie Festival](https://cses.fi/problemset/task/1629)**
   - Klasičan *Activity Selection* problem. Sortiramo po kraju filma.
2. **[Stick Lengths](https://cses.fi/problemset/task/1074)**
   - Minimizacija sume razlika $|x - p_i|$. Optimalni $x$ je **medijan**.
3. **[Tasks and Deadlines](https://cses.fi/problemset/task/1630)**
   - Maksimizacija nagrade $= deadline - finish$.
   - *Hint:* Kraće zadatke obavljamo prve.
4. **[Towers](https://cses.fi/problemset/task/1073)**
   - Slaganje kocki jedne na drugu. Zahtijeva `multiset` za efikasno traženje "baze".

---

# Codeforces preporuke

Tražite zadatke s tagom `greedy` težine 800-1200.

- **[Hit the Lottery](https://codeforces.com/problemset/problem/996/A)**
  - Problem novčića s novčanicama 1, 5, 10, 20, 100 (kanonski sustav).
- **[Boats Competition](https://codeforces.com/problemset/problem/1399/C)**
  - Formiranje parova s istim zbrojem težina. Sortiranje + Two Pointers.

---

<!-- _class: title -->
# Movie Festival (CSES)

## Activity Selection u praksi

---

# Analiza: Movie Festival

**Problem:**
U kinu se prikazuje $n$ filmova. Svaki ima vrijeme početka i kraja.
Želimo pogledati **maksimalan broj filmova** u cijelosti (bez preklapanja).

**Intuicija:**
Ovo je identičan problem kao **Activity Selection**.
Pohlepna strategija: uvijek biramo film koji **najranije završava**, a da ne počinje prije nego što je prethodni završio.

Zašto? Time ostavljamo najviše vremena za ostale filmove.

---

# Implementacija: Movie Festival

```cpp
int n; cin >> n;
vector<pair<int, int>> movies(n);
for (int i = 0; i < n; ++i)
    cin >> movies[i].second >> movies[i].first; // Učitavamo kao {kraj, početak}

sort(movies.begin(), movies.end()); // Sortira po kraju (first)

int ans = 0;
int current_time = 0;

for (auto m : movies) {
    if (m.second >= current_time) { // m.second je početak
        ans++;
        current_time = m.first; // m.first je kraj
    }
}
cout << ans << "\n";
```

---

<!-- _class: title -->
# Stick Lengths (CSES)

## Medijan kao optimalna točka

---

# Analiza: Stick Lengths

**Problem:**
Imamo $n$ štapova duljina $p_1, p_2, \dots, p_n$.
Želimo ih sve skratiti ili produžiti na istu duljinu $x$.
Cijena promjene je $|p_i - x|$. Treba minimizirati ukupnu cijenu $\sum |p_i - x|$.

**Intuicija:**
Tražimo broj $x$ koji minimizira sumu apsolutnih udaljenosti.

- Da je kvadratna udaljenost $(p_i - x)^2$, to bi bio prosjek (mean).
- Za apsolutnu udaljenost, to je **medijan**.

Ako sortiramo niz, medijan je element na sredini (`p[n/2]`).

---

# Implementacija: Stick Lengths

```cpp
int n; cin >> n;
vector<int> p(n);
for (int i = 0; i < n; ++i) cin >> p[i];

sort(p.begin(), p.end());

int median = p[n / 2];
long long cost = 0;

for (int x : p) {
    cost += abs(x - median);
}

cout << cost << "\n";
```

**Napomena:** Koristite `long long` za cijenu jer suma može biti velika!

---

<!-- _class: title -->
# Tasks and Deadlines (CSES)

## Minimizacija kazne

---

# Analiza: Tasks and Deadlines

**Problem:**
Imamo $n$ zadataka. Svaki traje $a_i$ i ima rok $d_i$.
Za svaki zadatak dobivamo nagradu $d_i - f_i$, gdje je $f_i$ vrijeme završetka.
Treba maksimizirati ukupnu nagradu.

**Intuicija:**
Ukupna nagrada = $\sum (d_i - f_i) = \sum d_i - \sum f_i$.
$\sum d_i$ je konstanta (ne ovisi o redoslijedu).
Da bismo maksimizirali izraz, moramo **minimizirati $\sum f_i$** (sumu vremena završetaka).

Suma završetaka je minimalna ako **kraće zadatke radimo prve**.
(Ako imamo zadatke trajanja 2 i 10: redoslijed 2, 10 daje završetke 2 i 12 (suma 14). Redoslijed 10, 2 daje 10 i 12 (suma 22).)

---

# Implementacija: Tasks and Deadlines

```cpp
int n; cin >> n;
vector<pair<int, int>> tasks(n);
for (int i = 0; i < n; ++i)
    cin >> tasks[i].first >> tasks[i].second; // {trajanje, rok}

sort(tasks.begin(), tasks.end()); // Sortiramo po trajanju

long long current_time = 0;
long long reward = 0;

for (auto t : tasks) {
    current_time += t.first;
    reward += (t.second - current_time);
}

cout << reward << "\n";
```

---

<!-- _class: title -->
# Towers (CSES)

## Pohlepno slaganje i Multiset

---

# Analiza: Towers

**Problem:**
Imamo $n$ kocaka koje dolaze jedna po jedna (veličine se mogu ponavljati).
Kocku možemo staviti na vrh postojećeg tornja samo ako je **strogo manja** od trenutne vršne kocke. Inače započinjemo novi toranj.
Treba minimizirati broj tornjeva.

**Intuicija:**
Kad dođe kocka veličine $X$, na koji toranj je staviti?
Želimo "potrošiti" toranj čiji je vrh **najmanji mogući, ali strogo veći od $X$**.
Zašto? Da bismo veće vrhove sačuvali za veće kocke koje možda dođu kasnije.

Vrhove svih tornjeva pratimo u `multiset`-u i za $X$ tražimo `upper_bound(X)`.
Zbog strogog uvjeta koristimo `upper_bound`, a ne `lower_bound` (jednaku kocku ne smijemo staviti na vrh).

---

# Implementacija: Towers

```cpp
int n; cin >> n;
multiset<int> towers;

for (int i = 0; i < n; ++i) {
    int x; cin >> x;

    // Najmanji vrh koji je strogo veći od x
    auto it = towers.upper_bound(x);

    if (it == towers.end()) {
        // Nema takvog tornja, radimo novi
        towers.insert(x);
    } else {
        // Proširujemo postojeći toranj:
        // mičemo stari vrh i stavljamo novi (x)
        towers.erase(it);
        towers.insert(x);
    }
}
cout << towers.size() << "\n";
```

---

# Towers korak po korak

Za kocku `x` tražimo najmanji vrh tornja strogo veći od `x` (`upper_bound`). Ako ga nema, otvaramo novi toranj.

<style scoped>
.gr-towers { margin-top: 0.3em; }
.gr-towers .chips { font-size: 20px; margin-bottom: 0.4em; }
.gr-towers .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.gr-towers .chip.take { background: #9fdc9f; }
.gr-towers .chip.skip, .gr-towers .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.gr-towers .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gr-towers .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.gr-towers .row { display: flex; gap: 6px; }
.gr-towers .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-towers .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gr-towers .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.gr-towers .cell.todo .val { color: #b5b5b5; }
.gr-towers .cell.rng { background: #d6e6f5; }
.gr-towers .cell.best { background: #9fdc9f; }
.gr-towers .cell.src { background: #f5db7e; }
.gr-towers .cell.cur { background: var(--main); color: #fff; }
.gr-towers .cell.cur .idx, .gr-towers .cell.cur .val { color: #fff; }
.gr-towers .rows .row { margin-bottom: 6px; }
.gr-towers .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.gr-towers .prow { margin-top: -4px; }
.gr-towers .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.gr-towers .cell.dim { opacity: .3; }
.gr-towers .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.gr-towers .wrap { display: flex; gap: 28px; align-items: flex-start; }
.gr-towers .side { padding-top: 6px; }
.gr-towers .gsvg { display: block; overflow: visible; }
.gr-towers .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.gr-towers .e polygon { fill: #9a9a9a; }
.gr-towers .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.gr-towers .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.gr-towers .e.tree polygon { fill: #2f9e44; }
.gr-towers .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.gr-towers .e.off polygon { fill: #d5d5d5; }
.gr-towers .e.off .w { fill: #b5b5b5; }
.gr-towers .e.hid { opacity: 0; }
.gr-towers .e.bad line { stroke: #e03131; stroke-width: 6; }
.gr-towers .e.bad polygon { fill: #e03131; }
.gr-towers .e.on line { stroke: var(--main); stroke-width: 6; }
.gr-towers .e.on polygon { fill: var(--main); }
.gr-towers .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.gr-towers .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.gr-towers .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.gr-towers .n.c1 circle { fill: #ffd8a8; } .gr-towers .n.c2 circle { fill: #a5d8ff; } .gr-towers .n.c3 circle { fill: #b2f2bb; }
.gr-towers .n.c4 circle { fill: #fcc2d7; } .gr-towers .n.c5 circle { fill: #d0bfff; } .gr-towers .n.c6 circle { fill: #ffec99; }
.gr-towers .n.done circle { fill: #9fdc9f; }
.gr-towers .n.src circle { fill: #f5db7e; }
.gr-towers .n.cur circle { fill: var(--main); stroke: var(--main); }
.gr-towers .n.cur .id { fill: #fff; }
.gr-towers .tbl { display: grid; gap: 5px; }
.gr-towers .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.gr-towers .th.hl { background: var(--main); color: #fff; }
.gr-towers .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gr-towers .tc.none { border-color: transparent; }
.gr-towers .tc.k { background: #e3ecf6; }
.gr-towers .tc.best { background: #9fdc9f; }
.gr-towers .tc.src { background: #f5db7e; }
.gr-towers .tc.cur { background: var(--main); color: #fff; }
.gr-towers .line1, .gr-towers .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.gr-towers .line1 { margin-top: 0.5em; }
.gr-towers .line2 { font-weight: bold; }
.gr-towers .ctrl { margin-top: 0.5em; }
.gr-towers button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gr-towers button:hover { background: var(--main); color: #fff; }
.gr-towers .hint { font-size: 16px; color: #6e6e6e; }
.gr-towers .rl { width: 70px; }
.gr-towers .towers { display: flex; gap: 22px; align-items: flex-end; min-height: 190px; padding: 0 10px; border-bottom: 4px solid #141414; }
.gr-towers .tower { display: flex; flex-direction: column-reverse; gap: 3px; }
.gr-towers .cube { height: 38px; line-height: 38px; font-size: 22px; font-weight: bold; }
.gr-towers .ms { align-self: flex-end; }
</style>

<div class="gr-towers" data-c="3,8,2,1,5,4,7,6,2">
  <div class="rows"></div>
  <div class="wrap">
    <div class="towers"></div>
    <div class="ms chips"></div>
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
  document.querySelectorAll('.gr-towers').forEach(function (root) {
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

    var cubes = root.dataset.c.split(',').map(Number), n = cubes.length;
    var box = root.querySelector('.rows');
    var R = lrow(box, 'kocke', n, 0, false);
    var P = prow(box, n);
    var tw = root.querySelector('.towers'), ms = root.querySelector('.ms');
    var towers = [], snaps = [];
    function tops() { return towers.map(function (t) { return t[t.length - 1]; }).sort(function (a, b) { return a - b; }); }
    snaps.push({ k: -1, towers: [], hit: -1, l1: 'Kocke dolaze redom; u multisetu pamtimo samo vrhove tornjeva', l2: 'Tornjeva: 0' });
    cubes.forEach(function (x, k) {
      var best = -1;
      towers.forEach(function (t, i) {
        var top = t[t.length - 1];
        if (lt(x, top)) if (best === -1 ? true : lt(top, towers[best][towers[best].length - 1])) best = i;
      });
      var l1;
      if (best === -1) { towers.push([x]); l1 = 'x = ' + x + ':  upper_bound(' + x + ') = end()  → nijedan vrh nije veći, novi toranj'; best = towers.length - 1; }
      else { var old = towers[best][towers[best].length - 1]; towers[best].push(x); l1 = 'x = ' + x + ':  upper_bound(' + x + ') = ' + old + '  → stavljamo na toranj s vrhom ' + old + ' (erase ' + old + ', insert ' + x + ')'; }
      snaps.push({ k: k, towers: towers.map(function (t) { return t.slice(); }), hit: best, l1: l1, l2: 'Tornjeva: ' + towers.length + (k === n - 1 ? '   ✓' : '') });
    });
    function draw(s) {
      R.cells.forEach(function (c, k) {
        setc(c, 'cell' + (k === s.k ? ' cur' : '') + (lt(k, s.k) ? ' dim' : ''));
        R.vals[k].textContent = cubes[k];
      });
      setPtrs(P, [['x', s.k]]);
      tw.textContent = '';
      s.towers.forEach(function (t, i) {
        var col = mk('div', 'tower');
        t.forEach(function (v, j) {
          col.appendChild(mk('div', 'cell cube' + (i === s.hit ? (j === t.length - 1 ? ' cur' : ' rng') : ''), v));
        });
        tw.appendChild(col);
      });
      ms.textContent = 'multiset vrhova:';
      var tp = s.towers.map(function (t) { return t[t.length - 1]; }).sort(function (a, b) { return a - b; });
      if (tp.length === 0) ms.appendChild(mk('span', 'muted', 'prazan'));
      tp.forEach(function (v) { ms.appendChild(mk('span', 'chip', v)); });
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
# Zaključak i najbitnije napomene

---

# Što smo danas naučili?

1. **Pohlepni pristup:**
   - Donošenje lokalno optimalnih odluka u nadi da ćemo doći do globalnog optimuma.
   - Brzo i jednostavno, ali ne radi uvijek (npr. problem novčića s neobičnim kovanicama).

2. **Ključni algoritmi:**
   - **Activity Selection:** Uvijek biramo događaj koji **najranije završava**.
   - **Huffmanovo kodiranje:** Spajamo dva čvora s najmanjom frekvencijom (koristeći `priority_queue`).

3. **Kada koristiti?**
   - Kad problem ima **svojstvo pohlepnog izbora** i **optimalnu podstrukturu**.

---

# Savjeti za rješavanje zadataka

- **Sortiranje je često prvi korak:**
  - Većina pohlepnih algoritama zahtijeva sortiran ulaz (po cijeni, težini, vremenu kraja...).
- **Pokušajte smisliti kontraprimjer:**
  - Prije kodiranja probajte naći mali testni slučaj na kojem vaša ideja pada.
- **Ako pohlepno ne radi:**
  - Vjerojatno trebate **dinamičko programiranje** (DP).
  