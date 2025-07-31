from pokedex import api, card, finder

# Initialize components
pokeapi = api.pokeapi
generate_card = card.generate
find_closest = finder.finder.find_closest

# Pokémon to generate card for
pokemon_name = "charizard"  

# Find closest match
actual_name = find_closest(pokemon_name)

if not actual_name:
    print(f"Couldn't find a match for '{pokemon_name}'.")
else:
    print(f"Fetching data for '{actual_name}' (closest match to '{pokemon_name}')...")
    data, species = pokeapi.fetch_pokemon(actual_name)
    generate_card(data, species)
