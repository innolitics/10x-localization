from itertools import product

import numpy as np

from simulate import add_noise, digitize


def generate_image(params):
    image = np.empty((params["sensors"]["count_x"], params["sensors"]["count_y"]), dtype=np.int64)

    for i, j in product(*map(range, image.shape)):
        extents = sensor_extents(i, j, params["sensors"]["width"], params["sensors"]["height"])
        result = integrate_sensor(params["object"], *extents[0], *extents[1])
        result_with_noise = add_noise(params["noise_sigma"], result)
        image[i, j] = digitize(params["digitizer"], result_with_noise)
    return image


def sensor_extents(center_x, center_y, width, height):
    return (
        (center_x - width / 2, center_x + width / 2),
        (center_y - height / 2, center_y + height / 2),
    )


def integrate_sensor(object_params, start_x, stop_x, start_y, stop_y):
    dx = stop_x - start_x
    baseline_at_start = object_params["baseline_constant"] + object_params["baseline_slope"] * start_x
    baseline_contribution = dx*baseline_at_start + dx*dx*object_params["baseline_slope"] / 2
    fiducial_start_x = object_params["fiducial_center_x"] - object_params["fiducial_radius"]
    fiducial_stop_x = object_params["fiducial_center_x"] + object_params["fiducial_radius"]
    fiducial_start_y = object_params["fiducial_center_y"] - object_params["fiducial_radius"]
    fiducial_stop_y = object_params["fiducial_center_y"] + object_params["fiducial_radius"]
    fiducial_contribution_x = max(0, min(fiducial_stop_x, stop_x) - max(fiducial_start_x, start_x))
    fiducial_contribution_y = max(0, min(fiducial_stop_y, stop_y) - max(fiducial_start_y, start_y))
    fiducial_contribution = max(fiducial_contribution_x, fiducial_contribution_y)
    return baseline_contribution + fiducial_contribution
