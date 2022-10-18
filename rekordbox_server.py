import socket
import asyncio
import json
import time
import threading
import random

import websocket


                # format recieved
                # b'2:209040 76692 87.50 0 - 87.50 - %rt_deck2_bpm% \n'

                # %title% ,,, %key% ,,, %rt_master_time% ,,, %rt_master_bpm% ,,, %rt_master_total_time%  ,,, %rt_deck1_bpm% ,,, %rt_deck2_bpm%
                # ['2:223249 ', ' 173 ', ' 115 ', ' 0 ', ' 115 ', '']

                # %title% ,,, %key% ,,, %rt_master_time% ,,, %rt_master_bpm% ,,, %rt_master_total_time%  ,,, %rt_deck1_bpm% ,,, %rt_deck2_bpm%
                # %title% %key% %rt_master_time% %rt_master_bpm% %rt_master_total_time%  %rt_deck1_bpm% %rt_deck2_bpm%
                # %title% %rt_master_time%
                
                # ['1: ', '  ', ' 80301 ', ' 93.50 ', ' 210793  ', ' 0 ', ' 93.50']

                # %rt_deck1_bpm% %rt_deck2_bpm%



def send_effect(show):
    dict_to_send = {
        'type': 'add_effect',
        'effect': show,
    }
    msg_to_send = json.dumps(dict_to_send)
    dj_client.send(msg_to_send)


def send_time_and_bpm(data):
    try:
        float(data['master_time'])
        float(data['master_bpm'])
    except:
        print(f'idk, data isnt floats {data}')
        return
        
    dict_to_send = {
        'type': 'time_and_bpm',
        'time': data['master_time'],
        'bpm': data['master_bpm'],
    }
    msg_to_send = json.dumps(dict_to_send)
    dj_client.send(msg_to_send)


def send_show_title(title):
    dict_to_send = {
        'type': 'title',
        'title': title,
    }
    msg_to_send = json.dumps(dict_to_send)
    dj_client.send(msg_to_send)


connected = False
def rekord_box_shit():
    global connected
    while not connected:
        time.sleep(.05)

    REKORDBOX_HOST = "127.0.0.1"
    REKORDBOX_PORT = 22345

    last_sent = float('-inf')
    current_title = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((REKORDBOX_HOST, REKORDBOX_PORT))
        s.listen()
        print('waiting for connection')
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                string_recieved = conn.recv(1024).decode()
                print(f'RAW DATA: {string_recieved}')
                if 'rt_master_time' in string_recieved:
                    print(f'INIT CONFIG: "{string_recieved}"')                
                    continue

                for line in string_recieved.split('\n'):
                    if 'quytdhsdg' not in line:
                        continue
                    title, rest = line.split('quytdhsdg')
                    stuff = list(map(lambda x: x.strip(), rest.split(',')))
                    print(stuff)
                    # %title% quytdhsdg %key%, %rt_master_time%, %rt_master_bpm%, %rt_master_total_time%               
                    data = {
                        'title': title,
                        'key': stuff[0],
                        'master_time': stuff[1],
                        'master_bpm': stuff[2],
                        'master_total_time': stuff[3],
                        # 'deck_1_bpm': stuff[4],
                        # 'deck_2_bpm': stuff[5],
                    }

                    if len(data['title']) > 3:
                        print(f'========TITLE ===== {last_sent} RECIEVED FROM REKORDBOX: "{data}"')                
                        current_title = data['title'][2:].strip()
                        send_show_title(current_title)
                    
                    if time.time() > (last_sent + .5):
                        print(f'{last_sent} sending ours: "{data}"')                
                        send_time_and_bpm(data)
                        last_sent = time.time()

                    if not data:
                        print('DATA WAS EMPTY, EXITING')
                        break

ok = threading.Thread(target=rekord_box_shit)
ok.start()

def on_open(wsapp):
    global connected
    connected = True

def on_message(wsapp, message):
    print('Got from server:', message)



dj_client = websocket.WebSocketApp("ws://localhost:1567", on_open=on_open, on_message=on_message)
dj_client.run_forever(ping_interval=10, ping_timeout=9, ping_payload="{\"ok\": \"ok2\"}") 



# dj_client = websocket.create_connection("ws://localhost:1567")
# time.sleep(.5)