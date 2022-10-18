import socket
import asyncio
import json
import time
import random

import websocket

REKORDBOX_HOST = "127.0.0.1"
REKORDBOX_PORT = 22345


# connected = False
# def on_open(wsapp):
#     global connected
#     connected = True

# def on_message(wsapp, message):
#     print('Got from server:', message)
# dj_client = websocket.WebSocketApp("ws://localhost:1567", on_open=on_open, on_message=on_message)

# while not connected:
#     time.sleep(.05)
# dj_client.run_forever() 


dj_client = websocket.create_connection("ws://localhost:1567")

def send_effect(show):
    dict_to_send = {
        'type': 'add_effect',
        'effect': show,
    }
    msg_to_send = json.dumps(dict_to_send)
    dj_client.send(msg_to_send)

send_effect('remember show')


last_sent = float('-inf')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((REKORDBOX_HOST, REKORDBOX_PORT))
    s.listen()
    print('waiting for connection')
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            # format recieved
            # b'2:209040 76692 87.50 0 - 87.50 - %rt_deck2_bpm% \n'

            # %title% ,,, %key% ,,, %rt_master_time% ,,, %rt_master_bpm% ,,, %rt_master_total_time%  ,,, %rt_deck1_bpm% ,,, %rt_deck2_bpm%
            # ['2:223249 ', ' 173 ', ' 115 ', ' 0 ', ' 115 ', '']


            # %title% ,,, %key% ,,, %rt_master_time% ,,, %rt_master_bpm% ,,, %rt_master_total_time%  ,,, %rt_deck1_bpm% ,,, %rt_deck2_bpm%
            

            data = conn.recv(1024)
            data = data.decode().strip().split(',,,')

            if time.time() > (last_sent + .5):
                
                if random.randint(1, 2) == 1:
                    send_effect('remember show')
                else:
                    send_effect('butter show')
                last_sent = time.time()
                print(f'{last_sent} RECIEVED FROM REKORDBOX: "{data}", trying to send to dj "{msg_to_send}"')

            if not data:
                print('DATA WAS EMPTY, EXITING')
                break
