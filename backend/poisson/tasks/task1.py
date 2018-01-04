import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFilter

from ..utils.img_dir import save_image


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
    # Iterate over each pixel in the image
    for index, pixel in enumerate(labelled_pixels):
        intensity, alpha = pixel

        def get_neighbours_count():
            index_in_row = index % im_width
            left = 1 if index_in_row - 1 >= 0 else 0
            right = 1 if index_in_row + 1 < im_width else 0
            top = 1 if index >= im_width else 0
            bottom = 1 if index < len(labelled_pixels) - im_width else 0
            return sum([left, right, top, bottom])

        n = get_neighbours_count()

        if alpha == 0:
            # region pixel
            A[k_pos, k_pos] = n
            k_pos += 1

    return A, b


def task1(image, region):
    """
    Takes an image and a region and returns the image with the region filled in
    with the results of Eq(2)
    """
    image = image.convert('L')
    im_width, im_height = image.size

    # Create b/w mask of region
    mask = Image.new('L', image.size, 255)
    ImageDraw.Draw(mask).polygon(region, fill=0, outline=0)
    # Get number of pixels in the region: k
    k = int(np.sum(np.asarray(mask)) / 255)
    # Remove region from image
    f_star = image.copy()
    # ImageDraw.Draw(f_star).polygon(region, fill=0)
    f_star.putalpha(mask)
    # Each pixel is a tuple (intensity, alpha)
    # alpha is either (0 = in region) or (255 = not in region)
    # from this can build matrix A and column vector b
    f_star_pixels = list(f_star.getdata())
    # Create A and b
    A, b = _generate_a_b(f_star_pixels, image.size)
    print(A)

    # Now, create system of equations for whole image to solve for unknowns
    # A = matrix (kxk)
    # x = column vector of unknowns (pixel intensities)
    # b = column vector solutions

    # Save result to `out`, returning path to image
    return save_image(f_star, name='t1')
