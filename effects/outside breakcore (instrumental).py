from effects.compiler import *

def bar_down(grid_info):
    if getattr(grid_info, 'y', None) is None or grid_info.curr_sub_beat == 0:
        grid_info.y = 0

    if grid_info.y > grid_helpers.GRID_HEIGHT - 1:
        return

    for y_off in range(grid_info.y_range):
        if grid_info.y + y_off < 0 or grid_info.y + y_off >= grid_helpers.GRID_HEIGHT:
            continue
        grid_helpers.grid[grid_info.x_pos][y_off + grid_info.y] = grid_info.color

    speed = int(1 / getattr(grid_info, 'speed', 1))
    if grid_info.curr_sub_beat % speed == 0:
        grid_info.y += 1



def spawn_half_fallers(start_beat, total_beats, start_color, end_color=None, intensity=1):
    if end_color == None:
        end_color = GColor.nothing
    building = []
    quarter_x = grid_helpers.GRID_WIDTH // 4
    for beat in range(start_beat, start_beat + total_beats + 1):
        percent_done = (beat - start_beat) / total_beats
        curr_color = interpolate_vectors_float(start_color, end_color, percent_done)
        curr_color = scale_vector(curr_color, intensity)
        building += [
            grid_f(beat, function=bar_down, length=8, x_pos=quarter_x - 4, y_range=5, color=curr_color),
            grid_f(beat + .25, function=bar_down, length=8, x_pos=quarter_x * 2 - 4, y_range=5, color=curr_color),
            grid_f(beat + .75, function=bar_down, length=8, x_pos=quarter_x * 3 - 4, y_range=5, color=curr_color),
            grid_f(beat + 1, function=bar_down, length=8, x_pos=quarter_x * 4 - 4, y_range=5, color=curr_color),
        ]
    return building





effects = {
    "sidechain grid repeat": {
        "length": 0.25,
        "beats": [
            grid_f(1, function=sidechain_grid, length=.12, intensity=0, priority=5000),
        ],
    },
    "outside breakcore (instrumental)": {
        "bpm": 89,
        "song_path": "songs/outside breakcore (instrumental).ogg",
        "delay_lights": 0.3631573033707865,
        "skip_song": 0.0,
        "beats": [
            *spawn_half_fallers(start_beat=1, total_beats=256, start_color=GColor.blue, intensity=1),

            b(64, name="sidechain grid repeat", length=64),

        ]
    }
}