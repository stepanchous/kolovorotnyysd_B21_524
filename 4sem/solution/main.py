import numpy as np
import sys
import os
from PIL import Image as pim

def rgb_to_grayscale(rgb_array):
    return  (0.3 * rgb_array[:, :, 0] + 
             0.59 * rgb_array[:, :, 1] + 
             0.11 * rgb_array[:, :, 2]).astype(np.uint8)

def calc_for_neighbors(padded_image, func):
    height, width = padded_image.shape

    res = np.zeros((height - 2, width - 2), dtype=np.int32)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            block = padded_image[i - 1 : i + 2, j - 1 : j + 2]

            res[i - 1][j - 1] = func(block)

    return (255 * res / np.max(res)).astype(np.uint8)

def find_edge(image, ker_x, ker_y, threshold):
    gs_image = rgb_to_grayscale(image)
    padded_image = np.pad(gs_image, (1, 1), 'edge')
    apply_grad = lambda block: (np.abs(np.sum(block * ker_x)) + 
                                np.abs(np.sum(block * ker_y)))
    
    grad = calc_for_neighbors(padded_image, apply_grad)

    return ((grad > 50) * 255).astype(np.uint8)

def main(argv: list[str]) -> None:
    if (len(argv) != 2):
        raise ValueError("Invalid number of arguments")
    
    path = argv[1]

    image = np.array(pim.open(path))

    ker_x = np.array([
        [-1, -1, -1],
        [ 0,  0,  0],
        [ 1,  1,  1]
    ])

    ker_y = np.array([
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]
    ])

    edge_image = find_edge(image, ker_x, ker_y, 60)

    _, name = os.path.split(path)
    
    pim.fromarray(edge_image).save(f'output/{name}')



if __name__ == "__main__":
    main(sys.argv)