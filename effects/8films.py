from effects.compiler import *



def box_filler(info):
    y_sections = 2
    x_sections = 3
    order = [(100,40,80), GColor.blue, (10, 80, 60), (50,0,50), GColor.yellow, GColor.orange]
    color_index = int(info.percent_done * 6)
    color = order[color_index]
    for y_section in range(y_sections):
        for x_section in range(x_sections):
            if (x_section + (y_section * x_sections)) != color_index:
                continue
            for dx in range(grid_helpers.GRID_WIDTH // x_sections):
                for dy in range(grid_helpers.GRID_HEIGHT // y_sections):
                    x = x_section * (grid_helpers.GRID_WIDTH // x_sections) + dx
                    y = y_section * (grid_helpers.GRID_HEIGHT // y_sections) + dy
                    grid_helpers.grid[x][y] = color


# pink, blue, seafoam, purple, yellow, orange, white, green, cyan, red


effects = {
    "8films effect": {
        "length": 24,
        "beats": [
            # b(1, name='Pink top', length=4),
            # b(5, name='Blue top', length=4),
            # b(9, name='Seafoam top', length=4),
            # b(13, name='Purple top', length=4),
            # b(17, name='Yellow top', length=4),
            # b(21, name='Orange top', length=4),
            grid_f(1, function=box_filler, length=24),
        ],
    },
    "8films": {
        "bpm": 130,
        "song_path": "songs/8films.ogg",
        "delay_lights": 0.3666384615384616,
        "skip_song": 0.0,
        "beats": [
            b(5, name='8films effect', length=1000),
            # grid_f(5, function=box_filler, length=1000),
        ]
    }
}