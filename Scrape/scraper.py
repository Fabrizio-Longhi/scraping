from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from rich import print
from datetime import datetime
import re
from utils import DataConverter


def scrape_news(url: str, keyword: str):
    """Scrapea las noticias de la página y devuelve los detalles de las noticias que contienen la palabra clave"""

    with sync_playwright() as playwright:
        chrome = playwright.chromium            # Usar Chromium para mayor compatibilidad
        browser = chrome.launch(headless=True)  # Ejecutar en headless True para mayor velocidad
        context = browser.new_context()         # Crear un nuevo contexto de navegación
        page = context.new_page()               # Crear una nueva página

        try:
            page.goto(url, timeout=30000)       # Navegar a la URL
            page.wait_for_load_state("domcontentloaded", timeout=15000)     # Esperar a que cargue la página
        except PlaywrightTimeoutError:
            print("Advertencia: Timeout esperando carga inicial, continuando...")

        all_links = page.locator("h2.is-display-inline.article-title a")
        links = [
            {"url": link.get_attribute("href")}
            for link in all_links.all()
        ]
        
        print(f"Se encontraron {len(links)} links de noticias")

        details_news = []
        for item in links:
            url = item["url"]
            if url and is_valid_news(item["url"]):
                try:
                    details = get_news_details(page, item["url"], keyword)

                    if details:
                        details_news.append(details)
                except Exception as e:
                    print(f"Error procesando noticia {item['url']}: {e}")
            else:
                print(f"URL no válida: {item['url']}")
                
        browser.close()
        return details_news
    

def is_valid_news(url: str) -> bool:
    """Verifica si una URL es una noticia válida"""
    pattern = r"https://www.pagina12.com.ar/\d+.*"
    return bool(re.match(pattern, url))    



def get_news_details(page, url: str, keyword: str):
    """Extrae los detalles de una noticia si tiene la palabra clave"""
    print(f"Extrayendo detalles de la noticia: {url}")
    
    DataConverter.set_spanish_locales()           # Establecer locale en español para parsear fechas          

    try:
        page.goto(url, timeout=20000)
        page.wait_for_load_state("domcontentloaded", timeout=10000)

        details = {"url": url}

        # Extraer título
        title = page.locator('div[class="col 2-col"] h1').first
        details["title"] = title.inner_text().strip() if title.count() > 0 else "No disponible"

        # Descripción de la noticia
        description = page.locator("h2.h3.ff-20px-w400").first
        details["headline"] = description.inner_text().strip() if description.count() > 0 else "No disponible"
        
        if keyword:
            keyword_lower= keyword.lower()
            title_lower = details["title"].lower()
            headline_lower = details["headline"].lower()

            if keyword_lower not in title_lower and keyword_lower not in headline_lower:
                return None
            else:
                found = []
                if keyword_lower in title_lower:
                    found.append("título")
                if keyword_lower in headline_lower:
                    found.append("descripción")

                print(f"La noticia '{url}' contiene la palabra clave '{keyword}' en: {', '.join(found)}")
        
        # Extraer autor
        author = page.locator("div.author-name.ff-14px-w800").first
        details["author"] = author.inner_text().strip() if author.count() > 0 else "No disponible"

        # Extraer fecha
        date_element = page.locator("div.date.modification-date.ff-14px time").first
        if date_element.count() > 0:
            date_text = date_element.inner_text().strip()
            date_text = re.sub(r"\s+", " ", date_text).strip()                                      # Remover espacios duplicados

            details["date"] = DataConverter.convert_to_iso8601(date_text)                         # Convertir fecha a ISO 8601

        else:
            details["date"] = "No disponible"

        # URL de imagen principal
        image = page.locator(".article-main-media-image__container picture source").first.get_attribute("srcset")
        if not image:
            image = page.locator("picture img").first.get_attribute("src")
        details["image_url"] = image if image else "No disponible"


    except Exception as e:
        print(f"Error en get_news_details: {e}")
        details["error"] = str(e)

        if keyword:
            return None

    return details