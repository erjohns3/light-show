from effects.compiler import b

effects = {
    "Delta Heavy  Punish My Love Official Video": {
        "bpm": 125,
        "song_path": "songs/Delta Heavy  Punish My Love Official Video.ogg",
        "delay_lights": 0.04,
        "skip_song": 0.0,
        "beats": [
            b(1, name='RBBB 1 bar', length=160),
            # b(48, name='dom intro bassline', length=32),
            # # b(40, name='me new', length=8),
            # b(71, name='dom drop sidechain', length=8),
            # b(80, name='dom chorus', length=64),
            # # b(78.8, name='dom chorus', length=64),
            # b(144, name='dom chorus 2', length=64),
            # b(200, name='dom drop sidechain', length=8),
            b(161, name='dom chorus', length=64),
            # b(207, name='Nothing', length=1),
            # b(208, name='dom chorus', length=64),
            # b(272, name='UV pulse', length=32),            
            # b(304, name='dom windy melody', length=64),
            # b(304, name='dom kicks', length=32, hue_shift=.3),
            # b(360, name='dom drop sidechain', length=8),
            # b(368, name='dom chorus', length=64),
            # b(432, name='dom windy melody', length=64),
            # b(432, name='dom intro bassline', length=64),
        ]
    }
}