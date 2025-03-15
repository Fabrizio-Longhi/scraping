from scraper import scrape_news
from storage import NewsStorage
import time
import os
from config import URL_base, check_robots

URL = URL_base


if __name__ == "__main__":

    # Verificar archivo robots.txt
    check_robots(URL)

    # Inicializar base de datos
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "noticias_pagina12.db")
    storage = NewsStorage(db_path)
    
    init = time.time()
    print(f"Iniciando scraping de {URL}...")
    
    word = input("Ingrese la palabra que desea buscar: ")
    
    # Realizar scraping
    news = scrape_news(URL,word)
    
    end = time.time()
    tiempo_total = end - init
    
    # Mostrar resultados
    print("\n--- RESULTADOS FINALES ---")
    for i, item in enumerate(news):
        print(f"\nNoticia {i+1}:")
        print(f"Título: {item.get('title', 'No disponible')}")
        print(f"URL: {item.get('url', 'No disponible')}")
        print(f"Autor: {item.get('author', 'No disponible')}")
        print(f"Fecha: {item.get('date', 'No disponible')}")
        print(f"Imagen Principal: {item.get('image_url', 'No disponible')}")
        print(f"Descripción: {item.get('headline', 'No disponible')}")
        print("-" * 50)
    
    # Guardar noticias en la base de datos
    total, nuevas = storage.save_news(news)
    
    
    # Mostrar estadísticas
    print(f"\n--- ESTADÍSTICAS DE ALMACENAMIENTO ---")
    print(f"Total de noticias procesadas: {total}")
    print(f"Noticias nuevas guardadas: {nuevas}")
    print(f"Tiempo total de ejecución: {tiempo_total:.2f} segundos")
    

    
    # Cerrar conexión a la base de datos
    storage.close()