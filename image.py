"""Module for processing small RGB images"""
import time
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from k_means_numpy import KMeans
from k_medoids_batch import BatchKMedoids
from k_medoids_numpy import KMedoids


def image_to_array(file):
    """Read image file into Numpy array"""
    with Image.open(file) as img:
        data = np.asarray(img)
    return data


def reshape_image(data):
    """Reshape RGB data into 2D array"""
    return data.reshape(-1, 3)


def scale_image(data):
    """Scale image data"""
    return data / 255


def rescale_image(data):
    """Rescale image data"""
    return data * 255


def load_data_from_image(file):
    """Read and process image data into Numpy array"""
    return scale_image(reshape_image(image_to_array(file)))


def compress_image(centroids, clusters) -> np.ndarray:
    """Function to compress image array by mapping clusters to centroids"""
    mapper = dict(enumerate(centroids))

    def map_centroid(cluster):
        return mapper.get(cluster)
    return np.array(list(map(map_centroid, clusters)))


class ImageConverter:
    """Class to convert images to and from Numpy arrays"""
    def __init__(self, file: str):
        self.file = file
        self.converted: np.ndarray = np.array(0)
        self.compressed: np.ndarray = np.array(0)

    @property
    def original(self) -> np.ndarray:
        """Read image file into Numpy array"""
        with Image.open(self.file) as img:
            data = np.asarray(img)
        return data

    @property
    def original_dim(self) -> Optional[Tuple[int, int]]:
        """Original image dimensions"""
        return self.original.shape

    def scale_reshape(self):
        """Reshape into 2D and scale image data"""
        self.converted = scale_image(reshape_image(self.original))
        return self.converted

    def to_3d(self, data):
        """Reshape RGB data into 3D array"""
        return data.reshape(self.original_dim)

    def rescale_reshape(self, compressed_image):
        """Rescale image to original scale and reshape to original dimensions"""
        self.compressed = rescale_image(self.to_3d(compressed_image))
        return self

    def show(self) -> None:
        """Show compressed image"""
        img = Image.fromarray(self.compressed.astype('uint8'), 'RGB')
        img.show()

    def print(self) -> None:
        """Print compressed image"""
        img = self.compressed.astype('uint8')
        plt.imshow(img)


def main():
    """
    Main function

    ** Using dog image **
    KMeans time: ~ 5s
    KMedoids time: ~13s
    KMedoids w/soft initialization time: ~ 5s
    BatchKMedoids time: ~ 2s
    """
    start = time.time()
    dog = ImageConverter('../data/dog.jpg')
    algo = KMedoids(k=16)
    algo.fit(dog.scale_reshape(), verbose=1)
    end = time.time()
    print(f'Time: {end - start}')
    dog.rescale_reshape(compress_image(algo.centroids, algo.clusters)).show()


if __name__ == '__main__':
    main()
