
# Extraccion de datos

Este proyecto consta de la extraccion de datos de un portal de noticias. El objetivo es que el usuario pase una palabra clave, y se realice la extraccion de las noticias que contenga esa palabra clave en el titulo o descripcion.

El proyecto esta elaborado con **Python, SQLite, Docker y Docker compose**. Para realizar el scraping se utiliza **Playwright**

## Requisitos

- Se necesita tener instalado Docker y Docker compose

## Instalacion

### Clonar repositorio

$ git clone git@github.com:Fabrizio-Longhi/PruebaTecnica-ReputacionDigital.git.

$ cd scraping

### Dar Permisos de Ejecución al Script (Solo Linux/Mac)


$ chmod +x run_scraper.sh

### Ejecutar el Web Scraper

#### En Linux/Mac

$ ./run_scraper.sh

#### En Windows (PowerShell/CMD):

$ bash run_scraper.sh

o sino:

docker build -t web-scraper .

docker run --rm -it -v "%cd%\data:/app/data" web-scraper

#### Dentro del script

Ingresar la palabra clave.

### Eliminar base de datos

#### En Linux/Mac:

$ rm -f ./data/noticias_pagina12.db

#### En windows:

$ del .\data\noticias_pagina12.db