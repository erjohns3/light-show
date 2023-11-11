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
    results = {}
    iters = 0
    time_start = time.time()
    for color, test_points in [('red', grid_helpers.red_test_points), ('green', grid_helpers.green_test_points), ('blue', grid_helpers.blue_test_points)]:
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
                        results_for_color.append((mse, (x1, y1, x2, y2)))
                        iters += 1
                        # print(f'{bx1}, {by1}, {bx2}, {by2}, {mse:.2f}')
                    # print_cyan(f'Per second: {iters/(time.time() - time_start):.2f} iters')
        results[color] = sorted(results_for_color)

    for color, results_for_color in results.items():
        print_cyan(f'color: {color}')
        for mse, (bx1, by1, bx2, by2) in results_for_color[:10]:
            print(f'    mse: {mse:.2f}, bx1: {bx1:.2f}, by1: {by1:.2f}, bx2: {bx2:.2f}, by2: {by2:.2f}')

find_best_bezier_points()




start_bezier_time = time.time()
grid_red_bezier = grid_helpers.compute_x_to_y_bezier_cubic((0.588, 0.06), (0.716, .705), resolution=100000)
grid_green_bezier = grid_helpers.compute_x_to_y_bezier_cubic((0.465, 0.09), (0.87, 0.573), resolution=100000)
grid_blue_bezier = grid_helpers.compute_x_to_y_bezier_cubic((0.932, 0.033), (0.653, 0.935), resolution=100000)
print_cyan(f'start_bezier_time: {time.time() - start_bezier_time:.2f} seconds')


# grid_helpers.debug_plot_bezier_curves(
#     {
#         # test points
#         ('red', 1): grid_helpers.red_test_points,
#         ('green', 1): grid_helpers.green_test_points,
#         ('blue', 1): grid_helpers.blue_test_points,

#         # bezier points from desmos
#         ('red', 0.15): [(0.588, 0.06), (0.716, 0.705)],
#         ('green', 0.15): [(0.465, 0.09), (0.87, 0.573)],
#         ('blue', 0.15): [(0.932, 0.033), (0.653, 0.935)],
#     },
#     [
#         (grid_red_bezier, 'red'),
#         (grid_green_bezier, 'green'),
#         (grid_blue_bezier, 'blue'),
#     ]
# )