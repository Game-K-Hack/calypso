BASE_LOGO_URL = "https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/"
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



import io
import calypso
import requests
from PIL import Image
from bs4 import BeautifulSoup
from types import FunctionType
from fake_useragent import UserAgent
from urllib.parse import urljoin

def find_icons(url:str):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    icons = set()

    # <link rel="icon" ...>
    for link in soup.find_all("link", rel=lambda x: x and "icon" in x.lower()):
        href = link.get("href")
        if href:
            icons.add(urljoin(resp.url, href))

    # try /favicon.ico
    icons.add(urljoin(resp.url, "/favicon.ico"))

    # manifest (android/modern sites)
    manifest_tag = soup.find("link", rel="manifest")
    if manifest_tag and manifest_tag.get("href"):
        try:
            murl = urljoin(resp.url, manifest_tag["href"])
            mresp = requests.get(murl, timeout=5)
            m = mresp.json()
            if "icons" in m:
                for ic in m["icons"]:
                    if "src" in ic:
                        icons.add(urljoin(murl, ic["src"]))
        except Exception:
            pass

    return [i for i in list(icons) if not i.endswith(".svg")]

def get_favicon(url: str, output_file: str = "favicon.ico") -> str:
    icons:dict[int, Image] = {}
    domain = "/".join(url.split("/")[:3])
    for favicon_url in find_icons(url):
        print(" \033[90mDEBUG  ", favicon_url, "\033[0m")
        try:
            content = requests.get(
                favicon_url, 
                headers={
                    "User-Agent": UserAgent().firefox, 
                    "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5", 
                    "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3", 
                    "Accept-Encoding": "gzip, deflate, br, zstd", 
                    "Connection": "keep-alive", 
                    "Origin": domain, 
                    "Referer": domain + "/", 
                    "Sec-Fetch-Dest": "image", 
                    "Sec-Fetch-Mode": "no-cors", 
                    "Sec-Fetch-Site": "same-origin", 
                    "DNT": "1", 
                    "Sec-GPC": "1", 
                    "Priority": "u=6", 
                    "Pragma": "no-cache", 
                    "Cache-Control": "no-cache", 
                    "TE": "trailers", 
                }, 
                timeout=10)
            image = Image.open(io.BytesIO(content.content))
            h, w = image.size
            icons[h*w] = image
        except: continue
    if len(list(icons.keys())) > 0:
        best_image = sorted(list(icons.keys()))[-1]
        icons[best_image].save(output_file)
    else:
        print("\033[31m ERROR   Tab icon not found, please enter the URL of the corresponding icon or leave blank for a default icon")
        best_image = input(" \033[35mINPUT\033[0m   \033[01m>\033[0m ")
        if best_image == "":
            output_file = BASE_LOGO_URL + "__not_found__.png"
        else:
            icons[best_image].save(output_file)
    return output_file

print("  \033[34mINFO\033[0m   Start")
with open("README.md", "w", encoding="utf8") as file:

    table = [
        "| Logo | Name | Address | Function |", 
        "| ---- | ---- | ------- | -------- |"
    ]

    for key in sorted(calypso.service.__dict__.keys()):
        if not key.startswith("__") and not key.endswith("__"):
            service = calypso.service.__dict__[key]
            if isinstance(service, type):
                print(f"  \033[33mWAIT\033[0m   Search icon of {service.domain}...")
                functions = [
                    key 
                    for key in service.__dict__.keys() 
                    if not key.startswith("__")
                    and not key.endswith("__") 
                    and isinstance(service.__dict__[key], FunctionType)
                ]
                functions = ("`" + "`, `".join(functions) + "`") if len(functions) > 0 else "*none*"
                imagepath = get_favicon(service.domain, f"./assets/logo/{service.__name__.lower()}.png")
                print(f"    \033[32mOK\033[0m   Icon of {service.domain} saved")
                domain_name = service.domain.split("://")[1].split("/")[0].split(".")
                domain_name = domain_name[-2] + "." + domain_name[-1]
                table.append(f"| ![{service.name} logo]({imagepath}) |  {service.name} |  [{domain_name}]({service.domain}) |  {functions} |")
                print("    \033[32mOK\033[0m   Writed in readme")

    content = BASE_README
    content = content.replace("%TABLE%", "\n".join(table))
    file.write(content)

print("  \033[34mINFO\033[0m   Ended")
