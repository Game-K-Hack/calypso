BASE_LOGO_URL = "https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/logo/"
BASE_README = """![banner](https://raw.githubusercontent.com/Game-K-Hack/calypso/master/assets/calypso-banner-rounded.jpg)

### CALYPSO

The *Calypso* is an oceanographic vessel equipped and used by the maritime explorer Jacques-Yves Cousteau for his scientific expeditions and documentary film productions.

Named after Calypso, the sea nymph from Greek mythology, the ship and its crew sailed the world’s seas and oceans from November 24, 1951, until January 1996. Through television and books, the *Calypso* became one of the symbols of maritime exploration and global ecology in the second half of the 20th century, in the tradition of its illustrious predecessors such as *La Boussole* and *L’Astrolabe*, the *Beagle*, the *Challenger*, the *Pourquoi Pas?*, and the *Hirondelle*.

## Description

**Calypso** is not only the name of a famous exploration vessel: it’s also a Python library for **web scraping**.  
Unlike general-purpose tools such as HTTrack, which download an entire site before extracting data, Calypso is designed to be **fast and targeted**. It only retrieves the information you need, in an optimized way.  
If the website you want to scrape is supported by the library, **Calypso is the ideal choice**.  

## Installation

You can install **Calypso** directly from **PyPI** with `pip`:

```bash
pip install pycalypso
```

Or from the GitHub repository to get the latest development version:

```bash
git clone https://github.com/Game-K-Hack/calypso.git
cd calypso
pip install -r requirements.txt
```

Make sure you are using Python 3.7 or higher.

## Supported website

%TABLE%

### Coming soon

%TABLE_COMING_SOON%

"""
COMING_SOON = {
    "Nautiljon": "https://www.nautiljon.com/", 
    "PictAero": "https://www.pictaero.com/", 
    "MyAnimeList": "https://myanimelist.net/", 
    "Jikan": "https://jikan.moe/", 
    "IGDB": "https://www.igdb.com/", 
    "TwitchTracker": "https://twitchtracker.com/", 
    "TMDB": "https://www.themoviedb.org/", 
    "TV Theme Tunes": "https://www.televisiontunes.com/", 
    "Games Theme Songs": "https://gamethemesongs.com/", 
    "Tv ad songs": "http://tvadsongs.com/", 
    "YARN": "https://yarn.co/", 
    "IMDb": "https://www.imdb.com/", 
    "ISBN DB": "https://isbndb.com/", 
    "MusicBrainz": "https://musicbrainz.org/", 
    "SteamDB": "https://steamdb.info/", 
    "JAV Database": "https://www.javdatabase.com/", 
}



import io
import os
import calypso
import urllib3
import requests
from PIL import Image
from bs4 import BeautifulSoup
from types import FunctionType
from fake_useragent import UserAgent
from urllib.parse import urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def find_icons(url:str) -> list[str]:
    resp = requests.get(url, timeout=30, verify=False)
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

    return [i for i in list(icons) if not i.endswith(".svg") and ".svg?" not in i]

def get_favicon(url:str, output_file:str="favicon.ico") -> str:
    icon_url = BASE_LOGO_URL + os.path.basename(output_file)
    if os.path.exists(output_file):
        print(f" \033[90mDEBUG   Get local image: {output_file}\033[0m")
        return icon_url

    icons:dict[int, Image] = {}
    domain = "/".join(url.split("/")[:3])
    for favicon_url in find_icons(url):
        print(" \033[90mDEBUG  ", favicon_url, "\033[0m")
        try:
            content = requests.get(
                favicon_url, 
                headers={
                    "User-Agent": UserAgent().firefox, 
                    "Origin": domain, 
                    "Referer": domain + "/", 
                    "Cache-Control": "no-cache", 
                }, 
                timeout=10, 
                verify=False)
        except requests.exceptions.InvalidSchema:
            continue
        if 200 <= content.status_code < 400:
            image = Image.open(io.BytesIO(content.content))
            h, w = image.size
            icons[h*w] = image
        else:
            continue
    if len(list(icons.keys())) > 0:
        best_image = sorted(icons.keys())[-1]
        icons[best_image].save(output_file)
    else:
        print("\033[31m ERROR   Tab icon not found, please enter the URL of the corresponding icon or leave blank for a default icon")
        filepath = input(" \033[35mINPUT\033[0m   \033[01m>\033[0m ")
        if filepath == "":
            icon_url = BASE_LOGO_URL + "__not_found__.png"
        else:
            Image.open(filepath).save(output_file)
    return icon_url

def resize(url:str) -> str:
    filepath = "./assets/logo/" + url.split("/")[-1]
    image = Image.open(filepath)
    image = image.resize((40, 40))
    resizefilepath = ".".join(url.split("/")[-1].split(".")[:-1]) + "-resized.png"
    image.save("./assets/logo/" + resizefilepath)
    return BASE_LOGO_URL + resizefilepath

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
                imagepath = resize(imagepath)
                print(f"    \033[32mOK\033[0m   Icon of {service.domain} saved")
                domain_name = service.domain.split("://")[1].split("/")[0].split(".")
                domain_name = domain_name[-2] + "." + domain_name[-1]
                table.append(f"| ![{service.name} logo]({imagepath}) |  {service.name} |  [{domain_name}]({service.domain}) |  {functions} |")
                print("    \033[32mOK\033[0m   Writed in readme")

    table_coming_soon = [
        "| Logo | Name | Address |", 
        "| ---- | ---- | ------- |"
    ]

    for key in sorted(COMING_SOON.keys()):
        url = COMING_SOON[key]
        domain_name = url.split("://")[1].split("/")[0].split(".")
        domain_name = domain_name[-2] + "." + domain_name[-1]
        print(f"  \033[33mWAIT\033[0m   Search icon of {domain_name}...")
        imagepath = get_favicon(url, f"./assets/logo/{domain_name.lower().replace(' ', '')}.png")
        imagepath = resize(imagepath)
        print(f"    \033[32mOK\033[0m   Icon of {domain_name} saved")
        table_coming_soon.append(f"| ![{key} logo]({imagepath}) |  {key} |  [{domain_name}]({url}) |")
        print("    \033[32mOK\033[0m   Writed in readme")

    content = BASE_README
    content = content.replace("%TABLE%", "\n".join(table))
    content = content.replace("%TABLE_COMING_SOON%", "\n".join(table_coming_soon))
    file.write(content)

print("  \033[34mINFO\033[0m   Ended")
