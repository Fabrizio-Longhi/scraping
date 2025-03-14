from scraper import scrape_news

URL = "https://www.pagina12.com.ar/"


if __name__ == "__main__":

    word = input ("Ingrese palabra clave: ")

    news = scrape_news(URL,word)
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