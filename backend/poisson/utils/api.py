import base64


def data_url(image):
    if not image:
        raise ValueError
    return base64.b64encode(open(image, 'rb').read())
