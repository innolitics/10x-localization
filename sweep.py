import argparse
import random

import matplotlib.pyplot as plt
import numpy as np

import algorithms
from simulate import generate_image


params = {
    "sensors": {
        "count": 100,
        "width": 1,
    },
    "digitizer": {
        "min": 0,
        "max": 2,
        "num_levels": 2**8,
    },
    "noise_sigma": 0.01,
    "object": {
        "baseline_constant": 0.02,
        "baseline_slope": 0,
        "fiducial_width": 3,
        "fiducial_center": 50,
    },
}


def main():
    parser = argparse.ArgumentParser(prog='sweep')
    parser.add_argument('key', type=lambda s: s.split('.'), help='key, e.g. "object.fiducial_width"')
    parser.add_argument('range', type=str, help='range, e.g. "3:10:0.5"')
    parser.add_argument('--algorithm', type=str, default='center_of_mass', help='algorithm name, e.g. "center_of_mass"')
    parser.add_argument('--output', type=str, default=None, help='file name for the output graph')
    parser.add_argument('--samples', type=int, default=100, help='number of samples per key value')
    args = parser.parse_args()

    args.range = value_range(args.range)  # XXX couldn't get arg parse to do this directly ...
    num_values = len(args.range)
    num_samples = args.samples

    errors = np.empty((num_values, num_samples), dtype=np.double)

    algorithm = getattr(algorithms, args.algorithm)

    for i, value in enumerate(args.range):
        set_value(params, args.key, value)
        for j in range(num_samples):
            center = random.uniform(40, 60)
            params['object']['fiducial_center'] = center
            image = generate_image(params)
            calculated_center = algorithm(image)
            errors[i, j] = abs(calculated_center - center)

    error_stds = np.std(errors, axis=1)
    error_means = np.mean(errors, axis=1)

    plt.errorbar(args.range, error_means, yerr=error_stds, fmt='o')
    plt.xlabel(' '.join(args.key).replace('_', ' '))
    plt.ylabel('fiducial localization error')
    plt.grid()
    plt.ylim(ymin=0)
    plt.title('{}, N = {}'.format(args.algorithm.replace('_', ' '), args.samples))
    if args.output is None:
        plt.show()
    else:
        plt.savefig(args.output)


def value_range(range_str):
    parts = [float(s) for s in range_str.split(':')]
    if len(parts) in [2, 3]:
        return np.arange(*parts)
    else:
        raise argparse.ArgumentTypeError("Must have form of X:Y or X:Y:Z")


def set_value(params, keys, value):
    if len(keys) == 1:
        params[keys[0]] = value
    else:
        set_value(params[keys[0]], keys[1:], value)



if __name__ == "__main__":
    main()
