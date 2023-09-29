from socket import socket
import os
from fernet import Fernet
from multiprocessing import Process
from server_data import read_csv, save_csv
from typing import Final

local_socket = socket()
BUFSIZE: Final[int] = 4096
def server_setup(ip: str, port: int):
    '''Setup for the the server'''
    if not os.path.isfile(f'{os.getcwd}/server_data/config/server.cfg'):
        with open(''): #Save ip
            socket_test(ip, port)
    
def socket_test(ip: str, port: int):
    global local_socket
    local_socket.bind((ip, port))
    local_socket.listen(5)
    try:
        print('Testing server socket...')
        test_s = socket()
        test_s.connect((ip, port))
        local_socket.accept()
        test_s.sendall('200'.encode())
        test_data = local_socket.recv(BUFSIZE).decode()
        if test_data == '200': return 200
        else: raise Exception()

    except:
        return 404

def create_child_process(client: object, target, extra_args):
    '''Creates a child process that has a target and returns something.'''

if __name__ == '__main__':
    success_tls = lambda x: 'Success' if x == 200 else 'Error!'

    print(success_tls(server_setup('127.0.0.1', 585)))