import numpy as np
from PIL import Image, ImageDraw

from ..utils.img_dir import save_image, clean_img_dir
from ..utils.img import generate_filled_pixels, get_neighbour_labels


def _generate_v_imported_gradient(labelled_pixels, im_size):
    im_width, _ = im_size
    pixel_count = len(labelled_pixels)
    # Setup v matrix
    v = np.zeros((pixel_count, pixel_count))
    # For each pixel...
    for index, pixel in enumerate(labelled_pixels):
        intensity, alpha = pixel
        in_region = alpha == 0

        if not in_region:
            continue

        top_n, _, _, left_n = get_neighbour_labels(
            index, im_width, len(labelled_pixels))

        # need to compute, for all <p, q>, v[pq] = g[p] - g[q]
        gp = intensity
        if top_n:
            n_index = index - im_width
            gq = labelled_pixels[n_index][0]
            v[index, n_index] = gp - gq
            v[n_index, index] = gq - gp
        if left_n:
            n_index = index - 1
            gq = labelled_pixels[n_index][0]
            v[index, n_index] = gp - gq
            v[n_index, index] = gq - gp

    # v[p, q] = gp - gq
    return v


def _generate_a_b(labelled_pixels_dest, labelled_pixels_source, dest_size,
                  source_size, import_gradients):
    dest_im_width, _ = dest_size
    source_im_width, _ = source_size
    # Count the number of pixels in the region
    region_length = sum(
        map(lambda p: 1 if p[1] == 0 else 0, labelled_pixels_dest))
    # Initialise the matrix and column vector
    A = np.zeros((region_length, region_length))
    b = np.zeros(region_length)
    # Record the number of region pixels encountered
    k_pos = 0
    # Record the k_pos for pixels in region
    region_pixel_k_pos = {}
    for index, pixel in enumerate(labelled_pixels_dest):
        _, alpha = pixel
        in_region = alpha == 0

        top_n, right_n, bottom_n, left_n = get_neighbour_labels(
            index, dest_im_width, len(labelled_pixels_dest))
        neighbour_count = top_n + right_n + bottom_n + left_n

        if in_region:
            region_pixel_k_pos[index] = k_pos
            # Add number of neighbours to A
            A[k_pos, k_pos] = neighbour_count
            # Add top and left neighbour pixels to A
            if top_n:
                try:
                    # check neighbour is in region
                    n_k_pos = region_pixel_k_pos[index - dest_im_width]
                    # mark neighbours with -1's
                    A[k_pos, n_k_pos] = -1
                    A[n_k_pos, k_pos] = -1
                except KeyError:
                    pass  # Not in region
            if left_n:
                try:
                    # check neighbour is in region
                    n_k_pos = region_pixel_k_pos[index - 1]
                    # mark neighbours with -1's
                    A[k_pos, n_k_pos] = -1
                    A[n_k_pos, k_pos] = -1
                except KeyError:
                    pass  # Not in region
            # Check if any neighbours are non region pixels (a.k.a on boundary)
            # and if so sum them and add to b
            b_value = 0
            if top_n:
                n_intensity, n_alpha = labelled_pixels_dest[
                    index - dest_im_width]
                if n_alpha != 0:
                    b_value += n_intensity
                # add in v[pq]
                if import_gradients:
                    b_value += labelled_pixels_source[index][0] - \
                               labelled_pixels_source[index - source_im_width][0]
                else:
                    g_b_add = labelled_pixels_source[index][0] - \
                              labelled_pixels_source[index - source_im_width][0]
                    f_b_add = labelled_pixels_dest[index][0] - \
                              labelled_pixels_dest[index - dest_im_width][0]
                    b_value += f_b_add if abs(f_b_add) > abs(g_b_add) \
                        else g_b_add
            if right_n:
                n_intensity, n_alpha = labelled_pixels_dest[index + 1]
                if n_alpha != 0:
                    b_value += n_intensity
                # add in v[pq]
                if import_gradients:
                    b_value += labelled_pixels_source[index][0] - \
                               labelled_pixels_source[index + 1][0]
                else:
                    g_b_add = labelled_pixels_source[index][0] - \
                              labelled_pixels_source[index + 1][0]
                    f_b_add = labelled_pixels_dest[index][0] - \
                              labelled_pixels_dest[index + 1][0]
                    b_value += f_b_add if abs(f_b_add) > abs(g_b_add) \
                        else g_b_add
            if bottom_n:
                n_intensity, n_alpha = labelled_pixels_dest[
                    index + dest_im_width]
                if n_alpha != 0:
                    b_value += n_intensity
                # add in v[pq]
                if import_gradients:
                    b_value += labelled_pixels_source[index][0] - \
                               labelled_pixels_source[index + source_im_width][0]
                else:
                    g_b_add = labelled_pixels_source[index][0] - \
                              labelled_pixels_source[index + source_im_width][0]
                    f_b_add = labelled_pixels_dest[index][0] - \
                              labelled_pixels_dest[index + dest_im_width][0]
                    b_value += f_b_add if abs(f_b_add) > abs(g_b_add) \
                        else g_b_add
            if left_n:
                n_intensity, n_alpha = labelled_pixels_dest[index - 1]
                if n_alpha != 0:
                    b_value += n_intensity
                # add in v[pq]
                if import_gradients:
                    b_value += labelled_pixels_source[index][0] - \
                               labelled_pixels_source[index - 1][0]
                else:
                    g_b_add = labelled_pixels_source[index][0] - \
                              labelled_pixels_source[index - 1][0]
                    f_b_add = labelled_pixels_dest[index][0] - \
                              labelled_pixels_dest[index - 1][0]
                    b_value += f_b_add if abs(f_b_add) > abs(g_b_add) \
                        else g_b_add

            b[k_pos] = b_value
            k_pos += 1

    return A, b


def task2(source_image, dest_image, region, import_gradients=True):
    # Clean img dir
    clean_img_dir('t2')
    # Convert images to greyscale
    source_image = source_image.convert('L')
    dest_image = dest_image.convert('L')
    # Create b/w mask of region
    mask = Image.new('1', source_image.size, 1)
    ImageDraw.Draw(mask).polygon(region, fill=0, outline=0)
    # Extract region from source
    g = source_image.copy()
    g.putalpha(mask)
    g_pixels = list(g.getdata())
    # Mark region in dest image
    f = dest_image.copy()
    f.putalpha(mask)
    f_pixels = list(f.getdata())
    # Note v must be the same shape as dest image
    # v = _generate_v_imported_gradient(g_pixels, source_image.size)
    A, b = _generate_a_b(
        f_pixels, g_pixels, dest_image.size, source_image.size,
        import_gradients)
    x = np.linalg.solve(A, b)
    filled_pixels = generate_filled_pixels(f_pixels, x)
    filled_image = np.reshape(filled_pixels,
                              (dest_image.height, dest_image.width, 2))

    # Save result to `out`, returning path to image
    return save_image(
        Image.fromarray(filled_image, mode='LA'), 't2')
