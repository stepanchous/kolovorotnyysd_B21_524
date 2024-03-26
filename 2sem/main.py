import numpy as np
import sys
import os
from PIL import Image as pim

def rgb_to_grayscale(rgb_array):
    return  (0.3 * rgb_array[:, :, 0] + 
             0.59 * rgb_array[:, :, 1] + 
             0.11 * rgb_array[:, :, 2]).astype(np.uint8)

def wolf_binarization(grayscale, n=15, k=0.5, r=128):
    min_brightness = grayscale.min()
    height, width = grayscale.shape

    row_count = height // n if height % n == 0 else height // n + 1
    col_count = width // n if width % n == 0 else width // n + 1

    for i in range(row_count):
        for j in range(col_count):
            block = grayscale[i * n : (i + 1) * n, j * n : (j + 1) * n].view()
        
            m = block.mean()
            s = block.std()

            threshold = ((1 - k) * m +
                      k * min_brightness + 
                      k * s / r * (m - min_brightness))
        
            block[...] = block > threshold

    grayscale *= 255

    return grayscale.astype(np.uint8)


def main(argv: list[str]) -> None:
    if (len(argv) != 2):
        raise ValueError("Invalid number of arguments")
    
    path = argv[1]
    dir, name = os.path.split(argv[1])
    rgb_array = np.array(pim.open(path))

    grayscale = rgb_to_grayscale(rgb_array)
    gs_image = pim.fromarray(grayscale)
    gs_image.save(os.path.join(dir, "gs_" + name))

    bin_array = wolf_binarization(grayscale.copy())
    bin_image = pim.fromarray(bin_array)
    bin_image.save(os.path.join(dir, "bin_" + name))



if __name__ == "__main__":
    main(sys.argv)