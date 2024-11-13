from effects.compiler import *

effects = {}

def perimeter(info):
    color = getattr(info, 'color')
    amt = getattr(info, 'amt')
    scaled_color = [int(x * amt / 100) for x in color]
    for y in [0, grid_helpers.GRID_HEIGHT - 1]:
        for x in range(grid_helpers.GRID_WIDTH):
            grid_helpers.grid[x][y] = scaled_color
    
    for x in [0, grid_helpers.GRID_WIDTH - 1]:
        for y in range(grid_helpers.GRID_HEIGHT):
            grid_helpers.grid[x][y] = scaled_color


for color_string, color in [('red', GColor.red), ('blue', GColor.blue), ('green', GColor.green)]:
    for amt in range(1, 101):
        if amt < 10:
            effects[f'{color_string} - {amt}'] = {
                'length': 1,
                'trigger': 'toggle',
                'profiles': [f'Ambient'],
                'beats': [
                    grid_f(1, function=perimeter, length=1, color=color, amt=amt),
                ],
            }

