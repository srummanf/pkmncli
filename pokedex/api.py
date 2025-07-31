import requests

class PokeAPI:
    BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

    def fetch_pokemon(self, name: str):
        res = requests.get(self.BASE_URL + name.lower())
        if res.status_code != 200:
            raise ValueError(f"Pokémon '{name}' not found.")
        data = res.json()

        species_url = data["species"]["url"]
        species = requests.get(species_url).json()
        return data, species

# Singleton instance
pokeapi = PokeAPI()
