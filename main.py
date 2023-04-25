import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool, freeze_support
from tqdm import tqdm

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z**2 + c
        n += 1
    if n == max_iter:
        return 0
    else:
        return n

def calculate_row(args):
    row, width, height, max_iter, xmin, xmax, ymin, ymax = args
    c = np.linspace(xmin, xmax, width) + (row*np.ones(width)*((ymax-ymin)/height) + ymin)*1j
    result = np.zeros(width)
    for j in range(width):
        result[j] = mandelbrot(c[j], max_iter)
    return result

def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter, num_colors, color_map_name):
    pool = Pool()
    rows = list(tqdm(pool.imap(calculate_row, [(i, width, height, max_iter, xmin, xmax, ymin, ymax) for i in range(height)]), total=height))
    pool.close()
    pool.join()
    fractal = np.vstack(rows)
    # Map the fractal values to colors
    color_scale = np.linspace(0, 1, num_colors)
    color_map = plt.cm.get_cmap(color_map_name)(color_scale)
    colors = color_map[np.uint8(fractal / max_iter * (num_colors-1))]
    return colors

if __name__ == '__main__':
    xmin, xmax, ymin, ymax = -1.2, 1.2, -1.2, 1.2
    img_size = 1000
    max_iter = 1000
    num_colors = 256
    color_map_name = 'afmhot'

    freeze_support() # added this line

    colors = mandelbrot_set(xmin, xmax, ymin, ymax, img_size, img_size, max_iter, num_colors, color_map_name)

    fig, ax = plt.subplots(figsize=(10,10))
    ax.imshow(colors, extent=[xmin, xmax, ymin, ymax])
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()
