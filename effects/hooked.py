effects = {
    "Hooked 4 Bar Timing Show":{
        "length": 2000,
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
            "2": [["Yellow bottom", 1, 1, 1]],
            "3": [["Pink bottom", 1, 1, 1]],
            "4": [["Indigo bottom", 1, 1, 1]],
            "5": [["Cyan bottom", 1, 1, 1]],
            "6": [["Yellow bottom", 1, 1, 1]],
            "7": [["Pink bottom", 1, 1, 1]],
            "8": [["Indigo bottom", 1, 1, 1]],
            "9": [["Cyan bottom", 8, 1, .2]]
        }
    },
    "hooked wandering top":{
        "length": 16,
        "beats":{
            "1": [["Cyan top", 1, 1, 1]],
            "2": [["Yellow top", 1, 1, 1]],
            "3": [["Pink top", 1, 1, 1]],
            "4": [["Indigo top", 1, 1, 1]],
            "5": [["Cyan top", 1, 1, 1]],
            "6": [["Yellow top", 1, 1, 1]],
            "7": [["Pink top", 1, 1, 1]],
            "8": [["Indigo top", 1, 1, 1]],
            "9": [["Cyan top", 8, 1, 0.2]]
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
        "length": 32,
        "beats":{
            "1": [["hooked red kick bottom", 0.50, .1, .3]],
            "17": [["hooked red kick bottom", 0.50, .3, .8]],
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
            "1": ["Cyan top", 0.2, 0.15, 0.1],
            "1.2": ["Cyan top", 0.8, 0.1, 0.1]
        }
    },
    "hooked bassline":{
        "length": 8,
        "beats":{
            "1": [["Firebrick bottom", 0.7, 0.20, 0.05], ["hooked top sidechain non red", 8], ["hooked claps", 8]]
        }
    },
    "hooked sub melody":{
        "length": 8,
        "beats": {
            "2.25": [["Yellow bottom", 0.15, 0.20, 0.20]],
            "2.5": [["Green bottom", 0.15, 0.20, 0.20]],
            "3": [["Yellow bottom", 0.15, 0.20, 0.20]],
            "3.5": [["Yellow bottom", 0.15, 0.20, 0.20]],
            "4.75": [["Yellow bottom", 0.15, 0.20, 0.10]],
            "5.25": [["Yellow bottom", 0.15, 0.20, 0.10]],
            "5.75": [["Yellow bottom", 0.15, 0.20, 0.10]],
            "6.25": [["Yellow bottom", 0.15, 0.20, 0.10]],
            "6.75": [["Yellow bottom", 0.15, 0.20, 0.10]],
            "7.25": [["Yellow bottom", 0.15, 0.20, 0.10]],
            "7.75": [["Yellow bottom", 0.15, 0.20, 0.10]]
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
            "17": [["Purple bottom", 16, 0.3, 0.05], ["hooked wandering top", 16, .8, .5]],
        }
    },
    "Hooked Show": {
        "length": 2000,
        "beats":{
            "8": [["hooked scream fade", 2, 0.4, 0.2]],
            "9": [["hooked bottom kick intro", 12, .1, .6]],
            "10": [["hooked scream fade", 6, 0.2, 0.1]],
            "21": [["hooked bottom kick intro", 12, .6, .6]],
            "33": [["hooked bottom kick intro", 8, .6, .2]],
            "41": [["wandering", 32]],
            "73": [["wandering", 32]],
            "105": [["hooked bottom kick increase", 32]],
            "133": [["hooked buildup", 4]],
            "137": [["hooked chorus", 128]]
        }
    }
}