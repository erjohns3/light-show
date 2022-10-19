import socket
import asyncio
import json
import time
import threading
import random

import websocket

from helpers import *


# docs: https://github.com/Unreal-Dan/RekordBoxSongExporter




connected_to_light_show_server = False
def wait_for_light_show_connection():
    global connected_to_light_show_server
    while not connected_to_light_show_server:
        print_blue('Sleeping because not connected to light show server')
        time.sleep(1)

def send_to_light_show_server(string):
    global dj_client
    wait_for_light_show_connection()
    dj_client.send(string)



def send_effect(show):
    dict_to_send = {
        'type': 'add_effect',
        'effect': show,
    }
    send_to_light_show_server(json.dumps(dict_to_send))


def send_time_and_bpm(data, string_recieved):
    try:
        float(data['master_time'])
        float(data['master_bpm'])
    except:
        print(f'idk, data wasnt floats {data}, raw string was {string_recieved}')
        return
        
    dict_to_send = {
        'type': 'time_and_current_bpm',
        'time': data['master_time'],
        'current_bpm': data['master_bpm'],
    }
    send_to_light_show_server(json.dumps(dict_to_send))

def send_show_title_original_bpm(title, original_bpm):
    dict_to_send = {
        'type': 'track_changed',
        'title': title,
        'original_bpm': original_bpm,
    }
    send_to_light_show_server(json.dumps(dict_to_send))



def rekord_box_server():
    wait_for_light_show_connection()

    REKORDBOX_HOST = "127.0.0.1"
    REKORDBOX_PORT = 22345

    last_sent = float('-inf')
    current_title = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((REKORDBOX_HOST, REKORDBOX_PORT))
        s.listen()
        print_green('Waiting for connection from rekordbox reading client')
        conn, addr = s.accept()
        with conn:
            print_green(f'Connected to rekordbox reading client: {addr}')
            while True:
                string_recieved = conn.recv(1024).decode()
                if 'rt_master_time' in string_recieved:
                    print_green(f'==== INIT CONFIG ====: "{string_recieved}"')                
                    continue

                if random.randint(1, 500) == 500:
                    print_green(f'RANDOM SAMPLED RAW DATA: {string_recieved}')

                for index, line in enumerate(string_recieved.split('\n')):
                    line = line.strip()
                    if not line:
                        continue
                    if index > 0:
                        print_green(f'In this raw data there were multiple lines for some reason... raw string: {string_recieved}')
                    if 'quytdhsdg' not in line:
                        print_green(f'In this raw data there wasnt quytdhsdg... raw string: {string_recieved}')
                        continue

                    # format coming in: %title% quytdhsdg %key%, %rt_master_time%, %rt_master_bpm%, %rt_master_total_time%, %bpm%             
                    title, rest = line.split('quytdhsdg')
                    stuff = list(map(lambda x: x.strip(), rest.split(',')))
                    data = {
                        'title': title,
                        'key': stuff[0],
                        'master_time': stuff[1],
                        'master_bpm': stuff[2],
                        'master_total_time': stuff[3],
                        'original_bpm': stuff[4],
                        # 'deck_1_bpm': stuff[5],
                        # 'deck_2_bpm': stuff[6],
                    }

                    if len(data['title']) > 3:
                        print_green(f'======= TRACK CHANGE ===== {last_sent} RAW DATA: "{string_recieved}"')
                        print_green(f'======= {last_sent} PROCESSED DATA: "{data}"')
                        current_title = data['title'][2:].strip()
                        send_show_title_original_bpm(current_title, data['original_bpm'])
                    
                    if time.time() > (last_sent + .5):
                        send_time_and_bpm(data, string_recieved)
                        last_sent = time.time()

                    if not data:
                        print_red('DATA FROM REKORDBOX WAS EMPTY, EXITING')
                        break
threading.Thread(target=rekord_box_server).start()




def light_show_on_open(wsapp):
    global connected_to_light_show_server
    connected_to_light_show_server = True
    print_blue('Is connected to light show!')

def light_show_on_close(wsapp):
    global connected_to_light_show_server
    connected_to_light_show_server = False

def light_show_on_error(wsapp, error):
    print_red('light_show_on_error, retrying in 1 second...')
    time.sleep(1)
    try_make_light_show_connection()


def light_show_on_message(wsapp, message):
    print_blue('Got from light show server:', message)


dj_client = None
def try_make_light_show_connection():
    global dj_client
    dj_client = websocket.WebSocketApp("ws://localhost:1567", on_error=light_show_on_error, on_open=light_show_on_open, on_message=light_show_on_message, on_close=light_show_on_close)
    try:
        dj_client.run_forever(ping_interval=10, ping_timeout=9, ping_payload="{\"ok\": \"ok2\"}") 
    except Exception as e:
        # import traceback
        # traceback.format_exc()
        print_red(f'dj_client.run_forever EXCEPTION: {e}')
        exit()

try_make_light_show_connection()



# dj_client = websocket.create_connection("ws://localhost:1567")
# time.sleep(.5)



# format stuff
# b'2:209040 76692 87.50 0 - 87.50 - %rt_deck2_bpm% \n'

# %title% ,,, %key% ,,, %rt_master_time% ,,, %rt_master_bpm% ,,, %rt_master_total_time%  ,,, %rt_deck1_bpm% ,,, %rt_deck2_bpm%
# ['2:223249 ', ' 173 ', ' 115 ', ' 0 ', ' 115 ', '']

# %title% ,,, %key% ,,, %rt_master_time% ,,, %rt_master_bpm% ,,, %rt_master_total_time%  ,,, %rt_deck1_bpm% ,,, %rt_deck2_bpm%
# %title% %key% %rt_master_time% %rt_master_bpm% %rt_master_total_time%  %rt_deck1_bpm% %rt_deck2_bpm%
# %title% %rt_master_time%

# ['1: ', '  ', ' 80301 ', ' 93.50 ', ' 210793  ', ' 0 ', ' 93.50']

# %rt_deck1_bpm% %rt_deck2_bpm%