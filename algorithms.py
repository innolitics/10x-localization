import numpy as np
import scipy.ndimage
from scipy.ndimage import gaussian_filter


def center_of_mass(image):
    x = np.arange(image.size, dtype=np.double)
    weights = image.astype(np.double)/np.sum(image)
    return np.sum(weights*x)


def center_of_mass_scipy(image):
    return scipy.ndimage.center_of_mass(image)


def gaussian_center_of_mass(image):
    blurred_image = gaussian_filter(image, 1.5, mode='reflect')
    return scipy.ndimage.center_of_mass(blurred_image)


def gaussian_threshold_center_of_mass(image):
    blurred_image = gaussian_filter(image, 1.5, mode='reflect')
    surface = blurred_image.copy()
    surface[1:-1, 1:-1] = np.nan
    roi_surface_max = np.nanmax(surface)
    roi_max = np.max(blurred_image)
    threshold = roi_surface_max + (roi_max - roi_surface_max) * 0.5
    labelled_array = (blurred_image > threshold).astype(int)
    return scipy.ndimage.center_of_mass(blurred_image, labelled_array)[0]
