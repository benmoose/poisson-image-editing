import numpy as np
from PIL import Image, ImageDraw

from .task2 import _generate_a_b
from ..utils.img_dir import save_image, clean_img_dir
from ..utils.img import generate_filled_pixels


def task3(source_image, dest_image, region):
    # Clean img dir
    clean_img_dir('t3')
    # Convert images to rgba
    source_image = source_image.convert('RGB')
    dest_image = dest_image.convert('RGB')
    # Create b/w mask of region
    mask = Image.new('L', source_image.size, 255)
    ImageDraw.Draw(mask).polygon(region, fill=0, outline=0)
    g = source_image.copy()
    f = dest_image.copy()
    # Split into three images, one for each channel (R, G, B)
    g_bands = g.split()
    f_bands = f.split()
    result_im = np.zeros(
        (dest_image.height * dest_image.width, 3), dtype='uint8')
    for i in range(3):
        print('pass', i, 'of 2')
        g_channel = g_bands[i]
        g_channel.putalpha(mask)
        f_channel = f_bands[i]
        f_channel.putalpha(mask)
        g_channel_pixels = list(g_channel.getdata())
        f_channel_pixels = list(f_channel.getdata())
        # Note v must be the same shape as dest image
        # v = _generate_v_imported_gradient(g_pixels, source_image.size)
        print('calculating a, b')
        A, b = _generate_a_b(
            f_channel_pixels, g_channel_pixels, dest_image.size,
            source_image.size,
            True)
        print('solving for x')
        x = np.linalg.solve(A, b)
        filled_pixels = generate_filled_pixels(f_channel_pixels, x)
        # Fill with pixel intensity data only
        result_im[..., i] = filled_pixels[..., 0]

    result_rgb_pixels = np.reshape(
        result_im, (dest_image.height, dest_image.width, 3))
    return save_image(
        Image.fromarray(result_rgb_pixels, mode='RGB'), 't3', name='t3')
