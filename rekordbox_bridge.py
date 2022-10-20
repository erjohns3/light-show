import socket
import asyncio
import json
import time
import threading
import random

import websocket

from helpers import *


# docs: https://github.com/Unreal-Dan/RekordBoxSongExporter


# light_show_server = 'localhost'
light_show_server = '192.168.86.55'


rt_data_ready_to_send = None
track_data_ready_to_send = None
def rekord_box_server():
    global rt_data_ready_to_send, track_data_ready_to_send
    REKORDBOX_HOST = "127.0.0.1"
    REKORDBOX_PORT = 22345

    current_title = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((REKORDBOX_HOST, REKORDBOX_PORT))
        # s.settimeout(.01)
        s.listen()
        print_green('Waiting for connection from rekordbox reading client')
        # while True:
        #     try:
        conn, addr = s.accept()
        # conn.settimeout(.01)
            #     break
            # except:
            #     pass
    
        with conn:
            print_green(f'Connected to rekordbox reading client: {addr}')
            while True:
                # try:
                data_recieved = conn.recv(1024)
                # except socket.timeout as e:
                #     if data is not None:
                #         print_yellow('Recieved no data from rekordbox, sending prev data')
                #         send_time_and_bpm(data)
                #         continue

                string_recieved = data_recieved.decode()
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
                        print_red(f'RAW DATA HAS MULTIPLE LINES, HAVING TROUBLE KEEPING UP SKIPPING ALL BUT FIRST... raw string: {string_recieved}')
                        continue
                    if 'quytdhsdg' not in line:
                        print_green(f'In this raw data there wasnt quytdhsdg... raw string: {string_recieved}')
                        continue

                    # format coming in: %title% quytdhsdg %key%, %rt_master_time%, %rt_master_bpm%, %rt_master_total_time%, %bpm%             
                    title, rest = line.split('quytdhsdg')
                    stuff = list(map(lambda x: x.strip(), rest.split(',')))
                    if len(stuff) < 5:
                        print_red(f'the above data shouldnt have less than 5 elements after quytdhsdg')
                        continue
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
                        data['title'] = data['title'][2:].strip()
                        data['title'] = data['title'].replace('.', '_')

                        with lock_track_copy:
                            track_data_ready_to_send = data
                    else:
                        with lock_rt_copy:
                            rt_data_ready_to_send = {
                                'master_time': data['master_time'],
                                'master_bpm': data['master_bpm'],
                            }

                    #     print_green(f'======= TRACK CHANGE ===== {last_sent} RAW DATA: "{string_recieved}"')
                    #     print_green(f'======= {last_sent} PROCESSED DATA: "{data}"')
                    #     send_to_light_show_server(data)
                    
                    # elif time.time() > (last_sent + .01):
                    #     send_time_and_bpm(data, string_recieved)
                    #     last_sent = time.time()

                    if not data:
                        print_red('DATA FROM REKORDBOX WAS EMPTY, EXITING')
                        break
threading.Thread(target=rekord_box_server).start()




last_sent = float('-inf')
connected_to_light_show_server = False
def wait_for_light_show_connection():
    global connected_to_light_show_server
    while not connected_to_light_show_server:
        print_blue('Sleeping because not connected to light show server')
        time.sleep(1)


def send_to_light_show_server(dictionary):
    global dj_client
    wait_for_light_show_connection()
    dictionary['timestamp'] = time.time()
    dj_client.send(json.dumps(dictionary))

def send_time_and_bpm(dict_to_send):
    try:
        float(dict_to_send['master_time'])
        float(dict_to_send['master_bpm'])
    except:
        print(f'idk, data wasnt floats {dict_to_send}')
        return
    send_to_light_show_server(dict_to_send)


from copy import deepcopy
lock_track_copy, lock_rt_copy = threading.Lock(), threading.Lock()
def light_show_client_sender():
    global last_sent, rt_data_ready_to_send, track_data_ready_to_send
    while True:
        if track_data_ready_to_send:
            print_green(f'======= TRACK CHANGE ===== {last_sent}')
            print_green(f'======= {last_sent} PROCESSED DATA: "{track_data_ready_to_send}"')
            with lock_track_copy:
                track_data_ready_to_send_copied = deepcopy(track_data_ready_to_send)
                track_data_ready_to_send =  None
            send_to_light_show_server(track_data_ready_to_send_copied)
        elif rt_data_ready_to_send and time.time() > (last_sent + .01):
            with lock_rt_copy:
                rt_data_copied = deepcopy(rt_data_ready_to_send)
            send_time_and_bpm(rt_data_copied)
            last_sent = time.time()
        time.sleep(.08)
threading.Thread(target=light_show_client_sender).start()


# def send_pause_if_no_update():
#     global last_sent
#     if global last

# threading.Thread(target=send_pause_if_no_update).start()




def light_show_on_open(wsapp):
    global connected_to_light_show_server
    connected_to_light_show_server = True
    print_blue('Is connected to light show!')

def light_show_on_close(wsapp):
    global connected_to_light_show_server
    connected_to_light_show_server = False

def light_show_on_error(wsapp, error):
    global connected_to_light_show_server
    connected_to_light_show_server = False
    print_red('light_show_on_error, retrying in 1 second...')
    time.sleep(1)
    try_make_light_show_connection()


def light_show_on_message(wsapp, message):
    print_blue('Got from light show server:', message)


dj_client = None
def try_make_light_show_connection():
    global dj_client
    dj_client = websocket.WebSocketApp(f"ws://{light_show_server}:1567", on_error=light_show_on_error, on_open=light_show_on_open, on_message=light_show_on_message, on_close=light_show_on_close)
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