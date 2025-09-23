import requests
import re
import os

from ..model.scraper import Scraper


class Gotanynudes(Scraper):
    name = "Got any Nudes?"
    domain = "https://gotanynudes.com/"

    def __init__(self):
        self.domain = "https://gotanynudes.com"

    def __extract_width__(self, url):
        return int(url.split()[-1].replace('w',''))

    def __request__(self, url:str) -> str:
        return requests.get(
            self.domain + url, 
        ).content.decode("utf8")

    def __download__(self, path:str, urlpath:str):
        try:
            os.makedirs(path, exist_ok=True)
            filepath = path + f"/{len(os.listdir(path))}.{urlpath.split('.')[-1]}"
            response = requests.get(urlpath, stream=True)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def search(self, text:str) -> list:

        result = []
        index = 1

        while True:
            data = self.__request__(f"/page/{index}/?s=" + text)

            h1 = data.split("<div id=\"content\"")[1].split("<h1 ")[1].split(">")[1].split("<")[0]
            if h1 == "Ooops, sorry! We couldn't find it":
                break

            for elm in data.split("<div id=\"primary\"")[1].split("<div id=\"secondary\"")[0].split("<article ")[1:]:
                url:str = elm.split("<a ")[1].split("href=\"")[1].split("\"")[0]
                images:list[str] = elm.split("<img ")[1].split("data-lazy-srcset=\"")[1].split("\"")[0].split(", ")
                image:str = sorted(images, key=self.__extract_width__)[-1].split(" ")[0]
                title:str = re.findall(
                    "<h3 .*<a .*>([^<]*)<\/a><\/h3>", 
                    elm, 
                    re.MULTILINE
                )[0]
                tag:str = re.findall(
                    "<span class=\"entry-categories\s?\">.*<a .*>([\S\d\w]*)<\/a>", 
                    elm, 
                    re.MULTILINE
                )[0]

                result.append({
                    "id": url[len(self.domain + "/"):] if url.startswith(self.domain) else url, 
                    "url": url, 
                    "image": image, 
                    "title": title, 
                    "tag": tag
                })

            index += 1

        return result

    def get_posts(self, id:str) -> dict[str, dict]:
        data = self.__request__("/" + id)

        data = data.split("<div id=\"content\"")[1]
        data = data.split("<article ")[1].split("<aside class=\"g1-related-entries\">")[0]

        images = []
        for image in data.split("<img ")[1:]:
            if "srcset=\"" in image:
                urls = image.split("srcset=\"")[1].split("\"")[0].split(", ")
                url = sorted(urls, key=self.__extract_width__)[-1].split(" ")[0]
                images.append(url)
        images = list(set(images))

        videos = []
        for image in data.split("<video ")[1:]:
            url = image.split("src=")[1].split(" ")[0]
            videos.append(url)
        videos = list(set(videos))

        return {
            id: {
                "video": videos, 
                "image": images
            }
        }

    def download(self, posts:dict[str, list]):
        for id in posts.keys():
            folderpath = f"download/{id}"

            for image in posts[id]["image"]:
                self.__download__(folderpath, image)

            for video in posts[id]["video"]:
                self.__download__(folderpath, video)
