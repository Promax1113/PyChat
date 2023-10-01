import socket, json, getpass
from fernet import Fernet
from typing import Final
from time import sleep

c = socket.socket()
BUFSIZE: Final[int] = 8192

def receive():
    pass
def send():
    pass


def code_to_str(code: int) -> None:
    '''Converts http code to letters.'''
    if code == 200: print('Successfully set up server!')
    else: print('Error!')

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
    print('Received!')
    key = Fernet(sec['sec'].encode())
    c.sendall(key.encrypt(json.dumps({'username': input('Username: '), 'password': getpass.getpass()}).encode()))
    print(f"\n{c.recv(BUFSIZE).decode()}\n")



if __name__ == '__main__':
    connect('localhost', 585)