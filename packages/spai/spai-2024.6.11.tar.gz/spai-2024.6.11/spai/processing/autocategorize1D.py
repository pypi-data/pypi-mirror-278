import numpy
from .utils import control_uint_type


def autocategorize1D(raster, iterations=200, centers=[0.1, 0.35, 0.50, 0.70]):
    # cluster pixels in given classes
    iterations = max([1, min([iterations, 200])])
    shape = raster.shape
    raster = raster.reshape(-1, 1)

    for i in range(iterations):
        clusters = numpy.argmin(numpy.abs(raster - centers), axis=1)
        centers = [numpy.mean(raster[clusters == j]) for j in range(len(centers))]

    array_categorized = clusters.reshape(shape)
    dtype = control_uint_type(array_categorized)  # Control uint type
    array_categorized = array_categorized.astype(dtype)

    return array_categorized
