from effects.compiler import b

effects = {
    "Lykke Li - I Follow Rivers (The Magician Remix)": {
        "bpm": 122,
        "song_path": "songs/Lykke Li - I Follow Rivers (The Magician Remix).ogg",
        "delay_lights": 0.0252,
        "skip_song": 0.0,
        "beats": [
            b(1, name='RBBB 1 bar', length=152),
            b(153, name='dom chorus', length=64),
            b(153 + 64, name='RBBB 1 bar', length=153),
        ]
    }
}