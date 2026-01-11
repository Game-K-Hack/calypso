from playwright.sync_api import sync_playwright
import requests
import re


class Largus():
    name = "L'argus"
    domain = "https://www.largus.fr/"

    def __init__(self):
        self.occasion_domain = "https://occasion.largus.fr"
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0", 
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3", 
            "Accept-Encoding": "gzip, deflate, br, zstd", 
            "Referer": "https://www.largus.fr/", 
            "Connection": "keep-alive", 
            "Upgrade-Insecure-Requests": "1", 
            "Sec-Fetch-Dest": "document", 
            "Sec-Fetch-Mode": "navigate", 
            "Sec-Fetch-Site": "same-site", 
            "Sec-Fetch-User": "?1", 
            "DNT": "1", 
            "Sec-GPC": "1", 
            "Priority": "u=0, i", 
            "Pragma": "no-cache", 
            "Cache-Control": "no-cache", 
        }

        self.pw_abort_filter = [
            "**/*.ico", 
            "**/*.png", 
            "**/*.jpg", 
            "**/*.jpeg", 
            "https://assets.largus.fr/**", 
            "**/*.css"
        ]

        self.pw = sync_playwright().start()
        self.pwbrowser = self.pw.firefox.launch(headless=True)

    def __new_browser_page__(self):
        self.pwpage = self.pwbrowser.new_page()

        for reg in self.pw_abort_filter:
            self.pwpage.route(reg, lambda route: route.abort())

        self.pwpage.route("**/*.js", lambda route: (
            route.continue_()
            if re.search("client\.[0-9a-z]{1,20}\.js", route.request.url)
            else route.abort()
        ))

    def __close_browser_page__(self):
        self.pwbrowser.close()

    def get_occasion_cars_list(self, index:int=1, url_only:bool=False) -> list[dict|str]:
        content = self.session.get(f"{self.occasion_domain}/auto/?currentpage={index}").content.decode("utf8")
        content = content.split("id=\"list-container\"")[1].split("id=\"filterList\"")[0]
        cars = []
        for item in content.split("<div class=\"list-group-item result\"")[1:]:
            href = self.occasion_domain + item.split("href=\"")[1].split("\"")[0]
            if not url_only:
                title = item.split("<h3")[1].split("/h3>")[0].split(">")[1].split("<")[0].strip()
                price = item.split("class=\"prix\"")[1].split("/span>")[0].split(">")[1].split("<")[0].strip()
                subitem = item.split("<ul class=\"list-unstyled\"")[1].split("</ul>")[0]
                carburant = subitem.split("<li class=\"energie")[1].split("</li>")[0].split(">")[1].strip()
                km = subitem.split("<li class=\"km")[1].split("</li>")[0].split(">")[1].strip()
                year = subitem.split("<li class=\"annee")[1].split("</li>")[0].split(">")[1].strip()
                city = subitem.split("<li class=\"col-3")[1].split("</li>")[0].split(">")[1].strip()
                cars.append({
                    "title": title, "price": price, "carburant": carburant, 
                    "km": km, "year": year, "city": city, "href": href, 
                })
            else:
                cars.append(href)
        return cars
    
    def get_occasion_car_detail(self, url_or_id:str) -> dict:
        """
        url_or_id:
            → url = https://occasion.largus.fr/auto/annonce-82fdc428db7c31e2_ds-ds-4-puretech-130ch-opera-automatique-37465-km.html
            → id = annonce-82fdc428db7c31e2_ds-ds-4-puretech-130ch-opera-automatique-37465-km
        """
        url = url_or_id if url_or_id.startswith("http") else f"{self.occasion_domain}/auto/{url_or_id}.html"

        self.__new_browser_page__()
        self.pwpage.goto(url)
        content:str = self.pwpage.content()
        title = content.split("class=\"modele\">")[1].split("<")[0].strip()
        price = content.split("class=\"prix\">")[1].split("<")[0].strip()
        km = content.split("class=\"km\"><span")[1].split("</span></li>")[0].split(">")[-1].strip()
        energy = content.split("class=\"energie\"><span")[1].split("</span></li>")[0].split(">")[-1].strip()
        if "Couleur" in content:
            color = content.replace("\n", "").replace(" ", "").split("Couleur</li><li")[1].split("</li></ul>")[0].split(">")[-1].strip()
        else:
            color = None

        description = content \
            .split("id=\"equipements\"")[1] \
            .split("class=\"bloc-equipements formatting-desc\"")[1] \
            .split("class=\"list-unstyled\"><li")[1] \
            .split(">")[1] \
            .split("</li></ul>")[0]
        description = "\n".join(description.split("\n")[:-1]).strip()

        self.__close_browser_page__()

        return {
            "title": title, 
            "price": price, 
            "km": km, 
            "energy": energy, 
            "color": color, 
            "description": description
        }
