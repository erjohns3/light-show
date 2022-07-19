from paramiko import SSHClient
from scp import SCPClient

from helpers import *

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(hostname='192.168.86.224',  # rpi0
            port = 22,
            username='pi',
            password='easy')

# SCPCLient takes a paramiko transport as its only argument
scp = SCPClient(ssh.get_transport())
scp.put(python_file_directory, '/home/pi/temp/light-show-andrew', recursive=True)
scp.close()