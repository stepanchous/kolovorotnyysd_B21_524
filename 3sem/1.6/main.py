import sys
import os
import numpy as np
from PIL import Image as pim

def rank_filter(image, rank):
    filtered_image = image.copy()

    padded_image = np.pad(image, (1, 1), 'edge')
    height, width = padded_image.shape

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            block = padded_image[i - 1 : i + 2, j - 1 : j + 2]
            white_count = np.count_nonzero(block)

            filtered_image[i - 1][j - 1] = (white_count >= rank) * 255
    
    return filtered_image
    
def main(argv: list[str]):
    if (len(argv) != 2):
        raise ValueError("Invalid number of arguments")
    
    path = argv[1]

    image = np.array(pim.open(path))

    filtered_image = rank_filter(image, 5)

    _, name = os.path.split(path)
    
    pim.fromarray(filtered_image).save(f'output/{name}')

if __name__ == "__main__":
    main(sys.argv)