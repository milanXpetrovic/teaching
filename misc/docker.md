---
nav_exclude: true
---

# Docker


`docker --help`: Prikazuje popis svih dostupnih naredbi za Docker i kratki opis svake naredbe.

```console
docker --help
```

`docker info`: Prikazuje informacije o Docker instalaciji, uključujući verziju, broj kontejnera i slika, te podatke o korištenju memorije i procesora.

```console
docker info
```

`docker ps`: Prikazuje aktivne Docker kontejnere.

```console
docker ps
```

`docker images`: Prikazuje lokalne Docker slike koje su preuzete ili kreirane na računalu.

```console
docker images
```

`docker start|stop`: Pokreće ili zaustavlja pokrenuti Docker kontejner.

```console
docker stop id-kontejnera
```

`docker rm`: Briše Docker kontejner.

```console
docker rm id-kontejnera
```

`docker rmi`: Briše Docker sliku.

```console
docker rmi ime-slike
```



`docker pull`: Preuzima Docker sliku s Docker registra (npr. Docker Hub-a) i sprema je lokalno na računalu.

```console
docker pull ime-slike
```


`docker build`: Koristi Dockerfile za kreiranje nove Docker slike. Dockerfile definira sve potrebne korake za kreiranje slike.

```console
docker build -t ime-slike putanja/do/Dockerfile
```


`docker run`: Pokreće novi Docker kontejner iz određene Docker slike.

```console
docker run ime-slike
```

`docker run --name <container_name> <image_name>`: Pokreće novi kontejner iz Docker slike, s prilagođenim imenom.

```console
docker run --name moj-kontejner ubuntu:latest
```

`docker run -p <host_port>:<container_port> <image_name>`: Pokreće novi kontejner iz Docker slike, povezujući portove hosta s portovima kontejnera.

```console
docker run -p 80:80 ubuntu:latest
```



`docker exec`: Pokreće novi proces u postojećem Docker kontejneru.

```console
docker exec id-kontejnera naredba
```

`docker image prune`: Uklanja sve neiskorištene Docker slike.

```console
docker image prune
```


