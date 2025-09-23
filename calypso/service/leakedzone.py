from datetime import datetime
from PIL import Image
import subprocess
import requests
import base64
import shutil
import json
import re
import os
import io

from ..model.scraper import Scraper


class Leakedzone(Scraper):
    name = "Leaked zone"
    domain = "https://leakedzone.com/"

    def __init__(self):
        self.domain = "https://leakedzone.com"
        self.cache_profile = {}

    def __request__(self, url:str) -> dict|list:
        return json.loads(
            requests.get(
                self.domain + url, 
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0", 
                    "Accept": "*/*", 
                    "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3", 
                    "Accept-Encoding": "gzip, deflate, br, zstd", 
                    "X-Requested-With": "XMLHttpRequest", 
                    "Sec-GPC": "1", 
                    "Connection": "keep-alive",  
                    "Sec-Fetch-Dest": "empty", 
                    "Sec-Fetch-Mode": "cors", 
                    "Sec-Fetch-Site": "same-origin", 
                }
            ).content.decode("utf8")
        )

    def __concat_ts_to_mp4__(self, folder:str, output_file:str):
        """
        Concatène tous les fichiers .ts d'un dossier et les convertit en un seul fichier MP4.
        
        Args:
            folder (str): chemin du dossier contenant les fichiers TS
            output_file (str): chemin du fichier MP4 en sortie
        """

        def natural_key(s):
            # Découpe en blocs texte / chiffres
            return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', s)]

        # Récupérer tous les fichiers .ts triés par nom
        ts_files = sorted([
            f for f in os.listdir(folder) 
            if f.lower().endswith(".ts")
        ], key=natural_key)

        if not ts_files:
            print("Aucun fichier TS trouvé dans le dossier.")
            return

        # Créer un fichier texte avec la liste des fichiers TS
        list_file = folder + "/tsfile.list"
        with open(list_file, "w") as f:
            for ts in ts_files:
                f.write(f"file '{ts}'\n")

        try:
            # Commande ffmpeg
            command = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", list_file,
                "-c", "copy",
                output_file
            ]
            
            subprocess.run(command, check=True)
            print(f"Conversion terminée : {output_file}")
        
        except subprocess.CalledProcessError as e:
            print("Erreur lors de la concaténation/conversion :", e)

    def __download__(self, path:str, urlpath:str, date:datetime, convert:str=None):
        try:
            os.makedirs(path, exist_ok=True)
            ext = urlpath.split("?")[0].split(".")[-1]
            filepath = path + f"/{len(os.listdir(path))}.{convert if convert else ext}"

            if ext == "webp" or convert:
                response = requests.get(urlpath)
                if convert:
                    image = Image.open(io.BytesIO(response.content))
                    image = image.convert("RGB")
                    image.save(filepath, convert)
                else:
                    open(filepath, "wb").write(response.content)
                os.utime(filepath, (date.timestamp(), date.timestamp()))
            else:
                if ext == "m3u8":
                    response = requests.get(urlpath)
                    content = response.content.decode("utf8")

                    cache_folder = path + "/cache"
                    os.makedirs(cache_folder, exist_ok=True)

                    urls = re.findall("^https://.*", content, re.MULTILINE)
                    for index, url in enumerate(urls):
                        response = requests.get(url, stream=True)
                        response.raise_for_status()
                        with open(f"{cache_folder}/{index}.ts", 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        # yield {
                        #     "current_size": index+1, 
                        #     "total_size": len(urls)
                        # }

                    filepath = ".".join(filepath.split(".")[:-1]) + ".mp4"
                    self.__concat_ts_to_mp4__(cache_folder, filepath)
                    shutil.rmtree(cache_folder)
                    os.utime(filepath, (date.timestamp(), date.timestamp()))
                    return
                else:
                    response = requests.get(urlpath, stream=True)
                    response.raise_for_status()
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    os.utime(filepath, (date.timestamp(), date.timestamp()))

                # yield {
                #     "current_size": os.path.getsize(filepath), 
                #     "total_size": int(response.headers['Content-length'])
                # }
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def __decode_video_url__(self, encoded: str) -> str:
        # Étape 1 : slice() dans JS → encoded[-0x25ef + -0x156d + 0x3b6c] = encoded[0:]
        s = encoded[:]  

        # Étape 2 : substring(0x11ea + 0x36*0x75 - 0x2a98, -(0xae0 + -0x178a + 0xcba))
        # Calcul des bornes
        start = (0x11ea + (0x36 * 0x75) - 0x2a98)   # = 0
        end = -(0xae0 + -0x178a + 0xcba)            # = 0
        s = s[start: len(s) + end if end != 0 else None]

        # Étape 3 : split('').reverse().join('')
        s = "".join(reversed(list(s)))

        # Étape 4 : base64 decode
        decoded_bytes = base64.b64decode(s)
        return decoded_bytes.decode("utf-8")

    def search(self, text:str, full:bool=False) -> list:
        result = []
        data = self.__request__("/search?search=" + text)
        for profile in data["models"]["data"]:
            self.cache_profile[profile["id"]] = profile["key"]
            if full:
                result.append(profile)
            else:
                result.append({
                    "id": profile["id"], 
                    "image": self.domain + "/" + profile["origin_image"], 
                    "key": profile["key"], 
                    "name": profile["name"], 
                    "description": profile["description"], 
                })
        return result

    def get_posts(self, key:str, full:bool=False) -> list[dict]:
        posts = []
        index = 1
        while True:
            data = self.__request__(f"/{key}?page={index}&type=all&order=0")
            if len(data) == 0:
                break

            for post in data:
                if full:
                    posts.append(post)
                else:
                    posts.append({
                        "id": post["id"],
                        "model_id": post["model_id"],
                        "published_date": post["published_date"],
                        "slug": post["slug"],
                        "image": post["image"], 
                        "stream_url_play": post["stream_url_play"]
                    })

            index += 1
        return posts

    def download(self, posts:list[dict], username:str=None):
        for index, post in enumerate(posts):
            if post["model_id"] not in self.cache_profile:
                if username:
                    user = username
                else:
                    raise "Username not found"
            else:
                user = self.cache_profile[post["model_id"]]
            folderpath = f"download/{user}"
            date = datetime.strptime(post["published_date"], "%Y-%m-%d %H:%M:%S")

            if post["stream_url_play"] == "": # image
                url = "https://image-cdn.leakedzone.com/storage/" + post["image"]
                self.__download__(folderpath, url, date, ("png" if url.endswith("webp") else None))
                # yield from self.__yield_info__(
                #     current=index, 
                #     total=len(posts), 
                #     download_status_value=self.__download__(folderpath, url, date, ("png" if url.endswith("webp") else None))
                # )
            else: # video
                url = self.__decode_video_url__(post["stream_url_play"])
                self.__download__(folderpath, url, date)
                # yield from self.__yield_info__(
                #     current=index, 
                #     total=len(posts), 
                #     download_status_value=self.__download__(folderpath, url, date)
                # )
