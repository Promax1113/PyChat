from socket import socket
import os, json, security, time
from fernet import Fernet
from multiprocessing import Process
import asyncio
from server_data import read_csv, save_csv
from typing import Final
from configparser import RawConfigParser

loop = asyncio.get_event_loop()


class Client:
    def __init__(self, client: socket, address: tuple) -> None:
        self.__username =  None
        self.__client: socket = client
        self.__address: tuple = address
        self.__key: str = None
        self.__is_authed = False
        self.__fernet_obj: Fernet = None

    async def login(self):
        '''Processes the login of the client.'''
        print('Started Login...')
        self.__key = Fernet.generate_key().decode()
        self.__fernet_obj = Fernet(self.__key.encode())
        await loop.sock_sendall(self.__client, json.dumps({'sec': self.__key}).encode())
        print('Sent key!')
        data = await loop.sock_recv(self.__client, BUFSIZE)
        user_data = json.loads(self.__fernet_obj.decrypt(data)) # Login details in dict.
        login_result = security.pass_check(user_data['username'], user_data['password'])
        await loop.sock_sendall(self.__client, code_to_str(login_result, print_o=False).encode())
        print('sent!')
        if login_result == 200:
            self.__is_authed = True
            return None
        else:
            self.__client.close()
            print('Closed connection!')

        await asyncio.sleep(1)

    async def receive(self, decode):
        data = None
        while not data:
            data = await loop.sock_recv(self.__client, BUFSIZE)
        return data

        
local_socket = socket()
# local_socket.settimeout(5)
BUFSIZE: Final[int] = 8192


def code_to_str(code: int, print_o = True):
    '''Converts http code to letters.'''
    if print == True:
        if code == 200: print('Success!')
        else: print('Error!')
    else:
        if code == 200: return 'Success!'
        else: return 'Error!'


def server_setup(ip: str = None, port: int = None):
    '''Setup for the the server'''
    
    if os.path.isfile(f'{os.getcwd()}/server_data/configs/default.ini'):
        config = RawConfigParser()
        config.read(f"{os.getcwd()}/server_data/configs/default.ini")
        data = dict(config.items('DEFAULT'))
        return socket_test(data['address'], int(data['port']))
    else:
        raise FileNotFoundError('/server_data/configs/default.ini not found.')
            
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
    
async def await_client():
    '''Waits for client to connect.'''
    while True:
        client, addr = await loop.sock_accept(local_socket)
        print(f'Connection from {addr} incoming. Accepting...')
        asyncio.create_task(handle_client(client, addr))

async def handle_client(client, addr):
    '''Handle a single client connection.'''
    c = Client(client, addr)
    await c.login()
    user_list.append(c)
    print(c)
    print(user_list)
    
user_list: list[Client] = []

    
if __name__ == '__main__':
    
    code_to_str(int(server_setup()))
    print('Awaiting connections...')
    loop.run_until_complete(await_client())
