from types import GeneratorType

class Scraper:
    name = "Scraper"

    def __init__(self):
        pass

    def __yield_info__(self, **kwargs):
        gens = {k: v for k, v in kwargs.items() if isinstance(v, GeneratorType)}
        static = {k: v for k, v in kwargs.items() if not isinstance(v, GeneratorType)}

        while gens:
            data = static.copy()
            remove_keys = []
            for key, gen in gens.items():
                try:
                    data[key] = next(gen)
                except StopIteration:
                    remove_keys.append(key)
            # enlever les générateurs épuisés
            for k in remove_keys:
                gens.pop(k)
            # ⚠️ ne yield que si on a encore au moins une valeur générée
            if len(data) > len(static):
                yield data

    def search(self, text:str, by_regex:bool=True) -> list:
        """Méthode pour rechercher un profil"""
        message = "[ERROR] Search method is not coded"
        print(message)

    def get_posts(self, id:str) -> list[dict]:
        """Récupérer les posts du profil"""
        message = "[ERROR] Get_posts method is not coded"
        print(message)

    def download(self, posts:list[dict]) -> None:
        """Télécharger les posts"""
        message = "[ERROR] Download method is not coded"
        print(message)
