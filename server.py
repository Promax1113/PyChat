import asyncio
import json
import os
from configparser import RawConfigParser
from socket import socket
from typing import Final

from fernet import Fernet

import security

loop = asyncio.get_event_loop()


class Client:
    def __init__(self, client: socket, address: tuple) -> None:
        self.__username = None
        self.__client: socket = client
        self.__address: tuple = address
        self.__key: str = None
        self.__is_authed = False
        self.__fernet_obj: Fernet = None

    async def login(self):
        """Processes the login of the client."""
        self.__key = Fernet.generate_key().decode()
        self.__fernet_obj = Fernet(self.__key.encode())
        await loop.sock_sendall(self.__client, json.dumps({'sec': self.__key}).encode())
        data = await loop.sock_recv(self.__client, BUFSIZE)
        user_data = json.loads(self.__fernet_obj.decrypt(data))  # Login details in dict.
        self.__username = user_data['username']
        login_result = security.pass_check(user_data['username'], user_data['password'])
        await loop.sock_sendall(self.__client, code_to_str(login_result, print_o=False).encode())
        if login_result == 200:
            self.__is_authed = True
            return None
        else:
            self.__client.close()
            print('Closed connection!')

        await asyncio.sleep(1)

    async def receive(self, decode: bool = True):
        if decode:
            data = await loop.sock_recv(self.__client, BUFSIZE)
            return data.decode()
        else:
            data = await loop.sock_recv(self.__client, BUFSIZE)

    async def send(self, data, encode: bool = True):
        if encode:
            await loop.sock_sendall(self.__client, data.encode())
        else:
            await loop.sock_sendall(self.__client, data)

    def get_info(self):
        return {'username': self.__username}


local_socket = socket()
BUFSIZE: Final[int] = 8192
username_list: list[str] = []


def code_to_str(code: int, print_o=True):
    """Converts http code to letters."""
    if print_o:
        if code == 200:
            print('Success!')
        else:
            print('Error!')
    else:
        if code == 200:
            return 'Success!'
        else:
            return 'Error!'


def server_setup(ip: str = None, port: int = None):
    """Setup for the server."""

    if os.path.isfile(f'{os.getcwd()}/server_data/configs/default.ini'):
        config = RawConfigParser()
        config.read(f"{os.getcwd()}/server_data/configs/default.ini")
        data = dict(config.items('DEFAULT'))
        return socket_test(data['address'], int(data['port']))
    else:
        raise FileNotFoundError('/server_data/configs/default.ini not found.')


def socket_test(ip: str, port: int):
    """Tests sockets before using them."""
    global local_socket
    local_socket.bind((ip, port))
    local_socket.listen(5)
    print('Testing server socket...')
    test_s = socket()
    test_s.connect((ip, port))
    client, addr = local_socket.accept()
    data_to_send = "200".encode()
    test_s.sendall(data_to_send)
    test_data = client.recv(BUFSIZE).decode()
    client.close()
    test_s.close()
    if test_data == '200':
        print(f'\nServing on {ip}:{port}\n')
        return 200
    else:
        return 404


async def await_client():
    """Waits for a client to connect."""
    while True:
        client, addr = await loop.sock_accept(local_socket)
        print(f'Connection from {addr} incoming. Accepting...')
        asyncio.create_task(handle_client(client, addr))


async def handle_client(client, addr):
    """Handle a single client connection."""
    global username_list
    c = Client(client, addr)
    await c.login()
    user_list.append(c)
    username_list = [username.get_info()['username'] for username in user_list]
    await handle_command(c)


async def send_message_callback(c: Client):
    # TODO Make it send a form w/ the recipient
    await c.send(json.dumps({'mode': 'send', 'message': None, 'recipient': None, 'author': c.get_info()['username']}))
    message = json.loads(await c.receive())
    print(username_list)
    for username in username_list:
        if username == message['recipient']:
            await user_list[username_list.index(username)].send(json.dumps(message))


async def read_message_callaback(c: Client):
    await c.send(json.dumps({'mode': 'read'}))


async def handle_command(c: Client):
    command_list = ['send_message', 'read_message']
    await c.send(str(command_list), encode=True)
    choice = await c.receive()
    match choice:
        case 'send_message':
            await send_message_callback(c)
        case 'read_message':
            await read_message_callaback(c)


user_list: list[Client] = []

if __name__ == '__main__':
    code_to_str(int(server_setup()))
    print('Awaiting connections...')
    loop.run_until_complete(await_client())
