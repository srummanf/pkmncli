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

    @staticmethod
    def lighten_hex(hex_color, factor=1.5):
        """Create a lighter shade of the given hex color"""
        rgb = tuple(int(hex_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        lightened = tuple(min(255, int(c * factor)) for c in rgb)
        return lightened

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
        light_bg_color = self.lighten_hex(bg_color)

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

        # Type Box - now using lighter shade of bg_color
        type_box_height = 35
        draw.rectangle([(margin, current_y), (width - margin, current_y + type_box_height)],
                       fill=light_bg_color, outline="black", width=2)
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

                # Increased sprite size from sprite_box_size - 20 to sprite_box_size - 10
                sprite_size = sprite_box_size - 10
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
                draw.rectangle([(margin, y_pos - 1), (width - margin, y_pos + row_height - 1)], fill=light_bg_color)
            label = label_map.get(key, key.replace('-', ' ').upper())
            self.draw_text(draw, label, (margin + 10, y_pos + 2), font_size=stat_font, fill="black")
            self.draw_text(draw, str(value), (width - margin - 10, y_pos + 2),
                           font_size=stat_font, fill="black", align="right", bold=True)

        # Save
        output_path = os.path.join(self.output_dir, f"{data['name'].lower()}.png")
        card.save(output_path)
        print(f"Saved card: {output_path}")


# Export singleton
card = CardGenerator()