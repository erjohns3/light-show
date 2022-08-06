effects = {
    "Ghosts melody": {
        "length": 32,
        "beats":{
            "1": [["Strobe", 0.6, .5, .5]],
            "2": [["Strobe", 0.6, .5, .5]],
            "3": [["Strobe", 0.6, .5, .5]],
            "4": [["Strobe", 0.6, .5, .5]],
            "9": [["Strobe", 0.6, .5, .5]],
            "10": [["Strobe", 0.6, .5, .5]],
            "15.5": [["Strobe", 0.3, .5, .5]],
            "16.5": [["Strobe", 0.3, .5, .5]],
            "17": [["Strobe", 0.6, .5, .5]],
            "18": [["Strobe", 0.6, .5, .5]],
            "19": [["Strobe", 0.6, .5, .5]],
            "25": [["Strobe", 0.6, .5, .5]],
            "31": [["Strobe", 0.6, .5, .5]],
            "32": [["Strobe", 0.6, .5, .5]],
        }
    },
    "Ghosts bassline": {
        "length": 2,
        "beats":{
            "1": [["Purple bottom", 1, 0.42, .2]],
            "2": [["Green bottom", 1, 0.42, .2]],
        }
    },
    "Ghosts UV": {
        "length": 1,
        "beats":{
            "1": [["UV", .6, 0.6, .2]]
        }
    },
    "Ghosts rainbow":{
        "length": 2,
        "beats":{
            "1": [[40, 0, 0, 0, 0, 0, 0], 0.7],
            "1.7": [[[40, 0, 0, 0, 0, 0, 0], 0.3, 1, 0], [[0, 30, 20, 0, 0, 0, 0], 0.3, 0, 1]],
            "2": [[0, 30, 20, 0, 0, 0, 0], 0.7],
            "2.7": [[[0, 30, 20, 0, 0, 0, 0], 0.3, 1, 0], [[40, 0, 0, 0, 0, 0, 0], 0.3, 0, 1]]
        }
    },
    "RB Strobe Top Bottom":{
        "length": 0.4,
        "beats":{
            "1": [[[50, 100, 0, 0, 0, 0, 0], 0.07]],
            "1.2": [[[0, 100, 50, 0, 0, 0, 0], 0.07]],
        }
    },
    "Ghosts riser":{
        "length": 4,
        "beats":{
            "1": [["Pink bottom", 2, .15, .3]],
            "3": [["Pink bottom", 2, .3, .15]],
        }
    },
    "Ghosts Show": {
        "beats":{
            "17": [["Ghosts melody", 96], ["Ghosts bassline", 96]],
            "81": [["Ghosts UV", 32]],
            "113": [["Rainbow bad", 32]],
            "145": [["RB Strobe Top Bottom", 4, .4, .4], ["Ghosts bassline", 32]],
            "149": [["Rainbow bad", 4]],
            "153": [["RB Strobe Top Bottom", 4, .4, .4]],

            # "145": [["Ghosts melody", 96], ["Ghosts bassline", 96], ["UV", 96, .4, .4]],
            "177": [["Ghosts melody", 64], ["Ghosts bassline", 64], ["UV", 64, .4, .4]],
            "209": [["Ghosts UV", 32]],
        }
    }
}