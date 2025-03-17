FROM python:3.10

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar locales y configurar el locale en español
RUN apt-get update && apt-get install -y locales \
    && sed -i '/es_ES.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen es_ES.UTF-8 \
    && update-locale LANG=es_ES.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# Configurar el locale por defecto
ENV LANG es_ES.UTF-8
ENV LC_ALL es_ES.UTF-8

# Instalar las dependencias del sistema para Playwright
RUN apt-get update && apt-get install -y \
    wget \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y \
    google-chrome-stable \
    fonts-ipafont-gothic \
    fonts-wqy-zenhei \
    fonts-thai-tlwg \
    fonts-kacst \
    fonts-freefont-ttf \
    libxss1 \
    libgconf-2-4 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    libxi6 \
    libxtst6 \
    && rm -rf /var/lib/apt/lists/*

# Copiar los archivos necesarios
COPY requirements.txt .
COPY src/ ./src/

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar los binarios de Playwright y sus dependencias
RUN playwright install --with-deps

# Crear el directorio para la base de datos
RUN mkdir -p /app/data

# Volumen para persistir los datos
VOLUME /app/data

# Configurar el script para usar la base de datos en el volumen
ENV DB_PATH=/app/data/noticias_pagina12.db

# Comando para ejecutar el script
ENTRYPOINT ["python", "src/main.py"]