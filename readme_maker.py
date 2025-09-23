BASE_README = """![banner](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/calypso-banner-rounded.jpg)

### CALYPSO

The *Calypso* is an oceanographic vessel equipped and used by the maritime explorer Jacques-Yves Cousteau for his scientific expeditions and documentary film productions.

Named after Calypso, the sea nymph from Greek mythology, the ship and its crew sailed the world’s seas and oceans from November 24, 1951, until January 1996. Through television and books, the *Calypso* became one of the symbols of maritime exploration and global ecology in the second half of the 20th century, in the tradition of its illustrious predecessors such as *La Boussole* and *L’Astrolabe*, the *Beagle*, the *Challenger*, the *Pourquoi Pas?*, and the *Hirondelle*.

## Description

**Calypso** is not only the name of a famous exploration vessel: it’s also a Python library for **web scraping**.  
Unlike general-purpose tools such as HTTrack, which download an entire site before extracting data, Calypso is designed to be **fast and targeted**. It only retrieves the information you need, in an optimized way.  
If the website you want to scrape is supported by the library, **Calypso is the ideal choice**.  

## Supported website

%TABLE%
"""



import calypso
from types import FunctionType
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_favicon(url: str, output_file: str = "favicon.ico") -> str:
    """
    Télécharge le favicon d'un site web.
    
    Args:
        url (str): URL du site (ex: "https://www.python.org")
        output_file (str): Nom du fichier de sortie (par défaut "favicon.ico")
    
    Returns:
        str: Chemin du fichier favicon téléchargé
    """
    try:
        # Normaliser l'URL
        if not url.startswith("http"):
            url = "https://" + url
        
        # Télécharger le HTML
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        favicon_url = None

        # Chercher une balise <link rel="icon"> ou <link rel="shortcut icon">
        for rel in ["icon", "shortcut icon", "apple-touch-icon"]:
            tag = soup.find("link", rel=rel)
            if tag and tag.get("href"):
                favicon_url = urljoin(url, tag["href"])
                break

        # Si rien trouvé, fallback vers /favicon.ico
        if not favicon_url:
            parsed_url = urlparse(url)
            favicon_url = f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"

        # Télécharger le favicon
        fav_response = requests.get(favicon_url, timeout=10, stream=True)
        fav_response.raise_for_status()

        with open(output_file, "wb") as f:
            for chunk in fav_response.iter_content(1024):
                f.write(chunk)

        return output_file

    except Exception as e:
        raise RuntimeError(f"Erreur lors de la récupération du favicon: {e}")

with open("README.md", "w", encoding="utf8") as file:

    table = [
        "| Logo | Name | Address | Function |", 
        "| ---- | ---- | ------- | -------- |"
    ]

    for key in sorted(calypso.service.__dict__.keys()):
        if not key.startswith("__") and not key.endswith("__"):
            service = calypso.service.__dict__[key]
            if isinstance(service, type):
                functions = [
                    key 
                    for key in service.__dict__.keys() 
                    if not key.startswith("__")
                    and not key.endswith("__") 
                    and isinstance(service.__dict__[key], FunctionType)
                ]
                functions = ("`" + "`, `".join(functions) + "`") if len(functions) > 0 else "*none*"
                get_favicon(service.domain, f"./assets/logo/{service.__name__.lower()}.png")
                logo_path = f"https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/{service.__name__.lower()}.png"
                domain_name = service.domain.split("://")[1].split("/")[0].split(".")
                domain_name = domain_name[-2] + "." + domain_name[-1]
                table.append(f"| ![{service.name} logo]({logo_path}) |  {service.name} |  [{domain_name}]({service.domain}) |  {functions} |")

    content = BASE_README
    content = content.replace("%TABLE%", "\n".join(table))
    file.write(content)
