import pathlib
import sys

from rich.console import Console
from rich.style import Style

this_file_directory = pathlib.Path(__file__).parent.resolve()
directory_above_this_file = this_file_directory.parent.resolve()
sys.path.insert(0, str(directory_above_this_file))

import grid_helpers
from effects.compiler import GridInfo
from helpers import *



# python -m cProfile -s tottime test_rich_console.py --local | tac
console = Console()

wait_frame = 0
def fill_grid_from_image_filepath(grid_info):
    global wait_frame
    image_filepath = directory_above_this_file.joinpath('images', grid_info.filename)
    grid_helpers.fill_grid_from_image_filepath(image_filepath, rotate_90=grid_info.rotate_90)
    if image_filepath.suffix.lower() in ['.gif', '.webp']:
        wait_frame += 1
        if wait_frame > 3:
            wait_frame = 0
            grid_helpers.increment_animation_frame(image_filepath)
    grid_helpers.render_grid(terminal=console)


while True:
    grid_info = GridInfo()
    grid_info.filename = 'ricardo.gif'
    grid_info.rotate_90 = False
    fill_grid_from_image_filepath(grid_info)


# older slow way with rich
# for y in range(GRID_HEIGHT):
#     row_string = []
#     for x in range(GRID_WIDTH):
#         time_to_end = ''
#         if x == GRID_WIDTH - 1:
#             time_to_end = '\n'
#         item = tuple(map(int, grid[x][y]))
#         rgb_style = f'rgb({item[0]},{item[1]},{item[2]})'
#         terminal.print('▆', style=rgb_style, end=time_to_end)
# terminal.print('', end='\033[F' * GRID_HEIGHT)
