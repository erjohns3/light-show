import sys
import time
import pathlib

import numpy as np
import matplotlib.pyplot as plt

this_file_directory = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(this_file_directory.parent))
import grid_helpers
from helpers import *


def bezier_full_cubic(t, p0, p1, p2, p3):
    return (1 - t)**3 * p0 + 3 * (1 - t)**2 * t * p1 + 3 * (1 - t) * t**2 * p2 + t**3 * p3


def compute_x_to_y_bezier_cubic(p1, p2):
    x_to_y_bezier = np.array(np.zeros((101)), np.double)
    resolution = 100000
    for i in range(resolution + 1):
        t = i / resolution
        x_to_y_bezier[round(bezier_full_cubic(t, 0, p1[0], p2[0], 1) * 100)] = bezier_full_cubic(t, 0, p1[1], p2[1], 1) * 100

    if any([value for value in x_to_y_bezier == None]):
        print_red(f'x_to_y_bezier: {x_to_y_bezier} has None values with {p1=}, exiting')
        exit()
    return x_to_y_bezier

start_bezier_time = time.time()
grid_red_bezier = compute_x_to_y_bezier_cubic((0.588, 0.06), (0.716, .705))
grid_green_bezier = compute_x_to_y_bezier_cubic((0.465, 0.09), (0.87, 0.573))
grid_blue_bezier = compute_x_to_y_bezier_cubic((0.932, 0.033), (0.653, 0.935))

def apply_bezier_to_grid():
    global grid
    grid_as_int = grid.astype(int)
    for x in range(grid_helpers.GRID_WIDTH):
        for y in range(grid_helpers.GRID_HEIGHT):
            grid[x][y][0] = grid_red_bezier[grid_as_int[x][y][0]]
            grid[x][y][1] = grid_green_bezier[grid_as_int[x][y][1]]
            grid[x][y][2] = grid_blue_bezier[grid_as_int[x][y][2]]


def debug_plot_bezier_curves(points_to_graph, arrs_to_graph):
    if is_andrews_main_computer():
        plt.style.use('dark_background')
    _fig, ax = plt.subplots()
    for graph, color in arrs_to_graph:
        ax.plot(graph, color=color)

    
    for (color, opacity), points in points_to_graph.items():
        xpoints = list(map(lambda x: x[0] * 100, points))
        ypoints = list(map(lambda x: x[1] * 100, points))
        # ax.plot(xpoints, ypoints, 'o', color=color)
        # above needs opacity (0-1)
        ax.scatter(xpoints, ypoints, color=color, alpha=opacity)
    plt.show()
    exit()


# grid debugging
debug_plot_bezier_curves(
    {
        # real points
        ('red', 1): [(0.75, .60), (0.50, 0.31), (0.25, 0.08)],
        ('green', 1): [(0.75, 0.52), (0.50, 0.31), (0.25, 0.10)],
        ('blue', 1): [(0.75, 0.60), (0.50, 0.17), (0.25, 0.04)],

        # bezier points
        ('red', 0.15): [(0.588, 0.06), (0.716, 0.705)],
        ('green', 0.15): [(0.465, 0.09), (0.87, 0.573)],
        ('blue', 0.15): [(0.932, 0.033), (0.653, 0.935)],
    },
    [
        (grid_red_bezier, 'red'),
        (grid_green_bezier, 'green'),
        (grid_blue_bezier, 'blue'),
    ]
)

print_cyan(f'start_bezier_time: {time.time() - start_bezier_time:.2f} seconds')