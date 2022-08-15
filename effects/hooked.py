effects = {
    "Hooked 4 Bar Timing Show":{
        "beats":{
            "1": [["Blue top", 8]],
            "9": [["RBBB 1 bar", 20]]
        }
    },
    "hooked scream fade":{
        "length": 1,
        "beats":{
            "1": [["Firebrick top", 0.8, 1, 0]]
        }
    },
    "hooked wandering bottom":{
        "length": 16,
        "beats":{
            "1": [["Cyan bottom", 1, 1, 1]],
            "2": [["Pink bottom", 1, 1, 1]],
            "3": [["Yellow bottom", 1, 1, 1]],
            "4": [["Green bottom", 1, 1, 1]],
            "5": [["Cyan bottom", 1, 1, 1]],
            "6": [["Yellow bottom", 1, 1, 1]],
            "7": [["Pink bottom", 1, 1, 1]],
            "8": [["Cyan bottom", 1, 1, 1]],
            "9": [["Green bottom", 8, 1, .2]]
        }
    },
    "hooked wandering top":{
        "length": 16,
        "beats":{
            "1": [["Cyan top", 1, 1, 1]],
            "2": [["Pink top", 1, 1, 1]],
            "3": [["Yellow top", 1, 1, 1]],
            "4": [["Green top", 1, 1, 1]],
            "5": [["Cyan top", 1, 1, 1]],
            "6": [["Yellow top", 1, 1, 1]],
            "7": [["Pink top", 1, 1, 1]],
            "8": [["Cyan top", 1, 1, 1]],
            "9": [["Green top", 8, 1, 0.2]]
        }
    },
    "hooked bottom kick intro":{
        "length": 1,
        "beats":{
            "1": [["Rosy brown bottom", 0.4, 1, 0]]
        }
    },
    "hooked red kick bottom":{
        "length": 1,
        "beats":{
            "1": [["Red bottom", 0.50, 1, 0]],
        }
    },
    "hooked bottom kick increase":{
        "length": 28,
        "beats":{
            "1": [["hooked red kick bottom", 16, .1, .3]],
            "17": [["hooked red kick bottom", 12, .3, .8]],
        }
    },
    "hooked hear you":{
        "length": 1,
        "beats":{
            "1": [["Cyan top", 0.4, 0.14, 0.14]],
            "1.4": [["Yellow bottom", 0.4, 0.14, 0.14]]
        }
    },
    "hooked top sidechain non red":{
        "length": 2,
        "beats":{
            "1": [[0, -100, -100, 0, 0, 0, 0], 0.1, 0, 1],
            "1.1": [[0, -100, -100, 0, 0, 0, 0], 0.3, 1, 0]
        }
    },
    "hooked claps":{
        "length": 1,
        "beats":{
            "1": ["Cyan top", 0.2, 0.2, 0.1],
            "1.2": ["Cyan top", 0.8, 0.1, 0.1]
        }
    },
    "hooked bassline":{
        "length": 8,
        "beats":{
            "1": [["Firebrick bottom", 0.7, 0.40, 0.05], ["hooked top sidechain non red", 8], ["hooked claps", 8]]
        }
    },
    "hooked sub melody":{
        "length": 8,
        "beats": {
            "2": [["Yellow bottom", 0.15, 0.30, 0.30]],
            "2.25": [["Yellow bottom", 0.15, 0.30, 0.30]],
            "2.5": [["Green bottom", 0.15, 0.30, 0.30]],
            "3": [["Yellow bottom", 0.15, 0.30, 0.30]],
            "3.5": [["Yellow bottom", 0.15, 0.30, 0.30]],
            "4.55": [["Yellow bottom", 0.10, 0.30, .30]],
            "5.05": [["Yellow bottom", 0.10, 0.30, .30]],
            "5.55": [["Yellow bottom", 0.10, 0.30, .30]],
            "6.05": [["Yellow bottom", 0.10, 0.30, .30]],
            "6.55": [["Yellow bottom", 0.10, 0.30, .30]],
            "7.05": [["Yellow bottom", 0.10, 0.30, .30]],
            "7.55": [["Yellow bottom", 0.10, 0.30, .30]],
        }
    },
    "hooked melody":{
        "length": 16,
        "beats": {
            "1": [["hooked sub melody", 24]]
        }
    },
    "hooked buildup":{
        "length": 4,
        "beats":{
            "1": [["hooked hear you", 3]],
            "4": [["UV", 1]]
        }
    },
    "hooked chorus":{
        "length": 32,
        "beats":{
            "1": [["hooked bassline", 32], ["hooked melody", 32]]
        }
    },
    "wandering":{
        "length": 32,
        "beats":{
            "1": [["UV", 4, 1, .28], ["hooked wandering bottom", 16, .8, .5]],
            "5": [["UV", 12, .28, 0]],
            "17": [["Purple bottom", 16, 0.2, 0.05], ["hooked wandering top", 16, .8, .5]],
        }
    },
    "hooked show": {
        "beats":{
            "8": [["hooked scream fade", 2, 0.4, 0.2]],
            "9": [["hooked bottom kick intro", 12, .1, .6]],
            "10": [["hooked scream fade", 6, 0.2, 0.1]],
            "21": [["hooked bottom kick intro", 12, .6, .6]],
            "33": [["hooked bottom kick intro", 8, .6, .2]],
            "41": [["wandering", 64]],
            "105": [["hooked bottom kick increase", 28]],
            "133": [["hooked buildup", 4]],
            "137": [["hooked chorus", 96]],
            "233": [["wandering", 64]],
            "297": [["hooked bottom kick increase", 28]],
            "325": [["hooked buildup", 4]],
            "329": [["hooked chorus", 96]],
            "425": [["Nothing", 6]],
        },
        "delay_lights": 0,
        "skip_song": 0,
        "bpm": 128,
        "song_path": "songs/Notion - Hooked.ogg",
        "profiles": ["Shows"],
    },
}
