from socket import socket
import os, time
from fernet import Fernet
from multiprocessing import Process
from server_data import read_csv, save_csv
from typing import Final
from configparser import RawConfigParser

local_socket = socket()
BUFSIZE: Final[int] = 4096

def code_to_str(code: int) -> str:
    if code == 200: return 'Successfully set up server!'
    else: return 'Error!'


def server_setup(ip: str = None, port: int = None):
    '''Setup for the the server'''
    
    if os.path.isfile(f'{os.getcwd()}/server_data/configs/default.ini'):
        config = RawConfigParser()
        config.read(f"{os.getcwd()}/server_data/configs/default.ini")
        data = dict(config.items('DEFAULT'))
        return socket_test(data['address'], int(data['port']))
    else:
        return 404
            
def socket_test(ip: str, port: int):
    global local_socket
    local_socket.bind((ip, port))
    local_socket.listen(5)
    print('Testing server socket...')
    test_s = socket()
    test_s.connect((ip, port))
    client, addr = local_socket.accept()
    data_to_send = ("200").encode()
    test_s.sendall(data_to_send)
    test_data = client.recv(BUFSIZE).decode()
    client.close()
    if test_data == '200':
        print(f'Serving on {ip}:{port}')
        return 200
    

def create_child_process(client: object, target, extra_args):
    '''Creates a child process that has a target and returns something.'''

if __name__ == '__main__':
    

    print(code_to_str(server_setup()))
    print('Awaiting connections...')
    while True:
        time.sleep(5)
