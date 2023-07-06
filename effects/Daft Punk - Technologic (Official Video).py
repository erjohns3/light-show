from effects.compiler import b

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

lyrics = {
    'buy': '🛒',
    'use': 'use',
    'break': '🔨',
    'fix': '🔧',
    'trash': '🗑',
    'change': 'change',
    'mail': '📬',
    'upgrade': 'upgrade',
}

effects = {
    "Daft Punk - Technologic (Official Video)": {
        "bpm": 128,
        "song_path": "songs/Daft Punk - Technologic (Official Video).ogg",
        # "delay_lights": 7.38275000000000003,
        "delay_lights": 0.25275000000000003,
        "skip_song": 0,
        "beats": [
            b(1, grid_filename='ricardo.gif', rotate_90=False, length=7),
            b(8, grid_text='😭', font_size=11, length=4),

            # b(16, name='RBBB 1 bar', length=8),
            b(16, grid_text=lyrics['buy'], font_size=13, rotate_90=True, length=4),
            b(20, grid_text=lyrics['use'], font_size=13, rotate_90=True, length=4),
            b(24, grid_text=lyrics['break'], font_size=13, rotate_90=True, length=4),
            b(28, grid_text=lyrics['fix'], font_size=13, rotate_90=True, length=4),
            b(32, grid_text=lyrics['trash'], font_size=13, rotate_90=True, length=4),
            b(36, grid_text=lyrics['change'], font_size=13, rotate_90=True, length=4),
            b(40, grid_text=lyrics['mail'], font_size=13, rotate_90=True, length=4),
            b(44, grid_text=lyrics['upgrade'], font_size=13, rotate_90=True, length=4),

            b(48, grid_text='😭', rotate_90=True, font_size=5, length=4),
            b(52, grid_text='😭', rotate_90=True, font_size=6, length=4),
            b(56, grid_text='😭', rotate_90=True, font_size=7, length=4),
            b(60, grid_text='😭', rotate_90=True, font_size=8, length=4),
            b(64, grid_text='😭', rotate_90=True, font_size=9, length=4),
            b(68, grid_text='😭', rotate_90=True, font_size=10, length=4),
            b(72, grid_text='😭', rotate_90=True, font_size=11, length=4),
            b(76, grid_text='😭', rotate_90=True, font_size=12, length=4),
            b(80, grid_text='😭', rotate_90=True, font_size=13, length=4),
            b(84, grid_text='😭', rotate_90=True, font_size=14, length=4),
            b(88, grid_text='😭', rotate_90=True, font_size=15, length=4),

        ]
    }
}