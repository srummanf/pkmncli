#!/usr/bin/env python3
import random
import sys
from pokedex import api, card, finder
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
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

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

# Pokemon color palette
POKEMON_RED = "#de1136"
POKEMON_YELLOW = "#fec401"
POKEMON_LIGHT_BLUE = "#27abfd"
POKEMON_DEEP_BLUE = "#1b70a2"
POKEMON_GREEN = "#51ad60"
POKEMON_GREY = "#dedede"

console = Console()

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

def generate_pokemon_card(pokemon_name):
    """Generate a Pokemon card with error handling and user feedback"""
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
            console.print(f"[bold {POKEMON_RED}]❌ Error generating card:[/bold {POKEMON_RED}] {e}")
            return False
    
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
            return False
    
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
    menu_text.append("Generate another Pokemon card\n", style=POKEMON_GREEN)
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
    welcome_text.append("Welcome to the Pokemon Card Generator! ", style=f"bold {POKEMON_LIGHT_BLUE}")
    welcome_text.append("🌟", style=POKEMON_YELLOW)
    welcome_text.append("\nThis tool creates beautiful trading card-style images of Pokemon.", style=POKEMON_DEEP_BLUE)
    
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
            
            # Generate the card
            success = generate_pokemon_card(pokemon_name)
            
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
                        console.print(Rule(f"[bold {POKEMON_LIGHT_BLUE}]🔄 Starting New Card Generation 🔄[/bold {POKEMON_LIGHT_BLUE}]", style=POKEMON_LIGHT_BLUE))
                        break  # Continue to outer loop
                    elif choice == "2":
                        goodbye_text = Text()
                        goodbye_text.append("👋 Thanks for using Pokemon Card Generator!\n", style=f"bold {POKEMON_LIGHT_BLUE}")
                        goodbye_text.append("🎴 Happy collecting! 🎴", style=f"bold {POKEMON_YELLOW}")
                        
                        console.print(Panel(
                            Align.center(goodbye_text),
                            title=f"[bold {POKEMON_GREEN}]Goodbye Trainer![/bold {POKEMON_GREEN}]",
                            border_style=POKEMON_YELLOW,
                            padding=(1, 2)
                        ))
                        sys.exit(0)
            else:
                # If card generation failed, ask if they want to try again
                retry = Confirm.ask(
                    "[bold yellow]🔄 Would you like to try with a different Pokemon?[/bold yellow]",
                    default=True
                )
                if not retry:
                    goodbye_text = Text()
                    goodbye_text.append("👋 Thanks for using Pokemon Card Generator!", style="bold bright_cyan")
                    
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
            interrupt_text.append("👋 Thanks for using Pokemon Card Generator!", style="bold bright_cyan")
            
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
                goodbye_text.append("👋 Thanks for using Pokemon Card Generator!", style="bold bright_cyan")
                
                console.print(Panel(
                    Align.center(goodbye_text),
                    title="[bold bright_green]Goodbye Trainer![/bold bright_green]",
                    border_style="bright_yellow",
                    padding=(1, 2)
                ))
                sys.exit(0)

if __name__ == "__main__":
    main()
