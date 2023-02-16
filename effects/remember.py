from effects.compiler import b

effects = {
    "Thing": {
        "length": 1,
        "beats": [
            [1, 'Rosy brown bottom', .2, 1, 0],
        ],
    },

    # 1 - 64: 
    "deadmau5 & Kaskade - I Remember (HQ)": {
        "not_done": False,
        "beats": [
            [1, "Red disco", 2000],
            [1, "Blue disco", 2000],
            [1, "Green disco", 2000],
            # [1, "RBBB 1 bar", 64],
            # [1, "Yellow Top to Bottom hang", 64],
            # [65, "wandering", 64],
            # [129, "Ghosts UV", 64],
            # [193, "Ghosts bassline", 64],
            # [257, "RBBB 1 bar", 64],
            # [394, "Blue top", 64],
        ],
        "delay_lights": 0.1,
        "skip_song": 0,
        "bpm": 128,
        "song_path": "songs/deadmau5 & Kaskade - I Remember (HQ).ogg",
        "profiles": ["Shows"],
    },
}