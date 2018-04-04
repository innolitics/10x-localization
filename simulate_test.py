import math
import pytest

from simulate import integrate_sensor, digitize


@pytest.fixture
def params():
    return {
        "num_pixels": 100,
        "sensor_width": 1,
        "sensor_spacing": 1,
        "sensor_min": 0,
        "sensor_max": 1,
        "num_grayscale_levels": 2**8,
        "sigma": 0,
        "baseline_constant": 0,
        "baseline_slope": 0,
        "fiducial_width": 3,
        "fiducial_center": 50,
    }


def test_integrate_sensor_no_overlap_no_baseline(params):
    assert integrate_sensor(params, 0, 1) == 0


def test_integrate_sensor_complete_overlap_no_baseline(params):
    assert math.isclose(integrate_sensor(params, 50, 51), 1.0)


def test_integrate_sensor_partial_overlap_no_baseline(params):
    assert math.isclose(integrate_sensor(params, 48, 49), 0.5)


def test_integrate_sensor_partial_overlap_constant_baseline(params):
    params["baseline_constant"] = 2.0
    assert math.isclose(integrate_sensor(params, 48, 49), 0.5 + params["baseline_constant"])


def test_integrate_sensor_partial_overlap_linear_baseline(params):
    params["baseline_slope"] = 2.0
    x0 = 48
    x1 = 49
    dx = x1 - x0
    triangle = dx*(dx*params["baseline_slope"])/2
    rectangle = dx*params["baseline_slope"]*x0
    assert math.isclose(integrate_sensor(params, 48, 49), 0.5 + triangle + rectangle)
