import uuid
import numpy as np
from PIL import Image


class ImageModel:
    """
    Base class for image models.
    Sets `self.pixels` from the image path path given to the constructor, and
    implements the `run` and `setup` stub methods, intended to be overridden.
    """
    def __init__(self, *args, **kwargs):
        # Get the image either as a keyword param or the first argument.
        image = kwargs.get('image') or args[0]
        if not image:
            raise AttributeError('No image supplied to ModelImage instance.')
        # Open the specified image and convert to greyscale.
        image = Image.open(image).convert('L')
        self.pixels = ImageModel.pixel_matrix(image.getdata())

    @staticmethod
    def pixel_matrix(image):
        """
        Takes an array and returns a 2D matrix of pixels.
        :param image PIL.Image instance
        """
        rows = image.size[1]
        cols = image.size[0]

        matrix = np.array(image)
        matrix.shape = rows, cols
        return matrix

    @staticmethod
    def setup():
        """
        Used to initialise a new instance of the model.
        This method should take user input (in needed) and return a model
        instance.
        """
        raise NotImplementedError

    def run(self):
        """Should run the algorithm and return an Image instance."""
        raise NotImplementedError

    def save(self, image):
        """Takes an image and saves it to `img/out/`."""
        uid = str(uuid.uuid4())[:5]
        ext = 'jpg'
        name = self.__class__.__name__
        image.save('img/out/{name}-{hash}.{ext}'.format(
            name=name, hash=uid, ext=ext))
        return uid


class PoissonImageEditor(ImageModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def setup():
        return PoissonImageEditor('static/birds.jpeg')

    def run(self):
        pass
