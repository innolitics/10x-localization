import numpy as np


def simulate(params):
    image = np.empty(params["num_pixels"])
    s = params["sensor_width"]
    for k in range(params["sensor_width"]):
        start = k + s/2
        stop = k + 1 - s/2
        result = integrate_sensor(params["image_params"], start, stop)
        result_with_noise = add_noise(params, result)
        image[k] = digitize(params, result_with_noise)
    return image


def integrate_sensor(image, start, stop):
    dx = stop - start
    baseline_at_start = image["baseline_constant"] + image["baseline_slope"]*start
    baseline_contribution = dx*baseline_at_start + dx*dx*image["baseline_slope"]/2
    fiducial_start = image["fiducial_center"] - image["fiducial_width"]/2
    fiducial_stop = image["fiducial_center"] + image["fiducial_width"]/2
    fiducial_contribution = max(0, min(fiducial_stop, stop) - max(fiducial_start, start))
    return baseline_contribution + fiducial_contribution


def add_noise(params, result):
    # TODO: implement
    return result


def digitize(params, result):
    # TODO: implement
    return result
