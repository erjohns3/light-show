from effects.compiler import b
import grid_helpers

lyrics = {
    'buy': 'buy',
    'use': 'use',
    'break': 'break',
    'fix': 'fix',
    'trash': 'trash',
    'change': 'change',
    'mail': 'mail',
    'upgrade': 'upgrade',
}


# lyrics = {
#     'buy': 'buy\n  it',
#     'use': 'use\n  it',
#     'break': 'break\n    it',
#     'fix': 'fix\n  it',
#     'trash': 'trash\n    it',
#     'change': 'change\n     it',
#     'mail': 'mail\n  it',
#     'upgrade': 'upgrade\n       it',
# }

# lyrics = {
#     'buy': '🛒',
#     'use': 'use',
#     'break': '🔨',
#     'fix': '🔧',
#     'trash': '🗑',
#     'change': 'change',
#     'mail': '📬',
#     'upgrade': 'upgrade',
# }



def increase_dim_offset(grid_info, dimension):
    if dimension == 'x':
        grid_info.offset_x = (grid_info.offset_x + 1) % grid_helpers.GRID_WIDTH
    elif dimension == 'y':
        grid_info.offset_y = (grid_info.offset_y + 1) % grid_helpers.GRID_HEIGHT



grid = grid_helpers.get_grid()
def grid_line_go(grid_info):
    if grid_info.curr_sub_beat == grid_info.start_sub_beat:
        grid_info.x = 0
        grid_info.y = 0
    if grid_info.curr_sub_beat % 1 == 0:
        grid_helpers.grid_reset()        
        for x in range(grid_info.width):
            for y in range(grid_info.height):
                grid[x + grid_info.x][y + grid_info.y] = grid_info.color
        grid_info.x = (grid_info.x + grid_info.change[0]) % grid_helpers.GRID_WIDTH
        grid_info.y = (grid_info.y + grid_info.change[1]) % grid_helpers.GRID_HEIGHT


def tech_left(grid_info):
    grid_info.x = 0
    grid_info.y = 0
    grid_info.color = (0, 30, 0)
    grid_info.width = grid_helpers.GRID_WIDTH
    grid_info.height = 1
    grid_info.change = [1, 0]


def tech_up(grid_info):
    grid_info.x = 0
    grid_info.y = 0
    grid_info.color = (30, 0, 0)
    grid_info.width = 1
    grid_info.height = grid_helpers.GRID_HEIGHT
    grid_info.change = [0, 1]
    


effects = {
    'tech effect testing sub': {
        'length': 8,
        'beats': [
            b(1, grid_text='😭', font_size=11, length=3),
        ]
    },
    'battling_lines': {
        'length': 4,
        'beats': [
            b(1, grid_function=grid_line_go, grid_setup_function=tech_left, grid_skip_top_fill=True, length=2),
            b(3, grid_function=grid_line_go, grid_setup_function=tech_up, grid_skip_top_fill=True, length=2),
        ]
    },

    'Daft Punk - Technologic (Official Video)': {
        'bpm': 128,
        'song_path': 'songs/Daft Punk - Technologic (Official Video).ogg',
        # 'delay_lights': 7.38275000000000003,
        'delay_lights': 0.25275000000000003,
        'skip_song': 0,
        'beats': [
            b(1, name='battling_lines', length=100),
            # b(8, grid_filename='ricardo.gif', length=2),
            # b(16, name='tech effect testing', length=15),
            # b(1, grid_filename='ricardo.gif', rotate_90=False, length=7),
            # b(8, grid_text='😭', font_size=11, length=4),

            # # b(16, name='RBBB 1 bar', length=8),
            # b(16, grid_text=lyrics['buy'], font_size=4, rotate_90=False, length=4),
            # b(20, grid_text=lyrics['buy'], font_size=5, rotate_90=False, length=4),
            # b(24, grid_text=lyrics['buy'], font_size=6, rotate_90=False, length=4),
            # b(28, grid_text=lyrics['buy'], font_size=7, rotate_90=False, length=4),
            # b(32, grid_text=lyrics['buy'], font_size=8, rotate_90=False, length=4),
            # b(36, grid_text=lyrics['buy'], font_size=9, rotate_90=False, length=4),
            # b(40, grid_text=lyrics['buy'], font_size=10, rotate_90=False, length=4),
            # b(44, grid_text=lyrics['buy'], font_size=11, rotate_90=False, length=4),

            # b(48, grid_text='😭', rotate_90=True, font_size=5, length=4),
            # b(52, grid_text='😭', rotate_90=True, font_size=6, length=4),
            # b(56, grid_text='😭', rotate_90=True, font_size=7, length=4),
            # b(60, grid_text='😭', rotate_90=True, font_size=8, length=4),
            # b(64, grid_text='😭', rotate_90=True, font_size=9, length=4),
            # b(68, grid_text='😭', rotate_90=True, font_size=10, length=4),
            # b(72, grid_text='😭', rotate_90=True, font_size=11, length=4),
            # b(76, grid_text='😭', rotate_90=True, font_size=12, length=4),
            # b(80, grid_text='😭', rotate_90=True, font_size=13, length=4),
            # b(84, grid_text='😭', rotate_90=True, font_size=14, length=4),
            # b(88, grid_text='😭', rotate_90=True, font_size=15, length=4),

        ]
    }
}