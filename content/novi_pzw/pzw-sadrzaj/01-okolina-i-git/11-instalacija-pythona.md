---
parent: Razvojna Okolina i Git
nav_order: 1
title: 1.1 Instalacija Pythona i pip-a
---

# 1.1 Instalacija Pythona i pip-a

Dobrodošli na prvi praktični korak! Prije nego što uopće napišemo ijednu liniju Django koda, moramo osigurati da imamo ispravno postavljene temelje. Najvažniji temelj je sam programski jezik na kojem Django radi – **Python**.

## Zašto nam je ovo važno?

Django je Python web framework. To znači da je sav Django kod koji ćemo pisati zapravo Python kod. Da bi naše računalo moglo razumjeti i izvršiti taj kod, potreban nam je Python interpreter.

Uz Python, automatski dolazi i **`pip`** – Pythonov upravitelj paketima (eng. *Package Installer for Python*). `pip` je alat pomoću kojeg ćemo instalirati Django, kao i sve druge biblioteke (pakete) koje će nam trebati u našim projektima.

> **Preporučena verzija:** Za ovaj tečaj, preporučujemo korištenje najnovije stabilne verzije **Pythona 3.11** ili novije. Uvijek je dobra praksa provjeriti službenu Django dokumentaciju kako biste vidjeli koje verzije Pythona podržava verzija Djanga koju planirate koristiti.

## Instalacija po operacijskim sustavima

Proces instalacije se malo razlikuje ovisno o vašem operacijskom sustavu. Slijedite upute za sustav koji koristite.

---

### 윈도우 **Windows**

Na Windowsima, najbolji način instalacije Pythona je korištenjem službenog instalera s web stranice `python.org`.

1.  **Preuzimanje instalera:**
    *   Posjetite službenu stranicu za preuzimanje Pythona: [https://www.python.org/downloads/](https://www.python.org/downloads/).
    *   Stranica bi trebala automatski prepoznati da koristite Windows i ponuditi vam najnoviju verziju za preuzimanje. Kliknite na "Download Python X.X.X".

2.  **Pokretanje instalera:**
    *   Nakon preuzimanja, pokrenite `.exe` datoteku.
    *   Pojavit će se prozor za instalaciju.

    > **NAJVAŽNIJI KORAK:** Prije nego što kliknete na `Install Now`, obavezno označite kućicu na dnu prozora koja kaže **"Add Python X.X to PATH"**. Ovo je ključno kako biste mogli pokretati Python iz komandne linije (CMD ili PowerShell) s bilo koje lokacije na računalu.

    ![Windows Python Installer PATH opcija](https://docs.python.org/3/_images/win_installer.png)

3.  **Instalacija:**
    *   Kliknite na `Install Now` i pričekajte da se instalacija završi.

---

### 🍎 **macOS**

Iako macOS dolazi s predinstaliranom verzijom Pythona, ta je verzija često zastarjela i koristi se za sistemske potrebe. **Nikada nemojte mijenjati ili brisati sistemski Python!** Umjesto toga, instalirat ćemo novu, modernu verziju.

Najlakši način za to je korištenjem **Homebrew**, upravitelja paketima za macOS.

1.  **Instalacija Homebrew (ako ga nemate):**
    *   Otvorite aplikaciju **Terminal**.
    *   Zalijepite sljedeću naredbu i pritisnite Enter:
      ```bash
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      ```
    *   Pratite upute na ekranu.

2.  **Instalacija Pythona pomoću Homebrew:**
    *   Kada je Homebrew instaliran, u Terminal unesite sljedeću naredbu:
      ```bash
      brew install python3
      ```
    *   Homebrew će automatski preuzeti i instalirati najnoviju stabilnu verziju Pythona i `pip`.

---

### 🐧 **Linux (Debian/Ubuntu)**

Većina Linux distribucija, uključujući Ubuntu i Debian, dolazi s predinstaliranim Pythonom. No, provjerit ćemo verziju i osigurati da imamo sve što nam treba.

1.  **Provjera verzije:**
    *   Otvorite Terminal i unesite:
      ```bash
      python3 --version
      ```
    *   Ako je verzija 3.8 ili novija, vjerojatno ste spremni. Ipak, preporučuje se instalacija najnovije verzije.

2.  **Ažuriranje i instalacija:**
    *   Prvo, ažurirajte listu paketa:
      ```bash
      sudo apt update
      ```
    *   Zatim instalirajte najnoviji Python 3, `pip` i `venv` (koji će nam trebati u sljedećem koraku):
      ```bash
      sudo apt install python3 python3-pip python3-venv
      ```

---

## Provjera uspješnosti instalacije (za sve sustave)

Nakon što ste završili instalaciju, vrijeme je da provjerimo je li sve prošlo kako treba.

1.  Otvorite novi prozor Terminala (ili CMD/PowerShell na Windowsima).
2.  Unesite sljedeću naredbu da provjerite verziju Pythona:
    ```bash
    # Na Windowsima možete koristiti i 'python'
    python3 --version
    ```
    Trebali biste vidjeti ispis verzije koju ste upravo instalirali, npr. `Python 3.11.5`.

3.  Zatim, provjerite verziju `pip`-a:
    ```bash
    # Na Windowsima možete koristiti i 'pip'
    pip3 --version
    ```
    Trebali biste vidjeti ispis verzije `pip`-a i lokaciju s koje se izvršava.

> **Napomena (`python` vs `python3`):** Na Linuxu i macOS-u, naredba `python` često pokreće stari, sistemski Python 2. Uvijek koristite `python3` i `pip3` kako biste bili sigurni da koristite verziju koju ste vi instalirali. Na Windowsima, naredbe su obično `python` i `pip`.

Čestitamo! Uspješno ste instalirali Python i `pip`, najvažnije alate za naš put. Spremni smo za sljedeći korak: organizaciju projekata pomoću virtualnih okruženja.