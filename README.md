# Reputacion Digital-Prueba técnica

## Extraccion de datos

Este proyecto consta de la extraccion de datos de un portal de noticias. El objetivo es que el usuario pase una palabra clave, y se realice la extraccion de las noticias que contenga esa palabra clave en el titulo o descripcion.
Se extra datos de sublinks del portal de noticias

El proyecto esta elaborado con **Python, SQLite, Docker**. Para realizar el scraping se utiliza **Playwright**

## Requisitos

- Se necesita tener instalado Docker

## Instalacion

1) **Clonar el repositorio:**

            git clone git@github.com:Fabrizio-Longhi/PruebaTecnica-ReputacionDigital.git.

            .cd scraping

2) **Dar Permisos de Ejecución al Script (Solo Linux/Mac)**

            chmod +x run_scraper.sh

3) **Ejecutar el Web Scraper**

    **En Linux/Mac**

            ./run_scraper.sh

    **En Windows (PowerShell/CMD):**

            bash run_scraper.sh

        o sino:

            docker build -t web-scraper .

            docker run --rm -it -v "%cd%\data:/app/data" web-scraper

4) **Dentro del script**

        Ingresar la palabra clave (ejemplo: milei).

5) **Eliminar base de datos**

    **En Linux/Mac:**

            rm -f ./data/noticias_pagina12.db

    **En windows:**

            del .\data\noticias_pagina12.db

## Instalacion sin docker

**Activar entorno virtual**

                source .venv/bin/activate

**Descargar requerimientos**

                pip install requirements.txt

**Ejecutar**
                python3 main.py

## Posibles mejoras

Si bien la extraccion anda bien, una posible mejora podria ser implementar concurrencia o asincronia.

La idea seria:

- En vez de extraer la informacion de una noticia a la vez, que se vayan extrayendo 6 noticias.concurrentemente.