#!/usr/bin/env python3
import random
import sys
from pokedex import api, card, finder

def display_ascii_art():
    """Display PkmnCLI ASCII art"""
    ascii_art = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║    ██████╗ ██╗  ██╗███╗   ███╗███╗   ██╗ ██████╗██╗     ██╗   ║
    ║    ██╔══██╗██║ ██╔╝████╗ ████║████╗  ██║██╔════╝██║     ██║   ║
    ║    ██████╔╝█████╔╝ ██╔████╔██║██╔██╗ ██║██║     ██║     ██║   ║
    ║    ██╔═══╝ ██╔═██╗ ██║╚██╔╝██║██║╚██╗██║██║     ██║     ██║   ║
    ║    ██║     ██║  ██╗██║ ╚═╝ ██║██║ ╚████║╚██████╗███████╗██║   ║
    ║    ╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═╝   ║
    ║                                                               ║
    ║                     🎴 Card Generator 🎴                      ║
    ║                                                               ║
    ║                    ⚡ Catch 'Em All in Cards! ⚡              ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(ascii_art)
    print()

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
        print(f"⚠️  Error getting random Pokemon: {e}")
        return "pikachu"  # Ultimate fallback

def prompt_pokemon_name():
    """Prompt user for Pokemon name with styling"""
    print("🔍 Enter a Pokemon name (or press Enter ↵ for a random Pokemon):")
    print("📝 Examples: pikachu, charizard, gengar, lucario...")
    print()
    
    user_input = input("➤ Pokemon name: ").strip()
    
    if not user_input:
        random_pokemon = get_random_pokemon()
        print(f"🎲 Random Pokemon selected: {random_pokemon.title()}")
        return random_pokemon
    
    return user_input

def generate_pokemon_card(pokemon_name):
    """Generate a Pokemon card with error handling and user feedback"""
    print(f"\n🔎 Searching for '{pokemon_name}'...")
    
    # Find closest match
    actual_name = finder.finder.find_closest(pokemon_name)
    
    if not actual_name:
        print(f"❌ Couldn't find a match for '{pokemon_name}'.")
        print("💡 Try checking the spelling or try a different Pokemon!")
        return False
    
    if actual_name.lower() != pokemon_name.lower():
        print(f"📍 Found closest match: '{actual_name.title()}' (you searched for '{pokemon_name}')")
    else:
        print(f"✅ Found exact match: '{actual_name.title()}'")
    
    print(f"📡 Fetching data from PokeAPI...")
    
    try:
        # Fetch Pokemon data
        data, species = api.pokeapi.fetch_pokemon(actual_name)
        
        print(f"🎨 Generating card...")
        
        # Generate the card
        card.generate(data, species)
        
        print(f"🎉 SUCCESS! Card generated for {actual_name.title()}!")
        print(f"📁 Check the 'output' folder for your card: {actual_name.lower()}.png")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating card: {e}")
        return False

def show_menu():
    """Display main menu options"""
    print("\n" + "="*60)
    print("What would you like to do?")
    print("1️⃣  Generate another Pokemon card")
    print("2️⃣  Exit")
    print("="*60)

def main():
    """Main CLI application loop"""
    display_ascii_art()
    
    print("Welcome to the Pokemon Card Generator! 🌟")
    print("This tool creates beautiful trading card-style images of Pokemon.")
    print()
    
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
                    choice = input("\n➤ Your choice (1 or 2): ").strip()
                    
                    if choice == "1":
                        print("\n" + "🔄 " + "="*58 + " 🔄")
                        break  # Continue to outer loop
                    elif choice == "2":
                        print("\n👋 Thanks for using Pokemon Card Generator!")
                        print("🎴 Happy collecting! 🎴")
                        sys.exit(0)
                    else:
                        print("❌ Invalid choice. Please enter 1 or 2.")
            else:
                # If card generation failed, ask if they want to try again
                retry = input("\n🔄 Would you like to try with a different Pokemon? (y/n): ").strip().lower()
                if retry not in ['y', 'yes']:
                    print("\n👋 Thanks for using Pokemon Card Generator!")
                    sys.exit(0)
                print("\n" + "🔄 " + "="*58 + " 🔄")
                    
        except KeyboardInterrupt:
            print("\n\n⚡ Interrupted by user")
            print("👋 Thanks for using Pokemon Card Generator!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            retry = input("🔄 Would you like to try again? (y/n): ").strip().lower()
            if retry not in ['y', 'yes']:
                print("\n👋 Thanks for using Pokemon Card Generator!")
                sys.exit(0)

if __name__ == "__main__":
    main()

# #!/usr/bin/env python3
# import random
# import sys
# import os
# from pokedex import api, card, finder

# try:
#     from rich.console import Console
#     from rich.panel import Panel
#     from rich.text import Text
#     from rich.table import Table
#     from rich.progress import Progress, SpinnerColumn, TextColumn
#     from rich.prompt import Prompt
#     from rich.align import Align
#     from rich.columns import Columns
#     from rich.layout import Layout
#     import keyboard
#     RICH_AVAILABLE = True
# except ImportError:
#     RICH_AVAILABLE = False
#     print("⚠️  For the best experience, install rich and keyboard:")
#     print("pip install rich keyboard")
#     print("Falling back to basic mode...\n")

# try:
#     import keyboard
#     KEYBOARD_AVAILABLE = True
# except ImportError:
#     KEYBOARD_AVAILABLE = False

# class PkmnCLI:
#     def __init__(self):
#         self.console = Console() if RICH_AVAILABLE else None
#         self.current_selection = 0
#         self.menu_options = ["🎲 Random Pkmn", "🔍 Search Pkmn", "📊 View Last Stats", "❌ Exit"]
#         self.last_pkmn_data = None
#         self.last_species_data = None

#     def display_ascii_art(self):
#         """Display colorful PkmnCLI ASCII art"""
#         if RICH_AVAILABLE:
#             ascii_text = Text()
#             ascii_text.append("██████╗ ██╗  ██╗███╗   ███╗███╗   ██╗ ██████╗██╗     ██╗\n", style="bold cyan")
#             ascii_text.append("██╔══██╗██║ ██╔╝████╗ ████║████╗  ██║██╔════╝██║     ██║\n", style="bold blue")
#             ascii_text.append("██████╔╝█████╔╝ ██╔████╔██║██╔██╗ ██║██║     ██║     ██║\n", style="bold magenta")
#             ascii_text.append("██╔═══╝ ██╔═██╗ ██║╚██╔╝██║██║╚██╗██║██║     ██║     ██║\n", style="bold red")
#             ascii_text.append("██║     ██║  ██╗██║ ╚═╝ ██║██║ ╚████║╚██████╗███████╗██║\n", style="bold yellow")
#             ascii_text.append("╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═╝\n", style="bold green")
            
#             panel = Panel(
#                 Align.center(ascii_text),
#                 title="[bold yellow]🎴 Card Generator 🎴[/bold yellow]",
#                 subtitle="[italic cyan]⚡ Catch 'Em All in Cards! ⚡[/italic cyan]",
#                 border_style="bright_blue",
#                 padding=(1, 2)
#             )
#             self.console.print(panel)
#         else:
#             # Fallback ASCII art
#             print("""
#     ╔═══════════════════════════════════════════════════════════════╗
#     ║    ██████╗ ██╗  ██╗███╗   ███╗███╗   ██╗ ██████╗██╗     ██╗   ║
#     ║    ██╔══██╗██║ ██╔╝████╗ ████║████╗  ██║██╔════╝██║     ██║   ║
#     ║    ██████╔╝█████╔╝ ██╔████╔██║██╔██╗ ██║██║     ██║     ██║   ║
#     ║    ██╔═══╝ ██╔═██╗ ██║╚██╔╝██║██║╚██╗██║██║     ██║     ██║   ║
#     ║    ██║     ██║  ██╗██║ ╚═╝ ██║██║ ╚████║╚██████╗███████╗██║   ║
#     ║    ╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═╝   ║
#     ║                     🎴 Card Generator 🎴                      ║
#     ║                    ⚡ Catch 'Em All in Cards! ⚡              ║
#     ╚═══════════════════════════════════════════════════════════════╝
#             """)

#     def display_stats(self, data, species):
#         """Display Pkmn stats in a colorful table"""
#         if not RICH_AVAILABLE:
#             self.display_stats_basic(data, species)
#             return

#         # Create main info table
#         info_table = Table(title=f"[bold cyan]{data['name'].title()}[/bold cyan] - #{data['id']:03d}", 
#                           show_header=False, border_style="bright_blue")
#         info_table.add_column("Property", style="bold yellow", width=15)
#         info_table.add_column("Value", style="bright_white")

#         # Basic info
#         types = [t["type"]["name"].title() for t in data["types"]]
#         type_colors = {"Fire": "red", "Water": "blue", "Grass": "green", "Electric": "yellow", 
#                       "Psychic": "magenta", "Ice": "cyan", "Dragon": "purple", "Dark": "bright_black"}
        
#         colored_types = []
#         for pkmn_type in types:
#             color = type_colors.get(pkmn_type, "white")
#             colored_types.append(f"[{color}]{pkmn_type}[/{color}]")
        
#         info_table.add_row("Height", f"{data['height']/10:.1f} m")
#         info_table.add_row("Weight", f"{data['weight']/10:.1f} kg")
#         info_table.add_row("Types", " / ".join(colored_types))
#         info_table.add_row("Base EXP", str(data['base_experience']))

#         # Stats table
#         stats_table = Table(title="[bold green]Base Stats[/bold green]", border_style="bright_green")
#         stats_table.add_column("Stat", style="bold cyan", width=12)
#         stats_table.add_column("Value", style="bold white", width=8)
#         stats_table.add_column("Bar", width=25)

#         stats_map = {
#             'hp': ('HP', 'red'),
#             'attack': ('Attack', 'bright_red'),
#             'defense': ('Defense', 'blue'),
#             'special-attack': ('Sp. Atk', 'magenta'),
#             'special-defense': ('Sp. Def', 'cyan'),
#             'speed': ('Speed', 'yellow')
#         }

#         for stat in data['stats']:
#             stat_name = stat['stat']['name']
#             stat_value = stat['base_stat']
#             display_name, color = stats_map.get(stat_name, (stat_name.title(), 'white'))
            
#             # Create a visual bar
#             bar_length = min(int(stat_value / 5), 25)  # Scale down for display
#             bar = f"[{color}]{'█' * bar_length}{'░' * (25 - bar_length)}[/{color}]"
            
#             stats_table.add_row(display_name, str(stat_value), bar)

#         # Abilities
#         abilities = [ability["ability"]["name"].replace("-", " ").title() for ability in data["abilities"]]
#         abilities_text = Text("Abilities: ", style="bold yellow")
#         abilities_text.append(" / ".join(abilities), style="bright_white")

#         # Layout
#         self.console.print()
#         self.console.print(Panel(info_table, border_style="bright_blue", padding=(0, 1)))
#         self.console.print(Panel(stats_table, border_style="bright_green", padding=(0, 1)))
#         self.console.print(Panel(abilities_text, border_style="bright_yellow", padding=(0, 1)))

#     def display_stats_basic(self, data, species):
#         """Fallback stats display without rich"""
#         print(f"\n{'='*60}")
#         print(f"📊 {data['name'].title()} - #{data['id']:03d}")
#         print(f"{'='*60}")
#         print(f"Height: {data['height']/10:.1f} m")
#         print(f"Weight: {data['weight']/10:.1f} kg")
        
#         types = [t["type"]["name"].title() for t in data["types"]]
#         print(f"Types: {' / '.join(types)}")
#         print(f"Base EXP: {data['base_experience']}")
        
#         print(f"\n📈 Base Stats:")
#         print("-" * 30)
#         for stat in data['stats']:
#             stat_name = stat['stat']['name'].replace('-', ' ').title()
#             stat_value = stat['base_stat']
#             bar = '█' * (stat_value // 10) + '░' * (15 - stat_value // 10)
#             print(f"{stat_name:12} {stat_value:3d} {bar}")
        
#         abilities = [ability["ability"]["name"].replace("-", " ").title() for ability in data["abilities"]]
#         print(f"\n🎯 Abilities: {' / '.join(abilities)}")
#         print(f"{'='*60}")

#     def show_interactive_menu(self):
#         """Show interactive menu with arrow key navigation"""
#         if not RICH_AVAILABLE or not KEYBOARD_AVAILABLE:
#             return self.show_basic_menu()

#         self.console.print("\n[bold cyan]Use ↑↓ arrow keys to navigate, Enter to select, Esc to exit[/bold cyan]")
        
#         while True:
#             self.console.clear()
#             self.display_ascii_art()
            
#             # Create menu
#             menu_table = Table(show_header=False, border_style="bright_blue", padding=(0, 2))
#             menu_table.add_column("Option", justify="left")
            
#             for i, option in enumerate(self.menu_options):
#                 if i == self.current_selection:
#                     menu_table.add_row(f"[bold green]► {option}[/bold green]")
#                 else:
#                     menu_table.add_row(f"  {option}")
            
#             panel = Panel(menu_table, title="[bold yellow]Main Menu[/bold yellow]", 
#                          border_style="bright_blue")
#             self.console.print(Align.center(panel))
            
#             # Handle input
#             try:
#                 event = keyboard.read_event()
#                 if event.event_type == keyboard.KEY_DOWN:
#                     if event.name == 'up':
#                         self.current_selection = (self.current_selection - 1) % len(self.menu_options)
#                     elif event.name == 'down':
#                         self.current_selection = (self.current_selection + 1) % len(self.menu_options)
#                     elif event.name == 'enter':
#                         return self.current_selection
#                     elif event.name == 'esc':
#                         return 3  # Exit
#             except:
#                 # Fallback to basic menu if keyboard events fail
#                 return self.show_basic_menu()

#     def show_basic_menu(self):
#         """Fallback menu without arrow keys"""
#         if RICH_AVAILABLE:
#             menu_table = Table(title="[bold yellow]Main Menu[/bold yellow]", border_style="bright_blue")
#             menu_table.add_column("Option", style="bold cyan", width=5)
#             menu_table.add_column("Description", style="bright_white")
            
#             for i, option in enumerate(self.menu_options):
#                 menu_table.add_row(str(i + 1), option)
            
#             self.console.print(Align.center(menu_table))
#             choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"], default="1")
#             return int(choice) - 1
#         else:
#             print("\n" + "="*60)
#             print("Main Menu:")
#             for i, option in enumerate(self.menu_options):
#                 print(f"{i + 1}. {option}")
#             print("="*60)
            
#             while True:
#                 try:
#                     choice = input("\nChoose an option (1-4): ").strip()
#                     if choice in ["1", "2", "3", "4"]:
#                         return int(choice) - 1
#                     else:
#                         print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
#                 except KeyboardInterrupt:
#                     return 3

#     def get_random_pkmn(self):
#         """Get a random Pkmn from the API"""
#         try:
#             random_id = random.randint(1, 1010)
#             import requests
#             res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{random_id}")
#             if res.status_code == 200:
#                 return res.json()["name"]
#             else:
#                 return random.choice(finder.finder.name_list)
#         except Exception as e:
#             if RICH_AVAILABLE:
#                 self.console.print(f"[red]⚠️  Error getting random Pkmn: {e}[/red]")
#             else:
#                 print(f"⚠️  Error getting random Pkmn: {e}")
#             return "pikachu"

#     def prompt_pkmn_name(self):
#         """Prompt user for Pkmn name"""
#         if RICH_AVAILABLE:
#             self.console.print(Panel(
#                 "[cyan]Enter a Pkmn name to search for:\n"
#                 "[yellow]Examples:[/yellow] pikachu, charizard, gengar, lucario...",
#                 title="[bold green]🔍 Search Pkmn[/bold green]",
#                 border_style="green"
#             ))
#             return Prompt.ask("➤ Pkmn name").strip()
#         else:
#             print("\n🔍 Enter a Pkmn name:")
#             print("📝 Examples: pikachu, charizard, gengar, lucario...")
#             return input("➤ Pkmn name: ").strip()

#     def generate_pkmn_card(self, pkmn_name):
#         """Generate a Pkmn card with progress indication"""
#         if RICH_AVAILABLE:
#             with Progress(
#                 SpinnerColumn(),
#                 TextColumn("[progress.description]{task.description}"),
#                 console=self.console,
#             ) as progress:
#                 task1 = progress.add_task("🔎 Searching for Pkmn...", total=None)
                
#                 # Find closest match
#                 actual_name = finder.finder.find_closest(pkmn_name)
                
#                 if not actual_name:
#                     self.console.print(f"[red]❌ Couldn't find a match for '{pkmn_name}'.[/red]")
#                     self.console.print("[yellow]💡 Try checking the spelling or try a different Pkmn![/yellow]")
#                     return False
                
#                 progress.update(task1, description="📡 Fetching data from API...")
                
#                 try:
#                     data, species = api.pokeapi.fetch_pokemon(actual_name)
#                     self.last_pkmn_data = data
#                     self.last_species_data = species
                    
#                     progress.update(task1, description="🎨 Generating card...")
#                     card.generate(data, species)
                    
#                     progress.update(task1, description="✅ Complete!", completed=True)
                
#                 except Exception as e:
#                     self.console.print(f"[red]❌ Error generating card: {e}[/red]")
#                     return False
            
#             self.console.print(f"[green]🎉 SUCCESS! Card generated for {actual_name.title()}![/green]")
#             self.console.print(f"[cyan]📁 Check the 'output' folder: {actual_name.lower()}.png[/cyan]")
            
#             # Show stats
#             self.display_stats(data, species)
#             return True
#         else:
#             # Basic version
#             print(f"\n🔎 Searching for '{pkmn_name}'...")
#             actual_name = finder.finder.find_closest(pkmn_name)
            
#             if not actual_name:
#                 print(f"❌ Couldn't find a match for '{pkmn_name}'.")
#                 return False
            
#             print(f"📡 Fetching data...")
#             try:
#                 data, species = api.pokeapi.fetch_pokemon(actual_name)
#                 self.last_pkmn_data = data
#                 self.last_species_data = species
                
#                 print(f"🎨 Generating card...")
#                 card.generate(data, species)
                
#                 print(f"🎉 SUCCESS! Card generated for {actual_name.title()}!")
#                 print(f"📁 Check the 'output' folder: {actual_name.lower()}.png")
                
#                 self.display_stats(data, species)
#                 return True
#             except Exception as e:
#                 print(f"❌ Error generating card: {e}")
#                 return False

#     def run(self):
#         """Main application loop"""
#         if RICH_AVAILABLE:
#             self.console.clear()
        
#         self.display_ascii_art()
        
#         if RICH_AVAILABLE:
#             welcome_text = Text()
#             welcome_text.append("Welcome to ", style="bright_white")
#             welcome_text.append("PkmnCLI", style="bold cyan")
#             welcome_text.append("! 🌟\n", style="bright_white")
#             welcome_text.append("Generate beautiful Pkmn trading cards with colorful stats!", style="italic yellow")
            
#             self.console.print(Panel(welcome_text, border_style="bright_green", padding=(1, 2)))
#         else:
#             print("Welcome to PkmnCLI! 🌟")
#             print("Generate beautiful Pkmn trading cards!")
        
#         while True:
#             try:
#                 choice = self.show_interactive_menu()
                
#                 if choice == 0:  # Random Pkmn
#                     random_pkmn = self.get_random_pkmn()
#                     if RICH_AVAILABLE:
#                         self.console.print(f"[yellow]🎲 Random Pkmn selected: {random_pkmn.title()}[/yellow]")
#                     else:
#                         print(f"🎲 Random Pkmn selected: {random_pkmn.title()}")
#                     self.generate_pkmn_card(random_pkmn)
                    
#                 elif choice == 1:  # Search Pkmn
#                     pkmn_name = self.prompt_pkmn_name()
#                     if pkmn_name:
#                         self.generate_pkmn_card(pkmn_name)
                    
#                 elif choice == 2:  # View Last Stats
#                     if self.last_pkmn_data:
#                         self.display_stats(self.last_pkmn_data, self.last_species_data)
#                     else:
#                         if RICH_AVAILABLE:
#                             self.console.print("[yellow]📊 No Pkmn data available. Generate a card first![/yellow]")
#                         else:
#                             print("📊 No Pkmn data available. Generate a card first!")
                    
#                 elif choice == 3:  # Exit
#                     if RICH_AVAILABLE:
#                         self.console.print("[green]👋 Thanks for using PkmnCLI![/green]")
#                         self.console.print("[cyan]🎴 Keep collecting those cards! 🎴[/cyan]")
#                     else:
#                         print("👋 Thanks for using PkmnCLI!")
#                         print("🎴 Keep collecting those cards! 🎴")
#                     sys.exit(0)
                
#                 # Wait for user input to continue
#                 if RICH_AVAILABLE:
#                     Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
#                 else:
#                     input("\nPress Enter to continue...")
                    
#             except KeyboardInterrupt:
#                 if RICH_AVAILABLE:
#                     self.console.print("\n[yellow]⚡ Interrupted by user[/yellow]")
#                     self.console.print("[green]👋 Thanks for using PkmnCLI![/green]")
#                 else:
#                     print("\n⚡ Interrupted by user")
#                     print("👋 Thanks for using PkmnCLI!")
#                 sys.exit(0)

# def main():
#     """Entry point"""
#     cli = PkmnCLI()
#     cli.run()

# if __name__ == "__main__":
#     main()