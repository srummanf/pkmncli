from PIL import Image
import requests
from io import BytesIO
ASCII_CHARS = ['@', '%', '#', '*', '+', '=', '-', ':', '.', ' ']

def fetch_pokemon_sprite_ascii(data, width=40):
    sprite_url = data.get('sprites', {}).get('front_default')
    if not sprite_url:
        return None
    try:
        img_resp = requests.get(sprite_url)
        img = Image.open(BytesIO(img_resp.content)).convert('L')
        aspect_ratio = img.height / img.width
        new_height = int(aspect_ratio * width * 0.55)
        img = img.resize((width, new_height))
        pixels = img.getdata()
        ascii_str = ''
        for i, pixel in enumerate(pixels):
            ascii_str += ASCII_CHARS[pixel // 25]
            if (i + 1) % width == 0:
                ascii_str += '\n'
        return ascii_str
    except Exception:
        return None
#!/usr/bin/env python3
import random
import sys
from pokedex import api, card, finder
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.rule import Rule
from rich.table import Table
from rich.columns import Columns
import time

# Initialize Rich console with Pokemon-themed colors
console = Console()

# Pokemon color palette
POKEMON_RED = "#de1136"
POKEMON_YELLOW = "#fec401"
POKEMON_LIGHT_BLUE = "#27abfd"
POKEMON_DEEP_BLUE = "#1b70a2"
POKEMON_GREEN = "#51ad60"
POKEMON_GREY = "#dedede"
POKEMON_ORANGE = "#ff8c00"
POKEMON_PURPLE = "#8b008b"

def display_ascii_art():
    """Display PkmnCLI ASCII art with split color styling for PKM / N / CLI"""

    ascii_lines = [
        "    ██████╗ ██╗  ██╗███╗   ███╗███╗   ██╗ ██████╗██╗     ██╗   ",
        "    ██╔══██╗██║ ██╔╝████╗ ████║████╗  ██║██╔════╝██║     ██║   ",
        "    ██████╔╝█████╔╝ ██╔████╔██║██╔██╗ ██║██║     ██║     ██║   ",
        "    ██╔═══╝ ██╔═██╗ ██║╚██╔╝██║██║╚██╗██║██║     ██║     ██║   ",
        "    ██║     ██║  ██╗██║ ╚═╝ ██║██║ ╚████║╚██████╗███████╗██║   ",
        "    ╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═╝   ",
    ]

    styled_text = Text()

    for line in ascii_lines:
        pkm = line[:25]   # approx range for PKM
        n = line[25:35]   # approx for N
        cli = line[35:]   # approx for CLI

        styled_text.append(pkm, style=f"bold {POKEMON_RED}")
        styled_text.append(n, style="bold white")
        styled_text.append(cli, style=f"bold {POKEMON_DEEP_BLUE}")
        styled_text.append("\n")

    panel = Panel(
        Align.center(styled_text),
        border_style=POKEMON_YELLOW,
        padding=(0, 1)
    )
    console.print(panel)

def get_random_pokemon():
    """Get a random Pokemon name from the API"""
    try:
        # Get a random number between 1 and 1010 (approximate number of Pokemon)
        random_id = random.randint(1, 1010)
        
        # Try to fetch Pokemon by ID first
        import requests
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{random_id}")
        if res.status_code == 200:
            return res.json()["name"]
        else:
            # Fallback: pick from the loaded name list
            return random.choice(finder.finder.name_list)
    except Exception as e:
        console.print(f"[bold {POKEMON_RED}]⚠️  Error getting random Pokemon:[/bold {POKEMON_RED}] {e}")
        return "pikachu"  # Ultimate fallback

def create_stat_bar(stat_name, stat_value, max_value=255, color=POKEMON_LIGHT_BLUE):
    """Create a visual bar representation of a stat"""
    bar_width = 30
    filled_width = int((stat_value / max_value) * bar_width)
    
    bar = "█" * filled_width + "░" * (bar_width - filled_width)
    return f"[{color}]{bar}[/{color}] {stat_value:3d}"

def display_pokemon_stats(data, species):
    """Display Pokemon stats in a beautiful format with bars"""
    
    # Basic Info Panel
    basic_info = Table(show_header=False, box=None, padding=(0, 1))
    basic_info.add_column(style=f"bold {POKEMON_YELLOW}", width=12)
    basic_info.add_column(style=f"bold {POKEMON_LIGHT_BLUE}")
    
    name = data["name"].title()
    pokemon_id = data["id"]
    height = data["height"] / 10  # Convert to meters
    weight = data["weight"] / 10  # Convert to kg
    base_experience = data.get("base_experience", "Unknown")
    
    # Get types
    types = [t["type"]["name"].title() for t in data["types"]]
    type_str = " / ".join(types)
    
    # Get abilities
    abilities = [a["ability"]["name"].title().replace("-", " ") for a in data["abilities"]]
    ability_str = ", ".join(abilities)
    
    basic_info.add_row("🆔 ID:", f"#{pokemon_id}")
    basic_info.add_row("📏 Height:", f"{height:.1f} m")
    basic_info.add_row("⚖️ Weight:", f"{weight:.1f} kg")
    basic_info.add_row("⭐ Base XP:", str(base_experience))
    basic_info.add_row("🏷️ Type:", type_str)
    basic_info.add_row("💪 Abilities:", ability_str)
    
    # Stats Panel with bars
    stats_table = Table(show_header=True, box=None, padding=(0, 1))
    stats_table.add_column("Stat", style=f"bold {POKEMON_YELLOW}", width=15)
    stats_table.add_column("Value", style=f"bold {POKEMON_LIGHT_BLUE}", width=40)
    stats_table.add_column("Rating", style=f"bold {POKEMON_GREEN}", width=10)
    
    stat_colors = {
        "hp": POKEMON_GREEN,
        "attack": POKEMON_RED,
        "defense": POKEMON_DEEP_BLUE,
        "special-attack": POKEMON_ORANGE,
        "special-defense": POKEMON_PURPLE,
        "speed": POKEMON_YELLOW
    }
    
    stat_names = {
        "hp": "💖 HP",
        "attack": "⚔️ Attack",
        "defense": "🛡️ Defense", 
        "special-attack": "✨ Sp. Attack",
        "special-defense": "🔮 Sp. Defense",
        "speed": "💨 Speed"
    }
    
    total_stats = 0
    for stat in data["stats"]:
        stat_name = stat["stat"]["name"]
        stat_value = stat["base_stat"]
        total_stats += stat_value
        
        display_name = stat_names.get(stat_name, stat_name.title())
        color = stat_colors.get(stat_name, POKEMON_LIGHT_BLUE)
        bar = create_stat_bar(display_name.split(" ")[-1], stat_value, color=color)
        
        # Rating based on stat value
        if stat_value >= 150:
            rating = "🌟🌟🌟"
        elif stat_value >= 100:
            rating = "🌟🌟"
        elif stat_value >= 70:
            rating = "🌟"
        else:
            rating = "⭐"
            
        stats_table.add_row(display_name, bar, rating)
    
    # Add total stats
    stats_table.add_row("", "", "")
    total_bar = create_stat_bar("Total", total_stats, max_value=800, color=POKEMON_YELLOW)
    stats_table.add_row(f"[bold {POKEMON_YELLOW}]📊 TOTAL", total_bar, f"[bold]{total_stats}[/bold]")
    
    # Create columns layout
    info_panel = Panel(
        basic_info,
        title=f"[bold {POKEMON_GREEN}]📋 Basic Info[/bold {POKEMON_GREEN}]",
        border_style=POKEMON_GREEN,
        padding=(1, 1)
    )
    
    stats_panel = Panel(
        stats_table,
        title=f"[bold {POKEMON_RED}]📊 Base Stats[/bold {POKEMON_RED}]",
        border_style=POKEMON_RED,
        padding=(1, 1)
    )
    
    # Main title
    title_text = Text()
    title_text.append(f"🎴 {name} Stats & Info 🎴", style=f"bold {POKEMON_LIGHT_BLUE}")
    
    main_panel = Panel(
        Align.center(title_text),
        border_style=POKEMON_YELLOW,
        padding=(0, 1)
    )
    
    console.print(main_panel)
    console.print(Columns([info_panel, stats_panel], equal=True, expand=True))
    
    # XP Growth Information
    if base_experience != "Unknown":
        xp_info = Text()
        xp_info.append("💡 XP Info: ", style=f"bold {POKEMON_YELLOW}")
        xp_info.append(f"This Pokémon gives {base_experience} base experience when defeated. ", style=POKEMON_LIGHT_BLUE)
        
        # XP Growth rate info (if available in species data)
        growth_rate = species.get("growth_rate", {}).get("name", "unknown")
        if growth_rate != "unknown":
            xp_info.append(f"Growth Rate: {growth_rate.replace('-', ' ').title()}", style=f"bold {POKEMON_GREEN}")
        
        console.print(Panel(
            xp_info,
            title=f"[bold {POKEMON_ORANGE}]⭐ Experience Details[/bold {POKEMON_ORANGE}]",
            border_style=POKEMON_ORANGE,
            padding=(1, 2)
        ))

def prompt_pokemon_name():
    """Prompt user for Pokemon name with styling"""
    # Create a styled prompt panel
    prompt_text = Text()
    prompt_text.append("🔍 Enter a Pokemon name ", style=f"bold {POKEMON_LIGHT_BLUE}")
    prompt_text.append("(or press Enter ↵ for a random Pokemon)", style=f"italic {POKEMON_YELLOW}")
    prompt_text.append("\n📝 Examples: ", style=f"bold {POKEMON_GREEN}")
    prompt_text.append("pikachu, charizard, gengar, lucario...", style=f"italic {POKEMON_DEEP_BLUE}")
    
    console.print(Panel(
        prompt_text,
        title=f"[bold {POKEMON_YELLOW}]Pokemon Selection[/bold {POKEMON_YELLOW}]",
        border_style=POKEMON_LIGHT_BLUE,
        padding=(1, 2)
    ))
    
    user_input = Prompt.ask(
        f"[bold {POKEMON_YELLOW}]➤ Pokemon name[/bold {POKEMON_YELLOW}]",
        default="",
        show_default=False
    ).strip()
    
    if not user_input:
        random_pokemon = get_random_pokemon()
        console.print(f"[bold {POKEMON_RED}]🎲 Random Pokemon selected:[/bold {POKEMON_RED}] [bold {POKEMON_LIGHT_BLUE}]{random_pokemon.title()}[/bold {POKEMON_LIGHT_BLUE}]")
        return random_pokemon
    
    return user_input

def generate_pokemon_card_and_stats(pokemon_name):
    """Generate a Pokemon card with stats display and error handling"""
    console.print(f"\n[bold {POKEMON_YELLOW}]🔎 Searching for '[{POKEMON_LIGHT_BLUE}]{pokemon_name}[/{POKEMON_LIGHT_BLUE}]'...[/bold {POKEMON_YELLOW}]")
    
    # Find closest match
    actual_name = finder.finder.find_closest(pokemon_name)
    
    if not actual_name:
        console.print(f"[bold {POKEMON_RED}]❌ Couldn't find a match for '[{POKEMON_LIGHT_BLUE}]{pokemon_name}[/{POKEMON_LIGHT_BLUE}]'.[/bold {POKEMON_RED}]")
        console.print(f"[bold {POKEMON_YELLOW}]💡 Try checking the spelling or try a different Pokemon![/bold {POKEMON_YELLOW}]")
        return False
    
    if actual_name.lower() != pokemon_name.lower():
        console.print(f"[bold {POKEMON_YELLOW}]📍 Found closest match:[/bold {POKEMON_YELLOW}] [bold {POKEMON_GREEN}]'{actual_name.title()}'[/bold {POKEMON_GREEN}] [dim {POKEMON_GREY}](you searched for '{pokemon_name}')[/dim {POKEMON_GREY}]")
    else:
        console.print(f"[bold {POKEMON_GREEN}]✅ Found exact match:[/bold {POKEMON_GREEN}] [bold {POKEMON_LIGHT_BLUE}]'{actual_name.title()}'[/bold {POKEMON_LIGHT_BLUE}]")
    
    # Progress indicator for API fetch
    with Progress(
        SpinnerColumn(style=POKEMON_YELLOW),
        TextColumn(f"[bold {POKEMON_DEEP_BLUE}]📡 Fetching data from PokeAPI..."),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("Fetching...", total=None)
        
        try:
            # Fetch Pokemon data
            data, species = api.pokeapi.fetch_pokemon(actual_name)
            
            # Small delay to show the spinner
            time.sleep(0.5)
            
        except Exception as e:
            console.print(f"[bold {POKEMON_RED}]❌ Error fetching data:[/bold {POKEMON_RED}] {e}")
            return False
    
    # Display Pokemon ASCII art first
    ascii_art = fetch_pokemon_sprite_ascii(data)
    if ascii_art:
        console.print(Panel(ascii_art, title=f"[bold {POKEMON_YELLOW}]ASCII Sprite[/bold {POKEMON_YELLOW}]", border_style=POKEMON_DEEP_BLUE, padding=(1,2)))
    else:
        console.print(f"[bold {POKEMON_RED}]No sprite available for ASCII art.[/bold {POKEMON_RED}]")

    # Display Pokemon stats
    console.print(Rule(f"[bold {POKEMON_LIGHT_BLUE}]📊 Pokemon Statistics 📊[/bold {POKEMON_LIGHT_BLUE}]", style=POKEMON_LIGHT_BLUE))
    display_pokemon_stats(data, species)
    
    # Ask if user wants to generate card too
    generate_card = Confirm.ask(
        f"\n[bold {POKEMON_YELLOW}]🎴 Would you like to generate a card for {actual_name.title()} as well?[/bold {POKEMON_YELLOW}]",
        default=True
    )
    
    if generate_card:
        console.print(Rule(f"[bold {POKEMON_GREEN}]🎨 Card Generation 🎨[/bold {POKEMON_GREEN}]", style=POKEMON_GREEN))
        
        # Progress indicator for card generation
        with Progress(
            SpinnerColumn(style=POKEMON_GREEN),
            TextColumn(f"[bold {POKEMON_RED}]🎨 Generating card..."),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("Generating...", total=None)
            
            try:
                # Generate the card
                card.generate(data, species)
                
                # Small delay to show the spinner
                time.sleep(0.5)
                
            except Exception as e:
                console.print(f"[bold {POKEMON_RED}]❌ Error generating card:[/bold {POKEMON_RED}] {e}")
                return True  # Return True because stats were shown successfully
        
        # Success message with styled panel
        success_text = Text()
        success_text.append(f"🎉 SUCCESS! Card generated for ", style=f"bold {POKEMON_GREEN}")
        success_text.append(f"{actual_name.title()}", style=f"bold {POKEMON_LIGHT_BLUE}")
        success_text.append("! 🎉", style=f"bold {POKEMON_GREEN}")
        success_text.append(f"\n📁 Check the 'output' folder for your card: ", style=f"bold {POKEMON_YELLOW}")
        success_text.append(f"{actual_name.lower()}.png", style=f"bold {POKEMON_DEEP_BLUE}")
        
        console.print(Panel(
            Align.center(success_text),
            title=f"[bold {POKEMON_GREEN}]Card Generated Successfully![/bold {POKEMON_GREEN}]",
            border_style=POKEMON_GREEN,
            padding=(1, 2)
        ))
    
    return True

def show_menu():
    """Display main menu options"""
    console.print(Rule(style=POKEMON_YELLOW))
    
    menu_text = Text()
    menu_text.append("What would you like to do?\n", style=f"bold {POKEMON_LIGHT_BLUE}")
    menu_text.append("1️⃣  ", style=f"bold {POKEMON_YELLOW}")
    menu_text.append("View another Pokemon's stats & generate card\n", style=POKEMON_GREEN)
    menu_text.append("2️⃣  ", style=f"bold {POKEMON_YELLOW}")
    menu_text.append("Exit", style=POKEMON_RED)
    
    console.print(Panel(
        menu_text,
        title=f"[bold {POKEMON_YELLOW}]Main Menu[/bold {POKEMON_YELLOW}]",
        border_style=POKEMON_DEEP_BLUE,
        padding=(1, 2)
    ))

def main():
    """Main CLI application loop"""
    display_ascii_art()
    
    welcome_text = Text()
    welcome_text.append("Welcome to the Enhanced Pokemon Stats & Card Generator! ", style=f"bold {POKEMON_LIGHT_BLUE}")
    welcome_text.append("🌟", style=POKEMON_YELLOW)
    welcome_text.append("\nThis tool shows detailed Pokemon statistics with XP info and creates beautiful trading cards.", style=POKEMON_DEEP_BLUE)
    
    console.print(Panel(
        welcome_text,
        title=f"[bold {POKEMON_YELLOW}]Welcome Trainer![/bold {POKEMON_YELLOW}]",
        border_style=POKEMON_GREEN,
        padding=(1, 2)
    ))
    console.print()
    
    while True:
        try:
            # Get Pokemon name from user
            pokemon_name = prompt_pokemon_name()
            
            # Generate stats and optionally card
            success = generate_pokemon_card_and_stats(pokemon_name)
            
            if success:
                # Show menu for next action
                show_menu()
                
                while True:
                    choice = Prompt.ask(
                        f"[bold {POKEMON_YELLOW}]➤ Your choice[/bold {POKEMON_YELLOW}]",
                        choices=["1", "2"],
                        show_choices=False
                    )
                    
                    if choice == "1":
                        console.print(Rule(f"[bold {POKEMON_LIGHT_BLUE}]🔄 Starting New Pokemon Lookup 🔄[/bold {POKEMON_LIGHT_BLUE}]", style=POKEMON_LIGHT_BLUE))
                        break  # Continue to outer loop
                    elif choice == "2":
                        goodbye_text = Text()
                        goodbye_text.append("👋 Thanks for using Pokemon Stats & Card Generator!\n", style=f"bold {POKEMON_LIGHT_BLUE}")
                        goodbye_text.append("🎴 Happy collecting! 🎴", style=f"bold {POKEMON_YELLOW}")
                        
                        console.print(Panel(
                            Align.center(goodbye_text),
                            title=f"[bold {POKEMON_GREEN}]Goodbye Trainer![/bold {POKEMON_GREEN}]",
                            border_style=POKEMON_YELLOW,
                            padding=(1, 2)
                        ))
                        sys.exit(0)
            else:
                # If lookup failed, ask if they want to try again
                retry = Confirm.ask(
                    "[bold yellow]🔄 Would you like to try with a different Pokemon?[/bold yellow]",
                    default=True
                )
                if not retry:
                    goodbye_text = Text()
                    goodbye_text.append("👋 Thanks for using Pokemon Stats & Card Generator!", style="bold bright_cyan")
                    
                    console.print(Panel(
                        Align.center(goodbye_text),
                        title="[bold bright_green]Goodbye Trainer![/bold bright_green]",
                        border_style="bright_yellow",
                        padding=(1, 2)
                    ))
                    sys.exit(0)
                console.print(Rule("[bold bright_cyan]🔄 Trying Again 🔄[/bold bright_cyan]", style="bright_cyan"))
                    
        except KeyboardInterrupt:
            console.print("\n")
            interrupt_text = Text()
            interrupt_text.append("⚡ Interrupted by user\n", style="bold bright_red")
            interrupt_text.append("👋 Thanks for using Pokemon Stats & Card Generator!", style="bold bright_cyan")
            
            console.print(Panel(
                Align.center(interrupt_text),
                title="[bold bright_red]Interrupted[/bold bright_red]",
                border_style="bright_red",
                padding=(1, 2)
            ))
            sys.exit(0)
        except Exception as e:
            console.print(f"\n[bold red]❌ Unexpected error:[/bold red] {e}")
            retry = Confirm.ask(
                "[bold yellow]🔄 Would you like to try again?[/bold yellow]",
                default=True
            )
            if not retry:
                goodbye_text = Text()
                goodbye_text.append("👋 Thanks for using Pokemon Stats & Card Generator!", style="bold bright_cyan")
                
                console.print(Panel(
                    Align.center(goodbye_text),
                    title="[bold bright_green]Goodbye Trainer![/bold bright_green]",
                    border_style="bright_yellow",
                    padding=(1, 2)
                ))
                sys.exit(0)

if __name__ == "__main__":
    main()