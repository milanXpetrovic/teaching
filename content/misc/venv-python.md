---
title: Venv
layout: default
parent: Misc
nav_exclude: false
---

Install the pip:

```python
sudo apt-get install python-pip
```

Install the virtual environment:

```python
sudo pip install virtualenv
```

Store your virtual environments somewhere:

```python
mkdir ~/.storevirtualenvs
```

Now you should be able to create a new virtualenv

```python
virtualenv -p python3 yourVenv
```

To activate:

```python
source yourVenv/bin/activate
```

To exit your new virtualenv, just `deactivate`
