---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
backgroundColor: #f4f4f4
footer: "FIDIT Web & Systems Lab (WSL) - Prezentacija projekata"
style: |
  strong {
    color: #140b66;
  }
---
<!-- _class: title  -->
# Web Sys tim - Pregled projekata i zadataka

### Fakultet informatike i digitalnih tehnologija (FIDIT)

---

# Predstavljanje projekata

1. **AI4Scale** - Skalabilna platforma za AI eksperimente.
2. **FIDIT Web** - Migracija fakultetskog weba (Joomla $\rightarrow$ Wagtail).
3. **FIDIT PhD aplikacija** - Održavanje i nadogradnja produkcije.
4. **IoT nadzor** - Sustav za praćenje vremenskih uvjeta.
5. **NLP analiza medija** - Scraping i analiza HR novinskih članaka.
6. **Klasifikator mušica** - ML analiza trajektorija vinskih mušica.
7. **Drosophila Web UI** - Sustav za analizu podataka iz eksperimenata.

---

<!-- _class: title  -->
# Projekt 1: AI4Scale
### Platforma za eksperimentiranje s umjetnom inteligencijom

---

# AI4Scale - Pregled i zadaci

Obrazovna platforma (nalik *Google Colabu*) za rad s AI modelima unutar kontejnerske infrastrukture (JupyterHub, Docker/K8s).

* **Zadatak 1:** Identity Broker - Razvoj integracijskog sloja za OIDC prijavu (MS 365, LDAP) i admin sučelje.
* **Zadatak 2:** Nadzor HPC klastera - Prikupljanje i prikaz metrika opterećenja čvorova (Prometheus $\rightarrow$ UI).
* **Zadatak 3:** AI asistent - Integracija LLM chat asistenta u sučelje za pomoć pri kodu i navigaciji.
* **Zadatak 4:** Dinamično upravljanje kontejnerima - Skripte za automatsko gašenje neaktivnih ili resursno prezahtjevnih kontejnera.

---

<!-- _class: title  -->
# Projekt 2 & 3: Web aplikacije
### FIDIT Web migracija i PhD Repozitorij

---

# FIDIT Web (Joomla $\rightarrow$ Wagtail) & PhD aplikacija

**FIDIT Web Migracija:**
* **Što:** Prebacivanje službenog weba na moderni Django/Wagtail CMS.
* **Zadaci:** Inženjerska analiza baze, izrada *StreamField* blokova, pisanje ETL skripti za migraciju prljavih podataka, Frontend (React/TS), CI/CD.

**FIDIT PhD Aplikacija:**
* **Što:** Živa produkcijska aplikacija za doktorske studente.
* **Zadaci:** Rješavanje GitHub *backloga* – ispravci bugova na produkciji, implementacija novih featurea, poboljšanje UX-a. Rad kroz standardni *Feature Branch Flow* (PR $\rightarrow$ Code Review $\rightarrow$ Merge).

---

<!-- _class: title  -->
# Projekt 4: IoT nadzor eksperimenata
### Hardware, senzorika i prikupljanje podataka

---

# IoT nadzor vremenskih uvjeta

Razvoj *end-to-end* hardversko-softverskog sustava za praćenje mikroklimatskih uvjeta tijekom provođenja eksperimenata u labu.

* **Hardver:** Raspberry Pi i set senzora (temperatura, vlaga, svjetlost...).
* **Kako radi:** Senzori kontinuirano prikupljaju podatke s lokacije eksperimenta, skripte na Raspberry Piju ih formatiraju i autonomno šalju na centralni server.
* **Što se radi:**
  * Povezivanje i kalibracija senzora s Raspberry Pijem.
  * Pisanje skripti za očitavanje podataka i mrežnu komunikaciju.
  * Backend prijemnik (API) na serveru i spremanje u bazu podataka.

---

<!-- _class: title  -->
# Projekt 5: NLP analiza hrvatskih medija
### Data Engineering & Natural Language Processing

---

# Sustav za prikupljanje i analizu novinskih članaka

Autonomni *pipeline* koji kontinuirano prikuplja tekstove s hrvatskih news portala i provodi naprednu analizu teksta.

* **Prikupljanje podataka:** Razvoj autonomnih *scraperskih* skripti koje redovito dohvaćaju najnovije članke i spremaju ih u bazu podataka.
* **Procesiranje i ML:**
  * **Semantička analiza:** Razumijevanje konteksta i značenja teksta.
  * **Topic modeling:** Automatsko grupiranje članaka po temama.
  * **Trend prediction:** Prepoznavanje i predviđanje rasta popularnosti određenih ključnih riječi i tema.

---

<!-- _class: title  -->
# Projekt 6 & 7: Vinske mušice (Drosophila)
### Machine Learning i FastAPI obrada podataka

---

# Projekt 6: Klasifikacija ponašanja vinskih mušica

* **Kontekst:** Proučavanje ponašanja vinskih mušica ključno je u mnogim biološkim eksperimentima.
* **Zadatak:** Izrada modela strojnog učenja (klasifikatora) koji iz *sirovih* prostornih trajektorija kretanja (X, Y koordinate kroz vrijeme) može automatski prepoznati i detektirati jedno od karakterističnih ponašanja vinske mušice.
* **Fokus:** Data Science, obrada *time-series* podataka, treniranje ML modela.

---

# Projekt 7: Web sučelje za procesiranje podataka

Razvoj alata koji znanstvenicima olakšava analizu rezultata eksperimenata (bez potrebe za ručnim radom sa Excel/CSV datotekama).

* **Ulaz:** Korisnik *uploada* CSV datoteke sa sirovim podacima.
* **Analiza:** Sustav računa prosjek aktivnosti, prosjek spavanja i druge dogovorene metrike.
* **Trenutno stanje:** Dobar dio frontenda je postavljen, a backend je djelomično refaktoriran u **FastAPI**.
* **Što se radi:** Dovršavanje FastAPI backenda, integracija s frontendom i rješavanje aktivnih *light issues-a* na GitHubu (odlično za brzi *onboarding*!).

---

# Kako odabrati?

Kao što vidite, pokrivamo cijeli *tech* spektar:

* **Infrastruktura / DevOps:** AI4Scale, Docker, Raspberry Pi (IoT).
* **Web Backend & CMS:** FIDIT Web (Wagtail), PhD app (Django), Drosophila Web (FastAPI).
* **Frontend:** React, TS, HTML/HTMX.
* **Data Science / ML:** NLP analiza medija, Klasifikacija mušica.

*Razmislite u kojem se području želite razvijati - ne morate znati sve, cilj je učenje kroz rad na stvarnim stvarima!*

---

## Hackathoni, STEM Games i Natjecanja!

* **Podrška WSL tima:** Pružamo punu podršku (mentorstvo, pripreme, organizacija) za sudjelovanje na natjecanjima, hackathonima i odlaske na IT konferencije.
* **STEM Games:** Okupljamo ekipu za najveće regionalno natjecanje STEM studenata (*Technology Arena*).
* **Pratite IT scenu?** Sve od evenata, hackathona i natjecanja što vam se učini zgodno obavezno *shareajte* u naš Discord kanal **`📅｜konferencije-hackatoni-eventi`**.
* **Tražimo Discord Admina!** Ima li netko tko ima iskustva i želi preuzeti uređivanje našeg Discord servera (podešavanje uloga, kanala, integracija botova)? Javite se!

---

<!-- _class: title  -->
# Pitanja i komentari
