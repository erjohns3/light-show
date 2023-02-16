from effects.compiler import b

effects = {
    "io  No Sleep Official Lyric Video": {
        "bpm": 125,
        "song_path": "songs/i_o - No Sleep (Official Lyric Video).ogg",
        "delay_lights": 0.25849999999999995,
        "skip_song": 0.0,
        "profiles": ["Eric"],
        "beats": [
            [4, 'Red top', 8, 1, 0],
            [4, 'Red disco', 144, 0, 1],
            [164, 'Red bottom pulse', 96],
            [164.5, 'Sleep Red disco pulse', 96],
            [260, 'Red top', 8, 1, 0],
            [260, 'Red disco', 128, 0, 1],
            [400, 'Red bottom pulse', 96],
            [400.5, 'Sleep Red disco pulse', 96],
        ]
    },

    "Red bottom pulse": {
        "length": 1,
        "trigger": "toggle",
        "loop": True,
        "profiles": ["Eric"],
        "beats": [
            b(1, 'Red bottom', length=.25),
        ]
    },

    "Sleep Red disco pulse": {
        "length": 1,
        "trigger": "toggle",
        "loop": True,
        "profiles": ["Eric"],
        "beats": [
            b(1, 'Red disco', length=.25),
        ]
    },
}