from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from math import ceil

def main():
    height_padding = 5

    letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    font = ImageFont.truetype("font/CaskaydiaMonoNerdFont-Regular.ttf", 20)

    for letter in letters:
        _, _, width, height = font.getbbox(letter)


        print(height)
        print(font.getbbox(letter))
        print()

        image = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), letter, font=font, fill=(0, 0, 0))
        image.save(f"font/{letter}.png")

if __name__ == '__main__':
    main()