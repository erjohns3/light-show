from effects.compiler import b

lyrics = {
    'buy': 'buy\n  it',
    'use': 'use\n  it',
    'break': 'break\n    it',
    'fix': 'fix\n  it',
    'trash': 'trash\n    it',
    'change': 'change\n     it',
    'mail': 'mail\n  it',
    'upgrade': 'upgrade\n       it',
}

lyrics = {
    'buy': '🛒\nit',
    'use': 'use\n  it',
    'break': '🔨\nit',
    'fix': '🔧\nit',
    'trash': '🗑\nit',
    'change': 'change\n     it',
    'mail': '📬\nit',
    'upgrade': 'upgrade\n       it',
}

effects = {
    "Daft Punk - Technologic (Official Video)": {
        "bpm": 128,
        "song_path": "songs/Daft Punk - Technologic (Official Video).ogg",
        # "delay_lights": 7.38275000000000003,
        "delay_lights": 0.25275000000000003,
        "skip_song": 0,
        "beats": [
            # b(16, name='RBBB 1 bar', length=8),
            b(16, grid_text=lyrics['buy'], font_size=8, length=.8),
            b(17, grid_text=lyrics['use'], font_size=8, length=.8),
            b(18, grid_text=lyrics['break'], font_size=8, length=.8),
            b(19, grid_text=lyrics['fix'], font_size=8, length=.8),
            b(20, grid_text=lyrics['trash'], font_size=8, length=.8),
            b(21, grid_text=lyrics['change'], font_size=8, length=.8),
            b(22, grid_text=lyrics['mail'], font_size=8, length=.8),
            b(23, grid_text=lyrics['upgrade'], font_size=8, length=.8),
        ]
    }
}