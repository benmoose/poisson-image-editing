import numpy as np
from PIL import Image, ImageDraw

from ..utils.img_dir import save_image, clean_img_dir


def _generate_a_b(labelled_pixels, im_size):
    """Generate matrix and column vector for region"""
    im_width, im_height = im_size
    # Count the number of pixels in the region
    region_length = sum(map(lambda p: 1 if p[1] == 0 else 0, labelled_pixels))
    # Initialise the matrix and column vector
    A = np.zeros((region_length, region_length))
    b = np.zeros(region_length)
    # Record the number of region pixels encountered
    k_pos = 0
    # Record the k_pos for pixels in region
    region_pixel_k_pos = {}
    # Iterate over each pixel in the image
    for index, pixel in enumerate(labelled_pixels):
        _, alpha = pixel
        in_region = alpha == 0

        def get_neighbour_labels():
            index_in_row = index % im_width
            left = 1 if index_in_row - 1 >= 0 else 0
            right = 1 if index_in_row + 1 < im_width else 0
            top = 1 if index >= im_width else 0
            bottom = 1 if index < len(labelled_pixels) - im_width else 0
            return top, right, bottom, left

        top_n, right_n, bottom_n, left_n = get_neighbour_labels()
        neighbour_count = top_n + right_n + bottom_n + left_n

        if in_region:
            region_pixel_k_pos[index] = k_pos
            # Add number of neighbours to A
            A[k_pos, k_pos] = neighbour_count
            # Add top and left neighbour pixels to A
            if top_n:
                try:
                    # check neighbour is in region
                    n_k_pos = region_pixel_k_pos[index - im_width]
                    A[k_pos, n_k_pos] = -1
                    A[n_k_pos, k_pos] = -1
                except KeyError:
                    # Not in region
                    pass
            if left_n:
                try:
                    # check neighbour is in region
                    n_k_pos = region_pixel_k_pos[index - 1]
                    A[k_pos, n_k_pos] = -1
                    A[n_k_pos, k_pos] = -1
                except KeyError:
                    # Not in region
                    pass
            # Check if any neighbours are non region pixels (a.k.a on boundary)
            # and if so sum them and add to b
            b_value = 0
            if top_n:
                n_intensity, n_alpha = labelled_pixels[index - im_width]
                if n_alpha != 0:
                    b_value += n_intensity
            if right_n:
                n_intensity, n_alpha = labelled_pixels[index + 1]
                if n_alpha != 0:
                    b_value += n_intensity
            if bottom_n:
                n_intensity, n_alpha = labelled_pixels[index + im_width]
                if n_alpha != 0:
                    b_value += n_intensity
            if left_n:
                n_intensity, n_alpha = labelled_pixels[index - 1]
                if n_alpha != 0:
                    b_value += n_intensity
            if b_value > 0:
                b[k_pos] = b_value
            k_pos += 1

    return A, b


def _generate_filled_pixels(labelled_pixels, x):
    k_pos = 0
    result = np.copy(labelled_pixels).astype(np.uint8)
    for index, pixel in enumerate(labelled_pixels):
        _, alpha = pixel
        if alpha == 0:
            result[index] = int(x[k_pos]), 255
            k_pos += 1
    return result


def task1(image, region):
    """
    Takes an image and a region and returns the image with the region filled in
    with the results of Eq(2)
    """
    # Clean task 1 img dir (silently fail)
    try:
        clean_img_dir('t1')
    except:
        pass
    # Convert to greyscale
    image = image.convert('L')
    # Create b/w mask of region
    mask = Image.new('L', image.size, 255)
    ImageDraw.Draw(mask).polygon(region, fill=0, outline=0)
    # Remove region from image
    f_star = image.copy()
    # ImageDraw.Draw(f_star).polygon(region, fill=0)
    f_star.putalpha(mask)
    # Each pixel is a tuple (intensity, alpha)
    # alpha is either (0 = in region) or (255 = not in region)
    # from this can build matrix A and column vector b
    # Get pixels as 1D array
    f_star_pixels = list(f_star.getdata())
    # Create A and b
    A, b = _generate_a_b(f_star_pixels, image.size)
    x = np.linalg.solve(A, b)
    filled_pixels = _generate_filled_pixels(f_star_pixels, x)
    filled_image = np.reshape(filled_pixels, (image.height, image.width, 2))

    # Save result to `out`, returning path to image
    return save_image(
        Image.fromarray(filled_image, mode='LA'), 't1', name='t1')
