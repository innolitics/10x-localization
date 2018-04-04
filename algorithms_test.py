import math

import numpy as np

from algorithms import center_of_mass


def test_center_of_mass_impulse():
    image = np.zeros(10)
    image[4] = 1.0
    assert center_of_mass(image) == 4.0


def test_center_of_mass_rect():
    image = np.zeros(10)
    image[4] = 1.0
    image[5] = 1.0
    assert math.isclose(center_of_mass(image), 4.5)


def test_center_of_mass_varying_density():
    image = np.zeros(10)
    image[0] = 1.0
    image[3] = 2.0
    assert math.isclose(center_of_mass(image), 2.0)
