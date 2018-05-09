import numpy as np

from log_likelihood import LogLikelihoodSolver


def center_of_mass(image):
    x = np.arange(image.size, dtype=np.double)
    weights = image.astype(np.double) / np.sum(image)
    return np.sum(weights * x)


def log_likelihood(image):
    return LogLikelihoodSolver(image, initial_guess=center_of_mass(image)).best_guess()
