---
title: Venv
layout: default
parent: Misc
nav_exclude: false
---

# Docker

## Osnovne naredbe

| Naredba |	Kratak Opis |
|---------|--------|
| `docker ps` |	Ispisuje sve aktivne kontejnere |
| `docker ps -a` |	Ispisuje sve kontejnere, uključujući one koji nisu aktivni |
| `docker run ` |	Stvara i pokreće novi kontejner |
| `docker start ` |	Pokreće postojeći zaustavljeni kontejner |
| `docker stop ` |	Zaustavlja aktivni kontejner |
| `docker restart ` |	Zaustavlja i pokreće kontejner |
| `docker rm ` |	Briše jedan ili više zaustavljenih kontejnera |
| `docker rm -f` | 	Silom briše aktivni kontejner |
| `docker logs ` |	Prikazuje dnevnike aktivnog kontejnera |
| `docker exec ` |	Pokreće naredbu u aktivnom kontejneru |


## Images

| Naredba |	Kratak Opis |
|---------|--------|
| `docker images` |	Prikazuje lokalne Docker slike koje su preuzete ili kreirane na računalu. |
| `docker pull` |	Preuzima Docker sliku s Docker registra (npr. Docker Hub-a) i sprema je lokalno na računalu.|
| `docker build` |	Koristi Dockerfile za kreiranje nove Docker slike. Dockerfile definira sve potrebne korake za kreiranje slike.|
| `docker tag` |	Omogućava označavanje lokalne slike s drugim imenom i/ili oznakom. |
| `docker rmi` |	Briše Docker sliku. |
| `docker save` |	Sprema Docker sliku kao TAR arhivu na lokalno računalo. |
| `docker load` |	Učitava Docker sliku u Docker iz TAR arhive spremljene na računalu. |
| `docker history` |	Prikazuje povijest izmjena i slojeva koje čine određenu Docker sliku. |
| `docker commit` |	Kreira novu Docker sliku iz postojećeg kontejnera. |
| `docker export` |	Sprema datoteke iz pokrenutog kontejnera kao TAR arhivu. |

## Netwrok

| Naredba |	Kratak Opis |
|---------|--------|
| `docker network create` | 	Kreira novu Docker mrežu. |
| `docker network ls` | 	Prikazuje dostupne Docker mreže. |
| `docker network inspect` | 	Prikazuje detalje o Docker mreži. |
| `docker network connect` | 	Povezuje Docker kontejner s određenom Docker mrežom. |
| `docker network disconnect` | 	Odspaja Docker kontejner od određene Docker mreže. |
| `docker network rm` | 	Uklanja određenu Docker mrežu. |


## Linux terminal

| Naredba |	Kratak Opis |
|---------|--------|
| `ls` |	Ispisuje sadržaj trenutnog direktorija. |
| `cd` |	Promjena trenutnog direktorija. |
| `mkdir` |	Stvara novi direktorij. |
| `rm` |	Briše datoteke i direktorije. |
| `cp` |	Kopira datoteke i direktorije. |
| `mv` |	Premješta/rename datoteke i direktorije. |
| `cat` |	Ispisuje sadržaj datoteke. |
| `chmod` |	Postavlja dozvole (permissions) za pristup datotekama i direktorijima. |