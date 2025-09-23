from datetime import datetime
from unidecode import unidecode
import requests
import json
import re
import os

from ..model.scraper import Scraper


class Coomer(Scraper):
    name = "Coomer"
    domain = "https://coomer.st/"

    def __init__(self):
        self.domain = "https://coomer.st/api"
        self.creators = self.__get_creators__()

    def __request__(self, url:str) -> dict|list:
        return json.loads(
            requests.get(
                self.domain + url, 
                headers={
                    "Accept": "text/css",
                }
            ).content.decode("utf8")
        )

    def __download__(self, path:str, urlpath:str, date:datetime):
        try:
            os.makedirs(path, exist_ok=True)
            filepath = path + f"/{len(os.listdir(path))}.{urlpath.split('.')[-1]}"
            response = requests.get("https://n4.coomer.st/data/" + urlpath, stream=True)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        # yield {
                        #     "current_size": os.path.getsize(filepath), 
                        #     "total_size": int(response.headers['Content-length'])
                        # }
            os.utime(filepath, (date.timestamp(), date.timestamp()))
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def __get_creators__(self) -> list[dict]:
        return self.__request__("/v1/creators")

    def search(self, text:str, by_regex:bool=True) -> list:
        result = []
        text = text if by_regex else unidecode(text).lower()
        for profile in self.creators:
            if by_regex:
                if re.search(text, profile["name"]):
                    profile["image"] = f"https://img.coomer.st/icons/{profile['service']}/{profile['id']}"
                    result.append(profile)
            else:
                if text in unidecode(profile["name"]).lower():
                    profile["image"] = f"https://img.coomer.st/icons/{profile['service']}/{profile['id']}"
                    result.append(profile)
        return result

    def get_posts(self, id:str) -> list[dict]:
        result = [p for p in self.creators if p["id"] == id]
        if len(result) == 0: raise ""
        profile = result[0]
        posts = []
        index = 0
        while True:
            data = self.__request__(f"/v1/{profile['service']}/user/{profile['name']}/posts?o={index}")
            if isinstance(data, dict) and "error" in data.keys(): break
            index += 50
            posts += data
        return posts

    def download(self, posts:list[dict]):
        for post in posts:
            folderpath = f"download/{post['user']}"
            date = datetime.strptime(post["published"], "%Y-%m-%dT%H:%M:%S")

            if "path" in list(post["file"].keys()):
                self.__download__(folderpath, post["file"]["path"], date)
                # yield from self.__yield_info__(
                #     current=index, 
                #     total=len(posts), 
                #     download_status_value=self.__download__(
                #         folderpath, 
                #         post["file"]["path"], 
                #         date
                #     )
                # )

            for attachment in post["attachments"]:
                self.__download__(folderpath, attachment["path"], date)
                # yield from self.__yield_info__(
                #     current=index, 
                #     total=len(posts), 
                #     download_status_value=self.__download__(
                #         folderpath, 
                #         attachment["path"], 
                #         date
                #     )
                # )
