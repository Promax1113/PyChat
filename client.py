import getpass
import json
import socket
from time import sleep
from typing import Final

from fernet import Fernet

c = socket.socket(socket.AF_INET, proto=socket.IPPROTO_TCP)
BUFSIZE: Final[int] = 4096


def receive(decode: bool = True):
    """
    This function is used to receive data.
    It takes one arg.
        - Decode -> defaults to True
    """
    global c
    data = c.recv(BUFSIZE)
    old_data = data
    

    if decode is True:
        return data.decode()
    else:
        return data


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
    sec = json.loads(receive())
    key = Fernet(sec['sec'].encode())
    c.sendall(key.encrypt(json.dumps({'username': input('Username: '), 'password': getpass.getpass()}).encode()))
    status = receive()
    if status == "Error":
        exit(1)
    print(f"\n{status}\n")
    await_commands()


def await_commands():

    command_list = eval(receive())

    print(f"Available commands")
    index = 1
    for  item in command_list:
        print(f"{index}. {item}")
        index += 1
    choice = int(input('Choose one: '))
    try:
        c.sendall(command_list[choice - 1].encode())
    except IndexError:
        print('Index out of list!')
    act_form = receive()
    form = json.loads(act_form)
    # Make it better, support group-chats add offline message queue for when message is sent but user not online.
    match form['mode']:
        case 'send':
            form['recipient'] = input('Recipient: ')
            form['message'] = input('Message: ')
            c.sendall(json.dumps(form).encode())
        case 'read':
            data = ''
            while not data:
                data = receive()
                print(data)

            message = json.loads(data)
            print(f"From user: {message['recipient']} Message: {message['message']}")


if __name__ == '__main__':
    connect('localhost', 585)
    while True:
        await_commands()