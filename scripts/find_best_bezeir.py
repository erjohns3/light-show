import sys
import time
import pathlib

from tqdm import tqdm

this_file_directory = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(this_file_directory.parent))
import grid_helpers
from helpers import *


@profile
def find_best_bezier_points():
    iters = 0
    time_start = time.time()
    # for color, test_points in [('red', grid_helpers.grid_red_test_points), ('green', grid_helpers.grid_green_test_points), ('blue', grid_helpers.grid_blue_test_points)]:
    for color, test_points in [('blue', grid_helpers.grid_blue_test_points)]:
        print_cyan(f'minimizing distance for color: {color}')
        results_for_color = []
        
        test_points_rounded = [(round(x * 100), round(y * 100)) for (x, y) in test_points]
        largest = 100
        for bx1 in tqdm(range(1, largest + 1)):
            for by1 in range(1, largest + 1):
                for bx2 in range(1, largest + 1):
                    for by2 in range(1, largest + 1):
                        x1, y1, x2, y2 = bx1 / largest, by1 / largest, bx2 / largest, by2 / largest
                        bezeir_x_to_y = grid_helpers.compute_x_to_y_bezier_cubic((x1, y1), (x2, y2), resolution=600)
                        mse = sum([(y - bezeir_x_to_y[x]) ** 2 for (x, y) in test_points_rounded])
                        results_for_color.append((mse, x1, y1, x2, y2))
                        iters += 1
                        # print(f'{bx1}, {by1}, {bx2}, {by2}, {mse:.2f}')
                    # print_cyan(f'Per second: {iters/(time.time() - time_start):.2f} iters')

        results_for_color.sort(key=lambda x: x[0])
        print_cyan(f'color: {color}')
        for mse, bx1, by1, bx2, by2 in results_for_color[:10]:
            print(f'    mse: {mse:.2f}, bx1: {bx1:.2f}, by1: {by1:.2f}, bx2: {bx2:.2f}, by2: {by2:.2f}')
find_best_bezier_points()


# color: red
# mse: 1.57, bx1: 0.44, by1: 0.01, bx2: 0.99, by2: 0.94
# mse: 1.60, bx1: 0.43, by1: 0.01, bx2: 0.95, by2: 0.88
# mse: 1.62, bx1: 0.40, by1: 0.01, bx2: 0.89, by2: 0.77
# mse: 1.62, bx1: 0.44, by1: 0.01, bx2: 0.98, by2: 0.93
# mse: 1.71, bx1: 0.40, by1: 0.01, bx2: 0.91, by2: 0.79
# mse: 1.73, bx1: 0.43, by1: 0.01, bx2: 0.97, by2: 0.90
# mse: 1.74, bx1: 0.44, by1: 0.01, bx2: 0.99, by2: 0.95
# mse: 1.74, bx1: 0.43, by1: 0.01, bx2: 0.97, by2: 0.91
# mse: 1.77, bx1: 0.44, by1: 0.01, bx2: 0.98, by2: 0.92
# mse: 1.79, bx1: 0.42, by1: 0.01, bx2: 0.95, by2: 0.87


# color: green
# mse: 5.05, bx1: 0.20, by1: 0.01, bx2: 1.00, by2: 0.60
# mse: 5.14, bx1: 0.25, by1: 0.03, bx2: 1.00, by2: 0.62
# mse: 5.17, bx1: 0.25, by1: 0.04, bx2: 1.00, by2: 0.61
# mse: 5.19, bx1: 0.20, by1: 0.02, bx2: 1.00, by2: 0.59
# mse: 5.21, bx1: 0.19, by1: 0.01, bx2: 0.99, by2: 0.58
# mse: 5.21, bx1: 0.20, by1: 0.01, bx2: 1.00, by2: 0.59
# mse: 5.28, bx1: 0.20, by1: 0.01, bx2: 0.98, by2: 0.58
# mse: 5.28, bx1: 0.22, by1: 0.02, bx2: 1.00, by2: 0.61
# mse: 5.34, bx1: 0.25, by1: 0.03, bx2: 1.00, by2: 0.63
# mse: 5.35, bx1: 0.18, by1: 0.01, bx2: 0.99, by2: 0.57

# color: blue
# mse: 0.00, bx1: 0.66, by1: 0.09, bx2: 0.40, by2: 0.09
# mse: 0.00, bx1: 0.73, by1: 0.06, bx2: 0.54, by2: 0.39
# mse: 0.01, bx1: 0.76, by1: 0.05, bx2: 0.58, by2: 0.50
# mse: 0.01, bx1: 0.85, by1: 0.05, bx2: 0.63, by2: 0.72
# mse: 0.01, bx1: 0.88, by1: 0.05, bx2: 0.64, by2: 0.80
# mse: 0.01, bx1: 0.81, by1: 0.05, bx2: 0.61, by2: 0.62
# mse: 0.01, bx1: 0.67, by1: 0.08, bx2: 0.43, by2: 0.15
# mse: 0.01, bx1: 0.87, by1: 0.05, bx2: 0.64, by2: 0.78
# mse: 0.01, bx1: 0.75, by1: 0.05, bx2: 0.57, by2: 0.47
# mse: 0.01, bx1: 0.95, by1: 0.05, bx2: 0.65, by2: 0.98