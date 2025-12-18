---
marp: true
theme: beam
size: 16:9
paginate: true
math: mathjax
header: "NASLOV"
footer: "IME_PREDMETA"
style: |
  section {
    font-size: 24px;
  }
  code {
    font-size: 18px; /* Optimizes code readability */
  }
  h1 {
    font-size: 40px;
    color: #005f87;
  }
  h2 {
    font-size: 32px;
    color: #005f87;
  }
  section::after {
    content: attr(data-marpit-pagination) ' / ' attr(data-marpit-pagination-total);
    font-weight: bold;
    font-size: 20px;
    color: #005f87;
    position: absolute;
    bottom: 25px; 
    right: 30px;
    z-index: 999; /* Osigurava da je broj IZNAD footera */
  }
---
<!-- paginate: false -->
<!-- _class: title  -->
# Naslov

IME_PREDMETA

---

<!-- paginate: true -->
## Slide sa slikom

**Opis slike**
![w:800px center](/path/to/imgage)
Izvor: [text](link)

---

# Prezentacija u pdf

```bash
marp file.md --html --theme-set beam.css --allow-local-files
```

---
