import difflib
import requests

class PokeFinder:
    def __init__(self):
        self.name_list = self.fetch_all_names()

    def fetch_all_names(self):
        url = "https://pokeapi.co/api/v2/pokemon?limit=10000"
        res = requests.get(url)
        if res.status_code != 200:
            raise Exception("Failed to fetch Pokémon list from API.")
        results = res.json()["results"]
        return [pokemon["name"] for pokemon in results]

    def find_closest(self, input_name: str):
        matches = difflib.get_close_matches(input_name.lower(), self.name_list, n=1, cutoff=0.6)
        return matches[0] if matches else None

# Singleton instance
finder = PokeFinder()
