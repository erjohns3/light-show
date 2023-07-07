import time
import serial
import random
import math
import socket
import signal
import sys


grid_serial = serial.Serial(
    port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
    baudrate = 2000000,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)  

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 7002  # Port to listen on (non-privileged ports are > 1023)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
while True:
    connection, address = server.accept()
    print(f"Connected by {address}")
    while True:
        data = connection.recv(640)
        if not data:
            print('Connection Lost')
            break

        print(data)

        grid_serial.write(data)
