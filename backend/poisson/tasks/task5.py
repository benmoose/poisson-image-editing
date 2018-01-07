import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from ..utils.img_dir import clean_img_dir, save_image
from ..utils.img import get_neighbour_labels, generate_filled_pixels


def _generate_v(labelled_pixels, im_width, edge_pixels, edge_threshold=100):
    pixel_count = len(labelled_pixels)
    v = np.zeros((pixel_count, pixel_count))

    def add_to_v_if_above_threshold(p_index, q_index):
        q_intensity, q_alpha = labelled_pixels[q_index]
        p_edge_value = edge_pixels[p_index]
        q_edge_value = edge_pixels[q_index]
        # Eqn (15)
        if abs(p_edge_value - q_edge_value) > edge_threshold:
            v[p_index, n_index] = p_intensity - q_intensity
            v[n_index, p_index] = q_intensity - p_intensity

    for p_index, p in enumerate(labelled_pixels):
        p_intensity, p_alpha = p
        p_in_region = p_alpha == 0

        if p_in_region:
            top_n, right_n, bottom_n, left_n = get_neighbour_labels(
                p_index, im_width, pixel_count)
            if top_n:
                n_index = p_index - im_width
                add_to_v_if_above_threshold(p_index, n_index)
            if left_n:
                n_index = p_index - 1
                add_to_v_if_above_threshold(p_index, n_index)
    return v


def _generate_a_b(labelled_pixels, image_width, v):
    region_length = sum(
        map(lambda p: 1 if p[1] == 0 else 0, labelled_pixels))
    A = np.zeros((region_length, region_length))
    b = np.zeros(region_length)
    # Setup counter for number of region pixels encountered so far
    k_pos = 0
    # Record the k_pos for pixels at position index in region
    region_pixel_k_pos = {}
    for index, pixel in enumerate(labelled_pixels):
        _, alpha = pixel
        in_region = alpha == 0

        top_n, right_n, bottom_n, left_n = get_neighbour_labels(
            index, image_width, len(labelled_pixels))
        neighbour_count = top_n + right_n + bottom_n + left_n

        if in_region:
            region_pixel_k_pos[index] = k_pos
            # Add number of neighbours to A
            A[k_pos, k_pos] = neighbour_count
            # Add top and left neighbour pixels to A
            if top_n:
                try:
                    # check neighbour is in region
                    n_k_pos = region_pixel_k_pos[index - image_width]
                    # mark neighbours with -1's
                    A[k_pos, n_k_pos] = -1
                    A[n_k_pos, k_pos] = -1
                except KeyError:
                    pass  # Neighbour not in region
            if left_n:
                try:
                    # check neighbour is in region
                    n_k_pos = region_pixel_k_pos[index - 1]
                    # mark neighbours with -1's
                    A[k_pos, n_k_pos] = -1
                    A[n_k_pos, k_pos] = -1
                except KeyError:
                    pass  # Neighbour not in region
            # Check if any neighbours are boundary pixels (a.k.a alpha != 0)
            # and if so sum them and add to b
            b_value = 0
            if top_n:
                n_index = index - image_width
                n_intensity, n_alpha = labelled_pixels[n_index]
                if n_alpha != 0:
                    b_value += n_intensity
                # add in v[pq]
                b_value += v[index, n_index]
            if right_n:
                n_index = index + 1
                n_intensity, n_alpha = labelled_pixels[n_index]
                if n_alpha != 0:
                    b_value += n_intensity
                # add in v[pq]
                b_value += v[index, n_index]
            if bottom_n:
                n_index = index + image_width
                n_intensity, n_alpha = labelled_pixels[n_index]
                if n_alpha != 0:
                    b_value += n_intensity
                # add in v[pq]
                b_value += v[index, n_index]
            if left_n:
                n_index = index - 1
                n_intensity, n_alpha = labelled_pixels[n_index]
                if n_alpha != 0:
                    b_value += n_intensity
                # add in v[pq]
                b_value += v[index, n_index]

            b[k_pos] = b_value
            k_pos += 1

    return A, b


def task5(image, region):
    # Clean img dir
    clean_img_dir('t5')
    # Get pixel count
    pixel_count = image.width * image.height
    image_bands = image.split()
    # Create binary mask of region
    mask = Image.new('1', image.size, 1)
    ImageDraw.Draw(mask).polygon(region, fill=0, outline=0)
    # Init final image with 0s
    result_image = np.zeros((pixel_count, 3), dtype='uint8')
    # Iterate through image bands (RGB)
    for ch, ch_pixels in enumerate(image_bands):
        print('doing channel', ch)
        # Get image edges for channel
        # Similar to applying laplace (2nd derivative) kernel
        image_edges_for_band = ch_pixels.filter(ImageFilter.FIND_EDGES)
        save_image(image_edges_for_band, 't5', 'edges-ch-{}'.format(ch))
        image_edges_for_band_arr = list(image_edges_for_band.getdata())
        # Add mask (labels) to band
        ch_pixels.putalpha(mask)
        ch_pixels_arr = list(ch_pixels.getdata())
        # Generate V
        v = _generate_v(ch_pixels_arr, image.width, image_edges_for_band_arr)
        # Generate A and b
        A, b = _generate_a_b(ch_pixels_arr, image.width, v)
        # Solve for x
        x = np.linalg.solve(A, b)
        # Fill in region with x values
        filled_pixels = generate_filled_pixels(ch_pixels_arr, x)
        # Save result to final image
        result_image[..., ch] = filled_pixels[..., 0]

    result_rgb_pixels = np.reshape(
        result_image, (image.height, image.width, 3))
    return save_image(
        Image.fromarray(result_rgb_pixels, mode='RGB'), 't5')
