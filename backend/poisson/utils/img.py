import numpy as np


def generate_filled_pixels(labelled_pixels, new_pixels):
    k_pos = 0
    result = np.copy(labelled_pixels).astype(np.uint8)
    for index, pixel in enumerate(labelled_pixels):
        _, alpha = pixel
        if alpha == 0:
            result[index] = int(max(min(new_pixels[k_pos], 255), 0)), 255
            k_pos += 1
    return result


def get_neighbour_labels(index, im_width, pixel_count):
    index_in_row = index % im_width
    left = 1 if index_in_row - 1 >= 0 else 0
    right = 1 if index_in_row + 1 < im_width else 0
    top = 1 if index >= im_width else 0
    bottom = 1 if index < pixel_count - im_width else 0
    return top, right, bottom, left
