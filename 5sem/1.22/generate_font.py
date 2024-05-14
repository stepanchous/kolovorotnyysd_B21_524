from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from math import ceil

def main():
    letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    font = ImageFont.truetype("font/CaskaydiaMonoNerdFont-Regular.ttf", 69)

    for letter in letters:
        _, _, width, height = font.getbbox(letter)

        image = Image.new("L", (width, height), color="white")
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), letter, font=font, color="black")
        image.save(f"font/{letter}.png")

if __name__ == '__main__':
    main()