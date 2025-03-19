# Define configuraciones como User-Agent, URL base, headers, etc
import requests


URL_base = "https://www.pagina12.com.ar/"

def check_robots(url: str):
    robots_url = url.rstrip("/") + "/robots.txt"
    response = requests.get(robots_url)
    if response.status_code == 200:
        print("El archivo robots.txt tiene las siguientes reglas:")
        print(response.text)
    else:
        print("No se encontró el archivo robots.txt")



