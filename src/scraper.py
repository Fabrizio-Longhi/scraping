from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from rich import print
import re
from utils import DataConverter
import random
import time 


user_agents = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.10 Mobile Safari/537.36"
]

def scrape_news(url: str, keyword: str):
    """Scrapea las noticias de la página y devuelve los detalles de las noticias que contienen la palabra clave"""

    with sync_playwright() as playwright:
        chrome = playwright.chromium           
        browser = chrome.launch(headless=True)
        

        context = browser.new_context(user_agent=random.choice(user_agents))
        page = context.new_page()

        try:
            try:
                 page.goto(url, timeout=30000)
            except PlaywrightTimeoutError:
                    print("Recibido 429, esperando antes de reintentar...")
                    time.sleep(random.uniform(10, 20))  
                    page.goto(url, timeout=30000) 
            page.wait_for_load_state("domcontentloaded", timeout=15000)
        except PlaywrightTimeoutError:
            print("Advertencia: Timeout esperando carga inicial, continuando...")


        all_links = page.locator("article.headline-card-inner h2.is-display-inline.article-title a, "
                                "div.element.title-prefix a, "
                                "div.headline-card h2.article-title a, "
                                "div.headline-suplemento h2.is-display-inline.article-title a")

        links = [
            {"url": link.get_attribute("href")}
            for link in all_links.all()
        ]

        print(f"Se encontraron {len(links)} links de noticias en la página principal")


        supplement_urls = []
        
        # Identificar URLs de suplementos
        for item in list(links):  
            url = item["url"]
            if url and re.match(r"^https://www\.pagina12\.com\.ar/suplementos(/.*)?$", url):
                supplement_urls.append(url)
                links.remove(item)  
        
        # Extraer links de los suplementos 
        if supplement_urls:
            for supplement_url in supplement_urls:
                print(f"Procesando suplemento: {supplement_url}")
                extract_supplement_links(page, supplement_url, links)
        
        print(f"Total de links después de procesar suplementos: {len(links)}")

        details_news = []
        i = 1

        for item in links:
            url = item["url"]
            print(f"Procesando link {i}/{len(links)}: {url}")

            if url and is_valid_news(item["url"]) and not any(d["url"] == url for d in details_news):
                try:
                    # Extraer detalles de la noticia
                    details = get_news_details(page, item["url"], keyword)  
                    if details:
                        details_news.append(details)

                    if  i%5 == 0:
                        print(f"Esperando 2 segundo antes de continuar...")
                        time.sleep(2.5)
                except Exception as e:
                    print(f"Error procesando noticia {item['url']}: {e}")
            else:
                print(f"URL no válida o duplicada: {item['url']}")
            i += 1
                
        browser.close()
        return details_news
    

def get_news_details(page, url: str, keyword: str):
    """Extrae los detalles de una noticia si tiene la palabra clave"""

    # Establecer locale en español para parsear fechas  
    DataConverter.set_spanish_locales()                              

    try:
        try:
            page.goto(url, timeout=30000)
        except PlaywrightTimeoutError:
                print("Recibido 429, esperando antes de reintentar...")
                time.sleep(random.uniform(10, 20))  
                page.goto(url, timeout=30000) 
        page.wait_for_load_state("domcontentloaded", timeout=20000)

        details = {"url": url}
        
        # Extraer título
        try:
            page.wait_for_selector('div[class="col 2-col"] h1', timeout=28000, state="attached")
            title = page.locator('div[class="col 2-col"] h1').first
            details["title"] = title.inner_text().strip() if title else "No disponible"
        except TimeoutError as e:
            print(f"Error en titulo: {e}")
            details["title"] = "No disponible"

        # Extraer descripción
        try:
            page.wait_for_selector('h2.h3.ff-20px-w400', timeout=35000, state="attached")
            headline = page.locator('h2.h3.ff-20px-w400').first
            details["headline"] = headline.inner_text().strip() if headline else "No disponible"
        except TimeoutError:
            details["headline"] = "No disponible"
        
        if keyword:
            title_contains_keyword = contains_exact_word(details["title"], keyword)
            headline_contains_keyword = contains_exact_word(details["headline"], keyword)
            if not title_contains_keyword and not headline_contains_keyword:
                return None
            else:
                found = []
                if title_contains_keyword:
                    found.append("título")
                if headline_contains_keyword:
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

    print("-"*238)
    return details


def is_valid_news(url: str) -> bool:
    """Verifica si una URL es una noticia válida"""
    pattern = r"https://www.pagina12.com.ar/\d+.*"
    return bool(re.match(pattern, url))    



def contains_exact_word(text: str, word: str) -> bool:
    """Verifica si la palabra aparece como una palabra completa en el texto."""
    pattern = rf"\b{re.escape(word)}\b"                       
    return bool(re.search(pattern, text, re.IGNORECASE))      



def extract_supplement_links(page, supplement_url: str, links: list):
    """Extrae enlaces de noticias de un suplemento usando la página existente"""
    try:
        page.goto(supplement_url, timeout=30000) 
        page.wait_for_load_state("domcontentloaded", timeout=15000)
    except PlaywrightTimeoutError:
        print(f"Advertencia: Timeout esperando carga de suplemento {supplement_url}, continuando...")
    
  
    
    new_links = page.locator("div.article-box__container h2 a")
    print(f"{new_links.count()} enlaces encontrados en total")
    
    found_links = 0
    num_links = new_links.count()
    try:
        for i in range(num_links):
            try:
                link = new_links.nth(i)         
                url = link.get_attribute("href")
                
                # Convertir a URL absoluta si es relativa
                if url and not url.startswith("http"):
                    url = f"https://www.pagina12.com.ar{url}"
                
                if url and is_valid_news(url) and not any(d["url"] == url for d in links):
                    links.append({"url": url})
                    found_links += 1
                    print(f"Enlace extraído del suplemento: {url}")
            except Exception as e:
                print(f"Error extrayendo enlace específico: {e}")
    except Exception as e:
            print(f"Error con selector {new_links}: {e}")
    
    print(f"Se encontraron {found_links} nuevos links en el suplemento {supplement_url}")