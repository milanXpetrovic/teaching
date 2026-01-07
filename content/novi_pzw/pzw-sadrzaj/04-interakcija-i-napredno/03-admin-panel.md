---
parent: 'Interakcija s Korisnikom i Napredne Teme'
nav_order: 3
has_children: false
title: 'Poglavlje 8: Admin Panel i Prilagodbe'
---

# Poglavlje 8: Admin Panel i Prilagodbe

Jedna od najpoznatijih i najmoćnijih značajki Djanga je njegovo automatski generirano **admin sučelje**. To je gotova web aplikacija koja vam omogućuje da vi, kao administrator stranice, upravljate podacima bez potrebe za pisanjem dodatnog koda.

Možete ga zamisliti kao moćan, siguran i prilagodljiv alat za direktnu manipulaciju podacima u vašoj bazi, ali kroz prijateljsko web sučelje.

> **Za koga je Admin?**
>
> Kako i "Two Scoops of Django" naglašava, važno je zapamtiti: Django Admin je namijenjen **administratorima i internom timu** (eng. *staff*), a **NE krajnjim korisnicima** vaše stranice. Iako ga je moguće u potpunosti redizajnirati, on primarno služi kao alat za brzo i efikasno upravljanje sadržajem "iza kulisa".

## 8.1 Registracija Modela u Admin Panelu

Da bi se vaši modeli uopće pojavili u admin sučelju, morate ih eksplicitno **registrirati**.

Recimo da imamo naš `Post` model iz prethodnih poglavlja.

1. **Otvorite `posts/admin.py`:** Svaka Django aplikacija ima ovu datoteku, koja je stvorena upravo za tu namjenu.
2. **Importajte model i registrirajte ga:** Postoje dva načina za to.

    * **Jednostavna registracija (bez prilagodbi):**
        Ovo je najbrži način. Jednostavno recite adminu da prikaže vaš model sa zadanim postavkama.

            # posts/admin.py
            from django.contrib import admin
            from .models import Post

            admin.site.register(Post)

    * **Registracija pomoću dekoratora (preporučeni način za prilagodbe):**
        Ovaj način je bolji jer nam omogućuje da odmah počnemo s prilagodbama, o čemu ćemo više u sljedećem odjeljku.

            # posts/admin.py
            from django.contrib import admin
            from .models import Post

            @admin.register(Post)
            class PostAdmin(admin.ModelAdmin):
                pass

        Ovdje kreiramo `ModelAdmin` klasu koja će sadržavati svu konfiguraciju za prikaz `Post` modela, a `@admin.register(Post)` dekorator radi istu stvar kao i `admin.site.register()`.

3. **Provjerite rezultat:**
    Pokrenite server (`python manage.py runserver`), prijavite se u admin sučelje (`/admin/`) sa svojim superuser računom i vidjet ćete novu sekciju "Posts" s linkom na vaš `Post` model. Sada možete kliknuti na njega i dodavati, mijenjati ili brisati postove putem grafičkog sučelja!

---

## 8.2 Prilagodba Admin Panela

Zadani prikaz je funkcionalan, ali često nije dovoljan. Želimo prilagoditi kako se podaci prikazuju, pretražuju i filtriraju. Sve to radimo unutar naše `ModelAdmin` klase.

### `list_display`: Prilagodba prikaza liste

Kada uđete u listu postova, vidite samo "čitljivi" prikaz svakog objekta (ono što vraća `__str__` metoda). `list_display` nam omogućuje da prikažemo više polja kao stupce u tablici.

    # posts/admin.py
    @admin.register(Post)
    class PostAdmin(admin.ModelAdmin):
        list_display = ('title', 'author', 'date_posted', 'was_published_recently')
        
        # Možemo dodati i vlastite "izračunate" metode
        def was_published_recently(self, obj):
            # ... neka logika koja vraća True/False
            return True
        was_published_recently.boolean = True # Prikazuje lijepu ikonicu

### `list_filter`: Filtriranje podataka

Ako imate stotine postova, filtriranje postaje nužno. `list_filter` dodaje bočnu traku s opcijama za filtriranje.

    # posts/admin.py
    @admin.register(Post)
    class PostAdmin(admin.ModelAdmin):
        list_display = ('title', 'author', 'date_posted')
        list_filter = ('date_posted', 'author')

Sada ćete s desne strane imati linkove za filtriranje postova po datumu (Danas, Prošlih 7 dana, Ovaj mjesec...) i po autoru.

### `search_fields`: Dodavanje pretrage

Za pretragu po tekstualnim poljima, koristimo `search_fields`.

    # posts/admin.py
    @admin.register(Post)
    class PostAdmin(admin.ModelAdmin):
        # ... (prethodne opcije)
        search_fields = ['title', 'content']

Ovo će na vrhu liste dodati polje za pretragu koje će pretraživati naslove i sadržaj vaših postova.

### Prilagodba forme za uređivanje: `fields` i `fieldsets`

Možemo kontrolirati i kako izgleda forma za dodavanje ili uređivanje pojedinog posta.

* **`fields`:** Jednostavno navođenje polja i njihovog redoslijeda.

        class PostAdmin(admin.ModelAdmin):
            fields = ('author', 'title', 'content')

* **`fieldsets`:** Omogućuje grupiranje polja u logičke cjeline s naslovima, što je puno preglednije za kompleksne modele.

        class PostAdmin(admin.ModelAdmin):
            fieldsets = (
                (None, {
                    'fields': ('title', 'content')
                }),
                ('Meta podaci', {
                    'fields': ('author', 'date_posted'),
                    'classes': ('collapse',)  # Ovaj odjeljak će biti skriven po defaultu
                }),
            )

### Povezani Modeli: `inlines`

Što ako imamo model `Comment` koji je `ForeignKey` vezom povezan s `Post` modelom? Bilo bi jako korisno da možemo uređivati komentare direktno na stranici za uređivanje posta. Za to služe **inlines**.

1. **Definiramo inline klasu:**

        # posts/admin.py
        from .models import Comment

        class CommentInline(admin.TabularInline): # Može biti i StackedInline za drugačiji prikaz
            model = Comment
            extra = 1 # Koliko praznih formi za unos novih komentara prikazati

2. **Dodamo je u `PostAdmin`:**

        @admin.register(Post)
        class PostAdmin(admin.ModelAdmin):
            # ...
            inlines = [CommentInline]

Sada, kada uređujete post, ispod glavne forme vidjet ćete tablicu s postojećim komentarima i formama za unos novih.

---

Django Admin je nevjerojatno moćan alat. S ovim osnovnim tehnikama prilagodbe, možete ga pretvoriti iz jednostavnog CRUD sučelja u kompleksnu internu aplikaciju prilagođenu točno vašim potrebama, i to uz minimalnu količinu koda.

Kao što "Two Scoops of Django" savjetuje, uvijek istražite što se sve može postići unutar Admina prije nego što krenete pisati potpuno novo sučelje od nule. Često ćete otkriti da je Django već predvidio vaše potrebe.