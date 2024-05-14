from PIL import Image as pim
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calc_black_weight(black_density):
    black_weight = np.sum(black_density)

    return black_weight, black_weight / black_density.size

def calc_black_weights(black_density):
    height, width = black_density.shape
    height_mid = height // 2
    width_mid = width // 2

    black_weights = list()
    norm_black_weights = list()


    top_left = black_density[:height_mid, :width_mid]
    top_right = black_density[:height_mid, width_mid:]
    bottom_left = black_density[height_mid:, :width_mid]
    bottom_right = black_density[height_mid:, width_mid:]

    black_weight, norm_black_weight = calc_black_weight(top_left)
    black_weights.append(black_weight)
    norm_black_weights.append(norm_black_weight)

    black_weight, norm_black_weight = calc_black_weight(top_right)
    black_weights.append(black_weight)
    norm_black_weights.append(norm_black_weight)

    black_weight, norm_black_weight = calc_black_weight(bottom_left)
    black_weights.append(black_weight)
    norm_black_weights.append(norm_black_weight)

    black_weight, norm_black_weight = calc_black_weight(bottom_right)
    black_weights.append(black_weight)
    norm_black_weights.append(norm_black_weight)


    return np.array(black_weights), np.array(norm_black_weights)

def calc_mass_center(black_density, black_weight):
    height, width = black_density.shape

    center_x = float(0)
    center_y = float(0)

    for x in range(height):
        for y in range(width):
            center_x += x * black_density[x][y]
            center_y += y * black_density[x][y]

    return center_x / black_weight, center_y / black_weight

def calc_horizontal_vertical_inertia_moments(black_density, center):
    height, width = black_density.shape
    x_center, y_center = center

    i_x = float(0)
    i_y = float(0)

    for x in range(height):
        for y in range(width):
            i_x += (y - y_center)**2 * black_density[x][y]
            i_y += (x - x_center)**2 * black_density[x][y]

    return i_x, i_y

def calc_profiles(black_density):
    height, width = black_density.shape

    x_profile = np.zeros(height)
    y_profile = np.zeros(width)

    for x in range(height):
        for y in range(width):
            x_profile[x] += black_density[x][y]
            y_profile[y] += black_density[x][y]
    
    return x_profile, y_profile

def main():
    letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

    report = pd.DataFrame(
        columns= ["Letter", "Black Weight Quoter", 
         "Normalized Black Weight Quoter", "Mass Center",
         "Normalized Mass Center", "Inertia Moments", 
         "Normalized Inertia Moments"])

    for i, letter in enumerate(letters):
        image = pim.open(f"../1.22/font/{letter}.png")
        image_array = np.array(image, dtype=np.uint8)
        black_density = 1 - image_array / 255
        height, width = black_density.shape

        quoter_black_weight, quoter_norm_black_weight = calc_black_weights(black_density)
        black_weight, norm_black_weight = calc_black_weight(black_density)
        mass_center = calc_mass_center(black_density, black_weight)
        norm_mass_center = (mass_center[0] / (height - 1), mass_center[1] / (width - 1))
        inertia_moments = calc_horizontal_vertical_inertia_moments(black_density, mass_center)
        norm_inertia_moments = (
            inertia_moments[0] / (height**2 * width**2),
            inertia_moments[1] / (height**2 * width**2)
        )

        row = {
            "Letter" : letter,
            "Black Weight Quoter" : quoter_black_weight,
            "Normalized Black Weight Quoter" : quoter_norm_black_weight,
            "Mass Center" : mass_center,
            "Normalized Mass Center" : norm_mass_center,
            "Inertia Moments" : inertia_moments,
            "Normalized Inertia Moments" : norm_inertia_moments,
        }

        print(row, end="\n\n")


if __name__ == "__main__":
    main()