# (c) 2022 DTU Wind Energy
"""
Generic default colormap module
"""
from ._helpers import HAS_MATPLOTLIB

if HAS_MATPLOTLIB:
    import matplotlib as mpl
    import matplotlib.pyplot as plt

import numpy as np

if HAS_MATPLOTLIB:
    colors_undersea = plt.cm.terrain(np.linspace(0, 0.17, 256))
    colors_land = plt.cm.terrain(np.linspace(0.25, 1, 256))
    elev_colors = np.vstack((colors_undersea, colors_land))

    colormaps_dict = {
        "z0meso": mpl.colors.LinearSegmentedColormap.from_list(
            "",
            [
                "#2A479E",
                "#0DCF69",
                "#F9FA96",
                "#A8906A",
                "#006600",
            ],
        ),
        "user_def_speedups": "coolwarm",
        "orographic_speedups": "coolwarm",
        "obstacle_speedups": "coolwarm",
        "roughness_speedups": "coolwarm",
        "user_def_turnings": "coolwarm",
        "orographic_turnings": "coolwarm",
        "obstacle_turnings": "coolwarm",
        "roughness_turnings": "coolwarm",
        "site_elev": mpl.colors.LinearSegmentedColormap.from_list("", elev_colors),
    }


def colormap_check(key):
    return key in colormaps_dict


def colormap_selector(key):
    return colormaps_dict[key]
