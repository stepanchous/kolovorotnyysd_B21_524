from PIL import Image, ImageFont, ImageDraw
from functools import reduce
import numpy as np
from matplotlib import pyplot as plt

def generate_phrase(phrase, font_path, font_size):
    font = ImageFont.truetype(font_path, font_size)

    width = reduce(
    lambda acc, curr: acc + curr,
    map(lambda symbol: font.getbbox(symbol)[2], phrase),
    0)

    height = max(map(lambda symbol: font.getbbox(symbol)[3], phrase))

    width_padding = 60
    height_padding = 20

    image = Image.new("L", (width + width_padding, height + height_padding), color="white")
    draw = ImageDraw.Draw(image)
    draw.text((width_padding // 2, height_padding // 2), phrase, font=font, color="black")
    image.save("output/phrase.bmp")

def calc_profiles(image):
    image_array = np.array(image)
    bd_image = 1 - image_array / 255

    horizontal_profile = bd_image.sum(axis=1)
    vertical_profile = bd_image.sum(axis=0)

    return horizontal_profile, vertical_profile

def plot_profiles(horizontal_profile , vertical_profile, output):
    _, (horizontal, vertical) = plt.subplots(1, 2)

    vertical.bar(range(vertical_profile.size), vertical_profile)
    vertical.set_title("Vertical profile")

    horizontal.barh(range(horizontal_profile.size), horizontal_profile)
    horizontal.invert_yaxis()
    horizontal.set_title("Horizontal profile")

    plt.savefig(output)
    plt.close()

def find_symbol_ranges(vertical_profile):
    ranges = []

    l = 0

    while l < vertical_profile.size:
        while l < vertical_profile.size and vertical_profile[l] == 0:
            l += 1

        r = l

        while r < vertical_profile.size and vertical_profile[r] != 0:
            r += 1

        if (l != r):
            ranges.append((l - 1, r))

        l = r

    filtered_ranges = []

    for symbol_range in ranges:
        if len(filtered_ranges) == 0:
            filtered_ranges.append(symbol_range)
            continue

        if (symbol_range[0] - filtered_ranges[-1][1] < 3):
            filtered_ranges[-1] = (filtered_ranges[-1][0], symbol_range[1])
        else:
            filtered_ranges.append(symbol_range)
    
    return filtered_ranges

def find_top_bottom(horizontal_profile):
    top = 0
    bottom = 0

    for i in range(horizontal_profile.size):
        if horizontal_profile[i] != 0:
            bottom = i
            break

    for i in range(horizontal_profile.size - 1, -1, -1):
        if (horizontal_profile[i] != 0):
            top = i
            break

    return top, bottom

def segement_phrase(horizontal_profile, vertical_profile):
    ranges = find_symbol_ranges(vertical_profile)
    top, bottom = find_top_bottom(horizontal_profile)

    boxes = []

    for symbol_range in ranges:
        boxes.append([(symbol_range[0], bottom),
                      (symbol_range[1], bottom),
                      (symbol_range[0], top),
                      (symbol_range[1], top)])
        
    return boxes

def display_boxes(image_path, boxes):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for box in boxes:
        lb, rb, lt, rt = box

        draw.line((lb, rb), fill=(0), width=1)
        draw.line((rb, rt), fill=(0), width=1)
        draw.line((lt, rt), fill=(0), width=1)
        draw.line((lb, lt), fill=(0), width=1)

    image.save("output/boxed_symbols.bmp")

def crop_symbols(image, boxes):
    for i, box in enumerate(boxes):
        lb, _, _, rt = box

        symbol_image = image.crop((*lb, *rt))
        symbol_image.save(f"output/letters/letter_{i}.bmp")

def main():
    generate_phrase("если жена мешает преферансу бросай жену",
                    "font/CaskaydiaMonoNerdFont-Regular.ttf",
                    69)
    
    image = Image.open("output/phrase.bmp")
    
    horizontal_profile, vertical_profile = calc_profiles(image)
    plot_profiles(horizontal_profile, vertical_profile, "output/profiles.png")

    boxes = segement_phrase(horizontal_profile, vertical_profile)
    display_boxes("output/phrase.bmp", boxes)

    for i, box in enumerate(boxes):
        lb, _, _, rt = box

        letter_image = image.crop((*lb, *rt))
        letter_image.save(f"output/letters/letter_{i}.bmp")
        horizontal_profile, vertical_profile = calc_profiles(letter_image)

        plot_profiles(horizontal_profile, vertical_profile, f"output/letters/profile_{i}.png")

if __name__ == "__main__":
    main()