from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import json


class VoirDrama():
    name = "Voir Drama"
    domain = "https://voirdrama.org/"

    def __init__(self):
        self.domain = "https://voirdrama.org/wp-admin"

    def __search__(self, data:str) -> requests.Response:
        content = requests.post(
            self.domain + "/admin-ajax.php", 
            data=data, 
            headers={
                "User-Agent": UserAgent().firefox, 
                "Accept": "text/html", 
                "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3", 
                "Accept-Encoding": "gzip, deflate, br, zstd", 
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8", 
                "Origin": VoirDrama.domain, 
                "Connection": "keep-alive", 
                "Referer": VoirDrama.domain, 
                "Sec-Fetch-Dest": "empty", 
                "Sec-Fetch-Mode": "cors", 
                "Sec-Fetch-Site": "same-origin", 
                "DNT": "1", 
                "Sec-GPC": "1", 
            }
        ).content.decode("utf8")

        data = content.split("___ASPSTART_DATA___")[1]
        data = data.split("___ASPEND_DATA___")[0]

        return json.loads(data)

    def search(self, text:str, vf:bool=True, vostfr:bool=True) -> list:
        result:list[dict] = []

        if vostfr:
            vostfrdata = self.__search__(f"action=ajaxsearchpro_search&aspp={text}&asid=7&asp_inst_id=7_2&options=aspf%5Bvf__1%5D%3Dvf%26asp_gen%5B%5D%3Dexcerpt%26asp_gen%5B%5D%3Dcontent%26asp_gen%5B%5D%3Dtitle%26filters_initial%3D1%26filters_changed%3D0%26qtranslate_lang%3D0%26current_page_id%3D11")
            result += vostfrdata["results"]

        if vf:
            vfdata = self.__search__(f"action=ajaxsearchpro_search&aspp={text}&asid=6&asp_inst_id=6_2&options=aspf%5Bvf__1%5D%3Dvf%26asp_gen%5B%5D%3Dexcerpt%26asp_gen%5B%5D%3Dcontent%26asp_gen%5B%5D%3Dtitle%26filters_initial%3D1%26filters_changed%3D0%26qtranslate_lang%3D0%26current_page_id%3D11")
            result += vfdata["results"]
        
        return result
    
    def get_drama(self, link:str) -> dict:
        result = {}
        # requête http
        content = requests.get(
            link, 
            headers={
                "User-Agent": UserAgent().firefox, 
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
                "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3", 
                "Accept-Encoding": "gzip, deflate, br, zstd", 
                "Referer": VoirDrama.domain, 
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
        # transformation du contenant de la page html en objet
        soup = BeautifulSoup(content, "html.parser")
        # récupération de l'image
        result["image"] = soup.find("div", class_="site-content").find("img").get("src")
        # box info
        info = soup.find("div", class_="post-content")
        # récupération de la note
        result["rate"] = float(info.find("div", class_="post-rating").find("span").text)
        # récupération des informations
        for infoline in info.find_all("div", class_="post-content_item"):
            key = infoline.find("div", class_="summary-heading").getText().strip()
            value = infoline.find("div", class_="summary-content").getText().strip()
            result[key] = eval(value) if value.isnumeric() else value
        # récupération de la deuxième partie de la page html
        part2 = soup.find("div", class_="main-col-inner")
        # récupération du résumé
        result["Synopsis"] = part2.find("div", class_="description-summary").getText().strip()
        # récupération de la liste des épisodes
        result["episode list"] = []
        for li in part2.find_all("li", class_="wp-manga-chapter"):
            result["episode list"].append({
                "name": li.find("a").getText().strip(), 
                "link": li.find("a").get("href"), 
                "upload date": li.find("span").getText().strip()
            })

        return result
