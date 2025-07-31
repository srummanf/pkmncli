from pokedex import card, api, finder

class PokedexApp:
    def __init__(self):
        self.api = api.pokeapi
        self.card = card
        self.finder = finder.finder

    def generate_card_for(self, name: str):
        actual_name = self.finder.find_closest(name)
        if not actual_name:
            print(f"Couldn't find a match for '{name}'.")
            return

        print(f"Fetching data for '{actual_name}' (closest match to '{name}')...")
        data, species = self.api.fetch_pokemon(actual_name)
        self.card.generate(data, species)

if __name__ == "__main__":
    app = PokedexApp()
    pokemon_name = "onix"  # Example Pokémon name
    app.generate_card_for(pokemon_name)  
