import random

import numpy as np


def generate_image(params):
    image = np.empty(int(params["sensors"]["count"]), dtype=np.int64)
    for k, extents in enumerate(sensor_extents(params["sensors"])):
        result = integrate_sensor(params["object"], *extents)
        result_with_noise = add_noise(params["noise_sigma"], result)
        image[k] = digitize(params["digitizer"], result_with_noise)
    return image


def sensor_extents(sensors):
    return [sensor_extent(k, sensors["width"]) for k in range(int(sensors["count"]))]


def sensor_extent(center, width):
    return (center - width/2, center + width/2)


def integrate_sensor(object_params, start, stop):
    dx = stop - start
    baseline_at_start = object_params["baseline_constant"] + object_params["baseline_slope"]*start
    baseline_contribution = dx*baseline_at_start + dx*dx*object_params["baseline_slope"]/2
    fiducial_start = object_params["fiducial_center"] - object_params["fiducial_width"]/2
    fiducial_stop = object_params["fiducial_center"] + object_params["fiducial_width"]/2
    fiducial_contribution = max(0, min(fiducial_stop, stop) - max(fiducial_start, start))
    return baseline_contribution + fiducial_contribution


def add_noise(sigma, result):
    return result + random.gauss(0, sigma)


def digitize(digitizer, result):
    if result <= digitizer["min"]:
        return 0
    elif result >= digitizer["max"]:
        return digitizer["num_levels"] - 1
    else:
        normalized = (result - digitizer["min"])/(digitizer["max"] - digitizer["min"])
        return int(round(normalized*(digitizer["num_levels"] - 1)))
