import numpy as np

from simulate import generate_image, undigitize

DEFAULT_ITERATION_LIMIT = 1
DEFAULT_DIGITIZER = {
    "min": 0,
    "max": 2,
    "num_levels": 2 ** 8,
}


class LogLikelihoodSolver:
    def __init__(self, image, initial_guess, iteration_limit=DEFAULT_ITERATION_LIMIT, digitizer=DEFAULT_DIGITIZER):
        self.image = image
        self.iteration_limit = iteration_limit
        self.digitizer = digitizer
        self.iteration_count = 0
        self.sample_count = len(image)
        self.sample_center = (self.sample_count - 1) / 2
        self.constant_bias = 0.0
        self.linear_bias = 0.0
        self.width = 3
        self.center = initial_guess
        self.amplitude = 1.0
        self.converged = False
        self.linear_image = np.array([k - self.sample_center for k in range(self.sample_count)])
        normalization_scale = 1.0 / np.sum(self.linear_image * self.linear_image)
        self.linear_image = self.linear_image * normalization_scale

    def undigitize(self, value):
        return undigitize(self.digitizer, value)

    @property
    def center(self):
        return self.integer_center + self.fractional_center

    @center.setter
    def center(self, value):
        self.integer_center = int(value)
        self.fractional_center = value - self.integer_center

    def signal_parameters(self, center=None):
        if center is None:
            center = self.center
        return {
            "sensors": {
                "count": self.sample_count,
                "width": 1,
            },
            "digitizer": self.digitizer,
            "noise_sigma": 0,
            "object": {
                "baseline_constant": self.constant_bias - self.sample_center * self.linear_bias,
                "baseline_slope": self.linear_bias,
                "fiducial_width": self.width,
                "fiducial_center": center,
            },
        }

    def best_guess(self):
        while not self.converged and self.iteration_count < self.iteration_limit:
            self.iteration_step()
            self.iteration_count += 1
        return self.center

    def iteration_step(self):
        for step in [
            self.estimate_constant_bias,
            self.estimate_linear_bias,
            self.estimate_width,
            self.estimate_amplitude,
            self.estimate_center,
        ]:
            step()

    def calculate_residual_image(self, center=None):
        expected_image = generate_image(self.signal_parameters(center=center))
        return self.image - expected_image

    def estimate_constant_bias(self):
        self.constant_bias += self.undigitize(np.mean(self.calculate_residual_image()))

    def estimate_linear_bias(self):
        # estimated_bias = np.sum(self.linear_image * self.calculate_residual_image())
        # self.linear_bias += self.undigitize(estimated_bias)
        pass  # WIP, not yet fully debugged

    def estimate_width(self):
        pass

    def estimate_amplitude(self):
        pass

    def estimate_center(self):
        start = 1 + int(self.width / 2)
        stop = int(self.sample_count - 1 - self.width / 2)
        best_location = start - 1
        prior_image = generate_image(self.signal_parameters(center=best_location))
        lowest_cost = self.log_likelihood_cost(prior_image)
        for k in range(start, stop):
            next_image = generate_image(self.signal_parameters(center=k))
            center, cost = self.best_interpolation(k, prior_image, next_image)
            if cost < lowest_cost:
                best_location = center
                lowest_cost = cost
            prior_image = next_image
        self.center = best_location

    def log_likelihood_cost(self, estimated_image):
        residual = estimated_image - self.image
        return np.sum(residual * residual)

    def best_interpolation(self, k, prior_image, next_image):
        delta_image = next_image - prior_image
        top = np.sum(delta_image * self.image)
        bottom = np.sum(delta_image * delta_image)
        alpha = top / bottom
        center = k + max(0, min(1.0, alpha))
        cost = self.log_likelihood_cost(generate_image(self.signal_parameters(center=center)))
        return center, cost
