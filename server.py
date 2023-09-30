from socket import socket
import os, json
from fernet import Fernet
from multiprocessing import Process
from server_data import read_csv, save_csv
from typing import Final
from configparser import RawConfigParser

class Client:
    def __init__(self, client: socket, address, username) -> None:
        self.__username =  username
        self.__client = client
        self.__address = address
        self.__key = None
        self.__fernet_obj = None

    def login(self):
        '''Processes the login of the client.'''
        self.__key = Fernet.generate_key()
        self.__fernet_obj = Fernet(self.__key)
        self.__client.sendall(json.dumps({'sec': self.__key.decode()}).encode())
        user_data = self.__client.recv(BUFSIZE) # Login details in dict.
local_socket = socket()
# local_socket.settimeout(5)
BUFSIZE: Final[int] = 4096


def code_to_str(code: int) -> str:
    '''Converts http code to letters.'''
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
    '''Tests sockets before using them.'''
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
    test_s.close()
    if test_data == '200':
        print(f'\nServing on {ip}:{port}\n')
        return 200
    else: return 404
    
def await_client():
    '''Waits for client to connect.'''
    while True:
        client, addr = local_socket.accept()
        print(f'Connection from {addr} incoming. Accepting...')

def create_child_process(client: object, target, extra_args):
    '''Creates a child process that has a target and returns something.'''

if __name__ == '__main__':
    

    print(code_to_str(int(server_setup())))
    print('Awaiting connections...')
    await_client()
