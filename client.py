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
        print('Successful!')
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
    sec = json.loads(c.recv(BUFSIZE).decode())
    key = Fernet(sec['sec'].encode())
    c.sendall(key.encrypt(json.dumps({'username': input('Username: '), 'password': getpass.getpass()}).encode()))
    print(f"\n{c.recv(BUFSIZE).decode()}\n")
    await_commands()


def await_commands():
    command_list = eval(c.recv(BUFSIZE).decode())
    print(f"Available commands: {command_list}")
    choice = int(input('Choose one: '))
    try:
        c.sendall(command_list[choice - 1].encode())
    except IndexError:
        print('Index out of list!')
    form = json.loads(c.recv(BUFSIZE).decode())
    # Make it better, support group-chats add offline message queue for when message is sent but user not online.
    match form['mode']:
        case 'send':
            form['recipient'] = input('Recipient: ')
            form['message'] = input('Message: ')
            c.sendall(json.dumps(form).encode())
        case 'read':
            message = json.loads(c.recv(BUFSIZE).decode())
            print(f"From {message['recipient']} Message: {message['message']}")


if __name__ == '__main__':
    connect('localhost', 585)
