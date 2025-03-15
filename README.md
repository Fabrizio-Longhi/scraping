# PruebaTecnica-ReputacionDigital

## Extraccion de datos

Este proyecto consta de la extraccion noticas de un sitio web de noticias. El objetivo es que el usuario pase una palabra clave, y se realice la extraccion de las noticias qud contenga esa palabra clave en el titulo o descripcion.

El proyecto esta elaborado con **Python, SQLite, Docker y Docker compose**. Para realizar el scraping se utiliza **Playwright**

## Requisitos

- Se necesita tener instalado Docker y Docker compose

## Instalacion

### Clonar repositorio

$ git clone git@github.com:Fabrizio-Longhi/PruebaTecnica-ReputacionDigital.git.

### Montar docker

$ docker-compose build

### Correr docker

$ docker-compose run scraper

### Dentro del script

Ingresar la palabra clave.

### Eliminar base de datos

$ docker-compose run scraper /bin/bash

$ rm /app/data/noticias_pagina12.db

$ exit