import math
import pytest

from simulate import integrate_sensor, digitize, sensor_extent


@pytest.fixture
def params():
    return {
        "sensors": {
            "count": 100,
            "width": 1,
            "spacing": 1,
        },
        "digitizer": {
            "min": 0,
            "max": 2,
            "num_levels": 2**8,
        },
        "noise_sigma": 0,
        "image": {
            "baseline_constant": 0,
            "baseline_slope": 0,
            "fiducial_width": 3,
            "fiducial_center": 50,
        },
    }


@pytest.fixture
def image_params(params):
    return params["image"]


@pytest.fixture
def sensor_params(params):
    return params["sensors"]


@pytest.fixture
def digitizer_params(params):
    return params["digitizer"]


def test_integrate_sensor_no_overlap_no_baseline(image_params):
    assert integrate_sensor(image_params, 0, 1) == 0


def test_integrate_sensor_complete_overlap_no_baseline(image_params):
    assert math.isclose(integrate_sensor(image_params, 50, 51), 1.0)


def test_integrate_sensor_partial_overlap_no_baseline(image_params):
    assert math.isclose(integrate_sensor(image_params, 48, 49), 0.5)


def test_integrate_sensor_partial_overlap_constant_baseline(image_params):
    image_params["baseline_constant"] = 2.0
    actual = integrate_sensor(image_params, 48, 49)
    expected = 0.5 + image_params["baseline_constant"]
    assert math.isclose(actual, expected)


def test_integrate_sensor_partial_overlap_linear_baseline(image_params):
    image_params["baseline_slope"] = 2.0
    x0 = 48
    x1 = 49
    dx = x1 - x0
    triangle = dx*(dx*image_params["baseline_slope"])/2
    rectangle = dx*image_params["baseline_slope"]*x0
    actual = integrate_sensor(image_params, 48, 49)
    expected = 0.5 + triangle + rectangle
    assert math.isclose(actual, expected)


def test_sensor_extents_single_full_width():
    assert sensor_extent(0, 1, 1) == (0.0, 1.0)
    assert sensor_extent(1, 1, 1) == (1.0, 2.0)


def test_sensor_extents_single_half_width():
    assert sensor_extent(0, 0.5, 1) == (0.25, 0.75)
    assert sensor_extent(1, 0.5, 1) == (1.25, 1.75)


def test_sensor_extents_single_half_width_half_spacing():
    assert sensor_extent(0, 0.5, 0.5) == (0, 0.5)
    assert sensor_extent(1, 0.5, 0.5) == (0.5, 1.0)


def test_digitize_below_min(digitizer_params):
    assert digitize(digitizer_params, -10) == 0


def test_digitize_above_max(digitizer_params):
    assert digitize(digitizer_params, 10) == digitizer_params["num_levels"] - 1


def test_digitize_rounded_down(digitizer_params):
    assert digitize(digitizer_params, 0.000001) == 0


def test_digitize_rounded_up(digitizer_params):
    assert digitize(digitizer_params, 2.0 - 0.000001) == digitizer_params["num_levels"] - 1
