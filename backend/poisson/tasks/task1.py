from PIL import Image, ImageDraw

from ..utils.img_dir import save_image


def task1(image, region):
    """
    Takes an image and a region and returns the image with the region filled in
    with the results of Eq(2)
    """
    # Image to greyscale (returns copy)
    f_star = image.convert('L')
    # Fill region with black (leaving f*)
    ImageDraw.Draw(f_star).polygon(region, fill=0)
    # Use border of region to interpolate for missing values inside region
    # aim is to have a minimised second-order derivative


    # Save result to `out`
    return save_image(f_star)
