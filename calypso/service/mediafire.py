import requests
from datetime import datetime
from os.path import join as join_path
from kelian import ProgressBar


class MediaFire():
    name = "MediaFire"
    domain = "https://www.mediafire.com"

    def __init__(self, url_or_code:str) -> None:
        self.domain = "https://www.mediafire.com/file/"
        self.url = url_or_code if url_or_code.startswith("http") else self.domain + url_or_code
        self.content = None

    def __request__(self) -> None:
        if self.content is None:
            self.content = requests.get(
                self.url, 
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0"
                }
            ).content.decode("utf8")

    def __convert_size__(self, size_str: str) -> int:
        units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
        size_str = size_str.strip().upper()
        for unit in sorted(units.keys(), key=len, reverse=True):
            if size_str.endswith(unit):
                number = size_str[: -len(unit)]
                return int(float(number) * units[unit])
        raise ValueError(f"Unité inconnue dans la chaîne: {size_str}")

    def get_info(self) -> dict:
        self.__request__()
        fn = self.content.split("<div class=\"filename\">")[1].split("</div>")[0]
        fs = self.content.split("<ul class=\"details\">")[1].split("</span>")[0].split("<span>")[1]
        d = self.content.split("<div class=\"DLExtraInfo-sectionDetails\">")[1].split("</p>")[0].split("<p>")[1]
        ud = datetime.strptime(d.split(" from ")[1].split(" on ")[1], "%B %d, %Y at %I:%M %p")
        uc = d.split(" from ")[1].split(" on ")[0]
        return {"filename": fn, "size": self.__convert_size__(fs), "uploaded date": ud, "uploaded contry": uc}
    
    def download(self, output:str, chunk_size:int=8192) -> None:
        self.__request__()
        url = self.content.split("aria-label=\"Download file\"")[1].split("href=\"")[1].split("\"")[0]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = self.get_info().get("size")
            pb = ProgressBar(total_size, enabled_average_time=False)
            pb.format("Download file [")
            with open(join_path(output, self.get_info().get("filename")), 'wb') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    pb.current += chunk_size
                    print(pb.display(), end="\r")
