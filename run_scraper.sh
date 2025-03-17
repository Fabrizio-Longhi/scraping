#!/bin/bash

# Crear directorio para datos si no existe
mkdir -p ./data

# Construir la imagen
docker build -t web-scraper .

# Ejecutar el contenedor
docker run --rm -it \
  -v "$(pwd)/data:/app/data" \
  web-scraper