---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Podijeli pa vladaj i binarno pretraživanje"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!-- _paginate: false -->
<!-- _class: title -->

# Podijeli pa vladaj i binarno pretraživanje

## Divide and Conquer, Binary Search, BS on Answer

---

# Sadržaj

1. **Uvod i motivacija**
   - Princip "podijeli pa vladaj"
   - Binarno pretraživanje
   - Binarno pretraživanje po rješenju
2. **Primjeri zadataka**
   - Maksimalni zbroj podniza (D&C)
   - Pronalaženje fiksne točke
   - Agresivne krave (BS on Answer)
3. **Zadaci za vježbu**

---

# Princip "podijeli pa vladaj" (Divide & Conquer)

Moćna paradigma koja rješava problem u tri koraka:

1. **Podijeli (Divide):** Problem razbijemo na manje podprobleme istog tipa.
2. **Vladaj (Conquer):** Podprobleme riješimo rekurzivno (ili direktno ako su mali).
3. **Kombiniraj (Combine):** Rješenja podproblema spojimo u konačno rješenje.

**Primjeri:**

- **Merge Sort:** Niz podijelimo na pola, sortiramo polovice i spojimo sortirane nizove ($O(N \log N)$).
- **Binarno pretraživanje:** Specijalni slučaj u kojem rješavamo samo jedan podproblem.

---

# Binarno pretraživanje

Traženje elementa u **sortiranom** nizu.

1. **Podijeli:** Nađemo sredinu (`mid`).
2. **Vladaj:**
   - Ako je `arr[mid] == target` $\to$ kraj.
   - Ako je `arr[mid] > target` $\to$ tražimo lijevo.
   - Ako je `arr[mid] < target` $\to$ tražimo desno.
3. **Kombiniraj:** Nema (rezultat podproblema je rezultat cijelog problema).

**Složenost:** **$O(\log N)$**.
Svakim korakom odbacujemo polovicu prostora pretrage.

---

# Binarno pretraživanje korak po korak

Svaki korak usporedi srednji element s traženim i odbaci polovicu niza (sivo).

<style scoped>
.dc-bs { margin-top: 0.3em; }
.dc-bs .chips { font-size: 20px; margin-bottom: 0.4em; }
.dc-bs .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.dc-bs .chip.take { background: #9fdc9f; }
.dc-bs .chip.skip, .dc-bs .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.dc-bs .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.dc-bs .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.dc-bs .row { display: flex; gap: 6px; }
.dc-bs .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dc-bs .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.dc-bs .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.dc-bs .cell.todo .val { color: #b5b5b5; }
.dc-bs .cell.rng { background: #d6e6f5; }
.dc-bs .cell.best { background: #9fdc9f; }
.dc-bs .cell.src { background: #f5db7e; }
.dc-bs .cell.cur { background: var(--main); color: #fff; }
.dc-bs .cell.cur .idx, .dc-bs .cell.cur .val { color: #fff; }
.dc-bs .rows .row { margin-bottom: 6px; }
.dc-bs .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.dc-bs .prow { margin-top: -4px; }
.dc-bs .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.dc-bs .cell.dim { opacity: .3; }
.dc-bs .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.dc-bs .wrap { display: flex; gap: 28px; align-items: flex-start; }
.dc-bs .side { padding-top: 6px; }
.dc-bs .gsvg { display: block; overflow: visible; }
.dc-bs .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.dc-bs .e polygon { fill: #9a9a9a; }
.dc-bs .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.dc-bs .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.dc-bs .e.tree polygon { fill: #2f9e44; }
.dc-bs .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.dc-bs .e.off polygon { fill: #d5d5d5; }
.dc-bs .e.off .w { fill: #b5b5b5; }
.dc-bs .e.hid { opacity: 0; }
.dc-bs .e.bad line { stroke: #e03131; stroke-width: 6; }
.dc-bs .e.bad polygon { fill: #e03131; }
.dc-bs .e.on line { stroke: var(--main); stroke-width: 6; }
.dc-bs .e.on polygon { fill: var(--main); }
.dc-bs .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.dc-bs .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.dc-bs .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.dc-bs .n.c1 circle { fill: #ffd8a8; } .dc-bs .n.c2 circle { fill: #a5d8ff; } .dc-bs .n.c3 circle { fill: #b2f2bb; }
.dc-bs .n.c4 circle { fill: #fcc2d7; } .dc-bs .n.c5 circle { fill: #d0bfff; } .dc-bs .n.c6 circle { fill: #ffec99; }
.dc-bs .n.done circle { fill: #9fdc9f; }
.dc-bs .n.src circle { fill: #f5db7e; }
.dc-bs .n.cur circle { fill: var(--main); stroke: var(--main); }
.dc-bs .n.cur .id { fill: #fff; }
.dc-bs .tbl { display: grid; gap: 5px; }
.dc-bs .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.dc-bs .th.hl { background: var(--main); color: #fff; }
.dc-bs .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dc-bs .tc.none { border-color: transparent; }
.dc-bs .tc.k { background: #e3ecf6; }
.dc-bs .tc.best { background: #9fdc9f; }
.dc-bs .tc.src { background: #f5db7e; }
.dc-bs .tc.cur { background: var(--main); color: #fff; }
.dc-bs .line1, .dc-bs .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.dc-bs .line1 { margin-top: 0.5em; }
.dc-bs .line2 { font-weight: bold; }
.dc-bs .ctrl { margin-top: 0.5em; }
.dc-bs button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.dc-bs button:hover { background: var(--main); color: #fff; }
.dc-bs .hint { font-size: 16px; color: #6e6e6e; }
</style>

<div class="dc-bs" data-arr="1,3,4,7,9,11,15,18,21,25,30,34" data-t="18,10">
  <div class="rows"></div>
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
  document.querySelectorAll('.dc-bs').forEach(function (root) {
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

    var a = root.dataset.arr.split(',').map(Number), n = a.length;
    var targets = root.dataset.t.split(',').map(Number);
    var box = root.querySelector('.rows');
    var A = lrow(box, 'a', n, 0, true);
    var P = prow(box, n);
    var snaps = [];
    targets.forEach(function (t) {
      var l = 0, r = n - 1, step = 0, hd = 'Tražimo ' + t;
      snaps.push({ l: l, r: r, mid: -1, found: -1, l1: hd + ': l = 0, r = ' + (n - 1) + ' (cijeli niz)', l2: 'Prostor pretrage: ' + n + ' elemenata' });
      while (le(l, r)) {
        var mid = Math.floor((l + r) / 2), l1;
        step++;
        if (a[mid] === t) {
          snaps.push({ l: l, r: r, mid: mid, found: mid, l1: 'mid = ' + mid + ': a[mid] = ' + a[mid] + ' == ' + t + '  → pronađeno!', l2: hd + ': indeks ' + mid + ' nakon ' + step + ' koraka   ✓' });
          break;
        }
        var go = lt(t, a[mid]);
        l1 = 'mid = ' + mid + ': a[mid] = ' + a[mid] + (go ? ' veće je od ' + t + '  → tražimo lijevo, r = mid − 1 = ' + (mid - 1) : ' manje je od ' + t + '  → tražimo desno, l = mid + 1 = ' + (mid + 1));
        if (go) r = mid - 1; else l = mid + 1;
        snaps.push({ l: l, r: r, mid: mid, found: -1, l1: l1, l2: 'Prostor pretrage: ' + Math.max(0, r - l + 1) + ' elemenata' });
      }
      if (lt(r, l)) snaps.push({ l: l, r: r, mid: -1, found: -1, l1: 'l = ' + l + ' veće je od r = ' + r + ': prostor pretrage je prazan', l2: hd + ': nije u nizu (' + step + ' koraka)   ✓' });
    });
    function draw(s) {
      A.cells.forEach(function (c, k) {
        var cl = 'cell';
        if (lt(k, s.l) ? true : lt(s.r, k)) cl += ' dim';
        if (k === s.found) cl += ' best';
        else if (k === s.mid) cl += ' cur';
        setc(c, cl);
        A.vals[k].textContent = a[k];
      });
      setPtrs(P, [['l', lt(s.l, n) ? s.l : -1], ['r', le(0, s.r) ? s.r : -1], ['mid', s.mid]]);
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
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 1000); }
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

# Binarno pretraživanje u STL-u

Na sortiranom nizu ili `set`/`multiset` strukturi:

```cpp
vector<int> v = {1, 3, 3, 5, 8};

binary_search(v.begin(), v.end(), 3);   // true: postoji li 3?

auto lo = lower_bound(v.begin(), v.end(), 3); // prvi element >= 3 (indeks 1)
auto hi = upper_bound(v.begin(), v.end(), 3); // prvi element  > 3 (indeks 3)

int cnt = hi - lo;                       // broj pojavljivanja broja 3 (= 2)
```

Za `set` i `multiset` koristimo metode: `s.lower_bound(x)`, `s.upper_bound(x)`.
Sve su $O(\log N)$.

---

# Binarno pretraživanje po rješenju (BS on Answer)

Jedna od najkorisnijih tehnika u natjecateljskom programiranju.
Koristi se za **optimizacijske probleme** (minimizacija/maksimizacija).

**Ideja:**
Umjesto traženja optimalnog $X$, pitamo se:
> *"Je li moguće postići rješenje s vrijednošću $X$?"*

**Uvjet:** Problem mora biti **monoton**.

- Ako je moguće za $X$, moguće je i za sve manje od $X$ (ili veće, ovisno o problemu).
- To nam omogućuje binarnu pretragu po mogućim vrijednostima rješenja.

---

# Problem 1: Maksimalni zbroj podniza

**Zadatak:** Treba naći podniz s najvećim zbrojem.
*(Znamo Kadaneov algoritam $O(N)$, ali riješimo ovo D&C pristupom.)*

**Strategija ($O(N \log N)$):**
Maksimalni podniz se nalazi ili:

1. Potpuno u **lijevoj** polovici.
2. Potpuno u **desnoj** polovici.
3. **Prelazi preko sredine** (dio lijevo + dio desno).

Rješenje je `max(Lijevo, Desno, Crossing)`.

---

# Max Subarray Sum: podniz preko sredine

```cpp
long long maxCrossingSum(const vector<int>& arr, int l, int m, int r) {
    long long sum = 0, left_sum = LLONG_MIN;
    for (int i = m; i >= l; i--) { // Od sredine nalijevo
        sum += arr[i];
        left_sum = max(left_sum, sum);
    }

    sum = 0;
    long long right_sum = LLONG_MIN;
    for (int i = m + 1; i <= r; i++) { // Od sredine nadesno
        sum += arr[i];
        right_sum = max(right_sum, sum);
    }
    return left_sum + right_sum;
}
```

Podniz koji prelazi sredinu mora sadržavati `arr[m]` i `arr[m+1]`.

---

# Max Subarray Sum: rekurzija

```cpp
long long maxSubarraySum(const vector<int>& arr, int l, int r) {
    if (l == r) return arr[l]; // Bazni slučaj: jedan element

    int m = l + (r - l) / 2;
    return max({
        maxSubarraySum(arr, l, m),      // Lijevo
        maxSubarraySum(arr, m + 1, r),  // Desno
        maxCrossingSum(arr, l, m, r)    // Preko sredine
    });
}
```

Svaka razina rekurzije radi $O(N)$ posla, a razina ima $O(\log N)$ $\Rightarrow$ $O(N \log N)$.

---

# Podijeli pa vladaj korak po korak

Žuto: u tijeku, zeleno: vraćeno; plavo + narančasto = podniz preko sredine.

<style scoped>
.dc-max { margin-top: 0.3em; }
.dc-max .chips { font-size: 20px; margin-bottom: 0.4em; }
.dc-max .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.dc-max .chip.take { background: #9fdc9f; }
.dc-max .chip.skip, .dc-max .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.dc-max .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.dc-max .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.dc-max .row { display: flex; gap: 6px; }
.dc-max .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dc-max .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.dc-max .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.dc-max .cell.todo .val { color: #b5b5b5; }
.dc-max .cell.rng { background: #d6e6f5; }
.dc-max .cell.best { background: #9fdc9f; }
.dc-max .cell.src { background: #f5db7e; }
.dc-max .cell.cur { background: var(--main); color: #fff; }
.dc-max .cell.cur .idx, .dc-max .cell.cur .val { color: #fff; }
.dc-max .rows .row { margin-bottom: 6px; }
.dc-max .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.dc-max .prow { margin-top: -4px; }
.dc-max .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.dc-max .cell.dim { opacity: .3; }
.dc-max .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.dc-max .wrap { display: flex; gap: 28px; align-items: flex-start; }
.dc-max .side { padding-top: 6px; }
.dc-max .gsvg { display: block; overflow: visible; }
.dc-max .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.dc-max .e polygon { fill: #9a9a9a; }
.dc-max .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.dc-max .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.dc-max .e.tree polygon { fill: #2f9e44; }
.dc-max .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.dc-max .e.off polygon { fill: #d5d5d5; }
.dc-max .e.off .w { fill: #b5b5b5; }
.dc-max .e.hid { opacity: 0; }
.dc-max .e.bad line { stroke: #e03131; stroke-width: 6; }
.dc-max .e.bad polygon { fill: #e03131; }
.dc-max .e.on line { stroke: var(--main); stroke-width: 6; }
.dc-max .e.on polygon { fill: var(--main); }
.dc-max .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.dc-max .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.dc-max .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.dc-max .n.c1 circle { fill: #ffd8a8; } .dc-max .n.c2 circle { fill: #a5d8ff; } .dc-max .n.c3 circle { fill: #b2f2bb; }
.dc-max .n.c4 circle { fill: #fcc2d7; } .dc-max .n.c5 circle { fill: #d0bfff; } .dc-max .n.c6 circle { fill: #ffec99; }
.dc-max .n.done circle { fill: #9fdc9f; }
.dc-max .n.src circle { fill: #f5db7e; }
.dc-max .n.cur circle { fill: var(--main); stroke: var(--main); }
.dc-max .n.cur .id { fill: #fff; }
.dc-max .tbl { display: grid; gap: 5px; }
.dc-max .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.dc-max .th.hl { background: var(--main); color: #fff; }
.dc-max .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dc-max .tc.none { border-color: transparent; }
.dc-max .tc.k { background: #e3ecf6; }
.dc-max .tc.best { background: #9fdc9f; }
.dc-max .tc.src { background: #f5db7e; }
.dc-max .tc.cur { background: var(--main); color: #fff; }
.dc-max .line1, .dc-max .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.dc-max .line1 { margin-top: 0.5em; }
.dc-max .line2 { font-weight: bold; }
.dc-max .ctrl { margin-top: 0.5em; }
.dc-max button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.dc-max button:hover { background: var(--main); color: #fff; }
.dc-max .hint { font-size: 16px; color: #6e6e6e; }
.dc-max .sl { stroke: #9a9a9a; stroke-width: 2; }
.dc-max .sn rect, .dc-max .ac rect { fill: #fff; stroke: #141414; stroke-width: 2; transition: fill .25s; }
.dc-max .sn .rg { font-size: 13px; fill: #6e6e6e; text-anchor: middle; dominant-baseline: central; }
.dc-max .sv { font-size: 20px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; }
.dc-max .sn.full rect { fill: #9fdc9f; }
.dc-max .sn.part rect { fill: #ffec99; }
.dc-max .sn.cur rect { stroke: var(--main); stroke-width: 5; }
.dc-max .ac.in rect { stroke: var(--main); stroke-width: 3; }
.dc-max .ac.hl rect { fill: #d6e6f5; }
.dc-max .ac.hr rect { fill: #ffe0b8; }
</style>

<div class="dc-max" data-arr="2,-3,1,5,-2,3,5,-2">
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
  document.querySelectorAll('.dc-max').forEach(function (root) {
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

    var a = root.dataset.arr.split(',').map(Number), n = a.length;
    var W = 900, TN = {};
    function lay(v, l, r, d) {
      TN[v] = { l: l, r: r, d: d };
      if (l === r) TN[v].x = (l + 0.5) * W / n;
      else {
        var m = l + Math.floor((r - l) / 2);
        TN[v].m = m;
        lay(2 * v, l, m, d + 1); lay(2 * v + 1, m + 1, r, d + 1);
        TN[v].x = (TN[2 * v].x + TN[2 * v + 1].x) / 2;
      }
      TN[v].y = 26 + d * 56;
    }
    lay(1, 0, n - 1, 0);
    var depth = 0;
    Object.keys(TN).forEach(function (k) { depth = Math.max(depth, TN[k].d); });
    var AY = 26 + (depth + 1) * 56, H = AY + 24;
    var svg = sv('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, 'class': 'gsvg' }, root.querySelector('.graph'));
    var gl = sv('g', {}, svg), bw = Math.min(96, W / n - 14);
    Object.keys(TN).forEach(function (k) {
      var v = Number(k);
      if (TN[2 * v]) [2 * v, 2 * v + 1].forEach(function (c) { sv('line', { x1: TN[v].x, y1: TN[v].y + 22, x2: TN[c].x, y2: TN[c].y - 22, 'class': 'sl' }, gl); });
    });
    Object.keys(TN).forEach(function (k) {
      var t = TN[k];
      t.g = sv('g', { 'class': 'sn' }, svg);
      sv('rect', { x: t.x - bw / 2, y: t.y - 22, width: bw, height: 44, rx: 6 }, t.g);
      sv('text', { x: t.x, y: t.y - 10, 'class': 'rg' }, t.g).textContent = t.l === t.r ? '[' + t.l + ']' : '[' + t.l + ', ' + t.r + ']';
      t.val = sv('text', { x: t.x, y: t.y + 9, 'class': 'sv' }, t.g);
    });
    var AR = [];
    for (var i = 0; i !== n; i++) {
      var x = (i + 0.5) * W / n, g = sv('g', { 'class': 'ac' }, svg);
      sv('rect', { x: x - bw / 2, y: AY - 18, width: bw, height: 36, rx: 6 }, g);
      sv('text', { x: x, y: AY, 'class': 'sv' }, g).textContent = a[i];
      AR.push(g);
    }
    var cls = {}, vals = {}, snaps = [];
    function snap(cur, l1, l2, hl, hr) {
      snaps.push({ cls: Object.assign({}, cls), vals: Object.assign({}, vals), cur: cur, hl: hl || [], hr: hr || [], l1: l1, l2: l2 || '' });
    }
    function rg(l, r) { return l === r ? '[' + l + ']' : '[' + l + ', ' + r + ']'; }
    function range(p, q) { var o = []; for (var t = p; t !== q + 1; t++) o.push(t); return o; }
    snap(-1, 'Niz dijelimo na pola dok ne dođemo do jednog elementa', 'Rješenje čvora = max(lijevo, desno, preko sredine)');
    function rec(v, l, r) {
      cls[v] = 'part';
      if (l === r) {
        vals[v] = a[l]; cls[v] = 'full';
        snap(v, 'Bazni slučaj ' + rg(l, r) + ': jedan element  → ' + a[l]);
        return a[l];
      }
      var m = TN[v].m;
      snap(v, 'maxSubarraySum(' + l + ', ' + r + '): dijelimo na ' + rg(l, m) + ' i ' + rg(m + 1, r));
      var L = rec(2 * v, l, m), R = rec(2 * v + 1, m + 1, r);
      var s = 0, ls = -Infinity, li = m;
      for (var i = m; i !== l - 1; i--) { s += a[i]; if (lt(ls, s)) { ls = s; li = i; } }
      s = 0; var rs = -Infinity, ri = m + 1;
      for (var j = m + 1; j !== r + 1; j++) { s += a[j]; if (lt(rs, s)) { rs = s; ri = j; } }
      var C = ls + rs;
      cls[v] = 'part';
      snap(v, rg(l, r) + ' preko sredine: najbolje lijevo ' + rg(li, m) + ' = ' + ls + ', desno ' + rg(m + 1, ri) + ' = ' + rs + '  → ' + C,
        'Podniz preko sredine mora sadržavati a[' + m + '] i a[' + (m + 1) + ']', range(li, m), range(m + 1, ri));
      var best = Math.max(L, R, C);
      vals[v] = best; cls[v] = 'full';
      snap(v, rg(l, r) + ': max(lijevo ' + L + ', desno ' + R + ', sredina ' + C + ') = ' + best);
      return best;
    }
    var ans = rec(1, 0, n - 1);
    snap(-1, 'Svaka razina radi O(n) posla, a razina ima O(log n)  → O(n log n)', 'Najveći zbroj podniza = ' + ans + '   ✓');
    function draw(s) {
      Object.keys(TN).forEach(function (k) {
        var c = 'sn';
        if (s.cls[k]) c += ' ' + s.cls[k];
        if (Number(k) === s.cur) c += ' cur';
        setc(TN[k].g, c);
        TN[k].val.textContent = s.vals[k] === undefined ? '' : s.vals[k];
      });
      AR.forEach(function (g, k) {
        var c = 'ac';
        if (s.hl.indexOf(k) !== -1) c += ' hl';
        if (s.hr.indexOf(k) !== -1) c += ' hr';
        if (s.cur !== -1 ? (le(TN[s.cur].l, k) ? le(k, TN[s.cur].r) : false) : false) c += ' in';
        setc(g, c);
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

# Problem 2: Fiksna točka

**Zadatak:** Zadan je sortiran niz različitih cijelih brojeva (indeksi od 0). Treba naći indeks $i$ takav da je $A[i] = i$.

**Analiza:**
Definirajmo $B[i] = A[i] - i$. Tražimo $i$ takav da je $B[i] = 0$.
Kako su elementi $A$ različiti cijeli brojevi i sortirani, niz $A$ raste barem za 1 u svakom koraku.
$\implies B$ je **monotono neopadajući**.
Možemo koristiti binarno pretraživanje na $B$ (implicitno).

---

# Fiksna točka: Implementacija

```cpp
int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;

    int l = 0, r = n - 1, ans = -1;

    while (l <= r) {
        int mid = l + (r - l) / 2;

        if (a[mid] == mid) {
            ans = mid;
            break; // Našli smo!
        } else if (a[mid] > mid) {
            // Vrijednost je prevelika, rješenje mora biti lijevo
            // (indeks raste sporije od vrijednosti)
            r = mid - 1;
        } else {
            // Vrijednost je premala, rješenje mora biti desno
            l = mid + 1;
        }
    }
    cout << ans << "\n";
}
```

---

# Fiksna točka korak po korak

Donji redak je `a[i] − i`: crveno negativno, plavo pozitivno. Tražimo nulu, a smjer nam kaže predznak u `mid`.

<style scoped>
.dc-fixed { margin-top: 0.3em; }
.dc-fixed .chips { font-size: 20px; margin-bottom: 0.4em; }
.dc-fixed .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.dc-fixed .chip.take { background: #9fdc9f; }
.dc-fixed .chip.skip, .dc-fixed .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.dc-fixed .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.dc-fixed .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.dc-fixed .row { display: flex; gap: 6px; }
.dc-fixed .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dc-fixed .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.dc-fixed .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.dc-fixed .cell.todo .val { color: #b5b5b5; }
.dc-fixed .cell.rng { background: #d6e6f5; }
.dc-fixed .cell.best { background: #9fdc9f; }
.dc-fixed .cell.src { background: #f5db7e; }
.dc-fixed .cell.cur { background: var(--main); color: #fff; }
.dc-fixed .cell.cur .idx, .dc-fixed .cell.cur .val { color: #fff; }
.dc-fixed .rows .row { margin-bottom: 6px; }
.dc-fixed .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.dc-fixed .prow { margin-top: -4px; }
.dc-fixed .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.dc-fixed .cell.dim { opacity: .3; }
.dc-fixed .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.dc-fixed .wrap { display: flex; gap: 28px; align-items: flex-start; }
.dc-fixed .side { padding-top: 6px; }
.dc-fixed .gsvg { display: block; overflow: visible; }
.dc-fixed .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.dc-fixed .e polygon { fill: #9a9a9a; }
.dc-fixed .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.dc-fixed .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.dc-fixed .e.tree polygon { fill: #2f9e44; }
.dc-fixed .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.dc-fixed .e.off polygon { fill: #d5d5d5; }
.dc-fixed .e.off .w { fill: #b5b5b5; }
.dc-fixed .e.hid { opacity: 0; }
.dc-fixed .e.bad line { stroke: #e03131; stroke-width: 6; }
.dc-fixed .e.bad polygon { fill: #e03131; }
.dc-fixed .e.on line { stroke: var(--main); stroke-width: 6; }
.dc-fixed .e.on polygon { fill: var(--main); }
.dc-fixed .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.dc-fixed .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.dc-fixed .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.dc-fixed .n.c1 circle { fill: #ffd8a8; } .dc-fixed .n.c2 circle { fill: #a5d8ff; } .dc-fixed .n.c3 circle { fill: #b2f2bb; }
.dc-fixed .n.c4 circle { fill: #fcc2d7; } .dc-fixed .n.c5 circle { fill: #d0bfff; } .dc-fixed .n.c6 circle { fill: #ffec99; }
.dc-fixed .n.done circle { fill: #9fdc9f; }
.dc-fixed .n.src circle { fill: #f5db7e; }
.dc-fixed .n.cur circle { fill: var(--main); stroke: var(--main); }
.dc-fixed .n.cur .id { fill: #fff; }
.dc-fixed .tbl { display: grid; gap: 5px; }
.dc-fixed .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.dc-fixed .th.hl { background: var(--main); color: #fff; }
.dc-fixed .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dc-fixed .tc.none { border-color: transparent; }
.dc-fixed .tc.k { background: #e3ecf6; }
.dc-fixed .tc.best { background: #9fdc9f; }
.dc-fixed .tc.src { background: #f5db7e; }
.dc-fixed .tc.cur { background: var(--main); color: #fff; }
.dc-fixed .line1, .dc-fixed .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.dc-fixed .line1 { margin-top: 0.5em; }
.dc-fixed .line2 { font-weight: bold; }
.dc-fixed .ctrl { margin-top: 0.5em; }
.dc-fixed button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.dc-fixed button:hover { background: var(--main); color: #fff; }
.dc-fixed .hint { font-size: 16px; color: #6e6e6e; }
.dc-fixed .rl { width: 130px; }
.dc-fixed .cell.neg { background: #ffd6d6; }
.dc-fixed .cell.pos { background: #d6e6f5; }
</style>

<div class="dc-fixed" data-arr="-3,-1,0,2,3,4,6,9">
  <div class="rows"></div>
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
  document.querySelectorAll('.dc-fixed').forEach(function (root) {
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

    var a = root.dataset.arr.split(',').map(Number), n = a.length;
    var box = root.querySelector('.rows');
    var A = lrow(box, 'a[i]', n, 0, true);
    var B = lrow(box, 'a[i] − i', n, 0, false);
    var P = prow(box, n);
    var l = 0, r = n - 1, snaps = [{ l: l, r: r, mid: -1, found: -1, showB: false, l1: 'Tražimo i takav da je a[i] = i', l2: 'Niz je sortiran i elementi su različiti cijeli brojevi' }];
    snaps.push({ l: l, r: r, mid: -1, found: -1, showB: true, l1: 'a[i] − i nikad ne pada (a raste barem za 1 po koraku, i točno za 1)', l2: 'Tražimo nulu u monotonom nizu → binarno pretraživanje' });
    while (le(l, r)) {
      var mid = Math.floor((l + r) / 2);
      if (a[mid] === mid) { snaps.push({ l: l, r: r, mid: mid, found: mid, showB: true, l1: 'mid = ' + mid + ': a[mid] = ' + a[mid] + ' == mid  → fiksna točka!', l2: 'ans = ' + mid + '   ✓' }); break; }
      var big = lt(mid, a[mid]);
      var l1 = 'mid = ' + mid + ': a[mid] = ' + a[mid] + (big ? ' veće od mid  → desno je a[i] − i još veće, idemo lijevo' : ' manje od mid  → lijevo je a[i] − i još manje, idemo desno');
      if (big) r = mid - 1; else l = mid + 1;
      snaps.push({ l: l, r: r, mid: mid, found: -1, showB: true, l1: l1, l2: 'l = ' + l + ', r = ' + r });
    }
    if (lt(r, l)) snaps.push({ l: l, r: r, mid: -1, found: -1, showB: true, l1: 'Prostor pretrage je prazan', l2: 'ans = −1 (fiksna točka ne postoji)   ✓' });
    function draw(s) {
      for (var k = 0; k !== n; k++) {
        var out = lt(k, s.l) ? true : lt(s.r, k);
        var cl = 'cell' + (out ? ' dim' : '') + (k === s.found ? ' best' : (k === s.mid ? ' cur' : ''));
        setc(A.cells[k], cl);
        A.vals[k].textContent = a[k];
        var d = a[k] - k;
        setc(B.cells[k], s.showB ? cl + (d === 0 ? '' : (lt(d, 0) ? ' neg' : ' pos')) : 'cell todo');
        B.vals[k].textContent = s.showB ? d : '';
      }
      setPtrs(P, [['l', lt(s.l, n) ? s.l : -1], ['r', le(0, s.r) ? s.r : -1], ['mid', s.mid]]);
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
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 1000); }
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

# Problem 3: Agresivne krave (Aggressive Cows)

**Zadatak:** Imamo $N$ štala na pozicijama $x_1, \dots, x_N$ i $C$ krava.
Krave treba rasporediti u štale tako da je **minimalna udaljenost** između bilo koje dvije krave **maksimalna**.

**Pristup (BS on Answer):**
Umjesto traženja udaljenosti, pitamo se:
> *"Možemo li smjestiti $C$ krava tako da je razmak barem $D$?"*

Ako možemo s razmakom $D$, probamo veći. Ako ne možemo, probamo manji.

*Zadatak je na SPOJ-u: [AGGRCOW](https://www.spoj.com/problems/AGGRCOW/) (ulaz ima više test primjera).*

---

# Provjera rješenja (Greedy Check)

Funkcija `check(d)` vraća `true` ako možemo postaviti krave s razmakom $\ge d$.

```cpp
bool check(long long d, int c, const vector<int>& stalls) {
    int cows_placed = 1;
    int last_pos = stalls[0]; // Prvu kravu uvijek stavimo u prvu štalu

    for (size_t i = 1; i < stalls.size(); ++i) {
        if (stalls[i] - last_pos >= d) {
            cows_placed++;
            last_pos = stalls[i];
        }
    }
    return cows_placed >= c;
}
```

*Napomena: štale moraju biti sortirane!*

---

# Agresivne krave: glavna petlja

```cpp
int main() {
    int n, c; cin >> n >> c;
    vector<int> stalls(n);
    for (int i = 0; i < n; ++i) cin >> stalls[i];

    sort(stalls.begin(), stalls.end()); // Obavezno sortiranje

    long long l = 0, r = 1e9, ans = 0;

    while (l <= r) {
        long long mid = l + (r - l) / 2;

        if (check(mid, c, stalls)) {
            ans = mid;   // Ovo je moguće rješenje, spremamo ga
            l = mid + 1; // Pokušavamo naći veće
        } else {
            r = mid - 1; // Razmak je prevelik, smanjujemo
        }
    }
    cout << ans << "\n";
}
```

Složenost: $O(N \log D)$, gdje je $D$ najveća moguća udaljenost.

---

# Agresivne krave korak po korak

Binarno pretražujemo razmak `d`; za svaki `mid` pohlepna provjera smješta krave slijeva nadesno (primjer s SPOJ-a).

<style scoped>
.dc-cows { margin-top: 0.3em; }
.dc-cows .chips { font-size: 20px; margin-bottom: 0.4em; }
.dc-cows .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.dc-cows .chip.take { background: #9fdc9f; }
.dc-cows .chip.skip, .dc-cows .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.dc-cows .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.dc-cows .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.dc-cows .row { display: flex; gap: 6px; }
.dc-cows .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dc-cows .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.dc-cows .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.dc-cows .cell.todo .val { color: #b5b5b5; }
.dc-cows .cell.rng { background: #d6e6f5; }
.dc-cows .cell.best { background: #9fdc9f; }
.dc-cows .cell.src { background: #f5db7e; }
.dc-cows .cell.cur { background: var(--main); color: #fff; }
.dc-cows .cell.cur .idx, .dc-cows .cell.cur .val { color: #fff; }
.dc-cows .rows .row { margin-bottom: 6px; }
.dc-cows .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.dc-cows .prow { margin-top: -4px; }
.dc-cows .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.dc-cows .cell.dim { opacity: .3; }
.dc-cows .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.dc-cows .wrap { display: flex; gap: 28px; align-items: flex-start; }
.dc-cows .side { padding-top: 6px; }
.dc-cows .gsvg { display: block; overflow: visible; }
.dc-cows .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.dc-cows .e polygon { fill: #9a9a9a; }
.dc-cows .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.dc-cows .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.dc-cows .e.tree polygon { fill: #2f9e44; }
.dc-cows .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.dc-cows .e.off polygon { fill: #d5d5d5; }
.dc-cows .e.off .w { fill: #b5b5b5; }
.dc-cows .e.hid { opacity: 0; }
.dc-cows .e.bad line { stroke: #e03131; stroke-width: 6; }
.dc-cows .e.bad polygon { fill: #e03131; }
.dc-cows .e.on line { stroke: var(--main); stroke-width: 6; }
.dc-cows .e.on polygon { fill: var(--main); }
.dc-cows .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.dc-cows .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.dc-cows .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.dc-cows .n.c1 circle { fill: #ffd8a8; } .dc-cows .n.c2 circle { fill: #a5d8ff; } .dc-cows .n.c3 circle { fill: #b2f2bb; }
.dc-cows .n.c4 circle { fill: #fcc2d7; } .dc-cows .n.c5 circle { fill: #d0bfff; } .dc-cows .n.c6 circle { fill: #ffec99; }
.dc-cows .n.done circle { fill: #9fdc9f; }
.dc-cows .n.src circle { fill: #f5db7e; }
.dc-cows .n.cur circle { fill: var(--main); stroke: var(--main); }
.dc-cows .n.cur .id { fill: #fff; }
.dc-cows .tbl { display: grid; gap: 5px; }
.dc-cows .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.dc-cows .th.hl { background: var(--main); color: #fff; }
.dc-cows .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dc-cows .tc.none { border-color: transparent; }
.dc-cows .tc.k { background: #e3ecf6; }
.dc-cows .tc.best { background: #9fdc9f; }
.dc-cows .tc.src { background: #f5db7e; }
.dc-cows .tc.cur { background: var(--main); color: #fff; }
.dc-cows .line1, .dc-cows .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.dc-cows .line1 { margin-top: 0.5em; }
.dc-cows .line2 { font-weight: bold; }
.dc-cows .ctrl { margin-top: 0.5em; }
.dc-cows button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.dc-cows button:hover { background: var(--main); color: #fff; }
.dc-cows .hint { font-size: 16px; color: #6e6e6e; }
.dc-cows .axis { stroke: #141414; stroke-width: 2; }
.dc-cows .tick { font-size: 15px; fill: #6e6e6e; text-anchor: middle; dominant-baseline: central; }
.dc-cows .stall rect { fill: #c9a26b; stroke: #141414; stroke-width: 2; }
.dc-cows .stall .cow, .dc-cows .stall .cowt { opacity: 0; transition: opacity .25s; }
.dc-cows .stall.has .cow, .dc-cows .stall.has .cowt { opacity: 1; }
.dc-cows .cow { fill: var(--main); }
.dc-cows .cowt { fill: #fff; font-size: 16px; font-weight: bold; text-anchor: middle; dominant-baseline: central; }
.dc-cows .gap { font-size: 17px; font-weight: bold; fill: #2f9e44; text-anchor: middle; dominant-baseline: central; }
.dc-cows .cell.bad { background: #ffc9c9; }
.dc-cows .rl { width: 110px; }
.dc-cows .rows { margin-top: 0.4em; }
</style>

<div class="dc-cows" data-x="1,2,8,4,9" data-c="3">
  <div class="graph"></div>
  <div class="rows"></div>
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
  document.querySelectorAll('.dc-cows').forEach(function (root) {
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

    var xs = root.dataset.x.split(',').map(Number), C = Number(root.dataset.c), n = xs.length;
    var lo0 = Math.min.apply(null, xs), hi0 = Math.max.apply(null, xs);
    var W = 860, H = 120, X0 = 40, sc = (W - 2 * X0) / Math.max(1, hi0 - lo0 + 2);
    function px(v) { return X0 + (v - lo0 + 1) * sc; }
    var svg = sv('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, 'class': 'gsvg' }, root.querySelector('.graph'));
    sv('line', { x1: 10, y1: 80, x2: W - 10, y2: 80, 'class': 'axis' }, svg);
    for (var v = lo0 - 1; v !== hi0 + 2; v++) {
      sv('line', { x1: px(v), y1: 74, x2: px(v), y2: 86, 'class': 'axis' }, svg);
      sv('text', { x: px(v), y: 104, 'class': 'tick' }, svg).textContent = v;
    }
    var S = xs.map(function (x) {
      var g = sv('g', { 'class': 'stall' }, svg);
      sv('rect', { x: px(x) - 15, y: 62, width: 30, height: 18, rx: 3 }, g);
      sv('circle', { cx: px(x), cy: 40, r: 15, 'class': 'cow' }, g);
      sv('text', { x: px(x), y: 40, 'class': 'cowt' }, g).textContent = 'K';
      return g;
    });
    var gaps = sv('g', {}, svg);
    var R = Math.max(0, hi0 - lo0);
    var box = root.querySelector('.rows');
    var D = lrow(box, 'razmak d', R + 1, 0, false);
    var P = prow(box, R + 1);
    var sorted = xs.slice().sort(function (p, q) { return p - q; });
    var snaps = [];
    var st = [];
    for (var k = 0; k !== R + 1; k++) st.push('');
    function check(d) {
      var placed = [sorted[0]], last = sorted[0];
      for (var i = 1; i !== n; i++) if (le(d, sorted[i] - last)) { placed.push(sorted[i]); last = sorted[i]; }
      return placed;
    }
    snaps.push({ cows: [], st: st.slice(), l: -1, r: -1, mid: -1, l1: 'Štale (sortirane): ' + sorted.join(', ') + ';  krava: ' + C, l2: 'Pitamo: možemo li smjestiti ' + C + ' krave s razmakom barem d?' });
    var l = 0, r = R, ans = 0;
    snaps.push({ cows: [], st: st.slice(), l: l, r: r, mid: -1, l1: 'Moguće vrijednosti razmaka: od 0 do ' + R + ' (najveća udaljenost dviju štala)', l2: 'Ako d prolazi, prolazi i svaki manji: odgovor je monoton' });
    while (le(l, r)) {
      var mid = l + Math.floor((r - l) / 2);
      var placed = check(mid), ok = le(C, placed.length);
      st[mid] = ok ? 'best' : 'bad';
      var l1 = 'mid = ' + mid + ': pohlepno stavljamo krave u ' + placed.join(', ') + '  → ' + placed.length + (ok ? ' krava, dovoljno' : ' krava, premalo');
      var ll = l, rr = r;
      if (ok) { ans = mid; l = mid + 1; } else r = mid - 1;
      snaps.push({ cows: placed, st: st.slice(), l: ll, r: rr, mid: mid, l1: l1, l2: (ok ? 'ans = ' + mid + ', probamo veći: l = ' + l : 'Prevelik razmak, smanjujemo: r = ' + r) });
    }
    snaps.push({ cows: check(ans), st: st.slice(), l: -1, r: -1, mid: -1, l1: 'l je prešao r: pretraga je gotova', l2: 'Najveći mogući minimalni razmak = ' + ans + '   ✓' });
    function draw(s) {
      S.forEach(function (g, k) { setc(g, s.cows.indexOf(xs[k]) !== -1 ? 'stall has' : 'stall'); });
      gaps.textContent = '';
      var cs = s.cows.slice().sort(function (p, q) { return p - q; });
      for (var i = 1; lt(i, cs.length); i++) {
        sv('text', { x: (px(cs[i - 1]) + px(cs[i])) / 2, y: 22, 'class': 'gap' }, gaps).textContent = '↔ ' + (cs[i] - cs[i - 1]);
      }
      D.cells.forEach(function (c, k) {
        var cl = 'cell';
        if (s.st[k] === 'best') cl += ' best';
        if (s.st[k] === 'bad') cl += ' bad';
        if (s.l !== -1 ? (lt(k, s.l) ? true : lt(s.r, k)) : false) cl += ' dim';
        if (k === s.mid) cl += ' cur';
        setc(c, cl);
        D.vals[k].textContent = k;
      });
      setPtrs(P, s.l === -1 ? [] : [['l', s.l], ['r', s.r], ['mid', s.mid]]);
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
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 1100); }
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

# Zadaci za vježbu

**CSES Problem Set**

1. **[Sum of Two Values](https://cses.fi/problemset/task/1640):** Dva broja koja daju zbroj $X$ (sortiranje + binarno pretraživanje ili dva pokazivača).
2. **[Factory Machines](https://cses.fi/problemset/task/1620):** Minimalno vrijeme za proizvodnju $t$ proizvoda (BS on Answer).
3. **[Towers](https://cses.fi/problemset/task/1073):** Slaganje tornjeva (`upper_bound` na `multiset`).

**Codeforces**

- Pretražite tagove: `binary search`, `divide and conquer`.
- Zadaci težine 800-1200 za početak.

---

<!-- _class: title -->
# Sum of Two Values (CSES)

## Two Pointers ili Binary Search

---

# Analiza: Sum of Two Values

**Problem:**
Zadan je niz od $n$ cijelih brojeva i ciljni zbroj $x$.
Treba pronaći **indekse** dva broja čiji je zbroj točno $x$.

**Pristup 1: sortiranje + binarno pretraživanje**

1. Spremimo parove `{vrijednost, originalni_indeks}` i sortiramo ih.
2. Za svaki element $a$ tražimo $x - a$ u ostatku niza binarnim pretraživanjem.

**Pristup 2: dva pokazivača**

1. Sortiramo niz i postavimo $L=0$, $R=N-1$.
2. Ako je $A[L] + A[R] = x$, našli smo par.
3. Ako je $A[L] + A[R] < x \implies L$++, a ako je $> x \implies R$--.

Oba pristupa su $O(N \log N)$ zbog sortiranja.

---

# Implementacija: Sum of Two Values

```cpp
int n, target; cin >> n >> target;
vector<pair<int, int>> a(n);
for (int i = 0; i < n; ++i) {
    cin >> a[i].first;
    a[i].second = i + 1; // 1-based indeksiranje
}
sort(a.begin(), a.end());

int l = 0, r = n - 1;
while (l < r) {
    int sum = a[l].first + a[r].first;
    if (sum == target) {
        cout << a[l].second << " " << a[r].second << "\n";
        return 0;
    }
    if (sum < target) l++;
    else r--;
}
cout << "IMPOSSIBLE" << "\n";
```

---

<!-- _class: title -->
# Factory Machines (CSES)

## Binarno pretraživanje po rješenju

---

# Analiza: Factory Machines

**Problem:**
Imamo $n$ strojeva. Stroj $i$ treba $k_i$ sekundi za jedan proizvod.
Koliko je minimalno vremena potrebno za proizvodnju $t$ proizvoda?

**Intuicija (BS on Answer):**
Ako možemo proizvesti $t$ proizvoda u vremenu $T$, možemo i u vremenu $T+1$.
Funkcija "možemo li proizvesti" je monotona.

**Check funkcija:**
Za zadano vrijeme `time` stroj $i$ proizvede $\lfloor \text{time} / k_i \rfloor$ proizvoda.
Ukupno proizvoda $= \sum \lfloor \text{time} / k_i \rfloor$.
Pazite na overflow: čim suma dosegne $t$, prekidamo zbrajanje.

---

# Implementacija: Factory Machines

```cpp
long long n, t; cin >> n >> t;
vector<long long> k(n);
for (int i = 0; i < n; ++i) cin >> k[i];

long long l = 0, r = 1e18, ans = 1e18; // 1e18 je sigurna gornja granica

while (l <= r) {
    long long mid = l + (r - l) / 2;
    long long products = 0;
    for (long long x : k) {
        products += mid / x;
        if (products >= t) break; // Optimizacija i zaštita od overflowa
    }

    if (products >= t) {
        ans = mid;
        r = mid - 1;
    } else {
        l = mid + 1;
    }
}
cout << ans << "\n";
```

---

<!-- _class: title -->
# Towers (CSES)

## Pohlepni pristup s multisetom

---

# Analiza: Towers

**Problem:**
Kocke dolaze jedna po jedna (veličine se mogu ponavljati). Kocku veličine $X$ možemo staviti na vrh postojećeg tornja ako je vrh tog tornja **strogo veći** od $X$.
Inače započinjemo novi toranj. Treba minimizirati broj tornjeva.

**Intuicija:**
Pohlepno: kocku $X$ stavljamo na toranj čiji je vrh **najmanji mogući, ali strogo veći od $X$**.
Zašto? Čuvamo velike vrhove za velike kocke koje dolaze kasnije.
Trebamo strukturu koja podržava:

1. Pronalazak najmanjeg elementa $> X$.
2. Brisanje tog elementa i ubacivanje $X$.

Koristimo `std::multiset` i `upper_bound` (ne `lower_bound`, jer jednaku kocku ne smijemo staviti na vrh).

---

# Implementacija: Towers

```cpp
int n; cin >> n;
multiset<int> towers;

for (int i = 0; i < n; ++i) {
    int x; cin >> x;

    // upper_bound vraća iterator na prvi element strogo veći od x
    auto it = towers.upper_bound(x);

    if (it == towers.end()) {
        // Nema većeg elementa -> novi toranj
        towers.insert(x);
    } else {
        // Našli smo toranj -> mijenjamo vrh
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
.dc-towers { margin-top: 0.3em; }
.dc-towers .chips { font-size: 20px; margin-bottom: 0.4em; }
.dc-towers .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.dc-towers .chip.take { background: #9fdc9f; }
.dc-towers .chip.skip, .dc-towers .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.dc-towers .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.dc-towers .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.dc-towers .row { display: flex; gap: 6px; }
.dc-towers .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dc-towers .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.dc-towers .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.dc-towers .cell.todo .val { color: #b5b5b5; }
.dc-towers .cell.rng { background: #d6e6f5; }
.dc-towers .cell.best { background: #9fdc9f; }
.dc-towers .cell.src { background: #f5db7e; }
.dc-towers .cell.cur { background: var(--main); color: #fff; }
.dc-towers .cell.cur .idx, .dc-towers .cell.cur .val { color: #fff; }
.dc-towers .rows .row { margin-bottom: 6px; }
.dc-towers .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.dc-towers .prow { margin-top: -4px; }
.dc-towers .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.dc-towers .cell.dim { opacity: .3; }
.dc-towers .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.dc-towers .wrap { display: flex; gap: 28px; align-items: flex-start; }
.dc-towers .side { padding-top: 6px; }
.dc-towers .gsvg { display: block; overflow: visible; }
.dc-towers .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.dc-towers .e polygon { fill: #9a9a9a; }
.dc-towers .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.dc-towers .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.dc-towers .e.tree polygon { fill: #2f9e44; }
.dc-towers .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.dc-towers .e.off polygon { fill: #d5d5d5; }
.dc-towers .e.off .w { fill: #b5b5b5; }
.dc-towers .e.hid { opacity: 0; }
.dc-towers .e.bad line { stroke: #e03131; stroke-width: 6; }
.dc-towers .e.bad polygon { fill: #e03131; }
.dc-towers .e.on line { stroke: var(--main); stroke-width: 6; }
.dc-towers .e.on polygon { fill: var(--main); }
.dc-towers .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.dc-towers .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.dc-towers .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.dc-towers .n.c1 circle { fill: #ffd8a8; } .dc-towers .n.c2 circle { fill: #a5d8ff; } .dc-towers .n.c3 circle { fill: #b2f2bb; }
.dc-towers .n.c4 circle { fill: #fcc2d7; } .dc-towers .n.c5 circle { fill: #d0bfff; } .dc-towers .n.c6 circle { fill: #ffec99; }
.dc-towers .n.done circle { fill: #9fdc9f; }
.dc-towers .n.src circle { fill: #f5db7e; }
.dc-towers .n.cur circle { fill: var(--main); stroke: var(--main); }
.dc-towers .n.cur .id { fill: #fff; }
.dc-towers .tbl { display: grid; gap: 5px; }
.dc-towers .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.dc-towers .th.hl { background: var(--main); color: #fff; }
.dc-towers .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dc-towers .tc.none { border-color: transparent; }
.dc-towers .tc.k { background: #e3ecf6; }
.dc-towers .tc.best { background: #9fdc9f; }
.dc-towers .tc.src { background: #f5db7e; }
.dc-towers .tc.cur { background: var(--main); color: #fff; }
.dc-towers .line1, .dc-towers .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.dc-towers .line1 { margin-top: 0.5em; }
.dc-towers .line2 { font-weight: bold; }
.dc-towers .ctrl { margin-top: 0.5em; }
.dc-towers button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.dc-towers button:hover { background: var(--main); color: #fff; }
.dc-towers .hint { font-size: 16px; color: #6e6e6e; }
.dc-towers .rl { width: 70px; }
.dc-towers .towers { display: flex; gap: 22px; align-items: flex-end; min-height: 190px; padding: 0 10px; border-bottom: 4px solid #141414; }
.dc-towers .tower { display: flex; flex-direction: column-reverse; gap: 3px; }
.dc-towers .cube { height: 38px; line-height: 38px; font-size: 22px; font-weight: bold; }
.dc-towers .ms { align-self: flex-end; }
</style>

<div class="dc-towers" data-c="3,8,2,1,5,4,7,6,2">
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
  document.querySelectorAll('.dc-towers').forEach(function (root) {
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

<!-- _class: lead -->

# Pitanja?

Sljedeća lekcija: Uvod u dinamičko programiranje
