import math

import pytest
import numpy as np

from simulate_2d import generate_image, integrate_sensor, digitize, sensor_extents


@pytest.fixture
def params():
    return {
        "sensors": {
            "count_x": 100,
            "count_y": 100,
            "width": 1,
            "height": 1,
        },
        "digitizer": {
            "min": 0,
            "max": 2,
            "num_levels": 2**8,
        },
        "noise_sigma": 0,
        "object": {
            "baseline_constant": 0,
            "baseline_slope": 0,
            "fiducial_radius": 1.5,
            "fiducial_center_x": 50,
            "fiducial_center_y": 50,
        },
    }


@pytest.fixture
def object_params(params):
    return params["object"]


@pytest.fixture
def sensor_params(params):
    return params["sensors"]


@pytest.fixture
def digitizer_params(params):
    return params["digitizer"]


def test_integrate_sensor_no_overlap_no_baseline(object_params):
    assert integrate_sensor(object_params, 0, 1, 0, 1) == 0


def test_integrate_sensor_complete_overlap_no_baseline(object_params):
    assert math.isclose(integrate_sensor(object_params, 50, 51, 50, 51), 1.0)


def test_integrate_sensor_partial_overlap_no_baseline(object_params):
    assert math.isclose(integrate_sensor(object_params, 48, 49, 48, 49), 0.5)


def test_integrate_sensor_partial_overlap_constant_baseline(object_params):
    object_params["baseline_constant"] = 2.0
    actual = integrate_sensor(object_params, 48, 49, 48, 49)
    expected = 0.5 + object_params["baseline_constant"]
    assert math.isclose(actual, expected)


def test_integrate_sensor_partial_overlap_linear_baseline(object_params):
    object_params["baseline_slope"] = 2.0
    x0 = 48
    x1 = 49
    dx = x1 - x0
    triangle = dx*(dx*object_params["baseline_slope"])/2
    rectangle = dx*object_params["baseline_slope"]*x0
    actual = integrate_sensor(object_params, 48, 49, 48, 49)
    expected = 0.5 + triangle + rectangle
    assert math.isclose(actual, expected)


def test_sensor_extents_single_full_width():
    assert sensor_extents(0, 0, 1, 1) == ((-0.5, 0.5), (-0.5, 0.5))
    assert sensor_extents(1, 1, 1, 1) == ((0.5, 1.5), (0.5, 1.5))


def test_sensor_extents_single_half_width():
    assert sensor_extents(0, 0, 0.5, 0.5) == ((-0.25, 0.25), (-0.25, 0.25))
    assert sensor_extents(1, 1, 0.5, 0.5) == ((0.75, 1.25), (0.75, 1.25))


def test_digitize_below_min(digitizer_params):
    assert digitize(digitizer_params, -10) == 0


def test_digitize_above_max(digitizer_params):
    assert digitize(digitizer_params, 10) == digitizer_params["num_levels"] - 1


def test_digitize_rounded_down(digitizer_params):
    assert digitize(digitizer_params, 0.000001) == 0


def test_digitize_rounded_up(digitizer_params):
    assert digitize(digitizer_params, 2.0 - 0.000001) == digitizer_params["num_levels"] - 1


def test_digitize_rounded_simple(digitizer_params):
    digitizer_params["num_levels"] = 4
    digitizer_params["min"] = 0
    digitizer_params["max"] = 3.0
    assert digitize(digitizer_params, 0.4) == 0
    assert digitize(digitizer_params, 0.6) == 1
    assert digitize(digitizer_params, 0.9) == 1
    assert digitize(digitizer_params, 1.4) == 1
    assert digitize(digitizer_params, 1.7) == 2


def test_generate_image_defaults(params):
    params["sensors"]["count_x"] = 10
    params["sensors"]["count_y"] = 10
    params["digitizer"]["num_levels"] = 4
    params["object"]["fiducial_center_x"] = 2.5
    params["object"]["fiducial_center_y"] = 2.5
    actual = generate_image(params)
    expected = np.array([
        [0, 1, 2, 2, 1, 0, 0, 0, 0, 0],
        [1, 1, 2, 2, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [1, 1, 2, 2, 1, 1, 1, 1, 1, 1],
        [0, 1, 2, 2, 1, 0, 0, 0, 0, 0],
        [0, 1, 2, 2, 1, 0, 0, 0, 0, 0],
        [0, 1, 2, 2, 1, 0, 0, 0, 0, 0],
        [0, 1, 2, 2, 1, 0, 0, 0, 0, 0],
        [0, 1, 2, 2, 1, 0, 0, 0, 0, 0],
    ], dtype=np.int64)
    assert np.all(actual == expected)
