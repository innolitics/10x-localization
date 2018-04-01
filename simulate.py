import numpy as np

params = {
    "A_max": 1,
    "b0": 0,
    "b1": 0,
    "N": 8,
    "s": 1,
    "sigma": 0,
    "w": 3,
    "c": 50,
}

num_pixels = 100

def simulate(params):
    image = np.empty(num_pixels)
    for k in range(num_pixels):
        start = k + s/2
        stop = k + 1 - s/2
        result = integrate_sensor(params, start, stop)
        image[k] = digitize(params, result)
    return image


def integrate_sensor(params, start, stop):
    pass


def digitize(params, result):
    pass
