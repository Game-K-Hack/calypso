from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import json


class PictAero():
    name = "PictAero"
    domain = "https://www.pictaero.com/"

    def __init__(self, lang:str="fr"):
        self.domain = "https://www.pictaero.com/"
        self.language = lang # 'fr' or 'en'
        # cache
        self.cache_manufacturers = {}

    def __request__(self, url:str) -> str:
        return requests.get(
            self.domain + self.language + url, 
            headers={
                "User-Agent": UserAgent().firefox, 
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
                "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3", 
                "Accept-Encoding": "gzip, deflate, br, zstd", 
                "Referer": self.domain, 
                "Connection": "keep-alive", 
                "Upgrade-Insecure-Requests": "1", 
                "Sec-Fetch-Dest": "document", 
                "Sec-Fetch-Mode": "navigate", 
                "Sec-Fetch-Site": "same-origin", 
                "Sec-Fetch-User": "?1", 
                "DNT": "1", 
                "Sec-GPC": "1", 
                "Priority": "u=0, i", 
                "Pragma": "no-cache", 
                "Cache-Control": "no-cache", 
            }
        ).content.decode("utf8")
    
    def __save_cache_manufacturers__(self):
        if len(self.cache_manufacturers.keys()) > 0:
            return
        for letter in list("abcdefghijklmnopqrstuvwxyz"):
            isdata = True
            index = 0
            cache = {}
            while isdata:
                url = f"/pictures/manufacturers,{letter},{index}"
                content = self.__request__(url)
                content = content.split('<div id="site">')[1]
                if "<table>" not in content:
                    break
                table = content.split("<table>")[1].split("</table>")[0]
                table = table.split("</a>")[:-1]
                for line in table:
                    texts = line.split(">")
                    name = texts[-1]
                    link = texts[-2].split('href="')[-1][:-1]
                    link = self.domain + self.language + link[2:]
                    cache[name] = link
                index += len(table)
            self.cache_manufacturers[letter] = cache

    def get_all_manufacturers(self, letter:str=None) -> list[str]:
        self.__save_cache_manufacturers__()
        
        if letter is None:
            names = []
            for key in self.cache_manufacturers.keys():
                names += list(self.cache_manufacturers[key].keys())
            return names
        else:
            return list(self.cache_manufacturers[letter].keys())

    def get_manufacturers(self) -> list:

pa = PictAero()
print(pa.get_all_manufacturers())
