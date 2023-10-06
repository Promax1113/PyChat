import getpass
import json
import socket
from time import sleep
from typing import Final

from fernet import Fernet

c = socket.socket()
BUFSIZE: Final[int] = 8192


def receive():
    pass


def send():
    pass


def code_to_str(code: int) -> None:
    """Converts http code to letters."""
    if code == 200:
        print('Successfully set up server!')
    else:
        print('Error!')


def connect(ip: str, port: int):
    global c
    tries = 0

    try:
        c.connect((ip, port))
        print(f'Connected to {ip}:{port} successfully.')
        login()
    except ConnectionRefusedError:
        if tries <= 10:
            print('Host probably offline, now retrying...')
            tries += 1
            sleep(2)
            connect(ip, port)

        else:
            print('Retried 10 times, no response. Quitting...')
            exit(1)


def login():
    global c
    print('Receiving!')
    sec = json.loads(c.recv(BUFSIZE).decode())
    print('Received!')
    key = Fernet(sec['sec'].encode())
    c.sendall(key.encrypt(json.dumps({'username': input('Username: '), 'password': getpass.getpass()}).encode()))
    print(f"\n{c.recv(BUFSIZE).decode()}\n")


def await_commands():
    command_list = eval(c.recv(BUFSIZE).decode())
    print(f"Available commands: {command_list}")
    choice = int(input('Choose one: '))
    c.sendall(command_list[choice].encode())


if __name__ == '__main__':
    connect('localhost', 585)
