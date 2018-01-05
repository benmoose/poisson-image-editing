from PIL import Image

from poisson.utils.api import APIError


def load_image_or_error(image_name):
    try:
        return Image.open('static/{}'.format(image_name))
    except FileNotFoundError:
        raise APIError('{} was not found'.format(image_name), status_code=404)


def parse_region(region, image_size):
    im_width, im_height = image_size
    """
    Parse region from query params and validate length.
    Region is converted to absolute values using image size.
    """
    if not region:
        raise APIError('region is a required parameter')
    # Convert region string to array (relative % -> abs px)
    region_arr = [round(float(p) * (im_width if i % 2 == 0 else im_height))
            for i, p in enumerate(region.split(','))]
    # Validate length
    if len(region_arr) % 2 != 0:
        raise APIError('There must be an even number of region values')
    return region_arr
