import numpy as np


def center_of_mass(image):
    x = np.arange(image.size, dtype=np.double)
    weights = image.astype(np.double)/np.sum(image)
    return np.sum(weights*x)
