import numpy as np
from PIL import Image, ImageFilter

from ..utils.img_dir import clean_img_dir, save_image


def task5(image, region):
    # Clean img dir
    clean_img_dir('t5')
    image_edges = image.filter(
        ImageFilter.Kernel((3, 3), [0, -1, 0, -1, 4, -1, 0, -1, 0], scale=1))

    return save_image(image_edges, 't5')
