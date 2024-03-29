---
parent: PZW
nav_order: 1
nav_exclude: false
title: CRUD
---

# Operacije nad bazom podataka (CRUD)

U nastavku su prikazani koraci implementacije sustav za upravljanje podacima o različitim vrstama sladoleda koristeći osnovne operacije CRUD (Create, Read, Update, Delete). Ovaj zadatak će zahtijevati da implementirate osnovne funkcije za upravljanje podacima o sladoledu, omogućujući korisnicima dodavanje novih unosa, pregled postojećih, ažuriranje informacija i brisanje unosa koji nisu potrebni. Ovo bi vam omogućilo bolje razumijevanje i primjenu CRUD operacija u konkretnom kontekstu razvoja aplikacija.

- Osigurajte da svaka operacija (stvaranje, čitanje, ažuriranje, brisanje) bude jasno implementirana i testirana.
- Napravite sučelje koje omogućuje korisnicima lako upravljanje podacima o sladoledu.
- Uvjerite se da su osnovni podaci o sladoledu dobro strukturirani kako bi omogućili jednostavno upravljanje.

## Create

Implementirati pogled i obrazac kako bi se omogućilo stvaranje novih unosa sladoleda.

**models.py**

Stvorite model za sladoled s poljima kao što su okus, opis i cijena.

```python
class IceCream(models.Model):
    name = models.CharField(max_length=50)
    flavor = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    expiration_date = models.DateField()
    
    def __str__(self):
        return self.name

```

**forms.py**

Dizajnirajte obrazac pomoću Django-ovog modula za obrasce za unos podataka o sladoledu.

```python
from django import forms
from .models import IceCream

class IceCreamForm(forms.ModelForm):
    class Meta:
        model = IceCream
        fields = ['name', 'flavor', 'description', 'price', 'expiration_date']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'})
        }

```

**views.py**

Napravite pogled za prikaz obrasca i obradu podnošenja obrasca. Nakon podnošenja, provjerite valjanost i spremite novi unos sladoleda u bazu podataka.

```python
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import IceCream
from .forms import IceCreamForm

class IceCreamCreateView(CreateView):
    model = IceCream
    form_class = IceCreamForm
    template_name = 'add_icecream.html'
    success_url = reverse_lazy('icecream:list')
```

**views.py za početnu stranicu**

```python
from django.views import View
from django.shortcuts import render

class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'landing.html')

def landing_page(request):
    return render(request, 'landing.html')
```

**urls.py**

```python
from django.urls import path
from . import views

app_name = 'icecream'

urlpatterns = [
    path('', views.icecream_landing, name='landing'),
    path('add/', views.IceCreamCreateView.as_view(), name='add'),
    path('list/', views.IceCreamListView.as_view(), name='list'),
    path('update/', views.IceCreamUpdateView.as_view(), name='update'),
    path('delete/', views.IceCreamDeleteView.as_view(), name='delete'),
]

```

### HTML predlošci

- Stvorite pogled koji će prikazati početnu stranicu aplikacije (`landing.html`)
- Dizajnirajte HTML predložak pod nazivom `add_icecream.html` koji će omogućiti dodavanje novih detalja o sladoledu.
- Povežite stvoreni predložak s pogledom kako bi se mogao prikazati kada korisnik pristupi početnoj stranici aplikacije.

**landing.html**

```text
{% raw %}
<!DOCTYPE html>
<html>
<head>
    <title>Ice Cream CRUD Operations</title>
</head>
<body>
    <h1>Welcome to Ice Cream CRUD Operations</h1>
    <ul>
        <li><a href="{% url 'icecream:add' %}">Add Ice Cream</a></li>
        <li><a href="{% url 'icecream:list' %}">List Ice Creams</a></li>
    </ul>
</body>
</html>
{% endraw %}
```

**add_icecream.html**

```text
{% raw %}
<!DOCTYPE html>
<html>
<head>
    <title>Add Ice Cream</title>
</head>
<body>
    <h1>Add New Ice Cream</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Add Ice Cream</button>
    </form>
</body>
</html>
{% endraw %}s
```

## Read

Stvoriti prikaz za dohvaćanje svih unosa sladoleda iz baze podataka.

**views.py**

```python
from django.views.generic import ListView
from .models import IceCream

class IceCreamListView(ListView):
    model = IceCream
    template_name = 'icecream/list_icecreams.html'
    context_object_name = 'icecreams'
```

**list_icecreams.html**

```text
{% raw %}
<!DOCTYPE html>
<html>
<head>
    <title>List Ice Creams</title>
</head>
<body>
    <h1>List of Ice Creams</h1>
    <h2><a href="{% url 'icecream:landing' %}">Landing</a></h2>
    <ul>
        {% for icecream in icecreams %}
            <li>{{ icecream.flavor }} - Price: ${{ icecream.price }}</li>
            <p>Description: {{ icecream.description }}</p>
            <p>Expires on: {{ icecream.expiration_date }}</p>
        {% empty %}
            <li>No ice creams available</li>
        {% endfor %}
    </ul>
</body>
</html>
{% endraw %}
```

## Update

Uređivanje postojećih detalja o sladoledu.

**views.py**

```python
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import IceCream
from .forms import IceCreamForm

class IceCreamUpdateView(UpdateView):
    model = IceCream
    form_class = IceCreamForm
    template_name = 'update_icecream.html'
    success_url = reverse_lazy('icecream:list')

```

**update_icecream.html**

```text
{% raw %}
<!DOCTYPE html>
<html>
<head>
    <title>Update Ice Cream</title>
</head>
<body>
    <h1>Update Ice Cream</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Update Ice Cream</button>
    </form>
</body>
</html>
{% endraw %}
```

**landing.html**

```text
{% raw %}
<!DOCTYPE html>
<html>
<head>
    <title>List Ice Creams</title>
</head>
<body>
    <h1>List of Ice Creams</h1>
    <h2><a href="{% url 'icecream:landing' %}">Landing</a></h2>
    <ul>
        {% for ice in icecreams %}
            <li>{{ ice.flavor }} - Price: ${{ ice.price }}</li>
            <a href="{% url 'icecream:update' ice.pk %}">Update</a>
            
            <p>Description: {{ ice.description }}</p>
            <p>Expires on: {{ ice.expiration_date }}</p>
        {% empty %}
            <li>No ice creams available</li>
        {% endfor %}
    </ul>
</body>
</html>
{% endraw %}
```

## Delete

Brisanje postojećih sladoleda iz baze.

**views.py**

```python
class IceCreamDeleteView(DeleteView):
    model = IceCream
    template_name = 'delete_icecream.html'
    success_url = reverse_lazy('icecream:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icecream'] = self.get_object()
        return context

```

**delete_icecream.html**

```text
{% raw %}
<!DOCTYPE html>
<html>
<head>
    <title>Delete Ice Cream</title>
</head>
<body>
    <h1>Delete Ice Cream</h1>
    <p>Are you sure you want to delete "{{ icecream.flavor }}"?</p>
    <form method="post">
        {% csrf_token %}
        <input type="submit" value="Confirm Delete">
    </form>
</body>
</html>
{% endraw %}
```

**landing.html**

```text
{% raw %}
<!DOCTYPE html>
<html>
<head>
    <title>List Ice Creams</title>
</head>
<body>
    <h1>List of Ice Creams</h1>
    <ul>
        {% for icecream in icecreams %}
            <li>
                {{ icecream.flavor }} - Price: ${{ icecream.price }}
                <a href="{% url 'icecream:update' ice.pk %}">Update</a>
                <a href="{% url 'icecream:delete' ice.pk %}">Delete</a>
            </li>
            <p>Description: {{ icecream.description }}</p>
            <p>Expires on: {{ icecream.expiration_date }}</p>
        {% empty %}
            <li>No ice creams available</li>
        {% endfor %}
    </ul>
</body>
</html>
{% endraw %}
```
