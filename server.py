from socket import socket
import os, json, security
from fernet import Fernet
from multiprocessing import Process
from server_data import read_csv, save_csv
from typing import Final
from configparser import RawConfigParser

class Client:
    def __init__(self, client: socket, address: tuple) -> None:
        self.__username =  None
        self.__client: socket = client
        self.__address: tuple = address
        self.__key: str = None
        self.__is_authed = False
        self.__fernet_obj: Fernet = None

    def login(self):
        '''Processes the login of the client.'''
        self.__key = Fernet.generate_key().decode()
        self.__fernet_obj = Fernet(self.__key.encode())
        self.__client.sendall(json.dumps({'sec': self.__key}).encode())
        user_data = json.loads(self.__fernet_obj.decrypt(self.__client.recv(BUFSIZE))) # Login details in dict.
        login_result = security.pass_check(user_data['username'], user_data['password'])
        code_to_str(login_result)
        if login_result == 200:
            self.__is_authed = True

    def receive(self, decode):
        data = None
        while not data:
            data = self.__client.recv(BUFSIZE)
        return data

        
local_socket = socket()
# local_socket.settimeout(5)
BUFSIZE: Final[int] = 4096


def code_to_str(code: int) -> None:
    '''Converts http code to letters.'''
    if code == 200: print('Successfully set up server!')
    else: print('Error!')


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
        create_child_process(client, Client(client, addr).login())

def create_child_process(client: object, target: function, extra_args: any = None):
    '''Creates a child process that has a target and returns something.'''
    Process(target=target, args=extra_args)
    
if __name__ == '__main__':
    

    code_to_str(int(server_setup()))
    print('Awaiting connections...')
    await_client()
