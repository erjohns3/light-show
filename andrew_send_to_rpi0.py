from paramiko import SSHClient
from scp import SCPClient

from helpers import *

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(hostname='192.168.86.224',  # rpi0
            port = 22,
            username='pi',
            password='easy')

copy_to_location = '/home/pi/temp/light-show-andrew'
# scp -r /home/andrew/programming/python/light-show rpi0:/home/pi/temp/light-show-andrew

scp = SCPClient(ssh.get_transport())
scp.put(python_file_directory, copy_to_location, recursive=True)
scp.close()