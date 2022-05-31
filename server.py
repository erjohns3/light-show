from ast import Num
from operator import length_hint
import threading
from types import new_class
import pigpio
import time
import sys
import json
import signal
import pathlib
import asyncio
import websockets
import http.server
import argparse
import os
from os import path
import math


LIGHT_PERIOD = 0.005


args = False
pi = None
light_task = False
light_mode = ""
rate = 120


async def set_light(new_mode, new_rate):
    global light_mode
    global light_task
    global rate

    if light_task:
        light_task.cancel()

    print("mode: " + str(new_mode))
    light_mode = new_mode
    rate = new_rate
    
    light_task = asyncio.create_task(light())

####################################

RED_PIN = 9
GREEN_PIN = 10
BLUE_PIN = 11

async def light():    

    beats = config[light_mode]['beats']
    length = config[light_mode]['length'] * 60 / rate

    start = time.time()

    while True:
        
        for key in beats:
            color = beats[key]
            beat = float(key) * 60 / rate

            while time.time() - start < beat: await asyncio.sleep(LIGHT_PERIOD)
            
            # pi.set_PWM_dutycycle(RED_PIN, color[0])
            # pi.set_PWM_dutycycle(GREEN_PIN, color[1])
            # pi.set_PWM_dutycycle(BLUE_PIN, color[2])  
            # print(f'{time.time() - start} : {color}')

        while time.time() - start < length: await asyncio.sleep(LIGHT_PERIOD)

        start += length

#################################################

async def init(websocket, path):
    global light_mode
    
    message = {
        'config': config,
        'status': {
            'rate': rate,
            'mode': light_mode
        }
    }
    dump = json.dumps(message)
    try:
        await websocket.send(dump)
    except:
        print("socket send failed", flush=True)

    while True:
        try:
            msg_string = await websocket.recv()
        except:
            print("socket recv FAILED - " + websocket.remote_address[0] + " : " + str(websocket.remote_address[1]), flush=True)
            break
        print("socket recv - " + websocket.remote_address[0] + " : " + str(websocket.remote_address[1]), flush=True)
        msg = json.loads(msg_string)
        print(msg, flush=True)

        if 'type' in msg:

            if msg['type'] == 'start':
                await set_light(msg['mode'], msg['rate'])

            message = {
                'status': {
                    'mode': light_mode,
                    'rate': rate
                }
            }
            dump = json.dumps(message)
            try:
                await websocket.send(dump)
            except:
                print("socket send failed", flush=True)

######################################

def setup_pigpio():
    global pi
    pi = pigpio.pi()
    if not pi.connected:
        exit()

    pi.set_mode(RED_PIN, pigpio.OUTPUT)
    pi.set_mode(GREEN_PIN, pigpio.OUTPUT)
    pi.set_mode(BLUE_PIN, pigpio.OUTPUT)

    pi.set_PWM_dutycycle(RED_PIN, 0)
    pi.set_PWM_dutycycle(GREEN_PIN, 0)
    pi.set_PWM_dutycycle(BLUE_PIN, 0)

    pi.set_PWM_frequency(RED_PIN, 1000)
    pi.set_PWM_frequency(GREEN_PIN, 1000)
    pi.set_PWM_frequency(BLUE_PIN, 1000)

#################################################

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        http.server.SimpleHTTPRequestHandler.end_headers(self)
        
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def http_server(testing=False):
    httpd = http.server.ThreadingHTTPServer(("", PORT), Handler)
    print("serving at port " + str(PORT), flush=True)
    httpd.serve_forever()

################################################

loc = pathlib.Path(__file__).parent.absolute()
drink_io_folder = str(loc)

with open(path.join(drink_io_folder, 'config.json'), 'r') as f:
    config = json.loads(f.read())

# for mode in config:
#     print(f'{mode}:')
#     for color in config[mode]:
#         print(f'    {color}:')

##################################################

def signal_handler(sig, frame):
    print('SIG Handler: ' + str(sig), flush=True)
    if pi is None:
        print('signal_handler skipped for testing', flush=True)
    else:
        pi.set_PWM_dutycycle(RED_PIN, 0)
        pi.set_PWM_dutycycle(GREEN_PIN, 0)
        pi.set_PWM_dutycycle(BLUE_PIN, 0)

        pi.stop()

    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

#################################################

def run_asyncio():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    start_server = websockets.serve(init, "0.0.0.0", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--testing', action='store_true', default=False,
                   help='To run webserver without drinkmaker attached')
    parser.add_argument('--local', action='store_true', default=False,
                   help='To run webserver without drinkmaker attached')
    args = parser.parse_args()

    #if not args.testing:
        #setup_pigpio()

    http_thread = threading.Thread(target=http_server, args=[args.testing], daemon=True)
    http_thread.start()

    run_asyncio()


if __name__ == "__main__":
    main()
