# pkmnCLI

This project generates custom Pokémon card images using data from the PokéAPI. Each card features a Pokémon's sprite, name, type, and base stats, styled with a unique background and font.

## Features

- Fetches Pokémon data and sprites from the PokéAPI
- Generates visually appealing card images for each Pokémon
- Custom background color and dotted pattern based on Pokémon type
- Displays Pokémon name, number, type, and all base stats
- Uses a retro pixel font for a classic look

## Folder Structure

```
├── app.py                # Main application entry point
├── cli.py                # Command-line interface 
├── requirements.txt      # Python dependencies
├── pokedex/              # Main package
│   ├── __init__.py
│   ├── api.py            # Handles API requests to PokéAPI
│   ├── card.py           # Card image generation logic
│   ├── finder.py         # Pokémon search and lookup logic
│   └── assets/           # Fonts and other static assets
│       └── BebasNeue-Regular.ttf
├── output/               # Generated card images
│   └── *.png
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/srummanf/pokedex.git
   cd pokedex
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Usage

1. Add your pokemon in app.py and run the main application to generate Pokémon cards:

```sh
python app.py
```

2. Use CLI arguments to specify the Pokémon to generate cards for:

```sh
python cli.py
```  

Generated cards will be saved in the `output/` directory.

## Customization

- To change the font, replace the file in `pokedex/assets/`.
- To adjust card appearance, edit `pokedex/card.py`.

## Credits

- [PokéAPI](https://pokeapi.co/) for Pokémon data and sprites
