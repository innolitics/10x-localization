import numpy as np


def center_of_mass(image):
    x = np.arange(image.size, dtype=np.double)
    weights = image.astype(np.double)/np.sum(image)
    return np.sum(weights*x)

def center_of_mass_with_threshold(image):
    x = np.arange(image.size, dtype=np.double)
    threshold = 0.4*np.max(image)
    image[image<threshold] = 0
    weights = image.astype(np.double)/np.sum(image)
    return np.sum(weights*x)
