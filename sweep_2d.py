from sweep import main

params = {
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
    "noise_sigma": 0.01,
    "object": {
        "baseline_constant": 0.02,
        "baseline_slope": 0,
        "fiducial_radius": 1.5,
        "fiducial_center_x": 50,
        "fiducial_center_y": 50,
    },
}

if __name__ == "__main__":
    main()
