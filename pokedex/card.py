from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO
import os

TYPE_COLORS = {
    "electric": "#FFEA70",
    "normal": "#B09398",
    "fire": "#FF675C",
    "water": "#0596C7",
    "ice": "#AFEAFD",
    "rock": "#999799",
    "flying": "#7AE7C7",
    "grass": "#4A9681",
    "psychic": "#FFC6D9",
    "ghost": "#561D25",
    "bug": "#A2FAA3",
    "poison": "#795663",
    "ground": "#D2B074",
    "dragon": "#DA627D",
    "steel": "#1D8A99",
    "fighting": "#2F2F2F",
    "default": "#2A1A1F"
}

class CardGenerator:
    def __init__(self):
        self.font_path = os.path.join(os.path.dirname(__file__), "assets", "BebasNeue-Regular.ttf")
        self.output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
        os.makedirs(self.output_dir, exist_ok=True)

    @staticmethod
    def darken_hex(hex_color, factor=0.6):
        rgb = tuple(int(hex_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        return tuple(int(c * factor) for c in rgb)

    def draw_text(self, draw, text, xy, font_size=20, fill=(0, 0, 0), align="left", bold=False):
        font = ImageFont.truetype(self.font_path, font_size)
        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        x, y = xy
        if align == "center":
            x -= w // 2
        elif align == "right":
            x -= w
        draw.text((x, y), text, fill=fill, font=font)

    def generate(self, data, species):
        width, height = 400, 700
        types = [t["type"]["name"] for t in data["types"]]
        primary_type = types[0] if types else "default"
        bg_color = TYPE_COLORS.get(primary_type, TYPE_COLORS["default"])
        dot_color = self.darken_hex(bg_color)

        card = Image.new("RGB", (width, height), "#F5F5F5")
        draw = ImageDraw.Draw(card)

        border_width = 6
        draw.rectangle([(0, 0), (width - 1, height - 1)], outline="black", width=border_width)

        name = data['name'].upper()
        sprite_url = data['sprites']['front_default']
        number = data['id']
        type_ = primary_type.upper()

        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}

        # Font sizes
        name_font = 28
        type_font = 20
        stat_font = 16
        number_font = 16

        margin = border_width + 15
        current_y = margin

        # Pokémon Name
        self.draw_text(draw, name, (width // 2, current_y), font_size=name_font, fill="black", align="center", bold=True)
        current_y += 40

        # Type Box
        type_box_height = 35
        draw.rectangle([(margin, current_y), (width - margin, current_y + type_box_height)],
                       fill="#CCCCCC", outline="black", width=2)
        self.draw_text(draw, type_, (width // 2, current_y + 8), font_size=type_font,
                       fill="black", align="center", bold=True)
        current_y += type_box_height + 20

        # Divider
        draw.rectangle([(margin, current_y), (width - margin, current_y + 4)], fill="black")
        current_y += 20

        # Sprite Box with dotted background
        sprite_box_size = 180
        sprite_x = (width - sprite_box_size) // 2
        sprite_y = current_y

        if sprite_url:
            try:
                sprite_img = Image.open(BytesIO(requests.get(sprite_url).content)).convert("RGBA")
                sprite_bg = Image.new("RGB", (sprite_box_size, sprite_box_size), bg_color)
                sprite_bg_draw = ImageDraw.Draw(sprite_bg)

                for y in range(0, sprite_box_size, 10):
                    for x in range((y // 10) % 2 * 5, sprite_box_size, 10):
                        sprite_bg_draw.ellipse((x, y, x + 2, y + 2), fill=dot_color)

                sprite_size = sprite_box_size - 20
                sprite_img = sprite_img.resize((sprite_size, sprite_size), Image.Resampling.LANCZOS)
                sprite_bg.paste(sprite_img,
                                ((sprite_box_size - sprite_size) // 2, (sprite_box_size - sprite_size) // 2),
                                sprite_img)

                card.paste(sprite_bg, (sprite_x, sprite_y))
                draw.rectangle([(sprite_x, sprite_y), (sprite_x + sprite_box_size, sprite_y + sprite_box_size)],
                               outline="black", width=3)
            except:
                self.draw_text(draw, "NO IMAGE", (width // 2, sprite_y + sprite_box_size // 2),
                               font_size=18, fill="black", align="center")

        current_y += sprite_box_size + 20

        # Divider
        draw.rectangle([(margin, current_y), (width - margin, current_y + 4)], fill="black")
        current_y += 20

        # Pokémon Number
        self.draw_text(draw, f"No. {number:03d}", (width // 2, current_y),
                       font_size=number_font, fill="black", align="center", bold=True)
        current_y += 30

        # Stats Header
        self.draw_text(draw, "STATS", (width // 2, current_y), font_size=type_font,
                       fill="black", align="center", bold=True)
        current_y += 30

        # Stats with alternating background
        row_height = 22
        label_map = {
            'hp': 'HP',
            'attack': 'ATTACK',
            'defense': 'DEFENSE',
            'special-attack': 'SP.ATK',
            'special-defense': 'SP.DEF',
            'speed': 'SPEED'
        }

        for i, (key, value) in enumerate(stats.items()):
            y_pos = current_y + i * row_height
            if i % 2 == 0:
                draw.rectangle([(margin, y_pos - 1), (width - margin, y_pos + row_height - 1)], fill="#E5E5E5")
            label = label_map.get(key, key.replace('-', ' ').upper())
            self.draw_text(draw, label, (margin + 10, y_pos + 2), font_size=stat_font, fill="black")
            self.draw_text(draw, str(value), (width - margin - 10, y_pos + 2),
                           font_size=stat_font, fill="black", align="right", bold=True)

        # Save
        output_path = os.path.join(self.output_dir, f"{data['name'].lower()}_brutalist.png")
        card.save(output_path)
        print(f"Saved brutalist card: {output_path}")


# Export singleton
card = CardGenerator()


# from PIL import Image, ImageDraw, ImageFont, ImageOps
# import requests
# from io import BytesIO
# import os

# TYPE_COLORS = {
#     "electric": "#FFEA70",
#     "normal": "#B09398",
#     "fire": "#FF675C",
#     "water": "#0596C7",
#     "ice": "#AFEAFD",
#     "rock": "#999799",
#     "flying": "#7AE7C7",
#     "grass": "#4A9681",
#     "psychic": "#FFC6D9",
#     "ghost": "#561D25",
#     "bug": "#A2FAA3",
#     "poison": "#795663",
#     "ground": "#D2B074",
#     "dragon": "#DA627D",
#     "steel": "#1D8A99",
#     "fighting": "#2F2F2F",
#     "default": "#2A1A1F"
# }

# class CardGenerator:
#     def __init__(self):
#         self.font_path = os.path.join(os.path.dirname(__file__), "assets", "BebasNeue-Regular.ttf")
#         self.output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
#         os.makedirs(self.output_dir, exist_ok=True)

#     def draw_text(self, draw, text, xy, font_size=20, fill=(0, 0, 0), align="left", bold=False):
#         font = ImageFont.truetype(self.font_path, font_size)
    
#         # Calculate text width and height using bounding box
#         bbox = font.getbbox(text)
#         w = bbox[2] - bbox[0]
#         h = bbox[3] - bbox[1]
    
#         x, y = xy
#         if align == "center":
#             x -= w // 2
#         elif align == "right":
#             x -= w
    
#         # # For bold effect, draw text multiple times with slight offset
#         # if bold:
#         #     for offset_x in range(-1, 2):
#         #         for offset_y in range(-1, 2):
#         #             if offset_x != 0 or offset_y != 0:
#         #                 draw.text((x + offset_x, y + offset_y), text, fill=fill, font=font)
        
#         draw.text((x, y), text, fill=fill, font=font)

    
    
#     def generate(self, data, species):
#         width, height = 400, 700  # Increased height to prevent cutoff

#         types = [t["type"]["name"] for t in data["types"]]
#         primary_type = types[0] if types else "default"
#         bg_color = TYPE_COLORS.get(primary_type, TYPE_COLORS["default"])

#         # Brutalist color scheme: white background, black text, grey accents
#         card = Image.new("RGB", (width, height), "#F5F5F5")  # Light grey background
#         draw = ImageDraw.Draw(card)

#         # Draw thick black border
#         border_width = 6
#         draw.rectangle([(0, 0), (width-1, height-1)], outline="black", width=border_width)

#         name = data['name'].upper()  # Uppercase for brutalist feel
#         sprite_url = data['sprites']['front_default']
#         number = data['id']
#         type_ = primary_type.upper()

#         stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}

#         # Font sizes - optimized for layout
#         name_font = 28
#         type_font = 20
#         stat_font = 16
#         label_font = 18
#         number_font = 16

#         margin = border_width + 15
#         current_y = margin

#         # Draw Pokémon Name - large, bold, black
#         self.draw_text(draw, name, (width//2, current_y), font_size=name_font, fill="black", align="center", bold=True)
#         current_y += 40

#         # Draw Type in a grey box
#         type_box_height = 35
#         draw.rectangle([(margin, current_y), (width - margin, current_y + type_box_height)], 
#                       fill="#CCCCCC", outline="black", width=2)
#         self.draw_text(draw, type_, (width//2, current_y + 8), font_size=type_font, fill="black", align="center", bold=True)
#         current_y += type_box_height + 20

#         # Thick horizontal divider
#         draw.rectangle([(margin, current_y), (width - margin, current_y + 4)], fill="black")
#         current_y += 20

#         # Draw sprite in a contained box with high contrast
#         sprite_box_size = 180
#         sprite_x = (width - sprite_box_size) // 2
#         sprite_y = current_y

#         # Create white background box for sprite
#         if sprite_url:
#             try:
#                 sprite_img = Image.open(BytesIO(requests.get(sprite_url).content)).convert("RGBA")

#                 # Create sprite background with dotted pattern
#                 sprite_bg_size = sprite_box_size
#                 sprite_bg = Image.new("RGB", (sprite_bg_size, sprite_bg_size), bg_color)
#                 sprite_bg_draw = ImageDraw.Draw(sprite_bg)

#                 for y in range(0, sprite_bg_size, 10):
#                     for x in range((y // 10) % 2 * 5, sprite_bg_size, 10):
#                         sprite_bg_draw.ellipse((x, y, x+2, y+2), fill=(200, 0, 0))

#                 # Resize and paste the sprite
#                 sprite_size = sprite_bg_size - 20
#                 sprite_img = sprite_img.resize((sprite_size, sprite_size), Image.Resampling.LANCZOS)
#                 sprite_bg.paste(sprite_img, ((sprite_bg_size - sprite_size) // 2, (sprite_bg_size - sprite_size) // 2), sprite_img)

#                 # Paste the entire sprite block onto the card with black border
#                 card.paste(sprite_bg, (sprite_x, sprite_y))
#                 draw.rectangle([(sprite_x, sprite_y), (sprite_x + sprite_box_size, sprite_y + sprite_box_size)], 
#                     outline="black", width=3)
#             except:
#                 self.draw_text(draw, "NO IMAGE", (width//2, sprite_y + sprite_box_size//2), 
#                     font_size=18, fill="black", align="center")
        



#         current_y += sprite_box_size + 20

#         # Another thick horizontal divider
#         draw.rectangle([(margin, current_y), (width - margin, current_y + 4)], fill="black")
#         current_y += 20

#         # Pokémon Number
#         self.draw_text(draw, f"No. {number:03d}", (width//2, current_y), font_size=number_font, 
#                       fill="black", align="center", bold=True)
#         current_y += 30

#         # Stats header
#         self.draw_text(draw, "STATS", (width//2, current_y), font_size=type_font, 
#                       fill="black", align="center", bold=True)
#         current_y += 30

#         # Stats with alternating background
#         row_height = 22
#         for i, (key, value) in enumerate(stats.items()):
#             y_pos = current_y + i * row_height
            
#             # Alternating grey background for readability
#             if i % 2 == 0:
#                 draw.rectangle([(margin, y_pos - 1), (width - margin, y_pos + row_height - 1)], 
#                               fill="#E5E5E5")
            
#             # Shorten stat names to fit better
#             label_map = {
#                 'hp': 'HP',
#                 'attack': 'ATTACK', 
#                 'defense': 'DEFENSE',
#                 'special-attack': 'SP.ATK',
#                 'special-defense': 'SP.DEF',
#                 'speed': 'SPEED'
#             }
            
#             label = label_map.get(key, key.replace('-', ' ').upper())
#             self.draw_text(draw, label, (margin + 10, y_pos + 2), font_size=stat_font, fill="black")
#             self.draw_text(draw, str(value), (width - margin - 10, y_pos + 2), font_size=stat_font, 
#                           fill="black", align="right", bold=True)

#         # Save card
#         output_path = os.path.join(self.output_dir, f"{data['name'].lower()}_brutalist.png")
#         card.save(output_path)
#         print(f"Saved brutalist card: {output_path}")

# # Export singleton
# card = CardGenerator()



# ------------ Previous Card

# from PIL import Image, ImageDraw, ImageFont, ImageOps
# import requests
# from io import BytesIO
# import os

# TYPE_COLORS = {
#     "electric": "#FFEA70",
#     "normal": "#B09398",
#     "fire": "#FF675C",
#     "water": "#0596C7",
#     "ice": "#AFEAFD",
#     "rock": "#999799",
#     "flying": "#7AE7C7",
#     "grass": "#4A9681",
#     "psychic": "#FFC6D9",
#     "ghost": "#561D25",
#     "bug": "#A2FAA3",
#     "poison": "#795663",
#     "ground": "#D2B074",
#     "dragon": "#DA627D",
#     "steel": "#1D8A99",
#     "fighting": "#2F2F2F",
#     "default": "#2A1A1F"
# }

# class CardGenerator:
#     def __init__(self):
#         self.font_path = os.path.join(os.path.dirname(__file__), "assets", "VT323-Regular.ttf")
#         self.output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
#         os.makedirs(self.output_dir, exist_ok=True)

#     def draw_text(self, draw, text, xy, font_size=20, fill=(0, 0, 0), align="left"):
#         font = ImageFont.truetype(self.font_path, font_size)
    
#         # Calculate text width and height using bounding box
#         bbox = font.getbbox(text)
#         w = bbox[2] - bbox[0]
#         h = bbox[3] - bbox[1]
    
#         x, y = xy
#         if align == "center":
#             x -= w // 2
#         elif align == "right":
#             x -= w
    
#         draw.text((x, y), text, fill=fill, font=font)


#     def generate(self, data, species):
#         width, height = 300, 450

#         types = [t["type"]["name"] for t in data["types"]]
#         primary_type = types[0] if types else "default"
#         bg_color = TYPE_COLORS.get(primary_type, TYPE_COLORS["default"])

#         card = Image.new("RGB", (width, height), "white")
#         draw = ImageDraw.Draw(card)

#         name = data['name'].capitalize()
#         sprite_url = data['sprites']['front_default']
#         number = data['id']
#         type_ = primary_type

#         stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}

#         # Font sizes
#         name_font = 26
#         stat_font = 20
#         label_font = 22

#         # Draw Pokémon Name
#         self.draw_text(draw, name, (width//2, 20), font_size=name_font, fill=(0, 0, 0), align="center")

#         # Draw sprite with dotted red background (sprite larger, box same size)
#         if sprite_url:
#             sprite_img = Image.open(BytesIO(requests.get(sprite_url).content)).convert("RGBA")
#             sprite_bg = Image.new("RGB", (150, 150), bg_color)
#             sprite_bg_draw = ImageDraw.Draw(sprite_bg)

#             for y in range(0, 150, 10):
#                 for x in range((y // 10) % 2 * 5, 150, 10):
#                     sprite_bg_draw.ellipse((x, y, x+2, y+2), fill=(200, 0, 0))

#             sprite_img = sprite_img.resize((130, 130), Image.Resampling.LANCZOS)
#             sprite_bg.paste(sprite_img, ((150 - 130)//2, (150 - 130)//2), sprite_img)
#             card.paste(sprite_bg, (75, 50))

#         # Number
#         self.draw_text(draw, f"No. {number}", (width//2, 210), font_size=label_font, align="center")

#         # Type box
#         type_box_y = 240
#         draw.rectangle([(50, type_box_y), (250, type_box_y + 30)], outline="gray", width=1)
#         self.draw_text(draw, type_, (width//2, type_box_y + 5), font_size=label_font, fill=(220, 70, 70), align="center")

#         # Stats section
#         start_y = 290
#         gap = 25
#         for i, (key, value) in enumerate(stats.items()):
#             label = key.replace('-', ' ').lower()
#             self.draw_text(draw, f"{label}", (30, start_y + i*gap), font_size=stat_font)
#             self.draw_text(draw, f"{value}", (220, start_y + i*gap), font_size=stat_font)

#         # Save card
#         output_path = os.path.join(self.output_dir, f"{name.lower()}.png")
#         card.save(output_path)
#         print(f"Saved: {output_path}")

# # Export singleton
# card = CardGenerator()