from socket import socket
from typing import Final

c = socket()
BUFSIZE: Final[int] = 8192


def code_to_str(code: int) -> None:
    '''Converts http code to letters.'''
    if code == 200: print('Successfully set up server!')
    else: print('Error!')

def connect(ip: str, port: int):
    global c
    print('Testing socket...')
    test_sock = socket()
    test_sock.bind(('127.0.0.1', 6005))
    test_sock.listen()
    c.connect(('127.0.0.1', 6005))
    c.sendall(('200').encode())
    data = test_sock.recv(BUFSIZE).decode()
    code_to_str(int(data))
    test_sock.close()
    print('Error occurred! Exiting...')
    exit(1)
    c.connect(ip, port)

def login():
    global c


if __name__ == '__main__':
    connect('localhost', 585)