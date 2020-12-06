from PIL import Image
import numpy as np


def resize(arr, scale) -> np.ndarray:
    _scale = lambda dim, s: int(dim * s / 100)
    im = Image.fromarray(np.array(arr))
    width, height = im.size
    new_width: int = _scale(width, scale)
    new_height: int = _scale(height, scale)
    new_dim: tuple = (new_width, new_height)
    return im.resize(new_dim)


if __name__ == '__main__':
    array = np.arange(0, 737280, 1, np.uint8)
    array = np.reshape(array, (1024, 720))
    resize(array,0.5)