from effects.compiler import b

effects = {
    "dayglow bump": {
        "length": 4,
        "beats": [
            b(1, name='Purple top', length=1, intensity=(1,0)),
            b(name='Green top', length=1, intensity=(1,0)),
            b(name='Yellow top', length=1, intensity=(1,0)),
            b(name='Red top', length=1, intensity=(1,0)),
        ],
    },


    "dayglow_close_to_you": {
        "bpm": 140,
        "delay_lights": 0.31,
        "skip_song": 0.0,
        "beats": [
            b(5, name='dayglow bump', length=128),
        ],
        "song_path": "songs/Dayglow - Close to You (Official Video).ogg",
        "length": 458,
    },
}