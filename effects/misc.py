effects = {
    "Nothing": {
        "length": 1,
        "beats":{
            "1": [[0, 0, 0, 0, 0, 0, 0], 1, 1, 1]
        }
    },
    "Red Top": {
        "length": 1,
        "beats":{
            "1": [[100, 0, 0, 0, 0, 0, 0], 0.25]
        } 
    },
    "Red Top Flash": {
        "length": 0.25,
        "beats":{
            "1": [[100, -100, -100, 0, 0, 0, 0], 0.125, 1, 1]
        } 
    },
    "Hat":{
        "length": 0.5,
        "beats":{
            "1": [[0, 0, 100, 0, 0, 0, 0], 0.25, 1, 1]
        }
    },
    "Red Bass":{
        "length": 2,
        "loop": False,
        "beats":{
            "1": ["Red Top Flash", 2, 1, 0, 0]
        }
    },
    "Red Pulse":{
        "length": 1,
        "loop": False,
        "beats":{
            "1": [[100, 0, 0, 100, 0, 0, 0], 1, 1, 0, 0]
        }
    },
    "Green Pulse":{
        "length": 1,
        "loop": False,
        "beats":{
            "1": [[0, 100, 0, 0, 100, 0, 0], 1, 1, 0, 0]
        }
    },
    "Blue Pulse":{
        "length": 1,
        "loop": False,
        "beats":{
            "1": [[0, 0, 100, 0, 0, 100, 0], 1, 1, 0, 0]
        }
    },
    "UV Pulse":{
        "length": 1,
        "loop": False,
        "beats":{
            "1": [[0, 0, 0, 0, 0, 0, 100], 1, 1, 0, 0]
        }
    },
    "Bassline":{
        "length": 4,
        "beats":{
            "1": "Red Bass",
            "3.5": "Red Bass"
        }
    },
    "Bassline 2":{
        "length": 4,
        "beats":{
            "2": [["Red Bass"]],
            "4": [["Red Bass"]]
        }
    },
    "Show 1":{
        "length": 8,
        "loop": False,
        "beats":{
            "1": [["Hat", 32, 1, 1, 0], ["Bassline", 4, 0, 1, 0]],
            "5": [["Bassline", 28, 1, 1, 4]]
        }
    },
    "Musician Lyrical Oo":{
        "length": 2,
        "beats":{
            "1": [[0, 100, 0, 0, 0, 0, 0], 0.5, 1, 0.2],
            "2": [[0, 80, 100, 0, 0, 0, 0], 0.5, 1, 0.2]
        }
    },
    "sidechain_test":{
        "length": 2,
        "beats":{
            "1.90": [[-30, -30, -30, 0, 0, 0, 100], 0.1, 0, 1],
            "2": [[-30, -30, -30, 0, 0, 0, 100], 0.7, 1, 0]
        }
    },
    "RBBB 1 bar":{
        "length": 4,
        "beats":{
            "1": [[100, 0, 0, 0, 0, 0, 0], 0.25],
            "2": [[0, 0, 100, 0, 0, 0, 0], 0.25],
            "3": [[0, 0, 100, 0, 0, 0, 0], 0.25],
            "4": [[0, 0, 100, 0, 0, 0, 0], 0.25]
        }
    },
    "Rainbow bad":{
        "length": 2,
        "beats":{
            "1": [[40, 0, 0, 0, 0, 0, 0], 0.7],
            "1.7": [[[40, 0, 0, 0, 0, 0, 0], 0.3, 1, 0], [[0, 30, 20, 0, 0, 0, 0], 0.3, 0, 1]],
            "2": [[0, 30, 20, 0, 0, 0, 0], 0.7],
            "2.7": [[[0, 30, 20, 0, 0, 0, 0], 0.3, 1, 0], [[40, 0, 0, 0, 0, 0, 0], 0.3, 0, 1]]
        }
    },
    "Cheesecake time":{
        "length": 8,
        "beats":{
            "7": ["Yellow top", .5, 1, 0],
            "7.5": ["Yellow top", .5, 1, 0],
        }
    },
    "RB Strobe Top Bottom":{
        "length": 0.4,
        "beats":{
            "1": [[[50, 100, 0, 0, 0, 0, 0], 0.07]],
            "1.2": [[[0, 100, 50, 0, 0, 0, 0], 0.07]],
        }
    },
    "cheesecake show":{
        "beats":{
            "1": [["Cheesecake time", 64], ["Rainbow bad", 64]],
            "65": [["Ghosts bassline", 14]],
            "79": [["RB Strobe Top Bottom", 2]],
            "81": [["Cheesecake time", 32], ["Rainbow bad", 32]]
        },
        "delay_lights": 6.3,
        "skip_song": 0.0,
        "bpm": 97,
        "song_path": "songs/Cheesecake.ogg",
        "profiles": ["Shows"]
    },
    "4 Bar Timing Show":{
        "beats":{
            "1": [["RBBB 1 bar", 200]]
        }
    },
    "musician show":{
        "length": 16,
        "beats":{
            "1": [["Rainbow bad", 12], ["sidechain_test", 12]],
            "13": [["Musician Lyrical Oo", 4]]
        },
        "delay_lights": 0.0,
        "skip_song": 0,
        "bpm": 125,
        "song_path": "songs/musician2.ogg",
        "profiles": ["Shows"],
    },
    "Telepathic Love Show":{
        "beats":{
            "1": [["RBBB 1 bar", 200]]
        }
    },
    "Blue Bottom Flash":{
        "length": 1,
        "beats":{
            "1": [[0, 0, 0, 0, 0, 60, 0], 0.25]
        }
    },
    "Blue Top Flash":{
        "length": 1,
        "beats":{
            "1": [[0, 0, 60, 0, 0, 0, 0], 0.25]
        }
    },
    "Flash all":{
        "length": 1,
        "beats":{
            "1": [[100, 100, 100, 100, 100, 100, 0], 0.3, 0.1, 0]
        }
    },
    "Attack repeater":{
        "length": 8,
        "beats":{
            "1": [[20, 0, 20, 0, 0, 0, 0], 0.55, 0.5, 0],
            "2": [[0, 0, 0, 0, 30, 5, 0], 0.55, 0.5, 0],
            "3": [[20, 0, 20, 0, 0, 0, 0], 0.55, 0.5, 0],
            "4": [[0, 0, 0, 0, 30, 5, 0], 0.55, 0.5, 0],
            "5": [[20, 0, 20, 0, 0, 0, 0], 0.3, 0.5, 0],
            "5.5": [[0, 0, 0, 0, 30, 0, 5], 0.3, 1, 0],
            "6": [[0, 0, 0, 0, 0, 0, 70], 0.3, 1, 0],
            "6.5": [[0, 0, 0, 0, 0, 0, 70], 0.3, 1, 0],
            "7": [[0, 0, 0, 0, 0, 0, 70], 1.2, 1, 0]
        }
    },
    "attack show":{
        "beats":{
            "1": [["Green fade", 1]],
            "3": [["Yellow fade", 1]],
            "5": [["Green fade", 1]],
            "7": [["Yellow fade", 1]],
            "9": [["Green fade", 1]],
            "11": [["Yellow fade", 1]],
            "13": [["Green fade", 1]],
            "15": [["Triplets top", 2]],
            "17": [["Flash all", 1], ["Attack repeater", 8]],
            "25": ["Attack repeater", 24]
        },
        "delay_lights": 0.0,
        "skip_song": 0.35,
        "bpm": 144,
        "song_path": "songs/attack_season_4_op.ogg",
        "profiles": ["Shows"],
    },
    "Luigi Bass hits":{
        "length": 4,
        "beats":{
            "1": [["Green fade", 1]],
            "1.75": [["Green fade", 1]],
            "2.5": [["Green fade", 1]],
            "3.35": [["Green fade", 1]],
            "4.25": [["Green fade", 1]]
        }
    },
    "Luigi Bassline":{
        "length": 16,
        "beats":{
            "1": [["Luigi Bass hits", 12]]
        }
    },
    "Luigi Hats":{
        "length": 0.5,
        "beats":{
            "1": [[0, 0, 0, 0, 0, 4, 0], 0.5, 1, 0.4]
        }
    },
    "Luigi Yellow Top":{
        "length": 1,
        "beats":{
            "1": [[20, 20, 0, 0, 0, 0, 0], 1]
        }
    },
    "Luigi Cyan Bottom":{
        "length": 1,
        "beats":{
            "1": [[0, 0, 0, 20, 0, 20, 0], 1]
        }
    },
    "Luigi Whoo":{
        "length": 1,
        "beats":{
            "1": [[0, 5, 0, 10, 0, 10, 5], 0.5, 0, 1],
            "1.5": [[0, 5, 0, 10, 0, 10, 5], 0.35, 1, 0]
        }
    },
    "luigi show":{
        "beats":{
            "1": [["Luigi Bassline", 32]],
            "13": [["UV", 4], ["Luigi Hats", 4]],
            "29": [["UV", 4], ["Luigi Hats", 4]],
            "33": [["Luigi Cyan Bottom", 2]],
            "35": [["Luigi Yellow Top", 2]],
            "37": [["Luigi Cyan Bottom", 2]],
            "39": [["Luigi Yellow Top", 2]],
            "41": [["Luigi Cyan Bottom", 2]],
            "43": [["Luigi Yellow Top", 2]],
            "45": [["Luigi Cyan Bottom", 2]],
            "47": [["Luigi Yellow Top", 2]],
            "51": [["Luigi Cyan Bottom", 0.5]],
            "51.5": [["Luigi Yellow Top", 0.5]],
            "52": [["Luigi Cyan Bottom", 0.5]],
            "52.5": [["Luigi Yellow Top", 0.5]],
            "53": [["Luigi Cyan Bottom", 3]],
            "57.5": [["Luigi Whoo", 1]],
            "59": [["Luigi Bassline", 32]],
            "71": [["UV", 4], ["Luigi Hats", 4]],
            "83": [["UV", 4], ["Luigi Hats", 4]]
        },
        "delay_lights": 0.0,
        "skip_song": 1.74,
        "bpm": 90,
        "song_path": "songs/luigi.ogg",
        "profiles": ["Shows"],
    },
}
