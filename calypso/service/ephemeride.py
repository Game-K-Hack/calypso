from kelian.utils import fix_encoding
from fake_useragent import UserAgent
import requests
import html


class Ephemeride():
    name = "Ephemeride"
    domain = "https://www.ephemeride.com/"

    def __init__(self):
        self.domain = "https://www.ephemeride.com/free/"

    def __request__(self, url:str) -> str:
        res = requests.get(self.domain + url).content.decode("iso-8859-1")
        return fix_encoding(html.unescape(res)).replace("\\'", "'").replace("\\\"", "\"")
    
    def get_fete_du_jour(self) -> str:
        content = self.__request__("fete.jsp")
        content = content.split("class=\"FeteHomme\">")
        return content[1].split("</font>")[0]
    
    def get_evenement_du_jour(self) -> str:
        content = self.__request__("evenement.jsp")
        content = content.split("<td class=\"fmb\"")[1]
        i = content.index(">") + 1
        content = content[i:].split("<br>")[0]
        content = content.replace("<b>", "").replace("</b>", "")
        return content
    
    def get_diction_du_jour(self) -> str:
        content = self.__request__("dicton.jsp")
        content = content.split("<td class=\"fmb\"")[1]
        i = content.index(">") + 1
        content = content[i:].split("<br>")[0]
        content = content.replace("<b>", "").replace("</b>", "")
        return content
    
    def get_citation_du_jour(self) -> tuple[str, str]:
        content = self.__request__("citation.jsp")
        content = content.split("<td class=\"fmb\"")[1]
        i = content.index(">") + 1
        content = content[i:].split("<br>")[0]
        content = content.replace("<b>", "").replace("</b>", "")
        p = content.split("\"cita\">")[1].split("</span>")[0]
        return content.split("<div")[0], p
    
    def get_proverbe_du_jour(self) -> str:
        content = self.__request__("proverbe.jsp")
        content = content.split("<td class=\"fmb\"")[1]
        i = content.index(">") + 1
        content = content[i:].split("<br>")[0]
        content = content.replace("<b>", "").replace("</b>", "")
        return content
    
    def get_jour(self) -> dict:
        res = requests.get(
            "https://www.ephemeride.com/home/1/calendriers-et-histoire.html", 
            headers={ "User-Agent": UserAgent().firefox })
        content = fix_encoding(html.unescape(res.content.decode("iso-8859-1")))
        content = content.replace("\\'", "'").replace("\\\"", "\"")
        td = content.split("class=\"TexteGrisClair\"")
        td1 = td[1].split("<br>")
        td2 = td[2].split("<br>")
        f = lambda x: x.replace("\r", "").replace("\n", "").replace("\t", "")
        return {
            "day_of_the_year": int(f(td1[1]).split("e")[0]),
            "days_remaining": int(f(td1[2]).split(" ")[0]),
            "week": int(f(td1[3]).split("e")[0]), 
            "hour": f(td2[1]).replace("<b>", "").replace("</b>", ""), 
            "timezone": f(td2[2]), 
            "type_of_time": f(td2[3]).split("<")[0]
        }
