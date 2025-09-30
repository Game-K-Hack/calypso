from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests


class BinSX():
    name = "Bin.sx"
    domain = "https://paste.bin.sx"

    def __init__(self):
        self.domain = "https://paste.bin.sx/"

    def get_text_by_id(self, id:str) -> str:
        content = requests.get(
            self.domain + "index.php?p=" + id, 
            headers={
                "User-Agent": UserAgent().firefox, 
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
                "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3", 
                "Accept-Encoding": "gzip, deflate, br, zstd", 
                "Connection": "keep-alive", 
                "Upgrade-Insecure-Requests": "1", 
                "Sec-Fetch-Dest": "document", 
                "Sec-Fetch-Mode": "navigate", 
                "Sec-Fetch-Site": "none", 
                "Sec-Fetch-User": "?1", 
                "DNT": "1", 
                "Sec-GPC": "1", 
                "Priority": "u=0, i", 
                "Pragma": "no-cache", 
                "Cache-Control": "no-cache", 
            }
        ).content.decode("utf8")
        soup = BeautifulSoup(content, "html.parser")
        box = soup.find("textarea", { "id": "textbox"})
        return box.getText()
